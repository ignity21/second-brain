# 学习流程落地

Status: Done（待用户首次实验反馈）

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
- [ ] 首次实验：用计算机网络一节走完流程，观察是否只记了卡点
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
