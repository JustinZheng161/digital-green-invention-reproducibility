# Digital Green Invention Reproducibility — Final Delivery Report

## 1. 审稿结论与任务定义

本项目研究的是**中国上市公司企业—年份观察性面板中的数字化转型与联合申请绿色发明产出关联**。分析窗口为 2014–2020 年；两个 DOI 数据源确定性匹配后得到 6,574 个 firm-year 观测、1,468 家企业。结果变量是联合申请绿色发明专利数及其 `ln(1+y)` 代理，不是授权率、引文影响、原创性、商业价值或完整的专利质量指数。

“模型性能”在本项目中不能被定义为单一 accuracy/F1/AUC，也不能把不同论文的回归系数直接排名。更严格的顶会审稿口径是比较：数据覆盖、结果测量、固定效应、估计器是否适配零值、识别强度、估计器保留样本和结果稳定性。该口径与研究报告规范对样本量、排除规则、数据处理、预设/事后分析和代码可用性的要求一致 [1] [2]。

## 2. 三个基准数据集

| 数据集 | 规模与年份 | 主要变量 | 引用/链接 | 可比边界 |
|---|---:|---|---|---|
| D1 map-green innovation | 11,051 firm-year；1,798 家企业；2014–2020 | 绿色发明、绿色实用新型、总绿色专利及 `lngpfm` 等字段 | Bai (2025), Mendeley Data, DOI [3] | 公开二次数据；联合申请绿色发明是合作产出代理，不等价于质量 |
| D2 Digital transformation and strategic risk taking | 17,089 firm-year；3,806 家企业；来源论文覆盖 2008–2021 | 年报数字关键词频率、R&D expenditure、revenue 等 | Meng et al. (2024), Data in Brief [4] | 当前 workbook 的数值变换/单位部分未完整标注；`DT_raw_count` 需视为 released field |
| 当前 D1×D2 matched panel | 6,574 firm-year；1,468 家企业；2014–2020 | `DT_log=ln(1+DT_raw_count)`、联合绿色发明计数、控制变量 | 本项目审计生成 | 59.5% 的 D1 观测进入匹配完整样本；PPML 最终只保留 2,774 观测、505 家企业 |

推荐的两个更权威数据集是 **EPO PATSTAT Global** 和 **OECD Environment-related technologies patents**。PATSTAT Global 官方说明覆盖超过 125 million patent applications，可用于申请、授权、专利族和引文重建，但需要许可、实体解析和中国申请人匹配 [5]。OECD ENV-TECH 提供可复核的环境技术分类和跨国技术指标，但主要是国家/技术领域粒度，不可直接替代当前 firm-year 微观面板 [6]。

## 3. Top-5 可比研究设计对照，而非虚假 SOTA 榜单

| 研究/年份 | 样本规模与年份 | 指标/模型 | 报告指标或结果 | 链接与可比结论 |
|---|---|---|---|---|
| Wang & Zhong (2024) | 中国 A 股，2009–2019；全文方法段报告约 24,905 个企业面板观测、筛选后约 24,791 个观测 | 年报 MD&A 数字关键词比例；绿色发明/实用新型申请；企业与年份 FE，另有 Lewbel IV、PSM-DID | 每一标准差 DT 与绿色创新数量/质量关联分别为 2.924%/2.124% | [7]；样本和识别强于本项目，但结果口径不同 |
| Fang & Li (2024) | 2,908 家中国上市企业，2011–2020 | 年报文本数字化指标；绿色专利申请与授权；多模型敏感性 | 报告数字化与申请/授权绿色专利的关联 | [8]；授权质量维度优于当前代理，但不可直接比系数 |
| Huang & Lau (2024) | 中国上市企业，2011–2020 | 数字化转型、绿色创新质量；机制与知识产权保护边界 | 报告正向绿色创新质量关联 | [9]；质量构造与样本筛选不同 |
| He & Su (2022) | 2,010 家中国上市企业，2012–2019 | 数字化、绿色创新、监管压力和国际机会调节 | 报告正向关联和调节作用 | [10]；可作主题基准，不能替代当前确定性匹配证据 |
| Dong et al. (2025; online 2024) | 中国上市企业，2007–2020 | 区分独立与合作绿色创新，讨论机制 | 报告数字化与不同绿色创新形式的关系 | [11]；直接支持把联合申请解释为合作形式而非天然质量指标 |

因此，当前项目的**定量差距**不是“比 Top-5 低多少百分点”，而是：匹配样本规模较小；结果仅为联合绿色发明代理；缺少授权/引文/原创性；识别强度低于 IV/PSM-DID/政策冲击设计；但在零值处理、企业/年份 FE、条件 PPML、估计器保留样本和多重检验透明度方面已补齐审稿关键缺口。

## 4. 当前基线与改进结果

| 规格 | 系数 | p 值 | 实际 N | 解释 |
|---|---:|---:|---:|---|
| Full-control TWFE OLS, `ln(1+DT)` | 0.019628 | 0.0536 | 6,443 | 严格企业内描述性关联 |
| Conditional firm/year FE PPML | 0.093325 | 0.0655 | 2,774 | 零值计数敏感性；估计器保留样本 |
| Core-control ablation TWFE OLS | 0.021635 | 0.0341 | 6,443 | 消融 A；非预设优选结果 |
| No-governance ablation TWFE OLS | 0.020037 | 0.0493 | 6,443 | 消融 A |
| No-financial-controls ablation PPML | 0.078754 | 0.1450 | 2,774 | 消融 B |
| 1%/99% winsorized DT, TWFE OLS | 0.019482 | 0.0563 | 6,443 | 尾部稳健性 |
| 1%/99% winsorized DT, PPML | 0.093206 | 0.0668 | 2,774 | 尾部稳健性 |

结论是**正向但规格敏感的描述性关联**，不是稳健因果效应，也不是预测 SOTA。核心控制块与去财务控制块下的 OLS p 值跨过 5% 边界，而完整 PPML 和截尾 PPML 仍不精确；这正是应在正文中如实报告的模型敏感性。

## 5. 三个性能瓶颈与两项代码优化

瓶颈一是绿色发明计数的零值约 80.2%，且条件 PPML 排除 945 家全零企业和 18 个分离/预处理观测。瓶颈二是 DT 右偏（均值 10.665、中位数 2、最大值 429），within-firm 方差只占总方差 13.6%。瓶颈三是规模、董事会、独立董事和员工规模变量存在高相关性，控制块改变会影响精度。

**优化一：条件 PPML + 高维固定效应。** 原有计数模型容易把不含企业 FE 的 Poisson/NB 与企业—年份 FE OLS 并列为同一证据。现在 `src/run_analysis.py` 和 `src/run_model_upgrades.py` 使用 `pyfixest.fepois(... | firm_id + year)`，固定企业/年份 FE、企业 CRV1 聚类，并报告 separation、全零企业边界和估计器 N。该补丁由 Correia, Guimarães, and Zylkin 的高维 FE PPML 原则支撑 [12]；PPML 与 log-OLS 不应视为相同 estimand 的依据是 Santos Silva and Tenreyro [13]。

**优化二：预设控制块 + 尾部稳健性。** 新增 `src/run_model_upgrades.py`，统一生成核心控制块、去治理控制块、去财务控制块、完整控制块和 1%/99% 截尾 `log1p` 结果；不按 p 值选择最终模型。该设计借鉴高维控制选择后推断需透明披露选择规则的原则 [14]，但不声称完成 double-selection causal inference。修改前后差异和结果位于 `docs/MODEL_UPGRADE_REPORT.md`。

## 6. 实验设计与预期图表结构

消融 A 固定 DT 变换、企业/年份 FE、企业聚类和样本，比较核心、去治理和完整控制块。消融 B 固定估计器，去除财务控制块并与完整控制块比较。稳健性组在完整控制块下将 raw DT 截尾到样本 1%/99% 后重新估计 OLS 与 PPML。预期图表使用同一横轴展示系数和 95% CI；每行必须标明估计器、结果变量、控制块、FE、聚类规则、候选 N 和估计器保留 N。第二张图展示 raw 与 winsorized DT 的系数区间，不作大小排名。

与 SOTA/外部研究比较时必须固定的三个条件是：`DT_log=ln(1+DT)`（尾部稳健性才使用 1%/99% 截尾后 `log1p`）；`firm_id + year` 固定效应；企业层级 CRV1 聚类、95% CI、双侧检验。任何改变都必须作为独立规格列出。

## 7. 论文修订摘要与方法补充

**修订摘要：** Digital transformation is often linked to corporate green innovation, yet inferences can change when digitalization and patent outcomes are assembled from separately released sources. This study examines the descriptive association between a supplied annual-report digital-keyword measure and jointly applied green invention patents in a deterministic 2014–2020 match of two public Chinese listed-firm data collections. The match contains 6,574 firm-year observations from 1,468 firms. We label the stored integer keyword-frequency field `DT_raw_count` and analyse `DT_log = ln(1 + DT_raw_count)`. The locked two-way fixed-effects log-outcome model retains 6,443 observations and estimates β=0.0196 (firm-clustered SE=0.0102, 95% CI −0.0003 to 0.0395; p=0.0536). The conditional PPML count-model sensitivity estimates β=0.0933 (SE=0.0507, 95% CI −0.0060 to 0.1927; p=0.0655), based on 2,774 observations from 505 firms. Control-block ablations and 1%/99% exposure winsorization preserve the positive sign but change precision. A transparent inventory of 33 distinct reported association tests yields no result below 0.05 after global Holm, Bonferroni, or BH-FDR adjustment. The analysis therefore documents a reproducible matched-data workflow and bounded association evidence; it does not estimate a causal effect, a population-average effect, or patent quality.

**方法新增段落：** The count outcome was re-estimated with conditional PPML absorbing firm and year fixed effects, which is appropriate for a non-negative, zero-heavy outcome and requires explicit reporting of separation and the estimator-retained contribution set [12,13]. The control set and exposure transformation were locked before comparison: two control-block ablations were evaluated without selecting a specification by its p-value, and a 1%/99% winsorization was used only as a declared tail-robustness check. These procedures improve transparency but do not create causal identification.

**消融分析段落：** The core-control ablation produced a TWFE OLS coefficient of 0.021635 (p=0.0341), the no-governance block produced 0.020037 (p=0.0493), and the full block produced 0.019628 (p=0.0536). The no-financial-controls ablation produced 0.020909 (p=0.0403) in TWFE OLS but 0.078754 (p=0.1450) in conditional PPML. After 1%/99% winsorization, the coefficients were 0.019482 (p=0.0563) for TWFE OLS and 0.093206 (p=0.0668) for conditional PPML. The direction is similar, but the significance boundary moves across control blocks; the results are therefore best described as specification-sensitive descriptive associations.

近两年综述可补充 Abilakimova et al. (2025) 关于欧洲制造业 SME 数字—绿色转型的系统综述 [15]、Song et al. (2025) 关于数字化转型与绿色创新的 PRISMA/文献计量综述 [16]、Żywiołek et al. (2025) 关于能源领域数字化与绿色创新的系统综述 [17]，以及 Zhu et al. (2025) 关于企业数字—绿色转型的综述性研究 [18]。该主题主要发表在管理、环境、创新和可持续发展期刊，而非计算机科学式“顶会”；不应把期刊综述伪称为顶会论文。

## 8. README、requirements、git 清单

README 模板已落地为当前公开仓 `README.md`，包含研究边界、数据 DOI、私有数据环境变量、运行顺序、聚合输出、隐私规则、结果解释和引用。依赖文件为 `requirements.txt`，锁定 numpy、pandas、scipy、statsmodels、pyfixest、matplotlib 和 python-docx；测试运行另需 `pytest`。

`.gitignore` 必须包含 `data/private/`、`data/raw/`、`data/derived/`、`paper/`、`submission/`、`.venv/`、`__pycache__/`、`.pytest_cache/`、`.env`、`*.xlsx`、`*.zip`、`*.dta`、`*.parquet` 和行级 CSV。公开仓保留代码、去敏聚合 CSV/PNG/Markdown、DOI、哈希和测试；私有仓保留原始压缩包、匹配面板、完整审计和升级版手稿。

完整命令序列：

```bash
gh repo clone JustinZheng161/digital-green-invention-reproducibility
cd digital-green-invention-reproducibility
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DGI_PRIVATE_DATA_ROOT=/absolute/path/to/digital-green-invention-data-private/data
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
git add .
git commit -m "Update reproducible model and experiment audit"
git push origin main
```

私有仓使用相同的 `git add/commit/push` 流程，但不得把 `data/raw`、`data/derived` 或 `paper` 复制到公开仓。

## 9. 交付前物理核查清单

| 检查项 | 状态/要求 |
|---|---|
| 目标提交 | 私有仓 `9f8cdd6` 已识别；当前升级后私有提交需另行记录 |
| 公开仓隐私扫描 | `tests/audit_public_release.py` 通过；无 raw archive、行级 ID、私有手稿或 token-like credential |
| 核心/R1/R2/R3/升级测试 | 逐个直接执行；不能仅依赖 pytest 无测试收集结果 |
| 数据来源标注 | D1/D2 DOI、版本、覆盖年份、变量和许可边界在 README、方法和数据声明中一致 |
| 数字一致性 | 6,574/1,468、6,443/1,337、2,774/505、零值 80.2%、within ratio 13.6% 与 CSV/手稿一致 |
| 模型一致性 | 主文不再把旧的 year-FE Poisson/NB 当作企业 FE PPML；旧值仅可留在明确标记的 archival comparison 表 |
| 论文渲染 | 升级 DOCX 可由 LibreOffice 渲染为 23 页 PDF；PDF 文本包含新增方法、消融和稳健性结果 |
| 文件哈希 | 升级 DOCX 与审计清单记录 SHA-256；提交后重新计算并记录 |
| 公开/私有边界 | 公开仓仅聚合数据；私有仓保存原始/派生行级数据和完整手稿 |
| 外部引用 | 所有外源事实均带 DOI/官方链接；不可核验的统一 SOTA 数值不得写入 |
| 结果措辞 | 不使用“首次、最优、最先进、革命性、因果证明”等无支撑措辞 |

## 10. 最终文件夹结构

```text
public: digital-green-invention-reproducibility/
├── data/                         # DOI instructions only; no raw/derived rows
├── docs/
│   ├── FINAL_DELIVERY_REPORT.md
│   ├── MODEL_UPGRADE_REPORT.md
│   ├── research_evidence_log.md
│   └── reviewer_r1/ reviewer_r3/
├── metadata/                     # public hashes and source notes
├── results/
│   ├── figures/
│   ├── tables/
│   │   ├── main_model_results.csv
│   │   ├── robustness_tests.csv
│   │   └── model_upgrade_sensitivities.csv
│   └── reviewer_r1/ reviewer_r2/ reviewer_r3/
├── src/
│   └── run_model_upgrades.py
├── tests/
│   └── test_model_upgrades.py
├── README.md
├── requirements.txt
└── .gitignore

private: digital-green-invention-data-private/
├── data/raw/                     # DOI source archives
├── data/derived/                 # matched firm-year panel
├── data/metadata/                # full audit and hashes
├── analysis/                     # private and public-release analysis scripts
├── docs/                         # full evidence, QC, responses, final report
├── paper/r3/
│   ├── Digital_Transformation_Green_Invention_R3_Revised.docx
│   └── Digital_Transformation_Green_Invention_R3_Model_Upgraded.docx
└── results/                      # row-level/private diagnostics plus aggregate mirrors
```

## References

[1] [Nature Portfolio reporting standards](https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards).

[2] [Science editorial and statistical reporting guidance](https://www.science.org/content/page/science-journals-editorial-policies).

[3] [Bai, B. (2025). map-green innovation, Mendeley Data, Version 1](https://doi.org/10.17632/wjw77byzc2.1).

[4] [Meng, M. et al. (2024). Digital transformation and strategic risk taking dataset for China’s public listed companies](https://doi.org/10.1016/j.dib.2024.110511).

[5] [EPO PATSTAT Global](https://www.epo.org/en/about-us/observatory-patents-and-technology/observatory-tools/patstat).

[6] [OECD patents on environment technologies](https://www.oecd.org/en/data/indicators/patents-on-environment-technologies.html).

[7] [Wang, X., & Zhong, X. (2024). Digital transformation and green innovation: firm-level evidence from China](https://doi.org/10.3389/fenvs.2024.1389255).

[8] [Fang, L., & Li, Z. (2024). Corporate digitalization and green innovation](https://doi.org/10.1002/bse.3677).

[9] [Huang, Y., & Lau, C.-W. (2024). Can digital transformation promote the green innovation quality of enterprises?](https://doi.org/10.1371/journal.pone.0296058).

[10] [He, J., & Su, H. (2022). Digital Transformation and Green Innovation of Chinese Firms](https://doi.org/10.3390/ijerph192013321).

[11] [Dong, X., Meng, S., Xu, L., & Xin, Y. (2025). Digital transformation and corporate green innovation forms](https://doi.org/10.1080/09640568.2024.2320830).

[12] [Correia, S., Guimarães, P., & Zylkin, T. (2020). Fast Poisson estimation with high-dimensional fixed effects](https://doi.org/10.1177/1536867X20909691).

[13] [Santos Silva, J. M. C., & Tenreyro, S. (2006). The log of gravity](https://doi.org/10.1162/rest.88.4.641).

[14] [Belloni, A., Chernozhukov, V., & Hansen, C. (2014). Inference on treatment effects after selection among high-dimensional controls](https://doi.org/10.1093/restud/rdt044).

[15] [Abilakimova, A., Bauters, M., & Ogunyemi, A. A. (2025). Systematic literature review of digital and green transformation of manufacturing SMEs in Europe](https://doi.org/10.1080/21693277.2024.2443166).

[16] [Song, C., Teh, S. Y., Alnoor, A., et al. (2025). Trends of the digital transformation and green innovation using PRISMA and bibliometric analysis review](https://doi.org/10.1007/s43621-025-01855-w).

[17] [Żywiołek, J. et al. (2025). From traditional to digital: The paradigm shift in the energy sector through green innovation](https://www.sciencedirect.com/science/article/pii/S2352484725003609).

[18] [Zhu, Y. et al. (2025). Research on the impact of digital and green transformation](https://www.mdpi.com/2079-8954/13/9/820).
