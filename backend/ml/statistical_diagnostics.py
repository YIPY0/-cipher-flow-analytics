"""
CIPHER-FLOW ANALYTICS — Statistical Diagnostics
VIF analysis, correlation matrix, feature selection pipeline.
"""
import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
import logging

logger = logging.getLogger(__name__)


def compute_vif(X: np.ndarray, feature_names: list[str]) -> pd.DataFrame:
    """
    Compute Variance Inflation Factor for each feature.
    VIF > 10 indicates severe multicollinearity.
    """
    df = pd.DataFrame(X, columns=feature_names)

    # Remove zero-variance columns first
    df = df.loc[:, df.std() > 1e-10]
    remaining = list(df.columns)

    vif_data = []
    for i, col in enumerate(remaining):
        try:
            vif_val = variance_inflation_factor(df.values, i)
        except Exception:
            vif_val = np.inf
        vif_data.append({"feature": col, "vif": vif_val})

    vif_df = pd.DataFrame(vif_data).sort_values("vif", ascending=False)
    logger.info("VIF Analysis:\n%s", vif_df.head(20).to_string())
    return vif_df


def compute_correlation_matrix(
    X: np.ndarray, feature_names: list[str]
) -> pd.DataFrame:
    """Return Pearson correlation matrix."""
    df = pd.DataFrame(X, columns=feature_names)
    corr = df.corr(method="pearson")
    return corr


def find_highly_correlated(
    corr_matrix: pd.DataFrame, threshold: float = 0.95
) -> list[str]:
    """Identify features with correlation above threshold for removal."""
    upper = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )
    to_drop = [
        col for col in upper.columns if any(upper[col].abs() > threshold)
    ]
    logger.info(
        "Features with |correlation| > %.2f: %s", threshold, to_drop
    )
    return to_drop


def feature_selection_pipeline(
    X: np.ndarray,
    feature_names: list[str],
    vif_threshold: float = 10.0,
    corr_threshold: float = 0.95,
) -> tuple[np.ndarray, list[str], dict]:
    """
    Full statistical feature selection:
    1. Remove highly correlated features
    2. Iteratively remove high-VIF features
    Returns cleaned X, remaining feature names, and diagnostics dict.
    """
    diagnostics = {}
    df = pd.DataFrame(X, columns=feature_names)

    # ── Step 1: Correlation-based removal ────────────────────────
    corr = compute_correlation_matrix(X, feature_names)
    corr_drops = find_highly_correlated(corr, corr_threshold)
    df = df.drop(columns=[c for c in corr_drops if c in df.columns])
    diagnostics["correlation_removed"] = corr_drops

    # ── Step 2: Iterative VIF-based removal ──────────────────────
    vif_removed = []
    max_iter = 20
    for _ in range(max_iter):
        cols = list(df.columns)
        if len(cols) < 3:
            break
        vif_df = compute_vif(df.values, cols)
        worst = vif_df.iloc[0]
        if worst["vif"] <= vif_threshold or np.isinf(worst["vif"]):
            break
        logger.info(
            "Removing %s (VIF=%.2f)", worst["feature"], worst["vif"]
        )
        vif_removed.append(worst["feature"])
        df = df.drop(columns=[worst["feature"]])

    diagnostics["vif_removed"] = vif_removed
    diagnostics["final_vif"] = compute_vif(
        df.values, list(df.columns)
    ).to_dict("records")
    diagnostics["remaining_features"] = list(df.columns)
    diagnostics["correlation_matrix"] = compute_correlation_matrix(
        df.values, list(df.columns)
    ).to_dict()

    logger.info(
        "Feature selection: %d → %d features",
        len(feature_names), len(df.columns),
    )

    return df.values, list(df.columns), diagnostics