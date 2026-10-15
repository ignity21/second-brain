---
name: inbox-processing
description: Process learning materials in the repo-root inbox/ into org-roam notes and Anki cards. Use when the user asks to "处理收件箱" or to extract notes from articles, transcripts, or slides they saved there.
---

# 处理收件箱

`inbox/` 位于仓库根目录（已 gitignore），存放待处理的原始材料；与 `roamnotes-v2/Unsorted/`（未分类的正式笔记）无关。

## 材料约定

一份材料一个子目录，如 `inbox/2026-10-15-tcp-handshake/`：正文或文稿 Markdown、幻灯片 PDF（可选）、侧边栏问答（可选），以及必需的 `questions.md`（用户的疑问、没看懂之处、原来的理解）。没有 `questions.md` 的材料先向用户索取，不对整篇材料直接做笔记。网页材料用 [web-capture-prompt.md](web-capture-prompt.md) 采集；`questions.md` 写「无」时不提取。

## 流程

1. 读取材料和 `questions.md`；检索已有笔记，判断是新内容、补充还是与旧笔记冲突。
2. **先看 `[目标]`**（缺省时问用户）。目标是「了解」：不写笔记、不做卡片，至多在该领域的能力地图里加几行「问题 → 解决办法」，具体机制和排障细节交给 AI；导论类材料通常是这一档。目标是「能判断」或「能排错」时，**围绕 `questions.md` 提取**，只收三类：
   - **误解**：原来怎么理解、错在哪、正确模型是什么。
   - **判断**：技术选择及理由、放弃的方案。
   - **故障**：触发条件、排查证据、确认原因的方法。
   概念定义、API、语法、按原文结构的复述不收。宁可少，不要把整篇材料重新整理一遍。
   **以材料为界**：笔记和卡片里的结论都要能在材料中找到依据。AI 只做纠正误解所必需的改写，不引入材料没讲的机制、参数、例外或更复杂的场景（例如重传退避、内核参数、NAT 例外）。用户关心但材料没覆盖的问题，在回复里列出，由用户决定要不要另外追问。
3. **粒度**：一个疑问最多对应一条内容，不按材料章节切分。逐条判断：
   - 换个时间问 AI 一次就能答对 → 不收。
   - 会改变技术选择或排查方式 → 收（判断 / 故障）。
   - 纠正了用户原来的理解 → 收，并做卡片（误解）。
   每条写一个结论 + 理由或证据 + 最小例子；一份材料通常 0–3 条，0 条是正常结果。
4. 按 `cc-note-writing` 写入或合并到已有笔记（优先合并，不重复新建），索引与验证遵循 AGENTS.md。
5. 为「误解」类内容生成 Anki 卡片（`anki-cards` skill；目标 Deck 的规则以该 skill 为准）。
6. 材料处理完后删除（不归档进知识库）；若用户要保留，移到 `inbox/_archive/`。
7. 回复列出：新增或修改的笔记、生成的卡片、没有提取出内容的材料及原因。
