"""
CIPHER-FLOW ANALYTICS — SHAP Explainability
Provides per-prediction feature contribution explanations.
"""
import numpy as np
import shap
import joblib
import logging

from config import settings

logger = logging.getLogger(__name__)


class ShapExplainer:
    """Wraps SHAP TreeExplainer for Random Forest."""

    def __init__(self):
        self.explainer = None
        self.feature_names = None
        self._ready = False

    def initialize(self, rf_model=None, feature_names: list[str] | None = None):
        """Create SHAP TreeExplainer from fitted Random Forest."""
        if rf_model is None:
            rf_model = joblib.load(settings.RF_MODEL_PATH)
        if feature_names is None:
            feature_names = joblib.load(settings.FEATURE_LIST_PATH)

        self.feature_names = feature_names
        self.explainer = shap.TreeExplainer(rf_model)
        self._ready = True
        logger.info("SHAP TreeExplainer initialized with %d features", len(feature_names))

    @property
    def is_ready(self) -> bool:
        return self._ready

    def explain(
        self, X_scaled: np.ndarray, predicted_class_idx: int, top_n: int = 10
    ) -> dict:
        """
        Explain a single prediction.
        Returns top contributing features with SHAP values.
        """
        if not self._ready:
            raise RuntimeError("SHAP explainer not initialized")

        if X_scaled.ndim == 1:
            X_scaled = X_scaled.reshape(1, -1)

        shap_values = self.explainer.shap_values(X_scaled)

        # shap_values is list of arrays (one per class) for RF
        if isinstance(shap_values, list):
            class_shap = shap_values[predicted_class_idx][0]
        else:
            class_shap = shap_values[0]

        # Flatten to 1D if needed
        class_shap = np.array(class_shap).flatten()

        # Get top N features by absolute SHAP value
        abs_shap = np.abs(class_shap)
        top_indices = np.argsort(abs_shap)[-top_n:][::-1]

        contributions = []
        for i in range(len(top_indices)):
            idx = int(top_indices[i])
            contributions.append({
                "feature": self.feature_names[idx] if idx < len(self.feature_names) else f"feature_{idx}",
                "shap_value": float(class_shap[idx]),
                "abs_shap": float(abs_shap[idx]),
                "feature_value": float(X_scaled[0, idx]) if idx < X_scaled.shape[1] else 0.0,
            })

        base_value = (
            self.explainer.expected_value[predicted_class_idx]
            if isinstance(self.explainer.expected_value, (list, np.ndarray))
            else float(self.explainer.expected_value)
        )

        return {
            "base_value": float(base_value),
            "predicted_class_idx": predicted_class_idx,
            "top_contributions": contributions,
            "all_shap_values": class_shap.tolist(),
        }

    def global_importance(self, X_sample: np.ndarray, top_n: int = 15) -> list[dict]:
        """Compute global feature importance from SHAP on a sample."""
        if not self._ready:
            raise RuntimeError("SHAP explainer not initialized")

        shap_values = self.explainer.shap_values(X_sample)

        if isinstance(shap_values, list):
            # Average absolute SHAP across all classes
            all_abs = []
            for sv in shap_values:
                all_abs.append(np.abs(sv).mean(axis=0))
            mean_abs = np.mean(all_abs, axis=0)
        else:
            mean_abs = np.abs(shap_values).mean(axis=0)

        # Flatten to 1D if needed
        mean_abs = np.array(mean_abs).flatten()

        top_indices = np.argsort(mean_abs)[-top_n:][::-1]
        importance = []
        for i in range(len(top_indices)):
            idx = int(top_indices[i])
            feat_name = self.feature_names[idx] if idx < len(self.feature_names) else f"feature_{idx}"
            importance.append({
                "feature": feat_name,
                "importance": float(mean_abs[idx]),
            })

        return importance