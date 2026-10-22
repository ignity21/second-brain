# LinearAlgebra 层级重组

Status: Complete

总任务见 `2026-10-22-v2-category-restructure.md`。用户 2026-10-22 确认目标结构：

```
Linear Algebra
├─ Linear Algebra Basics
│   ├─ Linear Algebra Overview（← 内容笔记 Linear Algebra 改名）
│   ├─ Vector → Cross Product
│   ├─ Matrix → Identity Matrix, Rotation Matrix, Pseudoinverse（Inverse 标题下）
│   ├─ Linear Transformation
│   ├─ Eigenvectors
│   └─ Orthonormal Basis
└─ Matrix Calculus（← Advanced Linear Algebra 改名）
    ├─ The Jacobian
    └─ The Hessian
```

## Checklist

- [x] 撤销 Linear Algebra Foundations（单子节点索引）
- [x] 重写根索引、Basics、Matrix Calculus
- [x] 内容笔记：Overview 去掉非子节点的整行链接标题和过期 TODO；Vector 收录 Cross Product；Matrix 收录 Pseudoinverse，去掉 `- links ::`
- [x] Roundoff Errors 移到 `MachineLearning/`（主父节点 Neural Network，改名留给 ML 子任务）
- [x] 验证：检查脚本、入链、行内标记、file 链接、org-roam-db-sync

Result: 深度 6→4，问题 12→1（剩余 1 条为允许的「笔记兼父节点」Vector → Cross Product）；删除单子节点索引 Linear Algebra Foundations，Advanced Linear Algebra 改名 Matrix Calculus（文件改名 `matrix_calculus.org`），内容笔记改名 Linear Algebra Overview，均保留 ID。顺带给 Matrix 补了 TOC_2。临时库 batch `org-roam-db-sync` 通过（313 节点，无悬空 ID 链接）；2026-10-22 用 Doom daemon 对真实 DB 执行了 `org-roam-db-sync`（305 节点，无悬空 ID 链接）。
留给 ML 子任务：`machine_learning-20230802.org` 的 Math Prerequisites 是只列链接的列表（含指向 Linear Algebra Overview 的链接）；Roundoff Errors 标题缺领域上下文。
另见：Matrix 笔记 Matrix multiplication 下的 2D / 3D 行列式小节应归到 Determinant（既有排版问题，未改）。
