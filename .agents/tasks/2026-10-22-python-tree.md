# Python 层级重组

Status: Complete

总任务见 `2026-10-22-v2-category-restructure.md`。初始检查：深度 5，问题 10（4 个孤立节点、5 个单子节点索引、Model/View 两个父节点）。全库没有来自 Python 以外的入链。

用户 2026-10-22 确认目标结构和改标题：

```
Python
├─ Language Features
│   ├─ Decorators → Class Decorators
│   ├─ asyncio, Exceptions, Type System
│   └─ Object-Oriented Programming → Metaclass, Abstract Class, Mixin Classes, MRO, __init_subclass__
├─ Development Practices → Style Guide, Practical Advice, Testing, radon（← Code Analysis Utilities）
├─ Package Management（← Packaging Management）→ uv, pyproject.toml, pipx, poetry
└─ Third-Party Libraries → wrapt, python-statemachine, loguru, websockets, Qt → Model/View, PyQt5, PySide6
```

## Checklist

- [x] 撤销单子节点或含义模糊的索引：Code Analysis Utilities、Code Helpers、Logging Libraries、Network Protocols、GUI Libraries
- [x] Package Management：列表链接改为主树整行链接，收回 4 个孤立节点
- [x] Qt 兼作 Model/View、PyQt5、PySide6 的父节点
- [x] 内容笔记：Practical Advice 圈复杂度处引用 radon（Decorator 的「用 wrapt 装饰类成员函数」标题含正文，不是整行链接，保留）
- [x] 标题补领域上下文，修正 `__init__subclass__` 拼写
- [x] 验证：检查脚本、入链、TOC、行内标记、file 链接、org-roam-db-sync

Result: 深度 5→4，问题 10→1（剩余 1 条为允许的「笔记兼父节点」Decorators → Class Decorators）；删除 5 个索引，4 个孤立的包管理笔记接入主树，Model/View 只剩 Qt 一个父节点。改名均保留 ID：Python Decorators、Python Class Decorators、Python Metaclass、Python Mixin Classes、Python Method Resolution Order (MRO)、Python Style Guide、Python Practical Advice、Python ~__init_subclass__~、Python Package Management。重新生成了 Qt 的 TOC。临时库 batch `org-roam-db-sync` 通过（308 节点，无悬空 ID 链接）；2026-10-22 用 Doom daemon 对真实 DB 执行了 `org-roam-db-sync`（305 节点，无悬空 ID 链接）。
另见：`Python/` 下的 `pyproject.toml`、`uv.lock` 是笔记代码块的运行环境（迁移时加入），不是笔记，未改动。wrapt、PyQt5、python-statemachine、=pyproject.toml= 几乎只有标题或一条外链（既有内容问题，未改）。
