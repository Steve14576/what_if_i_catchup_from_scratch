# SOP：课件扒取（通用版 · 任意 PPT / PPTX 课件）

> **定位**：把**任意一套** PPT / PPTX 课件扒成「逐页、保真、可引用」文字稿的**可复跑操作规程**。与同目录 `SOP_课件扒取.md`（项目实例）**同构**：同样的 §0–§8、同样的流程与判据；差别只是把项目相关项换成参数（`<SRC_DIR>` / `<WORK>` / `<OUT>` / `<SCRIPTS>` / `<LEC>`）。
> **通用方法论**见 skill `courseware-transcript`（`~/.qoder/skills/`）。本文件是它的"可执行清单"形态，供换新课件时直接照做。
> **一讲 = 一份源文件**；讲次边界 = 文件边界（不按学时拆）。

---

## 0. 产物形态

一讲产出**三件套**，落在 `<OUT>/`：

| 产物 | 内容 |
|---|---|
| `<LEC>.md` | 头部来源说明 → **图索引** → 逐页正文 |
| `<LEC>-images/` | 归档的**教学图**，命名 `p页码_中文描述.png` |
| `<LEC>-render/` | 矢量图页 / OLE 页的**整页渲染兜底**，命名 `<LEC>_pNN.png` |

`<LEC>.md` 的逐页固定格式：

````markdown
## 第 N 页

![P{NN} {中文描述}]({LEC}-images/{文件名})

（图中：……把图里对文字层不可见的信息补齐……）

<正文文本，按页序逐行照录>

> [Speaker Notes] ……（该页若有讲者备注，附一行）
````

头部固定两段：来源行（`> 来源: ... | 共 N 页`）+ 说明行（口径与产物位置）；其后是 `## 图索引`，逐条列 `- P{页码} — \`{LEC}-images/{文件名}\` — {说明}`。

---

## 1. 讲次编号映射

`<LEC>` 按源文件的**自然讲次顺序**分配（主序号 + 子序号）。规则示例：`Lecture 9_1` < `9_2` < `10 I` < `10 II`；带罗马数字后缀的按 I/II/III 映射为子号。

| Lec | 源文件（`<SRC_DIR>/`） |
|---|---|
| Lec01 | `<第 1 份源文件>` |
| Lec02 | `<第 2 份源文件>` |
| … | … |
| LecNN | `<第 N 份源文件>` |

编号由提取脚本的 `build_lecture_map()` 按自然顺序**自动生成**，勿手工维护；若下游教程自有编号体系，需额外维护一张对照表。

---

## 2. 目录契约

```
<SRC_DIR>/                        源课件（只读，不改动）
<WORK>/                           中间件（可重建，非交付物）
├─ pdf/                           导出的 PDF
├─ raw/                           每页原始稿（含 <!-- meta --> 注释）
├─ pages/                         逐页元数据 JSON
├─ media/                         从 ppt/media/ 抠出的位图 + _slide_media.json
├─ imgmap/                        每讲图映射 JSON（页码 → {src,name,cap}），供组装读取
└─ contact/                       接触表（triage 用）
<OUT>/                            交付物
├─ <LEC>.md
├─ <LEC>-images/
└─ <LEC>-render/
<SCRIPTS>/                        流水线脚本（§5）
```

中间件一律进 `<WORK>/`，**不散落**；交付物只进 `<OUT>/`。

---

## 3. 口径（硬规则）

1. **公式**：一律由 OMML（`m:oMath`）**结构化还原**为 LaTeX（`sSub/sSup/f/rad/d/nary/func/bar/limUpp` 等节点 → `_{}/^{}/\frac/\sqrt/...`），**不读图**。**`p:oleObj` 不一定是公式**：实测中它多为**嵌入的表格/插图**；其内容由所在页的整页渲染保留。遇到 OLE 先看渲染图再判断，不要预设"OLE = 公式"。
2. **图**：**只归教学图**（矢量绘制示意图、结构示意、晶胞图、相图、显微照片、教科书插图）与**块状文本/公式截图**（很多例题、推导、题目只有截图、无文字层）；**参考数据表截图不归**（靠正文即可）；纯 logo、风景/人物照片、纯装饰不归。矢量图页嵌**整页渲染**；位图嵌 `ppt/media/` **原图**。
3. **只还原不加工**：按页序原样落，不融合、不跳重点、不打乱顺序、不替老师改写；中英混排照录。
4. **渲染定向**：只渲染「含矢量绘制（`a:custGeom` / `p:cxnSp`）**或** OLE 对象（`p:oleObj`）」的页（`render` 标志），**不整本渲染**。
5. **公式定界符**：行内 `$...$`，块级 `$$...$$`（不用 `\(...\)` / `\[...\]`）。
6. **图片引用**：走**相对路径**（相对 md 所在目录）。

> 口径 2 是**可调**的：不同课程对"哪些算教学图"的尺度不同，迁移时先做 1 讲交用户确认粒度，再批量。

---

## 4. 流程（逐讲六步）

### Step 0 · 环境
`uv` 管理（Python 3.12）。依赖：`pillow`、`pymupdf`、`python-pptx`（`lxml` 随 python-pptx 带入）。
渲染/导出通路二选一：**本机 Microsoft PowerPoint**（Windows，经 COM 自动化，实测路线）或 **LibreOffice**（`soffice --headless --convert-to pdf`）。

### Step 1 · 导出 PDF（给渲染做底）
```powershell
$c = Get-Content -LiteralPath "<SCRIPTS>\export_pdf.ps1" -Raw -Encoding UTF8
Invoke-Expression $c
Export-PptxToPdf -PptxPath "<源.pptx>" -PdfPath "<WORK>\pdf\<LEC>.pdf"
```
批量时在**一个** PowerPoint 会话里循环 `Open → SaveAs → Close`，跳过已存在非空 PDF。
**必须**用 `[System.Activator]` 晚绑定创建 COM（见 §7）。无 PowerPoint 时改用 LibreOffice 命令。
拿到 PDF 后**仍需探测文本层**（空 → 该页按纯图页处理）。

### Step 2 · 结构化提取
```powershell
uv run python <SCRIPTS>/extract_lecture.py <LEC>
```
产 `<WORK>/raw/<LEC>.md`（每页文本 + `$…$` 公式 + `<!-- meta -->`）与 `<WORK>/pages/<LEC>.json`（逐页 `chars/omml/pic/vec/ole/notes/render`）。

### Step 3 · 定向渲染 + media
```powershell
uv run python <SCRIPTS>/make_assets.py <LEC>
```
产 `<LEC>-render/`（按 `render` 标志渲染，dpi 220 为当场选取）与 `<WORK>/media/<LEC>/`（位图原图 + `_slide_media.json`）。

### Step 4 · 接触表 triage（人工判图）
```powershell
uv run python <SCRIPTS>/build_contact.py render <LEC> 4      # 渲染页接触表（页码标签）
uv run python <SCRIPTS>/build_contact.py dir "<图目录>" 5     # 任意图目录接触表
```
读接触表，按 §3.2 判「哪些页出图、用渲染还是原图」，把结论写进下一步的图映射。

### Step 5 · 组装
在 `<WORK>/imgmap/<LEC>.json`（或脚本内联 `IMGMAP`）里补本讲的 `{页码: {src, name, cap}}`（允许**一页多图**，值为列表；`cap` 即「图中：…」说明），然后：
```powershell
uv run python <SCRIPTS>/assemble_lecture.py <LEC>
```
产 `<LEC>.md`（头部 + 图索引 + 逐页）与 `<LEC>-images/`（拷贝并中文命名，脚本内校验源↔目标一一对应）。

### Step 6 · 校验（每次必做）
```powershell
uv run python <SCRIPTS>/validate_lecture.py <LEC>
```
判据见 §6；输出须为 `PASS`。

---

## 5. 脚本职责（参考实现，路径需参数化）

> 下表是**本项目 `scripts1/` 的参考实现**。迁移到新项目时，把脚本里的根路径、讲次清单改成命令行参数或配置，不要带着硬编码路径走。

| 脚本 | 职责 |
|---|---|
| `export_pdf.ps1` | PowerPoint COM 导出单份 PPTX→PDF（函数 `Export-PptxToPdf`） |
| `export_decks.ps1` | 批量导出（读讲次清单，单会话循环，跳过已存在） |
| `extract_lecture.py` | XML 全遍历文本 + OMML→LaTeX + notes + 表格 + 逐页元数据；`list` 模式生成讲次清单 |
| `make_assets.py` | 定向渲染 PNG（dpi 220）+ 抠 `ppt/media/` + slide→图映射 |
| `build_contact.py` | 拼接触表（`render` 模式 / `dir` 模式） |
| `build_triage.py` | 每讲合并 triage 图（渲染页 + 被引用位图，带标签） |
| `assemble_lecture.py` | 按 `<WORK>/imgmap/<LEC>.json`（或内联 `IMGMAP`）组装 md + 拷贝图（内联引用 + 图索引节） |
| `validate_lecture.py` | 交付前校验（页数 / 图片 / 占位符 / 公式计数） |
| `check_imgmaps.py` | 全量检查映射里的 src 是否存在（组装前先跑） |
| `probe_decks.py`、`probe_vector.py` | 只读探测：规模统计、矢量/OLE/media 统计 |
| `omml_census.py` | OMML 元素普查（验证渲染器覆盖）+ `dump <frag> <slide>` 单页 OMML 转储 |

---

## 6. 校验判据

| 项 | 判据 |
|---|---|
| 页数对齐 | `<LEC>.md` 的 `## 第 N 页` 段数 = 源文件页数 |
| 图片可解析 | 每个 `![…](路径)` 的文件都真实存在 |
| 占位符清零 | 无 `TODO` / `待补` / `<!-- meta` / `@@OMML` / `[公式对象]` |
| 图注齐全 | 每个出图页都有 `（图中：…）` |
| 公式计数 | 打印行内 `$…$` / 块级 `$$…$$` 计数备查 |

> **注意**：不要把 `{{` 当占位符——它是 LaTeX 合法嵌套花括号（如 `^{{2}}`），按它判会误报。

---

## 7. 已知坑（实测）

- **PowerShell 调 Office COM**：`New-Object -ComObject PowerPoint.Application` 会走 Office PIA，属性一访问就抛 `TYPE_E_ELEMENTNOTFOUND (0x8002802B)`（`Version` 空、`Visible/Quit` 报错、`Presentations` 为 Null）。**必须**用
  `[System.Activator]::CreateInstance([System.Type]::GetTypeFromProgID("PowerPoint.Application"))`
  的纯 IDispatch 晚绑定。
- **stdout 包装防重**：脚本被 `import` 时若重复包 `sys.stdout`，底层 buffer 被关，触发 `I/O operation on closed file`。包装须加**守卫**：仅当当前 `sys.stdout.encoding` 非 utf-8 才包。
- **中文 / 路径**：命令行传中文路径易乱码——命令行保持纯 ASCII，中文路径硬编码进脚本源码（或全程用 ASCII 路径）。
- **OMML 属性节点**：`m:sSubPr` / `m:fPr` / `m:radPr` 等排在内容节点**之前**，取子节点**必须按 tag 名**（`e`/`num`/`den`/`sub`/`sup`/`deg`），不能按位置索引，否则上下标错位甚至丢内容。
- **`mc:AlternateContent` 双分支**：数学区 `Choice` 是真 OMML、`Fallback` 是压平文本；段落级也要**择一**，否则公式出现两次（一次 LaTeX、一次压平）。
- **数学粗斜体 Unicode**：`𝑎`、`𝑅`、`𝟏` 等需 **NFKC 归一化**成 ASCII，否则 KaTeX 渲染不了。
- **公式压平**：纯文本拼接会把 `a=2R√2` 压成 `a=2R2`——**必须**走结构化渲染，不能引用纯文本稿。
- **媒体扩展名靠猜**：`ppt/media/` 里是 `.jpg/.jpeg/.png` 混合，映射里写错扩展名会 `missing image src`；组装前先跑一遍全量 src 存在性检查。
- **非位图混进 PIL**：`svg/emf/wmf` 用 PIL 打不开，会让接触表整批崩；按扩展名白名单（png/jpg/jpeg/gif/bmp）过滤。
- **接触表只按宽度缩放**：高窄图会把整张拼图撑到几万像素、不可读；按包围盒（限宽 + 限高）缩放。
- **JSON 里写 LaTeX**：反斜杠必须 `\\`（`"\\Delta"`），否则 `\D` 是非法转义、整份 JSON 报错；省事的话图注用纯文本数学，LaTeX 留给正文。
- **`.ppt`（旧二进制）**：本流程**未实测**直接导出；先另存为 `.pptx`/PDF，别把"应该能"写成"已验证"。
- **一次性全量跑**：口径错了要整套返工；**先做 1 讲完整样本交用户验收，再批量**。

---

## 8. 状态与历史

- **来源**：本通用版由一次真实课件扒取（669 页 / 19 份 PPTX，全部通过校验）的实测流程**去项目化**整理而来。
- **适用边界**：需要能导出 PDF 的办公软件（PowerPoint 或 LibreOffice）；否则只能做文本 + OMML 公式，矢量图页与 OLE 页拿不到。`.ppt` 未实测。
- **与项目实例的关系**：具体项目的路径、讲次映射、图筛选结果、进度，记在该项目的实例 SOP（本项目为同目录 `SOP_课件扒取.md`）里；本文件只记**方法**。
- **维护**：口径或目录契约调整时改本文件；项目实例只同步差异，不逐字复制。

---

*本通用版与项目实例 SOP 同构（§0–§8 一一对应），可对照阅读。*
