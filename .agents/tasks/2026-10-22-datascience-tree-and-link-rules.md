# DataScience 层级重组与链接规则

Status: Complete

用户 2026-10-22 确认：SciPy、pingouin 搬入 DataScience；链接规则直接写进 AGENTS.md；去掉 Polars 子笔记里往上链的 `See Polars ...`（不新增对 Pandas 的引用）。

目标结构：

```
Data Science
├─ Data Analysis Workflow   ← 吸收 Data Analysis 笔记的流程图
│   ├─ Data Importing
│   ├─ Data Cleaning        ← 变为索引，吸收 Data Quality and Constraints；收入 Cross Field Validation（← ML）
│   ├─ Data Manipulation    ← Numerical / Categorical（← Statistics）/ Date and Time（← Statistics）/ Data Transforming
│   ├─ Exploratory Data Analysis
│   ├─ Data Visualization
│   └─ Data Reporting
└─ Python Data Libraries    ← 吸收 Python DA Modules
    ├─ NumPy, Pandas（→ Basics / Advanced / Timeseries / Datetime ← Statistics）
    ├─ Polars（← Python）, Matplotlib, Seaborn
    └─ statsmodels, SciPy（← Statistics）, pingouin（← Statistics）
```

## Checklist

- [x] AGENTS.md：笔记间链接规则；跨领域笔记放主父节点所在大类；标题级节点标题带上下文
- [x] 搬文件：Polars 5 篇 + 图片；Statistics 5 篇 + 截图；Cross Field Validation
- [x] 重写索引：datascience、Data Analysis Workflow、Data Cleaning、Data Manipulation、Python Data Libraries、Pandas
- [x] 撤销节点：Data Analysis、Data Analysis and Visualization、Data Quality and Constraints、Data Visualization and Reporting、Core Data Libraries、Statistical Python Libraries、Python DA Modules；Data Cleaning 内 3 个分组标题 ID
- [x] 笔记内整行链接标题改为正文引用（DataScience 内，及其他大类指向 DataScience 节点的）
- [x] Python/libraries.org、ML model_evaluation 去掉搬走的节点
- [x] Polars 子笔记去掉 `See Polars ...`
- [x] 验证：入链、唯一主父节点、层数、出度、可达性、file 链接、行内标记、org-roam-db-sync

Result: DataScience 树 5 层内、唯一主父节点、出度 2–8、无跨大类主树连线（scratchpad 检查脚本）。Python / Statistics / MachineLearning 的规则问题数 16→13、46→29、59→49，未引入新问题。补了 6 篇笔记的 TOC。用户 Emacs 已 `org-roam-db-sync`。
另：cc-note-writing 的 library.md、theory.md 与新链接规则对齐。
