"""
CIPHER-FLOW ANALYTICS — Central Configuration
"""
from pydantic_settings import BaseSettings
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    # ── Application ──────────────────────────────────────────────
    APP_NAME: str = "CIPHER-FLOW ANALYTICS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # ── Server ───────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── MongoDB ──────────────────────────────────────────────────
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "cipherflow"

    # ── Paths ────────────────────────────────────────────────────
    MODELS_DIR: Path = BASE_DIR / "models"
    DATA_DIR: Path = BASE_DIR / "data"
    DATASET_DIR: Path = BASE_DIR / "data" / "raw"

    # ── ML ───────────────────────────────────────────────────────
    RF_MODEL_PATH: Path = BASE_DIR / "models" / "random_forest.joblib"
    IF_MODEL_PATH: Path = BASE_DIR / "models" / "isolation_forest.joblib"
    SCALER_PATH: Path = BASE_DIR / "models" / "scaler.joblib"
    LABEL_ENCODER_PATH: Path = BASE_DIR / "models" / "label_encoder.joblib"
    FEATURE_LIST_PATH: Path = BASE_DIR / "models" / "feature_list.joblib"
    METRICS_PATH: Path = BASE_DIR / "models" / "metrics.joblib"
    SHAP_EXPLAINER_PATH: Path = BASE_DIR / "models" / "shap_explainer.joblib"

    # ── Capture ──────────────────────────────────────────────────
    CAPTURE_INTERFACE: str | None = None  # None = auto-detect
    FLOW_TIMEOUT: int = 120               # seconds
    FLOW_PACKET_THRESHOLD: int = 50       # packets before early export
    CAPTURE_BPF_FILTER: str = "tcp or udp"

    # ── Hybrid Engine Thresholds ─────────────────────────────────
    IF_ANOMALY_THRESHOLD: float = -0.3
    RF_CONFIDENCE_HIGH: float = 0.75
    RF_CONFIDENCE_LOW: float = 0.50

    # ── Categories ───────────────────────────────────────────────
    THREAT_CATEGORIES: list = [
        "benign", "malware", "suspicious",
        "exfiltration", "botnet", "scanning"
    ]

    LABEL_MAP: dict = {
        "BENIGN": "benign",
        "FTP-Patator": "suspicious",
        "SSH-Patator": "suspicious",
        "DoS slowloris": "malware",
        "DoS Slowhttptest": "malware",
        "DoS Hulk": "malware",
        "DoS GoldenEye": "malware",
        "Heartbleed": "malware",
        "Web Attack – Brute Force": "suspicious",
        "Web Attack – XSS": "suspicious",
        "Web Attack – Sql Injection": "suspicious",
        "Web Attack \x96 Brute Force": "suspicious",
        "Web Attack \x96 XSS": "suspicious",
        "Web Attack \x96 Sql Injection": "suspicious",
        "Infiltration": "exfiltration",
        "Bot": "botnet",
        "PortScan": "scanning",
        "DDoS": "malware",
    }

    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.DATASET_DIR.mkdir(parents=True, exist_ok=True)