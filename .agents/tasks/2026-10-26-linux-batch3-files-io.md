# Linux 迁移批次 3：文件系统与 I/O

Status: Complete

总计划见 `2026-10-26-next-linux-os-migration.md`，上一批见 `2026-10-26-linux-batch2-memory.md`。源笔记、图片和 `assets/Linux/` 全部保留。

## 现状

- 18 篇约 640 行。`file_system`、`file_i_o`、`file_io_buffering` 是 TLPI / APUE 的摘抄（约 400 行，大半是 API 签名和 flag 列表）；`hard_link`、`file_descriptor`、`dentry`、`inode`、`i_o_multiplexing` 只有几行；`system_caches` 与 `page_cache` 内容重复；`special_files` 实为 `/proc` 文件和 =/dev/fd= 的零散记录。
- 范围外入链：只有已迁移的旧根 `linux`（→ `file_system`、`file_sharing`、`special_files`、`i_o`）和批次 1 已迁移的 `system_calls`（→ `file_i_o`），`contents.org` 不计。新库中没有指向本批 ID 的链接。
- 本批旧笔记的出链：`tmpfs` → Shared Memory `681a06e2`、Memory Mappings `c2e41773`（批次 2 保留，已存在）；`i_o` → I/O Metrics `f44727ab`、I/O Troubleshooting `ed3469d5`、I/O Optimization `f593c3a7`（批次 4），I/O System Calls `203da24b`（全库不存在）。

## 归属与调整

- 全部归 `Linux/`，新建中间索引 Linux Files and I/O，沿用旧 `i_o` 的 ID `603a0f71`（旧 `i_o` 本身就是 I/O 的分组页）。
- I/O 多路复用留在 `Linux/`：它是内核的 fd 就绪通知接口，管道、终端、socket 通用，面试也按「Linux I/O 模型」问；`Network/` 的笔记需要时引用它（批次 7 处理 Linux 网络栈时）。
- `special_files` 拆散：=/proc/interrupts= 、 =/proc/softirqs= 已在批次 1 的 Interrupts and Softirqs 中； =/proc/stat= 等 =/proc= 指标归批次 4 的 `proc` 系列；=/dev/fd= 并入 File Descriptors。ID 废弃。

## 目标树

18 篇 → 6 篇笔记 + 1 个索引。`←` 后为并入的旧笔记。

```
Linux (4f8f2615)
├─ Linux Processes
├─ Linux Scheduling and Kernel Entry
├─ Linux Memory
└─ Linux Files and I/O (i_o 603a0f71，改为独立索引文件)
    ├─ Linux File System Structure (file_system 72e5eb39；标题 Linux tmpfs 保留 52cc876c)
    │     ← virtual_file_system, inode, dentry, hard_link, journaling_file_systems, tmpfs
    ├─ Linux File Descriptors and Open Files (file_descriptor 937b44b4)
    │     ← file_sharing, file_i_o 的 Open File Table / dup / fcntl / =/dev/fd= 部分, special_files 的 =/dev/fd=
    ├─ Linux Page Cache and Writeback (page_cache a20150eb) ← system_caches, dirty_pages
    ├─ Linux File I/O Buffering and Durability (file_io_buffering c7ce9028)
    │     ← file_i_o 的 read / write / sync 部分（stdio 缓冲、fsync、O_SYNC、O_DIRECT、fadvise）
    ├─ Linux Block Layer and I/O Stack (block_layer d5d10c24) ← i_o 的 I/O 栈与三层划分
    └─ Linux I/O Models and Multiplexing (i_o_multiplexing 6a9a7f5c)
          ← i_o 的 I/O Op Types 与 C10K, file_i_o 的 Nonblocking I/O
```

出度：根 4，Files and I/O 6。深度 3。

笔记间横向链接（单向，使用方 → 被使用方）：

- 本批内：Buffering → Page Cache（fsync、O_DIRECT 绕过谁）；Page Cache → Block Layer（回写下发）；File System Structure → Page Cache（inode / dentry 缓存与页缓存的区别）；I/O Models → File Descriptors（非阻塞是 open file description 的状态标志）。
- 与已迁移笔记：Page Cache → Linux Memory Reclaim（文件页的回收，批次 2 留下的方向选择）；tmpfs → Linux Memory Mappings、Linux Shared Memory；Linux Memory Mappings 中「写入进入页缓存」→ Page Cache；Linux System Calls 「事件通知」行 → I/O Models；Linux Process Lifecycle 的 ~O_CLOEXEC~ 一句 → File Descriptors。

## 改造原则

- 补核心模型（能判断）：
  - 文件系统：VFS 四个对象（superblock、inode、dentry、file），文件名属于目录项而不是 inode，硬链接 / 软链接 / 删除仍打开的文件，rename 原子替换，日志的三种模式（ext4 ~data=ordered~ ），tmpfs 的内存与 swap。
  - fd：三张表；fd 标志（ ~FD_CLOEXEC~ ）与状态标志（ ~O_APPEND~ 、 ~O_NONBLOCK~ ）的作用范围；dup / fork / 各自 open 是否共享偏移量；fd 泄漏。
  - 页缓存：读缓存与预读、写回（脏页阈值、30 秒过期、回写线程）、写入被节流导致的延迟尖峰、 =Buffers= / =Cached= 的含义、 ~drop_caches~ 。
  - 持久化：数据经过的三级缓冲（stdio → 页缓存 → 磁盘缓存）、 ~fflush~ 与 ~fsync~ 的区别、 ~fdatasync~ 、 ~O_SYNC~ / ~O_DSYNC~ 、安全写文件（写临时文件 → fsync → rename → fsync 目录）、 ~O_DIRECT~ 的用途与对齐、 ~posix_fadvise~ 。
  - 块层：I/O 栈全貌、合并与调度、多队列调度器（none / mq-deadline / bfq / kyber）的选择、HDD 与 SSD 的代价差异。
  - I/O 模型：阻塞 / 非阻塞是「数据没准备好时调用怎么办」，同步 / 异步是「谁完成拷贝」；多路复用是同步 I/O；select / poll / epoll 对比；LT / ET 与 ET 必须读到 ~EAGAIN~ ；普通文件不支持 epoll 且非阻塞无效，所以文件异步 I/O 用 io_uring 或线程池。
- 删去：API 签名与示例程序、 ~fcntl~ 命令列表、挂载叠加、 =/etc/mtab= 、文件系统基准清单、 ~hdparm~ 命令、 ~O_RSYNC~ 、 ~creat~ 、 ~setvbuf~ 参数细节（只留三种缓冲模式和默认规则）。
- 图（PlantUML，旧截图不复制）：fd 三张表、写回时序、I/O 栈。

## 已发现的旧笔记错误（已核对，新笔记已改正）

- 「 ~O_NONBLOCK~ 对普通文件被忽略，因为缓存保证普通文件 I/O 不阻塞」：页缓存未命中时读照样阻塞（进程处于 D 状态）， ~O_NONBLOCK~ 只是不起作用。
- 「I/O 多路复用：异步、非阻塞 IO」：多路复用等的是就绪通知，之后的 ~read~ 仍是同步拷贝，属于同步 I/O。
- 「脏页由内核线程 ~pdflush~ 刷新」：2.6.32 起换成按设备的回写线程（ =kworker/u*:*-flush-*= ）。
- 「CFQ 是很多发行版的默认 IO 调度器」：CFQ、deadline、noop 随旧块层在 5.0 移除，现在是 none、mq-deadline、bfq、kyber。
- 「 ~sync()~ 只把修改排队就返回」（APUE 的 POSIX 描述）：Linux 的 ~sync~ 等写完才返回。
- 「inode 会缓存到页缓存中」：内存中的 inode 和 dentry 在 slab 缓存（ =ext4_inode_cache= 、 =dentry= ），不在页缓存。
- 「inode 是每个文件的唯一标识」：只在同一文件系统内唯一，全局要用（设备号, inode 号）。
- 「磁盘有内部缓存时 ~O_SYNC~ 只把数据送到磁盘缓存」：开启写屏障（默认）时，内核对有易失性写缓存的设备发 flush / FUA，fsync 会落到持久存储。
- 「Direct I/O 按物理块大小（通常 512 字节）对齐」：按设备的逻辑块大小（512 或 4096），Linux 6.1 起可用 ~statx~ 的 ~STATX_DIOALIGN~ 查询。
- =/proc/softirqs= 中「SCHED：非自愿上下文切换」：SCHED 软中断做调度器的负载均衡，与非自愿切换无关。
- 「打开 =/dev/fd/n= 等效于复制描述符 n」（APUE）：Linux 上是重新 ~open~ 该文件，得到新的打开文件描述（本机实测偏移量 10 → 0）。

## Checklist

- [x] 核对（scratchpad `linux3/`）：dup 共享偏移（读 3 后 dup 的偏移为 3）、fork 子进程读 2 后父进程偏移为 5、再次 open 偏移为 0； ~O_NONBLOCK~ 随 dup 生效而 ~FD_CLOEXEC~ 不随； ~O_APPEND~ 下 lseek 到 0 再写仍追加；=/dev/fd/n= 是重新打开；链接数 1 → 2 → 0 后 fstat 仍可读、 =/proc/self/fd= 显示 =(deleted)= ；普通文件 ~O_NONBLOCK~ 读正常、加入 epoll 返回 ~EPERM~ ；管道上 LT 读一半仍报告、ET 不报告直到新数据；stdio：终端 stdout 行缓冲 1024 B、文件全缓冲 4096 B（ =st_blksize= ）、stderr 无缓冲；256 MiB 写入页缓存 0.11 s、fsync 0.54 s、DONTNEED 后 mincore 为 0、冷读 8.4 s / 热读 0.04 s；1 字节写 + fdatasync 平均 54 ms（btrfs，机械盘）；btrfs 上不对齐 ~O_DIRECT~ 静默成功、 ~STATX_DIOALIGN~ 不返回；tmpfs 上 ~O_DIRECT~ 打开返回 ~EINVAL~ （未写入笔记）；io_uring_setup 可用、 ~kernel.io_uring_disabled~ 在 6.5 不存在。本机：dirty_bytes 400 MB / dirty_background_bytes 200 MB（ratio 读出为 0）、expire 3000、writeback 500；NVMe 调度器 none、sda / sdb bfq、sdc mq-deadline；所有盘 write_cache 为 write back；ulimit -n 65535；/dev/shm 1 GiB；根分区 btrfs。无 ext4 / xfs 可写挂载，ext4 / xfs 上不对齐 ~O_DIRECT~ 返回 ~EINVAL~ 按 open(2) 写。
- [x] 笔记 6 篇 + 索引 1 个，根索引接入
- [x] 已迁移笔记中的横向链接：Memory Mappings → Page Cache，System Calls → I/O Models，Process Lifecycle → File Descriptors
- [x] 本批卡片：19 张，`ankinotes/linux.org` 共 48 张
- [x] 总计划：批次 3 勾选
- [x] 验证：无笔记需要 TOC（一级最多 5 个、二级最多 1 个）；行内标记检查为空（含卡片）；block 配平；ID / 标题 / 别名无重复；链接目标全部存在；主树可达、唯一父节点，出度根 4 / Files and I/O 6；去掉了 Page Cache ↔ Buffering 的互链（保留 Buffering → Page Cache）；无指向索引或祖先的正文链接；3 张 PlantUML 图渲染并补上 `#+RESULTS:` ，已目检（I/O 栈图中 NFS 改为经页缓存）
- [x] `org-roam-db-sync`（临时 daemon `cc-sync`）：468 节点，其中 Linux 27；无悬空 ID 链接

## 废弃 ID

| 旧笔记 / 标题 | ID | 内容去向 |
|---|---|---|
| virtual_file_system | `808b8114…` | Linux File System Structure |
| inode | `d81b6ab9…` | 同上 |
| dentry | `3876fd6e…` | 同上 |
| hard_link | `537013df…` | 同上 |
| journaling_file_systems | `06344419…` | 同上 |
| file_sharing | `be6c0364…` | Linux File Descriptors and Open Files |
| special_files | `d39a009f…` | =/dev/fd= → File Descriptors；=/proc= 部分 → 批次 4 / 已在批次 1 |
| system_caches | `93b82365…` | Linux Page Cache and Writeback |
| dirty_pages | `7910f1b4…` | 同上 |
| file_i_o（`[SC] I/O`） | `dfdba3bb…` | Buffering and Durability / File Descriptors；API 部分删去 |
| file_i_o 的 Open File Table、Nonblocking I/O、/dev/fd 标题 | `cdcabfaf…` `2fff5bbd…` `02b1924c…` | File Descriptors；I/O Models |
| i_o 的 I/O Op Types 标题 | `d48ec305…` | Linux I/O Models and Multiplexing |

以上 ID 在迁移范围外均无入链（旧根和 `system_calls` 已迁移）。

## 指向未迁移笔记的链接

新笔记中没有。旧 `i_o` 指向的 I/O Metrics、Troubleshooting、Optimization 在批次 4 迁移，届时由它们引用本批笔记（观测 → 机制），不反向链接。

## 给后续批次

- 批次 4：I/O 指标、I/O 排障、I/O 优化引用本批笔记（ ~iostat~ 的 await / %util 读法、页缓存命中、D 状态进程），不反向链接；「删除仍打开的文件」「inode 耗尽」已在 File System Structure 中，排障笔记链过去即可。 =/proc/stat= 等原 `special_files` 的内容归 `proc` 系列。
- 批次 5：fio、iostat、 ~fincore~ / ~vmtouch~ 、 ~lsof~ 只写在工具地图里，链到本批的概念笔记。
- 批次 7：Linux 网络栈笔记引用 Linux I/O Models and Multiplexing（socket 的就绪通知、忙轮询）。
