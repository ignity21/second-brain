# 经验 / 坑笔记

适用于用户亲历的调试过程、事故和踩坑记录。

**默认档位**：「能判断」。价值不在修复命令（以后问 AI 就有），而在 **排查路径和被修正的认知**：它们训练排查直觉，并且只有用户本人才拥有。

## 放在哪里

- **短的坑**（一两句话说清，只和一个库或特性有关）：写进相关笔记的 `Pitfalls` 章节。
- **长的调试经历，或跨领域的坑**：单独成篇，放入最相关的大类（无法归类时放 `Inbox/`），由相关笔记在正文中链接。

## 模板

```org
:PROPERTIES:
:ID:       <uuid4>
:END:
#+title: <Symptom or Lesson, with domain context>

* Context            ; 环境、版本、当时在做什么
* Symptom            ; 实际看到的现象，原样保留关键报错
* Wrong Hypotheses   ; 当时怀疑过什么、为什么错
* Root Cause         ; 根因的技术解释
* Corrected Model    ; 修正了哪条认知：原来以为 X，其实是 Y
* Early Signals      ; 下次怎样更早发现
* Fix                ; 简短的修复方法
* Prevention         ; 测试、lint、AGENTS.md 规则等防止复发的手段
```

## 人机分工

- 这类笔记大部分事实只有用户知道。`Context`、`Symptom` 和 `Wrong Hypotheses` 以用户的叙述为准：AI 可以整理措辞，但不能补充用户没说过的细节。缺少的信息在回复中询问。
- AI 负责 `Root Cause` 的技术解释（需要核对）、归纳 `Corrected Model`（用户确认）、提出 `Early Signals` 和 `Prevention` 的建议。
- 用户想原样保留的叙述，放在 `:mine:` 标题下。

## 要求

- **`Corrected Model` 是核心**，必须写出来；写不出来，说明这个坑可能只是一个可检索的事实，按准入测试处理即可。
- **`Prevention`** 优先选择可执行的形式：测试用例、lint 规则、AGENTS.md 规则或 skill，而不是一句「以后注意」。
- 通用的坑（AI 都知道的，例如可变默认参数）不单独成篇，只在相关笔记的 `Pitfalls` 里写症状特征，帮助下次一眼认出。
