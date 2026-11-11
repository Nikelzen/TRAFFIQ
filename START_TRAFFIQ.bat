@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title TrafficIQ - Start All Services
echo ============================================================
echo                  TRAFFIQ - STARTUP
echo ============================================================

if not exist "backend\.venv\Scripts\python.exe" goto run_setup
if not exist "frontend\node_modules\vite\bin\vite.js" goto run_setup
goto check_ports

:run_setup
echo Setup is incomplete. Running first-time setup...
call "%~dp0SETUP_TRAFFIQ.bat"
if errorlevel 1 exit /b 1

:check_ports
echo Checking ports 8000 and 5173...
powershell -NoProfile -Command "if (Get-NetTCPConnection -State Listen -LocalPort 8000 -ErrorAction SilentlyContinue) { exit 1 }"
if errorlevel 1 goto port8000_busy
powershell -NoProfile -Command "if (Get-NetTCPConnection -State Listen -LocalPort 5173 -ErrorAction SilentlyContinue) { exit 1 }"
if errorlevel 1 goto port5173_busy

echo Applying database migrations...
pushd backend
call .venv\Scripts\python.exe -m alembic upgrade head
if errorlevel 1 goto migration_failed
popd

echo Starting TrafficIQ API...
start "TrafficIQ API - KEEP OPEN" /D "%~dp0backend" "%~dp0backend\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000

echo Waiting for API health check...
set "API_READY="
for /L %%I in (1,1,30) do call :check_api
if not defined API_READY goto api_failed

echo API is healthy. Starting frontend...
start "TrafficIQ Frontend - KEEP OPEN" /D "%~dp0frontend" cmd /k npm run dev -- --host 127.0.0.1 --port 5173 --strictPort
timeout /t 5 /nobreak >nul
start "" "http://localhost:5173"
echo.
echo Frontend: http://localhost:5173
echo API:      http://localhost:8000
echo API docs: http://localhost:8000/docs
echo Keep both service terminal windows open.
pause
exit /b 0

:check_api
if defined API_READY exit /b
powershell -NoProfile -Command "try { $r=Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/api/v1/health -TimeoutSec 2; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>nul
if not errorlevel 1 set "API_READY=1"
if not defined API_READY timeout /t 1 /nobreak >nul
exit /b

:port8000_busy
echo [ERROR] Port 8000 is already in use. Close the other app using it and retry.
pause
exit /b 1
:port5173_busy
echo [ERROR] Port 5173 is already in use. Close the other app using it and retry.
pause
exit /b 1
:migration_failed
popd
echo [ERROR] Database migration failed. Check backend\.env.
pause
exit /b 1
:api_failed
echo [ERROR] API did not become healthy. Inspect the TrafficIQ API terminal.
pause
exit /b 1
