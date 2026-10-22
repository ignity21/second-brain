# Network 层级与链接整理

Status: Complete

总任务见 `2026-10-22-v2-category-restructure.md`。初始检查：深度 3，问题 9（Fundamentals、Tools 单子节点；笔记两两互链）。Network 以外无引用。

用户 2026-10-22 确认：

- 树不变：Fundamentals、Tools 虽然只有一个子节点，但预期扩展（IP / 路由；tcpdump、ip），保留。
- 横向引用只留一个方向，由使用方指向被使用方：Reliable Delivery → Layers，Connection Management → Reliable Delivery，Congestion Control → Reliable Delivery，ss → 三篇 TCP 笔记。反方向的行内指引改成纯文字，Connections 中的反向条目删除。

## Checklist

- [x] Layers：去掉 → Reliable 的链接和空的 Connections 段
- [x] Reliable Delivery：去掉 → Connection、Congestion、ss
- [x] Connection Management：去掉 → Congestion、ss
- [x] Congestion Control：去掉 → Connection、ss
- [x] 验证：检查脚本、行内标记、临时库 org-roam-db-sync

Result: 问题 9→2，剩余 2 条是用户确认保留的单子节点索引（Networking Fundamentals、Linux Network Tools）。删除 10 条反向引用，Layers 的 Connections 段随之删除；Reliable Delivery 中指向拥塞控制的三处行内指引改成纯文字（窗口缩放一句补了带宽时延积的含义）。无行内标记问题；临时库 batch `org-roam-db-sync` 通过（305 节点，无悬空 ID 链接）；2026-10-22 用 Doom daemon 对真实 DB 执行了 `org-roam-db-sync`（305 节点，无悬空 ID 链接）。
