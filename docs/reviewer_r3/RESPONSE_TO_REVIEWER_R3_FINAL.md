# Response to Reviewers — Round 3

**Manuscript:** *Digital Transformation and Collaborative Green Invention Output: A Transparent Analysis of a Matched Panel of Chinese Listed Firms*

We appreciate the reviewers’ close reading. The revision adopts the stricter report as the minimum threshold. We have not attempted to preserve a broad substantive claim by adding selective specifications. Instead, we have reconstructed the manuscript around a narrower, reproducibility-oriented question: what descriptive DT–collaborative-green-invention association can be reproduced from a deterministic match of two independently released public data collections?

The revised manuscript is explicit that it does **not** identify a causal effect, a treatment effect, a population-average association for all Chinese listed firms, or a patent-quality effect. All results cited below are regenerated from locked scripts and are accompanied by code, aggregate outputs, and input lineage information.

| Revision category | Principal change |
|---|---|
| Design scope | Reframed the study as a transparent observational matched-panel analysis; removed wording that could imply causal or population-generalizable inference. |
| PPML scope | Downgraded PPML from a preferred population count model to a conditional count-model sensitivity in the actual estimator-retained contribution set. |
| R&D/knowledge boundary | Audited available source fields; added strict-calendar-lag source-labelled proxy sensitivities while stating why these do not constitute verified R&D intensity or knowledge stock controls. |
| Multiplicity | Added a deduplicated global inventory of 33 distinct reported DT-association tests and report global Holm, Bonferroni, and BH-FDR transparency screens separately from the five-row Table 5 family. |
| Diagnostics | Added retained-sample Pearson residual, extreme-residual deletion, and anonymous high-contribution-firm deletion screens for conditional PPML. |
| Presentation | Rebuilt the paper as a problem-driven report with separate estimator-scale figures, concise analytical position, data lineage, and revised archival transparency language. |

## Response to the strict R3 report

### P0-1. Conditional PPML applies to only 42.2% of matched observations

**Comment.** The reviewer notes that conditional PPML may be uninformative for the full matched panel when most observations do not contribute to conditional firm-effect identification.

**Response.** We agree. The revised manuscript no longer calls conditional PPML the preferred count specification for the population represented by the 6,574 matched observations. Table 2 now reports that the estimator retains **2,774 observations from 505 firms (42.2% of observations; 34.4% of firms)**. The retention decomposition is now a central design result: 945 firms with all-zero collaborative green-invention counts account for 3,782 observations, and a further 18 ever-positive observations are removed in fixed-effect preprocessing/separation.

The abstract, Methods, Table 4 note, Results, Discussion, Figure 2, and Appendix B now describe M3 only as a **conditional count-model sensitivity within its estimator-retained contribution set**. The main descriptive result is the two-way fixed-effect log-outcome association, and its distinct 6,443-observation support is displayed beside the PPML support. We do not infer that the PPML coefficient applies to the all-zero firms, the full matched panel, or a treatment-defined group.

We also added an estimator-retained PPML diagnostic screen. Its Pearson X² is 4,390.8 with an explicitly approximate N-minus-slope-parameters ratio of 1.59; 65/2,774 observations have absolute Pearson residual above 3. Removing every one of these observations once gives β=0.0861, 95% CI −0.0011 to 0.1733, p=0.0529. Six one-at-a-time anonymous firm deletions selected solely by Pearson-X² contribution yield coefficients from 0.0782 to 0.1016; we show all six and do not select the one unadjusted p<0.05 result. These are sensitivity screens, not validation of a Poisson variance model.

### P0-2. R&D investment and prior knowledge stock are insufficiently addressed

**Comment.** The reviewer requests controls for R&D intensity and knowledge stock, because these may jointly relate to digital transformation and green innovation.

**Response.** We agree with the substantive concern, but do not claim that the available data can fully resolve it. We first audited the sources rather than constructing an undocumented variable. The D1 source contains no dedicated R&D-expenditure, technical-personnel, or patent-stock field. The D2 workbook does contain `R&D expenditure` and `Gross revenue` for every matched observation. However, the data article describes R&D expenditure conceptually as annual investment and R&D intensity as investment divided by sales, whereas the released R&D numerical field’s transformation and units are not documented in the workbook. Literal released-R&D/revenue ratios are implausibly small; exponentiating the released field produces a different, more plausible scale but remains only a scale diagnostic. We therefore do **not** call either ratio verified R&D intensity.

To make the remaining evidence more informative without overstating it, Table 6 adds strict-calendar-lag sensitivities with: (i) the released D2 R&D-expenditure field; (ii) D1 `lngpfm`, labelled `ln(1 + invention patent)`; and (iii) both fields. The latter is accurately termed preceding-period inventive-activity, not cumulative knowledge stock. The log-outcome coefficients are 0.0239 (p=0.1109), 0.0232 (p=0.1182), and 0.0236 (p=0.1125), respectively. The corresponding conditional-PPML estimates are 0.0742 (p=0.1978), 0.0704 (p=0.2180), and 0.0695 (p=0.2237). The restrictions to strict calendar lags yield 4,222 log-outcome and 1,891 retained PPML observations.

These analyses are now explicitly presented as **limited proxy sensitivities**. We state that neither source-labelled proxy eliminates time-varying R&D/knowledge confounding, that the bias direction cannot be identified from the current sources, and that contemporaneous R&D may itself mediate a digital-transformation pathway. The Discussion now identifies a harmonized licensed source with documented R&D intensity and patent-stock records as a requirement for a causal extension.

### P0-3. Local multiplicity adjustment is insufficiently transparent

**Comment.** The reviewer asks for a uniform account of all relevant hypothesis tests rather than a correction only within Table 5.

**Response.** We agree that the prior wording did not make the broader reporting boundary sufficiently transparent. We retain the Table 5 adjustment only as an internal five-model family, now titled **“Sensitivity functional-form and multiplicity adjustment.”** Its note states that the raw p-values are descriptive, the family is post hoc rather than preregistered, Holm and Bonferroni use m=5, and this is not a global correction.

Separately, we created a deduplicated global inventory of every distinct reported DT-association coefficient test retained in the R3 manuscript and appendices. It includes 33 tests: main estimates, nonduplicate functional-form variants, timing/period estimates, availability-calibration variants, two-part descriptive components, lagged proxy variants, the all-extreme-residual PPML sensitivity, and the six anonymous high-contribution-firm deletions. Exact duplicates are entered once (S1=M0, S3=M1, and the R3 reference rows repeat M1/M3). It excludes residual normality, heteroskedasticity, Pearson-dispersion, matching-key, sample-flow, and balance screens because they are not coefficient tests of the DT–outcome association.

The smallest raw p-value is 0.0112 for the explicitly downgraded count-OLS sensitivity. **No association test is below 0.05 under global Holm, Bonferroni, or BH-FDR adjustment.** The manuscript does not assert that 33 is the uniquely correct scientific family; it presents this post-review screen to prevent selective emphasis on isolated variants and keeps the heterogeneous estimands visibly separate.

### P1. PPML diagnostic reporting is incomplete

**Response.** Addressed in Methods §3.3, Results §4.4, Table 7, Figure C1, and Appendix C. The residual definition, scope of the approximate degrees-of-freedom denominator, number above the |Pearson|>3 threshold, all-extreme deletion, and all six rank-defined firm deletions are reported. Firm identifiers and record-level residuals are not released.

### P1. DT terminology should distinguish stored data from analyst transformations

**Response.** Addressed throughout. The manuscript now consistently uses **DT_raw_count** for the stored D2 integer annual-report digital-keyword frequency field and **DT_log = ln(1 + DT_raw_count)** for the analyst-applied regressor. The Code Availability section maps legacy code aliases `dt_raw` and `log_dt` to these paper terms. The data-lineage section notes that the stored raw field may reflect provider versioning or export choice, but does not claim this as an established fact. The source article’s described `ln(1+frequency)` construction is cited separately.

### P1. Literature review is too broad relative to the design

**Response.** Addressed in §§1–2. The review has been shortened to measurement and design comparability. It distinguishes published IV/PSM-DID claims from the current observational matched-source design and removes any suggestion that the paper contributes a competing causal estimator or a coefficient “SOTA” ranking.

### P1. Future-DT placebo should not be treated as a valid falsification test

**Response.** Addressed in Appendix D. The strict t+1 result is retained only for descriptive timing completeness. It is explicitly not described as an exclusion restriction, instrument, or valid falsification test. The table and figure show endpoint loss and estimator-specific support.

### P1. Figures mix noncomparable scales or repeat source-flow information

**Response.** Addressed. The workflow diagram was removed from the main paper. Figure 2 has two separate panels: log-outcome estimates on the left and conditional-PPML estimates on the right. Each row reports retained N and firm count; the caption states that the panels use different outcome scales and samples and must not be ranked by coefficient magnitude.

### P1. Archive discrepancy language must not attribute unverified causes

**Response.** Addressed in Appendix F, retitled **“Archived Record for Transparency.”** It states that the discrepancy was not reconstructed in R3. Data version, field mapping, complete-case rules, controls, winsorization, singleton/separation handling, and software/convergence are listed only as candidate diagnostic paths. The appendix separately states that repeated locked-pipeline tests pass and that archived values do not enter current inference.

## Response to the clarity-focused R3 report

### Table 5 title and multiplicity wording

**Response.** The title is now “Sensitivity functional-form and multiplicity adjustment.” The table note distinguishes raw p-values, the m=5 post hoc family correction, and the separate 33-test global transparency inventory. It explicitly says that neither adjustment is confirmatory/preregistered inference and that Table 5 is not used for model selection.

### Explanation of stored D2 raw values

**Response.** The revised data-lineage paragraph now makes three separate statements: the data article describes `ln(1 + frequency)`; the Version 1 workbook stores nonnegative integer values; and the reason for the released scale is not identified from available documentation. The phrase “may reflect provider versioning or export choice” is deliberately modal and not offered as fact.

### Appendix E archival wording

**Response.** The historical discrepancy section is now Appendix F, “Archived Record for Transparency.” The first paragraph states that archived values are not used for R3 inference and that the discrepancy was not reconstructed. Deterministic locked-pipeline repetition is described separately from the archived numerical comparison.

## Closing statement

The new manuscript is more limited than the prior version by design. It now shows that the available evidence is not robustly significant at the conventional 5% level in the stated log-outcome or conditional PPML samples, does not establish a causal or population claim, and remains constrained by source matching and unverified R&D/knowledge measurement. We believe this narrower, fully traceable account is the appropriate response to the reviewers’ methodological concerns.
