# C++ 旧笔记迁移

Status: Complete

把 `roamnotes/C++/`（105 篇，6075 行）按新规则改造迁入 `roamnotes-v2/C++/`。源笔记、`images/`、`assets/CPP/` 全部保留，由用户比对后决定删除（2026-10-26 用户要求，已写入 note-migration skill）。

## 现状

- 旧树：`C++ → C++ Coding → Basics / Modern / Compile-time / Advanced / STL / Libraries`，大量单篇只有几行语法或 API（Literal、`std::array`、`std::map`、GDB、Static Local Variable 为空）。
- 内容最扎实的是并发（约 30 篇，源自 /C++ Concurrency in Action/ 和 CppCon）、类型推导和值类别（/Effective Modern C++/）。
- 旧库内的断链：`C++ Concurrency` 里的 STL Concurrency（`bfb36506…`）、`STL` 里的 Modern STL Evolution（`442b8404…`）指向不存在的 ID。
- 旧库其他目录指向 C++ 的入链：`Default/` 的 error_handling → RAII、languages → C++、process_memory_model → Memory Allocation、system_design → ZeroMQ。迁移保留这些 ID，对方迁移时自动恢复。
- 学习目标：2026-10-26 用户选择「工作和面试」，已写入 `.agents/learning-goals.md`。

## 归属

- 留在 C++：语言、模板、资源管理、STL、并发、工具链（CMake、Conan、GDB 只服务 C++ 项目）。
- ZeroMQ（`5521b2f9…`，旧标签 `:Network:`）：本轮不迁。与 `Default/zeromq-20250730.org`、`pub_sub_pattern` 一起在迁移 `Default/` 时合并，归属届时再定。
- 竞争条件、死锁、内存模型、无锁结构虽是通用概念，但笔记以 C++ API 讲解，留在 C++。
- Memory Allocation 中的栈 / 堆 / 静态区通用部分与 `Default/process_memory_model` 重叠；本轮只保留 C++ 特有内容（`new`/`delete`、placement new），通用部分等迁移 Linux 内容时处理。

## 目标树（草案）

105 篇 → 约 20 篇笔记 + 6 个索引。`←` 后为并入的旧笔记，括号内为保留的主 ID 来源。

```
C++ (c-20230801)
├─ C++ Language Core (c_coding)
│   ├─ C++ Value Categories and Move Semantics (move_semantics) ← copy_semantics, perfect_forwarding, constructors, variadic perfect forwarding
│   ├─ C++ Type Deduction (type_deduction) ← template_type_deduction, auto, decltype, type_deduction_diagnosis, std_initializer_list（花括号初始化陷阱）
│   ├─ C++ Classes and Special Member Functions (c_class) ← c_oop, struct, operator_overloading, keywords（explicit / mutable）, chaining_function_calls
│   ├─ C++ Polymorphism and Object Layout (vtables) ← virtual_destructor, rtti, type_casting, trivially_copyable, standard_layout, union
│   ├─ C++ Callables (c_lambda) ← function_pointer, std_function, std_bind, std_mem_fn, functions（inline）
│   └─ C++ Language Basics (pointers) ← c_built_in_array, enum, namespace, using, macro, exception, multiple_return_values, temporary_variables, literals
├─ C++ Templates (c_template)
│   ├─ C++ Template Basics (function_template) ← class_template, variable_template, extern_template, variadic_arguments, variadic_templates, c_20_concepts
│   └─ C++ Compile-time Programming (constexpr) ← if_constexpr, static_assert, type_traits
├─ C++ Resource Management (c_memory_management)
│   ├─ C++ RAII and Smart Pointers (smart_pointers) ← raii, circular_references
│   └─ C++ Dynamic Memory Allocation (c_memory_allocation)
├─ C++ Standard Library (stl_functions)
│   ├─ C++ STL Containers and Iterators (std_vector) ← std_array, std_deque, std_map, std_unordered_map, iterator, built_in_data_structures
│   └─ C++ STL Algorithms and Ranges (stl_algorithms) ← istringstream?
├─ C++ Concurrency (concurrency)
│   ├─ C++ Threads and Async Tasks (std_thread) ← std_async, std_future, std_packaged_task, stl_concurrency, parallel_computation
│   ├─ C++ Mutexes, Locks and Deadlock (mutex) ← locks, deadlock, race_condition, thread_safe_lazy_initialization, c_singleton, design_pattern, static_local_variable
│   ├─ C++ Condition Variables (condition_variable)
│   ├─ C++ Memory Model and Atomics (atomics) ← c_memory_model, memory_barriers, compare_and_swap, spin_lock
│   ├─ C++ Lock-based Concurrent Data Structures (designing_thread_safe_data_structures) ← thread_safe_stack, thread_safe_queue, thread_safe_lookup_table, thread_safe_list
│   └─ C++ Lock-free Data Structures (designing_lock_free_data_structures) ← lock_free, lock_free_stack
└─ C++ Toolchain (← Build Tools 标题 ID 18384124)
    ├─ C++ Compilation and Linking (c_compilation) ← include_guard, static_library
    ├─ CMake (cmake)
    ├─ Conan 2 (conan2)
    └─ C++ Debugging Tools (gdb) ← debugging, valgrind 段（来自 memory_allocation）
```

出度：根 6，各索引 2–6。深度 3。

## 改造原则

- 每篇按 cc-note-writing 的语言特性 / 库模板重写：保留核心模型（值类别、推导规则、内存序、锁粒度、异常安全）、坑和对比；API 清单、构造写法、教程式代码压缩为能力地图或删去。
- 旧书中的长实现（细粒度锁队列、查找表、无锁栈）保留关键片段和设计理由，不保留整段代码；整段可运行代码若值得保留，放 `projects/cpp-concurrency/`（需用户确认）。
- 截图：能用文字 / 表格 / PlantUML 表达的改写，必须保留的复制到 `roamnotes-v2/C++/images/`；`assets/CPP/` 的两张图迁入 `roamnotes-v2/assets/CPP/`。
- 被并入笔记的 ID 尽量保留为标题级 ID；内容整体删去的笔记 ID 记入下方「废弃 ID」。
- 代码示例在 scratchpad 用 `g++ 16.2.1 -std=c++23` 编译运行核对，笔记写 `:VERIFIED_WITH:`。
- 修正旧笔记中的错误（如 `pop()` 原子队列示例并非线程安全、`const_cast` 修改 const 对象是 UB、`~std::shared_ptr~` 的 `static_pointer_cast` 示例方向等），在回复中列出。

## Checklist

- [x] 用户确认（2026-10-26）：学习目标「工作和面试」；长代码只留关键片段，不建 `projects/`；按草案执行，ZeroMQ 延后
- [x] 学习目标写入 `.agents/learning-goals.md`
- [x] 资源：旧图片不复制。需要的图（值类别、vtable、编译流程、细粒度队列、release/acquire、shared_ptr 控制块）改画为 PlantUML，其余改成文字或表格；`assets/CPP/` 不再需要
- [x] Language Core（6 篇）、Templates（2）、Resource Management（2）、Standard Library（2）、Concurrency（6）、Toolchain（4）
- [x] 7 个索引（根 + 6 个中间索引）；v2 没有全库总入口，根 `C++` 独立
- [x] 代码示例与说法：在 scratchpad 用 GCC 16.2.1 `-std=c++23` 编译运行（并发示例加 `-fsanitize=thread`）；CMake 4.4.4、Conan 2.33.0 用 uvx 临时运行，Conan 使用 scratchpad 内的 `CONAN_HOME`
- [x] 验证：TOC（9 篇用 `TOC_1`，`update_toc.py` 无报错）、行内标记检查为空、表格单元 `~` 成对、block 配平、无 `file:` 链接、ID 无重复、链接目标全部存在、主树可达且唯一父节点、出度 2–6、无互链和指向索引的正文链接
- [x] `org-roam-db-sync`（临时 daemon `cc-sync`）：322 节点，其中 C++ 29；无悬空 ID 链接
- [x] PlantUML 渲染：用户安装 PlantUML 1.2026.8 后运行 `render_plantuml.py`，6 张图生成并补上 `#+RESULTS:`；修正 vtable 图的单行 object 语法错误和编译流程图中 `#include` 标签的图标误渲染，逐张目检

## 改写后的 ID

保留的主 ID 见上方目标树（索引沿用旧索引 ID；Toolchain 使用旧 `Build Tools` 标题 ID）。RAII and Smart Pointers 改用 `raii` 的 ID `474df27e…`（有 `Default/error_handling` 入链），不用 `smart_pointers`。

其余旧笔记和旧标题级 ID 全部随合并废弃：迁移范围外没有指向它们的入链（`Default/` 的入链只指向 C++ 根、RAII、Memory Allocation、ZeroMQ，均保留或未迁移）。旧文件 → 新笔记的对应关系即目标树中的 `←` 列表；另有：

- 删除未收：`istringstream`（改为在 Algorithms 中推荐 `std::from_chars`）、`c_literals`、`static_local_variable`（空笔记）、`C++ Coding` 中的 For Loop 片段、`std_map` 的截图、标准演进截图（改为 Threads 笔记中的版本表）
- `functions` 的 inline 段 → C++ Compilation and Linking（原「无循环、无递归」等要求是错误说法，已改为 ODR 含义）
- `memory_barriers`、`compare_and_swap`、`spin_lock`、`c_memory_model` → C++ Memory Model and Atomics

## 指向未迁移笔记的链接

新笔记中没有。未迁移笔记指向 C++ 的入链：`Default/languages` → C++ 根、`Default/error_handling` → RAII、`Default/process_memory_model` → Memory Allocation（均有效）；`Default/system_design` → ZeroMQ（待迁移 `Default/` 时处理）。

## 修正的旧笔记错误

- 16 字节结构体的 `std::atomic` 在 GCC 16 / x86-64 上不是 lock-free（旧表写 Yes on x86）
- 「x86 上 acq_rel 与 seq_cst 相同」：只有 seq_cst store 不同（`xchg`），已用汇编核对
- 旧 Atomic Queue 示例不是线程安全的发布
- 条件变量谓词缺 `return` 且逻辑相反
- Meyers singleton 是惰性初始化（旧笔记写 No lazy initialization）；双重检查锁的单例写法有数据竞争
- `const_cast` 后写 const 对象是 UB（旧示例当作合法输出 30）
- 迭代器 `it = erase(it); --it;` 在删除首元素时是 UB（debug 模式已复现）
- `res2 = std::ranges::copy_if(...)` 返回值不是容器
- CMake `block()` 示例输出应为 dog（旧写 cat）
- `std::async` 是否用线程池取决于实现，libstdc++ 每次新建线程
- GDB `x\7tb` → `x/7tb`
- 旧库自身问题：多张截图文件已缺失；`C++ Concurrency`、`STL` 中各有一个指向不存在 ID 的链接
