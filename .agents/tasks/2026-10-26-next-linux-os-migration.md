# Linux / OS 迁移总计划（来自 `Default/`）

Status: Planned — 批次 1 未开始

把 `roamnotes/Default/` 中 `filetags` 含 `Linux`、`OS`、`SystemCall`、`Performance`、`Hardware` 的 103 篇笔记（约 3,000 行）分 8 批迁入 `roamnotes-v2/`。*每批开一个新 session*，按 note-migration skill 执行。本文件是总计划；各批的归属方案、目标树和 ID 映射写在各自的任务文件里。

## 为什么先做这一组

- C++、Trading 迁完后，旧库只剩 `Default/`（243 篇）和 `Games/`（2 篇）；Linux 一组在 `Default/` 中最大。
- 有待接的线：C++ 迁移把栈 / 堆 / 静态区的通用内容留给 `Default/process_memory_model`；它指向 C++ Memory Allocation 的入链等它迁移后才算接上。
- 与学习目标相关：内核旁路、核绑定、系统调用、性能调优服务于 C++ 低延迟和交易系统开发（见 `.agents/learning-goals.md`）。

## 全局约定（所有批次）

- 旧索引 `linux-20230802.org`（ID `4f8f2615…`）的结构只作参考，不沿用。批次 1 建立 v2 大类 `Linux/` 及其根索引，沿用这个 ID；后续批次把中间索引接到这个根下。大类名如需调整（如 `OS/`），在批次 1 与用户确认。
- 每批开始时：读本文件和上一批的任务文件，检查已迁节点，避免重复；指向后续批次笔记的 ID 链接原样保留，记入该批任务文件。
- 每批结束时：按 AGENTS.md「按改动验证」完成验证和 `org-roam-db-sync`，在下方勾选该批、填上任务文件名；用户要求时提交并推送。
- 命令行工具类笔记（top、sysstat、perf 等）按 cc-note-writing 大幅压缩为能力地图；保留「什么现象用什么工具、读哪个指标」的判断。
- 不在本计划内的 `Default/` 笔记（Network 标签中其余 20 多篇、Algorithm、SystemDesign、Tools 中的非 Linux 工具等）留给后续计划。

## 批次

| # | 主题 | 笔记（旧文件名，省略日期） | 去向 |
|---|---|---|---|
| 1 | 进程、调度与系统调用 | linux（旧索引）、process_environment、process_state、fork、threads、scheduler、context_switching、interrupt、hardware_interrupt、short_period_process、system_calls、system_header_files、glibc | 新建 `Linux/` 根索引 |
| 2 | 内存 | process_memory_model、memory_hierarchy、memory_allocation、malloc、sbrk、virtual_memory、memory_mappings、shared_memory、swap、out_of_memory、garbage_collection、memory_leak | `Linux/`；接上 C++ Dynamic Memory Allocation 的通用部分 |
| 3 | 文件系统与 I/O | file_system、journaling_file_systems、virtual_file_system、inode、dentry、hard_link、file_descriptor、file_sharing、special_files、tmpfs、block_layer、page_cache、dirty_pages、system_caches、file_i_o、file_io_buffering、i_o、i_o_multiplexing | `Linux/`；I/O 多路复用与 `Network/` 的关系在此决定 |
| 4 | 观测与排障方法 | cpu_metrics、cpu_troubleshooting、memory_metrics、memory_troubleshooting、i_o_metrics、i_o_optimization、i_o_troubleshooting、performance_optimization、process_troubleshooting、system_troubleshooting、system_error、system_limits、proc、proc_pid、proc_sys、proc_zoneinfo | `Linux/` |
| 5 | 性能与诊断工具 | linux_tools、performance_tools、perf、perf_tools、bcc_tools、sysstat、top、dstat、stress、sysbench、fio、strace、monitoring_tools、diagnostic_tools、testing_tools、memory_tools、io_tools、process_management_tools、pstree | `Linux/`，合并为少数几篇能力地图 |
| 6 | 系统管理与 Shell | linux_bootstrap、startup_scripts、users_and_groups、cron、system_time、shell_script、shell_tips、awk、sed、grep、curl | `Linux/`；Shell 是否独立成组在此决定 |
| 7 | Linux 网络 | linux_network_stack、tcp_ip_layers、network、network_tools、iptables、iperf3、pktgen | 并入现有 `Network/`（已有 `Linux Network Tools`、TCP 笔记） |
| 8 | 硬件与 Python 性能分析 | computer_hardware、cpu_hardware、motherboard、computer_display；python_profiling、python_sampling_profiler、viztracer | 硬件归属在此与用户确认；Python 三篇并入 `Python/` |

顺序理由：1、2 是后面各批引用的基础概念（进程、内存）；3 依赖内存（页缓存）；4、5 引用 1–3 的模型，先写方法（4）再写工具地图（5）；6–8 相对独立，可按兴趣调换。

## 进度

- [ ] 批次 1：进程、调度与系统调用 —— 任务文件：
- [ ] 批次 2：内存 ——
- [ ] 批次 3：文件系统与 I/O ——
- [ ] 批次 4：观测与排障方法 ——
- [ ] 批次 5：性能与诊断工具 ——
- [ ] 批次 6：系统管理与 Shell ——
- [ ] 批次 7：Linux 网络 ——
- [ ] 批次 8：硬件与 Python 性能分析 ——

## 每批新 session 的开场白

> 迁移 Linux 笔记批次 N，按 `.agents/tasks/2026-10-26-next-linux-os-migration.md` 执行。

批次 1 额外加一句：「先问我 Linux 的学习目标。」

## 其他遗留

C++ 和 Trading 的 Anki 卡片另见 `2026-10-26-cpp-trading-anki-cards.md`，与本计划互不依赖。
