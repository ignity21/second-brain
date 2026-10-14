# 语言特性笔记

适用于编程语言本身的机制，例如 Python 的 MRO、描述符、asyncio，Emacs Lisp 的宏和动态作用域，C++ 的移动语义。

**默认档位**：「能判断」——能读懂和审查使用这个特性的代码，知道什么时候该用、什么时候不该用。语言核心惯用法（推导式、解包、上下文管理器等高频写法）属于「能写」，可以单独设 `Core Idioms` 章节。

## 模板

```org
:PROPERTIES:
:ID:       <uuid4>
:VERIFIED_WITH: <Language> <version> (<YYYY-MM-DD>)
:END:
#+title: <Language> <Feature>

* Mental Model      ; 规则本身，例如 C3 线性化如何决定 MRO
* Minimal Examples  ; 每个例子验证模型的一个推论，给出结果
* Edge Cases        ; 规则的边界和反直觉之处
* Compared with <L> ; 与用户已掌握语言的对应机制对比
* When to Use       ; 适用场景、替代方案、什么时候避免
* Pitfalls
* Core Idioms       ; 可选：需要脱手写出的惯用法
* My Take :mine:
```

## 各章节要求

- **Mental Model**：用规则描述，不用比喻代替规则。读者应能据此预测没见过的情况。
- **Minimal Examples**：每个例子对应一个推论，并附上运行结果，`#+RESULTS:` 或 `example` block 均可。示例必须在 `:VERIFIED_WITH:` 写明的版本上实际运行过。
- **Compared with**：用户掌握的其他语言（查全库，例如 C++、Elisp）中有对应机制时才写，重点写语义差异，不只写语法差异。
- **When to Use**：这里是判断最集中的地方，给出替代方案。例如「用 `__init_subclass__` 代替元类的大多数场景」。

## 不记

- 语法速查和标准库函数清单（属于库类笔记，或直接问 AI）。
- 不改变判断的历史和背景介绍。
