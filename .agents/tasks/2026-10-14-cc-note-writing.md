# cc-note-writing skill 与 Polars 试点

Status: Paused — pilot reverted, notes to be rewritten later

目标：建立按笔记类型区分的写作规则 skill（`cc-note-writing`），并用它重写 Polars 三篇笔记作为试点，供用户对比新旧版本（旧版本见 Git）。

## 已确定的设计

- 准入测试：第 0 步「需要能写出来吗」，再用第 1–5 步过滤（可检索 / 需在脑中 / 关于我 / AI 易错 / 区分相似选项）。
- 掌握目标三档：知道 / 能判断 / 能写；每类笔记有默认档位，面试准备另作目标。
- 载体分工：笔记管理解，Anki 管回忆，练习管熟练。
- 人机分工：用户写关键内容并标记，AI 不改写；AI 负责整理、补充、版本核对。
- 类型：库 / 工具、语言特性、算法、理论 / 数学、方法 / 实践、经验 / 坑。
- 不引用原始资料；库类笔记标注所核对的版本。

## 检查清单

- [x] 阅读现有 skills、布局约定，确认名称无冲突。
- [x] 起草 `.agents/skills/cc-note-writing/SKILL.md` 与各类型 references。
- [x] 建立 `.claude/skills/cc-note-writing` 软链接，并在 AGENTS.md 登记 skill。
- [x] 在 Polars 2.0.0 上运行验证试点笔记中的代码与 API。
- [x] 按 skill 重写三篇 Polars 笔记（保留 ID、标题、入链）。
- [x] 验证 TOC、Org block、property drawer、链接、中文排版。
- [x] 记录试点发现与 skill 待改进点。

## 进度记录

- 2026-10-14：本地 `uv run --with polars` 安装得到 Polars 2.0.0，试点以此为核对版本。
- 2026-10-14：skill 与 6 个类型模板完成；`.claude/skills/cc-note-writing` 软链接已建，AGENTS.md 已登记。
- 2026-10-14：Polars 三篇按 skill 重写（836 → 479 行），保留 ID、标题和入链；51 处示例在 Polars 2.0.0 上运行通过（弃用警告视为失败）；Emacs 批处理对齐表格、生成 TOC；`org-roam-db-sync` 已执行。
- 2026-10-14：顺带修正 `ankinotes/polars.org` 中两句「The source notes use cut/qcut」（笔记已改用 `bin_*`）。

## 试点发现

- 2.0 的版本漂移：`cut`/`qcut` 弃用，`bin_intervals` 默认左闭，和 `cut` 不同；`DataFrame.corr()` 需要 numpy。
- 原笔记未写的坑：`str.replace` 默认按正则匹配、`unique()` 默认不保序、`concat_str` 遇 null 返回 null、`pivot` 遇重复组合报错。
- 已写回 skill：Emacs 格式化脚本、文件内标题链接写法、检查脚本中弃用警告视为失败。

## 待用户反馈

- 新旧版本对比：`git diff roamnotes-v2/Python/*polars*.org`。
- 三篇都没有 `My Take`（不代写），等用户补充。
- 待验证：各类型模板是否合用；`:mine:` 标签和 `:VERIFIED_WITH:` 属性在 Emacs 和 org-roam-ui 中的显示效果。
- 2026-10-14：用户要求：`* TOC :TOC_N:` 下的条目由其 Emacs 自动生成，AI 不手写、不修改。已写入 AGENTS.md；`format.el` 改为只对齐表格。
- 2026-10-14：用户要求：Anki 卡片中的行内代码用 `~code~`，不用 `=...=`。`ankinotes/polars.org` 已转换（128 处），规则写入 anki-cards skill。
- 2026-10-14：用户要求恢复 Polars 三篇笔记（`git checkout HEAD`），以后重新改造；删除 `scripts/format.el`（不批量对齐表格）。Anki 中两句改回「The source notes use ~cut~/~qcut~」，与恢复后的笔记一致。
