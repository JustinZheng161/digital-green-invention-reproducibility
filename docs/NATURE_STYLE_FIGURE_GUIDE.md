# Nature-style figure delivery guide

## Scope and boundary

This directory contains a **Nature-inspired graphical redesign** of the manuscript’s seven figures. It aligns technical presentation choices with the publicly available Nature figure and initial-submission guidance, including a clean sans-serif hierarchy, accessible colours, visible axes and ticks, lowercase bold panel labels, RGB delivery, editable vector formats, and high-resolution raster delivery.[1] [2] It **does not** claim that the manuscript has been submitted to, accepted by, or is within the scope of *Nature*.

The redesign does not alter the matched panel, estimators, confidence intervals, samples, reported coefficients, p-values, or scientific conclusions. Figure 1 uses a symmetric-log horizontal axis solely to expose the observed right tail of `DT_raw_count`; its underlying observations and 70-bin display remain unchanged. Figure 2 keeps separate horizontal scales for the log-outcome and conditional-PPML panels because their coefficients and retained samples are estimator-specific.

## Delivery package

Every semantic figure stem has four same-content outputs: a **600 dpi RGB PNG**, a **600 dpi RGB LZW-compressed TIFF**, an editable **SVG** retaining `<text>` elements, and a **PDF** embedding TrueType/Type-42-compatible fonts. The visual overview is [`nature_style_figure_contact_sheet.png`](../results/nature_style_figures/nature_style_figure_contact_sheet.png); the machine-readable provenance record is [`nature_style_figure_manifest.json`](../results/nature_style_figures/nature_style_figure_manifest.json).

| Manuscript figure | Semantic file stem | Reproducible input boundary | Design purpose |
|---|---|---|---|
| Figure 1 | `figure_01_dt_and_green_invention_distributions` | Private matched complete-case panel | Displays the observed DT right tail and zero-heavy count outcome. |
| Figure 2 | `figure_02_estimator_specific_associations` | Released aggregate R3 coefficient table | Shows estimates and 95% CIs without treating estimator-specific samples as interchangeable. |
| Figure A1 | `figure_A1_count_ols_residual_diagnostic` | Private matched panel; locked deterministic diagnostic | Displays residual-versus-fitted values for the established 3,000-observation subsample. |
| Figure B1 | `figure_B1_matching_selection_standardized_differences` | Released aggregate selection-SMD table | Shows descriptive source-versus-matched covariate differences. |
| Figure B2 | `figure_B2_estimator_sample_retention` | Released aggregate R2 sample-flow table | Shows estimator-specific retention relative to the matched panel. |
| Figure C1 | `figure_C1_ppml_residual_and_dispersion_diagnostics` | Private matched panel; locked conditional-PPML diagnostic | Shows residual and descriptive binned-dispersion screens. |
| Figure D1 | `figure_D1_strict_timing_estimator_support` | Released aggregate R2 year-support table | Shows calendar-year support for strict timing estimators. |

## Reproduction and checks

The source is [`src/rebuild_nature_style_figures.py`](../src/rebuild_nature_style_figures.py). It reads only designated aggregate tables for Figures 2/B1/B2/D1 and uses the configured private panel for the three diagnostics requiring row-level data. It writes no private inputs to this public repository. Set `DGI_PRIVATE_DATA_ROOT` to a local private data directory before running it.

```bash
export DGI_PRIVATE_DATA_ROOT="/absolute/path/to/digital-green-invention-data-private/data"
python src/rebuild_nature_style_figures.py
python src/build_figure_contact_sheet.py
python tests/test_nature_style_figures.py
```

The asset test fails closed unless there are exactly seven manifest figures; each has a semantic PNG/PDF/SVG/TIFF quartet; PNG/TIFF are 600 dpi RGB; TIFF uses LZW; SVG contains live text; the PDF contains embedded TrueType/Type-42-compatible font data; and the contact sheet exists. This repository releases only code, aggregate inputs, figures, and documentation. The row-level matched panel and the complete manuscript remain private.

## References

[1] [Nature Portfolio. *Figure guide*.](https://www.nature.com/nature/for-authors/final-submission)

[2] [Nature Portfolio. *Initial submission: formatting guide*.](https://www.nature.com/nature/for-authors/initial-submission)
