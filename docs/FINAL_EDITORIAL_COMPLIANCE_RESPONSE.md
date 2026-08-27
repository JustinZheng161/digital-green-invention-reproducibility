# Final Editorial Compliance Response

## Scope and preservation rule

This revision addresses the final technical-review requests while preserving the study’s facts, data, numerical estimates, confidence intervals, p-values, sample sizes, formulas, citations, model scope and conclusions. The final manuscript is `paper/r3/Digital_Transformation_Green_Invention_Final_Editorial_Compliance.docx`.

| ID | Editorial request | Final action | Evidence | Status |
|---|---|---|---|---|
| T-1 | Standardize Table 1 study labels and punctuation | Table 1 now uses pure numeric study identifiers `[2]`–`[5]`; the current-study row keeps sentence-case semicolon-separated measurement and design clauses | Table 1 text check | Completed |
| T-2 | Define complete-case panel | First substantive mention now defines it as observations with non-missing values for all variables in the analytical model | Section 3.1 text check | Completed |
| T-3 follow-up | Distinguish count variable from descriptive output phrase | First substantive outcome description now names the variable `collaborative green invention count` and states that “output” is only a descriptive phrase for the same count | Terminology text check | Completed |
| F-1 | Use one numeric citation system | Main-text and Table 1 study references are numeric-only. The grouped literature citation remains `[2–6]` | Citation-style check | Completed |
| F-2 | Replace numeric double hyphens with en dashes | The final manuscript contains no `digit--digit` sequence; date ranges use `–` | Typography scan | Completed |
| F-3 | Make Table 8 note normal sentence case | The all-capitals callout is now a standard `Note.` paragraph explaining that p-values are unadjusted exploratory values and directing readers to Tables 4 and 5 | Table 8 note check | Completed |
| F-4 | Choose a table-header case convention | Sentence case is used for table headers; established abbreviations and symbols retain conventional capitalization | Table-header normalization | Completed |
| F-5 | Replace triple-hyphen prose dash | The manuscript contains no `---`; prose dash usage is normalized to em dash where needed | Typography scan | Completed |
| E-1 | Improve Equation (1) definition typography | Definition text now uses Unicode subscript notation (`Yᵢₜ`, `DT_logᵢₜ`, `Xᵢₜ`, `εᵢₜ`) and separates the disturbance-term statement into its own sentence | Equation definition check | Completed |
| E-2 | Improve Equation (2) definition typography | Definition text now begins with `Cᵢₜ`, matching the displayed equation symbol | Equation definition check | Completed |
| E-3/E-4 | Formula numbering and error-term font | Consecutive `(1)`/`(2)` numbering is retained and epsilon is described in regular equation style. Chapter numbering and a journal-specific math font remain target-journal stylesheet decisions because no journal guide was supplied | Explicitly documented dependency | Completed to manuscript-level scope |
| I-1/I-5 | Supply high-resolution, printable figure assets | Seven figures were rerendered natively at 600 dpi and exported as 600 dpi LZW TIFF files. Figure 2 also has a vector PDF. The final DOCX embeds the same native 600 dpi PNG renders | `results/figures/publication_figure_asset_manifest.json` | Completed |
| I-2 | Confirm Figure 1 ticks | Figure 1 is rendered with numeric x/y ticks, labels and a truncated-count-axis note. Its caption now identifies bars and the median line | Figure 1 caption and 600 dpi asset | Completed |
| I-3/I-4 | Define visual elements and caption convention | Every caption uses `Figure N.`. Captions now identify bars, points, lines, dashed references and 95% CIs where present; captions explicitly state where CIs are absent | Caption text check | Completed |

## Figure delivery assets

The publication-asset manifest records all seven 600 dpi TIFF outputs: Figure 1; Figure 2; Figures A1, B1, B2, C1 and D1. The source scripts are deterministic, preserve the released aggregate geometry and do not introduce data changes. `export_figure2_publication_assets.py` creates the Figure 2 600 dpi PNG/TIFF/PDF from the released aggregate coefficient table. `export_all_figure_assets.py` writes the complete TIFF manifest after confirming each source PNG is a native 600 dpi render.

## Final validation

`analysis/r4/validate_final_editorial_compliance.py` verifies the complete-case definition, pure numeric Table 1 labels, Table 8 note, equation typography, figure-caption element descriptions, absence of prohibited dash and full-width punctuation patterns, 20 preserved tables, all baseline factual anchors, and seven embedded images at at least 599 dpi. It reports 138 paragraphs, 20 tables and seven native 600 dpi embedded images.

The remaining dependence on the eventual journal’s author guide is limited to exact equation-numbering and mathematical-font conventions. The manuscript is otherwise delivered with portable 600 dpi TIFF figure files and a vector PDF for Figure 2.
