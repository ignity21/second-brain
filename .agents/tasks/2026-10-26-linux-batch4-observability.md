# Linux 迁移批次 4：观测与排障方法

Status: Complete

总计划见 `2026-10-26-next-linux-os-migration.md`，上一批见 `2026-10-26-linux-batch3-files-io.md`。源笔记保留。

## 现状

- 17 篇约 440 行，多为「Linux 性能优化实战」课程的摘抄：指标定义 + 工具名单。`performance_optimization` 只有一个链接；`process_troubleshooting`、`short_period_process`、`system_troubleshooting` 各十行左右；`proc`、`proc_pid` 重复（同一份 =/proc/<pid>/= 文件列表）；`system_error` 的 errno 内容已在批次 1 的 Linux System Calls 中。
- 范围外入链（已迁移的旧根 `linux`、旧 `i_o`、`contents.org` 不计）：`system_limits` `505fb55e` ← `system_time`（批次 6）；`proc_zoneinfo` `b879e051` ← `cpu_hardware`（批次 8，NUMA 一节的 Zone）。其余 ID 只有本批内部入链。
- 本批旧笔记的出链：Context Switching `706d7e91`、Interrupt `18ebf2c0`、=/proc/interrupts= 标题 `3158f50d`、Garbage Collection（现 Linux Memory Reclaim）`065d6f74`，均已迁移；工具笔记 top、pidstat、perf、strace、pstree、execsnoop、Common Tools 属批次 5，按批次 1 的做法改为纯文本。
- 学习目标：性能排障「从现象到指标到工具的判断链」为「能判断」，工具本身只到「知道」。

## 归属与调整

- 全部归 `Linux/`，新建中间索引 Linux Observability and Troubleshooting（新 ID `8a6eab8f`），接到根下。旧 `performance_optimization` 只是分组页、无范围外入链，废弃。
- 每类资源一篇「指标 + 判断链 + 坑」，不再按「指标 / 排障 / 优化」拆三篇：判断时三者要一起看。
- `proc_zoneinfo`（`b879e051`，有批次 8 入链）放到 Linux Memory Reclaim 的水位线一节，该节改为标题级节点 Linux Memory Zones and Watermarks，补一句 zone 的划分。
- `system_limits`（`505fb55e`，有批次 6 入链）扩展为 Linux Resource Limits：rlimit、sysctl 全局上限、cgroup、编译期常量与 ~sysconf~ ，以及「错误码 → 撞了哪个限制」。`system_error` 的资源类错误并入这里，其余（errno、 ~EINTR~ ）已在 System Calls，ID 废弃。
- `short_period_process`（`35d07be4`）：批次 1 预想作为标题级节点保留，但它唯一的入链来自本批的 `process_troubleshooting`，按迁移规则废弃 ID，内容并入 CPU 笔记的一节。

## 目标树

17 篇 → 6 篇笔记 + 1 个索引；另改 Linux Memory Reclaim 的一节。

```
Linux (4f8f2615)
├─ Linux Processes / Scheduling and Kernel Entry / Memory / Files and I/O
└─ Linux Observability and Troubleshooting (新 8a6eab8f)
    ├─ Linux Performance Troubleshooting Method (system_troubleshooting fa3e0959)
    │     ← process_troubleshooting, performance_optimization
    ├─ Linux CPU Performance Analysis (cpu_metrics 00e92d55) ← cpu_troubleshooting, short_period_process
    ├─ Linux Memory Performance Analysis (memory_metrics 0696af2e) ← memory_troubleshooting，批次 2 留下的 memory_leak 主题
    ├─ Linux I/O Performance Analysis (i_o_metrics f44727ab) ← i_o_troubleshooting, i_o_optimization
    ├─ Linux /proc and sysctl Interfaces (proc 8e974bc1) ← proc_pid, proc_sys
    └─ Linux Resource Limits (system_limits 505fb55e) ← system_error 的资源类错误
Linux Memory Reclaim 中：Linux Memory Zones and Watermarks (proc_zoneinfo b879e051)
```

出度：根 5，Observability 6（批次 5 的工具地图若也放这里，到 7–8 时评估拆分）。深度 3。

笔记间横向链接（单向，使用方 → 被使用方）：

- 本批内：Method → CPU / Memory / I/O 三篇（按资源进入）；CPU → I/O（iowait 转 I/O）；Resource Limits → /proc and sysctl（怎么改 sysctl）。
- 指向已迁移笔记（观测 → 机制）：CPU → Process States（平均负载、D）、Context Switching、Interrupts and Softirqs、CPU Scheduling and Affinity；Memory → Virtual Memory（RES / PSS）、Memory Reclaim、Memory Allocation（泄漏与碎片）、Page Cache；I/O → Page Cache、Block Layer、File System Structure（删除仍打开的文件、inode 耗尽）、Buffering（批量 fsync）、I/O Models（io_uring）；Resource Limits → File Descriptors（ ~EMFILE~ ）、Process Address Space（栈上限）。
- 已迁移笔记不反向链接。

## 改造原则

- 补核心模型（能判断）：
  - 方法：USE（利用率 / 饱和度 / 错误）逐资源检查；先整体再进程再线程再函数；on-CPU 与 off-CPU 两类慢；平均值掩盖单核和尖峰；保持复现；观测工具本身的开销（strace）。
  - CPU：平均负载是 R + D 任务数的指数衰减平均，与核数比较；负载与使用率的组合判断；=/proc/stat= 各列（guest 已计入 user）；iowait 是空闲的一种、不可靠；steal；饱和度看运行队列等待时间（ =schedstat= 、PSI）；单核打满被平均值掩盖；短时进程导致 top 看不到；IPC。
  - 内存：procps 4 的 =used= = total − available；available 的含义；内存去哪了（进程匿名、页缓存、Shmem、slab 不可回收、大页）；压力信号（缺页、si / so、直接回收、PSI、OOM 日志）；泄漏 vs 碎片 vs 缓存增长。
  - I/O：IOPS / 吞吐 / 延迟 / 队列深度与按负载选指标；=%util= 对 SSD 不代表饱和；await 含块层排队；判断链（空间与 inode → 是否命中缓存 → 设备 → 进程 → 文件和调用）；=/proc/<pid>/io= 的 =rchar= 与 =read_bytes= ；优化手段的判断（顺序化、批量 fsync、mmap 不一定更快、ionice 只对 BFQ / mq-deadline 有效）。
  - /proc 与 sysctl：按问题查哪个文件的能力地图，=/proc/sys= 与 =/sys= 的分工，临时与永久设置（ =sysctl.d= ），网络命名空间与容器中的 sysctl。
  - 限制：soft / hard、继承、 =limits.conf= 只对 PAM 登录会话生效、systemd 服务用 ~LimitNOFILE=~ ；错误码到限制的对照表；不硬编码 ~PATH_MAX~ 等，用 ~sysconf~ / ~getconf~ 。
- 删去：top / pidstat 等工具的选项（批次 5 处理）、 =/proc= 文件的完整清单、 ~perror~ / ~strerror~ 示例代码、 =/proc/stat= 原始输出。
- 图（PlantUML）：排障流程图（Method）。

## 已发现的旧笔记错误（已核对，新笔记已改正）

- 「平均负载是单位时间内的平均进程数」：是 R + D 任务数的指数衰减平均，按线程计。
- 「磁盘使用率超过 80% 通常意味着瓶颈」「饱和度 100% 时磁盘无法接受新的请求」：只对一次服务一个请求的机械盘成立；SSD / NVMe / RAID 的 =%util= 100% 可能远未饱和，饱和看排队。
- 「CFQ 调度器时用 ionice 调整优先级」：CFQ 在 5.0 移除；现在只有 BFQ 和 mq-deadline 处理 I/O 优先级（本机 6.5 的 mq-deadline 有 =prio_aging_expire= ），NVMe 默认 =none= 。
- 「频繁读写同一块磁盘时用 mmap 代替 read/write 减少拷贝」：不一定更快（缺页、何时读盘不可控、 ~SIGBUS~ ），改写为适用条件。
- 「 ~strace -P [PID]~ 」：按 PID 跟踪是 ~-p~ ， ~-P~ 是按路径过滤。
- 「used：已使用内存（包括共享内存）」：procps-ng 4 起 used = total − available（本机核对）。
- 「RES 不包括 Swap 和共享内存」：RES 包含已驻留的共享内存页（批次 2 核对 =VmRSS= = =RssAnon= + =RssFile= + =RssShmem= ）。
- 「swappiness 范围 0–100，桌面推荐 10」：5.8 起 0–200；「推荐 10」是经验说法，不写（swappiness 已在批次 2 的 Reclaim 中）。
- 「永久修改：写 =/etc/sysctl.conf= 再 ~sysctl -p~ 」：systemd 系统读 =/etc/sysctl.d/*.conf= ， ~sysctl -p~ 只读 =/etc/sysctl.conf= ，Arch 默认没有这个文件。
- 拼写： ~pipstat~ → ~pidstat~ ， ~getconf AGR_MAX~ → ~ARG_MAX~ ， =/proc/stats= → =/proc/stat= 。

## Checklist

- [x] 核对（scratchpad `linux4/`）：procps-ng 4.0.7 的 used = total − available、buff/cache = Buffers + Cached + SReclaimable；meminfo 各项合计 30.1 GB / total − free 30.6 GB；两个死循环绑同一核 3 秒，schedstat 运行 1.50 s、等待 1.50 s，PSI cpu =some avg10= 0.02 → 9.99；系统级 cpu =full= 为 0；=/proc/<pid>/io= 热读 64 MiB =read_bytes= 0、冷读 53 MiB；=kernel.task_delayacct= 0；mq-deadline 有 =prio_aging_expire= ；根分区 relatime；软限制 16 时第 14 次 open 返回 ~EMFILE~ ；ARG_MAX 2 MiB → ~ulimit -s 16384~ 后 4 MiB；单个参数 131,071 字节可 exec、131,072 返回 ~E2BIG~ ；zone：DMA / DMA32 / Normal 单节点。sysctl 来源：~vm.max_map_count~ 1048576 来自 Arch `filesystem` 包的 `10-arch.conf`，~kernel.pid_max~ 4194304 来自 systemd 的 `50-pid-max.conf`，~fs.nr_open~ / ~fs.file-max~ 由 systemd 启动时调大；systemd 262 默认 ~DefaultLimitNOFILE=1024:524288~ 。本机没有 sysstat、perf、strace、bcc，工具的列名和选项按手册写，未运行。
- [x] 笔记 6 篇 + 索引 1 个，根索引接入；Reclaim 的水位线一节改为标题级节点 Linux Memory Zones and Watermarks（ `b879e051` ），补 zone 划分
- [x] 本批卡片：18 张，`ankinotes/linux.org` 共 66 张（平均负载已有批次 1 的卡，不重复）
- [x] 总计划：批次 4 勾选
- [x] 验证：无笔记需要 TOC（一级最多 5 个、二级 0 个）；行内标记检查为空（含卡片）；block 配平；ID / 标题 / 别名无重复；链接目标全部存在；主树可达、唯一父节点，出度根 5 / Observability 6；无指向索引或祖先的正文链接、无互链；排障流程图渲染并补上 `#+RESULTS:` ，已目检
- [x] `org-roam-db-sync`（临时 daemon `cc-sync`）：377 节点（与磁盘上的 =:ID:= 数一致），其中 Linux 35；无悬空 ID 链接

## 废弃 ID

| 旧笔记 / 标题 | ID | 内容去向 |
|---|---|---|
| cpu_metrics 的 Load Average、CPU Usage、Cache Hit Rate 标题 | `fc75e5c3…` `bf6dd008…` `397c168b…` | Linux CPU Performance Analysis |
| cpu_troubleshooting | `3c55f112…` | 同上 |
| short_period_process | `35d07be4…` | 同上（短时进程一节） |
| memory_troubleshooting | `b21233f1…` | Linux Memory Performance Analysis |
| i_o_troubleshooting | `ed3469d5…` | Linux I/O Performance Analysis |
| i_o_optimization | `f593c3a7…` | 同上（优化手段的判断） |
| performance_optimization | `9386e730…` | 分组页，由新索引 Linux Observability and Troubleshooting 取代 |
| process_troubleshooting | `9b389f92…` | Linux Performance Troubleshooting Method |
| system_error 及其 Linux Error Handling 标题 | `a7b6885c…` `510e4c03…` | errno、 ~EINTR~ 已在 Linux System Calls；资源类错误 → Linux Resource Limits |
| proc_pid | `6e5f182c…` | Linux /proc and sysctl Interfaces |
| proc_sys 及其 /proc/sys/vm 标题 | `fd21b119…` `6333bfdb…` | 同上；swappiness、drop_caches 已在 Reclaim / Page Cache |

以上 ID 在迁移范围外均无入链。

## 指向未迁移笔记的链接

新笔记中没有：工具笔记（top、pidstat、perf、strace、pstree、execsnoop、Common Tools）的链接改为纯文本。

## 给后续批次

- 批次 5：工具能力地图链到本批的分析笔记（工具 → 判断链），不反向链接。Method 笔记已有「整体检查」的命令表（只写看哪一列），工具地图不重复这张表，而是写各工具的能力和开销。Observability 索引出度已是 6，工具笔记若放这里到 7–8 时评估拆出 Linux Performance Tools 子索引。
- 批次 6：`system_time` → `505fb55e` 现为 Linux Resource Limits（ ~CLK_TCK~ 在其常量表中），迁移后自动恢复。
- 批次 7：USE 表的网卡一行和 =/proc/net/= 、 ~net.core.somaxconn~ 只写了一句，网络笔记展开时由网络笔记引用本批（或 Resource Limits），不反向链接。
- 批次 8：`cpu_hardware` 的 NUMA / Zone → `b879e051` 现为 Reclaim 中的标题级节点 Linux Memory Zones and Watermarks，迁移后自动恢复。
