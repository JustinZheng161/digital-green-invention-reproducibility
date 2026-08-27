# 交付前物理核查清单

| 核查项 | 状态 | 物理证据 |
|---|---|---|
| Revised DOCX exists | PASS | Digital_Transformation_Green_Invention_Revised.docx: 369449 bytes |
| Public repository exists | PASS | /home/ubuntu/digital-green-invention-reproducibility |
| Private repository exists | PASS | /home/ubuntu/digital-green-invention-data-private |
| Manuscript contains “Abstract” | PASS | present in DOCX XML text |
| Manuscript contains “3. Data and Methods” | PASS | present in DOCX XML text |
| Manuscript contains “Table 1. Research-design comparison” | PASS | present in DOCX XML text |
| Manuscript contains “Figure 3.” | PASS | present in DOCX XML text |
| Manuscript contains “Declarations” | PASS | present in DOCX XML text |
| Manuscript contains “References” | PASS | present in DOCX XML text |
| Manuscript contains “Appendix A. Reported-Result Reproduction Audit” | PASS | present in DOCX XML text |
| References span [1]–[13] | PASS | numbered references inspected in DOCX XML text |
| Private raw archives match recorded SHA-256 | PASS | data/raw/map_green_innovation_v1.zip: OK<br>data/raw/digital_transformation_risktaking_v1.zip: OK |
| Public release privacy audit | PASS | PASS: public release audit found no raw archives, row-level IDs, private manuscript files, or token-like credentials. |
| Cross-repository reproducibility test | PASS | PASS: all reproducibility and integrity checks completed |
| No archives, microdata, or manuscript files in public tree | PASS | none found |
| Public repository clean | PASS | clean |
| Public repository synchronized with origin/main | PASS | 0	0 |
| Private repository clean | PASS | clean |
| Private repository synchronized with origin/main | PASS | 0	0 |
| Public artifact present: results/tables/main_model_results.csv | PASS | 1129 bytes |
| Public artifact present: results/tables/specification_sensitivity.csv | PASS | 1502 bytes |
| Public artifact present: results/tables/robustness_tests.csv | PASS | 789 bytes |
| Public artifact present: results/figures/coefficient_comparison.png | PASS | 156726 bytes |
| Public artifact present: results/figures/distribution_diagnostics.png | PASS | 113785 bytes |
| Public artifact present: results/figures/research_workflow.png | PASS | 127722 bytes |

## 数据来源标注核查

| 数据/方法事实 | 主稿标注位置 | 可复现记录 | 状态 |
|---|---|---|---|
| D1 map-green innovation, V1, DOI 10.17632/wjw77byzc2.1 | §3.1、Data Availability、References [12] | `data/DATA_ACCESS.md`、私有`data/metadata/green_dataset.json` | PASS |
| D2 Digital transformation and strategic risk taking dataset, V1, DOI 10.17632/s3cdwjthnv.1 | §3.1、Data Availability、References [13] | `data/DATA_ACCESS.md`、私有`data/metadata/dt_dataset.json` | PASS |
| PPML高维固定效应方法 | §2.3、§3.3、References [6] | `docs/model_and_methods_upgrade.md` | PASS |
| 线性对数与PPML异方差敏感性 | §2.3、§3.3、References [7] | `docs/model_and_methods_upgrade.md` | PASS |
| 近期可比研究及设计边界 | Table 1、§2、References [1]–[5] | `docs/research_evidence_log.md` | PASS |

## 结果解释核查

主稿将联合申请绿色发明定义为“协作绿色发明产出代理”，而非完整专利质量；报告OLS与PPML的不同有效样本；将严格滞后、未来暴露和分期结果定位为诊断；未作因果主张。以上表述与结果表和源数据元数据一致。

## 必须由作者最终确认的专属事项

1. 作者姓名、机构、通讯作者、CRediT贡献与资金信息。
2. 目标期刊的具体格式、字数、数据共享、AI使用与伦理披露要求。
3. D1在研究声称的完成日期是否已可获得：其V1页面标注发布日期为2025-09-11。
4. 上游CNRDS、CSMAR、Wind和年报材料对再分发/衍生数据保存的许可边界。

**总计：25项通过，0项失败。**
