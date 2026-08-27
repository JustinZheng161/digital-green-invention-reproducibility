"""Regression tests for R2 aggregate model-audit outputs.

Run after `src/run_reviewer_r2_analysis.py` with DGI_PRIVATE_DATA_ROOT set.
Tests inspect only aggregate CSV outputs and do not read row-level data.
"""
from pathlib import Path
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / 'results' / 'reviewer_r2' / 'tables'

required = [
    'r2_sample_flow_and_estimator_profiles.csv',
    'r2_ppml_retention_decomposition.csv',
    'r2_timing_estimates_with_sample_composition.csv',
    'r2_timing_year_support.csv',
    'r2_availability_weight_diagnostics.csv',
    'r2_availability_calibration_models.csv',
]
for filename in required:
    path = TABLES / filename
    assert path.exists() and path.stat().st_size > 0, f'Missing R2 aggregate output: {path}'

profiles = pd.read_csv(TABLES / 'r2_sample_flow_and_estimator_profiles.csv')
expect_profiles = {
    'Matched complete-case panel': (6574, 1468),
    'TWFE log-outcome retained sample': (6443, 1337),
    'Conditional PPML retained sample': (2774, 505),
    'Strict t−1 PPML retained sample': (1891, 418),
    'Strict t+1 PPML retained sample': (1742, 387),
}
for label, (n, firms) in expect_profiles.items():
    row = profiles.loc[profiles['Sample'].eq(label)]
    assert len(row) == 1, label
    assert int(row['Observations'].iloc[0]) == n, (label, row['Observations'].iloc[0])
    assert int(row['Firms'].iloc[0]) == firms, (label, row['Firms'].iloc[0])

retention = pd.read_csv(TABLES / 'r2_ppml_retention_decomposition.csv')
expected_retention = {
    'All-zero-invention firms (not retained by conditional PPML)': (3782, 945),
    'Ever-positive firms removed by PPML preprocessing/separation': (18, 18),
    'Conditional PPML retained contribution set': (2774, 505),
}
for label, (n, firms) in expected_retention.items():
    row = retention.loc[retention['Stage / observed outcome group'].eq(label)]
    assert len(row) == 1, label
    assert int(row['Observations'].iloc[0]) == n
    assert int(row['Firms'].iloc[0]) == firms
assert int(retention['Observations'].sum()) == 13148, 'Rows overlap by design; do not interpret as a partition including the baseline row.'
assert int(retention.loc[retention['Stage / observed outcome group'].ne('Matched complete-case panel'), 'Observations'].sum()) == 6574

timing = pd.read_csv(TABLES / 'r2_timing_estimates_with_sample_composition.csv')
lag = timing.loc[timing['Test'].eq('Strict t−1 log DT PPML')].iloc[0]
lead = timing.loc[timing['Test'].eq('Strict t+1 log DT PPML placebo')].iloc[0]
assert int(lag['Retained observations']) == 1891
assert int(lead['Retained observations']) == 1742
assert math.isclose(float(lag['95% CI lower']), -0.06297, abs_tol=0.0002)
assert math.isclose(float(lead['95% CI upper']), 0.20663, abs_tol=0.0002)

support = pd.read_csv(TABLES / 'r2_timing_year_support.csv')
assert int(support.loc[(support['Test'].eq('Strict t−1')) & (support['Outcome year'].eq(2014)), 'Candidate observations'].iloc[0]) == 0
assert int(support.loc[(support['Test'].eq('Strict t+1')) & (support['Outcome year'].eq(2020)), 'Candidate observations'].iloc[0]) == 0

weights = pd.read_csv(TABLES / 'r2_availability_weight_diagnostics.csv').iloc[0]
assert math.isclose(float(weights['McFadden pseudo R2']), 0.0668, abs_tol=0.0002)
assert math.isclose(float(weights['Effective sample size after trimming']), 6228.0675, abs_tol=0.1)
models = pd.read_csv(TABLES / 'r2_availability_calibration_models.csv')
weighted = models.loc[models['Model'].eq('Availability-weighted FE calibration; selection covariates included')].iloc[0]
assert math.isclose(float(weighted['Coefficient on ln(1+DT)']), 0.0176366, abs_tol=0.0002)
assert math.isclose(float(weighted['p_value']), 0.1029822, abs_tol=0.0002)

print('PASS: R2 model-audit aggregate outputs match the locked published values.')
