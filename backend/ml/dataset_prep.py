"""
CIPHER-FLOW ANALYTICS — Dataset Preparation
Handles CIC-IDS2017 loading and synthetic data generation for testing.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import logging
import joblib

from config import settings

logger = logging.getLogger(__name__)

# ── Features selected for encrypted traffic analysis ─────────────
SELECTED_FEATURES = [
    "flow_duration",
    "total_fwd_packets",
    "total_bwd_packets",
    "total_length_fwd_packets",
    "total_length_bwd_packets",
    "fwd_packet_length_max",
    "fwd_packet_length_min",
    "fwd_packet_length_mean",
    "fwd_packet_length_std",
    "bwd_packet_length_max",
    "bwd_packet_length_min",
    "bwd_packet_length_mean",
    "bwd_packet_length_std",
    "flow_bytes_per_s",
    "flow_packets_per_s",
    "flow_iat_mean",
    "flow_iat_std",
    "flow_iat_max",
    "flow_iat_min",
    "fwd_iat_total",
    "fwd_iat_mean",
    "fwd_iat_std",
    "fwd_iat_max",
    "fwd_iat_min",
    "bwd_iat_total",
    "bwd_iat_mean",
    "bwd_iat_std",
    "bwd_iat_max",
    "bwd_iat_min",
    "fwd_psh_flags",
    "fwd_header_length",
    "bwd_header_length",
    "fwd_packets_per_s",
    "bwd_packets_per_s",
    "min_packet_length",
    "max_packet_length",
    "packet_length_mean",
    "packet_length_std",
    "packet_length_variance",
    "fin_flag_count",
    "syn_flag_count",
    "rst_flag_count",
    "psh_flag_count",
    "ack_flag_count",
    "average_packet_size",
    "avg_fwd_segment_size",
    "avg_bwd_segment_size",
    "init_win_bytes_forward",
    "init_win_bytes_backward",
    "active_mean",
    "active_std",
    "idle_mean",
    "idle_std",
]

# Column mapping: CIC-IDS2017 original → our internal names
CIC_COLUMN_MAP = {
    "Flow Duration": "flow_duration",
    "Total Fwd Packets": "total_fwd_packets",
    "Total Backward Packets": "total_bwd_packets",
    "Total Length of Fwd Packets": "total_length_fwd_packets",
    "Total Length of Bwd Packets": "total_length_bwd_packets",
    "Fwd Packet Length Max": "fwd_packet_length_max",
    "Fwd Packet Length Min": "fwd_packet_length_min",
    "Fwd Packet Length Mean": "fwd_packet_length_mean",
    "Fwd Packet Length Std": "fwd_packet_length_std",
    "Bwd Packet Length Max": "bwd_packet_length_max",
    "Bwd Packet Length Min": "bwd_packet_length_min",
    "Bwd Packet Length Mean": "bwd_packet_length_mean",
    "Bwd Packet Length Std": "bwd_packet_length_std",
    "Flow Bytes/s": "flow_bytes_per_s",
    "Flow Packets/s": "flow_packets_per_s",
    "Flow IAT Mean": "flow_iat_mean",
    "Flow IAT Std": "flow_iat_std",
    "Flow IAT Max": "flow_iat_max",
    "Flow IAT Min": "flow_iat_min",
    "Fwd IAT Total": "fwd_iat_total",
    "Fwd IAT Mean": "fwd_iat_mean",
    "Fwd IAT Std": "fwd_iat_std",
    "Fwd IAT Max": "fwd_iat_max",
    "Fwd IAT Min": "fwd_iat_min",
    "Bwd IAT Total": "bwd_iat_total",
    "Bwd IAT Mean": "bwd_iat_mean",
    "Bwd IAT Std": "bwd_iat_std",
    "Bwd IAT Max": "bwd_iat_max",
    "Bwd IAT Min": "bwd_iat_min",
    "Fwd PSH Flags": "fwd_psh_flags",
    "Fwd Header Length": "fwd_header_length",
    "Bwd Header Length": "bwd_header_length",
    "Fwd Packets/s": "fwd_packets_per_s",
    "Bwd Packets/s": "bwd_packets_per_s",
    "Min Packet Length": "min_packet_length",
    "Max Packet Length": "max_packet_length",
    "Packet Length Mean": "packet_length_mean",
    "Packet Length Std": "packet_length_std",
    "Packet Length Variance": "packet_length_variance",
    "FIN Flag Count": "fin_flag_count",
    "SYN Flag Count": "syn_flag_count",
    "RST Flag Count": "rst_flag_count",
    "PSH Flag Count": "psh_flag_count",
    "ACK Flag Count": "ack_flag_count",
    "Average Packet Size": "average_packet_size",
    "Avg Fwd Segment Size": "avg_fwd_segment_size",
    "Avg Bwd Segment Size": "avg_bwd_segment_size",
    "Init_Win_bytes_forward": "init_win_bytes_forward",
    "Init_Win_bytes_backward": "init_win_bytes_backward",
    "Active Mean": "active_mean",
    "Active Std": "active_std",
    "Idle Mean": "idle_mean",
    "Idle Std": "idle_std",
    "Label": "label",
}


def load_cic_ids2017(dataset_dir: Path | None = None) -> pd.DataFrame:
    """Load and concatenate all CIC-IDS2017 CSV files."""
    data_dir = dataset_dir or settings.DATASET_DIR
    csv_files = list(data_dir.glob("*.csv"))

    if not csv_files:
        logger.warning("No CIC-IDS2017 CSV files found in %s", data_dir)
        return pd.DataFrame()

    frames = []
    for f in csv_files:
        logger.info("Loading %s …", f.name)
        df = pd.read_csv(f, encoding="utf-8", low_memory=False, on_bad_lines='skip', encoding_errors='ignore')
        # Strip leading/trailing whitespace from column names
        df.columns = df.columns.str.strip()
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    logger.info("Total records loaded: %d", len(combined))
    return combined


def map_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename CIC-IDS2017 columns to internal feature names."""
    rename_dict = {}
    for orig, internal in CIC_COLUMN_MAP.items():
        matches = [c for c in df.columns if c.strip() == orig]
        if matches:
            rename_dict[matches[0]] = internal
    df = df.rename(columns=rename_dict)
    return df


def map_labels(df):
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Check for common label column variations
    label_variations = ['label', 'Label', ' Label', 'class', 'attack', 'category']
    label_col = None
    
    for col in df.columns:
        if any(var in col for var in label_variations):
            label_col = col
            break
    
    if label_col and label_col != 'label':
        df.rename(columns={label_col: 'label'}, inplace=True)
    
    if 'label' not in df.columns:
        print("Available columns:", df.columns.tolist())
        raise ValueError("'label' column not found after column mapping")
    df["label"] = df["label"].map(
        lambda x: settings.LABEL_MAP.get(x.strip(), "suspicious")
    )
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates, infinities, NaNs; ensure numeric types."""
    initial = len(df)

    # Keep only selected features + label
    available = [f for f in SELECTED_FEATURES if f in df.columns]
    if "label" in df.columns:
        available.append("label")
    df = df[available].copy()

    # Convert to numeric (coerce errors to NaN)
    for col in available:
        if col != "label":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Replace infinity
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Drop NaN rows
    df.dropna(inplace=True)

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    logger.info(
        "Cleaning: %d → %d records (removed %d)",
        initial, len(df), initial - len(df),
    )
    return df.reset_index(drop=True)


def balance_classes(
    df: pd.DataFrame,
    max_per_class: int = 50000,
    min_per_class: int = 500,
) -> pd.DataFrame:
    """Balance classes via undersampling majority and oversampling minority."""
    counts = df["label"].value_counts()
    logger.info("Class distribution before balancing:\n%s", counts)

    frames = []
    for label, count in counts.items():
        subset = df[df["label"] == label]
        if count > max_per_class:
            subset = subset.sample(n=max_per_class, random_state=42)
        elif count < min_per_class:
            # Oversample via duplication with noise
            factor = min_per_class // count + 1
            subset = pd.concat([subset] * factor, ignore_index=True)
            subset = subset.head(min_per_class)
        frames.append(subset)

    balanced = pd.concat(frames, ignore_index=True).sample(
        frac=1, random_state=42
    ).reset_index(drop=True)

    logger.info(
        "Class distribution after balancing:\n%s",
        balanced["label"].value_counts(),
    )
    return balanced


def generate_synthetic_dataset(n_samples: int = 60000) -> pd.DataFrame:
    """
    Generate realistic synthetic encrypted traffic data for testing.
    Mimics statistical properties of CIC-IDS2017 features.
    """
    rng = np.random.RandomState(42)
    n_per = n_samples // 6

    def _benign(n):
        return {
            "flow_duration": rng.exponential(30_000_000, n),
            "total_fwd_packets": rng.poisson(15, n).astype(float),
            "total_bwd_packets": rng.poisson(12, n).astype(float),
            "total_length_fwd_packets": rng.exponential(3000, n),
            "total_length_bwd_packets": rng.exponential(5000, n),
            "fwd_packet_length_max": rng.uniform(100, 1460, n),
            "fwd_packet_length_min": rng.uniform(0, 100, n),
            "fwd_packet_length_mean": rng.uniform(50, 800, n),
            "fwd_packet_length_std": rng.uniform(10, 400, n),
            "bwd_packet_length_max": rng.uniform(100, 1460, n),
            "bwd_packet_length_min": rng.uniform(0, 100, n),
            "bwd_packet_length_mean": rng.uniform(50, 900, n),
            "bwd_packet_length_std": rng.uniform(10, 500, n),
            "flow_bytes_per_s": rng.exponential(50000, n),
            "flow_packets_per_s": rng.exponential(100, n),
            "flow_iat_mean": rng.exponential(500000, n),
            "flow_iat_std": rng.exponential(300000, n),
            "flow_iat_max": rng.exponential(2000000, n),
            "flow_iat_min": rng.uniform(0, 100000, n),
            "fwd_iat_total": rng.exponential(20000000, n),
            "fwd_iat_mean": rng.exponential(1000000, n),
            "fwd_iat_std": rng.exponential(800000, n),
            "fwd_iat_max": rng.exponential(5000000, n),
            "fwd_iat_min": rng.uniform(0, 200000, n),
            "bwd_iat_total": rng.exponential(20000000, n),
            "bwd_iat_mean": rng.exponential(1200000, n),
            "bwd_iat_std": rng.exponential(900000, n),
            "bwd_iat_max": rng.exponential(5000000, n),
            "bwd_iat_min": rng.uniform(0, 200000, n),
            "fwd_psh_flags": rng.binomial(1, 0.3, n).astype(float),
            "fwd_header_length": rng.uniform(20, 60, n),
            "bwd_header_length": rng.uniform(20, 60, n),
            "fwd_packets_per_s": rng.exponential(50, n),
            "bwd_packets_per_s": rng.exponential(40, n),
            "min_packet_length": rng.uniform(0, 60, n),
            "max_packet_length": rng.uniform(200, 1500, n),
            "packet_length_mean": rng.uniform(50, 800, n),
            "packet_length_std": rng.uniform(10, 500, n),
            "packet_length_variance": rng.uniform(100, 250000, n),
            "fin_flag_count": rng.binomial(2, 0.4, n).astype(float),
            "syn_flag_count": rng.binomial(1, 0.5, n).astype(float),
            "rst_flag_count": rng.binomial(1, 0.05, n).astype(float),
            "psh_flag_count": rng.binomial(3, 0.3, n).astype(float),
            "ack_flag_count": rng.binomial(4, 0.5, n).astype(float),
            "average_packet_size": rng.uniform(50, 800, n),
            "avg_fwd_segment_size": rng.uniform(50, 800, n),
            "avg_bwd_segment_size": rng.uniform(50, 900, n),
            "init_win_bytes_forward": rng.uniform(1000, 65535, n),
            "init_win_bytes_backward": rng.uniform(1000, 65535, n),
            "active_mean": rng.exponential(500000, n),
            "active_std": rng.exponential(200000, n),
            "idle_mean": rng.exponential(5000000, n),
            "idle_std": rng.exponential(3000000, n),
        }

    def _malware(n):
        base = _benign(n)
        base["flow_duration"] = rng.exponential(500000, n)
        base["total_fwd_packets"] = rng.poisson(200, n).astype(float)
        base["total_bwd_packets"] = rng.poisson(5, n).astype(float)
        base["flow_bytes_per_s"] = rng.exponential(500000, n)
        base["flow_packets_per_s"] = rng.exponential(2000, n)
        base["flow_iat_mean"] = rng.exponential(5000, n)
        base["flow_iat_std"] = rng.exponential(3000, n)
        base["fwd_packet_length_mean"] = rng.uniform(40, 200, n)
        base["syn_flag_count"] = rng.binomial(5, 0.6, n).astype(float)
        base["rst_flag_count"] = rng.binomial(3, 0.4, n).astype(float)
        return base

    def _suspicious(n):
        base = _benign(n)
        base["flow_duration"] = rng.exponential(2000000, n)
        base["total_fwd_packets"] = rng.poisson(50, n).astype(float)
        base["total_bwd_packets"] = rng.poisson(20, n).astype(float)
        base["fwd_packet_length_mean"] = rng.uniform(100, 500, n)
        base["flow_packets_per_s"] = rng.exponential(500, n)
        base["psh_flag_count"] = rng.binomial(5, 0.5, n).astype(float)
        return base

    def _exfiltration(n):
        base = _benign(n)
        base["flow_duration"] = rng.exponential(100000000, n)
        base["total_fwd_packets"] = rng.poisson(80, n).astype(float)
        base["total_bwd_packets"] = rng.poisson(5, n).astype(float)
        base["total_length_fwd_packets"] = rng.exponential(50000, n)
        base["total_length_bwd_packets"] = rng.exponential(500, n)
        base["fwd_packet_length_max"] = rng.uniform(1200, 1460, n)
        base["fwd_packet_length_mean"] = rng.uniform(600, 1400, n)
        base["flow_iat_mean"] = rng.exponential(2000000, n)
        base["flow_iat_std"] = rng.exponential(500000, n)
        return base

    def _botnet(n):
        base = _benign(n)
        base["flow_duration"] = rng.uniform(5000000, 60000000, n)
        base["total_fwd_packets"] = rng.poisson(8, n).astype(float)
        base["total_bwd_packets"] = rng.poisson(6, n).astype(float)
        base["fwd_packet_length_mean"] = rng.uniform(40, 150, n)
        base["flow_iat_mean"] = rng.uniform(4000000, 6000000, n)
        base["flow_iat_std"] = rng.uniform(100000, 500000, n)
        base["init_win_bytes_forward"] = rng.uniform(200, 2000, n)
        return base

    def _scanning(n):
        base = _benign(n)
        base["flow_duration"] = rng.exponential(50000, n)
        base["total_fwd_packets"] = rng.poisson(2, n).astype(float) + 1
        base["total_bwd_packets"] = rng.binomial(1, 0.3, n).astype(float)
        base["total_length_fwd_packets"] = rng.uniform(40, 100, n)
        base["total_length_bwd_packets"] = rng.uniform(0, 60, n)
        base["syn_flag_count"] = rng.binomial(2, 0.9, n).astype(float)
        base["rst_flag_count"] = rng.binomial(2, 0.6, n).astype(float)
        base["flow_packets_per_s"] = rng.exponential(5000, n)
        return base

    generators = {
        "benign": _benign,
        "malware": _malware,
        "suspicious": _suspicious,
        "exfiltration": _exfiltration,
        "botnet": _botnet,
        "scanning": _scanning,
    }

    frames = []
    for label, gen_fn in generators.items():
        data = gen_fn(n_per)
        df = pd.DataFrame(data)
        df["label"] = label
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True).sample(
        frac=1, random_state=42
    ).reset_index(drop=True)

    # Ensure no negatives in non-negative features
    for col in combined.select_dtypes(include=[np.number]).columns:
        combined[col] = combined[col].clip(lower=0)

    logger.info("Generated synthetic dataset with %d records", len(combined))
    return combined

def prepare_dataset(
    use_synthetic: bool = False,
    dataset_dir: Path | None = None,
    sample_size=None,
) -> dict:
    """
    Full preparation pipeline.
    Returns dict with X_train, X_val, X_test, y_train, y_val, y_test,
    label_encoder, feature_names.
    """
    if use_synthetic:
        logger.info("Using SYNTHETIC dataset for training")
        df = generate_synthetic_dataset(n_samples=60000)
    else:
        logger.info("Loading CIC-IDS2017 dataset")
        df = load_cic_ids2017(dataset_dir)
        if df.empty:
            logger.warning("Dataset empty — falling back to synthetic data")
            df = generate_synthetic_dataset(n_samples=60000)
        else:
            # SAMPLE EARLY before map_columns to save memory
            if sample_size is not None and len(df) > sample_size:
                logger.info(f"Sampling {sample_size} records from {len(df)} total (memory efficiency)")
                df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)

            df = map_columns(df)
            df = map_labels(df)

    df = clean_dataset(df)
    df = balance_classes(df)

    # Separate features and labels
    feature_cols = [c for c in SELECTED_FEATURES if c in df.columns]
    X = df[feature_cols].values
    y = df["label"].values

    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Split: 70% train, 15% validation, 15% test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y_encoded, test_size=0.15, random_state=42, stratify=y_encoded
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.176, random_state=42, stratify=y_temp
        # 0.176 of 85% ≈ 15% of total
    )

    # Save label encoder and feature list
    joblib.dump(le, settings.LABEL_ENCODER_PATH)
    joblib.dump(feature_cols, settings.FEATURE_LIST_PATH)

    logger.info(
        "Splits — Train: %d | Val: %d | Test: %d",
        len(X_train), len(X_val), len(X_test),
    )
    logger.info("Classes: %s", list(le.classes_))

    return {
        "X_train": X_train,
        "X_val": X_val,
        "X_test": X_test,
        "y_train": y_train,
        "y_val": y_val,
        "y_test": y_test,
        "label_encoder": le,
        "feature_names": feature_cols,
    }