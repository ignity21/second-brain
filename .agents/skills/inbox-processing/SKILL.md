---
name: inbox-processing
description: Process learning materials in the repo-root inbox/ into org-roam notes and Anki cards. Use when the user asks to "处理收件箱" or to extract notes from articles, transcripts, or slides they saved there.
---

# 处理收件箱

`inbox/` 位于仓库根目录（已 gitignore），存放待处理的原始材料；与 `roamnotes-v2/Unsorted/`（未分类的正式笔记）无关。

## 材料约定

一份材料一个子目录，如 `inbox/2026-10-15-tcp-handshake/`：正文或文稿 Markdown、幻灯片 PDF（可选）、侧边栏问答（可选），以及必需的 `questions.md`（用户的疑问、没看懂之处、原来的理解）。没有 `questions.md` 的材料先向用户索取，不对整篇材料直接做笔记。

## 流程

1. 读取材料和 `questions.md`；检索已有笔记，判断是新内容、补充还是与旧笔记冲突。
2. **围绕 `questions.md` 提取**，只收三类：
   - **误解**：原来怎么理解、错在哪、正确模型是什么。
   - **判断**：技术选择及理由、放弃的方案。
   - **故障**：触发条件、排查证据、确认原因的方法。
   概念定义、API、语法、按原文结构的复述不收。宁可少，不要把整篇材料重新整理一遍。
3. 按 `cc-note-writing` 写入或合并到已有笔记（优先合并，不重复新建），索引与验证遵循 AGENTS.md。
4. 为「误解」类内容生成 Anki 卡片（`anki-cards` skill；目标 Deck 的规则以该 skill 为准）。
5. 材料处理完后删除（不归档进知识库）；若用户要保留，移到 `inbox/_archive/`。
6. 回复列出：新增或修改的笔记、生成的卡片、没有提取出内容的材料及原因。
