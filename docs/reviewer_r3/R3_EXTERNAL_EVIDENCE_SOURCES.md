# R3 External Evidence Sources

## Data lineage and R&D-field interpretation

| Source | Verified point used in R3 | URL |
|---|---|---|
| Meng et al., *Data in Brief* (2024), “Digital transformation and strategic risk taking dataset for China’s public-listed companies” | The D2 collection covers 17,089 firm-year observations from 2008–2021. The article describes digital transformation as annual-report keyword frequency transformed as `ln(frequency + 1)`. It describes R&D expenditure conceptually as annual R&D investment and R&D intensity as R&D investment divided by sales revenue, but the released workbook does not state the numerical transformation/unit for the `R&D expenditure` column. | https://doi.org/10.1016/j.dib.2024.110511 ; https://www.sciencedirect.com/science/article/pii/S2352340924004803 |
| Bai, Mendeley Data Version 1 (2025), “map-green innovation” | D1 source used to construct collaborative green-invention outcome and to audit `lngpfm`, whose Stata label is `ln(invention patent +1)`. | https://doi.org/10.17632/wjw77byzc2.1 |
| Meng, Mendeley Data Version 1 (2024), “Digital transformation and strategic risk taking dataset” | D2 DOI archive supplying the stored “Digital Transformation”, “R&D expenditure”, and “Gross revenue” fields. | https://doi.org/10.17632/s3cdwjthnv.1 |

## R&D and green-innovation methodological boundary

| Source | R3 use | URL |
|---|---|---|
| He & Su (2022), *International Journal of Environmental Research and Public Health* | Supports the substantive relevance of R&D intensity to research on digital transformation and green innovation among Chinese firms. | https://doi.org/10.3390/ijerph192013321 |
| Huang & Lau (2024), *PLOS ONE* | Supports the relevance of firm digital transformation, green innovation measurement, and R&D-related mechanisms/controls in a Chinese listed-firm setting; cited without treating its causal claims as transferable to the present cross-source match. | https://doi.org/10.1371/journal.pone.0296058 |

## Reporting-structure references used for R3 blueprint

| Source | R3 reporting implication | URL |
|---|---|---|
| Nature Portfolio reporting standards | Clearly separate study design, data handling, sample exclusions, statistics, and availability conditions. | https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards |
| Science editorial and statistical reporting guidance | State sample sizes, tests, intervals, exclusions, data processing, and distinctions between pre-specified and post hoc analysis. | https://www.science.org/content/page/science-journals-editorial-policies |
| *Scientific Data* editorial policies | Make data versioning, technical validation, data availability, and code availability specific and reproducible. | https://www.nature.com/sdata/editorial-policies |

The R3 manuscript’s use of these sources is limited to transparent reporting, source-field interpretation, and methodological boundary-setting. It does not imply endorsement by the cited journals or data providers.
