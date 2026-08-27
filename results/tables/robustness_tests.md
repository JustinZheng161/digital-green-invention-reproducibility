# Robustness and Timing Tests

| Test                                                        |   Coefficient |   SE (firm-clustered) |   p_value |   95% CI lower |   95% CI upper |   N used by estimator |   p-value display |
|:------------------------------------------------------------|--------------:|----------------------:|----------:|---------------:|---------------:|----------------------:|------------------:|
| R1 Timing: PPML count with strict t−1 log DT; firm/year FE  |     0.0528994 |             0.0591176 |  0.370885 |     -0.062969  |      0.168768  |                  1891 |            0.3709 |
| R2 Placebo: PPML count with strict t+1 log DT; firm/year FE |     0.0910102 |             0.0589892 |  0.122872 |     -0.0246065 |      0.206627  |                  1742 |            0.1229 |
| R3a Period: 2014–2017 OLS log quality; firm/year FE         |     0.0103719 |             0.0126067 |  0.410849 |     -0.0143368 |      0.0350805 |                  3338 |            0.4108 |
| R3b Period: 2018–2020 OLS log quality; firm/year FE         |     0.0105489 |             0.0215505 |  0.624592 |     -0.0316893 |      0.0527872 |                  2753 |            0.6246 |

## Interpretation rule

R1 replaces a merely adjacent-record lag with a strict calendar-year lag. R2 is a future-exposure placebo: a non-null coefficient would be consistent with reverse timing, serial persistence, or omitted trends, so it cannot support a causal claim. R3a/R3b examine period sensitivity in the linear log-quality model; the short late subsample has fewer within-firm time changes and should be interpreted cautiously. As with the main models, conditional PPML excludes firms with all-zero invention counts in the relevant period.
