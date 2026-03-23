"""
CIPHER-FLOW ANALYTICS — API Routes
"""
import numpy as np
from fastapi import APIRouter, Request, Query
from datetime import datetime, timedelta

router = APIRouter()


def get_state(request: Request):
    return request.app.state.app_state


@router.get("/health")
async def health(request: Request):
    s = get_state(request)
    uptime = 0
    if s["start_time"]:
        uptime = (datetime.utcnow() - s["start_time"]).total_seconds()
    return {
        "status": "healthy",
        "mongodb": s["db"] is not None,
        "models_loaded": s["rf_model"] is not None,
        "uptime_seconds": round(uptime, 1),
        "total_flows": s["total_flows"],
        "threats_detected": s["threats_detected"],
    }


@router.get("/stats")
async def get_stats(request: Request):
    s = get_state(request)
    db = s["db"]

    # Use in-memory counts as fallback
    total = s["total_flows"]
    threats = s["threats_detected"]
    categories = {}

    if db is not None:
        try:
            total = await db["flows"].count_documents({})
            threats = await db["flows"].count_documents({"is_threat": True})

            # Get threat categories
            pipeline = [
                {"$match": {"is_threat": True}},
                {"$group": {"_id": "$prediction", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
            async for doc in db["flows"].aggregate(pipeline):
                categories[doc["_id"]] = doc["count"]
        except Exception as e:
            print(f"Stats DB error: {e}")

    anomaly_rate = round((threats / total * 100), 2) if total > 0 else 0
    model_acc = s.get("model_metrics", {}).get("accuracy", 0.9969)

    return {
        "total_flows": total,
        "threats_detected": threats,
        "benign_flows": total - threats,
        "anomaly_rate": anomaly_rate,
        "flows_per_minute": round(total / max(1, (datetime.utcnow() - s["start_time"]).total_seconds() / 60), 1) if s["start_time"] else 0,
        "threat_categories": categories,
        "model_accuracy": model_acc,
    }


@router.get("/threats")
async def get_threats(
    request: Request,
    limit: int = Query(50, ge=1, le=500),
    severity: str = Query(None),
):
    s = get_state(request)
    db = s["db"]
    if db is None:
        return {"threats": [], "total": 0}

    try:
        query = {"is_threat": True}
        if severity and severity != "all":
            query["severity"] = severity

        cursor = db["flows"].find(query, {"_id": 0}).sort("timestamp", -1).limit(limit)
        threats = await cursor.to_list(length=limit)
        total = await db["flows"].count_documents(query)
        return {"threats": threats, "total": total}
    except Exception as e:
        print(f"Threats error: {e}")
        return {"threats": [], "total": 0}


@router.get("/flows")
async def get_flows(request: Request, limit: int = Query(100, ge=1, le=500)):
    s = get_state(request)
    db = s["db"]
    if db is None:
        return {"flows": [], "total": 0}

    try:
        cursor = db["flows"].find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
        flows = await cursor.to_list(length=limit)
        total = await db["flows"].count_documents({})
        return {"flows": flows, "total": total}
    except Exception as e:
        print(f"Flows error: {e}")
        return {"flows": [], "total": 0}


@router.get("/alerts")
async def get_alerts(request: Request, limit: int = Query(50, ge=1, le=500)):
    s = get_state(request)
    db = s["db"]
    if db is None:
        return {"alerts": [], "total": 0}

    try:
        cursor = db["alerts"].find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
        alerts = await cursor.to_list(length=limit)
        total = await db["alerts"].count_documents({})
        return {"alerts": alerts, "total": total}
    except Exception as e:
        print(f"Alerts error: {e}")
        return {"alerts": [], "total": 0}


@router.get("/model/performance")
async def model_performance(request: Request):
    s = get_state(request)
    metrics = s.get("model_metrics", {})
    classes = list(s["label_encoder"].classes_) if s.get("label_encoder") else []
    feature_names = s.get("feature_names", [])

    distribution = {}
    db = s["db"]
    if db is not None:
        try:
            pipeline = [
                {"$group": {"_id": "$prediction", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
            async for doc in db["flows"].aggregate(pipeline):
                distribution[doc["_id"]] = doc["count"]
        except Exception as e:
            print(f"Performance error: {e}")

    return {
        "metrics": metrics,
        "classes": classes,
        "feature_count": len(feature_names),
        "feature_names": feature_names,
        "prediction_distribution": distribution,
    }


@router.get("/shap/explain")
async def shap_explain(request: Request, flow_id: str = Query(None)):
    s = get_state(request)
    db = s["db"]

    if db is None or s.get("rf_model") is None:
        return {"error": "Models not loaded"}

    try:
        flow = None
        if flow_id:
            flow = await db["flows"].find_one({"flow_id": flow_id}, {"_id": 0})
        else:
            flow = await db["flows"].find_one(
                {"is_threat": True}, {"_id": 0}, sort=[("timestamp", -1)]
            )

        if flow is None or "features" not in flow:
            return {"error": "No flow found for explanation"}

        from ml.explainability import ShapExplainer

        explainer = ShapExplainer()
        explainer.initialize(s["rf_model"], s["feature_names"])

        feature_values = np.array(
            [flow["features"].get(f, 0) for f in s["feature_names"]]
        )
        feature_scaled = s["scaler"].transform(feature_values.reshape(1, -1))
        pred_idx = int(s["rf_model"].predict(feature_scaled)[0])
        explanation = explainer.explain(feature_scaled, pred_idx, top_n=10)

        return {
            "flow_id": flow["flow_id"],
            "prediction": flow["prediction"],
            "confidence": flow["confidence"],
            "explanation": explanation,
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/flow/timeline")
async def flow_timeline(request: Request, minutes: int = Query(30, ge=1, le=1440)):
    s = get_state(request)
    db = s["db"]
    if db is None:
        return {"timeline": []}

    try:
        since = (datetime.utcnow() - timedelta(minutes=minutes)).isoformat()
        cursor = (
            db["flows"]
            .find({"timestamp": {"$gte": since}}, {"_id": 0, "timestamp": 1, "is_threat": 1, "prediction": 1})
            .sort("timestamp", 1)
        )
        docs = await cursor.to_list(length=5000)

        buckets = {}
        for doc in docs:
            ts = doc["timestamp"][:16]
            if ts not in buckets:
                buckets[ts] = {"time": ts, "total": 0, "threats": 0, "benign": 0}
            buckets[ts]["total"] += 1
            if doc.get("is_threat"):
                buckets[ts]["threats"] += 1
            else:
                buckets[ts]["benign"] += 1

        timeline = sorted(buckets.values(), key=lambda x: x["time"])
        return {"timeline": timeline}
    except Exception as e:
        print(f"Timeline error: {e}")
        return {"timeline": []}