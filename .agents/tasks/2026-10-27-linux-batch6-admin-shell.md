# Linux 迁移批次 6：系统管理与 Shell

Status: Complete

总计划见 `2026-10-26-next-linux-os-migration.md`，上一批见 `2026-10-26-linux-batch5-tools.md`。源笔记保留。

## 现状

- 11 篇约 370 行：`shell_script`（176 行，大半是 Bash 语法速查）最多；`linux_bootstrap`、`startup_scripts`、`users_and_groups` 各 30–40 行；`cron`、`awk`、`sed`、`grep` 只有一张速查图；`shell_tips`、`system_time`、`curl` 各十几行。
- 入链：全部来自旧根 `linux` 和批次 5 已迁移的 `linux_tools`，迁移范围外没有入链。
- 出链：`system_time` → System Limits `505fb55e`（已迁为 Linux Resource Limits）。
- 资源：`Default/images/screenshots/Diagram/2024-09-22_17-23-38_screenshot.png`（启动流程图）、`assets/Linux/CronCheatsheet.png`、awk / sed / grep 三张 `Cheat_Sheet` 截图。
- 学习目标：Shell、cron、用户组、启动脚本只到「知道」，细节交给 AI；只保留模型和坑。`system_time` 涉及打时间戳，属于低延迟的「能判断」。

## 归属与调整

- Shell 不独立成大类，也不建子索引：「知道」档位下只剩两篇 Shell 笔记，与用户、cron、启动同属自用机器管理，合成一个中间索引。
- 新建中间索引 *Linux System Administration and Shell* （新 ID），接在 Linux 根下（出度 5 → 6）。
- 11 篇 → 8 篇：
  - *Linux Boot Process* （保留 `linux_bootstrap` 的 ID `2fd5f48e`）：固件 → 引导程序 → 内核 + initramfs → systemd → target 的流程（PlantUML 重画，不迁截图），启动慢、启动失败时看什么。删去原文第 4 步（程序装入内存）和 RAM 行列寻址的题外话。
  - *Linux Users, Groups and Credentials* （保留 `users_and_groups` 的 ID `2f57cc5e`）：内核只认数字 ID、名字由 NSS 映射；三个文件的分工；进程凭证在登录时确定（加组后要重新登录）；密码哈希格式。库函数清单和 ~crypt()~ 示例压缩为一句。
  - *Linux Scheduled Jobs with cron and systemd Timers* （保留 `cron` 的 ID `61298d1f`）：五个字段与「日」「星期」两字段的「或」语义，cron 的环境与 ~%~ 等坑，systemd timer 的对比。速查图不迁（可查询，且其中 =L= 、 =W= 、 =#= 、 =?= 不是 cron 的语法）。
  - *Shell Startup Files and Environment Variables* （保留 `startup_scripts` 的 ID `956bf88a`）：登录 / 交互 shell 读哪些文件；环境变量只经 ~execve~ 从父进程传给子进程，图形会话、systemd 服务、cron 为什么看不到 rc 文件中的变量。吸收 `shell_script` 的环境变量一节。
  - *Shell Scripting Pitfalls in Bash and Zsh* （保留 `shell_script` 的 ID `08fd1b02`）：只留坑——引号与分词、数组下标、 ~=~ 两侧空格、重定向顺序、整数运算、 ~$SHELL~ 与当前 shell。吸收 `shell_tips`。
  - *Text Processing with grep, sed and awk* （保留 `grep` 的 ID `3dc23ed1`）：三者的分工、正则方言（BRE / ERE / PCRE）、GNU 与 BSD 差异。吸收 `sed`、`awk`；三张速查图不迁。
  - *Linux Clocks and Time Measurement* （保留 `system_time` 的 ID `87695f72`）：墙钟、单调时钟、CPU 时间；测间隔用哪个时钟；TSC。接在 Linux Scheduling and Kernel Entry 下（出度 4 → 5）：与时钟中断、vDSO 同属内核时间机制。HZ / jiffies 已在 Linux CPU Scheduling and Affinity，只链接。
  - *curl for HTTP and TLS Debugging* （保留 `curl` 的 ID `6148d379`）：迁入 `Network/`，接在 Linux Network Tools 下（出度 1 → 2）。
- 资源：全部不迁（启动图改为 PlantUML，速查图可查询）。

## 目标树

```
Linux (4f8f2615)
├─ ...
├─ Linux Scheduling and Kernel Entry (d8350135)
│   ├─ ...（4 篇）
│   └─ Linux Clocks and Time Measurement (system_time 87695f72)
└─ Linux System Administration and Shell (新)
    ├─ Linux Boot Process (2fd5f48e)
    ├─ Linux Users, Groups and Credentials (2f57cc5e)
    ├─ Linux Scheduled Jobs with cron and systemd Timers (61298d1f)
    ├─ Shell Startup Files and Environment Variables (956bf88a)
    ├─ Shell Scripting Pitfalls in Bash and Zsh (08fd1b02)
    └─ Text Processing with grep, sed and awk (3dc23ed1)

Linux Network Tools (ca95e333)
├─ ss
└─ curl for HTTP and TLS Debugging (6148d379)
```

笔记间横向链接（单向）：

- Clocks → Linux CPU Scheduling and Affinity（HZ、 ~USER_HZ~ ）、Linux System Calls（vDSO 的代价）。
- Startup Files → Linux /proc and sysctl Interfaces（ =/proc/<pid>/environ= ）、Linux Process Lifecycle（ ~execve~ 传递环境）。
- Scheduled Jobs → Startup Files（cron 不读 rc 文件）。
- Boot Process → Linux CPU Scheduling and Affinity（ ~isolcpus=~ 、 ~nohz_full=~ 是启动参数）。

## 已发现的旧笔记错误（核对后改正）

- shell_script「双引号中 ~!~ 要写成 ~\!~ 」：Bash 双引号中的 ~\!~ 会保留反斜杠（ ~echo "hi\!"~ 输出 =hi\!= ）；历史展开只在交互 shell 中发生，脚本不需要转义；交互时用单引号。
- 「 ~var = value~ 是相等判断」：是以 =var= 为命令名、 === 和 =value= 为参数执行，报 =command not found= 。相等判断要在 ~[ ]~ / ~[[ ]]~ 中。
- 彩色输出 ~echo "\e[1;31m..."~ ：Bash 的 ~echo~ 默认不解释 ~\e~ （zsh 的解释），可移植写法是 ~printf~ 。
- 「环境变量是从父进程继承来的变量」：只有 ~export~ 过的变量进入环境、经 ~execve~ 传给子进程；未导出的 shell 变量不传。
- 「识别当前 Shell： ~echo $SHELL~ 」： ~$SHELL~ 是 =/etc/passwd= 中的登录 shell，不随当前运行的 shell 变化；看 ~$0~ 或 ~ps -p $$~ 。
- shell_tips ~[command] 2>&1 > grep keyword~ ：把输出写进名为 =grep= 的文件；且 ~2>&1 >file~ 的顺序让 stderr 仍去终端。应为 ~cmd 2>&1 | grep keyword~ 。
- 数组示例 ~${array[0]}~ ：zsh 数组下标从 1 开始；不加引号的 ~${array[@]}~ 会按空白再次拆分元素。
- users_and_groups「 =/etc/group= 中的 GID 指定组成员」：第四个字段的用户列表才是附加组成员；主组由 =/etc/passwd= 的 GID 字段决定。
- users_and_groups 密码哈希只写了 ~$6$~ （SHA-512）：Debian 11+、Fedora 35+ 默认 yescrypt（ ~$y$~ ）；本机 Arch 的 =login.defs= 为 SHA512。
- cron 速查图中的 =L= 、 =W= 、 =#= 、 =?= ：是 Quartz 等调度器的扩展，cronie / Vixie cron 不支持。
- linux_bootstrap 流程图「BIOS / UEFI 从 NVRAM 载入」：固件存放在主板的 SPI flash；NVRAM 保存的是启动项等设置。
- system_time「jiffy 是内核按轮转算法分配 CPU 的单位」：是旧内核（2.6 早期）的说法；CFS / EEVDF 的时间片与 HZ 无关（已在 Linux CPU Scheduling and Affinity 中改正），且内核可配置为无节拍（ ~NO_HZ~ ）。

## Checklist

- [x] 核对（scratchpad `linux6/`）：Bash 5.3.20 / zsh 5.9.2 的分词、数组下标、 ~$(( 5 / 2.0 ))~ 、通配无匹配、 ~"\!"~ 、 ~echo "\e"~ 、重定向顺序、 ~set -e~ 、 ~export~ ；GNU grep 3.12 的 ~\d~ 警告；时钟读取开销（ ~clock_gettime~ 各时钟、 ~rdtsc~ ）、 ~*_COARSE~ 精度 4 ms、4 线程的 real / user；libstdc++ ~high_resolution_clock~ == ~system_clock~ （ ~static_assert~ ）；curl 8.23 的 ~-v~ 输出、 ~--resolve~ 、 ~--connect-to ::IP:~ 、 ~-w~ 计时、 ~-f~ 退出码 22；systemd 262 的 ~systemd-analyze calendar~ 。本机没有 cron，cron 部分按 crontab(5) 写，未运行。
- [x] 笔记 8 篇 + 新索引，接入 Linux 根（出度 6）、Scheduling and Kernel Entry（出度 5）、Linux Network Tools（出度 2）。Users 笔记文件名改为 `linux_users_groups-20261027.org` （含 credentials 的路径被权限规则拒绝写入）。
- [x] PlantUML 渲染：`Linux/images/linux_boot_process.png`
- [x] 本批卡片：Linux 11 张（`ankinotes/linux.org` 共 90 张），curl 2 张（`ankinotes/network.org` 共 31 张）
- [x] 总计划：批次 6 勾选
- [x] 验证：Clocks 一级标题 6 个，加 ~TOC_1~ 并运行 `update_toc.py`；其余无需 TOC；行内标记检查为空（含卡片）；block 配平；ID / 标题 / 别名无重复；新 ID 只由各自唯一父节点的整行标题引用，正文链接不指向索引或祖先、无互链
- [x] `org-roam-db-sync`（临时 daemon `cc-sync`）：389 节点（与磁盘上的 =:ID:= 数一致），其中 Linux 46；悬空 ID 链接只有 `dd` 、 `ab` 两个预期的

## 废弃 ID

| 旧笔记 | ID | 内容去向 |
|---|---|---|
| shell_tips | `96dbc600…` | Shell Scripting Pitfalls in Bash and Zsh |
| awk、sed | `bced3ab6…` `9334e14b…` | Text Processing with grep, sed and awk |

以上 ID 在迁移范围外均无入链。

## 给后续批次

- 批次 7：curl 已迁入 `Network/`（Linux Network Tools 下），网络批次可在其中补充或引用。
