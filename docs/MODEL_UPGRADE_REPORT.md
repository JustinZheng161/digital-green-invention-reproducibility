# Model and Experiment Upgrade Report

##审稿结论

本项目是中国上市公司企业—年份观察性面板，不存在可将所有论文压缩为单一准确率的统一 SOTA leaderboard。外部研究的样本、专利口径、数字化指标、识别策略和估计样本不同；因此，本文把“性能差距”定义为**识别强度、测量完整性、样本覆盖与估计器适配度的差距**，不把外部回归系数直接当作可比模型分数。

## 三个已确认的性能/科学瓶颈

第一，绿色发明结果有约 80.2% 的零值，且条件 PPML 因企业固定效应识别规则只保留 2,774 个观测和 505 家企业。若只报告 log(1+y) OLS，会把计数分布和零值结构压缩到线性残差中；若只报告不含企业固定效应的 Poisson/NB，则会混入大量跨企业差异。当前代码已采用 `pyfixest.fepois` 的企业和年份固定效应条件 PPML，并同时披露估计器保留样本。

第二，DT 原始值高度右偏，均值 10.665、中位数 2、最大值 429；且 DT 的 within-firm 方差只占总方差的 13.6%。这意味着 TWFE 主要依赖较小的企业内部变化，极端企业值与有限的时间变化可能显著影响标准误和系数。新增 1%/99% 截尾后的 `ln(1+DT)` 敏感性，不改变结果的方向或总体不精确模式。

第三，控制变量存在治理与规模变量的高相关性。新增两组控制块消融将理论核心/去治理/完整控制块，以及去财务控制块/完整控制块并列估计，禁止按照 p 值挑选规格。该报告不把核心控制块下的较小 p 值包装成稳健胜出，而是把它标记为规格敏感性。

## 两组消融与一组稳健性测试

| 组别 | 设计 | 固定条件 | 目的 | 代码输出 |
|---|---|---|---|---|
| 消融 A | 核心控制块、去治理控制块、完整控制块 | 相同 firm/year FE、firm-clustered CRV1、同一 DT 变换 | 判断治理与冗余控制是否改变 DT 关联 | `results/tables/model_upgrade_sensitivities.csv` 中 `A_control_block` |
| 消融 B | 去财务控制块与完整控制块对照 | 相同样本、估计器和聚类规则 | 识别财务控制集合对结论的贡献 | 同一 CSV 中 `B_control_block` |
| 稳健性 | raw DT 在样本 1%/99% 分位点截尾后使用 `ln(1+DT)` | 相同 firm/year FE、估计器和完整控制块 | 检查右尾极端值是否驱动结论 | 同一 CSV 中 `B_exposure_winsorization` |

消融 A 的实际结果显示，完整控制块下 TWFE OLS 系数为 0.01963（p=0.0536），核心控制块为 0.02164（p=0.0341），去治理控制块为 0.02004（p=0.0493）；条件 PPML 三种控制块的 p 值分别为 0.0655、0.0650 和 0.0512。消融 B 的去财务控制块将 TWFE OLS 系数变为 0.02091（p=0.0403），条件 PPML 变为 0.07875（p=0.1450）。由于规格间显著性边界发生变化，结论应表述为**对控制块敏感的正向描述性关联**，不能表述为稳定的因果或 SOTA 优势。

稳健性组中，1%/99% 截尾 DT 的 TWFE OLS 系数为 0.01948（p=0.0563），条件 PPML 系数为 0.09321（p=0.0668），与完整规格方向一致但仍不精确。所有计量结果均为给定匹配样本和模型条件下的关联。

## 代码前后差异

修改前，公开仓没有独立的模型升级入口，控制变量集合、计数估计与右尾处理分散在不同脚本中，无法一次性并列产生同口径消融表。修改后新增 `src/run_model_upgrades.py`：统一读取私有派生面板；固定 `FULL_CONTROLS`、`CORE_CONTROLS`、`NO_GOVERNANCE_CONTROLS` 和 `NO_FINANCIAL_CONTROLS`；统一调用 `feols` 与企业/年份固定效应 `fepois`；统一报告候选样本、估计器样本、企业数、系数、聚类标准误和置信区间；并对 1%/99% 截尾暴露值生成独立列。该脚本只写出聚合 CSV/Markdown，不写出企业标识或行级数据。

## 两项方法优化及文献支撑

**优化方案 1：将条件 PPML 固定效应作为计数型结果的主敏感性。** 对非负、零值密集且可能异方差的绿色专利计数，使用企业与年份固定效应的 PPML，并显式记录分离、全零企业删除和估计器保留样本。该方案遵循高维固定效应 PPML 对非负因变量、零值和分离诊断的处理原则 [1]，同时避免把对数线性 OLS 与 PPML 当作相同 estimand [2]。替换/新增文件：`src/run_analysis.py` 的 M3 计数模型已保留；新增 `src/run_model_upgrades.py` 用于一致性实验。

**优化方案 2：将控制块与暴露值变换预先锁定并并列审计。** 不根据 p 值挑选控制变量；把理论核心块、去治理块、去财务块、完整块和 1%/99% 截尾暴露值作为事先声明的敏感性矩阵。这样把“模型性能”从单个显著性结果改为规格稳定性、估计样本透明度和边界诊断。该报告借鉴高维控制变量选择后推断应明确选择规则、避免选择后过度解释的原则 [3]；本实现是控制块敏感性，而非声称完成 double-selection causal inference。

## 对外部研究的定量差距定位

| 维度 | 本项目 | 可比外部研究 | 差距解释 |
|---|---|---|---|
| 样本覆盖 | 2014–2020，6,574 匹配 firm-year、1,468 家企业 | Wang & Zhong (2024) 2009–2019，约 24,905 个企业面板观测；Fang & Li (2024) 2,908 家企业、2011–2020 | 本项目覆盖较窄，且跨源匹配损失较多观测 |
| 结果测量 | 联合申请绿色发明数的 `ln(1+y)` 代理；计数零值约 80.2% | 外部研究常区分绿色发明/实用新型、申请/授权，部分使用质量指标 | 本项目无法声称专利质量 SOTA；最紧迫的是授权、引文和原创性字段缺失 |
| 识别 | TWFE 描述性关联；条件 PPML 有 2,774 个保留观测 | Wang & Zhong 报告 IV 与 PSM-DID；其他研究采用机制/异质性设计 | 识别强度明显低于带外生冲击或 IV/准实验的文献 |
| 估计适配 | 已补充企业/年份 FE 条件 PPML和右尾敏感性 | 外部估计器不统一 | 方法适配度改善，但不能转化为统一数值排名 |

## 固定的三个超参数/实验条件

| 条件 | 建议固定值 | 理由 |
|---|---:|---|
| DT 变换 | `log1p(DT)`；稳健性使用样本 1%/99% 截尾后 `log1p` | 处理右偏，同时不丢失零值；截尾仅作为预先声明的敏感性 |
| 固定效应 | `firm_id + year` | 保持企业内部比较并控制共同年度冲击 |
| 推断 | 企业层级 CRV1 聚类，95% CI，双侧检验 | 与主结果一致，避免在显著性后更换推断规则 |

## 参考文献

[1] [Correia, S., Guimarães, P., & Zylkin, T. (2020). Fast Poisson estimation with high-dimensional fixed effects. *The Stata Journal*, 20(1), 95–115.](https://doi.org/10.1177/1536867X20909691)

[2] [Santos Silva, J. M. C., & Tenreyro, S. (2006). The log of gravity. *The Review of Economics and Statistics*, 88(4), 641–658.](https://doi.org/10.1162/rest.88.4.641)

[3] [Belloni, A., Chernozhukov, V., & Hansen, C. (2014). Inference on treatment effects after selection among high-dimensional controls. *The Review of Economic Studies*, 81(2), 608–650.](https://doi.org/10.1093/restud/rdt044)

[4] [Wang, X., & Zhong, X. (2024). Digital transformation and green innovation: Firm-level evidence from China. *Frontiers in Environmental Science*, 12, 1389255.](https://doi.org/10.3389/fenvs.2024.1389255)

[5] [Fang, L., & Li, Z. (2024). Corporate digitalization and green innovation: Evidence from textual analysis of firm annual reports and corporate green patent data in China. *Business Strategy and the Environment*, 33(5), 3936–3964.](https://doi.org/10.1002/bse.3677)
