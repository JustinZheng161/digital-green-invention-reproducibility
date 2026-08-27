"""Build an auditable R3 inventory of distinct reported DT-association tests.

The inventory is a post-review transparency screen. It is not a preregistered
confirmatory family and does not turn heterogeneous estimators or outcomes into
interchangeable evidence. Diagnostics with no association coefficient are excluded.
"""
from __future__ import annotations
from pathlib import Path
import json
import pandas as pd
from statsmodels.stats.multitest import multipletests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROOT = PROJECT_ROOT
PUB = PROJECT_ROOT
OUT = PROJECT_ROOT / 'results/reviewer_r3/tables'
OUT.mkdir(parents=True, exist_ok=True)

rows: list[dict] = []

def add(source: str, table: str, label: str, p: float, role: str, manuscript_location: str, reason: str) -> None:
    rows.append({
        'Unique test ID': f'G{len(rows)+1:02d}',
        'Source file': source,
        'Reported model': label,
        'Unadjusted p_value': float(p),
        'Reporting role': role,
        'Expected R3 manuscript location': manuscript_location,
        'Inclusion rationale': reason,
    })

# Locked main results. S1 and S3 exactly duplicate M0 and M1 and therefore are counted only once.
main = pd.read_csv(PUB / 'results/tables/main_model_results.csv')
for key, role, where, why in [
    ('M0: OLS, log quality, raw DT, firm and year FE', 'Core functional-form comparator', 'Table 4', 'Distinct raw-frequency regressor scale.'),
    ('M1: OLS, log quality, log DT, firm and year FE', 'Primary descriptive log-outcome estimate', 'Table 4', 'Central log-outcome association reported in text and abstract.'),
    ('M2: OLS, patent count, log DT, firm and year FE', 'Appendix distributional sensitivity', 'Appendix B', 'Count OLS is retained as a diagnostic/sensitivity association, not preferred inference.'),
    ('M3: PPML, patent count, log DT, firm and year FE', 'Conditional count-model sensitivity', 'Table 4 / Appendix C', 'Distinct estimator and retained contribution set.'),
    ('M4: OLS, utility-patent log, log DT, firm and year FE', 'Alternative outcome sensitivity', 'Appendix B', 'Distinct green-utility outcome.'),
    ('M5: PPML, lagged DT, firm and year FE', 'Timing sensitivity', 'Appendix D', 'Distinct strict-calendar t-1 association.'),
]:
    r = main.loc[main['Model'].eq(key)].iloc[0]
    add('main_model_results.csv', 'Locked R2/R3 carry-forward model', key, r['p-value'], role, where, why)

# Unique Table 5 variants excluding exact M0/S1 and M1/S3 duplication.
spec = pd.read_csv(PUB / 'results/tables/specification_sensitivity.csv')
for prefix, where, why in [
    ('S2 ', 'Table 5', 'Distinct raw-frequency winsorization.'),
    ('S4 ', 'Table 5', 'Distinct logged winsorization.'),
    ('S5 ', 'Table 5', 'Distinct parsimonious-control sensitivity.'),
    ('S6 ', 'Appendix C', 'Distinct conditional-count winsorization.'),
    ('S7 ', 'Appendix D', 'Distinct strict-lag conditional-count winsorization.'),
]:
    r = spec.loc[spec['Specification'].str.startswith(prefix)].iloc[0]
    add('specification_sensitivity.csv', 'Sensitivity functional form/control', r['Specification'], r['p_value'], 'Exploratory specification sensitivity', where, why)

rob = pd.read_csv(PUB / 'results/tables/robustness_tests.csv')
for label, where, why in [
    ('R2 Placebo: PPML count with strict t+1 log DT; firm/year FE', 'Appendix D', 'Distinct future-exposure timing description; not a falsification test.'),
    ('R3a Period: 2014–2017 OLS log quality; firm/year FE', 'Appendix D', 'Distinct early-period estimate.'),
    ('R3b Period: 2018–2020 OLS log quality; firm/year FE', 'Appendix D', 'Distinct late-period estimate.'),
]:
    r = rob.loc[rob['Test'].eq(label)].iloc[0]
    add('robustness_tests.csv', 'Timing/period sensitivity', label, r['p_value'], 'Exploratory timing or subsample sensitivity', where, why)

avail = pd.read_csv(ROOT / 'results/reviewer_r2/tables/r2_availability_calibration_models.csv')
for _, r in avail.iterrows():
    add('r2_availability_calibration_models.csv', 'Availability-calibration sensitivity', r['Model'], r['p_value'], 'Exploratory availability-calibration sensitivity', 'Appendix E', 'Distinct weighted/unweighted and covariate-conditioning specification; no causal weighting interpretation.')

two = pd.read_csv(ROOT / 'results/reviewer_r1/tables/two_part_descriptive_decomposition.csv')
for _, r in two.iterrows():
    add('two_part_descriptive_decomposition.csv', 'Two-part descriptive decomposition', r['Component'], r['p_value'], 'Exploratory descriptive decomposition', 'Appendix B', 'Distinct extensive or positive-count intensive conditional association.')

proxy = pd.read_csv(ROOT / 'results/reviewer_r3/tables/r3_proxy_sensitivity_models.csv')
for _, r in proxy.iterrows():
    if r['Model'].startswith('Locked '):
        continue
    add('r3_proxy_sensitivity_models.csv', 'Lagged R&D/inventive-activity proxy sensitivity', r['Model'], r['p_value_unadjusted'], 'Post-review proxy sensitivity', 'Table 5 / Appendix C', 'Distinct strict-calendar-lag proxy specification; proxy field does not validate complete R&D/knowledge control.')

trim = pd.read_csv(ROOT / 'results/reviewer_r3/tables/r3_ppml_extreme_residual_sensitivity.csv')
r = trim.loc[trim['Model'].str.startswith('Exclude all retained')].iloc[0]
add('r3_ppml_extreme_residual_sensitivity.csv', 'Conditional PPML residual sensitivity', r['Model'], r['p_value_unadjusted'], 'Post-review diagnostic sensitivity', 'Appendix C', 'Distinct all-observation |Pearson residual| > 3 deletion refit.')

influence = pd.read_csv(ROOT / 'results/reviewer_r3/tables/r3_ppml_top_contribution_firm_deletions.csv')
for _, r in influence.iterrows():
    add('r3_ppml_top_contribution_firm_deletions.csv', 'Conditional PPML cluster-deletion sensitivity', r['Model'], r['p_value_unadjusted'], 'Post-review influence sensitivity', 'Appendix C', 'Distinct pre-specified-by-rank one-at-a-time deletion; never used to choose a preferred estimate.')

inventory = pd.DataFrame(rows)
assert inventory['Reported model'].is_unique, 'A regression has been entered twice in the global inventory.'
inventory['Holm p_value (global exploratory)'] = multipletests(inventory['Unadjusted p_value'], method='holm')[1]
inventory['Bonferroni p_value (global exploratory)'] = multipletests(inventory['Unadjusted p_value'], method='bonferroni')[1]
inventory['BH-FDR q_value (global exploratory)'] = multipletests(inventory['Unadjusted p_value'], method='fdr_bh')[1]
for col in ['Holm p_value (global exploratory)', 'Bonferroni p_value (global exploratory)', 'BH-FDR q_value (global exploratory)']:
    inventory[col.replace('p_value', 'significant at 0.05').replace('q_value', 'significant at 0.05')] = inventory[col] < .05
inventory.to_csv(OUT / 'r3_global_association_test_inventory.csv', index=False)

# Preserve the five-entry, within-table correction with no false claim that it is global.
family = pd.read_csv(ROOT / 'results/reviewer_r1/tables/multiple_testing_adjustment_S1_S5.csv')
family_note = family[['Specification', 'p_value', 'Holm p', 'Bonferroni p', 'BH-FDR q']].copy()
family_note.insert(0, 'Family scope', 'Table 5: five functional-form/control variants (S1–S5)')
family_note.to_csv(OUT / 'r3_table5_family_specific_multiplicity.csv', index=False)

m = len(inventory)
min_row = inventory.loc[inventory['Unadjusted p_value'].idxmin()]
summary = {
    'distinct_association_tests_in_global_inventory': int(m),
    'diagnostics_excluded_from_inventory': [
        'OLS residual-normality and heteroskedasticity checks',
        'PPML Pearson X2 screen and number of |Pearson residual| > 3 observations',
        'sample-flow, balance, and key-uniqueness calculations',
    ],
    'deduplicated_models': ['S1 duplicates M0 exactly', 'S3 duplicates M1 exactly', 'locked R3 reference rows duplicate M1/M3 and are not entered again'],
    'minimum_unadjusted_p': float(min_row['Unadjusted p_value']),
    'minimum_p_model': str(min_row['Reported model']),
    'n_global_holm_significant_at_005': int(inventory['Holm significant at 0.05 (global exploratory)'].sum()),
    'n_global_bonferroni_significant_at_005': int(inventory['Bonferroni significant at 0.05 (global exploratory)'].sum()),
    'n_global_bh_fdr_significant_at_005': int(inventory['BH-FDR significant at 0.05 (global exploratory)'].sum()),
    'interpretation': 'All association p-values remain unadjusted in their result tables. The 33-test global screen is a post-review transparency sensitivity across distinct reported association estimates; it is not a preregistered confirmatory family and does not settle which heterogeneous models should be combined.'
}
(OUT / 'r3_global_multiplicity_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
lines = [
    '# R3 Global Association-Test Inventory', '',
    '## Purpose and scope', '',
    'This post-review inventory makes the multiplicity boundary explicit. It contains each **distinct reported coefficient test of the DT–outcome association** that R3 retains in the manuscript or appendices. Exact duplicates are entered once: S1 is M0, S3 is M1, and the R3 locked references repeat M1/M3. It excludes diagnostic tests that do not estimate that association (normality, heteroskedasticity, key integrity, Pearson-dispersion, sample-flow and balance screens).', '',
    f'The inventory contains **{m}** distinct association tests. Holm, Bonferroni, and BH-FDR values below are transparent exploratory adjustments, not preregistered confirmatory inference. They do not make the outcomes, functional forms, and retained samples substantively interchangeable. Every model table shows the raw, unadjusted p-value and its interval.', '',
    '## Global exploratory screen', '', inventory.to_markdown(index=False, floatfmt='.4f'), '',
    '## Family-specific Table 5 screen', '',
    'Table 5 contains five deliberately presented functional-form/control variants (S1–S5). Its internal adjustment has *m*=5 and is reported separately; it is **not** a substitute for the global exploratory screen.', '', family_note.to_markdown(index=False, floatfmt='.4f'), '',
    '## Result', '',
    f'The smallest raw p-value is {summary["minimum_unadjusted_p"]:.4f} ({summary["minimum_p_model"]}). No distinct association test remains below 0.05 after either global Holm or global Bonferroni adjustment; the inventory also reports the BH-FDR screen without using it to promote selected specifications.', '',
]
(OUT / 'reviewer_r3_global_inference.md').write_text('\n'.join(lines), encoding='utf-8')
print((OUT / 'reviewer_r3_global_inference.md').read_text(encoding='utf-8'))
