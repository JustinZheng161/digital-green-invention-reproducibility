# Model-upgrade sensitivity results

The file reports two pre-specified ablations and one robustness check. Ablation A compares a small theory-motivated block (`firm_size+leverage+roa+growth+soe`), a no-governance block (`leverage+cash_flow+firm_size+book_to_market+roa+growth+fixed_asset_ratio+equity_balance+largest_holder+employee_scale+soe`), and the locked full block. Ablation B removes the financial controls and retains size/governance controls. No specification is selected using its p-value. The robustness check clips raw DT at the sample 1st and 99th percentiles before applying `ln(1+DT)` and refits the identical firm/year fixed-effects models. The clipping thresholds are `0` and `134`.

These are association sensitivities under the matched observational design. Conditional PPML has a distinct estimator-retained sample because all-zero firms do not identify a conditional firm effect. The results must not be interpreted as causal effects or as a machine-learning accuracy score.
