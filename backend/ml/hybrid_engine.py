"""
CIPHER-FLOW ANALYTICS — Hybrid Decision Engine
Combines Random Forest classification + Isolation Forest anomaly detection.
"""
import numpy as np
import joblib
import logging
from datetime import datetime, timezone

from config import settings

logger = logging.getLogger(__name__)


class HybridEngine:
    """
    Two-layer detection:
      Layer 1 — Random Forest supervised classification
      Layer 2 — Isolation Forest unsupervised anomaly detection
      Fusion  — Combined severity assessment
    """

    SEVERITY_LEVELS = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]

    def __init__(self):
        self.rf = None
        self.iso = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = None
        self._loaded = False

    def load_models(self):
        """Load all persisted models and artifacts."""
        try:
            self.rf = joblib.load(settings.RF_MODEL_PATH)
            self.iso = joblib.load(settings.IF_MODEL_PATH)
            self.scaler = joblib.load(settings.SCALER_PATH)
            self.label_encoder = joblib.load(settings.LABEL_ENCODER_PATH)
            self.feature_names = joblib.load(settings.FEATURE_LIST_PATH)
            self._loaded = True
            logger.info("Hybrid engine: all models loaded successfully")
        except FileNotFoundError as e:
            logger.error("Model file missing: %s — run training first", e)
            self._loaded = False

    @property
    def is_ready(self) -> bool:
        return self._loaded

    def predict(self, features: np.ndarray) -> dict:
        """
        Run both models on a single feature vector (1D or 2D).
        Returns a comprehensive prediction result dict.
        """
        if not self._loaded:
            raise RuntimeError("Models not loaded — call load_models() first")

        if features.ndim == 1:
            features = features.reshape(1, -1)

        # Scale
        X_scaled = self.scaler.transform(features)

        # ── Layer 1: Random Forest ───────────────────────────────
        rf_proba = self.rf.predict_proba(X_scaled)[0]
        rf_pred_idx = np.argmax(rf_proba)
        rf_confidence = float(rf_proba[rf_pred_idx])
        rf_label = self.label_encoder.inverse_transform([rf_pred_idx])[0]

        # ── Layer 2: Isolation Forest ────────────────────────────
        if_score = float(self.iso.decision_function(X_scaled)[0])
        if_prediction = int(self.iso.predict(X_scaled)[0])  # 1=normal, -1=anomaly

        # ── Fusion Logic ─────────────────────────────────────────
        is_rf_malicious = rf_label != "benign"
        is_if_anomaly = if_score < settings.IF_ANOMALY_THRESHOLD

        if is_rf_malicious and is_if_anomaly:
            severity = "CRITICAL"
            final_label = rf_label
        elif is_rf_malicious and rf_confidence >= settings.RF_CONFIDENCE_HIGH:
            severity = "HIGH"
            final_label = rf_label
        elif is_if_anomaly and not is_rf_malicious:
            severity = "MEDIUM"
            final_label = "anomaly"
        elif is_rf_malicious and rf_confidence < settings.RF_CONFIDENCE_HIGH:
            severity = "LOW"
            final_label = rf_label
        else:
            severity = "INFO"
            final_label = "benign"

        # Build probability distribution
        class_probs = {
            self.label_encoder.inverse_transform([i])[0]: float(p)
            for i, p in enumerate(rf_proba)
        }

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "rf_label": rf_label,
            "rf_confidence": rf_confidence,
            "rf_probabilities": class_probs,
            "if_anomaly_score": if_score,
            "if_is_anomaly": if_prediction == -1,
            "severity": severity,
            "final_label": final_label,
        }

    def predict_batch(self, features: np.ndarray) -> list[dict]:
        """Run prediction on multiple samples."""
        results = []
        for i in range(features.shape[0]):
            results.append(self.predict(features[i]))
        return results