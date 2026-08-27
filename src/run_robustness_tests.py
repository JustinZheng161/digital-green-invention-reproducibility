"""Robustness tests for timing and period sensitivity.

A future-DT placebo is a diagnostic for timing and persistence, not a valid instrument.
All causal interpretations remain outside the scope of the available data and design.
"""
from pathlib import Path
import os
import numpy as np
import pandas as pd
import pyfixest as pf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_DATA_ROOT = Path(os.environ.get('DGI_PRIVATE_DATA_ROOT', PROJECT_ROOT / 'data/private'))
panel = pd.read_csv(PRIVATE_DATA_ROOT / 'derived/matched_panel_private.csv').sort_values(['firm_id', 'year']).reset_index(drop=True)
OUT = PROJECT_ROOT / 'results/tables'
OUT.mkdir(parents=True, exist_ok=True)
CONTROLS = [
    'leverage', 'cash_flow', 'firm_size', 'book_to_market', 'roa', 'growth',
    'fixed_asset_ratio', 'equity_balance', 'independent_directors', 'board_size',
    'largest_holder', 'employee_scale', 'ceo_duality', 'soe',
]
controls = ' + '.join(CONTROLS)

# Calendar-consistent lags and leads rather than merely the previous/next observed row.
panel['previous_year_check'] = panel.groupby('firm_id')['year'].shift(1)
panel['next_year_check'] = panel.groupby('firm_id')['year'].shift(-1)
panel['log_dt_lag1_strict'] = panel.groupby('firm_id')['log_dt'].shift(1)
panel['log_dt_lead1_strict'] = panel.groupby('firm_id')['log_dt'].shift(-1)
panel.loc[panel['year'] - panel['previous_year_check'] != 1, 'log_dt_lag1_strict'] = np.nan
panel.loc[panel['next_year_check'] - panel['year'] != 1, 'log_dt_lead1_strict'] = np.nan


def summarize(label, estimator, formula, data, variable):
    fit = estimator(formula, data=data, vcov={'CRV1': 'firm_id'})
    beta = float(fit.coef().loc[variable])
    se = float(fit.se().loc[variable])
    return {
        'Test': label,
        'Coefficient': beta,
        'SE (firm-clustered)': se,
        'p_value': float(fit.pvalue().loc[variable]),
        '95% CI lower': beta - 1.959964 * se,
        '95% CI upper': beta + 1.959964 * se,
        'N used by estimator': int(fit._N),
    }

rows = []
lagged = panel.dropna(subset=['log_dt_lag1_strict'])
rows.append(summarize(
    'R1 Timing: PPML count with strict t−1 log DT; firm/year FE',
    pf.fepois,
    f'green_invention_count ~ log_dt_lag1_strict + {controls} | firm_id + year',
    lagged,
    'log_dt_lag1_strict'))

leading = panel.dropna(subset=['log_dt_lead1_strict'])
rows.append(summarize(
    'R2 Placebo: PPML count with strict t+1 log DT; firm/year FE',
    pf.fepois,
    f'green_invention_count ~ log_dt_lead1_strict + {controls} | firm_id + year',
    leading,
    'log_dt_lead1_strict'))

for name, years in [('R3a Period: 2014–2017 OLS log quality; firm/year FE', [2014, 2015, 2016, 2017]),
                    ('R3b Period: 2018–2020 OLS log quality; firm/year FE', [2018, 2019, 2020])]:
    sub = panel[panel['year'].isin(years)].copy()
    rows.append(summarize(name, pf.feols, f'green_quality_log ~ log_dt + {controls} | firm_id + year', sub, 'log_dt'))

results = pd.DataFrame(rows)
results['p-value display'] = results['p_value'].map(lambda p: '<0.001' if p < 0.001 else f'{p:.4f}')
results.to_csv(OUT / 'robustness_tests.csv', index=False)

text = [
    '# Robustness and Timing Tests',
    '',
    results.to_markdown(index=False),
    '',
    '## Interpretation rule',
    '',
    'R1 replaces a merely adjacent-record lag with a strict calendar-year lag. R2 is a future-exposure placebo: a non-null coefficient would be consistent with reverse timing, serial persistence, or omitted trends, so it cannot support a causal claim. R3a/R3b examine period sensitivity in the linear log-quality model; the short late subsample has fewer within-firm time changes and should be interpreted cautiously. As with the main models, conditional PPML excludes firms with all-zero invention counts in the relevant period.',
]
(OUT / 'robustness_tests.md').write_text('\n'.join(text) + '\n', encoding='utf-8')
print((OUT / 'robustness_tests.md').read_text(encoding='utf-8'))
