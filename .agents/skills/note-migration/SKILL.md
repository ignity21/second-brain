---
name: note-migration
description: Migrate old org-roam notes from the legacy library (roamnotes/) into roamnotes-v2/. Use when the user asks to migrate, port, or move old notes or a whole category (e.g. "迁移 C++ 笔记", "迁移下一个笔记", "迁移 DataScience"), or to clean up already-migrated source notes, images, or shared assets.
---

# 旧笔记迁移

仅在将 `roamnotes/` 的内容迁往 `roamnotes-v2/` 时使用。笔记的一般组织规则遵循根目录 [AGENTS.md](../../../AGENTS.md)（索引树、ID、资源、验证约定），本 skill 只覆盖迁移特有的步骤。

## 目标与映射

- `Default/` → `Inbox/`。
- `C++/`、`DataScience/`、`Games/`、`Python/`、`Trading/` 默认迁入同名大类。
- 旧备忘录将 `EmacsLisp/` 映射为同名目录；当前目标已有 `Elisp/`，迁移相关内容时先核对现有索引和语义，避免另建重复大类。
- 分类图片迁入目标分类的 `images/`，共享 `assets/` 迁入目标库根目录的 `assets/`。
- 源、目标的实际内容以文件系统为准。2026-07-28 备忘录中的文件数、测试文件和「需新建」目录清单属于历史快照，不作为当前状态。

## 迁移与清理

1. 确认源内容有可恢复的 Git 备份，检查目标文件是否已存在，避免覆盖已有笔记或资源。
2. 将请求范围内的笔记及依赖资源迁入目标；保留正文、property drawer、原 ID 和内部 ID 链接。将笔记接入合适的主索引，并按新位置更新资源路径。
3. 检查目标内容完整、索引已接入且相关资源链接可解析后，在同一次迁移中删除对应源笔记。该清理属于迁移任务本身，无需逐文件确认。
4. `images/`、`assets/` 等源资源保留到所有相关笔记迁移完成后统一清理；清理前检查剩余引用。注意 `Default/puml/SystemDesign/` 中的 PlantUML 资源及其引用。
5. 按根规则完成受影响范围的验证，并执行一次 `org-roam-db-sync`；无法同步时说明原因。

## 相对路径示例

当笔记位于 `roamnotes-v2/C++/example.org` 时：

- 本类图片：`[[file:images/Overview/example.png]]` → `roamnotes-v2/C++/images/Overview/example.png`。保留原资源子目录时通常无需改路径。
- 共享资源：旧 `[[../assets/CPP/example.svg]]` 统一为 `[[file:../assets/CPP/example.svg]]` → `roamnotes-v2/assets/CPP/example.svg`。
- 此处不能写成 `file:assets/...`，否则会指向 `C++/assets/`。从更深目录移出笔记时，重新计算所有受影响的相对路径。

缓存和忽略配置以目标库实际配置为准，不迁移生成的 org-roam 数据库作为笔记内容。保留 `pages/`、`logseq/`。
