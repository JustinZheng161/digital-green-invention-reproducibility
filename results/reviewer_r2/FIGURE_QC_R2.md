# R2新增图表视觉核查

## Figure R2-1：Estimator-specific sample retention

已检查 `r2_estimator_sample_retention.png`。图形分辨率为2370×1350，横向条形图按匹配完整案例面板、TWFE log-outcome、conditional PPML、strict t−1 PPML和strict t+1 PPML显示保留比例。数值标签为100.0%、98.0%、42.2%、28.8%和26.5%，与锁定审计结果一致。标题、坐标轴和估计器名称清楚，没有截断或视觉重叠。该图可用于说明PPML和严格时序模型的估计对象显著小于线性面板，不能作为效应量比较。

## Figure R2-2：Calendar-year support for strict timing estimators

已检查 `r2_timing_year_support.png`。图形分辨率为2370×1410，分别显示strict t−1与strict t+1条件PPML在各结果年份的实际保留观测。t−1在2014年为0，t+1在2020年为0，图形明确呈现了严格日历滞后/领先的边界缺失；2015–2019年均有保留观测。标题、图例、年份刻度和纵轴文字均清楚。图注应明确这展示的是**条件PPML保留观测**而非全匹配面板的年份分布，且t−1的2014零值由定义所致。

**结论：两图均通过视觉验收，可纳入返修稿附录。**
