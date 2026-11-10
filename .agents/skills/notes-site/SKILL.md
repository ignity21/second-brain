---
name: notes-site
description: Work on the published org-roam-ui notes site. Use when changing the frontend fork ignity21/org-roam-ui (~/repos/org-roam-ui), the publish/ export and build scripts, or .github/workflows/publish-roam-ui.yml, and when confirming that a push deployed.
---

# 笔记站（org-roam-ui 发布）

## 发布方式

站点由 `.github/workflows/publish-roam-ui.yml` 构建。推送到 `master` 并改动了 `roamnotes-v2/**`、`publish/**` 或工作流文件时触发，也可以手动触发。工作流按 `ORG_ROAM_UI_REF` 固定的 fork `ignity21/org-roam-ui` 提交构建前端，再用 `publish/export.el` 导出 `roamnotes-v2/` 下的全部笔记。

推送后确认部署：用 `gh run list --workflow publish-roam-ui.yml --limit 1` 找到这次运行，`gh run watch <id>` 等它结束；失败时用 `gh run view <id> --log-failed` 查原因并修复。

## fork 分支约定

本地仓库在 `~/repos/org-roam-ui`。

- `main` 跟随上游 `org-roam/org-roam-ui`，不放自有改动。
- `enhanced` 是自用开发分支，Doom 从它安装并使用其中的 `out/`。Emacs 和静态站都需要的功能（搜索、主题、侧栏等）在这里开发，提交时一并重建 `out/`。
- `static` = `enhanced` + 仅用于静态化的提交（`NEXT_PUBLIC_STATIC` 模式、快照数据、静态默认值）。`enhanced` 更新后：
  1. 把 `static` rebase 到 `enhanced`，用 `--force-with-lease` 推送，不反向合并。
  2. 把 `ORG_ROAM_UI_REF` 改为新的 `static` 提交。
- 上游已停止维护（最后一次合并 PR 在 2022 年）。通用功能只在 `enhanced` 开发，不另开 `pr/*` 分支。现有 `pr/*` 分支及其上游 PR 只作记录保留，不再 rebase 或催审；上游恢复合并 PR 后，再从 `enhanced` 挑提交提 PR。

## 构建与完成标准

- 本机 Node 26 构建需设 `NODE_OPTIONS=--openssl-legacy-provider`。
- 受影响分支的 `tsc --noEmit` 通过，且 `next build && next export` 成功。
- 推送了新的 `ORG_ROAM_UI_REF` 时，按上文确认 Publish 工作流部署成功。
