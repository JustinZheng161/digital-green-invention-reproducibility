# 数据来源与隔离管理清单

本研究使用的两个数据集均在 Mendeley Data 页面标注为 **CC BY 4.0**。二者是来自 CNRDS、CSMAR、Wind 和年报文本挖掘的二次发布数据；许可允许再利用并不自动证明底层数据库的再分发权限。为避免错误公开，数据文件、匹配产物和可能含受限字段的派生数据将仅同步至**私有**仓库；公开仓库只保留获取脚本、哈希、数据字典和不可逆汇总结果。

| 标识 | 数据集 | 已核验官方版本与发布日期 | 官方样本说明 | 下载地址 | GitHub 归属 |
|---|---|---:|---|---|---|
| D1 | `map-green innovation` | V1；2025-09-11 | 中国A股2014–2020；1,798家企业、11,051个有效公司年度观测。页面说明数据经行业、风险警示、破产、缺失值筛选，并对连续变量进行了1%/99%缩尾。 | `https://data.mendeley.com/public-api/zip/wjw77byzc2/download/1` | 私有数据仓库；公开仓库仅记录DOI、获取脚本与哈希。 |
| D2 | `Digital transformation and strategic risk taking dataset` | V1；2024-03-19 | 页面说明数据来自年报、CSMAR 与 Wind，含数字化转型与战略风险承担变量；检索到的数据论文摘要称覆盖2008–2021、17,089公司年度观测。 | `https://data.mendeley.com/public-api/zip/s3cdwjthnv/download/1` | 私有数据仓库；公开仓库仅记录DOI、获取脚本与哈希。 |

> 关键版本风险：D1的公开版本发布时间为2025-09-11。论文中若主张在该发布日期以前完成的实证分析，必须以可审计的原始下载时间、旧版本存档或作者保存的文件证明其可得性；否则该数据不能支撑早期完成时间的表述。

## 下载和再分发政策

1. 原始档案应仅在私有工作区从 DOI 官方端点下载，并同时记录下载时间、HTTP响应、文件大小和 SHA-256。
2. 原始文件存放在私有仓库的 `data/raw/`；公开仓库不包含该目录。
3. 清洗后的可复现工作数据存放在私有仓库的 `data/derived/`；默认私有同步，因为它仍可含受限的公司—年度记录。
4. 公开仓库只提交 `src/`、`tests/`、`docs/`、`data/DATA_ACCESS.md`、根目录 `metadata/` 下的哈希，以及由数据聚合生成且无微观记录的 `results/tables/` 与 `results/figures/`。
5. 任何原始或派生数据在推送前必须通过敏感文件检查、大小检查和哈希清单检查。

## 私有工作区下载示例

以下命令只能在私有数据目录执行，且下载后必须使用公开仓库中 `metadata/source_archive_sha256.txt` 对照SHA-256值；不得将下载结果提交至公开仓库。

```bash
mkdir -p data/raw
curl -fL "https://data.mendeley.com/public-api/zip/wjw77byzc2/download/1" -o data/raw/map_green_innovation_v1.zip
curl -fL "https://data.mendeley.com/public-api/zip/s3cdwjthnv/download/1" -o data/raw/digital_transformation_risktaking_v1.zip
sha256sum data/raw/*.zip
```

## 引用

[1] [Bai, B. (2025). *map-green innovation* (V1) [Data set]. Mendeley Data.](https://doi.org/10.17632/wjw77byzc2.1)

[2] [Meng, M. (2024). *Digital transformation and strategic risk taking dataset* (V1) [Data set]. Mendeley Data.](https://doi.org/10.17632/s3cdwjthnv.1)
