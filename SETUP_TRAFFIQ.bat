@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title TrafficIQ - First Time Setup
echo ============================================================
echo                 TRAFFIQ - FIRST TIME SETUP
echo ============================================================
echo Installs dependencies and prepares an EMPTY local database.
echo No sample or synthetic traffic records are created.
echo.

where node >nul 2>nul
if errorlevel 1 goto no_node
where npm >nul 2>nul
if errorlevel 1 goto no_npm
where py >nul 2>nul
if errorlevel 1 goto use_python
set "PYTHON_CMD=py -3"
%PYTHON_CMD% --version >nul 2>nul
if errorlevel 1 goto use_python
goto python_found

:use_python
where python >nul 2>nul
if errorlevel 1 goto no_python
set "PYTHON_CMD=python"

:python_found
echo Python:
%PYTHON_CMD% --version
echo Node:
node --version

if exist "backend\.venv\Scripts\python.exe" goto venv_ready
echo [1/4] Creating Python environment...
%PYTHON_CMD% -m venv backend\.venv
if errorlevel 1 goto failed

:venv_ready
echo [2/4] Installing backend dependencies...
call "backend\.venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto failed
call "backend\.venv\Scripts\python.exe" -m pip install -r backend\requirements.txt
if errorlevel 1 goto failed

if exist "backend\.env" goto env_ready
echo [3/4] Creating local SQLite configuration...
>"backend\.env" echo APP_NAME=TrafficIQ
>>"backend\.env" echo ENVIRONMENT=development
>>"backend\.env" echo API_V1_PREFIX=/api/v1
>>"backend\.env" echo DATABASE_URL=sqlite:///./traffiq_dev.db
>>"backend\.env" echo CORS_ORIGINS=http://localhost:5173
>>"backend\.env" echo UPLOAD_DIR=./uploads
>>"backend\.env" echo MAX_UPLOAD_MB=20
>>"backend\.env" echo TRACKING_RATE_LIMIT_PER_MINUTE=120
>>"backend\.env" echo TRACKING_SIGNING_SECRET=CHANGE_THIS_LOCAL_SECRET
goto frontend_setup

:env_ready
echo [3/4] Keeping existing backend\.env...

:frontend_setup
if exist "frontend\node_modules\vite\bin\vite.js" goto frontend_ready
echo [4/4] Installing frontend dependencies. Internet is required.
pushd frontend
call npm install
if errorlevel 1 goto frontend_failed
popd
goto migrate

:frontend_failed
popd
goto failed

:frontend_ready
echo [4/4] Frontend dependencies already installed.

:migrate
echo Applying database migrations...
pushd backend
call .venv\Scripts\python.exe -m alembic upgrade head
if errorlevel 1 goto migration_failed
popd
echo.
echo SETUP COMPLETED SUCCESSFULLY.
echo Next: double-click START_TRAFFIQ.bat
echo The database is empty until you import your genuine traffic CSV.
pause
exit /b 0

:migration_failed
popd
goto failed

:no_node
echo [ERROR] Install Node.js 20 or newer from https://nodejs.org/
goto failed
:no_npm
echo [ERROR] npm was not found. Reinstall Node.js.
goto failed
:no_python
echo [ERROR] Install Python 3.11 or newer from https://www.python.org/downloads/
goto failed
:failed
echo.
echo [ERROR] Setup failed. Read the message above, correct it, then rerun setup.
pause
exit /b 1
