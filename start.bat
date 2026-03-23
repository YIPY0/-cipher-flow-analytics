@echo off
echo ═══════════════════════════════════════════════════════
echo   CIPHER-FLOW ANALYTICS — Startup (Windows)
echo ═══════════════════════════════════════════════════════

REM ── Backend ─────────────────────────────────────────────
echo.
echo ▶ Setting up backend...
cd backend

if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

if not exist "models\random_forest.joblib" (
    echo.
    echo ▶ Models not found — running training pipeline...
    python -m scripts.train_pipeline --synthetic --skip-vif
)

echo.
echo ▶ Starting backend on :8000 ...
start /B python main.py

cd ..

REM ── Frontend ────────────────────────────────────────────
echo.
echo ▶ Setting up frontend...
cd frontend

if not exist "node_modules" (
    call npm install
)

echo ▶ Starting frontend on :5173 ...
start /B npm run dev

cd ..

echo.
echo ═══════════════════════════════════════════════════════
echo   Backend:   http://localhost:8000
echo   Frontend:  http://localhost:5173
echo   API Docs:  http://localhost:8000/docs
echo ═══════════════════════════════════════════════════════
echo   Press Ctrl+C to stop
pause