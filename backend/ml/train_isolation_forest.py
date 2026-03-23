"""
CIPHER-FLOW ANALYTICS — Isolation Forest Anomaly Detector Training
"""
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import logging

from config import settings

logger = logging.getLogger(__name__)


def train_isolation_forest(
    X_train_benign: np.ndarray,
    contamination: float = 0.05,
    n_estimators: int = 200,
    max_samples: str | int = "auto",
    n_jobs: int = -1,
) -> IsolationForest:
    """
    Train Isolation Forest on benign-only data.
    Anomaly detection: anything deviating from benign baseline is anomalous.
    """
    logger.info("Training Isolation Forest (n_estimators=%d) …", n_estimators)

    iso = IsolationForest(
        n_estimators=n_estimators,
        contamination=contamination,
        max_samples=max_samples,
        random_state=42,
        n_jobs=n_jobs,
    )

    iso.fit(X_train_benign)

    # Score training set
    scores = iso.decision_function(X_train_benign)
    logger.info(
        "Benign anomaly scores — mean: %.4f, std: %.4f, min: %.4f",
        scores.mean(), scores.std(), scores.min(),
    )

    joblib.dump(iso, settings.IF_MODEL_PATH)
    logger.info("Isolation Forest saved → %s", settings.IF_MODEL_PATH)

    return iso