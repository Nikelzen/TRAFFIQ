# Micro Project 14: Model and Predict Website Traffic Over Time

**Product:** TrafficIQ

**Institution:** [Insert verified institution name]

**Department:** [Insert department]

**Student name / register number:** [Complete editable placeholders]

## Certificate
[Institution-approved certificate text and signatures to be inserted by the department.]

## Declaration
[Insert the student's own declaration and signature.]

## Acknowledgement
[Insert acknowledgement.]

## Abstract
TrafficIQ is designed to analyse website traffic observations and explore mathematical and statistical methods for estimating future traffic. The application architecture combines a React and TypeScript interface with a Python FastAPI service and a relational database. It accepts user-provided traffic observations and derives descriptive measures, polynomial curve analysis, baseline forecasts, anomaly indicators and visitor-volume capacity estimates. The system follows a data-integrity principle: it does not generate sample visitor counts or fabricate model scores. Results are available only when an actual data source has supplied observations. This draft describes the implemented foundation and clearly identifies unfinished components; final experimental findings must be added only after testing with a genuine dataset.

## 1. Introduction
Website traffic varies over time due to audience behaviour, content changes, campaigns and external events. Understanding historical patterns can support planning, but forecasting must be evaluated against later observations rather than judged from a graph alone.

## 2. Problem statement
A user needs a transparent application that imports genuine traffic observations, analyses temporal patterns and applies mathematical models to estimate future visitor volume without presenting invented data as evidence.

## 3. Objectives
- Import and preserve genuine traffic observations and their source.
- Calculate descriptive traffic statistics.
- demonstrate derivatives, curvature, critical points and numerical integration on fitted traffic curves.
- Compare chronological forecasting baselines using error metrics.
- Identify unusual observations and estimate visitor-volume headroom.
- Export calculated findings for review.

## 4. Proposed system
TrafficIQ uses a browser-based React frontend, FastAPI services and PostgreSQL persistence. The initial build includes CSV ingestion, site records, observation retrieval, analytics services and a subset of mathematical and forecasting methods.

## 5. Mathematical foundation
Let V(t) represent the fitted visitor curve. Its first derivative estimates rate of change, its second derivative describes curvature, and numerical integration approximates area under the curve. Discrete visitor totals remain a separate sum. Polynomial fitting is limited in degree and should not be extrapolated beyond its evidence range without validation.

## 6. Methodology
CSV timestamps are parsed and normalised to UTC. Missing values, invalid timestamps, negative counts and duplicate timestamps within a file are rejected. Forecast evaluation uses a chronological holdout and does not randomly shuffle observations. MAE, RMSE and sMAPE are calculated from held-out predictions.

## 7. Implementation status
See `../technical/IMPLEMENTATION_STATUS.md`. The frontend module screens, production authentication, GA4 integration, full tracking aggregation, logistic fitting and full academic report exports are incomplete.

## 8. Testing and results
[Insert only test cases actually executed, environment details, screenshots captured from the real application and results from a genuine dataset. Do not invent accuracy scores or test outcomes.]

## 9. Limitations and future work
Complete authenticated multi-user access, production tracker privacy controls, GA4 integration, seasonal aggregation, logistic model fitting, uncertainty intervals, richer visualisations and deployment hardening.

## 10. Conclusion
TrafficIQ establishes a data-first foundation for website traffic analysis and mathematical forecasting. Its credibility depends on genuine observations, chronological evaluation and transparent reporting of limitations.

## References
[Add only sources actually consulted, with complete bibliographic details and verified URLs.]
