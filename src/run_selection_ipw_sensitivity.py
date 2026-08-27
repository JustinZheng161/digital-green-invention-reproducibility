"""IPW sensitivity for availability of the D1–D2 matched panel.

This is a descriptive observed-covariate calibration. It cannot correct selection
on unobserved determinants of digital transformation or patent output.
"""
from pathlib import Path
import os
import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path(os.environ.get('DGI_PRIVATE_DATA_ROOT', PROJECT_ROOT / 'data/private'))
TABLES = PROJECT_ROOT / 'results/reviewer_r1/tables'
METADATA = PRIVATE / 'metadata'
TABLES.mkdir(parents=True, exist_ok=True)

GREEN_PATH = PRIVATE / 'raw/extracted/green/map-green innovation/dataset-final.dta'
PANEL_PATH = PRIVATE / 'derived/matched_panel_private.csv'
CONTROLS = [
    'leverage', 'cash_flow', 'firm_size', 'book_to_market', 'roa', 'growth',
    'fixed_asset_ratio', 'equity_balance', 'independent_directors', 'board_size',
    'largest_holder', 'employee_scale', 'ceo_duality', 'soe',
]
GREEN_COLS = {
    '股票代码': 'firm_id', '会计年度': 'year', '资产负债率': 'leverage', 'Cflow': 'cash_flow',
    'Size': 'firm_size', 'BM': 'book_to_market', 'ROA': 'roa', 'Growth': 'growth',
    '固定资产比率': 'fixed_asset_ratio', '股权制衡度': 'equity_balance', 'Indep': 'independent_directors',
    '董事会规模': 'board_size', '第一大股东持股比率': 'largest_holder', 'Staff': 'employee_scale',
    'Dual': 'ceo_duality', 'soe': 'soe', '当年联合申请的绿色发明数量': 'green_invention_count',
}

green = pd.read_stata(GREEN_PATH, convert_categoricals=False)
green = green[list(GREEN_COLS)].rename(columns=GREEN_COLS)
for key in ('firm_id', 'year'):
    green[key] = pd.to_numeric(green[key], errors='raise').astype('int64')
matched = pd.read_csv(PANEL_PATH)
matched_keys = matched[['firm_id', 'year']].drop_duplicates().assign(matched=1)
frame = green.merge(matched_keys, on=['firm_id', 'year'], how='left', validate='one_to_one')
frame['matched'] = frame['matched'].fillna(0).astype(int)

# Availability model uses covariates observed in the green source and year only;
# it deliberately excludes contemporaneous patent outcomes to avoid conditioning on the outcome.
selection_formula = 'matched ~ ' + ' + '.join(CONTROLS) + ' + C(year)'
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    select_fit = smf.logit(selection_formula, data=frame).fit(disp=False, maxiter=100)
frame['p_matched'] = np.asarray(select_fit.predict(frame))
matched_frame = frame.loc[frame['matched'].eq(1), ['firm_id', 'year', 'p_matched']].copy()
analysis = matched.merge(matched_frame, on=['firm_id', 'year'], how='inner', validate='one_to_one')
firm_counts = analysis.groupby('firm_id')['firm_id'].transform('size')
analysis = analysis.loc[firm_counts > 1].copy()
stabilizer = frame['matched'].mean()
analysis['ipw_stabilized'] = stabilizer / analysis['p_matched']
# Protect the reported weighting sensitivity from a small set of very large weights.
lo, hi = analysis['ipw_stabilized'].quantile([0.01, 0.99])
analysis['ipw_stabilized_winsor'] = analysis['ipw_stabilized'].clip(lo, hi)

outcome_formula = 'green_quality_log ~ log_dt + ' + ' + '.join(CONTROLS) + ' + C(firm_id) + C(year)'
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    unweighted = smf.ols(outcome_formula, data=analysis).fit(cov_type='cluster', cov_kwds={'groups': analysis['firm_id']})
    ipw = smf.wls(outcome_formula, data=analysis, weights=analysis['ipw_stabilized_winsor']).fit(cov_type='cluster', cov_kwds={'groups': analysis['firm_id']})

rows = []
for label, fit in [('Unweighted dummy-FE reference', unweighted), ('Stabilized IPW (1%/99% winsorized) dummy-FE sensitivity', ipw)]:
    beta = float(fit.params['log_dt'])
    se = float(fit.bse['log_dt'])
    rows.append({
        'Model': label,
        'Coefficient on ln(1+DT)': beta,
        'Firm-clustered SE': se,
        'p_value': float(fit.pvalues['log_dt']),
        'CI 95 lower': beta - 1.959964 * se,
        'CI 95 upper': beta + 1.959964 * se,
        'N': int(fit.nobs),
    })
results = pd.DataFrame(rows)
results.to_csv(TABLES / 'selection_ipw_sensitivity.csv', index=False)
weight_summary = pd.DataFrame([{
    'D1 source observations': int(len(frame)),
    'Matched observations': int(frame['matched'].sum()),
    'Matched share': float(frame['matched'].mean()),
    'Propensity min in matched': float(analysis['p_matched'].min()),
    'Propensity p1 in matched': float(analysis['p_matched'].quantile(.01)),
    'Propensity median in matched': float(analysis['p_matched'].median()),
    'Propensity p99 in matched': float(analysis['p_matched'].quantile(.99)),
    'Propensity max in matched': float(analysis['p_matched'].max()),
    'Stabilized IPW mean before winsor': float(analysis['ipw_stabilized'].mean()),
    'Stabilized IPW p1/p99': f'{lo:.6f} / {hi:.6f}',
    'Pseudo R2 selection logit': float(select_fit.prsquared),
}])
weight_summary.to_csv(TABLES / 'selection_ipw_weight_diagnostics.csv', index=False)

lines = [
    '# Observed-Covariate Selection Calibration (IPW Sensitivity)', '',
    'The propensity model predicts D1–D2 matched-panel availability using the D1 controls and calendar-year indicators. It **does not** use patent outcomes and cannot correct selection on unobserved determinants, different source-population frames, or DT values unavailable for unmatched observations. It is therefore a sensitivity analysis for observed covariate imbalance, not an identification strategy.', '',
    '## Weight diagnostics', '', weight_summary.to_markdown(index=False), '',
    '## Weighted two-way-FE linear sensitivity', '', results.to_markdown(index=False), '',
    'The weighted result should be interpreted only as: “after reweighting matched observations toward the D1 green-source distribution on observed D1 controls and year, the linear association has the following value.” It does not permit extrapolation to all listed firms or resolve causal confounding.',
]
(TABLES / 'selection_ipw_sensitivity.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
(METADATA / 'selection_ipw_audit.json').write_text(json.dumps({'weights': weight_summary.iloc[0].to_dict(), 'models': results.to_dict(orient='records')}, ensure_ascii=False, indent=2), encoding='utf-8')
print((TABLES / 'selection_ipw_sensitivity.md').read_text(encoding='utf-8'))
