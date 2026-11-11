# Data dictionary

| Entity | Important fields | Meaning |
|---|---|---|
| sites | id, name, domain, owner_id, created_at | A tracked website or analysis workspace. |
| datasets | id, site_id, source, filename, timezone_name, row_count | Imported or collected data batch and provenance. |
| traffic_observations | timestamp, visitors, sessions, page_views, dataset_id | Aggregated traffic observation for a timestamp. |
| tracking_events | event_id, event_type, page_path, referrer_host, anonymous_session, occurred_at | First-party event record. |
| forecasts | model_name, horizon, result | Persistable forecast output. |
| model_evaluations | mae, rmse, smape, mape, test_count | Chronological holdout evaluation. |
| anomalies | observed, expected, deviation, method, severity | Detected unusual traffic observations. |
| capacity_configurations | capacity_limit, headroom_percent, horizon | Visitor-volume planning parameters. |

All site-owned records reference `sites.id`. The current `owner_id` field is a placeholder pending authenticated identity integration.
