# 学习流程落地

Status: In progress（首次实验后重新设计采集与整理流程）

来源：学习流程说明（2026-10-15 讨论）。

## 设计依据

- 可查询细节不再抄录；笔记保存核心模型、判断依据和用户卡点。
- 采集与整理解耦：浏览器端只搬运原文到 `inbox/`，判断由能看到全库的 Claude Code 完成。
- 每份材料必须附 `questions.md`，卡点只能来自用户。
- 全局讲解偏好属于 claude.ai 个人偏好，不在本仓库；仓库内只保留「在库里学习」的简化版（AGENTS.md）。

## 检查清单

- [x] `inbox/` 建立并 gitignore（与 `roamnotes-v2/Unsorted/` 区分）
- [x] `inbox-processing` skill + `.claude/skills` 软链接
- [x] `cc-note-writing` 增加「误解 / 判断」类型与优先保留用户疑问的准入项
- [x] AGENTS.md 增加入库与学习辅助规则、登记 skill
- [x] 首次实验：用计算机网络一节（趣谈网络协议第 6 讲：交换机与 VLAN）走完流程，结果见下节
- [ ] 清点不符合入库规则的既有笔记（待用户要求，先列清单）

## 2026-10-15 仓库清理

- [x] 去掉所有 Logseq 内容（`roamnotes-v2/logseq`、`pages`、`tips.org`、相关忽略和排除规则）
- [x] 删除根目录 `dailies/`、`roamnotes-v2/dailies/`（Unsorted 取代其用途）
- [x] 删除 `pdfnotes/`（org-noter 已不用）
- [x] `roamnotes-v2/Inbox/` 改名 `Unsorted/`，同步仓库文档与 Doom 配置（默认类别、README）
- [x] `inbox/.gitkeep`
- [x] fork `static` 默认 allowlist 改为 `Unsorted/`（`a5bb99b`），`ORG_ROAM_UI_REF` 已更新；待 Publish 工作流部署确认
- [ ] Doom：`init.el` 与 `+roam.el` 中仍有 dailies 目录派生；org-noter / PDF 相关配置（`+noter`）按需移除
- [ ] 讨论书籍类学习流程：如何从 PDF 摘录或书签提取内容作为笔记原料；org-noter 作为备选方案

## 2026-10-15 首次实验反馈

结果：产出一篇环路误解笔记和一张卡片，用户不满意，已全部删除（笔记、卡片和随后的网络能力地图）。另外顺手修好了 `ankinotes/network.org` 中「3 层交换机」卡的层级。

暴露的问题：
- 预测题在采集端出：题目脱离原文看不懂（编号含义、配图缺失），或超出原文讲到的范围（Trunk 只一句带过）；答错被当成「误解」，产出用户并不关心的内容。
- 笔记和卡片都是同一个场景问答，笔记里没有核心模型。
- 没有学习目标：导论类文章里的 corner case 只是用来说明复杂性的；网络这类繁琐领域的排障交给 AI，用户只需做到「了解」。
- 网页上往往拿不到完整原文，`source.md` 可能只是一份总结。

已改：
- [x] 采集提示词先问学习目标（`[目标]`），去掉预测题
- [x] 处理流程先看目标；「了解」档不写笔记、不做卡片

待设计：
- [ ] `source.md` 是总结时，由 AI 展开笔记内容；与「以材料为界」规则如何协调，哪些地方需要先问用户确认
- [ ] 预测题移到写完笔记之后，按笔记出题，题目可直接做成 Anki 卡片巩固
- [ ] 「了解」档的产出放哪里（能力地图怎么组织），还是什么都不收
