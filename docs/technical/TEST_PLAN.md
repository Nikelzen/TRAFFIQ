# Test plan

## Backend
- CSV required columns, missing values, invalid timestamps, negative/non-integer values, duplicates, timezone normalisation.
- Site ownership filters.
- Summary totals and optional metric availability.
- Polynomial derivatives, critical-point sign classification, inflection sign changes, trapezoidal integration.
- Chronological split, MAE/RMSE/sMAPE/MAPE handling, insufficient-history refusal.
- Robust MAD anomaly detection and capacity arithmetic.
- CSV/PDF response content and headers.

## Frontend
- Navigation and empty state.
- Theme toggle and local persistence.
- API unavailable and error states.
- Responsive layout and chart rendering with real observation payloads.

## End-to-end
Create site → import genuine CSV → retrieve observations → calculate analytics → run calculus → evaluate forecast → detect anomalies → calculate capacity → export reports.

Record actual command output, environment and dataset provenance before marking any test as passed.
