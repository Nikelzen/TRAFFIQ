# API overview

Base path: `/api/v1`

- `GET /health` — service health.
- `POST /sites` — create a site (development owner identifier only).
- `GET /sites?owner_id=...` — list sites for owner identifier.
- `POST /sites/{site_id}/datasets/csv` — validate and import CSV.
- `GET /sites/{site_id}/analytics/summary` — calculated summary.
- `GET /sites/{site_id}/observations` — stored observations.
- `GET /sites/{site_id}/calculus` — polynomial and calculus analysis.
- `GET /sites/{site_id}/forecast/evaluation` — chronological holdout metrics.
- `GET /sites/{site_id}/forecast` — baseline forecast.
- `GET /sites/{site_id}/anomalies` — rolling robust anomaly detection.
- `POST /sites/{site_id}/capacity` — visitor-volume capacity estimate.
- `POST /tracking/{site_id}` — first-party event ingestion (not yet production hardened).
- `GET /sites/{site_id}/reports/summary.csv` — observations export.
- `GET /sites/{site_id}/reports/summary.pdf` — calculated summary PDF.

Interactive OpenAPI documentation is served by FastAPI at `/docs`. All site routes require the current development `owner_id` query parameter; this is not a substitute for authentication.
