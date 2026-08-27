# Specification Sensitivity

Observed 1st/99th percentile of raw DT: **0 / 134**.

| Specification                                                          | Regressor               |   Coefficient |   SE (firm-clustered) |   p_value |    CI 95 low |   CI 95 high |   N used by estimator |   p-value display |
|:-----------------------------------------------------------------------|:------------------------|--------------:|----------------------:|----------:|-------------:|-------------:|----------------------:|------------------:|
| S1 OLS log quality; raw DT; full controls; firm/year FE                | dt_raw                  |   0.000832071 |           0.000636157 | 0.191111  | -0.000414775 |   0.00207892 |                  6443 |            0.1911 |
| S2 OLS log quality; winsorized raw DT; full controls; firm/year FE     | dt_winsor_1_99          |   0.00101013  |           0.00088185  | 0.25222   | -0.000718263 |   0.00273853 |                  6443 |            0.2522 |
| S3 OLS log quality; ln(1+DT); full controls; firm/year FE              | log_dt                  |   0.0196279   |           0.0101615   | 0.0536213 | -0.000288311 |   0.039544   |                  6443 |            0.0536 |
| S4 OLS log quality; ln(1+winsorized DT); full controls; firm/year FE   | log_dt_winsor_1_99      |   0.0194822   |           0.010198    | 0.056297  | -0.000505565 |   0.0394699  |                  6443 |            0.0563 |
| S5 OLS log quality; ln(1+winsorized DT); core controls; firm/year FE   | log_dt_winsor_1_99      |   0.0203456   |           0.0101566   | 0.045358  |  0.000439083 |   0.0402521  |                  6443 |            0.0454 |
| S6 PPML count; ln(1+winsorized DT); full controls; firm/year FE        | log_dt_winsor_1_99      |   0.0932056   |           0.0508403   | 0.0667576 | -0.0064395   |   0.192851   |                  2774 |            0.0668 |
| S7 PPML count; lagged ln(1+winsorized DT); full controls; firm/year FE | log_dt_lag1_winsor_1_99 |   0.052999    |           0.0591574   | 0.370307  | -0.0629474   |   0.168945   |                  1891 |            0.3703 |

## Interpretation rule

S1–S5 are two-way fixed-effects linear estimates on the identical matched complete-case panel. S6–S7 are conditional PPML estimates with firm and year fixed effects. The PPML procedures drop firms that have zero green-invention counts in every observed period because their firm effect is not identified; their estimation sample is therefore not directly comparable to the OLS sample. Sensitivity estimates are descriptive associations and do not establish causal effects.

The pre-specified decision rule for the manuscript is to report the raw-DT two-way fixed-effects model as a transparent linear benchmark and the log-transformed DT specification with two-way fixed effects as the main functional-form sensitivity result. PPML with firm and year fixed effects is reported as an outcome-distribution sensitivity, not as a replacement causal estimate.
