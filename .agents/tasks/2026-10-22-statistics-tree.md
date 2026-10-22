# Statistics 层级重组

Status: Complete（用户 Emacs 的 org-roam-db-sync 待执行）

总任务见 `2026-10-22-v2-category-restructure.md`。用户 2026-10-22 确认：Generating Samples 放到 SciPy，Probability and Distributions 可正文引用；内容笔记 `Statistics` 改名 `Statistics Overview` 保留。

目标结构：

```
Statistics
├─ Descriptive Statistics and Sampling
│   ├─ Statistics Overview（← 内容笔记 Statistics 改名）, Types of Data, Correlation, Relative Error
│   ├─ Descriptive Statistics → IQR
│   └─ Data Sampling → Sampling Distribution → Central Limit Theorem; Bootstrap Distribution
├─ Probability and Distributions
│   ├─ Probability
│   ├─ Discrete Distributions → Binomial, Discrete Uniform, Poisson → Poisson Process
│   └─ Continuous Distributions → Continuous Uniform, Normal, Exponential, Log-normal, T, Z, Chi-squared
└─ Hypothesis Testing and Inference
    ├─ Inferential Statistics, Statistic Experiments, Confidence Intervals, Degrees of Freedom
    └─ Hypothesis Testing → P-Values, Z-Test, T-Test, ANOVA
```

## Checklist

- [x] 撤销 Statistical Foundations、Probability Foundations、Continuous Probability Distributions
- [x] 重写根索引与三个中间索引
- [x] 内容笔记：整行链接标题只连直接子节点，其余改正文引用；去掉 `- links ::`
- [x] Generating Samples 并入 SciPy 的同名标题（保留 ID，标题 `Generating Samples with SciPy`）
- [x] 改名：Statistics Overview；Discrete / Continuous Uniform Distribution
- [x] 验证：检查脚本、入链、TOC、行内标记、file 链接、org-roam-db-sync

Result: 深度 7→5，问题 34→0（剩余 8 条为允许的「笔记兼父节点」）；唯一主父节点，无互链、无指向祖先的引用。顺带给 Descriptive Statistics、Data Sampling 补了 TOC_2。临时库 batch `org-roam-db-sync` 通过（314 节点）；用户 Emacs 未运行 server，真实 DB 未同步。
另见：MachineLearning `supervised_learning-20230817.org` 有 4 个指向不存在 ID 的链接（既有问题，留给 ML 子任务）。
