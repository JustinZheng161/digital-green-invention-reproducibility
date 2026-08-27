"""Supplementary analyses requested in Reviewer 1.

The script makes no causal claim. It distinguishes (i) a linear fixed-effects
sensitivity on a count outcome from (ii) the preferred conditional PPML count
specification and reports diagnostics that demonstrate why the former is not
interpreted as primary evidence.
"""
from pathlib import Path
import os
import json
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyfixest as pf
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.multitest import multipletests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path(os.environ.get('DGI_PRIVATE_DATA_ROOT', PROJECT_ROOT / 'data/private'))
RESULTS = PROJECT_ROOT / 'results' / 'reviewer_r1'
TABLES = RESULTS / 'tables'
FIGURES = RESULTS / 'figures'
METADATA = PRIVATE / 'metadata'
for directory in (TABLES, FIGURES, METADATA):
    directory.mkdir(parents=True, exist_ok=True)

PANEL_PATH = PRIVATE / 'derived/matched_panel_private.csv'
GREEN_PATH = PRIVATE / 'raw/extracted/green/map-green innovation/dataset-final.dta'
SENSITIVITY_PATH = PROJECT_ROOT / 'results/tables/specification_sensitivity.csv'
CONTROLS = [
    'leverage', 'cash_flow', 'firm_size', 'book_to_market', 'roa', 'growth',
    'fixed_asset_ratio', 'equity_balance', 'independent_directors', 'board_size',
    'largest_holder', 'employee_scale', 'ceo_duality', 'soe',
]
PRIMARY_VARS = [
    'dt_raw', 'log_dt', 'green_invention_count', 'green_quality_log',
    'green_utility_count', 'firm_size', 'roa', 'leverage', 'cash_flow',
    'book_to_market', 'growth', 'soe',
]

# The matched panel is complete-case as constructed by the locked core script.
panel = pd.read_csv(PANEL_PATH).copy()
panel['positive_invention'] = (panel['green_invention_count'] > 0).astype(int)
panel['log_positive_invention'] = np.where(
    panel['green_invention_count'] > 0,
    np.log(panel['green_invention_count']),
    np.nan,
)

# HDFE linear estimators discard 131 firm singletons. Make the diagnostic sample
# align exactly with the reported two-way-FE OLS sample rather than silently use N=6574.
counts_by_firm = panel.groupby('firm_id')['firm_id'].transform('size')
ols_sample = panel.loc[counts_by_firm > 1].copy()
assert len(ols_sample) == 6443, len(ols_sample)
assert ols_sample['firm_id'].nunique() == 1337

# 1) Descriptive statistics and correlation matrices.
def summary_table(df, columns):
    rows = []
    for col in columns:
        ser = pd.to_numeric(df[col], errors='coerce').dropna()
        rows.append({
            'Variable': col,
            'N': int(ser.size),
            'Mean': float(ser.mean()),
            'SD': float(ser.std(ddof=1)),
            'Min': float(ser.min()),
            'P5': float(ser.quantile(0.05)),
            'P25': float(ser.quantile(0.25)),
            'Median': float(ser.median()),
            'P75': float(ser.quantile(0.75)),
            'P95': float(ser.quantile(0.95)),
            'Max': float(ser.max()),
            'Skewness': float(stats.skew(ser, bias=False)),
        })
    return pd.DataFrame(rows)

desc = summary_table(panel, PRIMARY_VARS + CONTROLS)
desc.to_csv(TABLES / 'appendix_descriptive_statistics.csv', index=False)
pearson = panel[PRIMARY_VARS].corr(method='pearson')
spearman = panel[PRIMARY_VARS].corr(method='spearman')
pearson.to_csv(TABLES / 'appendix_correlation_pearson.csv')
spearman.to_csv(TABLES / 'appendix_correlation_spearman.csv')

# 2) Selection diagnostics: original green source versus matched complete-case panel.
GREEN_COLS = {
    '股票代码': 'firm_id', '会计年度': 'year', '资产负债率': 'leverage', 'Cflow': 'cash_flow',
    'Size': 'firm_size', 'BM': 'book_to_market', 'ROA': 'roa', 'Growth': 'growth',
    '固定资产比率': 'fixed_asset_ratio', '股权制衡度': 'equity_balance', 'Indep': 'independent_directors',
    '董事会规模': 'board_size', '第一大股东持股比率': 'largest_holder', 'Staff': 'employee_scale',
    'Dual': 'ceo_duality', 'soe': 'soe', '当年联合申请的绿色发明数量': 'green_invention_count',
    '当年联合申请的绿色实用新型数量': 'green_utility_count', 'Lngp': 'green_output_log',
}
green = pd.read_stata(GREEN_PATH, convert_categoricals=False)
green = green[list(GREEN_COLS)].rename(columns=GREEN_COLS)
for k in ['firm_id', 'year']:
    green[k] = pd.to_numeric(green[k], errors='coerce')
green['green_quality_log'] = np.log1p(green['green_invention_count'])
selection_vars = ['firm_size', 'roa', 'leverage', 'cash_flow', 'book_to_market', 'growth', 'green_output_log', 'green_invention_count', 'green_quality_log']
sel_rows = []
for col in selection_vars:
    pre = pd.to_numeric(green[col], errors='coerce').dropna()
    post = pd.to_numeric(panel[col], errors='coerce').dropna()
    pooled_sd = np.sqrt((pre.var(ddof=1) + post.var(ddof=1)) / 2)
    smd = (post.mean() - pre.mean()) / pooled_sd if pooled_sd > 0 else np.nan
    sel_rows.append({
        'Variable': col,
        'Green-source mean': float(pre.mean()),
        'Matched-panel mean': float(post.mean()),
        'Mean difference': float(post.mean() - pre.mean()),
        'Pooled SD': float(pooled_sd),
        'Standardized mean difference': float(smd),
        'Absolute SMD': float(abs(smd)),
        'Green-source N': int(pre.size),
        'Matched-panel N': int(post.size),
    })
selection = pd.DataFrame(sel_rows)
selection.to_csv(TABLES / 'selection_standardized_mean_differences.csv', index=False)

# Love plot of sample selection standardized differences.
plot_sel = selection.sort_values('Absolute SMD')
fig, ax = plt.subplots(figsize=(7.0, 4.4), dpi=600)
ax.hlines(y=np.arange(len(plot_sel)), xmin=0, xmax=plot_sel['Absolute SMD'], color='#94a3b8', lw=1.5)
ax.scatter(plot_sel['Absolute SMD'], np.arange(len(plot_sel)), color='#1f4e79', s=34, zorder=3)
ax.axvline(0.1, color='#b91c1c', ls='--', lw=1, label='|SMD| = 0.10 reference')
ax.set_yticks(np.arange(len(plot_sel)), plot_sel['Variable'])
ax.set_xlabel('Absolute standardized mean difference\n(green source vs matched panel)')
ax.set_title('Selection diagnostics for matched panel')
ax.legend(frameon=False, loc='lower right', fontsize=8)
fig.tight_layout()
fig.savefig(FIGURES / 'selection_love_plot.png', bbox_inches='tight')
plt.close(fig)

# 3) OLS diagnostics. This is not a test of whether OLS has 'normal errors' in a
# fixed-effect setting; it transparently describes non-normality, heteroskedasticity,
# and influence to establish why OLS count is supplemental only.
formula = 'green_invention_count ~ log_dt + ' + ' + '.join(CONTROLS) + ' + C(firm_id) + C(year)'
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    ols_fit = smf.ols(formula, data=ols_sample).fit()
resid = np.asarray(ols_fit.resid)
fitted = np.asarray(ols_fit.fittedvalues)
# Shapiro-Wilk's documented exact p-value accuracy is limited for N > 5000, so use a
# deterministic 5,000-residual subset and also report full-sample Jarque–Bera.
rng = np.random.default_rng(20260827)
shapiro_sub = rng.choice(resid, size=5000, replace=False)
shapiro_stat, shapiro_p = stats.shapiro(shapiro_sub)
jb_stat, jb_p = stats.jarque_bera(resid)
bp_lm, bp_p, bp_f, bp_f_p = het_breuschpagan(resid, ols_fit.model.exog, robust=True)
influence = ols_fit.get_influence()
cooks = np.asarray(influence.cooks_distance[0])
cook_threshold = 4 / len(ols_sample)
ols_diag = pd.DataFrame([{
    'Diagnostic': 'OLS count model residual diagnostics',
    'N': int(len(ols_sample)),
    'Mean residual': float(resid.mean()),
    'Residual SD': float(resid.std(ddof=1)),
    'Shapiro-Wilk W (deterministic n=5000 subset)': float(shapiro_stat),
    'Shapiro-Wilk p': float(shapiro_p),
    'Jarque-Bera statistic (full sample)': float(jb_stat),
    'Jarque-Bera p': float(jb_p),
    'Koenker-Breusch-Pagan LM': float(bp_lm),
    'Koenker-Breusch-Pagan p': float(bp_p),
    'Cook threshold 4/N': float(cook_threshold),
    'Max Cook distance': float(cooks.max()),
    'Observations above 4/N': int((cooks > cook_threshold).sum()),
    'Share above 4/N': float((cooks > cook_threshold).mean()),
}])
ols_diag.to_csv(TABLES / 'appendix_ols_count_diagnostics.csv', index=False)

# Residual versus fitted plot; a fixed random subsample prevents overplotting.
idx = rng.choice(np.arange(len(resid)), size=min(3000, len(resid)), replace=False)
fig, ax = plt.subplots(figsize=(7.0, 4.5), dpi=600)
ax.scatter(fitted[idx], resid[idx], alpha=0.20, s=9, color='#1f4e79', linewidths=0)
ax.axhline(0, color='black', lw=0.9)
ax.set_xlabel('Fitted value from count-OLS with firm/year dummies')
ax.set_ylabel('OLS residual')
ax.set_title('Count-OLS residual versus fitted diagnostic')
ax.text(0.02, 0.96, f'N={len(ols_sample):,}; zero count share={panel.green_invention_count.eq(0).mean():.1%}\n'
        f'Koenker–BP p={bp_p:.3g}; Shapiro p={shapiro_p:.3g}', transform=ax.transAxes,
        va='top', ha='left', fontsize=8, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#64748b', alpha=0.9))
fig.tight_layout()
fig.savefig(FIGURES / 'ols_count_residual_diagnostic.png', bbox_inches='tight')
plt.close(fig)

# 4) Declared five-model family multiple testing adjustment (S1–S5).
sens = pd.read_csv(SENSITIVITY_PATH)
family = sens.loc[sens['Specification'].str.startswith(('S1 ', 'S2 ', 'S3 ', 'S4 ', 'S5 '))].copy()
assert len(family) == 5, family['Specification'].tolist()
family['Bonferroni p'] = np.minimum(family['p_value'] * len(family), 1.0)
family['Holm p'] = multipletests(family['p_value'], method='holm')[1]
family['BH-FDR q'] = multipletests(family['p_value'], method='fdr_bh')[1]
family['Unadjusted significant at .05'] = family['p_value'] < 0.05
family['Holm significant at .05'] = family['Holm p'] < 0.05
family['Bonferroni significant at .05'] = family['Bonferroni p'] < 0.05
family.to_csv(TABLES / 'multiple_testing_adjustment_S1_S5.csv', index=False)

# 5) Two-part descriptive decomposition: the intensive model is conditioned on a
# current positive count. Both components are descriptive, not a structural hurdle/ZIP model.
controls_str = ' + '.join(CONTROLS)
extensive = pf.feols(f'positive_invention ~ log_dt + {controls_str} | firm_id + year', data=ols_sample, vcov={'CRV1': 'firm_id'})
positive = ols_sample.loc[ols_sample['positive_invention'].eq(1)].copy()
intensive = pf.feols(f'log_positive_invention ~ log_dt + {controls_str} | firm_id + year', data=positive, vcov={'CRV1': 'firm_id'})
def extract_component(name, fit):
    beta = float(fit.coef().loc['log_dt'])
    se = float(fit.se().loc['log_dt'])
    return {'Component': name, 'Coefficient': beta, 'Firm-clustered SE': se, 'p_value': float(fit.pvalue().loc['log_dt']),
            'CI 95 lower': beta - 1.959964 * se, 'CI 95 upper': beta + 1.959964 * se, 'N used by estimator': int(fit._N)}
two_part = pd.DataFrame([
    extract_component('Extensive margin: Pr(count > 0), TWFE linear probability sensitivity', extensive),
    extract_component('Intensive margin: ln(count) | count > 0, TWFE OLS sensitivity', intensive),
])
two_part.to_csv(TABLES / 'two_part_descriptive_decomposition.csv', index=False)

# 6) Updated self-contained distribution plot with requested key statistics.
dt = panel['dt_raw'].dropna()
count = panel['green_invention_count'].dropna()
fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.8), dpi=600)
axes[0].hist(dt, bins=70, color='#475569', edgecolor='white', linewidth=0.2)
axes[0].axvline(dt.median(), color='#b91c1c', lw=1.2, ls='--', label='Median')
axes[0].set_title('Raw digital-transformation score')
axes[0].set_xlabel('DT score')
axes[0].set_ylabel('Firm-year observations')
axes[0].text(0.98, 0.96, f'Mean = {dt.mean():.3f}\nMedian = {dt.median():.3f}\nSkewness = {stats.skew(dt, bias=False):.3f}',
             transform=axes[0].transAxes, ha='right', va='top', fontsize=8,
             bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#64748b', alpha=0.95))
axes[1].hist(count, bins=np.arange(-0.5, min(int(count.max()), 15) + 1.5, 1), color='#1f4e79', edgecolor='white', linewidth=0.4)
axes[1].set_title('Collaborative green invention count')
axes[1].set_xlabel('Patent count (axis truncated at 15 for visibility)')
axes[1].set_ylabel('Firm-year observations')
axes[1].text(0.98, 0.96, f'Zero share = {(count.eq(0).mean()):.1%}\nMean = {count.mean():.3f}\nMedian = {count.median():.3f}\nSkewness = {stats.skew(count, bias=False):.3f}',
             transform=axes[1].transAxes, ha='right', va='top', fontsize=8,
             bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#64748b', alpha=0.95))
fig.suptitle('Outcome zero mass and exposure skewness', y=1.02, fontsize=11)
fig.tight_layout()
fig.savefig(FIGURES / 'distribution_diagnostics_annotated.png', bbox_inches='tight')
plt.close(fig)

# Human-readable supplement.
def fmt(x):
    if isinstance(x, float):
        return f'{x:.6g}'
    return str(x)
lines = [
    '# Reviewer 1 Supplementary Statistical Analyses', '',
    '## A. Count-OLS diagnostic and status', '',
    'The two-way-fixed-effect OLS count model is reported only as a descriptive linear sensitivity. It is not the preferred count specification because the outcome has a large zero mass. Conditional PPML is retained as the preferred count model; it also has a different effective sample because all-zero firms do not identify a conditional firm effect.', '',
    ols_diag.T.rename(columns={0: 'Value'}).to_markdown(), '',
    'Shapiro–Wilk is run on a fixed, reproducible random subset of 5,000 residuals because its p-value calibration is documented as inaccurate for larger N. Jarque–Bera and robust Koenker–Breusch–Pagan are shown for the full diagnostic sample. With a discrete zero-heavy outcome, residual normality rejection is expected and is not used to make a causal conclusion; it supports demoting count-OLS below PPML.', '',
    '## B. Multiple-comparison adjustment', '',
    family.to_markdown(index=False), '',
    'The declared S1–S5 family contains five variations of one question: the two-way-fixed-effect association between DT and the same log collaborative-green-invention outcome. The Bonferroni threshold is 0.0100 (=0.05/5). No model in this family is significant after Holm, Bonferroni, or BH-FDR adjustment. Results are accordingly described as estimation uncertainty, not as a robust positive association.', '',
    '## C. Sample-selection diagnostics', '',
    selection.to_markdown(index=False), '',
    'Positive SMD means the matched complete-case panel has a higher mean than the full green-innovation source. SMD is a descriptive balance metric, not a causal correction. The graph `selection_love_plot.png` displays absolute SMDs, including a 0.10 visual reference.', '',
    '## D. Two-part descriptive decomposition', '',
    two_part.to_markdown(index=False), '',
    'This is not a ZIP or a structural hurdle model. It is a descriptive decomposition that separates current positive-count occurrence from logged count conditional on positivity, while retaining firm/year fixed effects in each linear component. It clarifies target populations without imposing an unverified zero-generating process.', '',
    '## E. Descriptive statistics and correlations', '',
    'See `appendix_descriptive_statistics.csv`, `appendix_correlation_pearson.csv`, and `appendix_correlation_spearman.csv`. The compact manuscript tables use a subset; full numeric tables are retained as supplement files.',
]
(TABLES / 'reviewer_r1_statistical_supplement.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')

# Machine-readable audit facts used by the revised manuscript.
audit = {
    'matched_panel_n': int(len(panel)),
    'ols_diagnostic_n': int(len(ols_sample)),
    'positive_count_share': float(panel['positive_invention'].mean()),
    'zero_count_share': float(1 - panel['positive_invention'].mean()),
    'raw_dt_mean': float(dt.mean()),
    'raw_dt_median': float(dt.median()),
    'raw_dt_skewness': float(stats.skew(dt, bias=False)),
    'count_mean': float(count.mean()),
    'count_median': float(count.median()),
    'count_skewness': float(stats.skew(count, bias=False)),
    'ols_diagnostics': ols_diag.iloc[0].to_dict(),
    'multiple_testing_family_size': int(len(family)),
    'bonferroni_alpha': 0.05 / len(family),
    'any_holm_significant': bool(family['Holm significant at .05'].any()),
    'selection_smd': selection.to_dict(orient='records'),
    'two_part': two_part.to_dict(orient='records'),
}
(METADATA / 'reviewer_r1_analysis_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
print((TABLES / 'reviewer_r1_statistical_supplement.md').read_text(encoding='utf-8'))
