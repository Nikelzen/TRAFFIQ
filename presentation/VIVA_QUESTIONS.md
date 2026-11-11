# TrafficIQ viva questions (starter bank)

1. What problem does TrafficIQ address? — It analyses historical website traffic and estimates future visitor volume.
2. Why must the data be genuine? — Fabricated inputs invalidate analysis and evaluation.
3. What is V(t)? — Website visitors represented as a function of time.
4. What does V'(t) mean? — The local rate of change of the fitted traffic curve.
5. What does V''(t) indicate? — The curve's local curvature or acceleration.
6. What is a critical point? — An interior candidate where the first derivative is zero or undefined.
7. Why check derivative signs around a critical point? — To distinguish maxima, minima and stationary points.
8. What is an inflection point? — A point where concavity changes.
9. Why is V''(t)=0 alone insufficient? — A zero need not correspond to a sign change.
10. What does integration represent here? — Approximate area under the traffic curve, not the discrete visitor sum.
11. Why normalise polynomial time coordinates? — To improve numerical conditioning.
12. What is polynomial overfitting? — A curve fitting noise rather than general temporal structure.
13. What is logistic growth? — Growth that slows as it approaches a carrying capacity.
14. When is logistic growth inappropriate? — When observations do not support saturation-like behaviour.
15. What is a naive forecast? — Repeating the latest observed value.
16. What is seasonal naive forecasting? — Repeating values from a previous seasonal cycle.
17. Why not shuffle time-series data? — It leaks future information into training.
18. What is MAE? — Mean absolute prediction error.
19. What is RMSE? — Square root of mean squared error; it penalises large errors more.
20. What is sMAPE? — A symmetric percentage-style error measure with a zero-safe denominator.
21. Why can MAPE be unsuitable? — It is undefined or unstable when actual values are zero or near zero.
22. What is MAD? — Median absolute deviation, a robust spread measure.
23. Does an anomaly prove an attack? — No, it only identifies an unusual observation.
24. What does capacity headroom mean? — Additional visitor-volume allowance above forecast peak demand.
25. Why cannot visitor counts directly predict CPU usage? — Resource usage requires infrastructure measurements or a calibrated model.
26. Why use PostgreSQL? — It provides relational integrity, constraints and indexing for persisted observations.
27. What does FastAPI provide? — Typed API endpoints, validation and OpenAPI documentation.
28. Why store dataset provenance? — To identify where observations originated.
29. What is the current authentication limitation? — Owner identifiers are temporary and not secure; production identity integration is required.
30. What is the most important limitation before deployment? — Production authentication/authorization and privacy hardening are not yet complete.
