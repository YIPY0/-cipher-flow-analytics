"""
CIPHER-FLOW ANALYTICS — Model Evaluation
Confusion matrix, classification report, ROC curves.
"""
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
)
from sklearn.preprocessing import label_binarize
import joblib
import logging

from config import settings

logger = logging.getLogger(__name__)


def evaluate_model(
    model, X_test: np.ndarray, y_test: np.ndarray, label_encoder=None
) -> dict:
    """Comprehensive evaluation of a classifier."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test) if hasattr(model, "predict_proba") else None

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    cm = confusion_matrix(y_test, y_pred).tolist()

    # Per-class metrics
    if label_encoder is not None:
        target_names = list(label_encoder.classes_)
    else:
        target_names = [str(i) for i in sorted(np.unique(y_test))]

    report = classification_report(
        y_test, y_pred, target_names=target_names, output_dict=True, zero_division=0
    )

    # ROC AUC (one-vs-rest, if multiclass)
    roc_auc = None
    if y_proba is not None:
        n_classes = len(np.unique(y_test))
        if n_classes == 2:
            roc_auc = float(roc_auc_score(y_test, y_proba[:, 1]))
        else:
            y_bin = label_binarize(y_test, classes=list(range(n_classes)))
            try:
                roc_auc = float(
                    roc_auc_score(y_bin, y_proba, average="weighted", multi_class="ovr")
                )
            except ValueError:
                roc_auc = None

    metrics = {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1),
        "roc_auc": roc_auc,
        "confusion_matrix": cm,
        "classification_report": report,
        "class_names": target_names,
    }

    # Save metrics
    joblib.dump(metrics, settings.METRICS_PATH)

    logger.info("Accuracy: %.4f | Precision: %.4f | Recall: %.4f | F1: %.4f",
                acc, prec, rec, f1)
    if roc_auc:
        logger.info("ROC AUC: %.4f", roc_auc)

    return metrics