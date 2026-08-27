# Digital Transformation and Collaborative Green Invention Output

[![Reproducibility](https://img.shields.io/badge/reproducibility-verified%20in%20sandbox-2e7d32)](#verification) [![Data](https://img.shields.io/badge/data-external%20DOI%20archives-blue)](data/DATA_ACCESS.md)

This repository provides an **auditable reproduction workflow** for the study *Digital Transformation and Collaborative Green Invention Output: A Transparent Matched-Panel Study of Chinese Listed Firms*. It links two public, DOI-archived data collections, rebuilds a 2014–2020 firm-year matched panel, fits two-way fixed-effects linear and PPML count specifications, and publishes only aggregate outputs.

> **Research scope.** This is an observational matched-panel analysis. It does not identify a causal effect of digital transformation. The available outcome is jointly applied green invention patents; it is reported as a proxy for **collaborative green invention output**, not as a complete measure of patent quality.

| Item | Value |
|---|---|
| Common analysis window | 2014–2020 |
| Matched raw panel | 6,574 firm-year observations; 1,468 firms |
| Main linear estimator | Firm and year fixed effects; firm-clustered CRV1 standard errors |
| Count sensitivity estimator | Conditional PPML with firm/year fixed effects; effective N=2,774 |
| Public data sources | Mendeley Data D1 and D2; see [data instructions](data/DATA_ACCESS.md) |
| Raw/matched data redistribution | **Not included in this public repository** |

## Key findings

The raw-DT two-way fixed-effects linear specification gives a coefficient of 0.000832 (`p=0.1911`) on the log collaborative-invention outcome. The `ln(1+DT)` variant gives 0.019628 (`p=0.0536`; N=6,443), and the preferred conditional PPML count model gives 0.093325 (`p=0.0655`; N=2,774). Neither is statistically significant at the conventional 5% level. No result in the declared five-model functional-form/control family remains significant after Holm or Bonferroni adjustment. Count-OLS is a supplemental diagnostic only; strict timing, period-split, IPW selection sensitivity, and descriptive extensive/intensive-margin results are also imprecise. These estimates indicate **estimation uncertainty**, not robust evidence of a positive association, a stable quality improvement, or a causal effect.

| Output | Location |
|---|---|
| Main estimates | [`results/tables/main_model_results.csv`](results/tables/main_model_results.csv) |
| Functional-form sensitivity | [`results/tables/specification_sensitivity.csv`](results/tables/specification_sensitivity.csv) |
| Strict timing/period tests | [`results/tables/robustness_tests.csv`](results/tables/robustness_tests.csv) |
| Reproduction audit | [`results/tables/reported_result_audit.md`](results/tables/reported_result_audit.md) |
| Literature/design comparison | [`docs/research_evidence_log.md`](docs/research_evidence_log.md) |
| Method upgrades and limitations | [`docs/model_and_methods_upgrade.md`](docs/model_and_methods_upgrade.md) |
| R1 diagnostics, multiplicity, selection and two-part results | [`results/reviewer_r1/`](results/reviewer_r1/) |
| R1 response letter | [`docs/reviewer_r1/RESPONSE_TO_REVIEWER_R1_FINAL.md`](docs/reviewer_r1/RESPONSE_TO_REVIEWER_R1_FINAL.md) |

## Repository layout

```text
.
├── data/                   # DOI links, license/reuse instructions; no source data
├── docs/                   # evidence log, experiment matrix, revision record
├── metadata/               # SHA-256 values of downloaded source archives
├── results/
│   ├── figures/            # aggregate diagnostic and coefficient figures
│   ├── tables/             # aggregate regression and audit tables
│   └── reviewer_r1/        # R1 aggregate diagnostics, selection/multiplicity supplements
├── src/                    # reproducible analysis scripts
├── tests/                  # integrity assertions
├── requirements.txt
└── README.md
```

## Quick start

### 1. Create an isolated environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Obtain the source archives

Follow the exact version and checksum guidance in [`data/DATA_ACCESS.md`](data/DATA_ACCESS.md). Put the two archives under a **local, private** directory, then point the public code to its `data/` directory. Do not commit downloaded files or the reconstructed firm-year panel to this public repository.

```bash
export DGI_PRIVATE_DATA_ROOT="/absolute/path/to/digital-green-invention-data-private/data"
```

### 3. Run the analysis in declared order

```bash
python src/run_analysis.py
python src/run_specification_sensitivity.py
python src/audit_reported_results.py
python src/run_robustness_tests.py
python src/run_reviewer_revision_analysis.py
python src/run_selection_ipw_sensitivity.py
python tests/test_reproducibility.py
python tests/test_reviewer_r1.py
```

The test assumes the source archives have been downloaded, their SHA-256 hashes match [`metadata/source_archive_sha256.txt`](metadata/source_archive_sha256.txt), and the private derived panel exists at the configured path. If your local path differs, set a private project root first rather than editing the source data.

## What is and is not publicly released

| Asset | Public repository | Private data repository | Reason |
|---|---:|---:|---|
| Analysis code and tests | Yes | Yes | Needed for auditability. |
| Environment specification | Yes | Yes | Needed for reproducibility. |
| DOI links, versions, hashes and variable notes | Yes | Yes | Provides source lineage without redistributing data. |
| Aggregate coefficient tables and figures | Yes | Yes | Non-row-level research outputs. |
| Downloaded ZIP/XLSX/DTA archives | No | Yes | Upstream source and redistribution terms may apply. |
| Matched firm-year panel | No | Yes | A derived dataset with firm identifiers and licensing constraints. |
| Original/submission manuscripts | No | Yes | Preserve author control before submission. |

## Reproducibility design

The scripts validate unique firm-year keys, year support, count zeros, matched sample size, model availability and figure creation. A second complete run produced byte-identical core matched-panel and main-model CSV outputs in the controlled environment. The R1 scripts add residual diagnostics for the supplemental count-OLS model, Holm/Bonferroni adjustment for the declared S1–S5 family, standardized mean differences, observed-covariate IPW sensitivity, and a descriptive two-part decomposition. The exact checks are described in [`docs/EXPERIMENT_MATRIX.md`](docs/EXPERIMENT_MATRIX.md), [`docs/MANUSCRIPT_REVISION_LOG.md`](docs/MANUSCRIPT_REVISION_LOG.md), and the [R1 response](docs/reviewer_r1/RESPONSE_TO_REVIEWER_R1_FINAL.md).

The source data are public DOI releases, but their underlying inputs cite services such as CNRDS, CSMAR, Wind and annual reports. This repository does not assert that those upstream records are sublicensable. Please review the source datasets’ terms before downloading, redistributing, or combining them with licensed data.

## Methodological notes

The study reports firm/year fixed effects and firm-clustered standard errors throughout. The PPML count model accommodates zero counts and high-dimensional fixed effects, but all-zero outcome firms do not identify a conditional firm effect and are excluded by the estimator. Its sample size must therefore be reported separately from linear FE models. The count-OLS result is retained only as a descriptive sensitivity and its residual diagnostics are public; PPML is the preferred count model. A zero-inflated or hurdle model would require unobserved-process assumptions not identified by the released fields, so the repository publishes a descriptive two-part decomposition rather than presenting a structural ZIP/hurdle claim. The model comparison follows the PPML and heteroskedasticity guidance of Correia, Guimarães, and Zylkin [1] and Santos Silva and Tenreyro [2].

For the detailed study-design comparison—rather than an invalid single-number “SOTA” ranking—see the evidence log. Published studies differ in source data, innovation outcomes, exposure construction, fixed effects and causal designs, so their coefficients and p-values cannot be treated as a common leaderboard.

## Citation

If this repository supports your work, cite the accompanying manuscript and the two data collections. A recommended data citation is:

```text
Bai, B. (2025). map-green innovation (Version 1) [Data set]. Mendeley Data.
https://doi.org/10.17632/wjw77byzc2.1

Meng, M. (2024). Digital transformation and strategic risk taking dataset
(Version 1) [Data set]. Mendeley Data. https://doi.org/10.17632/s3cdwjthnv.1
```

## References

[1] [Correia, S., Guimarães, P., & Zylkin, T. (2020). *Fast Poisson estimation with high-dimensional fixed effects*. The Stata Journal, 20(1), 95–115.](https://doi.org/10.1177/1536867X20909691)

[2] [Santos Silva, J. M. C., & Tenreyro, S. (2006). *The log of gravity*. The Review of Economics and Statistics, 88(4), 641–658.](https://doi.org/10.1162/rest.88.4.641)

[3] [Fang, L., & Li, Z. (2024). *Corporate digitalization and green innovation: Evidence from textual analysis of firm annual reports and corporate green patent data in China*. Business Strategy and the Environment, 33(5), 3936–3964.](https://doi.org/10.1002/bse.3677)

[4] [Dong, X., Meng, S., Xu, L., & Xin, Y. (2025). *Digital transformation and corporate green innovation forms: evidence from China*. Journal of Environmental Planning and Management, 68(11), 2644–2672.](https://doi.org/10.1080/09640568.2024.2320830)
