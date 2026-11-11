@echo off
title TrafficIQ Launcher
echo ==========================================
echo   Setting up and starting TrafficIQ...
echo ==========================================

if not exist ".env" (
    echo DATABASE_URL=sqlite:///./traffiq.db> .env
    echo CORS_ORIGINS=*>> .env
)

cd backend
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
start "TrafficIQ Backend" cmd /k "call venv\Scripts\activate && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
cd ..

cd frontend
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)
start "TrafficIQ Frontend" cmd /k "npm run dev"
cd ..

echo ==========================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo ==========================================
pause
