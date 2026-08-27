# Reported-Result Reproduction Audit

## Reported values appearing in the submitted manuscript

| Specification                              |   reported_coefficient |   reported_se |   reported_p_value |   reported_n |
|:-------------------------------------------|-----------------------:|--------------:|-------------------:|-------------:|
| Reported two-way FE, raw DT, log quality   |               0.001015 |      0.001    |             0.31   |         6574 |
| Reported two-way FE, log DT, log quality   |               0.021026 |      0.011568 |             0.0691 |         6574 |
| Reported two-way FE, log DT, count OLS     |               0.125084 |      0.052239 |             0.0166 |         6574 |
| Reported year-FE Poisson, log DT           |               0.173469 |      0.054027 |             0.0013 |         6574 |
| Reported year-FE negative binomial, log DT |               0.264182 |      0.060419 |             0.0005 |         6574 |

## Independently regenerated values from the downloaded public data

| Specification                                                |   coefficient |          se |     p_value |   n_estimator |
|:-------------------------------------------------------------|--------------:|------------:|------------:|--------------:|
| Regenerated two-way FE, raw DT, log quality, full controls   |   0.000832071 | 0.000636157 | 0.191111    |          6443 |
| Regenerated two-way FE, log DT, log quality, full controls   |   0.0196279   | 0.0101615   | 0.0536213   |          6443 |
| Regenerated two-way FE, log DT, count OLS, full controls     |   0.116616    | 0.0458849   | 0.0111502   |          6443 |
| Regenerated two-way FE, log DT, log quality, basic controls  |   0.0209866   | 0.0102017   | 0.0398639   |          6443 |
| Regenerated two-way FE, log DT, log quality, no controls     |   0.0243041   | 0.0100454   | 0.0156782   |          6443 |
| Regenerated year-FE Poisson, log DT, full controls           |   0.174091    | 0.0555026   | 0.00170901  |          6574 |
| Regenerated year-FE negative binomial, log DT, full controls |   0.288869    | 0.0614067   | 2.54878e-06 |          6574 |

## Audit interpretation

The public-data match is exactly 6,574 firm-year observations for 1,468 firms, and the descriptive diagnostics in the manuscript are reproduced. However, the manuscript’s regression tables cannot be treated as fully reproducible until the exact preprocessing script, exact control set, and treatment of fixed-effect singletons are reconciled. In this regenerated pipeline, the high-dimensional OLS estimator reports 6,443 estimation observations after its fixed-effects preprocessing; the raw merged panel remains 6,574 observations. The final manuscript must distinguish these counts.

The year-FE count models are regenerated only as a diagnostic comparison. Their fixed-effect structure is not equivalent to the two-way FE models. They must not be described as a robustness test for within-firm causal inference. The two-way FE PPML result is separately reported in `reproduction_summary.md` and uses a smaller conditional estimation sample because all-zero outcome firms do not identify a firm Poisson effect.
