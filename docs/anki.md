# Anki 卡片

创建或修改 `ankinotes/*.org` 时使用；这些文件默认是 Anki 笔记，不套用 org-roam 主索引和 TOC 结构。

- `ankinotes/` 下每个 Org 文件对应一个 Deck；已有主题写入对应文件，没有对应文件时新建文件。每个文件以 `* Deck` 为唯一一级标题，在其 property drawer 中填写 `:ANKI_DECK:`。
- 每张卡片是 Deck 下的二级标题，主题根据内容确定；字段使用三级标题，名称由 Note Type 决定。
- 新卡片的 property drawer 只填 `:ANKI_NOTE_TYPE: <支持的类型名称>`，名称按下表原样填写。牌组继承自 Deck，不在卡片中重复填写 `:ANKI_DECK:`。
- 不预填 `:ANKI_NOTE_ID:` 或 `:ANKI_NOTE_HASH:`，由同步流程生成；编辑已有卡片时保留已有同步字段。
- 制作卡片的完成标准是结构和所选类型的必填字段内容完整，不需要代替用户确认或同步 Anki。

## 支持的 Note Type

| `ANKI_NOTE_TYPE` | 字段（三级标题） | 填写要求 |
|---|---|---|
| `CC Basic` | `Front` / `Back` | 两个字段都填写 |
| `CC Basic (R)` | `Front` / `Back` | 两个字段都填写 |
| `CC Cloze` | `Text` / `Back` | `Text` 必填；`Back` 仅用于补充说明，无需补充时省略整个 `*** Back` 标题及内容 |

Cloze 在 `Text` 中直接使用 Anki 标准挖空语法，例如 `This is a {{c1::apple::hint}}.`。其中 `c1` 是挖空编号，`apple` 是答案，`hint` 是提示；不需要提示时写作 `{{c1::apple}}`。

## Basic 模板

`CC Basic (R)` 使用相同的字段结构，只需将类型值改为 `CC Basic (R)`。

```org
* Deck
:PROPERTIES:
:ANKI_DECK: <deck name>
:END:

** <topic>
:PROPERTIES:
:ANKI_NOTE_TYPE: CC Basic
:END:

*** Front
<question or prompt>

*** Back
<answer>
```

## Cloze 示例

以下二级标题放在所属文件的 `* Deck` 下；示例没有补充说明，因此省略 `Back`。

```org
** Apple
:PROPERTIES:
:ANKI_NOTE_TYPE: CC Cloze
:END:

*** Text
This is a {{c1::apple::hint}}.
```

需要补充说明时，在同一卡片的 `*** Text` 后添加 `*** Back` 并填写说明。

## 从笔记提炼卡片

- 先筛选值得主动回忆的知识：常用操作、关键概念、容易混淆的边界和能迁移到新场景的判断。索引导航、单纯的资料链接、随手可查且低频的命令表默认不制卡。
- 一张卡只考一个明确的判断或动作。题面应给出足够上下文，让答案唯一；不要把整段笔记、长列表或完整函数塞进一张卡。
- 优先用场景、短代码的结果或关键步骤发问，而非只考术语定义。比较相近概念时，指出具体差别及适用条件；必要时拆成多张卡。
- 区分通用 Emacs Lisp 知识、Doom 行为和个人配置。快捷键卡写明适用环境或 keymap；版本敏感、个人绑定或来源存疑的内容先核对，再制卡。
- `CC Basic` 用于场景题、比较题、代码求值；`CC Cloze` 用于上下文完整且只有一个关键缺口的简短事实。不要挖空整段代码或在一张卡里测试多个互不相关的答案。
- 答案先给直接结论，再给必要的理由或简短例子；避免含糊表述和多余背景。代码卡应能通过阅读推导，不依赖未写出的变量或配置。
- 从 org-roam 笔记提炼时，在 `Back` 中附来源 `[[id:...][来源笔记标题]]`，便于回查和修订。Cloze 需要来源时用 `Back` 补充；纯个人经验也要标明其适用范围。
- 卡片中的图片可直接使用相对路径链接，例如 `[[file:../roamnotes-v2/Python/images/example.webp]]`；上传 Anki 时作为媒体记录。
- 制卡前核对来源事实和示例；发现错误或歧义时先修正或跳过，不把未经核实的内容固化为记忆。完成后检查题目是否能独立作答、答案是否准确、字段和同步属性是否符合上述格式。
