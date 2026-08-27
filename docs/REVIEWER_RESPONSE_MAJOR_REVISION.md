# Reviewer Decision: Major Revision — Response Matrix

## Decision summary

The review decision is **major revision**. There are two P0 items, four P1 items, and no fatal error. The revision is accepted as a structural and reporting correction, not as a request to manufacture stronger statistical evidence.

| ID | Reviewer concern | Required modification | Evidence / validation rule | Status |
|---|---|---|---|---|
| P0-1 | Model-upgrades section appears after References; numbering and citations are confusing | Move the section into the main text after Section 4.4 and before Discussion/Conclusion; keep References last; remove duplicate “Additional references” list; cite Belloni in the section and consolidate references | Section order must be Introduction → Methods → Results → Discussion → Conclusion → Declarations → References; no new numbered main section may follow References | Completed |
| P0-2 | Unadjusted p<0.05 ablations appear inconsistent with “no significant result” wording | Distinguish unadjusted exploratory p-values from adjusted global inference in Abstract, Section 4.3, new sensitivity section and Conclusion | Required wording: no result remains below 0.05 after global adjustment; individual exploratory specifications may cross 0.05 unadjusted; none is confirmatory | Completed |
| P1-1 | Control-block definitions lack a declared basis | Explain financial, governance, and core size/ROA groupings as literature-informed descriptive blocks; acknowledge no preregistration and no p-value selection | New section must state that block definitions are descriptive ablations, not a search for significance | Completed |
| P1-2 | Table 8 repeats the full-control PPML estimate from Table 4/M3 | Add table footnote identifying the duplicate reference row and explaining why it is repeated | Table 8 note explicitly says full-control PPML duplicates Table 4 M3 | Completed |
| P1-3 | Winsorized TWFE OLS row repeats Table 5 | Add table footnote identifying the duplicate and its comparison purpose | Table 8 note explicitly says the winsorized TWFE OLS row is the Table 5 row-4 estimate | Completed |
| P1-4 | Belloni et al. is listed but not cited in body text | Cite it when explaining that the ablations are not formal post-selection inference | Body text must contain Belloni citation and References must contain one consolidated entry | Completed |
| P2-1 | “Model upgrades” implies a value judgment | Rename section neutrally | Title becomes “Additional sensitivity experiments: control-block ablations and winsorization” | Completed |
| P2-2 | PPML N in Table 8 lacks estimator-retained clarification | Add footnote | Table note states PPML N is estimator-retained contribution set | Completed |

## Verification record

The structural and textual validation script `analysis/r3/validate_reviewer_revision.py` passed. It confirms that Section 4.5 appears before Discussion and References, the duplicate Additional references block is removed, Belloni et al. is cited in the body and consolidated in References, Table 8 contains the duplicate-row and estimator-retained-N notes, and the Abstract/Conclusion distinguish unadjusted exploratory p-values from globally adjusted inference. The revised manuscript is `paper/r3/Digital_Transformation_Green_Invention_R3_Reviewer_Revised.docx`.

## Non-negotiable consistency rules

The abstract and conclusion must not state that every unadjusted p-value exceeds 0.05. They must state that **no result remains below 0.05 after the declared global correction**, while individual exploratory unadjusted specifications can cross the conventional threshold. Archived pre-revision estimates may remain only in a table explicitly labeled archival comparison; they must not appear as current narrative estimates.

The main text must end before References. Any post-References material must be an Appendix or Supplementary Material with a separate label. The revised manuscript will therefore place the new sensitivity section before Discussion, retain Table 8 in the main-text sequence, move Belloni into the consolidated reference list, and remove the “Additional references” subsection.
