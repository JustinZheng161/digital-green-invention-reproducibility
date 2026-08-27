# Reviewer 1 Supplementary Statistical Analyses

## A. Count-OLS diagnostic and status

The two-way-fixed-effect OLS count model is reported only as a descriptive linear sensitivity. It is not the preferred count specification because the outcome has a large zero mass. Conditional PPML is retained as the preferred count model; it also has a different effective sample because all-zero firms do not identify a conditional firm effect.

|                                              | Value                                |
|:---------------------------------------------|:-------------------------------------|
| Diagnostic                                   | OLS count model residual diagnostics |
| N                                            | 6443                                 |
| Mean residual                                | 3.1492424685414116e-14               |
| Residual SD                                  | 1.5627561859636458                   |
| Shapiro-Wilk W (deterministic n=5000 subset) | 0.6224652385162567                   |
| Shapiro-Wilk p                               | 3.4214891980113264e-74               |
| Jarque-Bera statistic (full sample)          | 151532.43210919862                   |
| Jarque-Bera p                                | 0.0                                  |
| Koenker-Breusch-Pagan LM                     | 3214.615024177775                    |
| Koenker-Breusch-Pagan p                      | 6.360657454558342e-152               |
| Cook threshold 4/N                           | 0.0006208288064566196                |
| Max Cook distance                            | 0.020107507613758253                 |
| Observations above 4/N                       | 309                                  |
| Share above 4/N                              | 0.04795902529877386                  |

Shapiro–Wilk is run on a fixed, reproducible random subset of 5,000 residuals because its p-value calibration is documented as inaccurate for larger N. Jarque–Bera and robust Koenker–Breusch–Pagan are shown for the full diagnostic sample. With a discrete zero-heavy outcome, residual normality rejection is expected and is not used to make a causal conclusion; it supports demoting count-OLS below PPML.

## B. Multiple-comparison adjustment

| Specification                                                        | Regressor          |   Coefficient |   SE (firm-clustered) |   p_value |    CI 95 low |   CI 95 high |   N used by estimator |   p-value display |   Bonferroni p |   Holm p |   BH-FDR q | Unadjusted significant at .05   | Holm significant at .05   | Bonferroni significant at .05   |
|:---------------------------------------------------------------------|:-------------------|--------------:|----------------------:|----------:|-------------:|-------------:|----------------------:|------------------:|---------------:|---------:|-----------:|:--------------------------------|:--------------------------|:--------------------------------|
| S1 OLS log quality; raw DT; full controls; firm/year FE              | dt_raw             |   0.000832071 |           0.000636157 | 0.191111  | -0.000414775 |   0.00207892 |                  6443 |            0.1911 |       0.955553 | 0.382221 |  0.238888  | False                           | False                     | False                           |
| S2 OLS log quality; winsorized raw DT; full controls; firm/year FE   | dt_winsor_1_99     |   0.00101013  |           0.00088185  | 0.25222   | -0.000718263 |   0.00273853 |                  6443 |            0.2522 |       1        | 0.382221 |  0.25222   | False                           | False                     | False                           |
| S3 OLS log quality; ln(1+DT); full controls; firm/year FE            | log_dt             |   0.0196279   |           0.0101615   | 0.0536213 | -0.000288311 |   0.039544   |                  6443 |            0.0536 |       0.268106 | 0.22679  |  0.0938284 | False                           | False                     | False                           |
| S4 OLS log quality; ln(1+winsorized DT); full controls; firm/year FE | log_dt_winsor_1_99 |   0.0194822   |           0.010198    | 0.056297  | -0.000505565 |   0.0394699  |                  6443 |            0.0563 |       0.281485 | 0.22679  |  0.0938284 | False                           | False                     | False                           |
| S5 OLS log quality; ln(1+winsorized DT); core controls; firm/year FE | log_dt_winsor_1_99 |   0.0203456   |           0.0101566   | 0.045358  |  0.000439083 |   0.0402521  |                  6443 |            0.0454 |       0.22679  | 0.22679  |  0.0938284 | True                            | False                     | False                           |

The declared S1–S5 family contains five variations of one question: the two-way-fixed-effect association between DT and the same log collaborative-green-invention outcome. The Bonferroni threshold is 0.0100 (=0.05/5). No model in this family is significant after Holm, Bonferroni, or BH-FDR adjustment. Results are accordingly described as estimation uncertainty, not as a robust positive association.

## C. Sample-selection diagnostics

| Variable              |   Green-source mean |   Matched-panel mean |   Mean difference |   Pooled SD |   Standardized mean difference |   Absolute SMD |   Green-source N |   Matched-panel N |
|:----------------------|--------------------:|---------------------:|------------------:|------------:|-------------------------------:|---------------:|-----------------:|------------------:|
| firm_size             |          22.6712    |           22.876     |        0.204819   |   1.26205   |                      0.16229   |      0.16229   |            11051 |              6574 |
| roa                   |           0.0325669 |            0.0421752 |        0.00960827 |   0.0443819 |                      0.216491  |      0.216491  |            11051 |              6574 |
| leverage              |           0.457039  |            0.468559  |        0.0115203  |   0.173873  |                      0.0662571 |      0.0662571 |            11051 |              6574 |
| cash_flow             |           0.0480035 |            0.0519024 |        0.00389898 |   0.0596037 |                      0.0654151 |      0.0654151 |            11051 |              6574 |
| book_to_market        |           0.647081  |            0.659676  |        0.0125953  |   0.254002  |                      0.0495874 |      0.0495874 |            11051 |              6574 |
| growth                |           0.150711  |            0.177132  |        0.0264209  |   0.349524  |                      0.0755911 |      0.0755911 |            11051 |              6574 |
| green_output_log      |           1.10421   |            1.40611   |        0.3019     |   1.35364   |                      0.223028  |      0.223028  |            11051 |              6574 |
| green_invention_count |           0.679667  |            0.94387   |        0.264203   |   2.93025   |                      0.090164  |      0.090164  |            11051 |              6574 |
| green_quality_log     |           0.208571  |            0.27694   |        0.0683695  |   0.614359  |                      0.111286  |      0.111286  |            11051 |              6574 |

Positive SMD means the matched complete-case panel has a higher mean than the full green-innovation source. SMD is a descriptive balance metric, not a causal correction. The graph `selection_love_plot.png` displays absolute SMDs, including a 0.10 visual reference.

## D. Two-part descriptive decomposition

| Component                                                            |   Coefficient |   Firm-clustered SE |   p_value |   CI 95 lower |   CI 95 upper |   N used by estimator |
|:---------------------------------------------------------------------|--------------:|--------------------:|----------:|--------------:|--------------:|----------------------:|
| Extensive margin: Pr(count > 0), TWFE linear probability sensitivity |     0.0046588 |          0.00752146 |  0.535758 |    -0.010083  |     0.0194006 |                  6443 |
| Intensive margin: ln(count) | count > 0, TWFE OLS sensitivity        |     0.0652997 |          0.0506259  |  0.198049 |    -0.0339252 |     0.164525  |                  1093 |

This is not a ZIP or a structural hurdle model. It is a descriptive decomposition that separates current positive-count occurrence from logged count conditional on positivity, while retaining firm/year fixed effects in each linear component. It clarifies target populations without imposing an unverified zero-generating process.

## E. Descriptive statistics and correlations

See `appendix_descriptive_statistics.csv`, `appendix_correlation_pearson.csv`, and `appendix_correlation_spearman.csv`. The compact manuscript tables use a subset; full numeric tables are retained as supplement files.
