# GitHub 发布与数据隔离指南

本项目已经建立两个仓库：公开代码与汇总结果仓库，以及私有原始/派生数据和论文仓库。公开仓库地址为 <https://github.com/JustinZheng161/digital-green-invention-reproducibility>；私有仓库仅对获授权成员开放：<https://github.com/JustinZheng161/digital-green-invention-data-private>。

| 仓库 | 可见性 | 应包含 | 不得包含 |
|---|---|---|---|
| `digital-green-invention-reproducibility` | Public | 代码、测试、数据DOI/哈希、汇总表、汇总图、方法与修改日志。 | ZIP、XLSX、DTA、匹配后的公司—年度数据、手稿、凭据。 |
| `digital-green-invention-data-private` | Private | 原始档案、提取数据、匹配面板、完整审计记录、手稿与私有复现材料。 | `.env`、令牌、私钥、浏览器下载的非研究文件。 |

## 从零开始的完整命令序列

以下命令是一套可复用的发布序列。示例先初始化公开库，再建立私有库；`OWNER`应替换为GitHub账户名。

```bash
# 0) 假设公开与私有目录已按README约定建立并分别放好内容。
export OWNER="YOUR_GITHUB_ACCOUNT"
export PUBLIC_REPO="digital-green-invention-reproducibility"
export PRIVATE_REPO="digital-green-invention-data-private"

# 1) 公开代码/汇总结果仓库。
cd /absolute/path/to/${PUBLIC_REPO}
git init -b main
git config user.name "Your Name"
git config user.email "YOUR_GITHUB_NOREPLY_EMAIL"
git add README.md LICENSE CITATION.cff requirements.txt .gitignore src tests data metadata results docs
git diff --cached --name-only
python tests/audit_public_release.py
git commit -m "Initial reproducibility and aggregate-results release"
gh repo create "${OWNER}/${PUBLIC_REPO}" --public --source=. --remote=origin --push
gh repo view "${OWNER}/${PUBLIC_REPO}" --json nameWithOwner,visibility,url

# 2) 私有数据与手稿仓库。
cd /absolute/path/to/${PRIVATE_REPO}
git init -b main
git config user.name "Your Name"
git config user.email "YOUR_GITHUB_NOREPLY_EMAIL"
git add .
git diff --cached --name-only
git commit -m "Initial private data and manuscript release"
gh repo create "${OWNER}/${PRIVATE_REPO}" --private --source=. --remote=origin --push
gh repo view "${OWNER}/${PRIVATE_REPO}" --json nameWithOwner,visibility,url

# 3) 后续更新的安全发布顺序。
cd /absolute/path/to/${PUBLIC_REPO}
python tests/audit_public_release.py
python tests/test_reproducibility.py   # 需先设置DGI_PRIVATE_DATA_ROOT
git add -A && git commit -m "Describe the update" && git push origin main

cd /absolute/path/to/${PRIVATE_REPO}
git status --short
git add -A && git commit -m "Sync private data and manuscript update" && git push origin main
```

## 已合并的 `.gitignore` 规则

| 分类 | 已忽略对象 | 目的 |
|---|---|---|
| 环境与缓存 | `.venv/`、`__pycache__/`、`.pytest_cache/`、`.coverage` | 避免提交可再生依赖与缓存。 |
| 凭据 | `.env*`、`*.pem`、`*.key` | 防止密钥和运行时秘密泄漏。 |
| 原始与派生数据 | `data/raw/`、`data/derived/`、`*.zip`、`*.dta`、`*.xlsx`、`*.parquet`等 | 阻止微观数据和上游受限档案进入公开库。 |
| 手稿与投稿文件 | `paper/`、`submission/`、`*.docx`、`*.pdf` | 保持作者对未投稿手稿的控制。 |
| 日志与临时文件 | `*.log`、`tmp/`、`.cache/` | 减少不可复现或含路径信息的噪声。 |
| 公开汇总例外 | `!results/tables/*.csv` | 允许公开无公司标识符的汇总结果表。 |

> 每次公开推送前必须运行 `python tests/audit_public_release.py`。任何 `firm_id`、`Stockcode`、`股票代码`列，或ZIP/XLSX/DTA/手稿文件都会使审计失败。
