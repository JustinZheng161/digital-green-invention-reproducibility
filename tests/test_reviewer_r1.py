"""Public-release integrity checks for the Reviewer-1 supplementary analyses."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / 'results/reviewer_r1/tables'
FIGURES = ROOT / 'results/reviewer_r1/figures'

for name in [
    'appendix_ols_count_diagnostics.csv', 'multiple_testing_adjustment_S1_S5.csv',
    'selection_standardized_mean_differences.csv', 'selection_ipw_sensitivity.csv',
    'two_part_descriptive_decomposition.csv', 'appendix_descriptive_statistics.csv',
    'appendix_correlation_pearson.csv', 'appendix_correlation_spearman.csv',
]:
    path = TABLES / name
    assert path.exists() and path.stat().st_size > 100, f'Missing R1 table: {path}'

for name in ['distribution_diagnostics_annotated.png', 'ols_count_residual_diagnostic.png', 'selection_love_plot.png']:
    path = FIGURES / name
    assert path.exists() and path.stat().st_size > 50_000, f'Missing R1 figure: {path}'

mult = pd.read_csv(TABLES / 'multiple_testing_adjustment_S1_S5.csv')
assert len(mult) == 5, 'Multiplicity family must remain the declared S1–S5 set.'
assert not mult['Holm significant at .05'].any(), 'No S1–S5 result should remain Holm-significant.'
assert not mult['Bonferroni significant at .05'].any(), 'No S1–S5 result should remain Bonferroni-significant.'
assert abs(0.05 / len(mult) - 0.01) < 1e-12, 'Expected Bonferroni alpha is 0.0100.'

ols = pd.read_csv(TABLES / 'appendix_ols_count_diagnostics.csv').iloc[0]
assert float(ols['Koenker-Breusch-Pagan p']) < 0.05, 'OLS diagnostic must record heteroskedasticity.'
assert float(ols['Shapiro-Wilk p']) < 0.05, 'OLS diagnostic must record non-normality.'

ipw = pd.read_csv(TABLES / 'selection_ipw_sensitivity.csv')
assert len(ipw) == 2 and float(ipw.loc[1, 'p_value']) > 0.05, 'Expected non-significant IPW sensitivity.'

print('PASS: R1 public aggregate artifacts and multiplicity/diagnostic assertions are intact.')
