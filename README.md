# TrafficIQ

**Micro Project 14: Model and Predict Website Traffic Over Time**

A real-data-first full-stack website traffic analytics project. A new
installation starts with an empty database. No sample visitors, random traffic,
fabricated charts or fake model scores are seeded.

## Windows quick start
1. Install Python 3.11+ and Node.js 20+.
2. Extract the ZIP.
3. Run `SETUP_TRAFFIQ.bat` once.
4. Run `START_TRAFFIQ.bat` to start the API and frontend together.
5. Keep both service terminal windows open.

The local setup uses SQLite to avoid requiring a separate database installation.
PostgreSQL is supported by configuring `DATABASE_URL` in `backend/.env` and
running migrations against an available PostgreSQL server.

## Addresses
- Frontend: http://localhost:5173
- API: http://localhost:8000
- Swagger/OpenAPI: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

## CSV
Required: `timestamp,visitors`
Optional: `sessions,page_views`
Use genuine exported traffic observations. Invalid/missing values, negative
counts and duplicate timestamps are rejected.

## Stack
React, TypeScript, Vite, Recharts; Python, FastAPI, SQLAlchemy, Alembic;
SQLite/PostgreSQL; Pandas, NumPy, SciPy and scikit-learn.

## Important limitations
This is an academic local-development foundation, not a production-ready
multi-tenant service. Production authentication/authorization, GA4 OAuth and
synchronisation, aggregation of first-party tracking events into visitor
observations, persistent result history, complete model comparison and full
browser end-to-end verification remain incomplete. Some analysis pages display
structured API results rather than finished interactive visualisations.
Review `docs/technical/IMPLEMENTATION_STATUS.md` before submission.
