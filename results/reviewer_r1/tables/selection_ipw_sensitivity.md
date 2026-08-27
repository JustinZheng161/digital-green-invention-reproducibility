# Observed-Covariate Selection Calibration (IPW Sensitivity)

The propensity model predicts D1–D2 matched-panel availability using the D1 controls and calendar-year indicators. It **does not** use patent outcomes and cannot correct selection on unobserved determinants, different source-population frames, or DT values unavailable for unmatched observations. It is therefore a sensitivity analysis for observed covariate imbalance, not an identification strategy.

## Weight diagnostics

|   D1 source observations |   Matched observations |   Matched share |   Propensity min in matched |   Propensity p1 in matched |   Propensity median in matched |   Propensity p99 in matched |   Propensity max in matched |   Stabilized IPW mean before winsor | Stabilized IPW p1/p99   |   Pseudo R2 selection logit |
|-------------------------:|-----------------------:|----------------:|----------------------------:|---------------------------:|-------------------------------:|----------------------------:|----------------------------:|------------------------------------:|:------------------------|----------------------------:|
|                    11051 |                   6574 |        0.594878 |                    0.101862 |                   0.289786 |                       0.664517 |                    0.930264 |                    0.978436 |                            0.968325 | 0.639473 / 2.052822     |                     0.11253 |

## Weighted two-way-FE linear sensitivity

| Model                                                   |   Coefficient on ln(1+DT) |   Firm-clustered SE |   p_value |   CI 95 lower |   CI 95 upper |    N |
|:--------------------------------------------------------|--------------------------:|--------------------:|----------:|--------------:|--------------:|-----:|
| Unweighted dummy-FE reference                           |                 0.0196279 |           0.0114186 | 0.0856263 |   -0.00275222 |     0.0420079 | 6443 |
| Stabilized IPW (1%/99% winsorized) dummy-FE sensitivity |                 0.0174571 |           0.0108708 | 0.108302  |   -0.00384926 |     0.0387635 | 6443 |

The weighted result should be interpreted only as: “after reweighting matched observations toward the D1 green-source distribution on observed D1 controls and year, the linear association has the following value.” It does not permit extrapolation to all listed firms or resolve causal confounding.
