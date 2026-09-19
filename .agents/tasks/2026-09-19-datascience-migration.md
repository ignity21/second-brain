# DataScience 迁移到 roamnotes-v2

- 状态: 完成
- 日期: 2026-09-19
- 提交: `eb44b4c`（迁移）、`58f9238`（清理源资源）

## 范围

将 `roamnotes/DataScience/` 的 146 篇笔记及依赖资源迁入 `roamnotes-v2/DataScience/`，
并接入主索引树。

## 检查清单

- [x] 复制 146 篇笔记 + `images/` + `pyproject.toml`/`uv.lock` 到 `roamnotes-v2/DataScience/`
- [x] 共享资源 `assets/ML|Statistics|Math` 复制到 `roamnotes-v2/assets/`
- [x] 修正链接路径：
  - [x] 40 处 `[[../assets/...]]` 统一为 `[[file:../assets/...]]`
  - [x] `mini_batch_gradient_descent` 的绝对路径改为相对路径
  - [x] 修复 `activation_functions` 的 SigmoidFunction 坏引用（指向 `images/ML/`）
  - [x] 修复 `bias_variance` 的 `BaisVariance_2.png` 文件名错拼（重命名资源文件）
  - [x] 修复 `linear_regression` 指向 notebooks 的相对路径层级（`../` → `../../`）
  - [x] 把 `activation_functions` 引用的 Overview 截图复制进 DataScience 图片目录
- [x] 生成 `datascience.org` 根索引 + 8 个中间索引 + 25 个子分组索引（UUID v4，纯导航）
- [x] 验证：ID 链接可解析、图片/资源链接可解析、索引树连通、单主父节点、
      无重复标题（为此改了 7 个与笔记重名的子分组标题）
- [x] 删除源笔记 + 源图片 + 源环境文件；移除已迁移的 `assets/ML|Statistics|Math`
- [x] 执行 `org-roam-db-sync`：204 个 DataScience 节点，无悬空链接

## 结果与剩余事项

- 索引树：`datascience.org` → 8 个中间索引 → 25 个子分组 → 146 篇笔记
- `roamnotes/DataScience/pandas-20241106.org_archive` 为非笔记归档文件（指向已不存在的
  旧 pages/ 路径），未删除，待用户自行清理
- `linear_algebra` 笔记仍链向 `Default/` 的 orthonormal_basis、eigenvectors（有效 ID
  引用），待 Default 迁移后解析
- 源 `roamnotes/assets/` 其余子目录按约定保留到其它大类迁移完成后统一清理
