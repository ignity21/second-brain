# 下一轮迁移：Linux / OS（来自 `Default/`）

Status: Not started

2026-10-26 Trading 迁移后，用户同意下一轮迁移 `roamnotes/Default/` 中的 Linux / OS 笔记。本文件只记录选择理由和交接事项，归属方案和目标树由下一轮按 note-migration skill 制定。

## 为什么选它

- C++、Trading 迁完后，旧库只剩 `Default/`（243 篇）和 `Games/`（2 篇）；Linux 一组在 `Default/` 中最大。
- 有待接的线：C++ 迁移把栈 / 堆 / 静态区的通用内容留给 `Default/process_memory_model`；它指向 C++ Memory Allocation 的入链等它迁移后才算接上。
- 与学习目标相关：内核旁路、核绑定、系统调用、性能调优服务于 C++ 低延迟和交易系统开发（见 `.agents/learning-goals.md`）。

## 范围（待确认）

`filetags` 含 `Linux`、`OS`、`SystemCall`、`Performance`、`Hardware` 的笔记约 103 篇，其中一部分属于网络（`linux_network_stack`、`tcp_ip_layers`、`iptables`、`iperf3`、`network_tools` 等，应并入现有 `Network/`），一部分是命令行工具（awk、sed、grep、curl、cron，可能归 Tools 一类或大幅压缩）。

规模较大，开始时先：

1. 与用户确认 Linux 子领域的学习目标（尚无记录）；
2. 划定本轮范围，可按主题分批：进程与内存 → 文件系统与 I/O → 性能工具与排障 → 硬件；
3. 查已有 `Network/Linux Network Tools`（`network_tools.org`）等节点，避免重复。

## 上一轮遗留

C++ 和 Trading 的 Anki 卡片另见 `2026-10-26-cpp-trading-anki-cards.md`，与本轮迁移互不依赖。
