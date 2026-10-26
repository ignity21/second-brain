# Linux 迁移批次 7：Linux 网络

Status: Complete

总计划见 `2026-10-26-next-linux-os-migration.md`，上一批见 `2026-10-27-linux-batch6-admin-shell.md`。源笔记保留。

## 现状

- 7 篇约 160 行：`linux_network_stack`（44 行，收发包流程 + 一张分层图）、`iptables`（36 行，选项速查 + 速查截图）、`network_tools`（旧工具索引）、`tcp_ip_layers`（分层表 + 5 个分层子笔记链接）、`network`（旧网络索引）、`iperf3`（14 行）、`pktgen`（一句话）。
- 入链：
  - `iptables` `cee785fb` ← `firewall`、`nftables`（均未迁移，不在本计划）。
  - `pktgen` `663e9802` ← `network_troubleshooting`（未迁移）。
  - `network_tools` `53273a0c` ← 旧 `network`、`linux_tools`（批次 5 已迁移，v2 中无引用）。
  - 其余入链只来自本批的旧 `network` 索引。
- 出链到未迁移笔记：`tcp_ip_layers` → 5 篇分层笔记（physical / data link / network / transport / application layer）；`network` → `network_troubleshooting`、`firewall`；`network_tools` → `ip`、`netcat`、`hping3`、`gost`。
- 资源：`assets/Linux/LinuxNetworkStack_1.png`（分层框图）、iptables 速查截图。
- 学习目标：网络栈收发路径属于面试高频 + 低延迟（中断、软中断、多队列、忙轮询、内核旁路），「能判断」；iptables 属于自用服务器管理，「知道」，留模型和坑；iperf3 / pktgen 是工具，「知道」。网络领域偏好：列出相关 sysctl / socket 选项，上游默认与本机值分开写。

## 归属与调整

- 全部并入 `Network/`。新建中间索引 *Linux Kernel Networking* （新 ID `1921bccf-d469-491a-8e2f-cc0997db17cb`），接在 Computer Networking 根下（出度 3 → 4）。现在只有 2 个子节点，保留理由：稳定领域边界，后续网络计划中的 nftables、ufw、firewall、ip route / rule、NAT 预计并入此处。
- 7 篇 → 3 篇 + 1 处合并：
  - *Linux Network Stack Receive and Transmit Paths* （保留 `linux_network_stack` 的 ID `f226240d`）：收发两条路径上包在哪些队列里等、在哪里丢、各看哪个计数器；拷贝次数；多队列扩展（RSS / RPS / RFS / XPS）；延迟相关可调项（中断合并、忙轮询、NAPI 预算）；内核路径与内核旁路的对比。硬中断 / 软中断 / NAPI 的细节已在 Linux Interrupts and Softirqs，只链接。分层框图不迁，改为 PlantUML 画收发路径。
  - *Linux Netfilter and iptables* （保留 `iptables` 的 ID `cee785fb`）：五个 hook、表与链、规则顺序与默认策略、conntrack；DROP 与 REJECT；坑（ ~-F~ 不重置策略、 ~-A~ 加在兜底规则之后、规则不持久、iptables-nft 与 legacy、Docker 绕过 INPUT）；nftables / ufw / firewalld 的定位。选项速查和截图不迁。
  - *Network Performance Testing with iperf3 and pktgen* （保留 `iperf3` 的 ID `87bbc997`；pktgen 一节保留 `663e9802` 作标题级节点，因有未迁移的 `network_troubleshooting` 入链）：测什么指标用什么工具；iperf3 的坑（UDP 默认 1 Mbit/s、单流受限于单核和窗口、3.16 前单线程、回环测的是内存拷贝）；pktgen 在驱动发送处注入，测的是网卡 / 驱动的 PPS。接在 Linux Network Tools 下（出度 2 → 3）。
  - `tcp_ip_layers`：并入现有 *Network Layers and Data Units* （`72d3cced`），只补「寻址」一列（端口 / IP 地址 / MAC 地址），其余内容已覆盖。
  - `network`、`network_tools`：旧索引，废弃，由 Computer Networking 根、Linux Network Tools 承接。
- 资源：全部不迁（框图改 PlantUML，速查图可查询）。

## 目标树

```
Computer Networking (855d4ede)
├─ Fundamentals (13ee1f3a)
│   └─ Layers and Data Units (72d3cced) ← 吸收 tcp_ip_layers
├─ TCP (ac00f69d)
├─ Linux Kernel Networking (新 1921bccf)
│   ├─ Linux Network Stack Receive and Transmit Paths (f226240d)
│   └─ Linux Netfilter and iptables (cee785fb)
└─ Linux Network Tools (ca95e333)
    ├─ ss
    ├─ curl
    └─ Network Performance Testing with iperf3 and pktgen (87bbc997；pktgen 标题 663e9802)
```

笔记间横向链接（单向）：

- Stack → Linux Interrupts and Softirqs（硬中断 / 软中断 / NAPI、中断亲和性）、Network Layers and Data Units（MSS 与分片）、TCP Reliable Delivery and Flow Control（接收缓存与 rwnd、 ~tcp_rmem~ ）、Linux CPU Scheduling and Affinity（隔离核）。
- Netfilter → Stack（hook 在路径上的位置）、TCP Connection Management（REJECT 回 RST，DROP 让 SYN 重传到超时）。
- Performance Testing → Stack（pktgen 注入点）、TCP Reliable Delivery and Flow Control（单流吞吐受窗口 / RTT 限制）。

## 已发现的旧笔记错误（核对后改正）

- linux_network_stack 收包第 3–4 步「硬中断处理程序把帧转换为 ~sk_buff~ ，再通过软中断通知内核」：NAPI 驱动的硬中断只关中断、调度轮询；建 ~sk_buff~ 、GRO、交给协议栈都在 ~NET_RX~ 软中断的轮询里做。
- 传输层「数据拷贝到 Socket 的接收缓存中」：协议栈只把 ~sk_buff~ 挂到 socket 接收队列，不拷贝；拷贝到用户空间发生在应用调用 ~recv~ 时。
- 发包「按照 MTU 大小进行分片（网络层）」：TCP 按 MSS 分段，开启 TSO / GSO 时推迟到网卡或驱动前一刻；IP 分片只发生在 UDP、原始 socket 等超过 MTU 的数据报上（已在 Network Layers and Data Units 说明）。
- 发包「由软中断通知驱动程序」：通常在发送进程的上下文里经 qdisc 直接调用驱动的发送函数；qdisc 暂时发不出时才交给 ~NET_TX~ 软中断。发送完成由中断通知，在 NAPI 轮询中释放 ~sk_buff~ 。
- iptables ~-F~ 「Delete all tables」：只清空（默认 filter 表）各链中的规则，不删表和链，也不重置默认策略；策略为 DROP 时远程执行 ~-F~ 会把自己锁在外面。原文选项写成了 en dash（ =–A= ），复制会报错。

## Checklist

- [x] 核对（scratchpad `linux7/`）：内核文档 sysctl/net、scaling、pktgen；`net/core/hotdata.c` 的默认值；iptables 1.8.13 (nf_tables) 在 ~unshare -rn~ 的独立网络命名空间中验证 ~-F~ 保留策略、REJECT（curl 退出码 7）与 DROP（超时 28）、兜底 DROP 后的 ~-A~ 不生效、策略 DROP 时缺 ESTABLISHED 规则连回环都连不上；iperf3 3.19.1（临时 alpine 容器，用后删除镜像）UDP 默认约 1 Mbit/s。本机为非初始网络命名空间，读不到 ~net.core.netdev_*~ 等全局 sysctl，未写本机值；没有 pktgen 模块和 ethtool，pktgen 按内核文档写，未运行。
- [x] 另在临时容器中核对 iperf3 服务端一次只跑一个测试（ =the server is busy running a test= ）、 ~-u -b 0~ 不限速。
- [x] 笔记 3 篇 + 新索引 + Layers 补列，接入 Computer Networking 根（出度 4）、Linux Network Tools（出度 3）。pktgen 标题级节点题为 *pktgen Kernel Packet Generator* 。
- [x] PlantUML 渲染：`Network/images/` 下 `linux_network_receive_path.png`、`linux_network_transmit_path.png`、`linux_netfilter_hooks.png`
- [x] 本批卡片：15 张（Stack 8、Netfilter 5、Performance Testing 2），`ankinotes/network.org` 共 46 张
- [x] 总计划：批次 7 勾选
- [x] 验证：Stack 一级标题 7 个，加 ~TOC_1~ 并运行 `update_toc.py`；其余无需 TOC；行内标记检查为空（含卡片），含下划线的标识符改用 =~...~= ；block、property drawer 配平；ID / 标题 / 别名无重复；新 ID 只由各自唯一父节点的整行标题引用，正文链接不指向索引或祖先、无互链；图片链接均存在
- [x] `org-roam-db-sync`（临时 daemon `cc-sync`）：394 节点（与磁盘上的 =:ID:= 数一致）；悬空 ID 链接只有批次 5 的 `dd` 、 `ab` 两个预期的

## 废弃 ID

| 旧笔记 | ID | 内容去向 |
|---|---|---|
| tcp_ip_layers | `c9141191…` | Network Layers and Data Units（`72d3cced`） |
| network | `ad44f747…` | Computer Networking 根（`855d4ede`） |
| network_tools | `53273a0c…`（及标题 ID `ef27cd4e…`、`eb9a725c…`） | Linux Network Tools（`ca95e333`） |

以上 ID 在迁移范围外均无入链。

## 给后续网络计划

旧索引废弃后，以下未迁移笔记失去了旧父节点，迁移时按内容接入：

- 5 篇分层笔记（`physical_layer` `9cc87b0d`、`data_link_layer` `21ac3d90`、`network_layer` `bbb2c010`、`transport_layer` `3e7a0f6a`、`application_layer` `a591c2c0`）：原父节点 `tcp_ip_layers`，候选去向 Fundamentals 下或并入 Network Layers and Data Units。
- `network_troubleshooting` `d53d47ee`：网络指标（带宽、吞吐、PPS、延迟），可与 Network Performance Testing 合并或作其上一层；其中指向 `pktgen` 的链接对应本批的标题级节点 `663e9802`。
- `firewall` `2824b785`、`nftables` `df7a26d0`、`ufw`：并入或接在 Linux Kernel Networking 下，与 Linux Netfilter and iptables 合并时保留 `cee785fb`。
- `ip` `6f61b842`（及 `ip_route`、`ip_rule`）、`netcat` `94c3d3d6`、`hping3` `a07e73bd`、`gost` `4cfade54`：原父节点 `network_tools`，接到 Linux Network Tools 或 Linux Kernel Networking。
