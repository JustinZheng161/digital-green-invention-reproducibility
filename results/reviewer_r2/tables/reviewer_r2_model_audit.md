# Reviewer 2 Model and Sample Audit

## Scope and non-causal interpretation

All items below are descriptive, estimator-specific audits of a deterministic D1–D2 firm-year match and its observed covariate composition. They do not identify a causal effect, recover unmatched D2 values, or correct selection on unobserved determinants.

## Sample flow and estimator profiles

| Sample                           |   Observations |   Firms |   Years |   Year minimum |   Year maximum |   Share of matched complete-case observations |   Zero invention-count share |   Positive invention-count share |   Mean raw DT |   SD raw DT |   Mean log DT |   Mean firm size |   Mean ROA |   Mean leverage |   Mean green invention count |   Share of D1 green-source observations |
|:---------------------------------|---------------:|--------:|--------:|---------------:|---------------:|----------------------------------------------:|-----------------------------:|---------------------------------:|--------------:|------------:|--------------:|-----------------:|-----------:|----------------:|-----------------------------:|----------------------------------------:|
| D1 green-source file             |          11051 |    1798 |       7 |           2014 |           2020 |                                      nan      |                       0.8460 |                           0.1540 |      nan      |    nan      |      nan      |          22.6712 |     0.0326 |          0.4570 |                       0.6797 |                                  1.0000 |
| Matched complete-case panel      |           6574 |    1468 |       7 |           2014 |           2020 |                                        1.0000 |                       0.8023 |                           0.1977 |       10.6650 |     26.2019 |        1.3543 |          22.8760 |     0.0422 |          0.4686 |                       0.9439 |                                  0.5949 |
| TWFE log-outcome retained sample |           6443 |    1337 |       7 |           2014 |           2020 |                                        0.9801 |                       0.8010 |                           0.1990 |       10.5763 |     25.7141 |        1.3523 |          22.8932 |     0.0422 |          0.4707 |                       0.9569 |                                  0.5830 |
| Conditional PPML retained sample |           2774 |     505 |       7 |           2014 |           2020 |                                        0.4220 |                       0.5379 |                           0.4621 |       11.2996 |     27.2967 |        1.4097 |          23.4745 |     0.0411 |          0.5193 |                       2.2224 |                                  0.2510 |
| Strict t−1 PPML retained sample  |           1891 |     418 |       6 |           2015 |           2020 |                                        0.2876 |                       0.4839 |                           0.5161 |       11.5875 |     27.6145 |        1.4476 |          23.6466 |     0.0420 |          0.5276 |                       2.5754 |                                  0.1711 |
| Strict t+1 PPML retained sample  |           1742 |     387 |       6 |           2014 |           2019 |                                        0.2650 |                       0.4960 |                           0.5040 |       10.7222 |     26.0183 |        1.3533 |          23.5650 |     0.0434 |          0.5233 |                       2.4506 |                                  0.1576 |

## Conditional PPML zero-firm boundary

|   Matched complete-case firms |   Firms with zero collaborative green inventions in all observed years |   Share of complete-case firms that are all-zero |   Matched complete-case observations from all-zero firms |   Share of complete-case observations from all-zero firms |   Conditional PPML retained observations |   Conditional PPML retained firms |
|------------------------------:|-----------------------------------------------------------------------:|-------------------------------------------------:|---------------------------------------------------------:|----------------------------------------------------------:|-----------------------------------------:|----------------------------------:|
|                     1468.0000 |                                                               945.0000 |                                           0.6437 |                                                3782.0000 |                                                    0.5753 |                                2774.0000 |                          505.0000 |

| Stage / observed outcome group                               |   Observations |   Firms |   Share of matched observations |
|:-------------------------------------------------------------|---------------:|--------:|--------------------------------:|
| Matched complete-case panel                                  |           6574 |    1468 |                          1.0000 |
| All-zero-invention firms (not retained by conditional PPML)  |           3782 |     945 |                          0.5753 |
| Ever-positive firms removed by PPML preprocessing/separation |             18 |      18 |                          0.0027 |
| Conditional PPML retained contribution set                   |           2774 |     505 |                          0.4220 |

The conditional PPML sample is the set retained by the high-dimensional fixed-effect estimator. It is not a treated group, and it does not represent the all-zero-invention population. The decomposition separates observed all-zero firms from the small residual group removed by estimator preprocessing/separation; it does not interpret either removal as random sampling.

## PPML and strict-timing sample comparison

| Comparison baseline         | Estimator sample          | Variable              |   Source mean |   Comparison mean |     SMD |   Absolute SMD |
|:----------------------------|:--------------------------|:----------------------|--------------:|------------------:|--------:|---------------:|
| Matched complete-case panel | TWFE log-outcome retained | firm_size             |       22.8760 |           22.8932 |  0.0137 |         0.0137 |
| Matched complete-case panel | Conditional PPML retained | firm_size             |       22.8760 |           23.4745 |  0.4696 |         0.4696 |
| Matched complete-case panel | Strict t−1 PPML retained  | firm_size             |       22.8760 |           23.6466 |  0.6110 |         0.6110 |
| Matched complete-case panel | TWFE log-outcome retained | roa                   |        0.0422 |            0.0422 |  0.0007 |         0.0007 |
| Matched complete-case panel | Conditional PPML retained | roa                   |        0.0422 |            0.0411 | -0.0311 |         0.0311 |
| Matched complete-case panel | Strict t−1 PPML retained  | roa                   |        0.0422 |            0.0420 | -0.0065 |         0.0065 |
| Matched complete-case panel | TWFE log-outcome retained | leverage              |        0.4686 |            0.4707 |  0.0130 |         0.0130 |
| Matched complete-case panel | Conditional PPML retained | leverage              |        0.4686 |            0.5193 |  0.3101 |         0.3101 |
| Matched complete-case panel | Strict t−1 PPML retained  | leverage              |        0.4686 |            0.5276 |  0.3675 |         0.3675 |
| Matched complete-case panel | TWFE log-outcome retained | dt_raw                |       10.6650 |           10.5763 | -0.0034 |         0.0034 |
| Matched complete-case panel | Conditional PPML retained | dt_raw                |       10.6650 |           11.2996 |  0.0237 |         0.0237 |
| Matched complete-case panel | Strict t−1 PPML retained  | dt_raw                |       10.6650 |           11.5875 |  0.0343 |         0.0343 |
| Matched complete-case panel | TWFE log-outcome retained | log_dt                |        1.3543 |            1.3523 | -0.0015 |         0.0015 |
| Matched complete-case panel | Conditional PPML retained | log_dt                |        1.3543 |            1.4097 |  0.0412 |         0.0412 |
| Matched complete-case panel | Strict t−1 PPML retained  | log_dt                |        1.3543 |            1.4476 |  0.0694 |         0.0694 |
| Matched complete-case panel | TWFE log-outcome retained | green_invention_count |        0.9439 |            0.9569 |  0.0041 |         0.0041 |
| Matched complete-case panel | Conditional PPML retained | green_invention_count |        0.9439 |            2.2224 |  0.3231 |         0.3231 |
| Matched complete-case panel | Strict t−1 PPML retained  | green_invention_count |        0.9439 |            2.5754 |  0.3948 |         0.3948 |

## Exact sample overlap

| Pair                                    |   Observation intersection |   Share of matched observations |   Firm intersection |   Share of matched firms |
|:----------------------------------------|---------------------------:|--------------------------------:|--------------------:|-------------------------:|
| PPML / matched complete-case            |                       2774 |                          0.4220 |                 505 |                   0.3440 |
| Strict t−1 PPML / matched complete-case |                       1891 |                          0.2876 |                 418 |                   0.2847 |
| Strict t−1 PPML / conditional PPML      |                       1891 |                          0.2876 |                 418 |                   0.8277 |

## Strict timing estimates and support

| Test                           | Relation                |   Coefficient |   Firm-clustered SE |   p_value |   95% CI lower |   95% CI upper |   Candidate observations before conditional PPML |   Retained observations |   Retained firms |   Retained years | Year range   |   Share of matched complete-case observations |
|:-------------------------------|:------------------------|--------------:|--------------------:|----------:|---------------:|---------------:|-------------------------------------------------:|------------------------:|-----------------:|-----------------:|:-------------|----------------------------------------------:|
| Strict t−1 log DT PPML         | Prior calendar year     |        0.0529 |              0.0591 |    0.3709 |        -0.0630 |         0.1688 |                                             4457 |                    1891 |              418 |                6 | 2015–2020    |                                        0.2876 |
| Strict t+1 log DT PPML placebo | Following calendar year |        0.0910 |              0.0590 |    0.1229 |        -0.0246 |         0.2066 |                                             4457 |                    1742 |              387 |                6 | 2014–2019    |                                        0.2650 |

| Test       | Relationship                           |   Outcome year |   Matched complete-case observations |   Candidate observations |   Retained PPML observations |   Candidate firms |   Retained PPML firms |
|:-----------|:---------------------------------------|---------------:|-------------------------------------:|-------------------------:|-----------------------------:|------------------:|----------------------:|
| Strict t−1 | DT measured in preceding calendar year |           2014 |                                  826 |                        0 |                            0 |                 0 |                     0 |
| Strict t−1 | DT measured in preceding calendar year |           2015 |                                  821 |                      601 |                          262 |               601 |                   262 |
| Strict t−1 | DT measured in preceding calendar year |           2016 |                                  930 |                      674 |                          289 |               674 |                   289 |
| Strict t−1 | DT measured in preceding calendar year |           2017 |                                  978 |                      763 |                          322 |               763 |                   322 |
| Strict t−1 | DT measured in preceding calendar year |           2018 |                                  998 |                      791 |                          332 |               791 |                   332 |
| Strict t−1 | DT measured in preceding calendar year |           2019 |                                 1049 |                      820 |                          350 |               820 |                   350 |
| Strict t−1 | DT measured in preceding calendar year |           2020 |                                  972 |                      808 |                          336 |               808 |                   336 |
| Strict t+1 | DT measured in following calendar year |           2014 |                                  826 |                      601 |                          244 |               601 |                   244 |
| Strict t+1 | DT measured in following calendar year |           2015 |                                  821 |                      674 |                          264 |               674 |                   264 |
| Strict t+1 | DT measured in following calendar year |           2016 |                                  930 |                      763 |                          296 |               763 |                   296 |
| Strict t+1 | DT measured in following calendar year |           2017 |                                  978 |                      791 |                          309 |               791 |                   309 |
| Strict t+1 | DT measured in following calendar year |           2018 |                                  998 |                      820 |                          320 |               820 |                   320 |
| Strict t+1 | DT measured in following calendar year |           2019 |                                 1049 |                      808 |                          309 |               808 |                   309 |
| Strict t+1 | DT measured in following calendar year |           2020 |                                  972 |                        0 |                            0 |                 0 |                     0 |

The strict t−1 candidate excludes outcome year 2014 by construction because no preceding calendar-year DT value can exist. Additional reduction reflects an unbalanced panel and conditional PPML retention; the year table reports both candidate and retained observations.

## Availability calibration (not treatment IPW)

The selection model is a logit for deterministic D1–D2 matched availability conditional on D1 firm size, ROA and calendar year. It is a selection-on-observables calibration / covariate-balance diagnostic. “Propensity” is not used for treatment assignment, policy exposure, causal weighting, or correction for unobserved confounding.

| Availability model                                                             |   Availability model observations |   D1 green-source observations |   Matched complete-case observations |   Matched availability share |   McFadden pseudo R2 |   Matched probability min |   Matched probability p1 |   Matched probability median |   Matched probability p99 |   Matched probability max |   Stabilized weight min |   Stabilized weight p1 |   Stabilized weight median |   Stabilized weight p99 |   Stabilized weight max | Trimming cutpoints (p1/p99)   |   Effective sample size after trimming |
|:-------------------------------------------------------------------------------|----------------------------------:|-------------------------------:|-------------------------------------:|-----------------------------:|---------------------:|--------------------------:|-------------------------:|-----------------------------:|--------------------------:|--------------------------:|------------------------:|-----------------------:|---------------------------:|------------------------:|------------------------:|:------------------------------|---------------------------------------:|
| Logit: matched D1–D2 availability ~ firm size + ROA + calendar-year indicators |                             11051 |                          11051 |                                 6574 |                       0.5949 |               0.0668 |                    0.0863 |                   0.3957 |                       0.6264 |                    0.8834 |                    0.9556 |                  0.6225 |                 0.6734 |                     0.9497 |                  1.5035 |                  6.8895 | 0.673414 / 1.503480           |                              6228.0675 |

| Model                                                               | Availability weighted   | Outcome covariates beyond FE        |   Coefficient on ln(1+DT) |   Firm-clustered SE |   p_value |   95% CI lower |   95% CI upper |    N |
|:--------------------------------------------------------------------|:------------------------|:------------------------------------|--------------------------:|--------------------:|----------:|---------------:|---------------:|-----:|
| Unweighted FE reference; no selection covariates                    | False                   | None beyond firm/year fixed effects |                    0.0243 |              0.0113 |    0.0313 |         0.0022 |         0.0464 | 6443 |
| Availability-weighted FE calibration; no selection covariates       | True                    | None beyond firm/year fixed effects |                    0.0211 |              0.0106 |    0.0476 |         0.0002 |         0.0419 | 6443 |
| Unweighted FE reference; selection covariates included              | False                   | Firm size and ROA                   |                    0.0217 |              0.0115 |    0.0587 |        -0.0008 |         0.0442 | 6443 |
| Availability-weighted FE calibration; selection covariates included | True                    | Firm size and ROA                   |                    0.0176 |              0.0108 |    0.1030 |        -0.0036 |         0.0388 | 6443 |

| Variable              | Comparison                                                   |   Source mean |   Comparison mean |    SMD |   Absolute SMD |
|:----------------------|:-------------------------------------------------------------|--------------:|------------------:|-------:|---------------:|
| firm_size             | D1 source vs retained matched sample (unweighted)            |       22.6712 |           22.8932 | 0.1759 |         0.1759 |
| firm_size             | D1 source vs retained matched sample (availability-weighted) |       22.6712 |           22.7221 | 0.0409 |         0.0409 |
| roa                   | D1 source vs retained matched sample (unweighted)            |        0.0326 |            0.0422 | 0.2170 |         0.2170 |
| roa                   | D1 source vs retained matched sample (availability-weighted) |        0.0326 |            0.0388 | 0.1436 |         0.1436 |
| leverage              | D1 source vs retained matched sample (unweighted)            |        0.4570 |            0.4707 | 0.0788 |         0.0788 |
| leverage              | D1 source vs retained matched sample (availability-weighted) |        0.4570 |            0.4656 | 0.0492 |         0.0492 |
| cash_flow             | D1 source vs retained matched sample (unweighted)            |        0.0480 |            0.0520 | 0.0667 |         0.0667 |
| cash_flow             | D1 source vs retained matched sample (availability-weighted) |        0.0480 |            0.0486 | 0.0101 |         0.0101 |
| growth                | D1 source vs retained matched sample (unweighted)            |        0.1507 |            0.1769 | 0.0753 |         0.0753 |
| growth                | D1 source vs retained matched sample (availability-weighted) |        0.1507 |            0.1729 | 0.0636 |         0.0636 |
| green_invention_count | D1 source vs retained matched sample (unweighted)            |        0.6797 |            0.9569 | 0.0941 |         0.0941 |
| green_invention_count | D1 source vs retained matched sample (availability-weighted) |        0.6797 |            0.8018 | 0.0440 |         0.0440 |

The weighted/no-covariate and weighted/selection-covariate variants are both reported to expose sensitivity to simultaneous weighting and regression adjustment. Neither is a causal estimate. If their direction differs, that is uncertainty rather than evidence for model selection.
