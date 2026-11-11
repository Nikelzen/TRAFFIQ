# TrafficIQ Windows setup and launch

## One-time setup

1. Extract the complete ZIP to a normal writable folder, for example `C:\Projects\TrafficIQ`.
2. Install **Python 3.11 or newer** and **Node.js 20 LTS or newer**. During Python installation, enable the Python launcher / PATH option.
3. Ensure the computer has internet access for the first dependency installation.
4. Double-click `SETUP_TRAFFIQ.bat` and wait until it reports `SETUP COMPLETE`.

The setup script creates `backend\\.venv`, installs Python packages, creates `backend\\.env` if one does not already exist, installs npm packages and applies Alembic migrations. It does not overwrite an existing `backend\\.env`.

## Start the complete application

Double-click `START_TRAFFIQ.bat`. It applies pending migrations, starts the API and Vite development server in separate terminal windows, then opens the browser.

- Frontend: http://localhost:5173
- API: http://localhost:8000
- Swagger API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/health

Keep both terminal windows open. Close them to stop the two development servers.

## Database modes

### Easy local mode (default for first setup)

The setup script creates `backend\\.env` with `DATABASE_URL=sqlite:///./traffiq_dev.db`. The database file is local to the backend directory. SQLite is intended for local development and first-run testing; it is not presented as PostgreSQL.

### PostgreSQL mode

Install PostgreSQL 15 or newer, create a database and a dedicated database user, then edit `backend\\.env`:

```dotenv
DATABASE_URL=postgresql+psycopg://traffiq:YOUR_URL_ENCODED_PASSWORD@localhost:5432/traffiq
```

If the password contains reserved URL characters, URL-encode them. Ensure PostgreSQL is running before launching `START_TRAFFIQ.bat`. The launcher applies migrations against the configured database. Do not use a production database for coursework experiments.

## Troubleshooting

- **Python not found:** install Python 3.11+ and reopen Command Prompt; verify `py -3 --version`.
- **Node/npm not found:** install Node.js 20+ and reopen Command Prompt; verify `node -v` and `npm -v`.
- **Dependency installation fails:** check internet/proxy/firewall access, then rerun `SETUP_TRAFFIQ.bat`.
- **Port 8000 or 5173 is busy:** stop the process using that port or change the corresponding port in the launcher and Vite configuration consistently.
- **PostgreSQL connection error:** check the service, database name, username, password, host and port in `backend\\.env`.
- **API starts but browser says network error:** visit the health URL above and inspect the API terminal for a traceback.

## Data integrity

TrafficIQ does not seed traffic observations. A new database is expected to show an empty state. Import a genuine CSV containing `timestamp,visitors` (optional `sessions,page_views`) or configure a genuine source. Do not use invented values in academic experiments.

## Stop and restart

Close the API and frontend terminal windows to stop. Run `START_TRAFFIQ.bat` again to restart. Do not delete `backend\\traffiq_dev.db` if you want to preserve locally imported observations.
