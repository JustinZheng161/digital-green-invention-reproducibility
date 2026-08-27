# 第二轮审稿意见逐条回复

**稿件：** *Digital Transformation and Collaborative Green Invention Output: A Transparent Study of a Matched Panel of Chinese Listed Firms*

**返修版本：** R2

**总体回应：** 感谢审稿人对模型有效性、样本外推、数据构造与报告透明度的严格审查。两份第二轮报告的总体建议分别为“小修”和“大修”。为避免以文字润色替代模型问题的实质处理，本次返修以更严格报告中的四项P0和六项P1为最低验收标准。所有新增数字均由锁定脚本在同一受控数据目录上重新生成；未能由保存材料唯一验证的历史差异，均保留为未解的透明性记录而非推测性解释。

| 处理结果 | 数量 | 说明 |
|---|---:|---|
| 已接受并完成 | 9 | P0-1、P0-3、P0-4，P1-1、P1-2、P1-3、P1-5、P1-6及两项P2。 |
| 已接受但修改其建议中的不当表述 | 1 | P0-2：补充PPML贡献集审计，但不将连续DT暴露错误称为ATT。 |
| 透明保留为未解局限 | 1 | P1-4：归档系数差异无法被保存记录唯一归因。 |

## 对第一份第二轮报告的回应

### P1-1：IPW术语的因果混淆风险

**回应：接受并强化修订。** 原有“availability propensity/IPW”的表达仍可能被误读为治疗分配的倾向得分。本次稿件将分析改名为 **availability-calibration sensitivity**，并把它严格定义为“给定D1企业规模、ROA和年份后，D1记录出现在确定性D1–D2匹配中的概率”的logit描述。它不是政策/处理分配模型，不是因果IPW，不会补全未匹配记录的D2数字化值，也不能校正未观测选择。

新logit的McFadden伪R²为0.0668。稳定化权重的p1/p99截尾点为0.673/1.503，未截尾最大权重为6.890，截尾后的有效样本量为6,228。为暴露而非掩盖权重与回归控制的双重调整，附录A10同时给出不额外控制和控制规模/ROA两种加权及未加权规格。本文不以任何加权规格作为首选估计或因果证据。

**修改位置：** 主文§3.3、§4.4、Table 6；Appendix D、Tables A9–A10；`src/run_reviewer_r2_analysis.py`。

### P1-2：Bonferroni调整p值标记

**回应：接受并完成。** Table 5的列名现在明确为 **Bonferroni p**，表注明确写为“Bonferroni-adjusted p is p×5 and is compared with 0.05；等价的未调整阈值为0.0100”。该修订消除了“调整后p值”与“调整α阈值”之间的解释混淆。

**修改位置：** 主文Table 5标题、表注和§4.3；`src/run_specification_sensitivity.py`的输出说明。

### P1-3：参考文献[8]未在正文引用

**回应：接受并完成。** 正文§2.1现已明确引用Zhuo et al. [8]，将其界定为使用文本数字化指标研究中国上市公司的相关研究；引言亦在相关文献群中纳入[8]。自动核查已确认参考文献[1]–[17]均在文稿中至少出现一次。

**修改位置：** 主文§1、§2.1、References；`paper/R2_CONTENT_VALIDATION.md`。

### P2-1：第5.2节序列词“Third”不完整

**回应：接受并完成。** 已删除孤立的“Third”，改用自然段衔接，避免前两段未使用First/Second时出现不完整的序列标记。

**修改位置：** 主文§5.2。

### P2-2：附录A1中文字段的可读性

**回应：接受并完成。** Table A1保留中文源字段以维持数据谱系，但已将每一字段对应的英文分析变量和解释置于第一列与第三列；例如“当年联合申请的绿色发明数量”对应“Collaborative green invention count”。这提供了英文学术读者可读的变量含义，同时避免将供应商字段误翻译为未经证实的计量构造。

**修改位置：** Appendix A, Table A1。

## 对严格第二轮报告的回应

### P0-1：匹配样本的泛化边界

**回应：接受并完成。** 标题副标题改为“**A Transparent Study of a Matched Panel of Chinese Listed Firms**”。摘要开头报告6,574个匹配公司—年度观测与1,468家企业，摘要结尾明确说明：结果是描述性的，仅适用于该匹配面板，而不支持对全部中国上市公司的泛化。§1、§3.1、§4.1、§5.2和§6使用相同范围表述。

新增Table 2、Table A5及Appendix C显示样本流：绿色源数据11,051个观测、匹配完整案例6,574个观测（59.5%）。样本比较显示企业规模和ROA存在可观测差异；这些SMD仅描述选择，不是抽样代表性检验。

**修改位置：** Title page；Abstract；§1、§3.1、§4.1、§5.2、§6；Tables 2、A5–A7；Figure A3。

### P0-2：PPML有效样本缩减与估计对象

**回应：接受分析要求，但修正ATT用语。** 审稿意见建议称PPML为“ATT conditional on the firm ever producing…”。由于DT是连续暴露，且研究不具备处理分配或因果识别设计，本文不采用ATT术语。替代地，本文在§3.3中精确定义PPML为：**高维条件PPML在实际保留的贡献集内估计的条件关联**。

锁定运行表明：TWFE log-outcome模型保留6,443个观测、1,337家企业；条件PPML保留2,774个观测、505家企业，即分别占匹配完整案例面板的42.2%和34.4%。945家全零协作绿色发明企业（3,782个观测；64.4%企业、57.5%观测）无法识别条件企业固定效应；另有18个ever-positive观测经固定效应预处理/分离后未保留。PPML贡献集相对完整案例面板具有更高的企业规模（SMD=0.470）、杠杆（SMD=0.310）和发明计数（SMD=0.323）。

**修改位置：** Abstract；§3.3、§4.1、§4.2、§5.2；Table 2、Table 4注；Appendix C Tables A6–A7、Figure A3；`src/run_reviewer_r2_analysis.py`。

### P0-3：IPW构造、理论边界和重复调整

**回应：接受并完成。** 为降低语义与模型风险，本文不再称其为治疗IPW，且不再使用完整D1控制组建立权重。R2选择模型仅含最易解释的D1可得性协变量（企业规模、ROA）与年份虚拟变量。正文报告logit形式、McFadden伪R²、概率分布、稳定化权重、截尾点、未截尾极值、有效样本量和加权前后SMD。由于同一协变量既可进入权重又可进入结果模型的做法改变了目标估计且可能引起重复调整解释争议，本文以成对规格透明呈现（不控制选择协变量 / 控制选择协变量），不将其称为“overcontrol bias”的必然诊断，也不以某个方向的衰减选择模型。

正文只保留一段方向与局限说明；完整权重和模型表移入Appendix D。加权并控制规模/ROA的关联为β=0.017637、SE=0.010816、p=0.1030、95% CI [−0.0036, 0.0388]，而不加权的同控制规格为β=0.021690、p=0.0587。这些差异表示规格敏感性，不表示因果修正成功或失败。

**修改位置：** §3.3、§4.4、Table 6、Appendix D Tables A9–A10；`src/run_reviewer_r2_analysis.py`；References [16]–[17]。

### P0-4：严格滞后置信区间与样本构成

**回应：接受并完成。** Table 7现为所有时序/时期规格报告95%置信区间和`N / firms / years`。严格t−1 PPML为β=0.052899，95% CI [−0.0630, 0.1688]，p=0.3709，N=1,891、418家企业、6个结果年份；严格t+1 placebo为β=0.091010，95% CI [−0.0246, 0.2066]，p=0.1229，N=1,742、387家企业、6个结果年份。

Appendix C的Table A8和Figure A4展示逐年候选与实际保留观测。t−1在2014年为零，完全由严格前一期定义决定；t+1在2020年为零。每个时序候选面板在条件PPML预处理前有4,457个观测，后续减少既反映非平衡面板的连续年可用性，也反映条件PPML贡献集限制。本文不把非显著的未来暴露安慰剂解释为不存在反向因果或遗漏趋势。

**修改位置：** §4.5、Table 7、Appendix C Tables A6–A8与Figures A3–A4；`src/run_reviewer_r2_analysis.py`。

### P1-1：DT构造公式溯源

**回应：接受并完成。** §3.1和Table A1新增来源构造说明。Meng et al. [15]说明其年报文本通过NLTK/JIEBA处理，以大数据、区块链、人工智能和云计算等类别的关键词字典匹配并计算词频，最终定义为ln(1+词频)。此外，本次对实际V1工作簿的字段审计发现名为“Digital Transformation”的存储列具有17,089个非缺失、全为非负整数、median=1、max=470的raw-count-like尺度。因此本文将存储列命名为Raw DT，再对该字段应用ln(1+raw DT)。本研究不独立验证爬虫、词典或上游文本算法。

**修改位置：** Abstract、§3.1–§3.2、Table 3、Appendix A Table A1；`r2_freeze/D2_MEASURE_AUDIT.json`。

### P1-2：core controls的预先声明状态

**回应：接受并采取更保守处理。** 保存的脚本定义了full和core控制集，但当前归档中没有可核验的、早于结果的预分析计划。因此不接受将core controls追溯声称为“a priori”或“pre-declared”的建议。Table 5和§4.3现在明确将S1–S5列为**post hoc exploratory family**；core controls的p=0.0454不作为确认性结果或模型选择理由。Holm、Bonferroni和BH-FDR校正均未保留显著性。

**修改位置：** §4.3、Table 5及表注；`src/run_specification_sensitivity.py`。

### P1-3：Figure 3跨尺度系数可比性

**回应：接受并完成。** Figure 3图注现在明确：log-outcome和count-PPML使用不同结果尺度，且PPML采用不同有效样本；系数绝对大小不可直接比较，图仅展示不确定性而不是效应量排名。为避免对不同估计量构造可能误导的“标准化效应”，本文保留原图并在图注、§4.2和Appendix C提供清晰的尺度与样本边界。

**修改位置：** Figure 3 caption；§4.2；Appendix C。

### P1-4：归档系数差异

**回应：部分接受，并保留未解状态。** 我们检查了存档结果、当前锁定脚本、数据哈希、完整案例过滤和可用运行记录。当前证据不足以唯一识别归档系数差异究竟由预处理、控制集、固定效应或软件版本造成。因此，我们未采用“主要因为未施加完整案例限制”的未经证实解释。Appendix E明确记录该差异为**unresolved archival discrepancy**；所有主文结果均由当前锁定脚本重建并取代旧数值作为本次返修的唯一推断版本。

**修改位置：** Appendix E、Table A11；`src/audit_reported_results.py`；冻结清单`r2_freeze/R2_FREEZE_MANIFEST.md`。

### P1-5：ZIP/hurdle与两部描述性分解的关系

**回应：接受并完成。** §2.3已承认ZIP/hurdle在技术上可以估计，但它们需要不同的零过程与分布性假设。当前研究不具备验证结构零/抽样零或为无高维固定效应的ZIP/hurdle建立与主模型可比解释的条件；因此不会将一个不含相同企业/年份固定效应的替代模型错误包装为主要证据。两部LPM/条件对数模型已明确为**exploratory descriptive decomposition**，不是预注册结果、结构hurdle或ZIP模型。

**修改位置：** §2.3、§4.4、Table 6及表注；References [12]–[13]。

### P1-6：不显著与零效应的区分

**回应：接受并完成。** 摘要、§4.2、§5.1和§6现在明确区分“未在常规阈值拒绝零假设”与“证明零效应”。例如log-outcome的95% CI为[−0.0003, 0.0395]，包含零及适度正向关联。文稿因此使用“statistical imprecision / absence of robust conventional statistical evidence”描述，而不把结果表述为确定性零效应。

**修改位置：** Abstract；§4.2、§5.1、§6。

### P2-1：专利质量表述重复

**回应：接受并精简。** 本文统一以“collaborative green invention output”描述当前结局。仅在变量定义和局限性中一次性说明它不提供授权、引用、权利要求、家族或商业价值信息，避免反复否定“patent quality”。

**修改位置：** Abstract、§2.2、Table 3注、§5.2、§6。

### P2-2：术语一致性

**回应：接受并完成。** 摘要首次出现时定义“count of jointly applied green invention patents, hereafter termed collaborative green invention output”。标题、摘要、变量表、结果和结论随后统一使用该概念；当需要说明原始字段时才使用“jointly applied green invention patents”。

**修改位置：** Title page、Abstract、§2.2、§3.2、Tables 3–4、§6。

## 复现与材料定位

| 材料 | 路径或位置 | 内容 |
|---|---|---|
| R2模型审计 | `results/reviewer_r2/tables/reviewer_r2_model_audit.md` | 样本流、PPML贡献集、逐年时序支持、可得性权重与平衡。 |
| R2分析脚本 | `src/run_reviewer_r2_analysis.py` | 完整的非因果样本/模型审计与聚合输出。 |
| R2论文验证 | `paper/R2_CONTENT_VALIDATION.md` | 36项正文、表图、引用和产物一致性检查。 |
| R2版式核查 | `paper/MANUSCRIPT_QC_NOTES_R2.md` | 28页逐段视觉验收记录。 |
| 公开仓库 | https://github.com/JustinZheng161/digital-green-invention-reproducibility | 代码、测试、聚合结果、图表、来源元数据和回复信。 |
| 私有仓库 | https://github.com/JustinZheng161/digital-green-invention-data-private | 受控原始文件、匹配面板、完整稿件、日志与私有审计材料。 |

> **最终解释边界：** 该研究提供的是透明、可复跑的确定性数据匹配和估计器样本审计。它不识别数字化转型的因果效应，不提供全体中国上市公司的总体结论，也不把不显著估计解释为零效应。
