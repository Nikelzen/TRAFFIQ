# TrafficIQ speaker notes and 5–7 minute demonstration script

## Speaker notes by slide
1. Introduce the project as a mathematical traffic analysis and prediction application.
2. Explain why historical traffic is useful and why forecasting needs validation.
3. State the objectives and the no-fabrication policy.
4. Explain the difference between CSV, first-party tracking and GA4; be clear about what is and is not implemented.
5. Walk through the browser, API, database and analysis-service layers.
6. Explain which descriptive metrics are currently calculated and which aggregations remain pending.
7. Explain derivatives, critical-point classification, inflection sign changes and numerical integration.
8. Explain chronological evaluation and the meaning of MAE, RMSE and sMAPE.
9. Explain robust anomaly indicators and visitor-only capacity calculations.
10. Report only the actual test evidence listed on the slide. Do not claim frontend or PostgreSQL tests passed.
11. Be transparent about unfinished production features and the plan to complete them.
12. Conclude with the importance of genuine data and reproducible calculations.

## 5–7 minute demonstration script
**0:00–0:40 — Introduction.** “This is TrafficIQ, a website traffic analysis and forecasting application. The central idea is to turn genuine historical traffic observations into transparent mathematical analysis and carefully evaluated forecasts.”

**0:40–1:30 — Data integrity.** Open the dashboard and show the empty state. Explain that the application intentionally shows no statistics until a real source is connected. Open Data Management, create a site and select a genuine CSV supplied by the project evaluator. Do not use invented values. Explain the required timestamp and visitors columns and optional sessions/page_views fields.

**1:30–2:15 — Historical analysis.** After importing a genuine dataset, return to the dashboard and explain the totals, average, peak, low and traffic trend. Open Traffic Analysis and show the stored observations.

**2:15–3:15 — Calculus.** Open Calculus Lab. Explain V(t), the first derivative, second derivative, critical points and the sign-change test for inflection points. Explain that trapezoidal integration approximates area under the curve and is different from the discrete visitor sum.

**3:15–4:20 — Forecasting.** Open Forecasting, select a baseline model and a horizon. Explain chronological holdout validation and the MAE, RMSE and sMAPE values returned for the available dataset. Do not describe a metric as accuracy.

**4:20–5:10 — Anomalies and capacity.** Show anomaly output and explain that unusual traffic is not proof of malicious activity. Open Capacity Planning and explain the visitor-volume headroom calculation.

**5:10–6:00 — Reports and limitations.** Export the observation CSV and summary PDF. State the current limitations honestly: authentication hardening, full tracking aggregation, GA4, logistic fitting, frontend test execution and PostgreSQL verification remain pending in this build.

**6:00–6:20 — Conclusion.** “TrafficIQ is designed around real observations, transparent calculations and honest model evaluation. Its next stage is to complete production integrations and verify the full workflow with a genuine dataset.”

## Before presenting
- Configure and start PostgreSQL, or clearly label SQLite as a local development fallback.
- Complete frontend dependency installation and run the production build.
- Use a genuine dataset with documented provenance and permission to use it.
- Capture screenshots from the actual running application.
- Replace placeholders with verified student and institution details.
- Do not claim incomplete features as working.
