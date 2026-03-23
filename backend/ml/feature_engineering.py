"""
CIPHER-FLOW ANALYTICS — Feature Engineering
Adds derived features: byte ratio, packet ratio, entropy estimate.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import logging

from config import settings

logger = logging.getLogger(__name__)


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute ratio and entropy features from base flow statistics."""
    df = df.copy()

    # Byte ratio  (fwd / total)
    total_bytes = (
        df.get("total_length_fwd_packets", 0)
        + df.get("total_length_bwd_packets", 0)
    )
    df["byte_ratio"] = np.where(
        total_bytes > 0,
        df.get("total_length_fwd_packets", 0) / (total_bytes + 1e-9),
        0.5,
    )

    # Packet ratio  (fwd / total)
    total_pkts = (
        df.get("total_fwd_packets", 0) + df.get("total_bwd_packets", 0)
    )
    df["packet_ratio"] = np.where(
        total_pkts > 0,
        df.get("total_fwd_packets", 0) / (total_pkts + 1e-9),
        0.5,
    )

    # Entropy estimate from packet length variance
    pkt_var = df.get("packet_length_variance", pd.Series(dtype=float))
    df["entropy_estimate"] = np.log1p(pkt_var.clip(lower=0))

    return df


def fit_scaler(X_train: np.ndarray) -> StandardScaler:
    """Fit StandardScaler and persist to disk."""
    scaler = StandardScaler()
    scaler.fit(X_train)
    joblib.dump(scaler, settings.SCALER_PATH)
    logger.info("Scaler fitted and saved to %s", settings.SCALER_PATH)
    return scaler


def transform(X: np.ndarray, scaler: StandardScaler | None = None) -> np.ndarray:
    """Apply scaling. Loads persisted scaler if not provided."""
    if scaler is None:
        scaler = joblib.load(settings.SCALER_PATH)
    return scaler.transform(X)