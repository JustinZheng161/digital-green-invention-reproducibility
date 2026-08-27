# 研究证据台账

本台账仅记录已经访问并核验的公开来源；其用途是支持后续论文修改、数据来源标注与复现性核查。由于该研究属于企业层面观察性实证研究，文献中的显著结果不能被作为本研究的可比“性能指标”或因果证据。

| 编号 | 已核验来源 | 研究设计与样本 | 与本稿的直接关联 | 可安全引用的结论 |
|---|---|---|---|---|
| E1 | He & Su (2022), *Digital Transformation and Green Innovation of Chinese Firms* | 中国上市公司，2012–2019，n=2,010；考察监管压力与国际机会的调节作用。 | 说明数字化转型—绿色创新关系受到研究设计和边界条件影响。 | 作者报告其样本中存在正向关联及调节效应；不应将其替代为本稿异质数据匹配设计的结论。 |
| E2 | Huang & Lau (2024), *Can digital transformation promote the green innovation quality of enterprises?* | 中国上市公司面板，2011–2020；论文报告数字化转型与绿色创新质量的正向关联，并考察高管数字经验及知识产权保护。 | 是本稿主题最直接的近期可比论文之一；其质量定义、样本筛选与识别策略必须逐项核对，不能只比系数。 | 该文报告正向结果；本稿在严格双向固定效应下的弱证据可被定位为口径与模型敏感性，而非对其结论的直接否定。 |
| E3 | Wang & Zhong (2024), *Digital transformation and green innovation: firm-level evidence from China* | 中国沪深A股，2009–2019；文本构建数字化指标，报告工具变量、PSM-DID、机制和异质性分析。 | 说明高质量投稿通常需包含明确的识别策略与机制或异质性证据。 | 作者报告每个数字化转型标准差与绿色创新数量、质量的正向关联；其因果识别主张取决于工具变量和准实验的有效性。 |
| E4 | Mendeley Data, *map-green innovation*, DOI 10.17632/wjw77byzc2.1 | 中国A股，2014–2020；1,798家企业、11,051个有效观测。数据说明称源自CNRDS（绿色创新）与CSMAR（基础与财务数据），并已对连续变量作1%/99%缩尾。 | 本稿的绿色创新数据来源；必须避免将该公开二次数据包描述为自行构建的原始专利数据库。 | 规模与清洗规则与论文表1一致；DOI页面显示发布时间为2025-09-11，故需核验“最终格式稿”在此日期前后是否可使用该版本。 |
| E5 | Meng et al. (2024) 数据论文 / Mendeley Data, *Digital transformation and strategic risk taking dataset*, DOI 10.17632/s3cdwjthnv.1 | 数据集覆盖2008–2021年、17,089个公司年度观测，数字化转型指标由年报文本挖掘生成。 | 本稿数字化转型变量来源；原稿写作“2010–2021”与检索到的数据论文摘要“2008–2021”存在时间范围不一致，须在复现时从实际文件重新统计。 | 可作为公开数据的引用来源；最终论文应以下载的数据字典和实际数据覆盖期为准。 |

## 原始链接

[1] [He, J., & Su, H. (2022). *Digital Transformation and Green Innovation of Chinese Firms*. *International Journal of Environmental Research and Public Health*, 19(20), 13321.](https://doi.org/10.3390/ijerph192013321)

[2] [Huang, Y., & Lau, C.-W. (2024). *Can digital transformation promote the green innovation quality of enterprises?* *PLOS ONE*, 19(3), e0296058.](https://doi.org/10.1371/journal.pone.0296058)

[3] [Wang, X., & Zhong, X. (2024). *Digital transformation and green innovation: firm-level evidence from China*. *Frontiers in Environmental Science*, 12, 1389255.](https://doi.org/10.3389/fenvs.2024.1389255)

[4] [Mendeley Data. *map-green innovation*. DOI: 10.17632/wjw77byzc2.1.](https://doi.org/10.17632/wjw77byzc2.1)

[5] [Meng, M., et al. (2024). *Digital transformation and strategic risk taking dataset for China’s public listed companies*. *Data in Brief*.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11168288/)

[6] [Mendeley Data. *Digital transformation and strategic risk taking dataset*. DOI: 10.17632/s3cdwjthnv.1.](https://doi.org/10.17632/s3cdwjthnv.1)

## 立即核验项目

1. **版本可得性**：`map-green innovation` DOI 页面记录的发布日期是 2025-09-11；应核验研究、数据下载和实际复现的时间戳，避免预先可得性问题。
2. **样本跨度一致性**：稿件正文中数字化数据集被写为2010–2021，但来源检索结果将其描述为2008–2021。最终版本只能保留由下载文件直接证明的区间。
3. **结局变量可比性**：`GreenQuality` 是“共同申请的绿色发明专利数”的对数代理，而主流质量论文可能使用授权、引文或知识宽度等指标；这些不构成同一指标。
4. **估计量可比性**：年固定效应 Poisson/NB 与企业—年份双固定效应 OLS 不识别相同变异来源，禁止把它们写成可互相替代的稳健性结果。

## 补充方法与文献证据

| 编号 | 已核验来源 | 可直接用于本研究的事实 | 在最终论文中的正确用途 |
|---|---|---|---|
| E6 | Correia, Guimarães, & Zylkin (2020) | 该方法论文说明PPML可处理非负因变量及零值，并可吸收多维高维固定效应；同时强调分离与极大似然存在性检查。 | 支撑将企业与年份固定效应PPML作为计数型结果的分布敏感性模型，并报告收敛/分离与有效估计样本。不能据此自动获得因果识别。 |
| E7 | Santos Silva & Tenreyro (2006) | 该文讨论异方差下对数线性OLS与PPML估计可能出现实质差异。 | 支撑并列报告对数因变量OLS和PPML，而非以较显著的一个模型取代另一模型。 |
| E8 | Fang & Li (2024), *Business Strategy and the Environment* | 使用中国上市公司2011–2020年、2,908家企业的年报文本与绿色专利数据，报告数字化与申请/授权绿色专利的关联，并使用不同指标、计量模型和样本检验。 | 支撑重建统一样本、年报文本指标和授权专利质量指标的优先级；本稿不应声称与其同一指标或同一识别质量。 |
| E9 | Dong et al. (2025; online 2024), *Journal of Environmental Planning and Management* | 使用中国上市公司2007–2020，区分独立与合作绿色创新，并以投资效率、研发投入、金融支持和市场监督讨论机制。 | 支撑将“联合申请”从质量代理中剥离，改为合作创新形式或单独的结果维度。 |
| E10 | Zhuo et al. (2024), *Frontiers in Environmental Science* | 使用中国A股2012–2022，分析绿色创新的数量和质量，并报告ESG机制与环境信息披露等边界条件。 | 表明该领域常见的机制与异质性路径；在缺少相应观测变量时，本稿不能新增未经估计的机制结论。 |
| E11 | Abilakimova, Bauters, & Ogunyemi (2025) | 对欧洲制造业中小企业数字—绿色转型开展系统综述，筛选42篇研究并强调资源、测量与实施障碍。 | 用于研究背景中说明“数字—绿色协同转型”是跨地域概念；不能把欧洲SME综述直接推广为中国A股因果证据。 |
| E12 | Song et al. (2025), *Discover Sustainability* | 使用PRISMA与文献计量方法审阅2019年至2025年6月的499篇文献；作者报告研究集中于中国，并提示治理透明度、跨学科整合与部门应用缺口。 | 用于近期综述章节，定位本研究在数据治理、指标透明性与可复现性方面的贡献边界。 |

### 补充引用链接

[7] [Correia, S., Guimarães, P., & Zylkin, T. (2020). *Fast Poisson estimation with high-dimensional fixed effects*. The Stata Journal, 20(1), 95–115.](https://doi.org/10.1177/1536867X20909691)

[8] [Santos Silva, J. M. C., & Tenreyro, S. (2006). *The Log of Gravity*. The Review of Economics and Statistics, 88(4), 641–658.](https://doi.org/10.1162/rest.88.4.641)

[9] [Fang, L., & Li, Z. (2024). *Corporate digitalization and green innovation: Evidence from textual analysis of firm annual reports and corporate green patent data in China*. Business Strategy and the Environment, 33(5), 3936–3964.](https://doi.org/10.1002/bse.3677)

[10] [Dong, X., Meng, S., Xu, L., & Xin, Y. (2025). *Digital transformation and corporate green innovation forms: evidence from China*. Journal of Environmental Planning and Management, 68(11), 2644–2672.](https://doi.org/10.1080/09640568.2024.2320830)

[11] [Zhuo, R., Zhang, Y., Zheng, J., & Xie, H. (2024). *Digitalization transformation and enterprise green innovation: empirical evidence from Chinese listed companies*. Frontiers in Environmental Science, 12, 1361576.](https://doi.org/10.3389/fenvs.2024.1361576)

[12] [Abilakimova, A., Bauters, M., & Ogunyemi, A. A. (2025). *Systematic literature review of digital and green transformation of manufacturing SMEs in Europe*. Production & Manufacturing Research, 13(1).](https://doi.org/10.1080/21693277.2024.2443166)

[13] [Song, C., Teh, S. Y., Alnoor, A., et al. (2025). *Trends of the digital transformation and green innovation using PRISMA and bibliometric analysis review*. Discover Sustainability, 6, 1010.](https://doi.org/10.1007/s43621-025-01855-w)

## 研究设计比较（替代“SOTA性能榜”）

在企业观察性面板研究中，不存在可按单一数值排名的通用SOTA。因变量定义、单位、样本覆盖、固定效应、工具变量和估计量不同，直接比较回归系数或p值不具备解释性。最终稿将用以下**设计对比表**替代“SOTA Top-5性能表”。

| 研究 | 样本 | 关键测量/模型 | 作者报告的发现 | 与本稿的可比边界 |
|---|---|---|---|---|
| He & Su (2022) | 中国上市公司，2012–2019，2,010家企业 | 数字化转型、绿色创新，加入监管压力和国际机会 | 报告正向关联和情境调节 | 与本稿公共数据拼接、联合绿色发明代理不同。 |
| Wang & Zhong (2024) | 中国A股，2009–2019 | 文本数字化指标、绿色创新数量/质量、IV和PSM-DID | 报告每一标准差DT与数量/质量的正向关联 | 含更强识别设计；本稿不将自己的系数与其百分比并列比较。 |
| Huang & Lau (2024) | 中国上市公司，2011–2020 | 数字化转型和绿色创新质量，含高管数字经历及IPP边界条件 | 报告正向关系 | “质量”代理和样本筛选必须在正文逐项区分。 |
| Fang & Li (2024) | 中国上市公司，2011–2020，2,908家企业 | 年报文本/熵权数字化指数，绿色专利申请与授权 | 报告数字化与绿色申请/授权专利的关联 | 该文使用统一年报和专利数据；本稿仅用匹配后的公开二次数据。 |
| Dong et al. (2025) | 中国上市公司，2007–2020 | 区分独立与合作绿色创新，考察机制和调节 | 报告数字化促进不同形式绿色创新 | 直接提示：联合申请是合作形式，不是天然的质量指标。 |

## 近期综述的合规写法

最终稿可以补充上述E11–E12及以下一篇领域内中文综述，但必须标明其为背景性综述而非计量证据：

[14] [Xie, K. (2024). *A review of green innovation research on digital transformation enabling enterprises*. E-Commerce Letters, 13(2), 798–805.](https://doi.org/10.12677/ecl.2024.132094)

当前能完整核验的近两年**同行评议综述**为E11、E12和E14三篇。对“近两年顶会综述”的原始要求，需要进行领域修正：该主题的主导发表载体是管理、环境、创新与经济学期刊，而不是计算机科学式顶会论文集；将期刊综述伪称为顶会综述是不准确的。

## 审稿意见R1：计数零值处理的补充方法证据

| 编号 | 已核验来源 | 与R1修改的直接关联 | 正确使用边界 |
|---|---|---|---|
| E15 | Feng (2021), *A comparison of zero-inflated and hurdle models for modeling zero-inflated count data*, Journal of Statistical Distributions and Applications, 8, 8. DOI:10.1186/s40488-021-00121-4 | 该综述指出ZIP与hurdle模型依赖不同的零生成过程，并建议根据数据与拟合评估选择模型。 | 支持不因“80%零值”就机械选择ZIP；当前数据没有可验证的结构零/抽样零划分，故报告PPML与两部描述性分解，而不虚构结构性ZIP主模型。 |
| E16 | Farewell, Long, Tom, Yiu, & Su (2017), *Two-Part and Related Regression Models for Longitudinal Data*, Annual Review of Statistics and Its Application, 4, 283–315. DOI:10.1146/annurev-statistics-060116-054131 | 该综述说明二部模型常由二元发生部分和条件于二元结果的正值部分组成，并讨论其在重复测量、零质量数据中的解释问题。 | 支持本稿把发生/强度模型作为描述性分解；不把它错误称为已完全指定、已验证的hurdle或ZIP模型。 |

[15] [Feng, C. X. (2021). *A comparison of zero-inflated and hurdle models for modeling zero-inflated count data*. Journal of Statistical Distributions and Applications, 8, 8.](https://doi.org/10.1186/s40488-021-00121-4)

[16] [Farewell, V. T., Long, D. L., Tom, B. D. M., Yiu, S., & Su, L. (2017). *Two-Part and Related Regression Models for Longitudinal Data*. Annual Review of Statistics and Its Application, 4, 283–315.](https://doi.org/10.1146/annurev-statistics-060116-054131)


## 2026-08-27：R2变量构造与可得性加权证据

| 主题 | 已核验来源 | 可用于返修的事实 | 返修用途 |
|---|---|---|---|
| D2数字化转型构造 | Meng, Fan, Li & Lei (2024), *Data in Brief*, 54, 110511, [DOI](https://doi.org/10.1016/j.dib.2024.110511)；[PMC全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC11168288/) | 数据论文明确说明：数字化转型以中国上市公司年报为文本来源，经内容分析、NLTK/JIEBA分词、数字关键词字典匹配和关键词频数统计构造；DT=`ln(数字化转型词频+1)`。来源涵盖沪深A股年报、CSMAR、Wind；2008–2021年17,089公司年度观测、12行业。 | 在数据与变量节/附录A1准确描述DT字段为来源作者构造的年报数字关键词频率对数指标，并说明本研究未独立重建或验证其上游爬取/词典流程。 |
| IPW术语边界 | Rosenbaum & Rubin (1983), *Biometrika*, 70(1), 41–55；Wooldridge (2002), *Portuguese Economic Journal*, 1(2), 117–139, [DOI](https://doi.org/10.1007/s10258-002-0008-x) | 经典propensity score通常定义为给定协变量的处理分配条件概率；IPW也可用于样本选择/流失/分层，但需要明确选择指标与可识别条件。 | 不将D1–D2确定性匹配的“可得性logit”称为治疗倾向得分或因果矫正；仅称为selection-on-observables/availability calibration，并报告选择模型、重叠、权重、ESS和未观测选择局限。 |
| 零值模型和二部描述 | Feng (2021), *Journal of Statistical Distributions and Applications*, 8, 8, [DOI](https://doi.org/10.1186/s40488-021-00121-4)；Farewell et al. (2017), *Annual Review of Statistics and Its Application*, 4, 283–315, [DOI](https://doi.org/10.1146/annurev-statistics-060116-054131) | ZIP/hurdle均可作为零值计数的技术模型，但分别蕴含不同数据生成和解释假设；二部纵向分析的发生与条件正值部分不等同于结构模型。 | 承认技术上可以拟合ZIP/hurdle，但基于固定效应可比性、强假设与透明性不将无HDFE的模型列为主推断；将现有二部结果明示为探索性描述分解。 |
