# Linux 迁移批次 5：性能与诊断工具

Status: Complete

总计划见 `2026-10-26-next-linux-os-migration.md`，上一批见 `2026-10-26-linux-batch4-observability.md`。源笔记保留。

## 现状

- 20 篇约 460 行，多为工具名单、命令示例和截图：`performance_tools`、`io_tools`、`diagnostic_tools`、`monitoring_tools`、`memory_tools`、`process_management_tools` 是只有一两个链接或一张表的分组页；`top`、`dstat`、`vmstat`、`pstree`、`strace` 各几行；内容较多的是 `perf`（ ~perf stat~ 计数器）、`sysstat`、`fio`、`stress`、`bcc_tools`。
- 入链：本批全部 ID 的入链都来自本批内部或批次 1–4 已迁移的旧笔记（旧根 `linux`、`system_troubleshooting`、`cpu_metrics`、`context_switching` 等），迁移范围外没有入链，ID 可按需保留或废弃。
- 本批旧笔记的出链：已迁移的 Swap（现 Linux Memory Reclaim 的标题级节点 `0bff214a`）；`58c36f85`（System Call）在新旧库中都已不存在，改指 Linux System Calls；未迁移、也不在 8 批计划内的 `dd` `17daaa09`、`ab` `49b1d0cc`、`hping3` `a07e73bd`；批次 6 的 `grep` / `sed` / `awk`；批次 7 的 Network Tools `53273a0c`。
- 资源：`assets/Linux/LinuxTools_1.png`（Brendan Gregg 的 Linux Performance Tools 全景图）、`assets/Linux/perf-tools_1.png`（perf-tools 分布图）、两张 `Cheat_Sheet` 截图（通用命令速查、进程管理命令与信号）。
- 学习目标：工具本身只到「知道」；判断链已在批次 4。本批的「能判断」只在：观测机制与开销（计数器 / 跟踪 / 采样）、perf 的读法与坑（IPC、调用栈、权限），以及基准测试结果是否可信。

## 归属与调整

- 全部归 `Linux/`，接在 Linux Observability and Troubleshooting 下（出度 6 → 7）。不建 Linux Performance Tools 子索引：总览笔记兼作两篇子笔记的父节点（AGENTS.md「库的主笔记可兼作其子主题的父节点」），省一层只有导航的索引。
- 20 篇 → 3 篇：
  - *Linux Performance Tools* （保留 `linux_tools` 的 ID `8c7cfc98`）：三类观测机制及其开销，按机制分的工具家族（procps、sysstat、top 系、strace / ltrace、ftrace 与 perf-tools、eBPF 与 bcc / bpftrace），全景图。吸收 `performance_tools`、`perf_tools`、`bcc_tools`、`sysstat`、`top`、`dstat`、`strace`、`vmstat`、`monitoring_tools`（ ~watch~ ）、`diagnostic_tools`、`memory_tools`、`io_tools`、`process_management_tools`、`pstree`。
  - *Linux perf Profiler* （保留 `perf` 的 ID `894e26d6`）： ~perf stat~ 计数器的读法、 ~perf top~ / ~record~ / ~report~ 与火焰图、调用栈（帧指针 / DWARF / LBR）、权限、容器与虚拟机中的限制、 ~perf sched~ / ~perf c2c~ / ~perf trace~ 的用途。
  - *Linux Benchmarking and Load Generation* （保留 `testing_tools` 的 ID `3eb94d17`）：压测的目的（复现、容量）、 ~stress~ / ~stress-ng~ 、 ~sysbench~ 、 ~fio~ 的参数和延迟指标、基准测试的坑（页缓存、写裸设备会毁数据、队列深度、预热、SSD 状态）；吸收 `stress`、`sysbench`、`fio`。
- 资源：全景图复制为 `Linux/images/linux_performance_tools_map.png`；perf-tools 分布图的信息已在全景图和正文中，不迁；两张 Cheat Sheet 截图是可随时查询的命令清单（且大半属于批次 6 的 Shell / 用户管理），不迁。
- 外部链接：`dd`、`ab` 在 Benchmarking 中提到时保留原 ID 链接（未迁移）；`hping3`、网络工具不在本批写，留给批次 7；文本处理工具留给批次 6。

## 目标树

```
Linux Observability and Troubleshooting (8a6eab8f)
├─ ...（批次 4 的 6 篇）
└─ Linux Performance Tools (linux_tools 8c7cfc98)
    ├─ Linux perf Profiler (perf 894e26d6)
    └─ Linux Benchmarking and Load Generation (testing_tools 3eb94d17)
```

深度 4（根 → Observability → Tools → perf）。

笔记间横向链接（单向）：

- Tools 总览 → Method（「先计数器后跟踪」对应「从整体到代码」）、Linux System Calls（strace 跟踪的对象）、Linux /proc and sysctl Interfaces（计数器类工具读的就是 /proc）。
- perf → Linux CPU Performance Analysis（IPC 的判断已在那里，此处只写怎么测）、Linux CPU Scheduling and Affinity（ ~perf sched~ 测调度延迟）。
- Benchmarking → Linux Page Cache and Writeback（为什么要 ~direct=1~ / ~fdatasync~ ）、Linux I/O Performance Analysis（观测到的 IOPS 与 fio 测出的上限比较）。
- 已迁移笔记不反向链接。批次 4 中 perf、strace、bcc 的纯文本提及保持不变。

## 已发现的旧笔记错误（核对后改正）

- perf 笔记「 =task-clock= 表示任务用了多少时钟周期」：是任务的 CPU 时间（毫秒），旁边的 =CPUs utilized= 是它除以墙钟时间。
- 「 =instructions= 与 =cycles= 的差反映向量化和流水线的好坏」：看的是比值 IPC；向量化减少指令数，IPC 不一定升高。
- 「IPC 反映流水线、乱序执行和超线程带来的加速」：超线程让两个硬件线程共享一个核，单个线程的 IPC 通常下降。
- 「 =migrations= 表示程序为等待内核操作（如 I/O）而停下」：是任务被调度到另一个 CPU 上运行的次数。
- 「 =cache-references= 在访问 L1 / L2 / L3 中的数据时增加」：通用事件 =cache-references= / =cache-misses= 在 x86 上对应末级缓存（LLC）的访问和未命中，不含 L1 / L2。
- 「把 =perf_event_paranoid= 设为 -1」：等于对所有用户开放内核采样；给需要的用户或程序 ~CAP_PERFMON~ （5.8 起）更安全。本机（Debian 内核）为 3，是发行版补丁，上游最高为 2。
- strace「多线程程序不加 ~-f~ 只会输出主进程的系统调用」：只跟踪 ~-p~ 指定的那个线程。
- stress 示例 ~stress -c 16 -- timeout 600~ ：应为 ~--timeout~ 。
- dstat：原项目 2020 年后停止维护，Red Hat 系用 pcp 的 ~pcp-dstat~ 代替，社区分支为 ~dool~ 。
- 「execsnoop 通过 ftrace 监控 ~exec()~ 」：只是 perf-tools 版本；bcc 版本基于 eBPF。

## Checklist

- [x] 核对（scratchpad `linux5/`）：本机 btrfs（ ~compress=lzo~ ）/ HDD 上 512 MiB 随机数据， ~dd~ 缓冲写 373 MB/s、 ~conv=fdatasync~ 59.5 MB/s；热读 7.5 GB/s、 ~iflag=direct~ 读 86 MB/s；全零数据缓冲写 1.0 GB/s、 ~fdatasync~ 357 MB/s（压缩所致）；=perf_event_paranoid= 为 3（Debian 内核补丁）。本机没有 perf、strace、sysstat、bcc、fio、stress-ng、sysbench，选项和列名按手册写，未运行。
- [x] 笔记 3 篇，Observability 索引接入总览（出度 7）；全景图复制为 `Linux/images/linux_performance_tools_map.png`
- [x] 本批卡片：13 张，`ankinotes/linux.org` 共 79 张
- [x] 总计划：批次 5 勾选
- [x] 验证：无笔记需要 TOC（内容一级标题最多 5 个、二级 0 个）；行内标记检查为空（含卡片）；block 配平；ID / 标题 / 别名无重复；链接目标存在（ `dd` 、 `ab` 除外，未迁移）；新 ID 只由各自唯一父节点的整行标题引用，无指向索引或祖先的正文链接、无互链
- [x] `org-roam-db-sync`（临时 daemon `cc-sync`）：380 节点（与磁盘上的 =:ID:= 数一致），其中 Linux 38；悬空 ID 链接只有 `dd` 、 `ab` 两个预期的

## 废弃 ID

| 旧笔记 / 标题 | ID | 内容去向 |
|---|---|---|
| linux_tools 的 Common Tools、Linux Toolkit 标题 | `0064e354…` `bf0a7313…` | Linux Performance Tools |
| performance_tools、diagnostic_tools、monitoring_tools、memory_tools、io_tools、process_management_tools（分组页） | `a416cc1c…` `aa8a566c…` `aae692ca…` `2818abfe…` `663df4ec…` `717580ba…` | 同上 |
| monitoring_tools 的 watch 标题 | `d5abaaa5…` | 同上 |
| perf_tools 及其 execsnoop 标题 | `605b3e38…` `54850633…` | 同上（ftrace 与 perf-tools 一节） |
| bcc_tools 及其 BCC Memory Tools、memleak、BCC IO Tools 标题 | `4c9b7236…` `2f3bee9b…` `0cdff663…` `73b2ea10…` | 同上（eBPF 一节） |
| sysstat 及其 pidstat、mpstat 标题 | `febe7777…` `4baf76c7…` `d12363f8…` | 同上 |
| top、dstat、vmstat、pstree、strace | `14101e01…` `ddd59b03…` `23925da8…` `80483dbf…` `a1819374…` | 同上 |
| testing_tools 的 Stress Testing、Website Testing 标题 | `6ead6128…` `385e6383…` | Linux Benchmarking and Load Generation |
| stress 及其 stress-ng 标题、sysbench、fio | `d63fa413…` `846d35f4…` `43ec7535…` `afdc900d…` | 同上 |

以上 ID 在迁移范围外均无入链。

## 指向未迁移笔记的链接

- Linux Benchmarking and Load Generation → `dd` `17daaa09`、`ab` `49b1d0cc`（均不在 8 批计划内，迁移时保留原 ID 即可恢复）。

## 给后续批次

- 批次 6：文本处理工具（grep / sed / awk）的旧链接只在本批源笔记中，新笔记未引用。
- 批次 7：网络工具（ ~ss~ 、 ~tcpdump~ 、 ~sar -n~ 、bcc 的 ~tcpretrans~ 等）在 Linux Performance Tools 中只列了名字；`hping3` `a07e73bd` 未迁移、不在计划内，网络批次可决定是否收录。网络笔记可引用 Linux Performance Tools 的 eBPF 一节，不反向链接。
- 未在计划内的 `dd` `17daaa09`、`ab` `49b1d0cc` 被 Linux Benchmarking and Load Generation 引用，迁移时保留原 ID。
