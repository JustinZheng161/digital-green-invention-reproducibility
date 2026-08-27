"""Regression tests for R3 aggregate outputs; no microdata are read."""
from pathlib import Path
import json
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
R3 = ROOT / 'results' / 'reviewer_r3'
TABLES = R3 / 'tables'
required = [
    'r3_proxy_sensitivity_models.csv',
    'r3_ppml_pearson_residual_summary.csv',
    'r3_ppml_extreme_residual_sensitivity.csv',
    'r3_ppml_top_contribution_firm_deletions.csv',
    'r3_global_association_test_inventory.csv',
    'r3_global_multiplicity_summary.json',
    'r3_d2_rd_proxy_audit.json',
    'r3_rd_ppml_feasibility.json',
    'd1_candidate_field_dictionary.json',
]
for name in required:
    p = TABLES / name
    assert p.exists() and p.stat().st_size > 0, f'Missing R3 public aggregate artifact: {p}'

proxy = pd.read_csv(TABLES / 'r3_proxy_sensitivity_models.csv')
assert len(proxy) == 8
base_log = proxy.loc[proxy['Model'].eq('Locked log-outcome reference')].iloc[0]
lag_rd_log = proxy.loc[proxy['Model'].eq('Lagged released R&D-expenditure field: log outcome')].iloc[0]
both_ppml = proxy.loc[proxy['Model'].eq('Both lagged proxy fields: conditional count')].iloc[0]
assert int(base_log['Retained observations']) == 6443
assert math.isclose(float(base_log['p_value_unadjusted']), .0536213, abs_tol=.0002)
assert int(lag_rd_log['Retained observations']) == 4222
assert math.isclose(float(lag_rd_log['Coefficient on DT_log']), .0239, abs_tol=.0002)
assert int(both_ppml['Retained observations']) == 1891
assert math.isclose(float(both_ppml['p_value_unadjusted']), .2237, abs_tol=.0003)

pearson = pd.read_csv(TABLES / 'r3_ppml_pearson_residual_summary.csv').iloc[0]
assert int(pearson['Retained observations']) == 2774
assert int(pearson['Retained firms']) == 505
assert int(pearson['Observations above absolute threshold']) == 65
assert math.isclose(float(pearson['Pearson X2 / approximate df']), 1.5914, abs_tol=.001)
trim = pd.read_csv(TABLES / 'r3_ppml_extreme_residual_sensitivity.csv')
trimmed = trim.loc[trim['Model'].str.startswith('Exclude all retained')].iloc[0]
assert int(trimmed['Retained observations']) == 2636
assert math.isclose(float(trimmed['Coefficient on DT_log']), .0861, abs_tol=.0002)
assert math.isclose(float(trimmed['p_value_unadjusted']), .0529, abs_tol=.0002)
influence = pd.read_csv(TABLES / 'r3_ppml_top_contribution_firm_deletions.csv')
assert len(influence) == 6
assert influence['Anonymous rank'].astype(int).tolist() == [1, 2, 3, 4, 5, 6]
assert math.isclose(float(influence['Coefficient on DT_log'].min()), .0782, abs_tol=.0002)
assert math.isclose(float(influence['Coefficient on DT_log'].max()), .1016, abs_tol=.0002)

inventory = pd.read_csv(TABLES / 'r3_global_association_test_inventory.csv')
summary = json.loads((TABLES / 'r3_global_multiplicity_summary.json').read_text(encoding='utf-8'))
assert len(inventory) == 33
assert summary['distinct_association_tests_in_global_inventory'] == 33
assert summary['n_global_holm_significant_at_005'] == 0
assert summary['n_global_bonferroni_significant_at_005'] == 0
assert summary['n_global_bh_fdr_significant_at_005'] == 0
assert math.isclose(float(summary['minimum_unadjusted_p']), .0111502, abs_tol=.000001)

rd_audit = json.loads((TABLES / 'r3_d2_rd_proxy_audit.json').read_text(encoding='utf-8'))
assert rd_audit['matched_panel_observations'] == 6574
assert rd_audit['valid_intensity_observations'] == 6574
assert rd_audit['rd_missing_or_negative'] == 0
assert rd_audit['revenue_missing_or_nonpositive'] == 0
assert rd_audit['unit_interpretation'].startswith('The data article describes')
feasibility = json.loads((TABLES / 'r3_rd_ppml_feasibility.json').read_text(encoding='utf-8'))
assert feasibility['rd_named_field_found'] is False
assert feasibility['technology_personnel_named_field_found'] is False
assert feasibility['ppml_retained_observations'] == 2774
labels = json.loads((TABLES / 'd1_candidate_field_dictionary.json').read_text(encoding='utf-8'))
lngpfm = [x for x in labels['candidate_fields'] if x['field'] == 'lngpfm']
assert len(lngpfm) == 1 and lngpfm[0]['stata_label'] == 'ln(invention patent +1)'
print('PASS: R3 aggregate proxy, diagnostic, and multiplicity outputs match locked values.')
