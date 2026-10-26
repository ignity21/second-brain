---
name: note-migration
description: Migrate old org-roam notes from the legacy library (roamnotes/) into roamnotes-v2/. Use when the user asks to migrate, port, or move old notes or a whole category (e.g. "迁移 C++ 笔记", "迁移下一个笔记", "迁移 DataScience"), or to clean up already-migrated source notes, images, or shared assets.
---

# 旧笔记迁移

仅在将 `roamnotes/` 的内容迁往 `roamnotes-v2/` 时使用。笔记的一般组织规则遵循根目录 [AGENTS.md](../../../AGENTS.md)（索引树、ID、资源、验证约定），内容取舍遵循 [cc-note-writing](../cc-note-writing/SKILL.md)；本 skill 只覆盖迁移特有的步骤。`roamnotes/` 不在 org-roam 数据库中，迁移期间新旧库同时存在同一 ID 不会冲突。

## 目标归属

- 源目录只是起点，逐篇按内容决定归属：`C++/`、`Trading/` 等默认迁入同名大类，但内容属于别的领域时，放进合适的现有大类（如网络笔记进 `Network/`），或在形成稳定、独立的知识领域时新建大类（标准见 AGENTS.md「主索引树」）。
- `Default/` 是旧库的默认收集箱，不整体映射到 `Unsorted/`：按内容分到各大类，确实无处归属的才放 `Unsorted/`。
- 已有 `Elisp/` 覆盖旧备忘录中的 `EmacsLisp/`，不另建重复大类。
- 迁移涉及新建大类或把较多笔记迁出源目录对应的大类时，先在任务文件中列出归属方案给用户确认。
- 分类图片迁入目标分类的 `images/`，共享 `assets/` 迁入目标库根目录的 `assets/`。源、目标的实际内容以文件系统为准；2026-07-28 备忘录中的文件数和目录清单是历史快照。

## 改造

迁移不是原样搬运，而是按新规则重写：

- 按 AGENTS.md「入库与学习辅助」和 cc-note-writing 重组内容：可查询的 API、语法细节删去或压缩，保留核心模型、判断依据和用户的卡点；碎片笔记可合并，过大的笔记可拆分；按新的主索引树重建分组，不沿用旧索引结构。
- 合并时保留主笔记的 ID（有外部入链的旧笔记优先作主笔记）。被并入笔记的 ID 只在有本次迁移范围之外的入链（未迁移的旧笔记或 `roamnotes-v2/`）时保留：放到承接其内容的标题上（标题级节点）；否则随合并废弃，迁移范围内的链接改指新节点，并在任务文件中记下旧笔记到新笔记的映射。
- 指向尚未迁移笔记的 ID 链接原样保留（对方迁移时保留原 ID 即可恢复），在任务文件中列出；指向已废弃 ID 的链接改为指向吸收其内容的节点或改成纯文本。
- 被删减的内容无需逐条确认：源笔记保留在 `roamnotes/`，用户可对照。

## 迁移与清理

1. 在 `.agents/tasks/` 建任务文件，写明归属方案、新索引树和合并/删减计划；检查目标文件是否已存在，避免覆盖已有笔记或资源。
2. 按方案写入目标笔记和依赖资源，接入主索引，按新位置更新资源路径。
3. 迁移完成后 *保留* 源笔记、`images/`、`assets/`，由用户比对后决定何时删除；只有用户要求清理时才删除，删除前检查剩余引用（含 `Default/puml/SystemDesign/` 的 PlantUML 资源）。
4. 按根规则完成受影响范围的验证，并执行一次 `org-roam-db-sync`；无法同步时说明原因。

## 相对路径示例

当笔记位于 `roamnotes-v2/C++/example.org` 时：

- 本类图片：`[[file:images/Overview/example.png]]` → `roamnotes-v2/C++/images/Overview/example.png`。保留原资源子目录时通常无需改路径。
- 共享资源：旧 `[[../assets/CPP/example.svg]]` 统一为 `[[file:../assets/CPP/example.svg]]` → `roamnotes-v2/assets/CPP/example.svg`。
- 此处不能写成 `file:assets/...`，否则会指向 `C++/assets/`。笔记迁往其他大类时，重新计算所有受影响的相对路径。

缓存和忽略配置以目标库实际配置为准，不迁移生成的 org-roam 数据库作为笔记内容。不迁移 `pages/`、`logseq/`（Logseq 已弃用）。
