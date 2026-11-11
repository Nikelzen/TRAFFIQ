# Mathematical foundation

Let V(t) denote the observed visitor count at time t. Observations are discrete; a polynomial curve is an approximation used to study local shape, not a claim that visitors are continuous.

## First derivative
V'(t) estimates the local rate of change. Positive values indicate an increasing fitted curve; negative values indicate a decreasing fitted curve. Units are visitors per chosen time unit.

## Second derivative
V''(t) describes curvature/acceleration of the fitted curve. Its sign alone does not identify a traffic increase or decrease.

## Critical points
Candidate points satisfy V'(t)=0. The implementation classifies local maxima/minima by checking the sign of the first derivative immediately on either side. Endpoints are not treated as interior critical points.

## Inflection points
A candidate root of V''(t)=0 is accepted only when the second derivative changes sign across it. A zero alone is insufficient.

## Integration
The implementation uses the trapezoidal rule over timestamp coordinates to approximate the area under the observed traffic curve. This has units of visitor-observation-time and is not the same as summing discrete visitor counts.

## Polynomial model
A bounded-degree polynomial is fitted using normalised time coordinates for numerical stability. Degree is capped to reduce overfitting. Extrapolation outside the observed time range is not performed by the calculus fit.

## Logistic growth
The logistic differential equation is dV/dt=rV(1−V/K), with solution V(t)=K/(1+Ae^(−rt)). It assumes growth toward a stable carrying capacity. This initial build documents the model but does not yet fit it; no logistic output should be reported as implemented.
