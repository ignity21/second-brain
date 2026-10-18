# 脚本生成 toc-org 目录

- 状态: 完成
- 日期: 2026-10-18
- 计划: 用 batch Emacs（`-Q`，只加载 Doom straight 里的 org 和 toc-org）调用 `toc-org-insert-toc`，
  不依赖运行中的 Emacs；AGENTS.md 改为由脚本生成 TOC；补齐现有 13 篇空的或过时的 TOC。

## 检查清单

- [x] `scripts/update_toc.py`
- [x] 验证：Emacs 生成过的 TOC（`polars-20260802.org`）重跑无变化；`ss-20261018.org` 生成完整目录
- [x] AGENTS.md：Org 排版的 TOC 规则、按改动验证
- [x] 补齐 13 篇：uv、practical_advice、time_series_with_polars、recursion、writing_doom_modules、
  MachineLearning 7 篇、ss
- [x] 补齐后全库重跑无变化，检查 TOC 链接语法

## 进度

- 原计划写成 13 篇「空的或过时的」TOC。实际上 12 篇是空的，`time_series_with_polars` 的条目本身没错，
  是 TOC 标题下多了一句指向 Polars 的正文，toc-org（Emacs 保存时也一样）会删掉它。这句已移到 TOC 前面。
  脚本加了保护：TOC 段里有非条目内容时报错并跳过该文件；AGENTS.md 写明 TOC 下不放正文。
- 验证：Emacs 生成过的 `polars-20260802.org` 重跑后逐字节不变；全库 22 篇带 TOC 的笔记重跑无变化；
  改动的笔记行内标记检查为空；脚本 ruff、basedpyright、radon（全部 B 以上）通过。
- 未改 ID，也没有移动文件，不需要 `org-roam-db-sync`。
