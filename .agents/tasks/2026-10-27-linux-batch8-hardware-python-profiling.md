# Linux 迁移批次 8：硬件与 Python 性能分析

Status: Complete

总计划见 `2026-10-26-next-linux-os-migration.md`，上一批见 `2026-10-27-linux-batch7-network.md`。源笔记保留。

## 现状

- 8 篇约 340 行：
  - 硬件：`computer_hardware`（旧硬件索引 + 课程词汇表）、`cpu_hardware`（SIMD、超线程、流水线各一两句，NUMA 一节含 Zone）、`memory_hierarchy`（课程式 L1 / L2 / L3 描述 + 4 张截图）、`motherboard`、`computer_display`（PC 装机课程笔记）。
  - Python：`python_profiling`（测量注意事项 + 工具速查）、`python_sampling_profiler`（py-spy、scalene、vmprof 的安装命令）、`viztracer`（一句介绍 + 两条命令）。
- 入链（迁移范围外）：
  - `viztracer` `5a4eceee` ← `py_troubleshooting`（未迁移，不在本计划）。
  - `python_profiling` `021750fa` ← 旧 `python` 索引（`python-20250102`，已由 v2 Python 根承接，不计）。
  - `cpu_hardware` `5dc17fb2`、`memory_hierarchy` `d734bb0e` ← 旧 `linux` 根（批次 1 已迁移，不计）。
  - 其余 ID 只有本批内部入链。
- 出链到已迁移节点：`cpu_hardware` 的 Zone → `proc_zoneinfo` `b879e051`（批次 4 的标题级节点 Linux Memory Zones and Watermarks）。
- 学习目标：硬件部分服务于 Linux 的低延迟（核绑定、NUMA、缓存、频率）一行，「能判断」；Python 性能分析由用户在本批确定为「能判断用哪种工具、测量的坑；工具的命令行只到知道」，写入 `.agents/learning-goals.md`。

## 用户决定（2026-10-27）

- CPU / 内存硬件并入 `Linux/`，建中间索引，沿用旧 `computer_hardware` 的 ID。
- `motherboard`、`computer_display` 和 `computer_hardware` 的词汇表 *不迁移* ，并在此记录（见下节）。
- Python 性能分析深度：能判断用哪种工具；命令行只到「知道」；按判断制卡。

## 不迁移的笔记

| 旧笔记 | ID | 内容 | 不迁原因 |
|---|---|---|---|
| motherboard | `4baf1454…` | 南北桥、扩展槽、ATX / ITX 规格、HDD / SSD 与 SATA / NVMe 接口、电源与电压电流、USB 各代速率与接口、设备接口截图 | PC 装机课程（IT 支持类）的可查询事实，不在任何学习目标内 |
| computer_display | `04eccc31…` | LCD（IPS / TN / VA）与 OLED 的分类 | 同上 |
| computer_hardware 的 Architecture 与 Glossary 两节 | （文件 ID 改作新索引） | CPU—内存控制器—内存的截图，MCC、地址总线、时钟、POST、UEFI 等词汇 | 同上；CPU 与内存的关系由新的缓存层级笔记承接 |

源文件和截图保留在 `roamnotes/Default/`。两篇笔记的 ID 在迁移范围外无入链，随本批废弃；以后若要入库，按新内容重写即可。

## 归属与调整

- 新中间索引 *CPU and Memory Hardware* （沿用 `computer_hardware` 的 ID `66716bea-36fc-4002-9a38-2081669626dd`），接在 Linux 根下（出度 6 → 7）。3 个子节点：
  - *CPU Cache Hierarchy* （保留 `memory_hierarchy` 的 ID `d734bb0e`）：层级、容量与延迟（本机实测 pointer chasing）、缓存行与局部性、预取、TLB 指向虚拟内存笔记、缓存一致性（MESI）与伪共享。Caches 标题 ID `9a304aa0` 无入链，废弃。截图不迁，拓扑改 PlantUML。
  - *CPU Core Execution Features* （保留 `cpu_hardware` 的 ID `5dc17fb2`）：流水线、乱序执行与分支预测；SMT（超线程）的共享资源、兄弟线程的编号、低延迟场景的取舍；SIMD 与 AVX-512 降频；频率调节（turbo、governor）与 C-state 对延迟和基准测试的影响。SIMD、Hyperthreading 标题 ID（`b361f3ec`、`f1faaf48`）无入链，废弃。
  - *NUMA Memory Architecture* （由 `cpu_hardware` 的 NUMA 标题 `29001a4b` 提升为文件节点）：节点、本地与远程访问、首次触碰（first-touch）分配、 ~numactl~ / ~numastat~ 、自动 NUMA 平衡、网卡所在节点；Zone 指向 Linux Memory Zones and Watermarks（`b879e051`）。
- Python 三篇合并为 *Python Profiling* （保留 `python_profiling` 的 ID `021750fa`），接在 Python Development Practices 下（出度 4 → 5）：
  - 三类剖析器（确定性 / 采样 / 追踪）的原理、开销与各自回答的问题；问题 → 工具的选型表；测量的坑（ ~time.time~ 、 ~timeit~ 关 GC、cProfile 放大调用开销、只剖析当前线程、频率波动等）；能力地图。
  - VizTracer 一节保留 `5a4eceee` 作标题级节点（有未迁移的 `py_troubleshooting` 入链）。
  - `python_sampling_profiler` `90997365` 无范围外入链，废弃，内容并入采样一节。
- 删去：安装命令、速查用法、GPU / PyTorch / Web 服务器工具中过时的（dowser、dozer）、旧笔记的 BIOS 操作清单（压缩为「测量环境」几条）。

## 目标树

```
Linux (4f8f2615)
├─ …（原 6 个中间索引）
└─ CPU and Memory Hardware (66716bea，原 computer_hardware)
    ├─ CPU Cache Hierarchy (d734bb0e)
    ├─ CPU Core Execution Features (5dc17fb2)
    └─ NUMA Memory Architecture (29001a4b)

Python (6922b85c)
└─ Development Practices (9caeb97a)
    ├─ …（原 4 个）
    └─ Python Profiling (021750fa；标题 VizTracer for Python 5a4eceee)
```

笔记间横向链接（单向，使用方 → 被使用方）：

- Cache Hierarchy → Linux Virtual Memory and Page Faults（TLB、大页）。
- Core Execution → Cache Hierarchy（依赖链无法被乱序执行重叠）。
- NUMA → Linux Memory Zones and Watermarks（zone 划分）。
- Core Execution、NUMA → Linux CPU Scheduling and Affinity（核隔离、绑核）。
- 已有笔记新增：C++ Memory Model and Atomics 伪共享一条 → Cache Hierarchy（一致性机制与实测）。
- Python Profiling → Linux perf Profiler（ ~-X perf~ ）、CPU Core Execution Features（测量前固定频率）。

## Checklist

- [x] 核对（scratchpad `linux8/`）：本机 i5-1155G7（4 核 8 线程，单节点，容器内）。 ~lscpu -e~ 与 =thread_siblings_list= 确认兄弟线程为 0/4、1/5；cpuidle 各状态退出延迟；C 程序指针追逐测各级延迟（THP 开 / 关结果相近，L3 段受系统负载约 6 的干扰，如实写入笔记）；原子计数器测伪共享（跨核 4.28 s 对 0.97 s，超线程兄弟上无代价）；普通 ~volatile~ 写只差约 10%；GCC 16.2.1 的 ~-O2~ / ~-O3~ / ~-march=native~ 向量化报告与 ~float~ 求和的 ~addss~ 对 ~addps~ 。Python：cProfile 在 3.11 漏掉工作线程、3.12 起经 ~sys.monitoring~ 记录全部线程；cProfile 与 VizTracer 对调用密集代码的放大（5.8 倍、4 倍），py-spy 比例基本不变；py-spy 默认不采空闲线程、 ~--idle~ 才有；3.15.0 的 ~profiling.sampling~ 子命令和 ~--mode wall~ / ~cpu~ ； ~timeit~ 期间 GC 关闭；line_profiler 5.1.0 的 ~profile~ 无 ~LINE_PROFILE=1~ 时不输出；VizTracer 1.1.1 缓冲区默认 1,000,000 条、满后丢弃最早的数据；memory_profiler 的 PyPI 说明已声明不再维护（最后发布 0.61.0，2022-11）。本机没有 perf、cpupower， =/dev/cpu_dma_latency= 在容器中不存在，相关做法按文档写，未运行。
- [x] 笔记 3 篇 + 新索引，接入 Linux 根（出度 7）
- [x] Python Profiling（英文，跟随 Python 大类和源笔记的语言），接入 Development Practices（出度 5）；learning-goals 增加 Python 一节
- [x] 已有笔记补链：只改了 C++ Memory Model and Atomics（伪共享一条 → CPU Cache Hierarchy）。原计划的 Scheduling and Affinity → 硬件笔记改为不加：Core Execution 和 NUMA 已经引用 Scheduling and Affinity（隔离核的做法），再反向引用就成了互链
- [x] PlantUML 渲染：`Linux/images/cpu_cache_hierarchy.png`、`numa_two_sockets.png`
- [x] 本批卡片：硬件 10 张写入 `ankinotes/linux.org`（Cache 4、Core Execution 4、NUMA 2），Python 8 张写入 `ankinotes/python.org`（英文）
- [x] 总计划：批次 8 勾选
- [x] 验证：各笔记一级标题 ≤ 5，不需要 TOC；行内标记检查为空（含卡片），裸写的 =line_profiler= 、 =memory_profiler= 改用 =~...~= ；block、property drawer 配平；全库 ID / 标题 / 别名无重复；新节点各只由唯一父节点的整行标题引用，正文链接不指向索引或祖先、无互链；图片链接均存在
- [x] `org-roam-db-sync`（临时 daemon `cc-sync`）：400 节点（与磁盘上的 =:ID:= 数一致）；悬空 ID 链接只有批次 5 的 `dd` 、 `ab` 两个预期的

## 废弃 ID

| 旧笔记 / 标题 | ID | 内容去向 |
|---|---|---|
| memory_hierarchy 的 Caches 标题 | `9a304aa0…` | CPU Cache Hierarchy |
| cpu_hardware 的 SIMD、Hyperthreading 标题 | `b361f3ec…`、`f1faaf48…` | CPU Core Execution Features |
| python_sampling_profiler | `90997365…` | Python Profiling 的采样一节 |
| motherboard、computer_display | `4baf1454…`、`04eccc31…` | 不迁移，见上 |

以上 ID 在迁移范围外均无入链。
