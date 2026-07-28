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
- 索引文件以树状层级列出该大类下的子 topic，链接格式 `[[id:...][Topic Name]]`

### 7.2 层级深度
- 默认 **3 层**：大类 → 分组 → 笔记
- 最多 **4 层**：大类 → 分组 → 子分组 → 笔记
- 如果某个笔记太底层、跨度太大，可补出中间分组，但不超过 4 层

### 7.3 中文文字修饰
- org-mode 中对中文使用 `**bold**`、`~~strike~~`、`=code=`、`~verbatim~` 等修饰时，标记符前后各空一格：`** 中文 **`、`~~ 中文 ~~`、`= 中文 =`、`~ 中文 ~`

### 7.4 索引层级规则
- **大类索引文件**（如 `python.org`）只包含 `*` 一级标题，每个标题链接到一个**分组索引文件**（如 `[[file:language_features.org][语言特性]]`）
- **分组索引文件**（如 `language_features.org`）用 `*` / `**` 标题放下级索引，文件本身也可以包含笔记内容
- **纯文本占位** → 笔记创建后要换成 `[[id:...][Topic]]` 链接
- **层级深度**：最多 4 层，即 `大类索引 → 分组索引 → 子分组 → 笔记`

### 7.5 长笔记目录生成
- 笔记较长（含多个标题）时，在标题下方添加 `* 目录 :TOC_1:` 或 `* 目录 :TOC_2:` 标签行，org-mode 会自动生成目录
  - `:TOC_1:` 只包含一级标题
  - `:TOC_2:` 包含一、二级标题

### 7.6 中文中嵌入英文的空格规则
- 中文段落中嵌入英文单词/短语时，英文整体前后各空一格半角空格
- 例：`你说 he 是谁？他是 Jerry 。`（注意 `Jerry` 后的空格在中文句号前）
- 标点符号（如 `。，？！`）与中文之间不空格，英文与中文标点之间也不空格
