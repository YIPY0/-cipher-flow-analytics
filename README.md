# 🔒 CipherFlow Analytics  
**Real-Time Network Intrusion Detection System with Explainable Machine Learning**

> **Academic Technical Project**  
> Production-oriented cybersecurity platform for live traffic monitoring, anomaly detection, and explainable intrusion analysis.

---

## 📌 Project Overview

**CipherFlow Analytics** is a technical cybersecurity project designed to detect malicious network behavior in real time using machine learning and packet-flow intelligence.

The system captures live traffic, converts packets into bidirectional flows, extracts statistical features, classifies threats using hybrid ML models, and presents live results through an interactive dashboard.

### Core Objectives
- Real-time packet capture from live interfaces  
- Flow-based intrusion detection  
- Hybrid ML classification for known + unknown threats  
- Explainable AI using SHAP  
- Web-based monitoring dashboard  
- Structured alert logging for analysis  

---

## 🧠 Technical Stack

### Backend
- Python  
- FastAPI  
- Scapy  
- PyShark  
- MongoDB  
- Scikit-learn  
- SHAP  

### Frontend
- React  
- Vite  
- Tailwind CSS  
- WebSocket Streaming  

### Machine Learning
- Random Forest  
- Isolation Forest  
- XGBoost  
- PCA + Feature Selection  
- SMOTE Balancing  

---

## 🏗️ System Workflow

```text
Network Traffic
     ↓
Packet Capture Layer
     ↓
5-Tuple Flow Aggregation
     ↓
Feature Extraction Engine
     ↓
ML Detection Engine
     ↓
SHAP Explainability
     ↓
Live Dashboard + Alert System
```

---

## 📂 Project Structure

```text
cipher-flow-analytics/
│
├── backend/
│   ├── api/
│   ├── ml/
│   ├── models/
│   ├── data/
│   ├── main.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── scripts/
│   ├── train_pipeline.py
│   └── download_dataset.py
│
├── README.md
└── .gitignore
```

```

---

## ⚙️ Major Technical Modules

### 1. Packet Processing Layer
- Live packet sniffing using Scapy  
- PCAP ingestion support  
- Flow aggregation using 5-tuple logic  

### 2. Feature Engineering Layer
- Flow macro-metrics  
- Packet inter-arrival time features  
- Packet size and direction metrics  
- Unified feature vector generation  

### 3. Machine Learning Layer
- Random Forest supervised classifier  
- Isolation Forest anomaly detector  
- XGBoost optimization layer  
- Fusion-based prediction logic  

### 4. Explainability Layer
- SHAP TreeExplainer integration  
- Per-alert feature contribution display  

### 5. Visualization Layer
- Real-time alert dashboard  
- Threat metrics panel  
- Historical flow monitoring  

---

## 📊 Dataset Used

### Primary Dataset
- CIC-IDS2017  

### Additional Dataset
- UNSW-NB15  

### Processing Applied
- Parsing  
- Cleaning  
- Balancing using SMOTE  
- VIF multicollinearity analysis  
- PCA feature pruning  

---

## 🚀 Running the Project

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📡 API Access

- Backend API: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`
- Frontend Dashboard: `http://localhost:5173`

---

## 👥 Team Responsibilities

| Member | Technical Contribution |
|--------|------------------------|
| **SHASHIDAR** | Architecture design, CLI framework, SHAP integration, system integration |
| **TCHEMAKO** | Repository setup, packet capture, PCAP ingestion, testing |
| **PARAVASTHU** | Dataset engineering, feature extraction, validation |
| **NUTPALLY** | Machine learning models, evaluation, performance tuning |

---

## 📅 Execution Model

The project was structured as a **3-week technical sprint (15 working days)** with clear phase-wise module ownership:

- **Week 1:** Foundation and capture architecture  
- **Week 2:** Feature intelligence and ML pipeline  
- **Week 3:** Explainability, dashboard, testing, integration  

---

## 🎯 Academic Value

This project demonstrates:
- Cybersecurity engineering  
- Applied machine learning  
- Real-time systems design  
- Explainable AI integration  
- Full-stack technical implementation  

Suitable for:
- Academic evaluation  
- Technical viva  
- GitHub portfolio presentation  

---

## 📌 Repository Presentation Tip

For GitHub upload:
- Keep only clean source folders  
- Exclude virtual environments  
- Exclude datasets larger than GitHub limits  
- Upload trained lightweight model artifacts only if needed  

Recommended `.gitignore`:
```text
venv/
node_modules/
__pycache__/
*.joblib
data/raw/
```

---

## 📄 License

Academic technical project for educational demonstration.
