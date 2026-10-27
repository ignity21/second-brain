# 迁移收尾：待决定与待处理事项

Status: Open — 迁移收尾的汇总入口：等用户一次性回答 A 节的问题，然后执行 B 节

用户说「处理迁移遗留」「迁移收尾」或问「还有什么没处理」时，从这个文件开始。旧笔记迁移（`roamnotes/` → `roamnotes-v2/`）在 2026-10-27 全部完成：`roamnotes/` 中每篇笔记都已迁入、合并，或记入复查清单；各批次的新旧 ID 对应在各迁移任务文件里，最后一轮见 `2026-10-27-remaining-categories-migration.md`。这里只收迁移之后还没做完的事。

## A. 需要用户决定（一次问完）

1. *推送* ：本地有 6 个未推送的提交（`223171f` 计划，`576a8bb`…`cac7790` 批次 1–5）。推送后 Publish 工作流会把新大类 Algorithms、SystemDesign、Tools 发布到笔记站。选项：现在推送 / 先自己在 Emacs 里看过再推。
2. *复查清单* （`2026-10-27-unmigrated-notes-review.md`，21 篇 + 1 处部分内容）：逐篇决定迁入还是确认不迁。可以按组回答：
   - 已迁大类里跳过的 5 篇：Literal、 ~std::istringstream~ 、Static Local Variable（C++）；Motherboard、Computer Display（硬件）。ZeroMQ 已处理。
   - 截图或链接类 7 篇：netcat、Python Cookbook、SML、Calculus、Git Cheat Sheet、AI Prompts、UML。
   - 个人内容 8 篇：Atomic Habits、Books、English、English Grammar、Have Fun、Oxygen Not Included、MC Server、Warhammer3。要迁的话需要新建个人类别（如 `Personal/`）。
   - `Default/computer_hardware` 中未迁的 Architecture、Glossary 两节。
3. *删除 `roamnotes/` 备份* （61 MB，含 `Default/puml/SystemDesign/`、各类 `images/`、`assets/`）：什么时候删；复查清单里决定不迁的笔记是一起删还是先留着。删除按 note-migration skill 的清理步骤，先查剩余引用。
4. *C++ 的 2 张旧卡* （`ankinotes/cpp.org` 的 Pointers、Pointers to Array）：Back 中「ptr 是 address of array」应为首元素地址； ~*(++ptr)~ / ~*(ptr++)~ 的说明依赖执行顺序。是否按此修改（详见 `2026-10-26-cpp-trading-anki-cards.md`）。
5. *还没有 Deck 的大类* ：LinearAlgebra、Statistics 没有卡片文件（批次 4 并入 The Jacobian 的多元链式法则因此没制卡）。是否新建 Deck 制卡，深度按什么档位（`.agents/learning-goals.md` 中没有这两个领域的记录）。
6. *`Unsorted/` 的两篇* ：`roamtest-20260901.org`（标题 Roamtest 20260901，看起来是测试笔记）是否删除；`model_vs_effect-20260802.org`（LLM 模型选择与努力程度的设置建议）是否归入 Tools 的 AI Tools。

## B. 可以直接做的（A 节答完后执行）

- [ ] *C++ 与 Trading 制卡* ：`2026-10-26-cpp-trading-anki-cards.md`，Status 仍是 Not started。C++ 约 25–30 张（取决于 A4），Trading 约 20 张（新建 `ankinotes/trading.org`，目前不存在）。按 note-migration skill，这是两次迁移的最后一步。
- [ ] *Keycloak 的 ~TODO verify~* ：「User Attribute 映射器是否读取用户所在组的属性」。用 Docker 起一个临时 Keycloak，建组、加属性、看 token，再改笔记。
- [ ] *两处既有链接问题* （不在迁移范围内，迁移时发现）：
  - `MachineLearning/overfitting_underfitting` 第 44 行用 =file:~/second-brain/notebooks/ML/...= 绝对路径；文件存在，但不符合「相对路径以引用文件为基准」，发布后失效。改为 =file:../../notebooks/ML/plot_learning_curves.ipynb= 。
  - `Statistics/probability` 第 11 行正文链接了两个索引（Discrete Distributions、Continuous Distributions），违反「引用不指向索引」；改为纯文本或指向具体分布。
- [ ] 按 A 节的决定执行：迁入复查清单中选中的笔记、删除备份、整理 `Unsorted/`，每项完成后跑对应验证和 `org-roam-db-sync`。

## C. 用户自己操作

- [ ] 把新卡同步到 Anki：新建的 Deck `RoamCards::Algorithms`（30 张）、`RoamCards::SystemDesign`（31 张）、`RoamCards::Tools`（4 张）；`RoamCards::Network` 新增 15 张、改写 3 张（ARP、VLAN、3 层交换机，保留了同步字段）；`RoamCards::Python` 新增 8 张。
- [ ] 推送后确认 Publish 工作流部署成功（AGENTS.md「org-roam-ui 发布」）。

## D. 与迁移无关、仍未完成的计划（只作索引）

- `2026-10-15-learning-workflow.md`：In progress，12 项未完成（入库规则清点、Doom dailies / org-noter 配置、书籍学习流程、收件箱处理方式的若干待设计项）。
- `2026-10-14-cc-note-writing.md`：Paused，Polars 三篇的试点已回退，待以后重写。

## 记录

- 2026-10-27：建立本文件。检查过所有任务文件的 Status 和未勾选项、`ankinotes/` 的 Deck 列表、未推送的提交和 `Unsorted/` 的内容。上次报告的「ML 笔记链接指向不存在的文件」是检查脚本没有展开 =~= 导致的误报，已改为 B 节的路径规范问题。
