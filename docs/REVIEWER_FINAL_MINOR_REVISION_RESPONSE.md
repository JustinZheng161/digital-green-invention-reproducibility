# Final Minor-Revision Response Matrix

## Decision context

The final-round reviews recommend **acceptance after minor revision**. The remaining requests were editorial or clarification requests; no new model claim or causal interpretation is introduced.

| ID | Reviewer request | Final change | Verification | Status |
|---|---|---|---|---|
| P1-1 | Do not let “20.34%” read as an estimate of R&D omitted-variable bias | Rephrased the Discussion to report the absolute increase 0.003992 and parenthetically identify 20.34% as a share of the reference coefficient. The sentence now states explicitly that it is a model-sensitivity magnitude induced by an unverified proxy field, **not an estimate of the true omitted-variable bias** | Final manuscript text scan and PDF render | Completed |
| P1-2 | Explain the relationship between Appendix A3 two-part components and Table 4 M3 conditional PPML | Added an Appendix A3 explanation: PPML jointly uses extensive- and intensive-margin information in a Poisson pseudo-likelihood count model; the two-part decomposition separates margins with linear models; PPML is not a weighted average and its scale differs | Final manuscript Appendix A3; existing `two_part_descriptive_decomposition.csv` | Completed |
| P1-3 / P2-1 | Make archived pre-revision values clearly superseded | Renamed Appendix F to “Archived record for transparency — pre-revision values are superseded” and added a strong statement that archived values are not current inference and must not be used for replication/comparison. The unresolved historical cause is retained transparently; current locked-pipeline determinism and test passage are stated without inventing a cause | Final manuscript Appendix F; SHA-256 and locked test output | Completed with limitation disclosed |
| P2-2 | Explain the choice of TWFE linear probability model for the extensive margin | Appendix A3 now states that the two-part analysis is descriptive, uses firm/year fixed effects and clustered SEs, and is not a structural hurdle/ZIP model; the linear-probability component is retained as a stable high-dimensional-FE sensitivity rather than a causal marginal-effect model | Final manuscript Appendix A3 and table note | Completed |
| P2-3 | Remove repeated control-block paragraph in Section 4.5 | Removed the duplicate paragraph beginning “The control-block definitions follow groupings commonly used…” while retaining the complete cited definition in the Section 4.5 opening | Final manuscript paragraph scan: zero duplicate occurrences | Completed |

## Final evidence

The existing two-part decomposition is unchanged numerically: extensive margin β=0.004659 (SE=0.007521, p=0.5358, N=6,443) and intensive margin β=0.065300 (SE=0.050626, p=0.1980, N=1,093). These values are descriptive sensitivities and are not combined arithmetically with conditional PPML β=0.093325.

The final private manuscript is `paper/r3/Digital_Transformation_Green_Invention_Final_Minor_Revision.docx`. The validator `analysis/r4/validate_final_minor_revision.py` checks the revised Appendix F title and statement, the non-calibrated wording, the A3/PPML explanation, the unique major paragraphs, Table 8 removal of repeated winsorization rows, and main-text order.

Raw and row-level data remain in the private repository only. The public repository contains the code, aggregate results, response matrix, hashes and reproducibility instructions.
