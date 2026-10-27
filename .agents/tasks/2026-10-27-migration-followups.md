# 迁移收尾：待决定与待处理事项

Status: Open — 迁移收尾的汇总入口：A、B 节已完成（2026-10-27）；剩 C 节由用户同步 Anki，以及 A3「删除 `roamnotes/` 备份」待用户以后决定

用户说「处理迁移遗留」「迁移收尾」或问「还有什么没处理」时，从这个文件开始。旧笔记迁移（`roamnotes/` → `roamnotes-v2/`）在 2026-10-27 全部完成：`roamnotes/` 中每篇笔记都已迁入、合并，或记入复查清单；各批次的新旧 ID 对应在各迁移任务文件里，最后一轮见 `2026-10-27-remaining-categories-migration.md`。这里只收迁移之后还没做完的事。

## A. 需要用户决定（一次问完）

1. ~~推送~~：已完成（2026-10-27，用户确认后推送到 `origin/master`，`87df866..2536dd9`）。
2. ~~复查清单~~：已决定（2026-10-27），逐篇结果记在 `2026-10-27-unmigrated-notes-review.md` 的 Checklist。
   - C++ 三篇（Literal、 ~std::istringstream~ 、Static Local Variable）不迁；硬件两篇（Motherboard、Computer Display）都迁入，接到 Linux 的 CPU and Memory Hardware 下。
   - 截图或链接类：netcat、Calculus、Git Cheat Sheet、AI Prompts、UML 不迁。Python Cookbook 改写成「工具 → 适用场景」，并扩展到常用标准库工具（collections、itertools、bisect、functools 等），不写具体用法——用户只需知道有哪些工具、什么场景用。SML 迁入，新建大类 `Programming/`（用户认为这门课的内容是理论概念类）。
   - 个人内容：新建 `Personal/`，迁有内容的 4 篇（Atomic Habits、Oxygen Not Included、MC Server、Warhammer3）；Books、Have Fun 两个索引和 English、English Grammar 截图不迁。
   - `Default/computer_hardware` 的 Architecture、Glossary 两节：挑有用的并入（MCC、地址总线、时钟、POST / ROM / UEFI 启动链等与 CPU、Memory Hierarchy 相关的概念）；散热器、导热硅脂、Mb/s 这类不收。
3. ~~删除 `roamnotes/` 备份~~：用户决定暂不删除（2026-10-27），以后再定；本轮不执行清理步骤。
4. ~~C++ 的 2 张旧卡~~：已修改（2026-10-27）。Pointers 无误未动；Pointers to Array 的 Back 改为首元素地址并注明类型，Front 注明最后两行按顺序执行（详见 `2026-10-26-cpp-trading-anki-cards.md`）。
5. ~~还没有 Deck 的大类~~：已决定（2026-10-27），LinearAlgebra、Statistics 都新建 Deck，档位「能判断」；已记入 `.agents/learning-goals.md`。
6. ~~`Unsorted/` 的两篇~~：已决定（2026-10-27），删除 `roamtest-20260901.org`；Model vs Effect 移到 `Tools/`，由 AI Tools 索引收录，标题改得带上下文，保留原 ID。

## B. 可以直接做的（A 节答完后执行）

- [x] *C++ 与 Trading 制卡* ：已完成（2026-10-27），见 `2026-10-26-cpp-trading-anki-cards.md`。C++ 新增 30 张、修正 1 张旧卡；Trading 新建 Deck，25 张。
- [x] *Keycloak 的 ~TODO verify~* ：已完成（2026-10-27）。在临时 Keycloak 26.4.0 容器里验证：User Attribute 映射器会读取组属性（含父组继承），顺序为用户自身 → 最近的组 → 父组；关闭 Aggregate 时只取第一个值，开启后合并成列表。笔记的 Pitfalls 已改写；容器、镜像和测试脚本已清理。
- [x] *两处既有链接问题* （不在迁移范围内，迁移时发现）：已完成（2026-10-27）。notebook 链接改为相对路径并确认文件存在；probability 中两个索引链接改为纯文本「离散分布（discrete distribution）」「连续分布（continuous distribution）」，它们与 Probability 同在 Probability and Distributions 索引下。已执行 `org-roam-db-sync`。
  - `MachineLearning/overfitting_underfitting` 第 44 行用 =file:~/second-brain/notebooks/ML/...= 绝对路径；文件存在，但不符合「相对路径以引用文件为基准」，发布后失效。改为 =file:../../notebooks/ML/plot_learning_curves.ipynb= 。
  - `Statistics/probability` 第 11 行正文链接了两个索引（Discrete Distributions、Continuous Distributions），违反「引用不指向索引」；改为纯文本或指向具体分布。
- [x] 按 A 节的决定执行，每项完成后跑对应验证和 `org-roam-db-sync`：已完成（2026-10-27），详见 `2026-10-27-migration-followups-execution.md`。
  - [x] 硬件：迁入 Motherboard、Computer Display（保留原 ID），并入 `computer_hardware` 两节中挑出的概念，接到 CPU and Memory Hardware 下
  - [x] 新建大类 `Programming/`（同名根索引），迁入 SML（保留原 ID，标题带上下文）；同步 `~/.config/doom/modules/cc/notes` 的类别目录约定（如有）；迁移时问用户该领域的学习目标
  - [x] Python 标准库工具笔记：以 Python Cookbook 的 ID 改写，按场景分组，接入 Python 主树
  - [x] 新建大类 `Personal/`（同名根索引），迁入 Atomic Habits、Oxygen Not Included、MC Server、Warhammer3（保留原 ID）；同步 Doom 配置（如有）
  - [x] `Unsorted/`：删除 `roamtest-20260901.org`；Model vs Effect 移到 `Tools/` 并接入 AI Tools
  - [x] 新建 Deck `RoamCards::LinearAlgebra`、`RoamCards::Statistics`（能判断）

## C. 用户自己操作

- [ ] 把新卡同步到 Anki：新建的 Deck `RoamCards::Algorithms`（30 张）、`RoamCards::SystemDesign`（31 张）、`RoamCards::Tools`（4 张）；`RoamCards::Network` 新增 15 张、改写 3 张（ARP、VLAN、3 层交换机，保留了同步字段）；`RoamCards::Python` 新增 8 张；`RoamCards::C++` 新增 30 张、改写 1 张（Pointers to Array，保留了同步字段）；新建的 Deck `RoamCards::Trading`（25 张）、`RoamCards::Programming`（8 张）、`RoamCards::LinearAlgebra`（22 张）、`RoamCards::Statistics`（29 张）。
- [x] 推送后确认 Publish 工作流部署成功：run 40439719314 的 build、deploy 均成功；线上 `data/graphdata.json` 已包含 Algorithms、System Design、Tools 等新节点（2026-10-27）。

## D. 与迁移无关、仍未完成的计划（只作索引）

- `2026-10-15-learning-workflow.md`：In progress，12 项未完成（入库规则清点、Doom dailies / org-noter 配置、书籍学习流程、收件箱处理方式的若干待设计项）。
- `2026-10-14-cc-note-writing.md`：Paused，Polars 三篇的试点已回退，待以后重写。

## 记录

- 2026-10-27：建立本文件。检查过所有任务文件的 Status 和未勾选项、`ankinotes/` 的 Deck 列表、未推送的提交和 `Unsorted/` 的内容。上次报告的「ML 笔记链接指向不存在的文件」是检查脚本没有展开 =~= 导致的误报，已改为 B 节的路径规范问题。
- 2026-10-27：用户逐个回答了 A2、A3、A5、A6，决定见 A 节；B 节最后一项拆成子项。
