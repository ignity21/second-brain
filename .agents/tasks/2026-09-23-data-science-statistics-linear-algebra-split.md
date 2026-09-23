# DataScience 分类拆分

- 状态: 完成
- 日期: 2026-09-23

## 范围

将 `roamnotes-v2/DataScience/` 中的 Statistics（含概率分布）与 Linear Algebra 主索引分支迁为独立大类，保留节点 ID 并修正根索引和资源路径。

## 检查清单

- [x] 盘点两棵索引分支、关联笔记和资源，并确认目标无冲突
- [x] 移动分支笔记，必要时调整 `file:` 链接
- [x] 新建两类根索引并更新 DataScience 根索引
- [x] 验证主索引可达性、ID 引用、Org 语法及资源链接
- [x] 执行一次 `org-roam-db-sync`

## 结果

将 Statistics（含 Probability & Distributions）46 个节点和 Linear Algebra 17 个节点迁至各自大类，保留原节点 ID；新增 Statistics 与 Linear Algebra 大类根索引并更新 Data Science 根索引。统计笔记引用的 24 张截图随笔记迁入 `Statistics/images/`，`assets/` 中的共享图像仍可由两个新目录通过 `../assets/` 引用。

验证：两个大类中的节点均可从新根索引到达；全库无重复 ID；两类笔记的本地 `file:` 链接均可解析。全库仍检出 8 个未定义 ID，均位于既有 MachineLearning 笔记，不由本次拆分引入。抽查发现部分搬迁笔记原先缺少 TOC 或 property drawer，内容未改，保留现状。`emacsclient --eval '(org-roam-db-sync)'` 成功返回 `nil`。
