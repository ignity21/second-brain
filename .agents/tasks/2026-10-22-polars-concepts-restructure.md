# Polars 概念笔记与 API 子树重组

Status: Complete（用户 Emacs 的 org-roam-db-sync 待执行）

目标：`Polars`（ID 190bfd1c）改写为概念 / 原理笔记；API 笔记移到新索引 `Polars APIs` 下。

结构（用户 2026-10-22 确认）：

```
Python → Third-Party Libraries → Polars → Polars APIs → {Core Operations, Practical Data Transformation, Time Series}
```

- 索引树上限由四层放宽到五层（AGENTS.md）；去掉只剩 Polars 的 `Python Data Analysis Libraries`（2d0b26a1）。
- 概念笔记含「Core API Map」，链接到 API 笔记里的标题级节点；带 ID 的标题加 Polars 上下文。
- 学习目标：Polars 原理「能判断」。

## Checklist

- [x] AGENTS.md：最多四层 → 五层
- [x] learning-goals.md：Polars 条目
- [x] 新建 `Polars Core Operations`（迁入现 Polars 的 API 内容）
- [x] 三篇 API 笔记的关键标题加 ID 和 Polars 上下文
- [x] 新建 `Polars APIs` 索引
- [x] 改写 `Polars` 概念笔记（在 Polars 2.0.0 上核对）
- [x] libraries.org 改链 Polars，删除 data_analysis.org
- [x] Anki `Source:` 行更新
- [x] 验证：TOC、PlantUML、行内标记、标题重名、入链、org-roam-db-sync

Result: 概念笔记在 Polars 2.0.0 / pandas 3.0.6 上逐例运行核对；11 个标题级节点；Anki 10 张卡的 `Source:` 改为 Core Operations。临时库 batch `org-roam-db-sync` 通过；用户 Emacs 未运行 server，真实 DB 未同步。
