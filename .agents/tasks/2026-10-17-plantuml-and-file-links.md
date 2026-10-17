# PlantUML 渲染与 org-roam-ui 文件链接

- 状态: 完成
- 日期: 2026-10-17
- 计划: UI 隐藏带 `:file` 的 plantuml 代码块；`file:` 资源链接（如 show-me 的 `demos/*.html`）可在新标签页打开；
  写笔记时由 agent 用 PlantUML CLI 生成图片。

## 检查清单

- [x] fork `enhanced`：`processOrg.tsx` 隐藏后面跟着 `#+RESULTS:` 的 plantuml 代码块（uniorg 不保留 header 参数，无法直接看 `:file`）
- [x] fork `enhanced`：`Link.tsx` 为 `file:` 链接（非 `.org`）生成新标签页链接，实时模式走 `/img/`
- [x] `enhanced` 的 `tsc --noEmit`、`next build && next export` 通过，重建 `out/` 并推送（`5e18a7e`）
- [x] `static` rebase 到 `enhanced`，静态模式 `file:` 链接走 `files/`，构建通过后 `--force-with-lease` 推送（`fac42a9`）
- [x] 更新 `ORG_ROAM_UI_REF`，确认 Publish 工作流部署成功（run 39014598272；线上重跑同一 Playwright 检查通过）
- [x] 本仓库加 `scripts/render_plantuml.py`，AGENTS.md 写入生成图片的步骤
- [x] Doom 的 org-roam-ui checkout 快进到新 `enhanced`

## 进度

- fork 开发在 `~/repos/org-roam-ui`（依赖用 `npx yarn@1.22.22` 安装）。新增 `util/resource.ts` 统一图片与文件链接的路径解析和 URL；
  `static` 的静态模式提交改为在这里按 `isStatic` 取 `files/`，`OrgImage.tsx` 不再含静态分支。路径先 `decodeURI`，
  修正带空格或非 ASCII 文件名的二次编码。
- 实时模式：Emacs `img` servlet 对 `demos/*.html` 返回 200 `text/html`。
- 静态站本地构建 + Playwright（Chrome）检查 TCP Reliable Delivery 笔记：plantuml 源码 0 个、两张图正常加载、
  demo 链接 `target=_blank` 指向 `/files/Network/demos/tcp_send_window.html`（200 `text/html`）；asyncio 笔记 4 个 Python 代码块照常显示。
- `render_plantuml.py`：对 Network 现有笔记重跑无任何变化（PlantUML 输出逐字节一致）；临时笔记验证补 `#+RESULTS:`、列表内缩进、
  svg 输出、无 `:file` 块跳过、语法错误返回 1；ruff、basedpyright、radon 通过。
