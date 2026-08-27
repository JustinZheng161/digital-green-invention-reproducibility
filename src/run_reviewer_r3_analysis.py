"""R3 non-causal sensitivity analysis and PPML diagnostics.

This script writes only aggregate diagnostics and coefficients. It never exports firm-year
records, firm identifiers, raw source values, or manuscript files. Results are descriptive
because the deterministic two-source match and observational design do not identify causality.
"""
from __future__ import annotations

from pathlib import Path
import json
import math
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyfixest as pf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path(os.environ.get('DGI_PRIVATE_DATA_ROOT', PROJECT_ROOT / 'data' / 'private'))
RESULTS = Path(os.environ.get('DGI_R3_RESULTS_ROOT', PROJECT_ROOT / 'results' / 'reviewer_r3'))
TABLES, FIGURES = RESULTS / 'tables', RESULTS / 'figures'
for folder in (TABLES, FIGURES):
    folder.mkdir(parents=True, exist_ok=True)
PANEL_PATH = PRIVATE / 'derived' / 'matched_panel_private.csv'
GREEN_PATH = PRIVATE / 'raw' / 'extracted' / 'green' / 'map-green innovation' / 'dataset-final.dta'
D2_PATH = PRIVATE / 'raw' / 'extracted' / 'dt' / 'Digital transformation and strategic risk taking dataset' / 'Digita Transformation and-Strategic Risk Taking Dataset.xlsx'
CONTROLS = [
    'leverage', 'cash_flow', 'firm_size', 'book_to_market', 'roa', 'growth',
    'fixed_asset_ratio', 'equity_balance', 'independent_directors', 'board_size',
    'largest_holder', 'employee_scale', 'ceo_duality', 'soe',
]
FULL = ' + '.join(CONTROLS)


def ci(beta: float, se: float) -> tuple[float, float]:
    return beta - 1.959964 * se, beta + 1.959964 * se


def fit_summary(name: str, fit, term: str, data: pd.DataFrame, estimator: str, scope: str, note: str) -> dict:
    beta = float(fit.coef().loc[term])
    se = float(fit.se().loc[term])
    low, high = ci(beta, se)
    retained = getattr(fit, '_data', data)
    return {
        'Model': name,
        'Estimator': estimator,
        'Scope': scope,
        'Coefficient on DT_log': beta,
        'Firm-clustered SE': se,
        '95% CI lower': low,
        '95% CI upper': high,
        'p_value_unadjusted': float(fit.pvalue().loc[term]),
        'Candidate observations': int(len(data)),
        'Retained observations': int(len(retained)),
        'Retained firms': int(retained['firm_id'].nunique()),
        'Note': note,
    }


def strict_lag(frame: pd.DataFrame, column: str, output: str) -> None:
    frame.sort_values(['firm_id', 'year'], inplace=True)
    previous_year = frame.groupby('firm_id')['year'].shift(1)
    frame[output] = frame.groupby('firm_id')[column].shift(1)
    frame.loc[frame['year'] - previous_year != 1, output] = np.nan

# ---- Construct provenance-preserving sensitivity covariates ----
panel = pd.read_csv(PANEL_PATH).sort_values(['firm_id', 'year']).reset_index(drop=True)
green = pd.read_stata(GREEN_PATH, convert_categoricals=False)[['股票代码', '会计年度', 'lngpfm']].rename(
    columns={'股票代码': 'firm_id', '会计年度': 'year', 'lngpfm': 'd1_invention_patent_log'}
)
for col in ['firm_id', 'year', 'd1_invention_patent_log']:
    green[col] = pd.to_numeric(green[col], errors='coerce')
green['firm_id'] = green['firm_id'].astype('int64')
green['year'] = green['year'].astype('int64')
d2 = pd.read_excel(D2_PATH, sheet_name='Digital Transformation')[['Stockcode', 'Year', 'R&D expenditure']].rename(
    columns={'Stockcode': 'firm_id', 'Year': 'year', 'R&D expenditure': 'd2_rd_expenditure_released'}
)
for col in ['firm_id', 'year', 'd2_rd_expenditure_released']:
    d2[col] = pd.to_numeric(d2[col], errors='coerce')
d2['firm_id'] = d2['firm_id'].astype('int64')
d2['year'] = d2['year'].astype('int64')
assert green.duplicated(['firm_id', 'year']).sum() == 0
assert d2.duplicated(['firm_id', 'year']).sum() == 0
panel = panel.merge(green, on=['firm_id', 'year'], how='left', validate='one_to_one')
panel = panel.merge(d2, on=['firm_id', 'year'], how='left', validate='one_to_one')
assert panel['d1_invention_patent_log'].notna().all()
assert panel['d2_rd_expenditure_released'].notna().all()
strict_lag(panel, 'd1_invention_patent_log', 'lag_d1_invention_patent_log')
strict_lag(panel, 'd2_rd_expenditure_released', 'lag_d2_rd_expenditure_released')

# ---- Sensitivities: explicitly lag controls so they precede contemporaneous DT/outcome ----
models: list[dict] = []
base_ols = pf.feols(f'green_quality_log ~ log_dt + {FULL} | firm_id + year', data=panel, vcov={'CRV1': 'firm_id'})
base_ppml = pf.fepois(f'green_invention_count ~ log_dt + {FULL} | firm_id + year', data=panel, vcov={'CRV1': 'firm_id'})
models += [
    fit_summary('Locked log-outcome reference', base_ols, 'log_dt', panel, 'TWFE OLS', 'Matched complete-case design', 'Reference only; descriptive association.'),
    fit_summary('Locked conditional count reference', base_ppml, 'log_dt', panel, 'Conditional PPML', 'Estimator-retained contribution set', 'Reference only; all-zero firms do not contribute to conditional FE identification.'),
]

specs = [
    ('Lagged released R&D-expenditure field', ['lag_d2_rd_expenditure_released'], 'D2 field is complete on the matched panel but its released numerical transformation/unit is not labeled; use is a proxy sensitivity, not verified R&D intensity.'),
    ('Lagged invention-patent activity', ['lag_d1_invention_patent_log'], 'D1 ln(1+invention patents) is a prior-period inventive-activity proxy, not a validated cumulative knowledge-stock measure.'),
    ('Both lagged proxy fields', ['lag_d2_rd_expenditure_released', 'lag_d1_invention_patent_log'], 'Joint sensitivity with two preceding-period proxy fields; neither resolves unobserved confounding.'),
]
for label, added, note in specs:
    candidate = panel.dropna(subset=added).copy()
    rhs = 'log_dt + ' + FULL + ' + ' + ' + '.join(added)
    ols = pf.feols(f'green_quality_log ~ {rhs} | firm_id + year', data=candidate, vcov={'CRV1': 'firm_id'})
    ppml = pf.fepois(f'green_invention_count ~ {rhs} | firm_id + year', data=candidate, vcov={'CRV1': 'firm_id'})
    models.append(fit_summary(f'{label}: log outcome', ols, 'log_dt', candidate, 'TWFE OLS', 'Strict calendar-lag candidate sample', note))
    models.append(fit_summary(f'{label}: conditional count', ppml, 'log_dt', candidate, 'Conditional PPML', 'Strict calendar-lag estimator-retained set', note))
models_df = pd.DataFrame(models)
models_df.to_csv(TABLES / 'r3_proxy_sensitivity_models.csv', index=False)

# ---- Conditional PPML residual and contribution diagnostics on actual retained data ----
ppml = base_ppml
retained = ppml._data.copy().reset_index(drop=True)
mu = np.asarray(ppml.predict(type='response'), dtype=float).reshape(-1)
response_resid = np.asarray(ppml.resid(type='response'), dtype=float).reshape(-1)
y = retained['green_invention_count'].to_numpy(dtype=float)
assert len(mu) == len(retained) == len(response_resid)
assert np.allclose(response_resid, y - mu, atol=1e-8)
pearson = response_resid / np.sqrt(mu)
retained['_pearson'] = pearson
retained['_pearson_sq'] = pearson ** 2
n = int(len(retained))
k_slope = int(len(ppml.coef()))
df_approx = n - k_slope
x2 = float(np.sum(pearson ** 2))
threshold = 3.0
extreme = np.abs(pearson) > threshold
residual_summary = pd.DataFrame([{
    'Model': 'Locked conditional PPML',
    'Retained observations': n,
    'Retained firms': int(retained['firm_id'].nunique()),
    'Slope parameters counted': k_slope,
    'Approximate df (N minus slope parameters)': df_approx,
    'Pearson X2': x2,
    'Pearson X2 / approximate df': x2 / df_approx,
    'Residual definition': '(y - fitted conditional mean) / sqrt(fitted conditional mean)',
    'Absolute Pearson threshold': threshold,
    'Observations above absolute threshold': int(extreme.sum()),
    'Share above absolute threshold': float(extreme.mean()),
    'Largest absolute Pearson residual': float(np.abs(pearson).max()),
    'Maximum fitted conditional mean': float(mu.max()),
    'Caution': 'The denominator ignores the high-dimensional fixed-effect degrees of freedom and is a descriptive dispersion screen, not a formal goodness-of-fit test.'
}])
residual_summary.to_csv(TABLES / 'r3_ppml_pearson_residual_summary.csv', index=False)

# Pre-specified after-review screen: remove every actual retained observation with |Pearson| > 3, then refit the identical conditional PPML formula.
trim_candidate = retained.loc[~extreme].drop(columns=['_pearson', '_pearson_sq']).copy()
trim_fit = pf.fepois(f'green_invention_count ~ log_dt + {FULL} | firm_id + year', data=trim_candidate, vcov={'CRV1': 'firm_id'})
diag_models = [fit_summary('Locked conditional PPML', ppml, 'log_dt', panel, 'Conditional PPML', 'Estimator-retained contribution set', 'Reference diagnostic model.'),
               fit_summary('Exclude all retained observations with |Pearson residual| > 3', trim_fit, 'log_dt', trim_candidate, 'Conditional PPML', 'Post-review diagnostic sensitivity', 'Threshold applied once to every observation in the locked PPML retained set; exploratory, not a model-selection rule.')]
pd.DataFrame(diag_models).to_csv(TABLES / 'r3_ppml_extreme_residual_sensitivity.csv', index=False)

# Cluster-deletion influence screen: rank firms by Pearson X2 contribution, delete each of top ceil(1%) clusters once, and report anonymous rank only.
firm_contrib = retained.groupby('firm_id', as_index=False).agg(
    pearson_x2=('_pearson_sq', 'sum'), retained_observations=('firm_id', 'size')
).sort_values('pearson_x2', ascending=False).reset_index(drop=True)
top_n = max(1, math.ceil(0.01 * len(firm_contrib)))
influence_rows = []
for rank, row in firm_contrib.head(top_n).iterrows():
    drop_firm = row['firm_id']
    candidate = retained.loc[retained['firm_id'] != drop_firm].drop(columns=['_pearson', '_pearson_sq']).copy()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        delete_fit = pf.fepois(f'green_invention_count ~ log_dt + {FULL} | firm_id + year', data=candidate, vcov={'CRV1': 'firm_id'})
    out = fit_summary(f'Leave out rank {rank + 1} Pearson-X2 contributing firm', delete_fit, 'log_dt', candidate, 'Conditional PPML', 'Post-review influence sensitivity', 'Firms are ranked within retained data by descriptive Pearson-X2 contribution; rank only is released.')
    out.update({
        'Anonymous rank': int(rank + 1),
        'Firm Pearson X2 contribution': float(row['pearson_x2']),
        'Firm share of total Pearson X2': float(row['pearson_x2'] / x2),
        'Removed retained observations': int(row['retained_observations']),
    })
    influence_rows.append(out)
influence_df = pd.DataFrame(influence_rows)
influence_df.to_csv(TABLES / 'r3_ppml_top_contribution_firm_deletions.csv', index=False)

# Binned, aggregate visual diagnostics; no raw firm-year points or firm IDs are written.
fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.9), dpi=300)
axes[0].hist(pearson, bins=55, color='#2f6f8f', edgecolor='white', linewidth=.3)
axes[0].axvline(-threshold, color='#a3342a', ls='--', lw=1)
axes[0].axvline(threshold, color='#a3342a', ls='--', lw=1, label='|Pearson| = 3')
axes[0].set_xlabel('Pearson residual')
axes[0].set_ylabel('Retained observations')
axes[0].set_title('Conditional PPML residual screen')
axes[0].legend(frameon=False, fontsize=8)
# Quantile bins make fitted-value diagnostic readable without releasing point-level values.
quantiles = pd.qcut(pd.Series(mu), q=20, duplicates='drop')
binned = pd.DataFrame({'mu': mu, 'pearson': pearson, 'bin': quantiles}).groupby('bin', observed=False).agg(
    fitted_mean=('mu', 'mean'), mean_sq_pearson=('pearson', lambda z: float(np.mean(np.square(z)))), n=('mu', 'size')
).reset_index(drop=True)
axes[1].plot(binned['fitted_mean'], binned['mean_sq_pearson'], marker='o', color='#2f6f8f', lw=1.5, ms=3)
axes[1].axhline(1, color='#6b6b6b', lw=1, ls='--')
axes[1].set_xlabel('Mean fitted conditional count (quantile bin)')
axes[1].set_ylabel('Mean squared Pearson residual')
axes[1].set_title('Binned dispersion pattern')
axes[1].grid(axis='y', alpha=.25)
fig.suptitle('Descriptive diagnostics for estimator-retained conditional PPML data', y=1.02, fontsize=11)
fig.tight_layout()
fig.savefig(FIGURES / 'r3_ppml_diagnostics.png', bbox_inches='tight')
plt.close(fig)

# Manifest and concise human-readable audit.
manifest = {
    'scope': 'Post-review descriptive sensitivity analysis; no causal interpretation.',
    'proxy_construction': {
        'released_rd_field': 'D2 column R&D expenditure as released; its workbook numerical transformation/unit is not documented in this pipeline.',
        'lagged_rd_field': 'Strict one-calendar-year lag of the released D2 R&D expenditure field.',
        'lagged_invention_proxy': 'Strict one-calendar-year lag of D1 lngpfm, labeled ln(1+invention patent).',
    },
    'ppml_residual_screen': residual_summary.iloc[0].to_dict(),
    'extreme_residual_rule': 'Apply |Pearson residual| > 3 to all observations retained by the locked conditional PPML, then refit once.',
    'firm_deletion_rule': f'Delete each of the top {top_n} of {len(firm_contrib)} retained firms ranked by Pearson X2 contribution, one at a time.',
    'files': [str(p.name) for p in TABLES.glob('r3_*.csv')] + [str((FIGURES / 'r3_ppml_diagnostics.png').name)],
}
(RESULTS / 'r3_model_diagnostics_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
lines = [
    '# R3 Proxy Sensitivity and Conditional-PPML Diagnostics', '',
    '## Scope', '',
    'All results are descriptive, estimator-specific analyses of the deterministic D1–D2 matched panel. The lagged released R&D-expenditure field is a source-labelled proxy rather than a verified R&D-intensity measure because the released workbook does not disclose the numerical transformation or unit. The D1 lagged ln(1+invention patents) field is a preceding-period inventive-activity proxy, not a cumulative knowledge-stock measure.', '',
    '## Lagged proxy sensitivity estimates', '', models_df.to_markdown(index=False, floatfmt='.4f'), '',
    '## Pearson-residual screen', '', residual_summary.to_markdown(index=False, floatfmt='.4f'), '',
    'The dispersion ratio uses N minus slope parameters only and therefore deliberately does not claim a high-dimensional fixed-effect degrees-of-freedom adjustment. It is a screen for heterogeneity, not a pass/fail test of Poisson variance.', '',
    '## Extreme-residual sensitivity', '', pd.DataFrame(diag_models).to_markdown(index=False, floatfmt='.4f'), '',
    '## High-contribution firm deletion sensitivity', '', influence_df.to_markdown(index=False, floatfmt='.4f'), '',
    'Firms are shown only by anonymous contribution rank. Each deletion is a post-review descriptive check; estimates are not used to select a preferred result.', '',
]
(TABLES / 'reviewer_r3_model_diagnostics.md').write_text('\n'.join(lines), encoding='utf-8')
print((TABLES / 'reviewer_r3_model_diagnostics.md').read_text(encoding='utf-8'))
