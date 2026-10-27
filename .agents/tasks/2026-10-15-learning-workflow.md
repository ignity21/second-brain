# 学习流程落地

Status: In progress — 首次实验后重新设计采集与整理流程

来源：学习流程说明（2026-10-15 讨论）。

## 设计依据

- 可查询细节不再抄录；笔记保存核心模型、判断依据和用户卡点。
- 采集与整理解耦：浏览器端只搬运原文到 `inbox/`，判断由能看到全库的 Claude Code 完成。
- 每份材料必须附 `questions.md`，卡点只能来自用户。（2026-10-16 取消，见末节）
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

## 2026-10-16 改用页面总结作为材料

用户在网页上直接点「summarize page」（不加提示词）得到的总结，质量比搬原文更好：
- 按「问题 → 机制」组织，结尾的总结表本身就是「了解」档的能力地图。
- 用标准术语（Root Bridge、Root Port、Access 和 Trunk 端口）替代原文比喻，便于以后检索和向 AI 描述。
- 补了原文缺的关键点（以太网帧无 TTL、Trunk 可限定 VLAN、VLAN 不等于完整安全边界），核对无误；用户原来卡住的「Trunk 口是什么」在总结里有答案。

决定：
- [x] 删除 `web-capture-prompt.md`；网页材料改为「summarize page 总结 → 用户读完写 `questions.md`」，SKILL 与 README 同步
- [ ] 用下一篇材料试这个方式，再据结果改 SKILL

试用后要定的规则：
- [ ] 「以材料为界」改为以学习目标 + 用户疑问为界：只展开目标档位需要或用户问到的内容
- [ ] 处理时核对总结里超出原文或存疑的说法，有疑点标出或问用户，不直接写进笔记
- [ ] 「了解」档可直接取总结里的「问题 → 机制」表，剩下的问题只是存放位置（见上节待设计项）
- [ ] 需要「能判断」以上而总结不够时，才补原文

## 2026-10-16 取消 questions.md，改为处理时提问

流程：summarize 总结存入 `inbox/` → 处理时 AI 按需提问 → 按学习目标写入 `roamnotes-v2/` → 按笔记出题并做成 Anki 卡片。

- [x] 新建 `.agents/learning-goals.md`：各领域目标档位与用途，问一次长期使用（网络从 Claude 私有 memory 移入；2026-10-16 用户补充角度与子领域档位：TCP、IP 层为面试「能判断」，VLAN 基本概念与 OpenWRT 常用配置项「了解」（家庭网络），企业组网「不需要」）
- [x] 重写 `inbox-processing`：提问规则（目标、卡点、冲突、个人背景，最多 3 个）与回答记录位置；核对总结；以目标档位和卡点为界；「了解」档合并进领域概览笔记；写完后出题做卡
- [x] AGENTS.md 入库规则、`cc-note-writing`（准入 0a、误解模板）、README 学习流程同步
- [ ] 下一篇材料试用：提问是否太多或太少；「了解」档概览笔记的组织方式；出题做卡的数量和质量

## 2026-10-16 按 cc-agent-instructions 审查后修正

- [x] 统一档位：以 `cc-note-writing` 的「不需要 / 知道 / 能判断 / 能写」为唯一定义（新增「不需要」；「了解」改名「知道」；「能排错」并入「能判断」），`inbox-processing` 与 `learning-goals.md` 只引用
- [x] 通用档位定义里去掉网络领域的偏好（「排障细节交给 AI」只留在 `learning-goals.md`）
- [x] AGENTS.md「在本库里直接学习」参考 `learning-goals.md`
- [x] 出题制卡去重：同一知识点只做一张卡
- [x] AGENTS.md 登记：修改 AGENTS、CLAUDE.md 或仓库 skills 时用 `cc-agent-instructions`
