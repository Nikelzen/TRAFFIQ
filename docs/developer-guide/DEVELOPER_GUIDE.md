# Developer guide

- Keep routes thin; calculations belong in `backend/app/services`.
- Add schema changes through Alembic revisions.
- Never add fabricated traffic rows to seed scripts or screenshots.
- Keep chronological validation: do not shuffle time-series data.
- Preserve source provenance for every imported observation.
- Run `pytest` from `backend/` and `npm test` / `npm run build` from `frontend/`.
- Before deployment, implement authentication, bind site ownership to authenticated principals, add consent/privacy controls, restrict upload origin and size, configure HTTPS, and review retention/deletion requirements.
