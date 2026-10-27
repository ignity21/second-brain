# 迁移剩余旧笔记（Default/、Games/）的总计划

Status: In progress — 归属方案已确认（2026-10-27）；批次 1–4 完成，下一步批次 5

C++、Trading、Linux/OS 三轮迁移之后，`roamnotes/` 中从未进入任何迁移计划的笔记共 130 篇（`Default/` 128 篇、`Games/` 2 篇），约 3,700 行；另加复查清单里延后的 `C++/zeromq`。旧根 `Default/contents.org` 不迁（其链接的 ID 均已迁移）。

盘点方法：`roamnotes/` 中文件级 `:ID:` 不在 `roamnotes-v2/` 的笔记，再排除已在 C++ / Trading / Linux 各批任务文件的 `←` 合并表中被吸收的。脚本在 scratchpad（`inv.py`、`inv2.py`），清单 `final.txt`。

## 总体情况

- 内容以碎片为主：一半以上不足 15 行；空笔记或只有链接的旧索引约 25 篇（`sha`、`consistent_hashing`、`shell_sort`、`physical_layer`、`mysql`、`full_text_search_data_model`、`pyside6` 等）；只有一张截图的约 15 篇（`arp`、`dhcp`、`nat`、`netcat`、`ufw`、`k8s`、`git_cheat_sheet`、`english*`、`calculus`、`ai_prompts`）。
- 较长的：`web_application_design`（283 行，6 张 PlantUML 图，源在 `Default/puml/SystemDesign/`）、`anki_tips`（175）、`nftables`（163）、`aider`（117）、`warhammer3`（111）、`ip`（92）、`preorder_traversal`（80，含 Morris 遍历）、`linux_directories`（80）、`ansible`（81）、`dynamic_programming`（76）。
- 新库对这批笔记的入链只有两处：`Linux/linux_benchmarking_load_generation` 指向 `dd` `17daaa09`、`ab` `49b1d0cc`。这批笔记对新库的出链：`error_handling` → RAII `474df27e`、`firewall` / `nftables` → iptables `cee785fb`、`network_troubleshooting` → pktgen `663e9802`、`py_troubleshooting` → VizTracer `5a4eceee`、`languages` → C++ 根，均有效。
- `.agents/learning-goals.md` 只记录了网络、C++、Trading、Linux、Python（性能剖析）、Polars；算法、系统设计、DevOps 等新领域的档位需要用户给出。

## 归属方案与批次

每批独立完成：写笔记、接索引、制卡、验证、提交。顺序先迁入现有大类（规则已定），再做新大类。

### 批次 1：Network 剩余（迁入现有 `Network/`，约 26 篇）

档位按「计算机网络」：IP 层能判断，VLAN 和路由器配置项知道，企业组网不需要。

```
Computer Networking
├─ Fundamentals (13ee1f3a，出度 1 → 4)
│   ├─ Network Layers and Data Units (72d3cced) ← physical / data_link / network / transport / application_layer（各层职责一节）, mtu（并入切分一节）
│   ├─ 新 Ethernet Switching, ARP and VLAN (保留 switchers 的 ID) ← switchers, arp
│   ├─ 新 NAT and DHCP (保留 nat 的 ID) ← nat, dhcp
│   └─ 新 TLS Handshake and Certificates (保留 tls 的 ID 176c3083) ← tls, tls_handshake, ssl_certificate（原文是 TLS 1.2 RSA 密钥交换，改写时补 1.3 / ECDHE）
├─ Linux Kernel Networking (1921bccf，出度 2 → 3)
│   ├─ Linux Netfilter and iptables (cee785fb) → 改为 Linux Netfilter: iptables, nftables and ufw ← firewall, nftables, ufw
│   └─ 新 Linux Routing and Policy Routing (保留 ip_route 的 ID) ← ip_route, ip_rule, ip 的 route / neigh 部分
└─ Tools (ca95e333 Linux Network Tools)
    ├─ Network Performance Testing (87bbc997) ← network_troubleshooting（指标一节）, hping3
    └─ ip、netcat、gost：并入 Linux Network Tools 的工具表或单列，执行时按内容决定；gost 是自用代理，可能只留一段
```

- `dd`、`ab`：不迁。Linux Benchmarking 已写了二者的用法和坑，把那两处 ID 链接改成纯文本。
- 制卡写入 `ankinotes/network.org`。

### 批次 2：算法与数据结构（新大类 `Algorithms/`，约 37 篇）

```
Algorithms (保留 algorithm 的 ID)
├─ Data Structures (data_structure) ← linked_list（+ floyd 快慢指针）, stack, queue（循环队列、阻塞 / 并发队列）, heap, 二叉树遍历（tree, tree_traversal, preorder, inorder, postorder；Morris 遍历一节）
├─ Sorting Algorithms (sorting_algorithm) ← bucket / counting / radix / shell_sort（线性排序一篇）
├─ Algorithm Design Paradigms ← recursion, backtracking（去重套路）, greedy, dynamic_programming
├─ astar_search（截图为主，改写或只留一段）
└─ LeetCode Techniques (leetcode) ← lt287, negative_marking, kmp（只有视频链接）
```

- `hashing`、`sha`、`consistent_hashing`（空）、`rendezvous_hashing`：分布式场景的哈希放批次 3 的分片笔记；`sha` 不迁。
- 档位：面试刷题能判断（见 learning-goals）。

### 批次 3：系统设计与数据库（新大类 `SystemDesign/`，约 33 篇）

```
System Design (保留 system_design 的 ID；其 → ZeroMQ 的入链随 ZeroMQ 归属处理)
├─ Design Goals ← reliability, availability, scalability, maintainability, data_system, 软件架构设计原则, error_handling（→ C++ RAII 的引用保留）
├─ Data Storage (database) ← sql（ACID）, no_sql / mongodb / mysql（空，废弃）, document_model, graph_like_data_model,
│                             b_trees, lsm_trees, hash_indexes（合成一篇存储引擎）, replication, sharding（+ consistent / rendezvous hashing）
├─ Distributed Systems ← load_balancing, leader_election, mapreduce, mongodb_mapreduce
├─ Messaging ← pub_sub_pattern, polling, streaming, ZeroMQ 三篇（C++/zeromq 保留 5521b2f9，Default/zeromq 截图改写）
└─ Web Application Design (system_design_interview 并入) ← web_application_design（6 张 PlantUML 图重渲染进 `SystemDesign/images/`）
```

- `low_latency`：并入 Trading 的 Low Latency Trading Design（内容是 Linux / C++ / 网络调优清单，与之重叠）。
- `nginx`、`keycloak`：归批次 5 的 Tools / DevOps。
- 数据库是否单独成大类：笔记合并后预计 4–5 篇，先放 SystemDesign 下。

### 批次 4：Python 与零散归属（迁入现有大类，约 12 篇）

- Python：`dictionary`（dict 的紧凑哈希表实现）→ Python Language Features 下新笔记或并入现有；`import_system` → 新笔记 Python Import System；`py_troubleshooting` → Python Profiling 或 Development Practices（icecream / PySnooper / hunter，「知道」）；`sqlalchemy` → Python Third-Party Libraries；`python_cookbook` 只有 collections / heapq 用法，不迁；`python_modules`（旧索引）、`pyside6`（空，新库已有 PySide6）不迁。
- Linux：`linux_directories`（FHS）→ Linux System Administration and Shell 下，「知道」档。
- Trading：`出入金流程` → Trading 的 Securities and Exchange Mechanics 或 Cryptocurrency Trading 附近，个人操作记录。
- 数学：`calculus`（截图）、`multivariate_derivative`（多元链式法则两行）→ 并入 LinearAlgebra 的 Matrix Calculus。
- `languages`（旧索引）不迁；`sml`（Coursera Programming Languages 课的语法摘录）→ `Unsorted/` 或不迁。

### 批次 5：DevOps、工具、前端（新大类 `Tools/`，约 21 篇）

DevOps、个人工具、前端作为 `Tools/` 下的分组，全部「知道」档，命令和截图大量删减，基本不制卡。

- DevOps：`devops`（索引）、`ansible`、`docker`、`docker_troubleshooting`（nsenter）、`k8s`（截图）、`nginx`、`keycloak`、`opencat`（自建服务的 docker 命令）、`uml`（一个外链）。
- 工具：`git_cheat_sheet`（截图）、`zotero`（设置记录）、`anki_tips`（175 行，含 20 rules 和模板技巧）、`ai_tools`（索引）、`ai_prompts`（截图）、`aider`（117 行；`Unsorted/` 已有另一篇 Aider，30 行安装配置，迁移时合并）。
- 前端：`frontend`、`html`、`html_examples`、`html_header`、`html_layout`、`meta_tag`、`css`，合计约 180 行，HTML / CSS 入门摘录，合并后 1–2 篇。

### 批次 6：个人内容（8 篇）— 不迁

用户决定不迁，已列入 `2026-10-27-unmigrated-notes-review.md`。
`atomic_habits`、`books`、`english`、`english_grammar`（截图）、`have_fun`、`oxygen_not_included`、`Games/mc_server`、`Games/warhammer3`。

## 已确认（2026-10-27）

- [x] 算法：建 `Algorithms/`，面试刷题能判断
- [x] 系统设计：建 `SystemDesign/`（数据库作其中一组），面试能判断
- [x] DevOps / 工具 / 前端：建一个 `Tools/` 大类，「知道」档
- [x] 个人内容：不迁，列入复查清单

## Checklist

- [x] 用户确认归属方案和档位，写入 `.agents/learning-goals.md`
- [x] 批次 1：Network 剩余（2026-10-27）
- [x] 批次 2：Algorithms（2026-10-27）
- [x] 批次 3：SystemDesign（2026-10-27）
- [x] 批次 4：Python 与零散归属（2026-10-27）
- [ ] 批次 5：DevOps、工具、前端
- [x] 批次 6：个人内容（不迁，已列入复查清单）
- [x] 复查清单 `2026-10-27-unmigrated-notes-review.md` 中的 ZeroMQ 随批次 3 处理

## 批次 1 执行记录（Network）

新笔记与合并：

| 新笔记 | ID | 吸收的旧笔记 |
|---|---|---|
| Ethernet Switching, ARP and VLAN | `5dd548b6`（原 switchers） | switchers、arp（`84b36379` 废弃） |
| NAT and DHCP in Home Networks | `42efb840`（原 nat） | nat、dhcp（`e38ec05a` 废弃） |
| TLS Handshake and Certificates | `176c3083`（原 tls） | tls、tls_handshake（`9699bb2e`）、ssl_certificate（`eeb31a4c`），后两个废弃 |
| Linux Routing and Policy Routing | `e29921b0`（原 ip_route） | ip_route、ip_rule（`9b34dbd7`）、ip（`6f61b842`），后两个废弃 |
| GOST Proxy Tunnels | `4cfade54`（原 gost） | gost |

并入现有笔记：
- Network Layers and Data Units ← 五篇分层笔记（链路层只检错，改为误解一节）、mtu（新增「MTU 不一致时」：PMTUD、黑洞、MSS clamping）。分层笔记 ID 均废弃。
- Linux Netfilter and iptables → 改名 *Linux Netfilter, iptables and nftables* ← firewall（索引，废弃）、nftables（`df7a26d0` 废弃；新增 nftables 一节和「多个 base chain 时 accept 不是最终结果」）、ufw（`684bdb05` 废弃）。
- Network Performance Testing ← network_troubleshooting（使用率、Web 服务指标；`d53d47ee` 废弃）、hping3（已有，`a07e73bd` 废弃）。

不迁：`netcat`（只有一张速查截图，可随时查询）；`dd`、`ab`（Linux Benchmarking 已有其用法，那里的两处 ID 链接改为纯文本）。所有废弃 ID 在迁移范围外都没有入链。

纠正的旧说法：三层交换机带 NAT（实际一般没有）；链路层纠错（以太网只检错）；TLS 握手中客户端用公钥加密 premaster secret（是 TLS 1.2 RSA 密钥交换，1.3 已删除）。

核对（scratchpad `tls/`、用户命名空间）：iproute2 7.2.0 中源地址策略路由与最长前缀匹配、规则指向的表无匹配路由时回落到下一条规则；nftables 1.1.7 中两条 input base chain（priority 0 accept、10 drop）时 ping 被丢弃；OpenSSL 3.6.5 只配叶子证书时校验返回 21、补中间证书后 0、主机名不符返回 62，TLS 1.3 协商组 =X25519MLKEM768= ；本机 sysctl：~rp_filter~ 由 systemd =50-default.conf= 设为 2，conntrack 超时 432000 / 30 / 120。邻居表 ~gc_thresh*~ 在容器的网络命名空间中不可见，写上游默认值。GOST 未安装，用户配置未运行。

Anki（`ankinotes/network.org`）：改写 ARP、VLAN、3 层交换机 3 张已有卡（保留同步字段，修正三层交换机卡的 NAT 说法），新增 15 张。

验证：行内标记检查为空；TOC（ARP、Netfilter 两篇加 ~TOC_1~ ）已生成；PlantUML 4 张图已渲染；全库 ID、标题、别名无重复，链接目标存在，主树唯一父节点、可达；`org-roam-db-sync` 完成（537 个节点）。

## 批次 2 执行记录（Algorithms）

新大类 `Algorithms/`，根索引 Algorithms 沿用旧 `algorithm` 的 ID `09857801`（其两个标题级 ID 废弃）。

```
Algorithms (09857801)
├─ Data Structures for Algorithms (92ec20d3，原 data_structure)
│   ├─ Linked List Techniques (f40d4fa6) ← linked_list, floyd_s_cycle_finding_algorithm（b3b36188 废弃）
│   ├─ Stacks and Queues (4b726816) ← stack, queue（571dac23 废弃）
│   ├─ Heaps and Priority Queues (6bda11af) ← heap, sorting_algorithm 的「多路归并」TODO
│   └─ Binary Tree Traversal (d1d44f25) ← tree_traversal, tree（1f50f329）, preorder（9e22e9d1，Morris 标题 60aec15c）, inorder（c38e1fa9）, postorder（cb25d06b），均废弃
├─ Sorting and Searching Algorithms（新 5327de41）
│   ├─ Sorting Algorithms (8426d96d) ← sorting_algorithm（4 个标题级 ID 废弃）, bucket / counting / radix / shell_sort（均废弃）
│   └─ A* Search (2b951be4) ← astar_search
├─ Algorithm Design Paradigms（新 e6313ffb）
│   ├─ Recursive Problem Solving (c2cf012a) ← recursion
│   ├─ Backtracking (3c0f22b4) ← backtracking
│   ├─ Greedy Algorithms (836f3c49) ← greedy_algorithm
│   └─ Dynamic Programming (0361445c) ← dynamic_programming
└─ LeetCode Problem-Solving Techniques（新 2a5c55d1）
    ├─ Array In-place Techniques (796f0cbe，原 leetcode；2 个标题级 ID 废弃) ← leetcode, lt287（37465830）, negative_marking（00d69c0f），后两个废弃
    └─ KMP String Matching (be7a4b6e) ← kmp（原只有视频链接，补写前缀函数与匹配模板）
```

- 所有废弃 ID 在迁移范围外没有入链（唯一的外部入链是 `contents.org` → 旧根）。
- 资源：旧截图（A* 课程结构图、启发函数手绘、回溯树、树遍历、链表插入示意）不迁；回溯树改用 PlantUML 重画（`images/backtracking_tree.png`），A* 课程的结构改写为 Pitfalls 中的两条。`roamnotes/assets/Algorithm/` 无需迁移。
- 补充与纠正：排序表补最坏情况和空间，基数排序空间改为 O(n + k)；后序遍历的 deepcopy 写法改为 ~prev~ 指针变体；贪心补交换论证和硬币反例；DP 补完全背包、组合数 / 排列数的循环顺序；LT287 各解法补「是否修改数组」一列。
- 核对：14 个 Python 代码块在 Python 3.14.8 上以 ~warnings.simplefilter("error")~ 运行通过（ ~scratchpad/runblocks.py~ ）；默认递归上限 1000、超过抛 ~RecursionError~ 已实测。

Anki：新建 `ankinotes/algorithms.org`（Deck `RoamCards::Algorithms`），30 张。

验证：行内标记检查为空；9 篇加 ~TOC_1~ 并生成；全库结构检查通过；`org-roam-db-sync` 完成。

## 批次 3 执行记录（SystemDesign）

新大类 `SystemDesign/`，笔记用英语（源笔记多为 DDIA、System Design Interview 的英文摘录）；错误处理一篇源笔记是中文，保持中文。

```
System Design (882501dd，原 system_design；4 个标题级 ID 废弃)
├─ System Design Goals（新 10d96252）
│   ├─ Reliability and Availability (28a88260) ← reliability, availability（bf48570b 废弃）
│   ├─ Scalability in System Design (45f0ae67) ← scalability
│   ├─ Maintainability and Architecture Principles (b5ea1dbf) ← maintainability, 软件架构设计原则（6ed2ea7c）, data_system（665b238c），后两个废弃
│   └─ Error Handling Design (b4fd80ae) ← error_handling（→ C++ RAII 的链接保留）
├─ Data Storage in System Design（新 581d29e4）
│   ├─ Data Models: Relational, Document and Graph (6de26b38，原 database；3 个标题级 ID 废弃) ← database, no_sql, mongodb, mysql, document_model, graph_like_data_model, full_text_search_data_model（后 6 个 ID 废弃）
│   ├─ Database Transactions and Isolation (33927767，原 sql；2 个标题级 ID 废弃) ← sql（补隔离级别与异常）
│   ├─ Storage Engines: Hash Indexes, LSM-Trees and B-Trees (8e0d2181，原 b_trees) ← b_trees, lsm_trees（25329cd5）, hash_indexes（26bfc8e3）
│   ├─ Database Replication (54f046db) ← replication, leader_election（e2798f28）, web_application_design 的主从复制一节
│   └─ Database Sharding and Consistent Hashing (3f815adf) ← sharding, consistent_hashing（3237b43a）, rendezvous_hashing（9fe0a1a4）, hashing（87987610）
├─ Distributed System Building Blocks（新 88d8cbc5）
│   ├─ Load Balancing (1d92f19c) ← load_balancing
│   ├─ Caching Strategies in System Design（新 e6126815）← web_application_design 的缓存与 CDN 两节
│   ├─ Message Queues and Pub/Sub (5561dbba) ← pub_sub_pattern, polling（6e803f5c）, streaming（c009f066）
│   ├─ ZeroMQ Messaging Patterns (5521b2f9，原 C++/zeromq) ← C++/zeromq, Default/zeromq（b09fb519 废弃；7 张 zguide 截图改写为模式表和拓扑列表）
│   └─ MapReduce Batch Processing (8f34f2a8) ← mapreduce, mongodb_mapreduce（da5d484d）
└─ System Design Interview (bed8b081)
    └─ Scaling a Web Application (66b1a5a2) ← web_application_design（6 个 PlantUML 块迁入 `images/web_*.png` 并重新渲染；单机图中「服务器把 IP 返回给浏览器」改为 HTTP 请求）
```

- 不迁：`sha`（空）。
- `low_latency` → 并入 Trading 的 Low Latency Trading Design（新增 NUMA 本地内存、SIMD 两条，链接 Linux 笔记）；其余条目（剖析工具、大页、核绑定、实时调度、Nagle、内核旁路）已在 Trading / Linux / Network 笔记中，ID `e7e8f2c3` 废弃。
- 所有废弃 ID 在迁移范围外没有入链；`Default/system_design` → ZeroMQ 的入链随本批迁移恢复。
- 核对：一致性哈希与 rendezvous 代码在 Python 3.14 上运行，4 → 5 个节点时取模移动 80%、一致性哈希 17%、rendezvous 20%；MapReduce 词频示例运行通过；ZeroMQ（pyzmq 27.2.0 / libzmq 4.3.5，scratchpad `zmq/check.py`）：SUB 连接后立即发送的 5 条全部丢失、200 ms 后的能收到；HWM 设为 10 时 PUB 0.09 s「发出」10 万条、SUB 收到 710 条；无对端的 PUSH 在 ~NOBLOCK~ 下返回 ~zmq.Again~ ；REQ 未收回复就再发报错。

Anki：新建 `ankinotes/systemdesign.org`（Deck `RoamCards::SystemDesign`），31 张（英语 29、中文 2）。

验证：行内标记检查为空；3 篇 TOC 已生成；全库结构检查通过；`org-roam-db-sync` 完成。

## 批次 4 执行记录（Python 与零散归属）

| 旧笔记 | 去向 |
|---|---|
| dictionary `6694ff04` | 新笔记 Python dict and set Internals，接在 Python Language Features 下（出度 5 → 7，另一篇是下一行） |
| import_system `6efd9059` | 新笔记 Python Import System，同上；原图片链接 `file:.../resources/...` 本就失效，不迁 |
| py_troubleshooting `949864f8` | 新笔记 Python Debugging Tools（「知道」档），接在 Python Development Practices 下（5 → 6），引用 Python Profiling 的 VizTracer 标题节点 |
| sqlalchemy `65ffd859` | 新笔记 SQLAlchemy，接在 Python Third-Party Libraries 下（5 → 6）；原示例是 1.x API，改写为 2.x 并加版本漂移表 |
| linux_directories `fae08b2e` | 新笔记 Linux Filesystem Hierarchy，接在 Linux System Administration and Shell 下（6 → 7）；改正 =/user= 笔误和「Unix System Resources」的说法，补 merged /usr |
| multivariate_derivative `a6bfbb45` | 并入 LinearAlgebra 的 The Jacobian（新增 Multivariate Chain Rule 一节，并把原有公式左边的 f(x, y) 改为 df/dt），ID 废弃 |
| 出入金流程 `b09d29da` | 并入 Trading 的 Cryptocurrency Trading，作为「我的出入金路线（2026-06） :mine:」一节（用户自己的路线，原样保留），ID 废弃 |
| python_modules、pyside6、languages、calculus（索引）| 不迁：旧索引或空笔记；calculus 的速查截图列入复查清单 |
| python_cookbook、sml | 不迁，列入复查清单 |

核对（CPython 3.14.8）：dict 在第 1、6、11、22、43、86、171 次插入时扩容（ ~sys.getsizeof~ ），set 在第 5、19、77 次；import：本机 ~sys.meta_path~ 为 DistutilsMetaFinder（setuptools 注入）、BuiltinImporter、FrozenImporter、PathFinder，path hooks 为 zipimporter 与 FileFinder，脚本方式运行相对导入报错、 ~-m~ 正常，本地 =json.py= 遮蔽标准库；SQLAlchemy 2.1.6 / pandas 3.1.0（scratchpad `sqla/check.py`）：无 ~table_names~ 、字符串执行报 ~ObjectNotExecutableError~ 、 ~connect()~ 不提交即回滚、 ~read_sql_table~ 传查询报 ~ValueError~ ；merged /usr：本机 =/bin= 、 =/sbin= 、 =/var/run= 均为符号链接。

Anki：`ankinotes/python.org` 新增 8 张（dict、import、SQLAlchemy）。Debugging Tools、Filesystem Hierarchy 是「知道」档，不制卡；链式法则所在的 LinearAlgebra 没有 Deck，本批不新建。

验证：行内标记检查为空（ =decorator= 笔记中「函数/类」的旧误报除外）；全库结构检查通过；`org-roam-db-sync` 完成。
