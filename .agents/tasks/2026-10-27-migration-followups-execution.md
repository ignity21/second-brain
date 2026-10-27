# 迁移收尾 B 节执行：复查清单迁入、Unsorted 整理、数学 Deck

Status: Complete — 由 `2026-10-27-migration-followups.md`（B 节）统筹；遗留问题见文末

决定来源见 `2026-10-27-migration-followups.md` A 节和 `2026-10-27-unmigrated-notes-review.md`。源笔记保留在 `roamnotes/`（A3：暂不删除）。

## 用户决定（2026-10-27，本轮开工前）

- `Programming/` 的学习目标：能判断（能讲清绑定、环境、求值规则、闭包、模式匹配、类型推断，并用来分析其他语言的行为；SML 语法本身不记），制概念卡。
- `Personal/` 4 篇：轻度整理（内容基本原样，只改标题、排版和索引），不制卡。

## 归属方案

- *硬件* ：Linux 下的中间索引 `66716bea`（原 CPU and Memory Hardware）改名为 *Computer Hardware* ——这个 ID 本来就是旧 `computer_hardware` 的，加入主板和显示器后旧名不再准确。子节点 3 → 5：
  - *PC Motherboard and Components* （保留 `4baf1454`）：芯片组演变（北桥并入 CPU）、并入 `computer_hardware` 词汇表中的内存控制器、地址总线、时钟；SATA / NVMe；规格；电源；USB；启动链（POST、固件 ROM、BIOS / UEFI）。连接器截图不迁。
  - *Computer Display Panel Types* （保留 `04eccc31`）：LCD（IPS / TN / VA）与自发光面板，修正原笔记把 mini-LED、micro-LED 归入 OLED 的错误。
  - 档位按 Linux 学习目标之外的「知道」处理，不制卡。
- *Python 标准库* ：*Python Standard Library Toolbox* （保留 Python Cookbook 的 `f3b97038`），库类笔记，按场景分组、只写工具名和何时用；接入 Python Language Features（出度 7 → 8）。
- *Programming/* ：新大类。根 `Programming` → 中间索引 *Programming Language Concepts* → *Function Bindings and Calls in ML* （保留 SML 的 `499faa16`，理论类）。按能判断制卡，新 Deck `RoamCards::Programming`。
- *Personal/* ：新大类。根 `Personal` → *Books* （Atomic Habits）/ *Games* （Oxygen Not Included、Total War: Warhammer III、Minecraft Server）。保留 4 篇原 ID 和 Warhammer3 的两个标题级 ID（`6e9cc01b`、`9d17e721`）。图片：缺氧的基地参考截图迁入 `Personal/images/`。
- *Unsorted/* ：删除 `roamtest-20260901.org`；Model vs Effect（`5147c72c`）移到 `Tools/`，改标题，接入 AI Tools（出度 2 → 3）。
- *数学 Deck* ：新建 `RoamCards::LinearAlgebra`、`RoamCards::Statistics`，档位能判断（见 `.agents/learning-goals.md`）。

新 ID：Programming 根 `dbc8ca9e-e151-4c7f-a872-4fb413110858`，Programming Language Concepts `51c2e040-f83a-4679-a5da-f9f25bd692e1`，Personal 根 `cd6561f4-f67b-4e26-81b5-daf7d095c0cd`，Books `13f42fcf-3c5d-4667-9d6b-f083eb3a6979`，Games `fbef54d3-f22a-4c80-a5bb-0d922c5025f6`。

Doom 配置（`~/.config/doom/modules/cc/notes`）按目录动态识别类别，新建大类无需改配置。

## Checklist

- [x] Unsorted 整理
- [x] 硬件两篇 + 索引改名
- [x] Python Standard Library Toolbox
- [x] Programming/ + SML + 卡片
- [x] Personal/ 4 篇
- [x] LinearAlgebra Deck
- [x] Statistics Deck
- [x] 验证（行内标记、TOC、链接、主树）+ `org-roam-db-sync`

## 记录

- 2026-10-27：建立本文件。
- 2026-10-27：完成前 5 项。索引文件 `linux_cpu_memory_hardware.org` 随改名移为 `linux_computer_hardware.org`。硬件、Python 标准库按「知道」不制卡；SML 例子在临时 Poly/ML 5.7.1 容器（ubuntu:24.04）里核对，容器和镜像已删除；`RoamCards::Programming` 8 张。Minecraft 笔记统一了 systemd 单元中前后不一致的目录名（`paper-server` → `paper`）。
- 2026-10-27：完成两个数学 Deck：`RoamCards::LinearAlgebra` 22 张、`RoamCards::Statistics` 29 张（英文，跟随笔记语言）。卡片用到的数值在 NumPy 2.5.4、SciPy 1.18.1 上核对。制卡时修正了笔记中的错误：
  - LinearAlgebra：Eigenvectors 的特征向量一节原本没写完，补上特征向量和 $M^{10}=PD^{10}P^{-1}$；The Hessian 的判别条件只对两个变量成立，改为按特征值判别，并用笔记自己的三元例子作反例；Rotation Matrix 注明该形式对列向量是顺时针旋转；Linear Transformation 中 SVD 的 $U$ 为 $m\times m$；Matrix 的可逆性测试（原为 ~assert LA.inv(M) != 0~ ）、 ~angle30~ 、 ~np.array[[...]]~ 语法。
  - Statistics：Bessel 校正公式缺平方；Pearson 公式缺 $1/n$；Bootstrap 中由 SE 估计总体标准差的代码写反（应为 ~standard_error * np.sqrt(n)~ ）；P-Values 的定义补上「至少同样极端」并说明不是 $H_0$ 为真的概率；T-Test 的 ~std(df=1)~ 、Normal Distribution 的 ~std1~ 笔误。
- 2026-10-27：验证：改动的 Org 文件行内标记检查只剩 Personal 笔记中中文之间的单个 `+` 、 `/` （不构成标记）；所有 ID 和 file 链接存在；新节点唯一主父节点、可从根到达；执行了 `org-roam-db-sync`（临时 daemon，共 475 个节点）。

## 遗留问题（未处理，供以后整理这些笔记时参考）

- Matrix：「Only square matrices can be inversed」下的例子（投影矩阵）语义不清。
- Linear Transformation：SVD 示例代码变量名不一致（~Σ_diag~ 与 ~S_diag~ ），且用 ~==~ 比较数组，应为 ~np.allclose~ 。
- Z-Test：「The variances are known (use bootstrapping)」说法混乱；T-Test 两样本检验用不合并方差的 SE 却配 $n_1+n_2-2$ 的自由度（课程简化，Welch 检验的自由度不同）。
- Data Sampling：聚类抽样示例中 ~sample(n=len(df_pop)//4)~ 对每个组各抽总体的 25%，与注释不符。
