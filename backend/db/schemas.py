"""
CIPHER-FLOW ANALYTICS — Pydantic Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AlertRecord(BaseModel):
    timestamp: datetime
    severity: str
    final_label: str
    rf_label: str
    rf_confidence: float
    if_anomaly_score: float
    if_is_anomaly: bool
    src_ip: str = ""
    dst_ip: str = ""
    src_port: int = 0
    dst_port: int = 0
    protocol: int = 0
    top_features: list[dict] = []
    rf_probabilities: dict = {}


class FlowRecordSchema(BaseModel):
    timestamp: datetime
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: int
    features: dict
    prediction: dict


class ModelMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: Optional[float] = None
    confusion_matrix: list = []
    class_names: list[str] = []
    classification_report: dict = {}


class LiveStats(BaseModel):
    total_packets: int = 0
    encrypted_sessions: int = 0
    active_flows: int = 0
    total_alerts: int = 0
    critical_alerts: int = 0
    suspicious_sessions: int = 0
    avg_anomaly_score: float = 0.0