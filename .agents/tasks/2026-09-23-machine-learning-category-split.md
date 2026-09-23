# MachineLearning 类别拆分

- 状态: 完成
- 日期: 2026-09-23

## 范围

将 `roamnotes-v2/DataScience/` 中机器学习主题笔记与专属图片迁至新大类
`roamnotes-v2/MachineLearning/`，保留节点 ID，并更新分类索引和资源链接。

## 检查清单

- [x] 确认机器学习笔记、索引及资源范围，无目标重名或覆盖
- [x] 移动节点并保留原 ID，补齐 MachineLearning 主索引树
- [x] 更新 DataScience 根索引及所有受影响 `file:` 链接
- [x] 将 ML 图片资源放入 MachineLearning 类目录，检查引用完整
- [x] 验证 ID 链接、主父节点、可达性、目录扁平性及 Org 语法
- [x] 执行一次 `org-roam-db-sync`

## 结果

将 88 篇现有机器学习笔记与索引迁至 `roamnotes-v2/MachineLearning/`，新增大类根索引
和 ML Libraries 索引；原 ID 均保留。ML 图片及其引用截图归入 `images/`，修正链接，
DataScience 根索引保留统计、概率、线性代数、数据分析和 Python 库入口。

检查结果：机器学习类本地 `file:` 链接均可解析；索引从新根逐层可达；全库检出的
6 个未定义 ID 中，4 个为正文注释示例，2 个是 Linear Algebra 笔记中待迁入的外部节点
（Eigenvectors、Orthonormal Basis），均非本次移动造成。普通笔记 TOC 规则已检查并修复。
`emacsclient --eval '(org-roam-db-sync)'` 成功返回 `nil`。
