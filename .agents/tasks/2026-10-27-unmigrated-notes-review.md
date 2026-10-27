# 已完成迁移中未迁的笔记（待复查）

Status: Open，等用户逐篇检查

C++、Trading 和 Linux/OS 三次迁移完成后（以及剩余笔记迁移计划中），源笔记全部留在 `roamnotes/` 作备份。下面前 6 篇是这三次迁移的范围内、经决定 *没有迁入* `roamnotes-v2/` 的笔记，后 8 篇是剩余笔记迁移计划中决定不迁的个人内容，与已迁移的备份区分开。用户检查后决定：迁入（按 note-migration skill，保留原 ID），或确认不迁。

`Default/` 其余未迁笔记由 `2026-10-27-remaining-categories-migration.md` 统一规划；其中决定不迁的个人内容（书、英语、游戏）也列在本清单。

## 清单

| 旧笔记 | ID | 内容 | 不迁原因 | 若要迁移 | 来源 |
|---|---|---|---|---|---|
| `C++/zeromq-20241224.org` | `5521b2f9-f8ea-44d3-887a-1e9190e366f7` | ZeroMQ 套接字的开销（序列化、IPC 缓冲、内存拷贝） | *延后* ：要与 `Default/zeromq-20250730.org`、`Default/pub_sub_pattern` 一起合并，归属未定 | 迁移 `Default/` 的网络或系统设计笔记时合并三篇，保留此 ID；`Default/system_design` 有入链指向它 | `2026-10-26-cpp-migration.md` |
| `C++/c_literals-20250220.org` | `93ea9dcc-19c5-43cf-8695-7d75e0e07522` | 整数、浮点、字符字面量的写法 | 可查询的语法细节 | 并入 C++ Language Basics 一行即可 | 同上 |
| `C++/istringstream-20230811.org` | `2eb32af4-4617-48c6-a5cb-d945ff3e494d` | 用 ~std::istringstream~ 从字符串读取数据 | 可查询的 API；C++ STL Algorithms and Ranges 已建议解析数字用 ~std::from_chars~ | 通常不需要 | 同上 |
| `C++/static_local_variable-20250403.org` | `bdaf53b0-a247-45a1-b7fb-278fbcbabb2b` | 空笔记，只有标题 | 无内容 | 无需迁移；函数内 ~static~ 的线程安全初始化已写进 C++ Mutexes, Locks and Deadlock | 同上 |
| `Default/motherboard-20240929.org` | `4baf1454-8d95-40de-ac60-2a13a4eeae60` | 南北桥、扩展槽、ATX / ITX 规格、HDD / SSD 与 SATA / NVMe 接口、电源、USB 各代速率、设备接口截图 | PC 装机课程（IT 支持类）的可查询事实，不在任何学习目标内（用户 2026-10-27 决定） | 写新内容接到 Linux 的 CPU and Memory Hardware 下 | `2026-10-27-linux-batch8-hardware-python-profiling.md` |
| `Default/computer_display-20241017.org` | `04eccc31-b7a3-4ba3-870e-64f7640bc447` | LCD（IPS / TN / VA）与 OLED 的分类 | 同上 | 同上 | 同上 |
| `Default/atomic_habits-20230820.org` | `ee0201ca-ae34-4fea-b3bc-b19882a836b3` | Atomic Habits 读书笔记（四定律、身份、习惯回路） | 个人内容，不属于知识库（用户 2026-10-27 决定） | 需要时另建个人类别 | `2026-10-27-remaining-categories-migration.md` |
| `Default/books-20230820.org` | `ce0a94cd-1c99-4a35-ac22-bd6ee5bf848e` | 书单索引，只链 Atomic Habits | 同上 | 无需迁移 | 同上 |
| `Default/english-20240915.org` | `2eee25fc-6420-4bdd-a0bd-092f26d52b63` | 条件句、关系代词截图 | 同上 | 同上 | 同上 |
| `Default/english_grammar-20240915.org` | `60538ae7-b57d-426f-a57a-71978db0d076` | 从句截图 | 同上 | 同上 | 同上 |
| `Default/have_fun-20230820.org` | `b4a3d870-9446-4fb2-8cd3-12d57bbf056e` | 游戏索引，只链 Warhammer3 | 同上 | 无需迁移 | 同上 |
| `Default/oxygen_not_included.org` | `dcc27a97-92dc-4e4f-ae2a-d0a8979a05c7` | 缺氧开局安排与技巧 | 同上 | 需要时另建个人类别 | 同上 |
| `Games/mc_server-20240721.org` | `f75bc364-5441-414d-b48d-5e35c41ca0ec` | PaperMC / Forge 服务器安装 | 同上 | 同上 | 同上 |
| `Games/warhammer3-20230820.org` | `35ca03c6-3482-48e7-9577-3bc2a218ff26` | 战锤 3 高精种族、法术、亲随 | 同上 | 同上 | 同上 |

另有一处部分内容未迁：`Default/computer_hardware` 的 Architecture、Glossary 两节（CPU、内存控制器与内存的截图，MCC、地址总线、时钟、POST、UEFI 等词汇）。该文件的 ID 已用作新索引 CPU and Memory Hardware。

## Checklist

- [x] ZeroMQ（C++）：已在剩余笔记迁移批次 3 中与 `Default/zeromq` 合并为 SystemDesign 的 ZeroMQ Messaging Patterns（保留 `5521b2f9`），Pub/Sub 并入 Message Queues and Pub/Sub
- [ ] Literal
- [ ] ~std::istringstream~
- [ ] Static Local Variable
- [ ] Motherboard
- [ ] Computer Display
- [ ] 个人内容 8 篇（Atomic Habits、Books、English、English Grammar、Have Fun、Oxygen Not Included、MC Server、Warhammer3）
