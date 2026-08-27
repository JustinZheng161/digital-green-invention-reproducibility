# Digital Transformation and Collaborative Green Invention Output

[![Reproducibility](https://img.shields.io/badge/reproducibility-verified%20in%20sandbox-2e7d32)](#verification) [![Data](https://img.shields.io/badge/data-external%20DOI%20archives-blue)](data/DATA_ACCESS.md)

This repository provides an **auditable reproduction workflow** for the study *Digital Transformation and Collaborative Green Invention Output: A Transparent Analysis of a Matched Panel of Chinese Listed Firms*. It links two public, DOI-archived data collections, rebuilds a deterministic 2014–2020 firm-year matched panel, fits two-way fixed-effects linear and conditional-PPML count specifications, and publishes only aggregate outputs.

> **Research scope.** This is an observational matched-panel analysis. It does not identify a causal effect of digital transformation. The available outcome is jointly applied green invention patents; it is reported as a proxy for **collaborative green invention output**, not as a complete measure of patent quality.

| Item | Value |
|---|---|
| Common analysis window | 2014–2020 |
| Matched complete-case panel | 6,574 firm-year observations; 1,468 firms (59.5% of the D1 green-source file) |
| Main linear estimator | Firm and year fixed effects; firm-clustered CRV1 standard errors; retained N=6,443 from 1,337 firms |
| Count sensitivity estimator | Conditional PPML with firm/year fixed effects; retained N=2,774 from 505 firms (42.2% of matched observations) |
| Stored D2 exposure field | `DT_raw_count`: integer-valued raw-count-like annual-report digital-keyword frequency; `DT_log = ln(1 + DT_raw_count)` is the primary transformed regressor |
| Public data sources | Mendeley Data D1 and D2; see [data instructions](data/DATA_ACCESS.md) |
| Raw/matched data redistribution | **Not included in this public repository** |

## Key findings

The raw-DT two-way fixed-effects linear specification gives a coefficient of 0.000832 (`p=0.1911`) on the log collaborative-invention outcome. The `ln(1+raw DT)` variant gives 0.019628 (`p=0.0536`; N=6,443), and the conditional PPML count model gives 0.093325 (`p=0.0655`; N=2,774). Neither is statistically significant at the conventional 5% level. No result in the **post hoc exploratory** five-model functional-form/control family remains significant after Holm or Bonferroni adjustment. A deduplicated R3 inventory of 33 distinct reported DT-association tests likewise has no result below 0.05 under global Holm, Bonferroni, or BH-FDR adjustment. Count-OLS is a supplemental diagnostic only; its formal residual-test p-values are not treated as exact iid panel tests. A descriptive two-part decomposition separates the extensive margin (Pr(count > 0)) from the positive-count intensive margin; strict timing, period-split, availability-calibration sensitivity, and both two-part components remain imprecise. These results indicate **statistical imprecision** rather than a robust positive association or a causal effect; they do not prove an exact zero association. Findings apply only to the deterministic matched panel and the stated estimator-retained contribution sets, not to the full population of Chinese listed firms.

| Output | Location |
|---|---|
| Main estimates | [`results/tables/main_model_results.csv`](results/tables/main_model_results.csv) |
| Functional-form sensitivity | [`results/tables/specification_sensitivity.csv`](results/tables/specification_sensitivity.csv) |
| Strict timing/period tests | [`results/tables/robustness_tests.csv`](results/tables/robustness_tests.csv) |
| Reproduction audit | [`results/tables/reported_result_audit.md`](results/tables/reported_result_audit.md) |
| Literature/design comparison | [`docs/research_evidence_log.md`](docs/research_evidence_log.md) |
| Method upgrades and limitations | [`docs/model_and_methods_upgrade.md`](docs/model_and_methods_upgrade.md) |
| Model and experiment upgrade report | [`docs/MODEL_UPGRADE_REPORT.md`](docs/MODEL_UPGRADE_REPORT.md) |
| Control-block ablation and exposure robustness | [`results/tables/model_upgrade_sensitivities.csv`](results/tables/model_upgrade_sensitivities.csv) |
| R1 diagnostics, multiplicity, selection and two-part results | [`results/reviewer_r1/`](results/reviewer_r1/) |
| R1 response letter | [`docs/reviewer_r1/RESPONSE_TO_REVIEWER_R1_FINAL.md`](docs/reviewer_r1/RESPONSE_TO_REVIEWER_R1_FINAL.md) |
| R2 sample/PPML/IPW/timing audit | [`results/reviewer_r2/tables/reviewer_r2_model_audit.md`](results/reviewer_r2/tables/reviewer_r2_model_audit.md) |
| R2 response letter | [`docs/RESPONSE_TO_REVIEWER_R2_FINAL.md`](docs/RESPONSE_TO_REVIEWER_R2_FINAL.md) |
| R3 R&D/proxy, PPML, and global-inference outputs | [`results/reviewer_r3/`](results/reviewer_r3/) |
| R3 reviewer matrix and response | [`docs/reviewer_r3/`](docs/reviewer_r3/) |
| Round-4 reviewer response and closure matrix | [`docs/REVIEWER_ROUND4_RESPONSE.md`](docs/REVIEWER_ROUND4_RESPONSE.md) |
| Two-part descriptive decomposition | [`results/reviewer_r1/tables/two_part_descriptive_decomposition.csv`](results/reviewer_r1/tables/two_part_descriptive_decomposition.csv) |

## Repository layout

```text
.
├── data/                   # DOI links, license/reuse instructions; no source data
├── docs/                   # evidence log, experiment matrix, revision record
├── metadata/               # SHA-256 values of downloaded source archives
├── results/
│   ├── figures/            # aggregate diagnostic and coefficient figures
│   ├── tables/             # aggregate regression and audit tables
│   ├── reviewer_r1/        # R1 aggregate diagnostics, selection/multiplicity supplements
│   ├── reviewer_r2/        # R2 estimator-retention, timing and availability-calibration audit
│   └── reviewer_r3/        # R3 proxy, PPML diagnostic, and global-multiplicity outputs
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
python src/run_model_upgrades.py
python src/run_specification_sensitivity.py
python src/audit_reported_results.py
python src/run_robustness_tests.py
python src/run_reviewer_revision_analysis.py
python src/run_selection_ipw_sensitivity.py
python src/run_reviewer_r2_analysis.py
python src/run_reviewer_r3_analysis.py
python src/build_r3_multiplicity_inventory.py
python tests/test_reproducibility.py
python tests/test_reviewer_r1.py
python tests/test_reviewer_r2.py
python tests/test_reviewer_r3.py
python tests/test_model_upgrades.py
python tests/audit_public_release.py
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

The scripts validate unique firm-year keys, year support, count zeros, matched sample size, model availability and figure creation. A second complete run produced byte-identical core matched-panel and main-model CSV outputs in the controlled environment. The R1 scripts add residual diagnostics for the supplemental count-OLS model, Holm/Bonferroni adjustment for the S1–S5 family, standardized mean differences, observed-covariate calibration, and a descriptive two-part decomposition. The R2 script verifies the raw-count-like stored D2 scale, reports conditional-PPML retention (including all-zero-firm and preprocessing/separation components), reports strict timing support by year, and redefines IPW as availability calibration—not causal weighting. The exact checks are described in [`docs/EXPERIMENT_MATRIX.md`](docs/EXPERIMENT_MATRIX.md), [`docs/MANUSCRIPT_REVISION_LOG.md`](docs/MANUSCRIPT_REVISION_LOG.md), and the [R2 response](docs/RESPONSE_TO_REVIEWER_R2_FINAL.md).

The source data are public DOI releases, but their underlying inputs cite services such as CNRDS, CSMAR, Wind and annual reports. The model-upgrade script produces aggregate tables only and runs with `DGI_PRIVATE_DATA_ROOT`; raw archives and row-level panels remain outside this public repository. This repository does not assert that those upstream records are sublicensable. Please review the source datasets’ terms before downloading, redistributing, or combining them with licensed data. The R3 proxy analyses use the released D2 `R&D expenditure` field only after a strict calendar-year lag; because the workbook does not disclose that field’s numerical transformation or units, it is not represented as verified R&D intensity. The D1 `lngpfm` field is similarly a lagged inventive-activity proxy, not a patent stock.

## Methodological notes

The study reports firm/year fixed effects and firm-clustered standard errors throughout. Conditional PPML accommodates zero counts and high-dimensional fixed effects, but its realized contribution set excludes 945 all-zero firms (3,782 observations) and a further 18 ever-positive observations removed in preprocessing/separation. The PPML coefficient is therefore an estimator-retained conditional association, not a population or treatment-effect estimate, and must not be compared mechanically with the 6,443-observation log-outcome model. R3 adds an aggregate Pearson-residual screen, an all-observation |Pearson residual| > 3 deletion, and rank-defined anonymous firm-deletion sensitivities; these are descriptive diagnostics, not confirmation of a Poisson variance model or a means to choose a favorable specification. Count-OLS is retained only as a descriptive sensitivity and its residual diagnostics are public. Zero-inflated or hurdle models are technically feasible but require different zero-process/distributional assumptions; this repository reports only an exploratory two-part decomposition rather than a structural ZIP/hurdle claim. The availability calibration uses a deterministic-match availability logit and is neither a treatment propensity score nor a causal correction. The model comparison follows the PPML and heteroskedasticity guidance of Correia, Guimarães, and Zylkin [1] and Santos Silva and Tenreyro [2].

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
