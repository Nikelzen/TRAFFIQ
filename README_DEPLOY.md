# TrafficIQ Deployment & Local Launch Guide

## 1. Quick Local Run (Windows)
1. Extract this folder anywhere without spaces (e.g., `C:\TrafficIQ`).
2. Double-click `ONE_CLICK_RUN.bat` — it automatically sets up the Python virtual environment, installs dependencies, creates `.env` with SQLite, and starts both Backend (`http://localhost:8000`) and Frontend (`http://localhost:5173`).

## 2. Cloud Deployment (Docker / Render / Railway / VPS)
- **Full-stack Docker:** Run `docker-compose up --build -d` from the root directory.
- **Backend Only (Render / Railway):**
  - Root Directory: `backend`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - Environment Variable: `DATABASE_URL=sqlite:///./traffiq.db` (or PostgreSQL URL)
- **Frontend Only (Vercel / Netlify):**
  - Root Directory: `frontend`
  - Build Command: `npm install && npm run build`
  - Output Directory: `dist`
  - Environment Variable: `VITE_API_BASE_URL=https://your-backend-url.onrender.com`
