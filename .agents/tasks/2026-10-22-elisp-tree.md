# Elisp 层级重组

Status: Complete

总任务见 `2026-10-22-v2-category-restructure.md`。初始检查：深度 5，问题 5（condition-case、Interactive Functions 各两个父节点；Data Structures、Functions、Learning Resources 单子节点）。Elisp 以外只有 `ankinotes/elisp.org` 的来源链接指向本类。

用户 2026-10-22 确认目标结构和改标题：

```
Emacs Lisp
├─ Language Fundamentals
│   ├─ Core Language → Symbols, nil, Evaluation, Functions → Inline Functions, Macros,
│   │     Special Forms → save-excursion, Interactive Functions
│   ├─ Control Flow and Error Handling → condition-case, Loops, Recursion
│   └─ List Functions（← 撤销 Data Structures）
├─ Emacs Buffer, Text, and Configuration APIs（← 撤销 Emacs APIs and Workflows）
├─ Emacs Debugging and Navigation Tools
├─ Doom Emacs（不变，对应 Doom 的 :completion/:ui/:editor/:tools 模块分组）
└─ Learning Resources（并入 Tutorials，叶节点）
```

## Checklist

- [x] 撤销 Data Structures、Emacs APIs and Workflows 索引；Tutorials 并入 Learning Resources
- [x] Special Forms：condition-case、interactive 整行链接改为正文引用
- [x] 正文引用说明关系：Doom Configuration → Writing Doom Modules，LSP → Profiling
- [x] 改标题（保留 ID）：ELisp Inline Functions、ELisp ~save-excursion~、Emacs Dired、Corfu in Doom、Vertico in Doom、Multiple Cursors in Doom；同步 anki 来源链接文字
- [x] 验证：检查脚本、入链、行内标记、file 链接、org-roam-db-sync

Result: 深度 5（Core Language → Functions → Inline Functions 仍是第 5 层），问题 5→2，剩余 2 条是允许的笔记兼父节点（Functions → Inline Functions、Special Forms → save-excursion）。根节点出度 5，删除 3 个索引（Data Structures、Emacs APIs and Workflows、Tutorials；全库无剩余引用），condition-case、Interactive Functions 只剩一个父节点。改名均保留 ID，anki 来源链接文字已同步。无行内标记问题、无重名标题；临时库 batch `org-roam-db-sync` 通过（305 节点，无悬空 ID 链接）；2026-10-22 用 Doom daemon 对真实 DB 执行了 `org-roam-db-sync`（305 节点，无悬空 ID 链接）。
另见：Special Forms 的例子里 ~setq!~ 是 Doom 宏而不是 special form（既有内容问题，未改）。
