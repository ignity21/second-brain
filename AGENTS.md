# Agents.md — 项目迁移备忘录

> 创建日期: 2026-07-28
> 目标: 将 `roamnotes/` 中的笔记迁移到 `roamnotes-v2/`，使用 org-roam 管理

---

## 1. 目录结构规则

### 不动目录（Logseq 专用）
- `pages/` — 不动
- `logseq/` — 不动

### 笔记分类目录
- `Inbox/` — 未分类笔记的默认目录（旧版中对应 `Default/`）
- 其他大写字母开头的目录 = 笔记大类（如 `C++/`, `Python/`, `DataScience/` 等）
- 每个大类下可以有 `images/` 目录存放该大类的图片
- 大类目录采用扁平结构：除 `images/` 等资源目录外，不再按 topic 建二级、三级文件目录
- topic 关系在大类索引文件中表达，不用文件系统目录重复表达知识层级

### 图片存放规则
- 每个大类下的 `images/` 存放该大类的所有图片
- 共享资产在 `assets/` 目录（旧版 `roamnotes/assets/`）

---

## 2. 源目录结构 (`roamnotes/`) — 待迁移

| 分类 | org 文件数 | 有 images? | 有 assets 引用? | 备注 |
|------|-----------|-----------|----------------|------|
| **Default** | ~245 | 是 (images/) | 是 (../assets/) | 旧版 Inbox，未分类笔记 |
| **C++** | ~105 | 是 (images/) | 是 (../assets/) | |
| **DataScience** | ~146 | 是 (images/) | 是 (../assets/) | images/ 下有 ML/, screenshots/ |
| **EmacsLisp** | ~40 | 否 | 否 | |
| **Games** | ~2 | 否 | 否 | |
| **Python** | ~30 | 是 (images/) | 否 | |
| **Trading** | ~20 | 是 (images/) | 否 | |

### 共享资产目录 `roamnotes/assets/`
- 被 C++, DataScience, Default 三个分类引用
- 子目录: Algorithm/, CPP/, Data/, Linux/, ML/, Math/, Python/, Statistics/, Trading/
- 图片格式: .png, .svg, .jpeg

### 图片链接格式（两种）

**类型 A: 本地图片 (相对路径)**
```
[[file:images/Overview/2024-02-22_19-40-49_screenshot.png]]
```
解析: 相对于 org 文件所在目录 → `roamnotes/<Category>/images/...`

**类型 B: 共享资产 (上跳一级)**
```
[[../assets/CPP/c-compilation-process.svg]]
```
解析: 从 org 文件上跳一级 → `roamnotes/assets/...`

---

## 3. 目标目录结构 (`roamnotes-v2/`) — 迁移目标

| 分类 | 已有文件 | 备注 |
|------|---------|------|
| **Inbox** | first-20260728.org | 旧版 Default → 迁移到这里 |
| **CS** | math-20260726.org | 新分类，旧版没有 |
| **Python** | testa, testb + images/screenshots/ | 已有少量文件 |
| **pages** | contents.org | 不动 (Logseq) |
| **logseq** | config.edn, custom.css | 不动 (Logseq) |

### 待迁移到 roamnotes-v2 的分类映射
- `Default/` → `Inbox/`
- `C++/` → `C++/`（需新建）
- `DataScience/` → `DataScience/`（需新建）
- `EmacsLisp/` → `EmacsLisp/`（需新建）
- `Games/` → `Games/`（需新建）
- `Python/` → `Python/`（已有）
- `Trading/` → `Trading/`（需新建）
- `assets/` → `assets/`（需新建，或决定是否保留共享资产模式）

---

## 4. 迁移要点

### 4.1 文件内容保留
- ✅ `:PROPERTIES:` `:ID:` 头部全部保留
- ✅ 内部链接 `[[id:...]]` 保留
- ✅ 图片链接保留（但需调整路径）

### 4.2 图片迁移策略
1. 每个大类的 `images/` 目录直接复制到目标分类下
2. `assets/` 目录直接复制到目标根目录（或决定新的存放方式）
3. 需要处理图片链接路径

### 4.3 图片链接处理

**类型 A (本地图片):**
```
旧: [[file:images/Overview/2024-02-22_19-40-49_screenshot.png]]
新: [[file:images/Overview/2024-02-22_19-40-49_screenshot.png]]
```
→ 如果保持相对路径且 images/ 在同类目录下，链接不变

**类型 B (共享资产):**
```
旧: [[../assets/CPP/c-compilation-process.svg]]
新: [[file:assets/CPP/c-compilation-process.svg]]
```
→ 需要改为 `file:assets/...` 或 `../assets/...`，取决于 assets 的位置

### 4.4 Default 目录特殊处理
- `Default/` 下还有一个 `puml/SystemDesign` 子目录（存放 puml 文件）
- 迁移时需要注意这个子目录

---

## 5. 当前 roamnotes-v2 配置
- 使用 org-roam 管理
- 有 `.cache/org-roam.db`（org-roam 数据库缓存，已 gitignored）
- `.gitignore` 排除: `logseq/bak/`, `logseq/.recycle/`, `ltximg/`, `.cache/`, `org-roam.db`, `.venv/`, `.ipynb_checkpoints/`, `.python-version`, `datasets/`, `journals/`, `.aider*`

---

## 6. 迁移步骤建议

1. **备份** — 确认 roamnotes 有 git 备份
2. **新建目标分类目录** — 在 roamnotes-v2 下创建 C++, DataScience, EmacsLisp, Games, Trading, assets
3. **复制图片目录** — 先迁移每个大类的 images/ 和 assets/
4. **复制 org 文件** — 将每个大类的 .org 文件复制到对应目录
5. **处理图片链接** — 更新路径引用
6. **验证** — 用 org-roam 打开验证链接和图片是否正常

---

## 7. 索引文件规则

### 7.1 大类索引文件
- 每个大类目录有一个与大类名同名的 `.org` 文件作为一级索引（如 `Python/python.org`）
- 大类索引只链接中间层级节点，不直接扇出到所有具体笔记
- 中间层级节点也是带 UUID v4 的 org-roam 文件，与其他笔记一起平铺在大类目录中
- 大类索引使用 `* [[id:...][Group Name]]` 链接中间层级节点
- 中间层级索引再使用 `[[id:...][Topic Name]]` 链接具体笔记

### 7.2 层级深度
- 文件系统默认只有 **2 层**：大类目录 → 笔记文件
- 图谱默认使用 **3 层节点**：大类索引 → 中间层级节点 → 具体笔记
- 中间层级索引内部可用 `*` / `**` 标题进一步整理展示，但普通标题不需要 ID，也不会成为图谱节点
- 只有某个中间节点仍然扇出过多时，才增加一个带 ID 的子分组节点；图谱最多 4 层

### 7.3 中文文字修饰
- org-mode 中对中文使用 `**bold**`、`~~strike~~`、`=code=`、`~verbatim~` 等修饰时，标记符前后各空一格：`** 中文 **`、`~~ 中文 ~~`、`= 中文 =`、`~ 中文 ~`

### 7.4 目录扁平与图谱层级规则
- **目录扁平化不等于图谱扁平化**：所有索引和笔记文件放在同一个大类目录，但通过 ID 链接形成层级
- **大类索引文件**（如 `python.org`）只链接 `Language Features`、`Libraries` 等中间层级节点
- **中间层级索引文件**负责链接具体笔记，用来限制大类节点的出度，避免图谱形成“大太阳”
- 中间层级索引可以是纯导航节点，不要求附带正文内容
- **纯文本占位** → 笔记创建后要换成 `[[id:...][Topic]]` 链接
- 图片、示例代码等资源可以使用 `[[file:...]]`，但应由合适的中间层级节点收录

### 7.5 目录生成规则
- 以下 TOC 规则适用于普通笔记文件；大类索引和中间层级索引本身已经是导航，不再额外生成 TOC
- 笔记文件中，一级标题（`*`）数量 **大于 5 个**时，在文件开头添加 `* TOC :TOC_1:` 作为第一个大标题
- 二级标题（`**`）总数 **大于 5 个**时，优先使用 `* TOC :TOC_2:`（覆盖一级标题规则）
  - `:TOC_1:` 只包含一级标题
  - `:TOC_2:` 包含一、二级标题

### 7.6 中文中嵌入英文的空格规则
- 中文段落中嵌入英文单词/短语时，英文整体前后各空一格半角空格
- 例：`你说 he 是谁？他是 Jerry 。`（注意 `Jerry` 后的空格在中文句号前）
- 标点符号（如 `。，？！`）与中文之间不空格，英文与中文标点之间也不空格

### 7.7 标题语言与别名规则
- 层级标题（大类索引、中间层级索引、笔记标题等）尽量使用**英语**
- 如需中文标题展示，在笔记的 `:PROPERTIES:` 抽屉中添加 `:ROAM_ALIASES:` 字段，填入中文别名
- 示例：
  ```org
  :PROPERTIES:
  :ID:       abc123-def456
  :ROAM_ALIASES: 语言特性
  :END:
  * Language Features
  ```
- 这样以英语标题组织层级结构，同时 org-roam 可通过中文别名搜索和反链展示

### 7.8 新文件归位规则
- 从旧版迁移过来的笔记文件，直接放入对应的大类目录，并加入合适的中间层级索引
- 如果某个笔记不属于现有中间节点，可以新建一个中间层级索引文件，并从大类索引链接它；不要为此新建文件目录
- 除 `Inbox/` 中的未分类笔记外，不允许具体笔记未被所属中间层级索引收录，也不允许中间层级索引未被大类索引收录
- 只有当一个主题已经形成稳定、独立的知识领域时才新建大类；不要为单篇或少量笔记新建大类

### 7.9 ID 格式规则
- 所有笔记文件的 `:ID:` 必须使用 **UUID v4 格式**（如 `95feb43d-d5a4-41de-8c70-40fedf3f6265`）
- 禁止使用人为可读的 ID（如 `python-lang-features-20260728`）
- 生成 ID 时使用 `uuid.uuid4()` 随机生成，确保全局唯一

### 7.10 链接引用规则
- 笔记之间的引用必须使用 `[[id:...][Title]]` 格式，禁止使用 `[[file:...][Title]]`
- 图片等资源文件仍使用 `[[file:...]]` 格式

### 4.5 源文件清理规则
- 笔记从 `roamnotes/` 迁移到 `roamnotes-v2/` 后，立即删除 `roamnotes/` 中的源文件
- 图片目录（`images/`、`assets/`）待所有文件迁移完成后统一清理

## 8. Anki 卡片规则

### 8.1 文件结构
- `ankinotes/*.org` 默认都是 Anki 笔记文件。
- 每个文件使用 `* Deck` 作为唯一的一级标题，并在其 `:PROPERTIES:` 抽屉中填写对应的 `:ANKI_DECK:`。
- 制作 Anki 卡片时，在 `* Deck` 下新增一个二级标题（`**`），标题主题由助手根据卡片内容自行确定。
- 卡片内容使用两个三级标题：`*** Front` 和 `*** Back`。

### 8.2 卡片属性
- 新卡片的 `:PROPERTIES:` 抽屉中只填写 `:ANKI_NOTE_TYPE: CC Basic`。
- 不要在新卡片中填写 `:ANKI_DECK:`；牌组从所属文件的 `* Deck` 属性继承。
- 不要预先填写 `:ANKI_NOTE_ID:` 或 `:ANKI_NOTE_HASH:`，这些字段由 Anki/同步流程生成。

### 8.3 标准模板
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

- 用户要求制作卡片时，完成上述结构和 Front/Back 内容即可；不需要代替用户确认或同步 Anki。
