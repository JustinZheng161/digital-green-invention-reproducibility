# Reproduction and Optimized-Model Run

## Sample and Key Validation

```json
{
  "green": {
    "rows": 11051,
    "firms": 1798,
    "years": [
      2014,
      2015,
      2016,
      2017,
      2018,
      2019,
      2020
    ],
    "duplicate_firm_year_rows": 0
  },
  "dt_full": {
    "rows": 17089,
    "firms": 3806,
    "years": [
      2008,
      2009,
      2010,
      2011,
      2012,
      2013,
      2014,
      2015,
      2016,
      2017,
      2018,
      2019,
      2020,
      2021
    ],
    "duplicate_firm_year_rows": 0
  },
  "dt_restricted_2014_2020": {
    "rows": 10563,
    "firms": 2743,
    "years": [
      2014,
      2015,
      2016,
      2017,
      2018,
      2019,
      2020
    ],
    "duplicate_firm_year_rows": 0
  },
  "matched_pre_complete_case": {
    "rows": 6574,
    "firms": 1468,
    "years": [
      2014,
      2015,
      2016,
      2017,
      2018,
      2019,
      2020
    ],
    "duplicate_firm_year_rows": 0
  },
  "matched_complete_case": {
    "rows": 6574,
    "firms": 1468,
    "years": [
      2014,
      2015,
      2016,
      2017,
      2018,
      2019,
      2020
    ],
    "duplicate_firm_year_rows": 0
  },
  "lagged_complete_case": {
    "rows": 4457,
    "firms": 1270,
    "years": [
      2015,
      2016,
      2017,
      2018,
      2019,
      2020
    ],
    "duplicate_firm_year_rows": 0
  }
}
```

## Model Results

| Model                                                 | Regressor   |   Coefficient |   SE (firm-clustered) |   p-value display |   95% CI lower |   95% CI upper |    N |
|:------------------------------------------------------|:------------|--------------:|----------------------:|------------------:|---------------:|---------------:|-----:|
| M0: OLS, log quality, raw DT, firm and year FE        | dt_raw      |   0.000832071 |           0.000636157 |            0.1911 |   -0.000414775 |     0.00207892 | 6443 |
| M1: OLS, log quality, log DT, firm and year FE        | log_dt      |   0.0196279   |           0.0101615   |            0.0536 |   -0.00028831  |     0.039544   | 6443 |
| M2: OLS, patent count, log DT, firm and year FE       | log_dt      |   0.116616    |           0.0458849   |            0.0112 |    0.0266835   |     0.206549   | 6443 |
| M3: PPML, patent count, log DT, firm and year FE      | log_dt      |   0.0933248   |           0.0506782   |            0.0655 |   -0.00600264  |     0.192652   | 2774 |
| M4: OLS, utility-patent log, log DT, firm and year FE | log_dt      |   0.015987    |           0.00884827  |            0.071  |   -0.00135529  |     0.0333293  | 6443 |
| M5: PPML, lagged DT, firm and year FE                 | log_dt_lag1 |   0.0528994   |           0.0591176   |            0.3709 |   -0.062969    |     0.168768   | 1891 |

## Diagnostics

|                                |     value |
|:-------------------------------|----------:|
| dt_total_sd                    | 26.2019   |
| dt_between_firm_sd             | 27.5684   |
| mean_dt_within_firm_sd         |  5.25106  |
| within_to_total_variance_ratio |  0.135923 |
| green_invention_zero_share     |  0.802251 |

## Specification Notes

All estimates include the declared firm-level controls and are clustered by firm. M0, M1, M2, M4 and M5 use firm and year fixed effects. M3 uses PPML with firm and year fixed effects, enabling a count-link model while retaining zero outcomes and absorbing time-invariant firm heterogeneity. Firms whose outcome is zero in every observed year do not identify a conditional Poisson firm effect and are therefore excluded by the estimator; its reported estimation sample must not be presented as identical to the OLS sample. The PPML estimator is an association model, not a causal design.

The raw and matched microdata are private outputs. This summary, aggregate tables and figures may be shared publicly only after a license and disclosure review.
