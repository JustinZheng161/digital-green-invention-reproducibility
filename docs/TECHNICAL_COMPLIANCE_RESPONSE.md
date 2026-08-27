# Technical Compliance Response

## Scope

This revision responds to the technical review of the manuscript `Digital Transformation and Collaborative Green Invention Output: A Transparent Analysis of a Matched Panel of Chinese Listed Firms`. No observation, estimate, p-value, confidence interval, sample size, formula meaning, citation, experiment, or conclusion was changed.

| ID | Technical request | Implemented change | Verification |
|---|---|---|---|
| T-1 | Define TWFE at first abstract use | Abstract now reads “two-way fixed-effects (TWFE) log-outcome model”; the main text retains its estimator definition | Text scan passed |
| T-2 | Define CNRDS | First use now reads “China Research Data Services Platform (CNRDS)” | Text scan passed |
| T-3 | Harmonize outcome terminology | Variable-definition language uses “collaborative green invention count”; “output” is retained only as a descriptive phrase and is explicitly mapped to the same count | Text scan passed |
| T-4 | Define ROA | Table 3 covariate mapping and descriptive-statistics row now use “Return on assets (ROA)” | Table scan passed |
| T-5 | Define extensive/intensive margins | Section 4.2 now defines extensive margin as the probability of a positive patent count and intensive margin as the count conditional on positivity | Text scan passed |
| F-1 | Remove author-name plus numeric-citation mixture | The main literature paragraph uses numeric-only `[2–6]`; source-provenance wording no longer repeats author names beside numeric citations | Mixed-style body scan passed |
| F-2 | Use English punctuation | Full-width Chinese punctuation was removed from the manuscript text | Scan passed |
| F-3 | Replace double hyphens in year ranges | All `--` occurrences were replaced by en dashes | Scan passed |
| F-4 | Use present tense for displayed data descriptions | Data-distribution wording uses present tense where it describes the displayed matched panel | Text scan passed |
| F-5 | Improve long-paragraph readability | The prior humanization pass varied sentence rhythm; the technical pass preserved the existing section organization and did not introduce mechanical section restructuring | Structure and anchor scans passed |
| E-1 | Define every Equation (1) symbol | Added a definition paragraph after the equation table: Y_it, DT_log_it, X_it, α_i, λ_t and ε_it; ε_it is described as the disturbance term in regular equation style | Text and table-order scan passed |
| E-2 | Define C_it in Equation (2) | Added a definition paragraph after Equation (2): C_it is the annual count of jointly applied green invention patents for firm i in year t | Text scan passed |
| E-3 | Formula numbering convention | Existing `(1)` and `(2)` numbering was retained because no target-journal rule was supplied; the formulas are internally consistent and cited by their displayed equation labels | Editorial dependency disclosed |
| I-1 | Image resolution/format | All 7 embedded PNG assets are approximately 300 dpi. Figure 1 and Figure 2 were visually inspected; no low-resolution replacement was required | `docs/figure_technical_manifest.json` |
| I-2 | Figure 1 axes/ticks | Figure 1 visibly contains numeric tick labels, axis labels, and the truncated-axis note for the patent-count panel | Visual inspection recorded in `analysis/r4/figure_technical_findings.md` |
| I-3 | Caption convention | Captions use the `Figure N.` convention | Caption scan passed |
| I-4 | Error bars/intervals | Figure 2 caption now states “Error bars indicate 95% confidence intervals.” Figure C1 identifies the dashed residual thresholds and the binned mean-squared Pearson-residual line; descriptive limitations remain explicit | Caption scan passed |
| I-5 | Figure text readability | Embedded assets are 2,070–3,033 px wide and approximately 300 dpi; axis labels and ticks were visually legible in inspected figures | Image manifest and visual inspection |

## Invariant audit

The technical-compliance version contains 138 paragraphs and 20 tables. It preserves all baseline factual anchors from the humanized version after intentionally normalizing numeric citations under F-1. A separate validator confirms that non-citation numeric values, estimator names, technical variables and key terms were not lost. The public-release privacy audit continues to pass; raw archives, row-level IDs, private manuscript files and token-like credentials are not present in the public repository.

## Files

The formatted manuscript is `paper/r3/Digital_Transformation_Green_Invention_Final_Technical_Compliance.docx`. The private repository also contains the image manifest, figure findings, revision script and validators. The public repository receives this response report and the image manifest summary, but not the private manuscript or row-level data.
