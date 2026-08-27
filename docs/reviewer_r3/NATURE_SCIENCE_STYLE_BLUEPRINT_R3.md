# R3高影响力期刊写作与报告准则

本文件不复制Nature或Science论文内容，而是将其公开作者规范转化为适用于本稿的**可执行结构、语言与方法透明度标准**。本稿不具备Nature/Science主刊所要求的突破性因果发现，因此这些准则用于提高可读性、可核查性与投稿材料质量，而不是暗示期刊层级或发表资格。

## 1. 官方规范提炼

| 来源 | 可执行原则 | 在本稿中的落地方式 |
|---|---|---|
| Nature Portfolio reporting standards | 主张必须可以被他人复核；数据、材料、代码限制应在稿件中透明披露；第三方处理步骤与共享限制需说明。 | 每一主张仅依赖已发布的聚合表或受控数据可重跑脚本；在Data/Code Availability中说明D1/D2 DOI、私有微观数据限制、哈希、访问条件和代码仓。 |
| Science research-article guidance | 摘要回答“为什么、做了什么、发现什么、意味着什么”；每个统计结果注明N、检验和不确定性；方法说明转换、缺失、排除与多重检验。 | 摘要先交代问题与匹配范围，再报告两个估计器样本和CI，最后限定解释；正文将设计、样本流、转换、PPML保留、缺失/排除与校正规则前置。 |
| Science design/statistics guidance | 事前假设与事后探索必须区分；多终点/多检验校正规则必须披露；结果需呈现点估计与CI，而非只报告显著性。 | 取消无证据的“pre-declared/core-control”暗示；将S1–S5标为sensitivity family；新增全局“报告的相关检验均为未校正，家族内校正仅作透明披露”的说明。 |
| Scientific Data author guide | 文章结构应让跨领域读者理解；方法精确给出输入数据版本与处理；数据/代码可用性应说明可获得内容、位置和限制。 | 压缩因果设计文献综述，突出数据谱系、构念和技术验证；以“Data lineage and scope”“Estimator-specific samples”“Technical checks”组织方法与结果。 |

## 2. R3论文叙事结构

> **研究叙事的核心变化：** 从“检验数字化是否促进绿色创新”的问题驱动叙事，改为“审计两个公开企业数据集确定性匹配后，数字化文本频数与协作绿色发明计数的关联在何种样本、计数模型与报告边界下可以被透明地描述”的证据驱动叙事。

| 章节 | 高影响力期刊式功能 | R3执行规则 |
|---|---|---|
| 标题与摘要 | 用客观、可检索词说明对象、设计与核心结果，不用宣传语。 | 标题保留matched panel；摘要首段明确D1–D2匹配、计数结果与最终解读；避免“proved/robust driver/quality”。 |
| 引言 | 用少量段落提出重要性、已知证据与当前可回答问题。 | 因果IV/PSM-DID文献压缩成一个对照段；研究空缺明确为数据谱系、计数零值与估计器样本，而不是争夺正向效应。 |
| Study design / data lineage | 前置可审计的研究单位、来源、时间窗、纳入与排除。 | 明确D1、D2版本、键连接、6,574观测、59.5%源样本、`DT_raw_count→DT_log`转换与来源算法未重建。 |
| Methods | 仅说明设计、估计器、假设和输出，避免在方法中解释结果。 | 单独列出：研究目标与非因果定位、变量与转换、主/补充估计器、PPML保留规则、全局与家族检验、R&D代理敏感性、软件版本。 |
| Results | 每段只回答一个可验证问题；首句为结果，随后给N、点估计、CI、限制。 | 先样本流，再主关联，再R&D代理、PPML诊断、校正与时间支持；t+1仅在附录，标为描述性完整性而非识别检验。 |
| Discussion | 解释最小充分结论；限制为“结果如何改变解读”，不逐句重复否定。 | 用一个限制段统一概括非因果、R&D/知识存量未观察、数据匹配选择和PPML贡献集；未来研究转向统一面板和外生冲击。 |
| Technical validation / appendices | 将验证与细节放在可查阅层，主文保留做结论必要的信息。 | 附录放置PPML诊断、D1字段审计、全局p值清单、历史归档差异、完整样本画像和逐年支持。 |

## 3. R3语言规则

| 需要避免 | 采用的替代表述 |
|---|---|
| “digital transformation increases/promotes …” | “the matched-panel estimate is consistent/inconsistent with a positive association, with the stated CI and sample boundary”。 |
| “preferred count specification” | “conditional PPML is the primary count-model sensitivity, reported with its estimator-specific contribution set”。 |
| “IPW correction/propensity score” | “availability-calibration sensitivity for observed D1 covariate imbalance；非治疗分配、非因果校正”。 |
| “unresolved discrepancy” | “archived discrepancy not reconstructed in this revision；当前锁定管道的可重复性经独立运行测试”。 |
| “no effect/no relationship” | “the estimate does not reject the null at α=0.05；CI includes zero and specified positive values”。 |

## 4. R3统计报告最低标准

每个主文或附录模型均须明确：研究单位、样本N/企业数/年份数、变量变换、固定效应、聚类层级、点估计、95% CI、双侧p值、纳入与排除规则。全局报告清单中的p值默认为未调整；仅对预定义的解释性“展示簇”提供校正结果并在表注明其不等同于全局确认性校正。

## Sources

[1] [Nature Portfolio. Reporting standards and availability of data, materials, code and protocols.](https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards)  
[2] [Science Journals. Instructions for authors of new research articles.](https://www.science.org/content/page/instructions-authors-new-research-articles)  
[3] [Science Journals. Editorial policies.](https://www.science.org/content/page/science-journals-editorial-policies)  
[4] [Scientific Data. Submission guidelines.](https://www.nature.com/sdata/submission-guidelines)
