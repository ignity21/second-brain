# roamnotes-v2 各大类层级与链接整理

Status: In progress

按 AGENTS.md「主索引树」「笔记间链接」逐个大类整理：去掉迁移时留下的平行索引层和冗余枢纽节点，保证唯一主父节点、≤ 5 层、出度 2–8，笔记内整行链接标题只连直接子节点，正文引用不指向祖先、索引，也不互链。每个大类一个子任务文件，目标结构先请用户确认。

检查脚本（2026-10-22 起草，在 scratchpad，未入库）按大类统计问题数；初始结果：

| 大类 | 笔记数 | 深度 | 问题数 | 主要问题 |
|---|---|---|---|---|
| DataScience | 37 | 5 | 6（均为允许的笔记兼父节点） | — |
| Statistics | 41 | 7 | 34 | 两套平行索引，几乎每篇两个父节点 |
| MachineLearning | 89 | 7 | 76 | 同上，规模最大 |
| LinearAlgebra | 17 | 6 | 12 | 两套父节点；`Roundoff Errors` 被 ML 收录 |
| Python | 37 | 5 | 10 | |
| Network | 9 | 3 | 9 | 笔记间互链；单子节点索引 |
| Elisp | 53 | 5 | 5 | |

## Checklist

- [x] DataScience（`2026-10-22-datascience-tree-and-link-rules.md`、`2026-10-22-polars-concepts-restructure.md`）
- [x] Statistics（`2026-10-22-statistics-tree.md`）
- [x] LinearAlgebra（`2026-10-22-linear-algebra-tree.md`）
- [ ] MachineLearning（依赖 Statistics、LinearAlgebra 的结果，最后做）
- [x] Python（`2026-10-22-python-tree.md`）
- [x] Network（`2026-10-22-network-tree.md`）
- [x] Elisp（`2026-10-22-elisp-tree.md`）
