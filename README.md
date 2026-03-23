\##🔒 CipherFlow Analytics - Real-Time Network Intrusion Detection System



> \*\*ML-Powered Network Security Monitoring with Live Packet Capture \& Explainable AI\*\*



\[!\[Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

\[!\[FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)

\[!\[React](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org/)

\[!\[MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248.svg)](https://www.mongodb.com/)



\---



\## 📋 Table of Contents

\- \[Overview](#overview)

\- \[System Architecture](#system-architecture)

\- \[Why This Tech Stack?](#why-this-tech-stack)

\- \[Requirements](#requirements)

\- \[Installation](#installation)

\- \[How to Run](#how-to-run)

\- \[Features](#features)

\- \[ML Pipeline](#ml-pipeline)

\- \[API Endpoints](#api-endpoints)

\- \[Project Structure](#project-structure)

\- \[Team \& Contributions](#team--contributions)



\---



\## 🎯 Overview



\*\*CipherFlow Analytics\*\* is a \*\*production-grade Network Intrusion Detection System (NIDS)\*\* that captures live network packets, classifies threats using Machine Learning, and provides real-time visualization through a responsive web dashboard.



\### Key Capabilities

\- ✅ \*\*Live Packet Capture\*\* from network interfaces (Scapy + Npcap)

\- ✅ \*\*Hybrid ML Detection\*\* - Random Forest + Isolation Forest

\- ✅ \*\*99.7% Accuracy\*\* on CIC-IDS2017 benchmark dataset

\- ✅ \*\*Explainable AI\*\* using SHAP for decision transparency

\- ✅ \*\*Real-Time Dashboard\*\* with WebSocket streaming (<2s latency)

\- ✅ \*\*Multi-Threat Detection\*\*: DDoS, Port Scanning, Malware, Botnet, etc.



\---



\## 🏗️ System Architecture

┌──────────────────────────────────────────────────────────────┐

│ USER BROWSER │

│ http://localhost:5173 │

└────────────────────────┬─────────────────────────────────────┘

│ HTTP / WebSocket

▼

┌──────────────────────────────────────────────────────────────┐

│ FRONTEND (React + Vite) │

│ • Dashboard.jsx → Live network monitoring │

│ • ThreatTable.jsx → Threat analysis │

│ • ShapPanel.jsx → AI explainability │

│ • FlowVisualizer.jsx → Charts \& graphs │

└────────────────────────┬─────────────────────────────────────┘

│ REST API + WebSocket

▼

┌──────────────────────────────────────────────────────────────┐

│ BACKEND (FastAPI + Python) │

│ ┌────────────────────────────────────────────────────┐ │

│ │ Packet Capture Thread (Scapy) │ │

│ │ • Sniffs live packets from NIC │ │

│ │ • Builds bidirectional flows │ │

│ │ • Extracts 28 statistical features │ │

│ └────────────────────────────────────────────────────┘ │

│ ┌────────────────────────────────────────────────────┐ │

│ │ ML Prediction Engine │ │

│ │ • Random Forest Classifier (Supervised) │ │

│ │ • Isolation Forest (Unsupervised Anomaly) │ │

│ │ • SHAP Explainer (Interpretability) │ │

│ └────────────────────────────────────────────────────┘ │

│ ┌────────────────────────────────────────────────────┐ │

│ │ WebSocket Manager │ │

│ │ • Broadcasts new flows to all clients │ │

│ └────────────────────────────────────────────────────┘ │

└────────────────────────┬─────────────────────────────────────┘

│ Motor (Async Driver)

▼

┌──────────────────────────────────────────────────────────────┐

│ MongoDB Database │

│ Collections: flows, alerts │

└──────────────────────────────────────────────────────────────┘

▲

│ Npcap Driver

┌──────────────────────────────────────────────────────────────┐

│ Network Interface Card (Wi-Fi/Ethernet) │

└──────────────────────────────────────────────────────────────┘



text





\---



\## 🧠 Why This Tech Stack?



\### Backend



| Technology | Why We Chose It |

|------------|-----------------|

| \*\*FastAPI\*\* | Async support for handling 1000+ concurrent WebSocket connections. 3x faster than Flask. Auto-generates API docs at `/docs`. |

| \*\*Scapy\*\* | Pure Python packet manipulation. Layer-wise dissection (IP/TCP/UDP). Works on Windows with Npcap. |

| \*\*Random Forest\*\* | Ensemble learning → 99.7% accuracy. Handles non-linear network patterns. Fast inference (<5ms). |

| \*\*Isolation Forest\*\* | Unsupervised anomaly detection. Detects zero-day attacks without labels. Low false-positive rate. |

| \*\*SHAP\*\* | Explainable AI using Shapley values. Shows exactly why a flow was flagged as malicious. |

| \*\*MongoDB\*\* | Schema-less JSON storage. Fast writes for high-throughput packet capture. Horizontal scaling support. |



\### Frontend



| Technology | Why We Chose It |

|------------|-----------------|

| \*\*React\*\* | Component-based UI. Virtual DOM for efficient real-time updates. Huge ecosystem. |

| \*\*Vite\*\* | 10x faster than Create React App. <500ms dev server startup. Instant Hot Module Replacement. |

| \*\*Tailwind CSS\*\* | Utility-first CSS. No custom stylesheet needed. Built-in dark mode. Smaller bundle size. |

| \*\*WebSockets\*\* | Real-time server push. <100ms latency. Single persistent connection vs. repeated HTTP polling. |



\---



\## 📦 Requirements



\### Software Requirements



| Software | Version | Download Link |

|----------|---------|---------------|

| \*\*Python\*\* | 3.9+ | https://www.python.org/downloads/ |

| \*\*Node.js\*\* | 18+ | https://nodejs.org/ |

| \*\*MongoDB\*\* | 7.0+ | https://www.mongodb.com/try/download/community |

| \*\*Npcap\*\* | 1.70+ | https://npcap.com/#download |

| \*\*Git\*\* | Latest | https://git-scm.com/ |



\### Hardware Requirements



| Component | Minimum | Recommended |

|-----------|---------|-------------|

| \*\*CPU\*\* | Intel i3 / AMD Ryzen 3 | Intel i5 / AMD Ryzen 5 |

| \*\*RAM\*\* | 8 GB | 16 GB |

| \*\*Storage\*\* | 50 GB | 100 GB SSD |

| \*\*Network\*\* | Wi-Fi/Ethernet | Gigabit Ethernet |



\### Python Packages



Create `backend/requirements.txt`:



```txt

fastapi==0.104.1

uvicorn==0.24.0

pydantic-settings==2.1.0

motor==3.3.2

pymongo==4.6.0

scikit-learn==1.3.2

pandas==2.1.3

numpy==1.24.4

joblib==1.3.2

shap==0.43.0

scapy==2.5.0

matplotlib==3.8.2

seaborn==0.13.0

scipy==1.11.4

websockets==12.0

Frontend Packages

Already in frontend/package.json:



JSON



{

&#x20; "dependencies": {

&#x20;   "react": "^18.2.0",

&#x20;   "react-dom": "^18.2.0",

&#x20;   "react-router-dom": "^6.20.0",

&#x20;   "recharts": "^2.10.0",

&#x20;   "lucide-react": "^0.294.0"

&#x20; },

&#x20; "devDependencies": {

&#x20;   "@vitejs/plugin-react": "^4.2.0",

&#x20;   "autoprefixer": "^10.4.16",

&#x20;   "postcss": "^8.4.32",

&#x20;   "tailwindcss": "^3.3.6",

&#x20;   "vite": "^5.0.0"

&#x20; }

}

🚀 Installation

1\. Install Prerequisites

Windows:

PowerShell



\# Install Python 3.9+ (Check "Add to PATH")

\# Install Node.js 18+ (LTS version)

\# Install MongoDB (Install as Windows Service)

\# Install Npcap (WinPcap compatibility mode)

Verify installations:



PowerShell



python --version  # Should show 3.9+

node --version    # Should show 18+

npm --version     # Should show 9+

mongod --version  # Should show 7.0+

2\. Clone Repository

Bash



git clone https://github.com/your-team/cipher-flow-analytics.git

cd cipher-flow-analytics

3\. Backend Setup

PowerShell



cd backend



\# Create virtual environment

python -m venv venv



\# Activate virtual environment

\# Windows PowerShell:

.\\venv\\Scripts\\Activate.ps1

\# Windows CMD:

venv\\Scripts\\activate.bat



\# Install dependencies

pip install -r requirements.txt

4\. Frontend Setup

PowerShell



cd frontend

npm install

5\. Download Dataset

Option A: Automatic



PowerShell



cd backend

.\\venv\\Scripts\\Activate.ps1

python ../scripts/download\_dataset.py

Option B: Manual



Visit https://www.unb.ca/cic/datasets/ids-2017.html

Download MachineLearningCSV.zip

Extract all CSV files to backend/data/raw/

6\. Train ML Models

PowerShell



cd backend

.\\venv\\Scripts\\Activate.ps1

python ../scripts/train\_pipeline.py

Expected output:



text



✅ Models loaded: 28 features

✅ Accuracy: 99.69%

✅ F1-Score: 99.69%

✅ ROC-AUC: 99.99%

Models saved to: backend/models/

Training takes 20-60 minutes depending on your CPU.



▶️ How to Run

Start All Services

Terminal 1: MongoDB

PowerShell



mongod --dbpath "C:\\data\\db"

Terminal 2: Backend (Run as Administrator!)

PowerShell



cd backend

.\\venv\\Scripts\\Activate.ps1

python main.py

Expected:



text



✅ MongoDB connected: cipherflow

✅ Models loaded: 28 features

🔴 LIVE CAPTURE ACTIVE

INFO: Uvicorn running on http://0.0.0.0:8000

Terminal 3: Frontend

PowerShell



cd frontend

npm run dev

Expected:



text



VITE ready in 500ms

➜ Local: http://localhost:5173/

Access Application

Dashboard: http://localhost:5173

API Docs: http://localhost:8000/docs

Health Check: http://localhost:8000/api/health

⚡ Features

Real-Time Monitoring

Live packet capture from network interface

Bidirectional flow aggregation

Sub-2-second latency from capture to UI display

ML-Powered Detection

Random Forest Classifier: 99.7% accuracy on known attacks

Isolation Forest: Detects unknown/zero-day threats

SHAP Explainability: Shows why flows are flagged

Interactive Dashboard

Live flow monitor with WebSocket streaming

Threat severity badges (Critical/High/Medium/Low)

Timeline charts \& distribution graphs

Alert history with filtering

Threat Categories

Benign - Normal traffic

DoS/DDoS - Denial of Service attacks

Port Scan - Network reconnaissance

Botnet - C\&C communications

Malware - Malicious payloads

Infiltration - Internal attacks

Web Attacks - SQL injection, XSS

🤖 ML Pipeline

Dataset: CIC-IDS2017

Metric	Value

Total Flows	2,830,743

Benign	80.3%

Attacks	19.7%

Original Features	78

Selected Features	28

Preprocessing

Feature Selection



VIF analysis removes multicollinearity

Correlation threshold > 0.95

78 features → 28 features

Feature Engineering



Packet counts (forward/backward)

Packet lengths (min/max/mean/std)

Inter-arrival times (IAT)

TCP flags (SYN/FIN/PSH/ACK)

Flow duration \& active/idle times

Scaling



StandardScaler (Z-score normalization)

Mean=0, Std=1 for all features

Model Configuration

Random Forest:



Python



n\_estimators=200    # 200 decision trees

max\_depth=30        # Prevent overfitting

min\_samples\_split=10

random\_state=42

Isolation Forest:



Python



contamination=0.05  # Expect 5% anomalies

n\_estimators=200

max\_samples=256

Performance Metrics

text



Accuracy:  99.69%

Precision: 99.69%

Recall:    99.69%

F1-Score:  99.69%

ROC-AUC:   99.99%

Per-Class Metrics:



text



&#x20;                 precision  recall  f1-score

benign              0.998    0.998     0.998

scanning            0.987    0.987     0.987

malware             0.996    0.997     0.996

botnet              0.962    1.000     0.980

📡 API Endpoints

REST API

http



GET  /api/health              # System health check

GET  /api/stats               # Overall statistics

GET  /api/threats             # Detected threats

GET  /api/flows               # All captured flows

GET  /api/alerts              # Alert timeline

GET  /api/model/performance   # ML model metrics

GET  /api/shap/explain        # SHAP explanation

GET  /api/flow/timeline       # Time-series data

WebSocket

JavaScript



ws://localhost:8000/ws

Message format:



JSON



{

&#x20; "type": "new\_flow",

&#x20; "data": {

&#x20;   "flow\_id": "uuid-123",

&#x20;   "src\_ip": "192.168.1.35",

&#x20;   "dst\_ip": "45.33.32.156",

&#x20;   "prediction": "scanning",

&#x20;   "confidence": 0.92,

&#x20;   "is\_threat": true,

&#x20;   "severity": "high"

&#x20; }

}

📂 Project Structure

text



cipher-flow-analytics/

│

├── backend/

│   ├── main.py                   # FastAPI app + packet capture

│   ├── config.py                 # Configuration

│   ├── requirements.txt          # Python dependencies

│   │

│   ├── api/

│   │   ├── routes.py             # REST API endpoints

│   │   └── websocket\_manager.py  # WebSocket handler

│   │

│   ├── ml/

│   │   ├── dataset\_prep.py       # Data preprocessing

│   │   ├── train\_random\_forest.py

│   │   ├── train\_isolation\_forest.py

│   │   ├── explainability.py     # SHAP integration

│   │   └── evaluation.py         # Metrics calculation

│   │

│   ├── models/                   # Trained models (generated)

│   │   ├── random\_forest.joblib

│   │   ├── isolation\_forest.joblib

│   │   ├── scaler.joblib

│   │   └── label\_encoder.joblib

│   │

│   └── data/

│       └── raw/                  # CIC-IDS2017 CSV files

│

├── frontend/

│   ├── package.json

│   ├── vite.config.js

│   │

│   └── src/

│       ├── main.jsx

│       ├── App.jsx

│       │

│       ├── components/

│       │   ├── LiveDashboard.jsx

│       │   ├── ThreatTable.jsx

│       │   ├── FlowVisualizer.jsx

│       │   └── ShapPanel.jsx

│       │

│       └── pages/

│           ├── Dashboard.jsx

│           ├── ThreatsPage.jsx

│           └── AlertsPage.jsx

│

├── scripts/

│   ├── train\_pipeline.py         # ML training script

│   └── download\_dataset.py       # Dataset downloader

│

├── README.md

└── .gitignore

👥 Team \& Contributions

Team Members

\[Your Name] - ML Pipeline, Backend Development

\[Member 2] - Frontend Development, UI/UX

\[Member 3] - Data Preprocessing, Testing

Project Guide

\[Guide Name] - \[Department], \[Institution]

Contribution Guidelines

Fork the repository

Create feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Open Pull Request

📚 References

Sharafaldin, I., et al. (2018). "CIC-IDS2017 Dataset"

Lundberg, S. M. (2017). "A Unified Approach to Interpreting Model Predictions" (SHAP)

Liu, F. T. (2008). "Isolation Forest"

Breiman, L. (2001). "Random Forests"

📄 License

MIT License - See LICENSE file



📧 Contact

GitHub: https://github.com/your-team/cipher-flow-analytics

Email: team@example.com

⭐ Star this repo if you found it helpful!

