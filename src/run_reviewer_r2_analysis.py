"""Second-round audit of sample boundaries, PPML retention, IPW availability calibration, and strict timing support.

This script never interprets any estimate as causal. It writes only aggregate outputs to
R2_RESULTS and stores row-level intermediate objects in memory / private metadata only.
"""
from pathlib import Path
import json
import os
import warnings

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 8, 'axes.labelsize': 9, 'axes.titlesize': 11, 'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8})
import numpy as np
import pandas as pd
import pyfixest as pf
import statsmodels.formula.api as smf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# Set DGI_PRIVATE_DATA_ROOT to the `data` directory of the separate private repository.
PRIVATE = Path(os.environ.get('DGI_PRIVATE_DATA_ROOT', PROJECT_ROOT / 'data' / 'private'))
R2_RESULTS = PROJECT_ROOT / 'results' / 'reviewer_r2'
TABLES = R2_RESULTS / 'tables'
FIGURES = R2_RESULTS / 'figures'
PRIVATE_METADATA = PRIVATE / 'metadata'
for folder in (TABLES, FIGURES, PRIVATE_METADATA):
    folder.mkdir(parents=True, exist_ok=True)

PANEL_PATH = PRIVATE / 'derived' / 'matched_panel_private.csv'
GREEN_PATH = PRIVATE / 'raw' / 'extracted' / 'green' / 'map-green innovation' / 'dataset-final.dta'
AUDIT_PATH = PRIVATE_METADATA / 'analysis_audit.json'
CONTROLS_FULL = [
    'leverage', 'cash_flow', 'firm_size', 'book_to_market', 'roa', 'growth',
    'fixed_asset_ratio', 'equity_balance', 'independent_directors', 'board_size',
    'largest_holder', 'employee_scale', 'ceo_duality', 'soe',
]
CONTROLS_CORE = [
    'leverage', 'cash_flow', 'firm_size', 'book_to_market', 'roa', 'growth',
    'fixed_asset_ratio', 'equity_balance', 'largest_holder', 'ceo_duality', 'soe',
]
SELECTION_COVARS = ['firm_size', 'roa']
GREEN_COLS = {
    '股票代码': 'firm_id', '会计年度': 'year', '资产负债率': 'leverage', 'Cflow': 'cash_flow',
    'Size': 'firm_size', 'BM': 'book_to_market', 'ROA': 'roa', 'Growth': 'growth',
    '固定资产比率': 'fixed_asset_ratio', '股权制衡度': 'equity_balance', 'Indep': 'independent_directors',
    '董事会规模': 'board_size', '第一大股东持股比率': 'largest_holder', 'Staff': 'employee_scale',
    'Dual': 'ceo_duality', 'soe': 'soe', '当年联合申请的绿色发明数量': 'green_invention_count',
}

panel = pd.read_csv(PANEL_PATH).sort_values(['firm_id', 'year']).reset_index(drop=True)
with AUDIT_PATH.open(encoding='utf-8') as fh:
    core_audit = json.load(fh)

# ---- Helpers ----
def ci(beta, se):
    return beta - 1.959964 * se, beta + 1.959964 * se

def safely_float(value):
    return float(value) if pd.notna(value) else np.nan

def sample_profile(name, data, source_n=None, source_label=None):
    """Aggregate profile used to state the target population of each estimator."""
    rows = {
        'Sample': name,
        'Observations': int(len(data)),
        'Firms': int(data['firm_id'].nunique()),
        'Years': int(data['year'].nunique()),
        'Year minimum': int(data['year'].min()),
        'Year maximum': int(data['year'].max()),
        'Share of matched complete-case observations': len(data) / len(panel),
        'Zero invention-count share': safely_float(data['green_invention_count'].eq(0).mean()),
        'Positive invention-count share': safely_float(data['green_invention_count'].gt(0).mean()),
        'Mean raw DT': safely_float(data['dt_raw'].mean()),
        'SD raw DT': safely_float(data['dt_raw'].std(ddof=1)),
        'Mean log DT': safely_float(data['log_dt'].mean()),
        'Mean firm size': safely_float(data['firm_size'].mean()),
        'Mean ROA': safely_float(data['roa'].mean()),
        'Mean leverage': safely_float(data['leverage'].mean()),
        'Mean green invention count': safely_float(data['green_invention_count'].mean()),
    }
    if source_n:
        rows[f'Share of {source_label or "source"} observations'] = len(data) / source_n
    return rows

def get_fit_sample(fit):
    data = getattr(fit, '_data', None)
    if not isinstance(data, pd.DataFrame):
        raise RuntimeError('pyfixest fit does not expose the retained DataFrame needed for this audit')
    needed = {'firm_id', 'year', 'green_invention_count', 'dt_raw', 'log_dt', 'firm_size', 'roa', 'leverage'}
    missing = needed - set(data.columns)
    if missing:
        raise RuntimeError(f'PPML retained sample missing expected fields: {sorted(missing)}')
    return data.copy()

def sdm(pre, post, weights=None):
    pre = pd.to_numeric(pre, errors='coerce').dropna()
    if weights is None:
        aligned = pd.to_numeric(post, errors='coerce').dropna()
        post_mean = aligned.mean()
        post_var = aligned.var(ddof=1)
    else:
        temp = pd.DataFrame({'x': pd.to_numeric(post, errors='coerce'), 'w': weights}).dropna()
        post_mean = np.average(temp['x'], weights=temp['w'])
        post_var = np.average((temp['x'] - post_mean) ** 2, weights=temp['w'])
    pre_mean = pre.mean()
    pre_var = pre.var(ddof=1)
    pooled = np.sqrt((pre_var + post_var) / 2)
    return {'Source mean': float(pre_mean), 'Comparison mean': float(post_mean),
            'SMD': float((post_mean - pre_mean) / pooled) if pooled else np.nan,
            'Absolute SMD': float(abs((post_mean - pre_mean) / pooled)) if pooled else np.nan}

# ---- 1. Fit retained estimator samples using the locked primary specifications ----
full_formula = ' + '.join(CONTROLS_FULL)
ols_fit = pf.feols(
    f'green_quality_log ~ log_dt + {full_formula} | firm_id + year',
    data=panel,
    vcov={'CRV1': 'firm_id'},
)
ppml_fit = pf.fepois(
    f'green_invention_count ~ log_dt + {full_formula} | firm_id + year',
    data=panel,
    vcov={'CRV1': 'firm_id'},
)
ols_retained = get_fit_sample(ols_fit)
ppml_retained = get_fit_sample(ppml_fit)
assert len(ols_retained) == 6443, len(ols_retained)
assert len(ppml_retained) == 2774, len(ppml_retained)

# Reconstruct strict lag and lead on calendar time and retain actual fepois samples.
panel['previous_year_r2'] = panel.groupby('firm_id')['year'].shift(1)
panel['next_year_r2'] = panel.groupby('firm_id')['year'].shift(-1)
panel['strict_lag_log_dt_r2'] = panel.groupby('firm_id')['log_dt'].shift(1)
panel['strict_lead_log_dt_r2'] = panel.groupby('firm_id')['log_dt'].shift(-1)
panel.loc[panel['year'] - panel['previous_year_r2'] != 1, 'strict_lag_log_dt_r2'] = np.nan
panel.loc[panel['next_year_r2'] - panel['year'] != 1, 'strict_lead_log_dt_r2'] = np.nan
lag_candidate = panel.dropna(subset=['strict_lag_log_dt_r2']).copy()
lead_candidate = panel.dropna(subset=['strict_lead_log_dt_r2']).copy()
lag_fit = pf.fepois(
    f'green_invention_count ~ strict_lag_log_dt_r2 + {full_formula} | firm_id + year',
    data=lag_candidate,
    vcov={'CRV1': 'firm_id'},
)
lead_fit = pf.fepois(
    f'green_invention_count ~ strict_lead_log_dt_r2 + {full_formula} | firm_id + year',
    data=lead_candidate,
    vcov={'CRV1': 'firm_id'},
)
lag_retained = get_fit_sample(lag_fit)
lead_retained = get_fit_sample(lead_fit)

# ---- 2. Sample flow, PPML composition and explicit overlap ----
source_keys = core_audit['source_keys']
source_n = source_keys['green']['rows']
profiles = pd.DataFrame([
    sample_profile('D1 green-source file', pd.read_stata(GREEN_PATH, convert_categoricals=False).rename(columns={'股票代码': 'firm_id', '会计年度': 'year', '当年联合申请的绿色发明数量': 'green_invention_count'}).assign(
        dt_raw=np.nan, log_dt=np.nan, firm_size=np.nan, roa=np.nan, leverage=np.nan
    ).loc[:, ['firm_id', 'year', 'green_invention_count', 'dt_raw', 'log_dt', 'firm_size', 'roa', 'leverage']], source_n=source_n, source_label='D1 green-source'),
    sample_profile('Matched complete-case panel', panel, source_n=source_n, source_label='D1 green-source'),
    sample_profile('TWFE log-outcome retained sample', ols_retained, source_n=source_n, source_label='D1 green-source'),
    sample_profile('Conditional PPML retained sample', ppml_retained, source_n=source_n, source_label='D1 green-source'),
    sample_profile('Strict t−1 PPML retained sample', lag_retained, source_n=source_n, source_label='D1 green-source'),
    sample_profile('Strict t+1 PPML retained sample', lead_retained, source_n=source_n, source_label='D1 green-source'),
])
# Preserve the verified D1 profile values where the D1 raw source contains differently named columns.
green_full = pd.read_stata(GREEN_PATH, convert_categoricals=False)
green = green_full[list(GREEN_COLS)].rename(columns=GREEN_COLS)
for col in ['firm_id', 'year']:
    green[col] = pd.to_numeric(green[col], errors='coerce')
source_row = profiles['Sample'].eq('D1 green-source file')
for column, source_column in [('Mean firm size', 'firm_size'), ('Mean ROA', 'roa'), ('Mean leverage', 'leverage'), ('Mean green invention count', 'green_invention_count')]:
    profiles.loc[source_row, column] = pd.to_numeric(green[source_column], errors='coerce').mean()
# The D1 source is the denominator, not a subset of the matched complete-case panel.
profiles.loc[profiles['Sample'].eq('D1 green-source file'), 'Share of matched complete-case observations'] = np.nan
profiles.to_csv(TABLES / 'r2_sample_flow_and_estimator_profiles.csv', index=False)

comparison_vars = ['firm_size', 'roa', 'leverage', 'dt_raw', 'log_dt', 'green_invention_count']
comp_rows = []
for variable in comparison_vars:
    full = panel[variable]
    for label, frame in [('TWFE log-outcome retained', ols_retained), ('Conditional PPML retained', ppml_retained), ('Strict t−1 PPML retained', lag_retained)]:
        metrics = sdm(full, frame[variable])
        comp_rows.append({'Comparison baseline': 'Matched complete-case panel', 'Estimator sample': label, 'Variable': variable, **metrics})
ppml_comp = pd.DataFrame(comp_rows)
ppml_comp.to_csv(TABLES / 'r2_estimator_sample_comparison.csv', index=False)

# Firm and observation overlap rates, preserving exact retained keys.
def key_set(data):
    return set(map(tuple, data[['firm_id', 'year']].astype(int).to_numpy()))
base_keys, ols_keys, ppml_keys, lag_keys, lead_keys = map(key_set, [panel, ols_retained, ppml_retained, lag_retained, lead_retained])
base_firms = set(panel['firm_id'].astype(int))
ppml_firms = set(ppml_retained['firm_id'].astype(int))
lag_firms = set(lag_retained['firm_id'].astype(int))
overlap = pd.DataFrame([
    {'Pair': 'PPML / matched complete-case', 'Observation intersection': len(ppml_keys & base_keys), 'Share of matched observations': len(ppml_keys & base_keys) / len(base_keys), 'Firm intersection': len(ppml_firms & base_firms), 'Share of matched firms': len(ppml_firms & base_firms) / len(base_firms)},
    {'Pair': 'Strict t−1 PPML / matched complete-case', 'Observation intersection': len(lag_keys & base_keys), 'Share of matched observations': len(lag_keys & base_keys) / len(base_keys), 'Firm intersection': len(lag_firms & base_firms), 'Share of matched firms': len(lag_firms & base_firms) / len(base_firms)},
    {'Pair': 'Strict t−1 PPML / conditional PPML', 'Observation intersection': len(lag_keys & ppml_keys), 'Share of matched observations': len(lag_keys & ppml_keys) / len(base_keys), 'Firm intersection': len(lag_firms & ppml_firms), 'Share of matched firms': len(lag_firms & ppml_firms) / len(ppml_firms)},
])
overlap.to_csv(TABLES / 'r2_sample_overlap.csv', index=False)

zero_firm = panel.groupby('firm_id')['green_invention_count'].sum().eq(0)
zero_firm_summary = pd.DataFrame([{
    'Matched complete-case firms': int(panel.firm_id.nunique()),
    'Firms with zero collaborative green inventions in all observed years': int(zero_firm.sum()),
    'Share of complete-case firms that are all-zero': float(zero_firm.mean()),
    'Matched complete-case observations from all-zero firms': int(panel['firm_id'].isin(zero_firm[zero_firm].index).sum()),
    'Share of complete-case observations from all-zero firms': float(panel['firm_id'].isin(zero_firm[zero_firm].index).mean()),
    'Conditional PPML retained observations': int(len(ppml_retained)),
    'Conditional PPML retained firms': int(ppml_retained.firm_id.nunique()),
}])
zero_firm_summary.to_csv(TABLES / 'r2_ppml_zero_firm_boundary.csv', index=False)
all_zero_firm_ids = set(zero_firm[zero_firm].index.astype(int))
retained_ppml_keys = key_set(ppml_retained)
nonretained = panel.loc[~panel.apply(lambda r: (int(r['firm_id']), int(r['year'])) in retained_ppml_keys, axis=1)].copy()
nonzero_nonretained = nonretained.loc[~nonretained['firm_id'].isin(all_zero_firm_ids)].copy()
ppml_exclusion = pd.DataFrame([
    {'Stage / observed outcome group': 'Matched complete-case panel', 'Observations': int(len(panel)), 'Firms': int(panel.firm_id.nunique()), 'Share of matched observations': 1.0},
    {'Stage / observed outcome group': 'All-zero-invention firms (not retained by conditional PPML)', 'Observations': int(panel['firm_id'].isin(all_zero_firm_ids).sum()), 'Firms': int(len(all_zero_firm_ids)), 'Share of matched observations': float(panel['firm_id'].isin(all_zero_firm_ids).mean())},
    {'Stage / observed outcome group': 'Ever-positive firms removed by PPML preprocessing/separation', 'Observations': int(len(nonzero_nonretained)), 'Firms': int(nonzero_nonretained.firm_id.nunique()), 'Share of matched observations': float(len(nonzero_nonretained) / len(panel))},
    {'Stage / observed outcome group': 'Conditional PPML retained contribution set', 'Observations': int(len(ppml_retained)), 'Firms': int(ppml_retained.firm_id.nunique()), 'Share of matched observations': float(len(ppml_retained) / len(panel))},
])
ppml_exclusion.to_csv(TABLES / 'r2_ppml_retention_decomposition.csv', index=False)

# ---- 3. Strict timing results with CI, year support and sample overlap ----
def summarize_fit(label, fit, term, retained, candidate, relation):
    beta = float(fit.coef().loc[term])
    se = float(fit.se().loc[term])
    low, high = ci(beta, se)
    return {
        'Test': label, 'Relation': relation, 'Coefficient': beta, 'Firm-clustered SE': se,
        'p_value': float(fit.pvalue().loc[term]), '95% CI lower': low, '95% CI upper': high,
        'Candidate observations before conditional PPML': int(len(candidate)),
        'Retained observations': int(len(retained)), 'Retained firms': int(retained.firm_id.nunique()),
        'Retained years': int(retained.year.nunique()), 'Year range': f'{int(retained.year.min())}–{int(retained.year.max())}',
        'Share of matched complete-case observations': len(retained) / len(panel),
    }
timing_results = pd.DataFrame([
    summarize_fit('Strict t−1 log DT PPML', lag_fit, 'strict_lag_log_dt_r2', lag_retained, lag_candidate, 'Prior calendar year'),
    summarize_fit('Strict t+1 log DT PPML placebo', lead_fit, 'strict_lead_log_dt_r2', lead_retained, lead_candidate, 'Following calendar year'),
])
timing_results.to_csv(TABLES / 'r2_timing_estimates_with_sample_composition.csv', index=False)

year_support = []
for name, candidate, retained, relationship in [
    ('Strict t−1', lag_candidate, lag_retained, 'DT measured in preceding calendar year'),
    ('Strict t+1', lead_candidate, lead_retained, 'DT measured in following calendar year'),
]:
    for year in range(2014, 2021):
        c = candidate.loc[candidate.year.eq(year)]
        r = retained.loc[retained.year.eq(year)]
        year_support.append({
            'Test': name, 'Relationship': relationship, 'Outcome year': year,
            'Matched complete-case observations': int(panel.year.eq(year).sum()),
            'Candidate observations': int(len(c)), 'Retained PPML observations': int(len(r)),
            'Candidate firms': int(c.firm_id.nunique()), 'Retained PPML firms': int(r.firm_id.nunique()),
        })
year_support = pd.DataFrame(year_support)
year_support.to_csv(TABLES / 'r2_timing_year_support.csv', index=False)

# ---- 4. Availability-calibration (IPW) sensitivity restricted to selection covariates ----
# This is not a treatment propensity score and is not a causal estimator. It predicts whether a D1 record
# appears in the deterministic D1–D2 matched panel, conditional on observed D1 covariates/year.
green = green.copy()
green['firm_id'] = pd.to_numeric(green['firm_id'], errors='coerce').astype('Int64')
green['year'] = pd.to_numeric(green['year'], errors='coerce').astype('Int64')
matched_keys = panel[['firm_id', 'year']].drop_duplicates().copy()
matched_keys['matched_available'] = 1
availability = green.merge(matched_keys, on=['firm_id', 'year'], how='left', validate='one_to_one')
availability['matched_available'] = availability['matched_available'].fillna(0).astype(int)
# patsy/statsmodels cannot consume pandas nullable Int64 in categorical terms; retain only complete keys and use ordinary integers.
availability = availability.dropna(subset=['firm_id', 'year', 'firm_size', 'roa']).copy()
availability['firm_id'] = availability['firm_id'].astype('int64')
availability['year'] = availability['year'].astype('int64')
selection_formula = 'matched_available ~ firm_size + roa + C(year)'
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    selection_fit = smf.logit(selection_formula, data=availability).fit(disp=False, maxiter=200)
availability['p_matched_available'] = np.asarray(selection_fit.predict(availability))
weighted = panel.merge(
    availability[['firm_id', 'year', 'p_matched_available']],
    on=['firm_id', 'year'], how='inner', validate='one_to_one'
)
# Align to the HDFE log-outcome support used in the primary OLS model.
weighted = weighted.merge(ols_retained[['firm_id', 'year']], on=['firm_id', 'year'], how='inner', validate='one_to_one')
stabilizer = float(availability.loc[selection_fit.model.data.row_labels, 'matched_available'].mean())
weighted['stabilized_availability_weight'] = stabilizer / weighted['p_matched_available']
weight_lo, weight_hi = weighted['stabilized_availability_weight'].quantile([0.01, 0.99])
weighted['stabilized_weight_trimmed'] = weighted['stabilized_availability_weight'].clip(weight_lo, weight_hi)
weights = weighted['stabilized_weight_trimmed']
ess = (weights.sum() ** 2) / (weights.pow(2).sum())

# Three transparent, noncausal calibration variants: no extra covariate control; duplicated covariate
# adjustment; and an unweighted restricted-control reference. They expose, rather than hide, sensitivity to
# simultaneous weighting and outcome conditioning.
formula_no_cov = 'green_quality_log ~ log_dt + C(firm_id) + C(year)'
formula_selection_cov = 'green_quality_log ~ log_dt + firm_size + roa + C(firm_id) + C(year)'
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    unweighted_no_cov = smf.ols(formula_no_cov, data=weighted).fit(cov_type='cluster', cov_kwds={'groups': weighted['firm_id']})
    weighted_no_cov = smf.wls(formula_no_cov, data=weighted, weights=weights).fit(cov_type='cluster', cov_kwds={'groups': weighted['firm_id']})
    unweighted_selection_cov = smf.ols(formula_selection_cov, data=weighted).fit(cov_type='cluster', cov_kwds={'groups': weighted['firm_id']})
    weighted_selection_cov = smf.wls(formula_selection_cov, data=weighted, weights=weights).fit(cov_type='cluster', cov_kwds={'groups': weighted['firm_id']})

ipw_rows = []
for name, fit, is_weighted, controls in [
    ('Unweighted FE reference; no selection covariates', unweighted_no_cov, False, 'None beyond firm/year fixed effects'),
    ('Availability-weighted FE calibration; no selection covariates', weighted_no_cov, True, 'None beyond firm/year fixed effects'),
    ('Unweighted FE reference; selection covariates included', unweighted_selection_cov, False, 'Firm size and ROA'),
    ('Availability-weighted FE calibration; selection covariates included', weighted_selection_cov, True, 'Firm size and ROA'),
]:
    beta, se = float(fit.params['log_dt']), float(fit.bse['log_dt'])
    low, high = ci(beta, se)
    ipw_rows.append({
        'Model': name, 'Availability weighted': is_weighted, 'Outcome covariates beyond FE': controls,
        'Coefficient on ln(1+DT)': beta, 'Firm-clustered SE': se, 'p_value': float(fit.pvalues['log_dt']),
        '95% CI lower': low, '95% CI upper': high, 'N': int(fit.nobs),
    })
ipw_results = pd.DataFrame(ipw_rows)
ipw_results.to_csv(TABLES / 'r2_availability_calibration_models.csv', index=False)

weight_diagnostics = pd.DataFrame([{
    'Availability model': 'Logit: matched D1–D2 availability ~ firm size + ROA + calendar-year indicators',
    'Availability model observations': int(selection_fit.nobs),
    'D1 green-source observations': int(len(availability)),
    'Matched complete-case observations': int(availability['matched_available'].sum()),
    'Matched availability share': float(availability['matched_available'].mean()),
    'McFadden pseudo R2': float(selection_fit.prsquared),
    'Matched probability min': float(weighted['p_matched_available'].min()),
    'Matched probability p1': float(weighted['p_matched_available'].quantile(.01)),
    'Matched probability median': float(weighted['p_matched_available'].median()),
    'Matched probability p99': float(weighted['p_matched_available'].quantile(.99)),
    'Matched probability max': float(weighted['p_matched_available'].max()),
    'Stabilized weight min': float(weighted['stabilized_availability_weight'].min()),
    'Stabilized weight p1': float(weighted['stabilized_availability_weight'].quantile(.01)),
    'Stabilized weight median': float(weighted['stabilized_availability_weight'].median()),
    'Stabilized weight p99': float(weighted['stabilized_availability_weight'].quantile(.99)),
    'Stabilized weight max': float(weighted['stabilized_availability_weight'].max()),
    'Trimming cutpoints (p1/p99)': f'{weight_lo:.6f} / {weight_hi:.6f}',
    'Effective sample size after trimming': float(ess),
}])
weight_diagnostics.to_csv(TABLES / 'r2_availability_weight_diagnostics.csv', index=False)

balance_rows = []
for variable in ['firm_size', 'roa', 'leverage', 'cash_flow', 'growth', 'green_invention_count']:
    source_values = availability[variable]
    raw = sdm(source_values, weighted[variable])
    wtd = sdm(source_values, weighted[variable], weights=weights)
    balance_rows += [
        {'Variable': variable, 'Comparison': 'D1 source vs retained matched sample (unweighted)', **raw},
        {'Variable': variable, 'Comparison': 'D1 source vs retained matched sample (availability-weighted)', **wtd},
    ]
balance = pd.DataFrame(balance_rows)
balance.to_csv(TABLES / 'r2_availability_balance_diagnostics.csv', index=False)

# ---- 5. Publication-ready aggregate figures ----
fig, ax = plt.subplots(figsize=(8.0, 4.6), dpi=600)
plot = profiles.loc[profiles['Sample'].ne('D1 green-source file'), ['Sample', 'Share of matched complete-case observations']].copy()
plot = plot.iloc[::-1]
ax.barh(plot['Sample'], plot['Share of matched complete-case observations'], color='#1f4e79')
for i, value in enumerate(plot['Share of matched complete-case observations']):
    ax.text(value + 0.015, i, f'{value:.1%}', va='center', fontsize=8)
ax.set_xlim(0, 1.12)
ax.set_xlabel('Share of matched complete-case observations')
ax.set_title('Estimator-specific sample retention')
ax.grid(axis='x', alpha=.25)
fig.tight_layout()
fig.savefig(FIGURES / 'r2_estimator_sample_retention.png', bbox_inches='tight')
plt.close(fig)

fig, ax = plt.subplots(figsize=(8.0, 4.8), dpi=600)
for test, sub in year_support.groupby('Test'):
    ax.plot(sub['Outcome year'], sub['Retained PPML observations'], marker='o', lw=1.8, label=test)
ax.set_xticks(range(2014, 2021))
ax.set_xlabel('Outcome year')
ax.set_ylabel('Conditional PPML retained observations')
ax.set_title('Calendar-year support for strict timing estimators')
ax.legend(frameon=False)
ax.grid(axis='y', alpha=.25)
fig.tight_layout()
fig.savefig(FIGURES / 'r2_timing_year_support.png', bbox_inches='tight')
plt.close(fig)

# ---- 6. Human-readable audit record ----
def markdown(df):
    return df.to_markdown(index=False, floatfmt='.4f')
lines = [
    '# Reviewer 2 Model and Sample Audit', '',
    '## Scope and non-causal interpretation', '',
    'All items below are descriptive, estimator-specific audits of a deterministic D1–D2 firm-year match and its observed covariate composition. They do not identify a causal effect, recover unmatched D2 values, or correct selection on unobserved determinants.', '',
    '## Sample flow and estimator profiles', '', markdown(profiles), '',
    '## Conditional PPML zero-firm boundary', '', markdown(zero_firm_summary), '', markdown(ppml_exclusion), '',
    'The conditional PPML sample is the set retained by the high-dimensional fixed-effect estimator. It is not a treated group, and it does not represent the all-zero-invention population. The decomposition separates observed all-zero firms from the small residual group removed by estimator preprocessing/separation; it does not interpret either removal as random sampling.', '',
    '## PPML and strict-timing sample comparison', '', markdown(ppml_comp), '',
    '## Exact sample overlap', '', markdown(overlap), '',
    '## Strict timing estimates and support', '', markdown(timing_results), '', markdown(year_support), '',
    'The strict t−1 candidate excludes outcome year 2014 by construction because no preceding calendar-year DT value can exist. Additional reduction reflects an unbalanced panel and conditional PPML retention; the year table reports both candidate and retained observations.', '',
    '## Availability calibration (not treatment IPW)', '',
    'The selection model is a logit for deterministic D1–D2 matched availability conditional on D1 firm size, ROA and calendar year. It is a selection-on-observables calibration / covariate-balance diagnostic. “Propensity” is not used for treatment assignment, policy exposure, causal weighting, or correction for unobserved confounding.', '',
    markdown(weight_diagnostics), '', markdown(ipw_results), '', markdown(balance), '',
    'The weighted/no-covariate and weighted/selection-covariate variants are both reported to expose sensitivity to simultaneous weighting and regression adjustment. Neither is a causal estimate. If their direction differs, that is uncertainty rather than evidence for model selection.', '',
]
(TABLES / 'reviewer_r2_model_audit.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')

audit = {
    'scope': 'Non-causal deterministic-match and estimator-sample audit.',
    'r2_source_and_complete_case_n': {'d1_green_source': int(source_n), 'matched_complete_case': int(len(panel))},
    'profiles': profiles.to_dict(orient='records'),
    'ppml_zero_firm_boundary': zero_firm_summary.iloc[0].to_dict(),
    'ppml_retention_decomposition': ppml_exclusion.to_dict(orient='records'),
    'sample_overlap': overlap.to_dict(orient='records'),
    'timing': timing_results.to_dict(orient='records'),
    'availability_model': weight_diagnostics.iloc[0].to_dict(),
    'availability_calibration_models': ipw_results.to_dict(orient='records'),
    'selection_covariates': SELECTION_COVARS,
    'full_outcome_controls': CONTROLS_FULL,
    'core_outcome_controls': CONTROLS_CORE,
}
(PRIVATE_METADATA / 'reviewer_r2_model_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
print((TABLES / 'reviewer_r2_model_audit.md').read_text(encoding='utf-8'))
