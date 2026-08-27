"""Specification-sensitivity analysis using the private matched panel.

This script does not select the most favorable model. It reports a declared set of
function-form and control-set choices so that conclusions cannot rely on one estimate.
"""
from pathlib import Path
import os
import json
import numpy as np
import pandas as pd
import pyfixest as pf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_DATA_ROOT = Path(os.environ.get('DGI_PRIVATE_DATA_ROOT', PROJECT_ROOT / 'data/private'))
DATA = PRIVATE_DATA_ROOT / 'derived/matched_panel_private.csv'
OUT = PROJECT_ROOT / 'results/tables'
OUT.mkdir(parents=True, exist_ok=True)

CONTROLS_FULL = [
    'leverage', 'cash_flow', 'firm_size', 'book_to_market', 'roa', 'growth',
    'fixed_asset_ratio', 'equity_balance', 'independent_directors', 'board_size',
    'largest_holder', 'employee_scale', 'ceo_duality', 'soe',
]
# A parsimonious alternative removes overlapping governance/scale proxies; it is a sensitivity model, not a post-hoc preferred model.
CONTROLS_CORE = [
    'leverage', 'cash_flow', 'firm_size', 'book_to_market', 'roa', 'growth',
    'fixed_asset_ratio', 'equity_balance', 'largest_holder', 'ceo_duality', 'soe',
]

def extract(label, fit, regressor):
    beta = float(fit.coef().loc[regressor])
    se = float(fit.se().loc[regressor])
    p = float(fit.pvalue().loc[regressor])
    return {
        'Specification': label,
        'Regressor': regressor,
        'Coefficient': beta,
        'SE (firm-clustered)': se,
        'p_value': p,
        'CI 95 low': beta - 1.959964 * se,
        'CI 95 high': beta + 1.959964 * se,
        'N used by estimator': int(fit._N),
    }

panel = pd.read_csv(DATA)
q01, q99 = panel['dt_raw'].quantile([0.01, 0.99])
panel['dt_winsor_1_99'] = panel['dt_raw'].clip(q01, q99)
panel['log_dt_winsor_1_99'] = np.log1p(panel['dt_winsor_1_99'])
panel['log_dt_lag1_winsor_1_99'] = panel.groupby('firm_id')['log_dt_winsor_1_99'].shift(1)
panel['previous_year_for_winsor_lag'] = panel.groupby('firm_id')['year'].shift(1)
panel.loc[panel['year'] - panel['previous_year_for_winsor_lag'] != 1, 'log_dt_lag1_winsor_1_99'] = np.nan

full = ' + '.join(CONTROLS_FULL)
core = ' + '.join(CONTROLS_CORE)
models = []

specs = [
    ('S1 OLS log quality; raw DT; full controls; firm/year FE', pf.feols, f'green_quality_log ~ dt_raw + {full} | firm_id + year', 'dt_raw', panel),
    ('S2 OLS log quality; winsorized raw DT; full controls; firm/year FE', pf.feols, f'green_quality_log ~ dt_winsor_1_99 + {full} | firm_id + year', 'dt_winsor_1_99', panel),
    ('S3 OLS log quality; ln(1+DT); full controls; firm/year FE', pf.feols, f'green_quality_log ~ log_dt + {full} | firm_id + year', 'log_dt', panel),
    ('S4 OLS log quality; ln(1+winsorized DT); full controls; firm/year FE', pf.feols, f'green_quality_log ~ log_dt_winsor_1_99 + {full} | firm_id + year', 'log_dt_winsor_1_99', panel),
    ('S5 OLS log quality; ln(1+winsorized DT); core controls; firm/year FE', pf.feols, f'green_quality_log ~ log_dt_winsor_1_99 + {core} | firm_id + year', 'log_dt_winsor_1_99', panel),
    ('S6 PPML count; ln(1+winsorized DT); full controls; firm/year FE', pf.fepois, f'green_invention_count ~ log_dt_winsor_1_99 + {full} | firm_id + year', 'log_dt_winsor_1_99', panel),
]
for label, estimator, formula, regressor, data in specs:
    models.append(extract(label, estimator(formula, data=data, vcov={'CRV1': 'firm_id'}), regressor))

lagged = panel.dropna(subset=['log_dt_lag1_winsor_1_99'])
lag_fit = pf.fepois(f'green_invention_count ~ log_dt_lag1_winsor_1_99 + {full} | firm_id + year', data=lagged, vcov={'CRV1': 'firm_id'})
models.append(extract('S7 PPML count; lagged ln(1+winsorized DT); full controls; firm/year FE', lag_fit, 'log_dt_lag1_winsor_1_99'))

results = pd.DataFrame(models)
results['p-value display'] = results['p_value'].map(lambda p: '<0.001' if p < 0.001 else f'{p:.4f}')
results.to_csv(OUT / 'specification_sensitivity.csv', index=False)

summary = [
    '# Specification Sensitivity',
    '',
    f'Observed 1st/99th percentile of raw DT: **{q01:.6g} / {q99:.6g}**.',
    '',
    results.to_markdown(index=False),
    '',
    '## Interpretation rule',
    '',
    'S1–S5 are two-way fixed-effects linear estimates on the identical matched complete-case panel. S6–S7 are conditional PPML estimates with firm and year fixed effects. The PPML procedures drop firms that have zero green-invention counts in every observed period because their firm effect is not identified; their estimation sample is therefore not directly comparable to the OLS sample. Sensitivity estimates are descriptive associations and do not establish causal effects.',
    '',
    'The pre-specified decision rule for the manuscript is to report the raw-DT two-way fixed-effects model as a transparent linear benchmark and the log-transformed DT specification with two-way fixed effects as the main functional-form sensitivity result. PPML with firm and year fixed effects is reported as an outcome-distribution sensitivity, not as a replacement causal estimate.',
]
(OUT / 'specification_sensitivity.md').write_text('\n'.join(summary) + '\n', encoding='utf-8')
(PRIVATE_DATA_ROOT / 'metadata/sensitivity_design.json').write_text(json.dumps({
    'dt_quantiles': {'q01': float(q01), 'q99': float(q99)},
    'full_controls': CONTROLS_FULL,
    'core_controls': CONTROLS_CORE,
    'decision_rule': 'Report linear two-way FE and log-DT two-way FE as complementary pre-specified functional-form evidence; report PPML FE as a count distribution sensitivity with its distinct estimation sample explicitly disclosed.'
}, ensure_ascii=False, indent=2), encoding='utf-8')
print((OUT / 'specification_sensitivity.md').read_text(encoding='utf-8'))
