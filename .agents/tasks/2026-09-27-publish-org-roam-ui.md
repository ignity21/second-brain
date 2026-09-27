# 发布 org-roam-ui 到 GitHub Pages

- 状态: 完成
- 日期: 2026-09-27
- 计划: 静态化自用 fork（`ignity21/org-roam-ui` 的 `search` 分支），发布 `roamnotes-v2/` 全部笔记到
  `https://ignity21.github.io/second-brain/`。

## 检查清单

- [x] fork 新建 `static` 分支：`NEXT_PUBLIC_STATIC=1` 时从静态文件取图谱、笔记、图片，隐藏 Emacs 专属操作
- [x] `publish/export.el`：Emacs batch 生成 `graphdata.json`、`variables.json`、`notes/<id>.org`
- [x] `publish/build.sh`：导出数据、构建 UI、组装 `site/`
- [x] 本地预览验证（图谱、正文、图片、搜索、LaTeX、无 localhost 请求）
- [x] `.github/workflows/publish-roam-ui.yml` 部署到 Pages
- [x] push fork 与 second-brain，确认线上页面

## 进度

- fork 改动在 `static` 分支（已推送，commit `58f720f`）：新增 `util/static.ts`，改 `pages/index.tsx`、
  `Link.tsx`、`uniorg.tsx`、`Search/index.tsx`、`OrgImage.tsx`、`contextmenu.tsx`、`webSocketFunctions.ts`、
  `next.config.js`；`tsc --noEmit` 通过，Node 26 下 `next build && next export` 成功。
- `publish/export.el` 用 org-roam-ui 自身函数导出 307 个节点、509 条链接；用 Doom 已装包与 MELPA 安装两种方式输出一致。
- 本地 `/second-brain/` 子路径预览：图谱、全文搜索、侧栏正文、KaTeX、代码块、反链、`images/` 与 `../assets/`
  图片均正常；无 localhost 请求，唯一 404 是站点根 `/favicon.ico`。
- 已推送（second-brain `71af752`），Actions 运行 36256014352 成功；线上图谱、搜索、正文与图片检查通过。搜索首次打开会并发请求约 300 个笔记文本，偶见单个 503，重试即恢复。
- 自定义域名：Cloudflare `CNAME roam → ignity21.github.io`（DNS only）；Pages custom domain 设为 `roam.ignity.xyz`，
  工作流 `BASE_PATH: ""` 改为根路径发布（`c34d4ca`），证书已签发并强制 HTTPS；旧地址 302 跳转到新域名。
  线上图谱、搜索、正文与图片检查通过，无 HTTP 错误。

## 后续

- [x] 搜索改为一次读取 `data/notes.json`，避免约 300 个并发请求偶发 503（fork `f82a941`，同时修复无标签节点显示空标签）
- [x] Actions 升级到 Node 24 版本（checkout/setup-node v7、upload-pages-artifact/deploy-pages v5、setup-emacs v8.0，构建用 Node 24）；`runs-on` 固定 `ubuntu-24.04`
- [x] GitHub 账户验证 `ignity.xyz` 域名（Cloudflare TXT `_github-pages-challenge-ignity21`，已 verified）
- 暂缓：线上主题、`file:~/…ipynb` 链接、`static` 与 `search` 分支合并
