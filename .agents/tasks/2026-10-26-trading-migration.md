# Trading 旧笔记迁移

Status: Complete

把 `roamnotes/Trading/`（20 篇，592 行）连同 `roamnotes/Default/` 中的 9 篇交易相关笔记按新规则改造，迁入新大类 `roamnotes-v2/Trading/`（Doom 配置 `modules/cc/notes/README.org` 已列出 `Trading/`）。源笔记和图片全部保留，由用户比对后决定删除。

## 现状

- 旧树：`Trading` 根直接挂 11 个条目（含普通标题 `Analysis`、空标题 `Risk Management`、`Trading Tips`），`Stock Market`、`Technical Analysis`、`Trading System` 是只有链接的索引。
- 内容多为课程笔记的骨架：TA Patterns 大部分小节为空（Entry Point / Stop-Loss / Profit Target 只有标题），OMS 只有一段，Cash Flow 只有一张截图。
- `Trading` 根链接的 Financial Terminology、Micro-Structure、Fundamental Analysis，以及 Stock Market 链接的 Dividends、ETFs、Financial Events 都在 `Default/`；Trading System 链接的 OMS 也在 `Default/`。
- 图片：引用的 18 张截图中只有 8 张存在（TA Patterns 全部、Low Latency 全部、Portfolio Example 缺失）；Log Returns 引用的 `../../resources/MOOC/...` 也不存在。
- 范围外入链：只有 `Default/contents.org`（旧全库目录）→ Trading 根、Stock Market。v2 没有全库总入口，contents 不迁。
- 学习目标：`.agents/learning-goals.md` 尚无 Trading 条目，待用户确认。

## 归属

- 全部归 `Trading/`。Low Latency Design 虽涉及网络，但讲的是交易系统的延迟来源与取舍，留在 Trading；与 `Network/` 的 TCP 笔记（`TCP_NODELAY` 等）在正文中引用。
- Log Returns 是量化中的收益率度量，留在 Trading；如需引用正态分布等统计概念，正文链接 `Statistics/`。
- `Default/` 中纳入本轮的 9 篇：dividends、etfs、financial_events、financial_terminology、fundamental_analysis、micro_structure、repurchase_agreement、treasure_bill、order_management_system。`Default/` 其余笔记不动。

## 目标树（草案）

29 篇 → 13 篇笔记 + 4 个索引（根 + 3 个中间索引；另有 3 篇主笔记兼作父节点）。`←` 后为并入的旧笔记，括号内为保留的主 ID 来源。

```
Trading (trading 7a671aa8)
├─ Financial Markets and Instruments (stock_market 1241ce9f，语义从「股市」扩为「市场与工具」)
│   ├─ Securities and Exchange Mechanics (financial_terminology 09ea9033) ← secondary_market, dividends（除息日 / 登记日，结算改为 T+1）, etfs（只留板块 ETF 的用途）
│   ├─ Money Market Instruments (treasure_bill 167c14ef) ← repurchase_agreement, Financial Terminology 的「货币市场名词」
│   └─ Market Microstructure (micro_structure 7fdff970) ← Financial Terminology 的 ECN 条目
├─ Macroeconomic Drivers of Markets (financial_events 916f4d11) ← monetary_policy
├─ Stock Analysis（新索引）
│   ├─ Fundamental Analysis of Stocks (fundamental_analysis f31358d3) ← cash_flow（FCF 截图改写为文字）
│   └─ Technical Analysis (technical_analysis ede0aad7) ← ta_indicators, ta_patterns
├─ Trading Strategy and Risk Control（新索引）
│   ├─ Trading Strategy Types (trading_strategy fac02460) ← Trading 根的 Trading Tips
│   └─ Position Sizing and Risk per Trade (money_management a8be299b) ← portfolio_management
├─ Quantitative Trading (quantitative_trading 6e4ae290，兼作父节点：工作流)
│   ├─ Log Returns in Quantitative Finance (log_returns dae7eefe)
│   └─ Python Quant Ecosystem (quantitative_libs 77055920) ← openbb（安装步骤删去）
├─ Trading System Architecture (trading_system 5955446b，兼作父节点：组件总览)
│   ├─ Low Latency Trading Design (low_latency_design dbc6bea0)
│   └─ Order and Risk Management Systems (order_management_system b5b5401b) ← risk_management_system, Financial Terminology 的 RMS / OMS 条目
└─ Cryptocurrency Trading (cryptocurrency af4b6edc，兼作父节点：出金路径)
    └─ Perpetual Futures Funding Rate (永续合约 62003c7e)
```

出度：根 7，各索引 / 父节点 1–3。深度 3。Cryptocurrency 只有一个子节点，因其本身有内容（出金路径）且预期扩展而保留。

## 改造原则

- 按 cc-note-writing 重写：术语表、ETF 清单、经济报告发布时间、库清单这类可查询内容压缩为一两句或删去；保留判断依据（指标适用于哪类策略、动量 vs 均值回归的筛选因素、仓位公式、延迟来源与对应优化、资金费率如何锚定现货）。
- 空小节（TA Patterns 的 Entry / Stop-Loss / Profit Target、Cash Dividends 等）删去；只剩名称的形态合并为一张表。
- 截图：FCF、RSI 公式图改写为文字 / 公式；VWAP 截图删去；「陆港美欧出入金一图流」是第三方信息图，复制到 `Trading/images/` 作为出金路径参考（若用户不需要则删）；缺失的图在任务文件中记下。
- 可画成流程的内容（量化工作流、订单经 RMS → OMS → 交易所的路径、资金费率方向）用 PlantUML。
- 修正旧笔记错误（见下方），在回复中列出。
- 中文名词首次出现写「中文（English）」。

## 已发现的旧笔记错误

- XLK 是科技板块，不是医疗（医疗是 XLV）
- 美股结算已于 2024-05-28 改为 T+1（旧写 T+2 / T+3）
- 「货币市场 (Monkey Market)」拼写；「Treasure Bill」应为 Treasury Bill
- 「Underbought」应为 oversold
- DDM 中 \(P_0\) 是当前股价，不是 Current Dividend
- ROE 写成 Return on investment / Return on Invest
- Fiscal Policy 下 Higher taxes 的「Positive Impact: Use taxes to stimulate the economy」逻辑不通
- 资金费率 clamp 写成 `clamp(x, 0.05%, -0.05%)`，上下界顺序反了
- 资金费率的利率 I 是 +0.01%（旧写 −0.01%）；平稳时费率恰为 0.01%，不是「≈ P − 0.01%」
- 溢价指数以价格指数为基准，不是标记价格；冲击买价是吃买盘（卖出）的成交均价，旧说明写成市价买单
- CEI 成分写错：应为非农就业、扣除转移支付的个人收入、工业产出、制造业与贸易销售；「制造业平均工时」属于 LEI
- ATR 只衡量波动，不说明趋势能延续多远
- Book Value 即股东权益（总资产 − 总负债），旧笔记把它写成「有形资产 − 负债」（那是有形账面价值）
- FPGA 是 Field-Programmable Gate Array，旧写 Fully Programmable

## Checklist

- [x] 用户确认（2026-10-26）：用途选「个人投资 / 交易」「交易系统开发工作」「量化研究」；按草案执行，`Default/` 9 篇纳入本轮
- [x] 学习目标写入 `.agents/learning-goals.md`
- [x] 资源：只复制出金信息图（`images/crypto_offramp_map.png`）；FCF、RSI 截图改写为文字、公式和表格，VWAP 截图删去
- [x] 笔记：Markets（3）、Macro（1）、Analysis（2）、Strategy & Risk（2）、Quant（3）、Systems（3）、Crypto（2）
- [x] 索引：根 + 3 个中间索引
- [x] 验证：TOC（4 篇 `TOC_1`，`update_toc.py` 无报错）、行内标记检查为空、block 配平、ID / 标题 / 别名无重复、链接目标和 `file:` 文件全部存在、主树可达且唯一父节点、出度 1–7、无互链、无指向索引或祖先的正文链接
- [x] PlantUML 渲染：3 张图（量化研究流程、系统组件、订单流）生成并补上 `#+RESULTS:`，逐张目检
- [x] `org-roam-db-sync`（临时 daemon `cc-sync`）：342 节点，其中 Trading 20；无悬空 ID 链接
- [x] 数字核对：复利表、基本面例子、连亏概率与回撤、序列化延迟、资金费率 clamp、RSI 映射均在 scratchpad 用 Python 计算；Binance 资金费率公式与 Conference Board LEI / CEI 成分经网页检索核对；库的维护状态取自 PyPI（2026-10-26）

## 改写后的 ID

保留的主 ID 见目标树。中间索引 Stock Analysis（`e74c2c72…`）、Trading Strategy and Risk Control（`d6f2b675…`）为新 ID。实际标题与草案略有不同：Stock Analysis Methods、Fundamental Analysis of Stocks、Log Returns in Quantitative Finance、Cryptocurrency Trading。

废弃 ID（迁移范围外没有入链；`Default/contents.org` 只链接根和 Stock Market，均保留）：

| 旧笔记 | ID | 内容去向 |
|---|---|---|
| monetary_policy | `d190f854…` | Macroeconomic Drivers of Markets → Monetary Policy |
| risk_management_system | `6dd40230…` | Order and Risk Management Systems |
| secondary_market | `4132e7b9…` | Securities and Exchange Mechanics → Primary and Secondary Markets |
| cash_flow | `8d449a14…` | Fundamental Analysis of Stocks → Free Cash Flow |
| ta_indicators | `3b0a02bb…` | Technical Analysis |
| ta_patterns | `dc806d70…` | Technical Analysis → Chart Patterns |
| portfolio_management | `b2753eb5…` | Position Sizing and Risk per Trade |
| openbb | `3bdb01fc…` | Python Quant Ecosystem（安装步骤删去） |
| Default/dividends | `0bc150e5…` | Securities and Exchange Mechanics → Dividends |
| Default/etfs | `bb4cb7de…` | Securities and Exchange Mechanics → ETFs |
| Default/repurchase_agreement | `4a0ccafb…` | Money Market Instruments → 回购协议 |

Financial Terminology 拆散：证券分类、一二级市场、经纪人 / 交易商、Float、ADR、交易时段 → Securities；货币市场名词 → Money Market；ECN → Microstructure；RMS / OMS / SLRMS / GRMS → Order and Risk Management；Tick Data → Quantitative Trading；Trading Strategy / Alpha-seeking → Trading Strategy Types；Loss Aversion → Position Sizing。旧根的 Trading Tips → Technical Analysis → Premise。

删除未收：OpenBB 安装与 Docker 命令、VWAP 截图、TA Patterns 中的空小节、Cash / Stock Dividends 空标题、各报告的发布机构细节、LEI / CEI 的旧成分清单。

## 指向未迁移笔记的链接

新笔记中没有。`Default/` 中其余未迁移笔记没有指向本轮笔记的入链（`contents.org` 除外，其链接的两个 ID 均保留）。

## 缺失的旧资源

旧笔记引用但文件不存在：TA Patterns 的全部 9 张截图、Low Latency Design 的 4 张截图、Portfolio Management 的示例截图、Log Returns 引用的 `../../resources/MOOC/Trading/returns_distributions.png`。内容已按文字重写，无需恢复。
