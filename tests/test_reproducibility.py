from pathlib import Path
import os
import json
import hashlib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_DATA_ROOT = Path(os.environ.get('DGI_PRIVATE_DATA_ROOT', PROJECT_ROOT / 'data/private'))
panel_path = PRIVATE_DATA_ROOT / 'derived/matched_panel_private.csv'
audit_path = PRIVATE_DATA_ROOT / 'metadata/analysis_audit.json'
model_path = PROJECT_ROOT / 'results/tables/main_model_results.csv'
robust_path = PROJECT_ROOT / 'results/tables/robustness_tests.csv'

for path in (panel_path, audit_path, model_path, robust_path):
    assert path.exists(), f'Missing required file: {path}'

panel = pd.read_csv(panel_path)
audit = json.loads(audit_path.read_text(encoding='utf-8'))
models = pd.read_csv(model_path)
robust = pd.read_csv(robust_path)

assert len(panel) == 6574, f'Expected 6574 matched rows; found {len(panel)}'
assert panel['firm_id'].nunique() == 1468, 'Unexpected number of matched firms'
assert panel.duplicated(['firm_id', 'year']).sum() == 0, 'Duplicate firm-year keys found'
assert sorted(panel['year'].unique().tolist()) == list(range(2014, 2021)), 'Year window drifted'
assert abs((panel['green_invention_count'] == 0).mean() - 0.802251) < 1e-5, 'Zero-count diagnostic drifted'
assert abs(audit['variance_components']['within_to_total_variance_ratio'] - 0.135923) < 1e-5, 'Within-variation ratio drifted'
assert {'M0: OLS, log quality, raw DT, firm and year FE', 'M3: PPML, patent count, log DT, firm and year FE'}.issubset(set(models['Model'])), 'Main model set incomplete'
assert {'R1 Timing: PPML count with strict t−1 log DT; firm/year FE', 'R2 Placebo: PPML count with strict t+1 log DT; firm/year FE'}.issubset(set(robust['Test'])), 'Timing/Placebo tests incomplete'
assert (PROJECT_ROOT / 'results/figures/coefficient_comparison.png').stat().st_size > 50_000, 'Coefficient figure appears invalid'
assert (PROJECT_ROOT / 'results/figures/distribution_diagnostics.png').stat().st_size > 50_000, 'Distribution figure appears invalid'

hashes = {}
for path in (panel_path, model_path, robust_path):
    hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
print('PASS: all reproducibility and integrity checks completed')
print(json.dumps(hashes, indent=2))
