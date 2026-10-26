# Linux 迁移批次 1：进程、调度与系统调用

Status: Complete

总计划见 `2026-10-26-next-linux-os-migration.md`。本批把 `roamnotes/Default/` 中 13 篇（约 350 行）迁入新大类 `roamnotes-v2/Linux/`，建立根索引。源笔记、图片和 `assets/Linux/` 全部保留。

## 现状

- 旧笔记多为课程笔记（APUE、Linux 性能优化课）的摘抄：`hardware_interrupt` 为空，`system_header_files`、`fork`、`scheduler` 只有几行；`threads` 的状态图是通用教材图（New / Runnable / Blocked），与 Linux 无关。
- 范围外入链：`contents.org`（旧全库目录，不迁）→ 根 `4f8f2615`、旧根中的标题 CPU `072ce693`、Memory `bcae4642`、Processes `7d47a7bc`；`cpu_metrics` → Context Switching `706d7e91`；`cpu_troubleshooting`、`linux_network_stack` → Interrupt `18ebf2c0`；`proc` → 标题 `/proc/interrupts` `3158f50d`（旧 ID 行后多了 `  :Linux:`，`proc` 中的链接也带着它，批次 4 迁移 `proc` 时改成纯 ID）；`process_troubleshooting` → Short Period Process `35d07be4`。
- 学习目标：2026-10-26 用户四个用途全选（低延迟 / 交易系统、性能排障、面试、日常使用），大类名 `Linux/`，已写入 `.agents/learning-goals.md`。
- 本机环境（核对用）：Docker 容器，宿主内核 Linux 6.5（Debian 6.5.10），Arch 用户态，glibc 2.44，GCC 16.2.1，i5-1155G7 8 核，物理机（无 hypervisor），时钟源 tsc，Meltdown 不受影响（无 KPTI）。

## 归属与调整

- 全部归 `Linux/`。
- `short_period_process`（`35d07be4`）改到批次 4：内容是排障方法（找短时进程），唯一范围外入链来自批次 4 的 `process_troubleshooting`，由它吸收为标题级节点更合适。已在总计划中移动。
- 语言：旧笔记中英混杂，实质内容（状态码、上下文切换、中断）以中文为主，最近的兄弟领域 `Network/` 也是中文，统一用中文正文、英文标题。

## 目标树

12 篇 → 7 篇笔记 + 3 个索引。`←` 后为并入的旧笔记。

```
Linux (linux 4f8f2615，根索引)
├─ Linux Processes (旧根中的 Processes 标题 7d47a7bc，改为独立索引文件)
│   ├─ Linux Process Lifecycle (fork 6f1e5033) ← process_environment
│   ├─ Linux Process States (process_state 925ecbf4)
│   └─ Linux Processes vs Threads (threads d63d5c4d) ← context_switching 的 Thread Context Switch 一节
└─ Linux Scheduling and Kernel Entry (新 ID d8350135)
    ├─ Linux CPU Scheduling and Affinity (scheduler d525dfda)
    ├─ Linux Context Switching (context_switching 706d7e91)
    ├─ Linux Interrupts and Softirqs (interrupt 18ebf2c0；标题 Interrupt Counters in /proc 保留 3158f50d) ← hardware_interrupt
    └─ Linux System Calls (system_calls b740640d) ← system_header_files, glibc
```

出度：根 2（后续批次增加），中间索引 3、4。深度 3。

笔记间横向链接（单向）：States → Lifecycle（僵尸）；Processes vs Threads → States、Context Switching；Scheduling → Context Switching、Interrupts（IRQ 亲和性）；Context Switching → System Calls、Interrupts。范围外：Trading 的 Low Latency Trading Design → Interrupts、Scheduling；C++ Threads and Async Tasks → Processes vs Threads。

## 改造原则

- 补核心模型（按学习目标「能判断」）：COW 与 fork 代价、多线程中 fork、各终止方式的清理差异、内核中进程 / 线程同为 task、调度策略与 RT 限流、绑核与核隔离、自愿 / 非自愿切换、软中断执行位置、IRQ 亲和性、系统调用路径与 vDSO、glibc 兼容方向。
- 删去：头文件清单、通用线程状态图、终止方式的 APUE 原文列表（改为对比表）。
- 工具（vmstat、pidstat、execsnoop）只写读哪个指标，不链接工具笔记；批次 5 的工具能力地图链接到这些概念笔记。
- 图：进程状态图改画 PlantUML；新增 fork / exec / wait 时序图、收包中断路径图、系统调用路径图。旧截图不复制。

## 已发现的旧笔记错误

- 「节拍率即 Linux 时间片的长度」：HZ 是时钟中断频率，时间片由调度器决定。
- 「一次系统调用发生了两次 CPU 上下文切换」：是两次特权模式切换，不换任务，`vmstat` 的 cs 不计入。
- 「中断只发生在内核态」：用户态也会被中断，处理程序在内核态运行。
- 「软中断通常以内核线程的方式运行」：通常在硬中断返回时就地执行，积压过多才交给 ksoftirqd。
- 「All system calls are executed atomically」：阻塞调用会睡眠、可被信号打断，read / write 可部分完成；只有特定操作有原子性保证。
- 「线程创建比进程快 100 倍」：取决于地址空间大小，本机小进程约 6 倍，1 GiB 已触碰堆时约 1,400 倍。
- glibc 版本路径 `/lib/libc.so.6` 因发行版而异。
- isolcpus 曾在内核文档中标为 deprecated，当前文档已无此说明（2026-10-26 查 kernel-parameters.txt），笔记不写 deprecated。

## Checklist

- [x] 学习目标写入 `.agents/learning-goals.md`
- [x] 核对（scratchpad `linux1/`）：fork 后 stdio 缓冲重复输出、各退出方式的 atexit / 析构行为、僵尸与 `SIGCHLD` 设为 `SIG_IGN`、T 状态、线程 TID 与每线程亲和性、syscall / vDSO / fork / pthread / 管道往返耗时、`/proc/interrupts` 与 `/proc/softirqs` 行名、RT 限流默认值；内核 Kconfig.hz 默认 250
- [x] 笔记 7 篇 + 索引 3 个
- [x] Trading、C++ 笔记中加入指向新笔记的引用
- [x] 总计划：批次 1 勾选，`short_period_process` 移入批次 4，开场白改为「开始下一个批次的笔记迁移」
- [x] 验证：无笔记需要 TOC（一级标题最多 5 个、二级最多 2 个）；行内标记检查为空；block 配平；ID / 标题 / 别名无重复；链接目标全部存在；主树可达、唯一父节点，出度 2 / 3 / 4；无互链、无指向索引或祖先的正文链接
- [x] PlantUML 渲染：4 张图（生命周期时序、状态图、收包中断路径、系统调用路径）生成并补上 `#+RESULTS:`，逐张目检
- [x] `org-roam-db-sync`（临时 daemon `cc-sync`）：353 节点，其中 Linux 11（10 个文件 + 1 个标题级节点）；无悬空 ID 链接

## 废弃 ID

迁移范围外没有入链（`contents.org` 不迁）：

| 旧笔记 / 标题 | ID | 内容去向 |
|---|---|---|
| process_environment | `084a32f7…` | Linux Process Lifecycle |
| hardware_interrupt | `d959170b…` | Linux Interrupts and Softirqs |
| system_header_files | `f56bc413…` | 删去（可查询） |
| glibc | `3d49b6d9…` | Linux System Calls → glibc |
| context_switching 的四个标题 | `d79d72f5…` `76f53542…` `412e656c…` `b912c69b…` | Context Switching 对比表；线程部分 → Processes vs Threads |
| interrupt 的 Hardware / Soft Interrupt 标题 | `2e165f86…` `7f05fbc8…` | Interrupts and Softirqs → 上半部与下半部 |
| 旧根的 Shell 标题 | `bb18c4e2…` | 批次 6 决定 |

旧根的 CPU（`072ce693…`）、Memory（`bcae4642…`）标题只有 `contents.org` 入链；批次 2 可让 Memory 索引沿用 `bcae4642`。

## 指向未迁移笔记的链接

新笔记中没有（工具链接改为纯文本，见改造原则）。批次 4 迁移 `cpu_metrics`、`cpu_troubleshooting`、`proc`、`process_troubleshooting`，批次 7 迁移 `linux_network_stack` 时，它们指向本批保留的 ID（`706d7e91`、`18ebf2c0`、`3158f50d`）会自动恢复。

## 给后续批次

- `vmstat`（`Default/vmstat-20230820.org`，标签 `:Tools:`）不在总计划的任何批次中，批次 5 一并处理。
- 平均负载只在 Process States 中写了一句（R + D），批次 4 的 CPU 指标笔记展开并链接过来。

## Anki 卡片（待补）

批次 1 完成后才加入「迁移时制卡」规则，卡片在批次 2 开始前补做，写入 `ankinotes/linux.org`（`RoamCards::Linux`），中文。候选：fork 返回两次；各退出方式的清理差异；R / S / D / Z 与平均负载只统计 R + D；自愿与非自愿切换各说明什么；硬中断与软中断的分工和软中断的执行位置；系统调用不是上下文切换；vDSO 退化为真正系统调用的条件；绑核之外还需要的核隔离手段；隔离核上忙轮询线程为何不用 ~SCHED_FIFO~ ；多线程进程 fork 后的限制。
