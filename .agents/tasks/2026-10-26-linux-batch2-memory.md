# Linux 迁移批次 2：内存

Status: Complete

总计划见 `2026-10-26-next-linux-os-migration.md`，上一批见 `2026-10-26-linux-batch1-processes.md`。源笔记、图片和 `assets/Linux/` 全部保留。

## 现状

- 12 篇约 290 行。`memory_mappings`、`shared_memory`、`memory_leak` 只有标题，`sbrk`、`malloc`、`memory_allocation` 只有几行；`garbage_collection` 实为内存回收（kswapd、水位线、NUMA 回收），与 GC 无关。
- 范围外入链（`contents.org` 不计，旧根已于批次 1 迁移）：
  - `memory_hierarchy` `d734bb0e` ← `computer_hardware`（批次 8）
  - `memory_mappings` `c2e41773`、`shared_memory` `681a06e2` ← `tmpfs`（批次 3）
  - `swap` `0bff214a` ← `sysstat`（批次 5）
  - `garbage_collection` `065d6f74` ← `proc_zoneinfo`（批次 4）
- 旧笔记中指向不存在 ID 的链接：Swap `fbf5ab03`、NUMA `aafc265a`、`/proc/sys/vm/swappiness` `e6a25528`、`/proc/zoneinfo` `38af873a`、`min_free_kbytes` `c6678eb9`、 ~brk()~ `3aed7004`、 ~mmap()~ `5a01f28f`。新笔记中不保留。

## 归属与调整

- 全部归 `Linux/`，新建中间索引 Linux Memory，沿用旧根 Memory 标题的 ID `bcae4642`。
- `memory_hierarchy`（`:Hardware:`，CPU 缓存层级）移到批次 8：内容是硬件而非 Linux，唯一范围外入链来自批次 8 的 `computer_hardware`，硬件归属本就在批次 8 与用户确认。已在总计划中移动。
- `memory_leak` 为空：泄漏的定位属于排障，留给批次 4 的 `memory_troubleshooting`；本批废弃其 ID（无入链）。

## 目标树

11 篇 → 5 篇笔记 + 1 个索引。`←` 后为并入的旧笔记。

```
Linux (4f8f2615)
├─ Linux Processes
├─ Linux Scheduling and Kernel Entry
└─ Linux Memory (旧根 Memory 标题 bcae4642，改为独立索引文件)
    ├─ Linux Process Address Space (process_memory_model c864c39e)
    ├─ Linux Virtual Memory and Page Faults (virtual_memory 4dc805d4) ← 旧根 Memory 下的 Types（VIRT / RES / SHR / Swap）
    ├─ Linux Memory Mappings (memory_mappings c2e41773；标题 Linux Shared Memory 保留 681a06e2)
    ├─ Linux Memory Allocation with malloc (memory_allocation f659b32b) ← malloc, sbrk
    └─ Linux Memory Reclaim (garbage_collection 065d6f74；标题 Linux Swap 保留 0bff214a) ← out_of_memory
```

出度：根 3，Memory 5。深度 3。

笔记间横向链接（单向，使用方 → 被使用方）：Address Space → Virtual Memory；Allocation → Address Space、Memory Mappings；Memory Mappings → Virtual Memory；Reclaim → Memory Mappings（文件页 / 匿名页）。范围外：C++ Dynamic Memory Allocation → Address Space、Allocation；Trading 的 Low Latency Trading Design → Virtual Memory（缺页、锁页、大页）。

## 改造原则

- 补核心模型（能判断）：按需分页与缺页（minor / major）、页表在内存而 TLB 是缓存、overcommit 与 RSS、大页与 TLB、热路径预缺页（ ~mlockall~ 、 ~MAP_POPULATE~ ）；文件 / 匿名、私有 / 共享两个维度的映射分类与 COW；POSIX 共享内存与 =/dev/shm= ；malloc 的 brk / mmap 阈值（动态调整）、arena、内存不归还系统的原因；回收的文件页 / 匿名页、水位线与直接回收、swappiness 的真实含义、OOM 选择与 ~oom_score_adj~ 。
- 删去：创建 swap 文件的命令、休眠、 ~sar~ 输出字段（批次 5 的工具地图处理）、教材式 L1/L2 描述（随 `memory_hierarchy` 去批次 8）。
- 图：进程地址空间布局改画 PlantUML；旧截图不复制。

## 已发现的旧笔记错误（已核对，新笔记已改正）

- 「页表实际上存储在 CPU 的 MMU 中」：页表在内存里，MMU 遍历页表，TLB 缓存翻译结果。
- 「只读段：Text+Data；数据段：BSS」：只读段是代码和只读常量（.text、.rodata），数据段是 .data，BSS 另列。
- 「栈大小固定，一般是 8MB」：主线程栈按需增长，上限是 ~RLIMIT_STACK~ （默认 8 MiB）；线程栈在创建时固定。
- 「小于 128K 用 brk，大于用 mmap」：128 KiB 是 ~M_MMAP_THRESHOLD~ 的初始值，释放 mmap 块后会动态上调；非主线程的 arena 不用 brk。
- 「brk 分配的内存不归还系统」：堆顶空闲超过 ~M_TRIM_THRESHOLD~ 时会收缩，只是中间的空洞还不回去。
- ~sbrk~ 是系统调用：Linux 上只有 ~brk~ 是系统调用， ~sbrk~ 是 glibc 函数。
- 「占用 CPU 越多 =oom_score= 越小」：2.6.36 起 OOM 评分只看内存占用（RSS、swap、页表）加 ~oom_score_adj~ 。 ~oom_adj~ （-17–15）已废弃，用 ~oom_score_adj~ （-1000–1000）。
- 水位线 =low= = 5/4 =min= 、 =high= = 3/2 =min= ：现行内核由 ~watermark_scale_factor~ 决定间距。
- 「剩余内存小于 pages_min：仅内核可分配」：低于 =min= 时普通分配进入直接回收，只有特殊分配可以动用 =min= 以下的保留。
- 「常驻内存不包括共享内存」（旧根 Types）：RES 包含已映射的共享页和文件页，SHR 是 RES 的一部分。
- swappiness 被描述为「Swap 的积极程度」：它是回收时匿名页相对文件页的 I/O 代价权重（0–200），设 0 也不完全禁止 swap。

## Checklist

- [x] 批次 1 卡片补做：`ankinotes/linux.org` 13 张
- [x] 核对（scratchpad `linux2/`，本机无 strace，用地址范围和 ~mallinfo2~ 判断）：malloc 100 KiB 走堆、200 KiB 走 mmap、释放后同样大小走堆、40 MiB 走 mmap；线程中 malloc 地址在映射区；线程栈 8 MiB；256 MiB 首次写 65,536 次次缺页 115 ms（约 1.5 µs/次），二次写 12.7 ms； ~MAP_POPULATE~ 后写入 0 缺页；THP madvise 在碎片化时只得 4 MiB 大页、首次写 612 ms；堆顶留存活块时 free 不降 RSS， ~malloc_trim~ 后 11.8 MB → 1.9 MB；VmRSS = RssAnon + RssFile + RssShmem；overcommit 0 下 mmap 60 GiB 成功、70 GiB 失败（31 GiB + 32 GiB swap）；水位线间距 7,705 页 ≈ managed × 10/10000，zoneinfo 值含 boost；本机 swappiness 100（上游 60）、THP always / defrag madvise、memlock 8 MiB、/dev/shm 1 GiB、ASLR 2。（注：GCC -O1 会删掉未使用的 malloc/free 对，第一次 overcommit 测试因此误报成功，改用 mmap 测）
- [x] 笔记 5 篇 + 索引 1 个，根索引接入
- [x] C++、Trading 笔记中加入指向新笔记的引用；批次 1 的 Processes vs Threads「进程 + 共享内存」一行链到 Linux Shared Memory
- [x] 本批卡片：16 张，`ankinotes/linux.org` 共 29 张
- [x] 总计划：批次 2 勾选，`memory_hierarchy` 移入批次 8
- [x] 验证：无笔记需要 TOC（一级最多 5 个、无二级）；行内标记检查为空（含卡片）；block 配平；ID / 标题 / 别名无重复；链接目标全部存在；主树可达、唯一父节点，出度根 3 / Memory 5；无互链（VM → Reclaim → Mappings → VM 为单向环）、无指向索引或祖先的正文链接；地址空间布局图渲染并补上 `#+RESULTS:`，已目检
- [x] `org-roam-db-sync`（临时 daemon `cc-sync`）：361 节点，其中 Linux 19；无悬空 ID 链接

## 废弃 ID

| 旧笔记 / 标题 | ID | 内容去向 |
|---|---|---|
| process_memory_model 的 Stack / Heap 标题 | `683abe49…` `e3867163…` | Linux Process Address Space |
| malloc | `53b16537…` | Linux Memory Allocation with malloc |
| sbrk | `409ebbc5…` | 同上 |
| out_of_memory | `0b2a6ecf…` | Linux Memory Reclaim → OOM |
| memory_leak | `3af97811…` | 空笔记，批次 4 处理泄漏排障 |

`memory_hierarchy`（`d734bb0e…`）及其 Caches 标题（`9a304aa0…`）不废弃，随批次 8 迁移。

## 指向未迁移笔记的链接

新笔记中没有。批次 3 迁移 `tmpfs`、批次 4 迁移 `proc_zoneinfo`、批次 5 迁移 `sysstat`、批次 8 迁移 `computer_hardware` 时，它们指向本批保留的 ID（`c2e41773`、`681a06e2`、`065d6f74`、`0bff214a`）会自动恢复；`computer_hardware` → `memory_hierarchy` 在批次 8 一起迁移。

## 给后续批次

- 批次 3：tmpfs 链到 Linux Memory Mappings 和标题 Linux Shared Memory；页缓存笔记是 Reclaim 中「文件页」的展开，由页缓存笔记引用 Reclaim 或反之，选一个方向。
- 批次 4：内存指标、内存排障吸收 `memory_leak` 的主题（泄漏 vs 碎片的判断已在 Allocation 的「观察」中写了两句）； `proc_zoneinfo` 可并入 Reclaim 的水位线一节或由排障笔记引用。
- 批次 5：sar -r / -S、-B 的字段只在工具地图中写，链到 Reclaim。
