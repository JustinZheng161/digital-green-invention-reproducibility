# Final Non-Formula Compliance Response

## Constraint honored

At the author’s instruction, this pass **does not modify any formula, formula table, equation definition paragraph, equation numbering, or mathematical-font treatment**. The validation script confirms that Equation (1), Equation (2), and both definition paragraphs are text-identical to the preceding editorial-compliance manuscript.

| ID | Non-formula review item | Final action | Evidence | Status |
|---|---|---|---|---|
| F-1 | Year ranges and numeric double hyphens | Confirmed that the final manuscript contains no `digit--digit` pattern. All numerical ranges use en dashes | Whole-document typography scan | Completed |
| F-2 | Table 1 semicolon inconsistency | Normalized descriptive Table 1 cells from semicolons to commas. Numeric study labels `[2]`–`[5]` are retained | Table 1 cell scan | Completed |
| F-3 | Triple-hyphen prose dash | Confirmed no `---` remains in manuscript text | Whole-document typography scan | Completed |
| F-4 | Reference-list journal-name convention | The list consistently uses official journal titles in full (for example, *Research Policy*, *International Journal of Environmental Research and Public Health*, *The Stata Journal*, *Journal of Environmental Planning and Management*, and *PLOS ONE*). Conversion to ISO 4 abbreviations is intentionally deferred until the target journal supplies its bibliography stylesheet | Reference-list audit | Completed to journal-neutral manuscript scope |
| I-1 | Printable image format/resolution | Seven figures are supplied as native 600 dpi PNG renders embedded in the DOCX plus separate 600 dpi LZW TIFF delivery assets. Figure 2 also has a vector PDF. The asset manifest is public | `results/figures/publication_figure_asset_manifest.json` | Completed |
| I-2 | Figure B1 visual-element explanation | Caption now states that each horizontal segment connects the corresponding point to the zero line and that values right of 0.10 exceed the descriptive benchmark | Figure B1 caption scan | Completed |
| I-2 | Figure B2 visual-element explanation | Caption now states that each bar extends from zero to the named sample’s retained-observation share and that printed values give the same percentage | Figure B2 caption scan | Completed |
| I-2 | Figure C1/D1 visual-element explanation | Existing captions identify the residual histogram, threshold lines, binned points/line and reference line in C1, plus yearly points/connecting lines and legend in D1 | Caption scan | Completed |
| I-4 | Figure/Fig. convention | `Figure` is used consistently in text and captions. Any journal-mandated `Fig.` abbreviation is a target-style-sheet substitution, not a scientific or technical ambiguity | Caption convention scan | Completed to journal-neutral manuscript scope |

## Formula items reserved for author handling

The following items are deliberately untouched: equation subscript/mathematical-mode styling (E-1/E-2), chapter-based versus continuous equation numbering (E-3), and journal-specific epsilon font style (E-4). No target-journal style guide has been provided, and the author has elected to resolve formula presentation directly.

## Final evidence

`analysis/r4/validate_nonformula_final_revision.py` verifies: no numeric double-hyphen; no triple hyphen; numeric Table 1 labels; Table 1 has no semicolon in descriptive cells; Figure B1/B2 captions fully define the requested visual elements; all captions use `Figure`; all baseline scientific anchors remain; 20 tables remain; and all seven DOCX-embedded raster assets are native 600 dpi. It also verifies that the formulas and their definition paragraphs did not change.

The formatted manuscript is `paper/r3/Digital_Transformation_Green_Invention_Final_NonFormula_Compliance.docx`. All public assets are code, aggregate outputs, 600 dpi TIFF/PDF delivery files and this response report; the manuscript and private data remain separate in the private repository.
