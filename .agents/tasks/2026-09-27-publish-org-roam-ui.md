# 发布 org-roam-ui 到 GitHub Pages

- 状态: 部署中
- 日期: 2026-09-27
- 计划: 静态化自用 fork（`ignity21/org-roam-ui` 的 `search` 分支），发布 `roamnotes-v2/` 全部笔记到
  `https://ignity21.github.io/second-brain/`。

## 检查清单

- [x] fork 新建 `static` 分支：`NEXT_PUBLIC_STATIC=1` 时从静态文件取图谱、笔记、图片，隐藏 Emacs 专属操作
- [x] `publish/export.el`：Emacs batch 生成 `graphdata.json`、`variables.json`、`notes/<id>.org`
- [x] `publish/build.sh`：导出数据、构建 UI、组装 `site/`
- [x] 本地预览验证（图谱、正文、图片、搜索、LaTeX、无 localhost 请求）
- [x] `.github/workflows/publish-roam-ui.yml` 部署到 Pages
- [ ] push fork 与 second-brain，确认线上页面

## 进度

- fork 改动在 `static` 分支（已推送，commit `58f720f`）：新增 `util/static.ts`，改 `pages/index.tsx`、
  `Link.tsx`、`uniorg.tsx`、`Search/index.tsx`、`OrgImage.tsx`、`contextmenu.tsx`、`webSocketFunctions.ts`、
  `next.config.js`；`tsc --noEmit` 通过，Node 26 下 `next build && next export` 成功。
- `publish/export.el` 用 org-roam-ui 自身函数导出 307 个节点、509 条链接；用 Doom 已装包与 MELPA 安装两种方式输出一致。
- 本地 `/second-brain/` 子路径预览：图谱、全文搜索、侧栏正文、KaTeX、代码块、反链、`images/` 与 `../assets/`
  图片均正常；无 localhost 请求，唯一 404 是站点根 `/favicon.ico`。
- 待办：提交并推送 fork `static` 分支与本仓库改动，观察 Actions 与线上页面。
