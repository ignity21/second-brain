# C++ 与 Trading 的 Anki 卡片

Status: Not started

C++、Trading 迁移（2026-10-26）后，按新笔记制卡。用 `anki-cards` skill；只写卡片文件，由用户自己同步到 Anki。制卡深度参考 `.agents/learning-goals.md` 中这两个领域的档位。

## C++

- Deck：`ankinotes/cpp.org`（`RoamCards::C++`，2026-10-26 由 `CS::C++` 改名）。只有 2 张旧卡（Pointers、Pointers to Array），保留其 `ANKI_NOTE_ID` / `ANKI_NOTE_HASH`。
- 旧卡问题，制卡时一并请用户决定是否修改：
  - Pointers to Array 的 Back 写 ~ptr~ 是「address of array」，应为首元素地址（类型 ~int*~，与 ~&array~ 的类型 ~int(*)[5]~ 不同）。
  - ~*(++ptr)~ 和 ~*(ptr++)~ 两行的说明依赖前面几行的执行顺序，没有写清楚。
- 来源：`roamnotes-v2/C++/` 的 20 篇笔记。学习目标是工作和面试，优先「能判断」的高频题：
  - 值类别与移动语义：何时调用移动构造，~std::move~ 只是转换，转发引用与 ~std::forward~
  - 类型推导：~auto~ / 模板推导丢掉顶层 const 和引用，~decltype((x))~，花括号初始化的坑
  - 特殊成员函数：rule of zero / five，什么情况下不再生成移动操作
  - 多态：vptr / vtable 调用开销，虚析构函数，在构造函数里调用虚函数
  - RAII 与智能指针：~unique_ptr~ vs ~shared_ptr~，控制块，~make_shared~，用 ~weak_ptr~ 打破循环
  - 并发：接口层面的竞争（~top()~ + ~pop()~），用 ~std::scoped_lock~ 避免死锁，条件变量必须带谓词，内存序（release / acquire、seq_cst），lock-free 与 lock-based 的取舍
- 规模：约 25–30 张，语言跟随笔记（英语）。

## Trading

- Deck：`RoamCards::Trading`（按 anki-cards skill 的大类规则），新建 `ankinotes/trading.org`。
- 来源：`roamnotes-v2/Trading/` 的 16 篇笔记，约 20 张。英文笔记用英文制卡，Money Market Instruments、Perpetual Futures Funding Rate、Python Quant Ecosystem 用中文。
- 候选：
  - 对数收益与简单收益：各自适合跨时间还是跨资产累加；+50% 再 −50% 的例子
  - 仓位公式：股数 = 账户 × 单笔风险 / (入场价 − 止损价)；风险 2% 不等于仓位 2%
  - 连续亏损造成的回撤，以及回本所需的涨幅
  - 资金费率：合约高于现货时哪一方付钱；为什么平稳时恰为 0.01%；年化约 11%
  - 动量与均值回归：各自的押注、失效的市场环境、选股因素（float、机构持股）
  - RSI 的 RS 映射与入场规则；ATR 用来设止损；VWAP 为什么能当日内支撑
  - DDM：$P_0 = D_1/(r-g)$，以及对 $r-g$ 的敏感性
  - FCF 与 FCF conversion
  - 延迟来源与对应优化；内核旁路的代价
  - 风控检查的两个位置（参数设置时、订单离开系统前），SLRMS 与 GRMS 的区别

## Checklist

- [ ] C++：确认是否修改 2 张旧卡；写新卡；行内标记检查
- [ ] Trading：新建 `ankinotes/trading.org`；写卡；行内标记检查
- [ ] 提交并推送
