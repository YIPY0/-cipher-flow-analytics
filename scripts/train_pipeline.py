"""
CIPHER-FLOW ANALYTICS — Complete Training Pipeline
Run this ONCE before starting the system.

Usage:
    cd backend
    python -m scripts.train_pipeline [--synthetic]
"""
import sys
import os
import argparse
import logging
import numpy as np
import joblib

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import settings
from ml.dataset_prep import prepare_dataset, SELECTED_FEATURES
from ml.feature_engineering import fit_scaler, transform
from ml.statistical_diagnostics import (
    feature_selection_pipeline,
    compute_vif,
    compute_correlation_matrix,
)
from ml.train_random_forest import train_random_forest
from ml.train_isolation_forest import train_isolation_forest
from ml.evaluation import evaluate_model
from ml.explainability import ShapExplainer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("train_pipeline")


def main():
    parser = argparse.ArgumentParser(description="CIPHER-FLOW Training Pipeline")
    parser.add_argument(
        "--synthetic", action="store_true",
        help="Use synthetic dataset instead of CIC-IDS2017",
    )
    parser.add_argument(
        "--dataset-dir", type=str, default=None,
        help="Path to directory containing CIC-IDS2017 CSVs",
    )
    parser.add_argument(
        "--skip-vif", action="store_true",
        help="Skip VIF-based feature selection (faster)",
    )
    parser.add_argument(
        "--sample-size", type=int, default=200000,
        help="Number of records to sample (default: 200000 for memory efficiency)",
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("  CIPHER-FLOW ANALYTICS — Training Pipeline")
    logger.info("=" * 60)
    logger.info("  Sample size: %d records (memory-efficient mode)", args.sample_size)

    # ── Step 1: Dataset Preparation ──────────────────────────────
    logger.info("\n▶ STEP 1: Dataset Preparation")
    data = prepare_dataset(
        use_synthetic=args.synthetic,
        dataset_dir=args.dataset_dir,
        sample_size=args.sample_size,  # ← ADDED THIS
    )
    X_train = data["X_train"]
    X_val = data["X_val"]
    X_test = data["X_test"]
    y_train = data["y_train"]
    y_val = data["y_val"]
    y_test = data["y_test"]
    le = data["label_encoder"]
    feature_names = data["feature_names"]

    logger.info("Features: %d | Classes: %s", len(feature_names), list(le.classes_))

    # ── Step 2: Statistical Diagnostics ──────────────────────────
    logger.info("\n▶ STEP 2: Statistical Diagnostics")

    if not args.skip_vif:
        X_train_sel, selected_features, diagnostics = feature_selection_pipeline(
            X_train, feature_names, vif_threshold=10.0, corr_threshold=0.95,
        )

        # Update all splits to use selected features only
        selected_indices = [feature_names.index(f) for f in selected_features]
        X_train = X_train[:, selected_indices]
        X_val = X_val[:, selected_indices]
        X_test = X_test[:, selected_indices]
        feature_names = selected_features

        # Save updated feature list
        joblib.dump(feature_names, settings.FEATURE_LIST_PATH)

        logger.info("Features after selection: %d", len(feature_names))
        logger.info(
            "Removed (correlation): %s", diagnostics.get("correlation_removed", [])
        )
        logger.info(
            "Removed (VIF): %s", diagnostics.get("vif_removed", [])
        )
    else:
        logger.info("VIF selection skipped — using all %d features", len(feature_names))
        # Still compute VIF for reporting
        vif_df = compute_vif(X_train[:5000], feature_names)
        logger.info("Top VIF values:\n%s", vif_df.head(10).to_string())

    # ── Step 3: Feature Scaling ──────────────────────────────────
    logger.info("\n▶ STEP 3: Feature Scaling")
    scaler = fit_scaler(X_train)
    X_train_scaled = transform(X_train, scaler)
    X_val_scaled = transform(X_val, scaler)
    X_test_scaled = transform(X_test, scaler)

    # ── Step 4: Train Random Forest ──────────────────────────────
    logger.info("\n▶ STEP 4: Training Random Forest")
    rf = train_random_forest(
        X_train_scaled, y_train,
        X_val_scaled, y_val,
        n_estimators=200,
        max_depth=30,
    )

    # ── Step 5: Train Isolation Forest ───────────────────────────
    logger.info("\n▶ STEP 5: Training Isolation Forest")
    benign_idx = le.transform(["benign"])[0]
    benign_mask = y_train == benign_idx
    X_train_benign = X_train_scaled[benign_mask]
    logger.info("Benign samples for IF training: %d", len(X_train_benign))

    iso = train_isolation_forest(
        X_train_benign,
        contamination=0.05,
        n_estimators=200,
    )

    # ── Step 6: Evaluation ───────────────────────────────────────
    logger.info("\n▶ STEP 6: Model Evaluation")
    metrics = evaluate_model(rf, X_test_scaled, y_test, le)

    logger.info("\nClassification Report:")
    for cls_name, cls_metrics in metrics["classification_report"].items():
        if isinstance(cls_metrics, dict) and "f1-score" in cls_metrics:
            logger.info(
                "  %-15s  P=%.3f  R=%.3f  F1=%.3f  support=%d",
                cls_name,
                cls_metrics["precision"],
                cls_metrics["recall"],
                cls_metrics["f1-score"],
                int(cls_metrics.get("support", 0)),
            )

    # Test Isolation Forest on test set
    if_scores = iso.decision_function(X_test_scaled)
    if_preds = iso.predict(X_test_scaled)
    anomaly_rate = (if_preds == -1).mean()
    logger.info(
        "\nIsolation Forest — Anomaly rate on test set: %.2f%%",
        anomaly_rate * 100,
    )

    # ── Step 7: SHAP Explainability ──────────────────────────────
    logger.info("\n▶ STEP 7: SHAP Explainability Setup")
    shap_exp = ShapExplainer()
    shap_exp.initialize(rf, feature_names)

    # Compute global importance on a sample
    sample_size = min(500, len(X_test_scaled))
    global_imp = shap_exp.global_importance(X_test_scaled[:sample_size], top_n=15)
    logger.info("\nGlobal SHAP Feature Importance:")
    for item in global_imp:
        logger.info("  %-35s  %.6f", item["feature"], item["importance"])

    # ── Summary ──────────────────────────────────────────────────
    logger.info("\n" + "=" * 60)
    logger.info("  TRAINING COMPLETE")
    logger.info("=" * 60)
    logger.info("  Accuracy:  %.4f", metrics["accuracy"])
    logger.info("  Precision: %.4f", metrics["precision"])
    logger.info("  Recall:    %.4f", metrics["recall"])
    logger.info("  F1 Score:  %.4f", metrics["f1_score"])
    if metrics["roc_auc"]:
        logger.info("  ROC AUC:   %.4f", metrics["roc_auc"])
    logger.info("")
    logger.info("  Models saved to: %s", settings.MODELS_DIR)
    logger.info("  You can now start the backend with: python main.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()