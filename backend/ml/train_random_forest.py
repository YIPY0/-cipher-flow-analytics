"""
CIPHER-FLOW ANALYTICS — Random Forest Classifier Training
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import joblib
import logging

from config import settings

logger = logging.getLogger(__name__)


def train_random_forest(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    n_estimators: int = 200,
    max_depth: int | None = 30,
    min_samples_split: int = 5,
    min_samples_leaf: int = 2,
    n_jobs: int = -1,
) -> RandomForestClassifier:
    """
    Train Random Forest with cross-validation.
    Returns the fitted model.
    """
    logger.info("Training Random Forest (n_estimators=%d) …", n_estimators)

    rf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        class_weight="balanced",
        random_state=42,
        n_jobs=n_jobs,
    )

    # Cross-validation on training set
    cv_scores = cross_val_score(
        rf, X_train, y_train, cv=5, scoring="f1_weighted", n_jobs=n_jobs
    )
    logger.info(
        "5-Fold CV F1 (weighted): %.4f ± %.4f",
        cv_scores.mean(), cv_scores.std(),
    )

    # Fit on full training set
    rf.fit(X_train, y_train)

    # Validation accuracy
    val_acc = rf.score(X_val, y_val)
    logger.info("Validation Accuracy: %.4f", val_acc)

    # Save model
    joblib.dump(rf, settings.RF_MODEL_PATH)
    logger.info("Random Forest saved → %s", settings.RF_MODEL_PATH)

    return rf