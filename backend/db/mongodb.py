"""
CIPHER-FLOW ANALYTICS — MongoDB Connection (async with Motor)
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import settings

logger = logging.getLogger(__name__)

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


async def connect_db():
    """Initialize MongoDB connection."""
    global _client, _db
    _client = AsyncIOMotorClient(settings.MONGO_URI)
    _db = _client[settings.MONGO_DB]
    # Verify connection
    await _client.admin.command("ping")
    logger.info("MongoDB connected: %s / %s", settings.MONGO_URI, settings.MONGO_DB)

    # Create indexes
    await _db.alerts.create_index("timestamp")
    await _db.alerts.create_index("severity")
    await _db.flows.create_index("timestamp")


async def close_db():
    """Close MongoDB connection."""
    global _client
    if _client:
        _client.close()
        logger.info("MongoDB connection closed")


def get_db() -> AsyncIOMotorDatabase:
    """Return the database instance."""
    if _db is None:
        raise RuntimeError("Database not initialized — call connect_db() first")
    return _db


async def insert_alert(alert_data: dict):
    db = get_db()
    await db.alerts.insert_one(alert_data)


async def insert_flow(flow_data: dict):
    db = get_db()
    await db.flows.insert_one(flow_data)


async def get_recent_alerts(limit: int = 50) -> list:
    db = get_db()
    cursor = db.alerts.find(
        {}, {"_id": 0}
    ).sort("timestamp", -1).limit(limit)
    return await cursor.to_list(length=limit)


async def get_alert_counts() -> dict:
    db = get_db()
    pipeline = [
        {"$group": {"_id": "$severity", "count": {"$sum": 1}}}
    ]
    results = {}
    async for doc in db.alerts.aggregate(pipeline):
        results[doc["_id"]] = doc["count"]
    return results


async def get_total_alerts() -> int:
    db = get_db()
    return await db.alerts.count_documents({})


async def get_avg_anomaly_score() -> float:
    db = get_db()
    pipeline = [
        {"$group": {"_id": None, "avg": {"$avg": "$if_anomaly_score"}}}
    ]
    async for doc in db.alerts.aggregate(pipeline):
        return doc.get("avg", 0.0)
    return 0.0


async def get_classification_distribution() -> dict:
    db = get_db()
    pipeline = [
        {"$group": {"_id": "$final_label", "count": {"$sum": 1}}}
    ]
    results = {}
    async for doc in db.alerts.aggregate(pipeline):
        results[doc["_id"]] = doc["count"]
    return results