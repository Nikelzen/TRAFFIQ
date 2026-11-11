# TrafficIQ user manual (initial build)

1. Start PostgreSQL and create the database, or use SQLite only for local development.
2. Configure backend environment variables and start FastAPI.
3. Start the Vite frontend.
4. Create a site from the dashboard. The current development build uses a local owner identifier; do not expose this configuration to the public internet.
5. Prepare a CSV with required `timestamp,visitors` columns. Optional columns are `sessions,page_views`. Use timezone-aware timestamps when possible.
6. Import the CSV through the API endpoint `POST /api/v1/sites/{site_id}/datasets/csv?owner_id=...`; the full upload UI is pending.
7. Review summary, observations, calculus, forecasting and export API endpoints in Swagger.
8. Empty or insufficient datasets intentionally produce empty/insufficient-data responses.
