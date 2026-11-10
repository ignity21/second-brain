# 学习路径（Learning 大类）

Status: In progress — 统计学路径待用户试用；Omarchy / mise 路径未开始

用户要为近期学习主题建立由浅入深的阅读顺序，跨大类收录相关笔记。规则写在 AGENTS.md「学习路径」。

## 已定

- 新建 `roamnotes-v2/Learning/` 专用大类，根索引 `learning.org`。
- 不另选目标档位（记笔记时已定），`learning-goals.md` 有则按它取舍。
- 路径随站点发布，供手机阅读；路径笔记加 `:learning:` 标签，可在 org-roam-ui 中过滤。
- 旧笔记问题不批量改：排路径时记为步骤下的「待改」，学到该步时处理（事实错误直接改，重写结合用户卡点）。原因：2026-10-14 的 AI 整篇重写试点被用户撤回。

## 检查清单

- [x] AGENTS.md 增加「学习路径」规则
- [x] `Learning/learning.org` 与 `statistics_learning_path.org`（6 阶段 25 步，含待改项和对应 Anki 卡片）
- [x] TOC、行内标记、ID 存在性检查；`org-roam-db-sync`（682 节点）
- [x] 新建 `README.md`（面向用户的目录与工作流说明）；AGENTS.md 要求工作流变化时同步 README
- [ ] 用户试用统计学路径，按反馈调整格式
- [ ] Omarchy 路径（含 mise；现有笔记少，以「待补」步骤为主）
- [x] 提交并推送后确认 Publish 工作流部署，手机上能看到 Learning 大类

## 2026-11-10 拆分 skill 与检查脚本

- [x] 新 skill：`learning-path`（建路径 + 陪学，含原 AGENTS「入库与学习辅助」的讲解规则和 show-me）、`notes-site`（原 AGENTS「org-roam-ui 发布」+ 推送后确认部署）；`.claude/skills` 链接
- [x] `scripts/check_notes.py`：替代 AGENTS 中的行内标记正则和手工结构检查；在库副本中注入错误验证能检出各类问题
- [x] AGENTS.md 精简（121 → 约 94 行）；README 补检查脚本、skill 列表、Anki 推送
- [x] `anki-cards` 加「推送到 Anki」（`anki-editor-push-notes` 经 `cc-sync` daemon）；已在未改动的 `statistics.org` 上验证无改动
- [ ] `roamnotes/` 清理后删除 `note-migration` skill 及 AGENTS、README 中的提及（时间由用户定）
- [ ] 全库检查的既有问题（2026-11-10）：11 篇缺 TOC，4 处正文链接指向索引（Pandas、Cost Function），`Personal/` 等处行内标记；`ankinotes/datascience.org` 18 张、`elisp.org` 2 张卡有 `ANKI_FAILURE_REASON`
