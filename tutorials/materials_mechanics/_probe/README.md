# 探针结论档：matplotlib mathtext × 中文 × SVG × GBK 边界

> 本目录的 `mathtext_probe.py` 是秒级探针，本文件是它的**结论档**（文档 + 可复现脚本成对）。
> 用途：把"图内用 mathtext 写希腊字母/公式"这件事从"凭手感"钉成"有实测依据"；本课程及后续力学类课程的配图据此执行。
> 复跑：`uv run --with numpy --with matplotlib python _probe/mathtext_probe.py`（秒级）。
> 环境：2026-10-08，Windows，Python stdout 编码 = **gbk**，matplotlib **Agg** 后端，`svg.fonttype = "path"`。

## 结论（八条）

| # | 断言 | 症状 / 依据 | 规则 |
|---|---|---|---|
| 1 | mathtext 在 text / title / xlabel / ylabel / legend / annotate / ticklabel **全部可用**，且支持希腊字母、上下标、`\frac`、`\sin\cos\max`、`\sum\int`、`^\circ` | `mathtext_probe.png` 目检全部正常 | 正常用即可 |
| 2 | **中文放进 `$...$` 内部 → 缺字形**，渲染成替身空框 | `_cjk_in_math.png` 显示 `σ_□□`、`□□`；控制台打印 `Font 'rm' does not have a glyph ... substituting with a dummy symbol`（**只有告警、不报错**） | 中文一律写在 `$...$` **之外** |
| 3 | **mathtext 内 `%` 未转义 → 直接硬报错** | 未转义 `$50%$` 在 savefig 渲染时抛 `ValueError/ParseException`（连图都出不来）；转义 `$50\%$` 正常（`_percent_ok.png`） | mathtext 内写 `\%` |
| 4 | **`$` 未配对（多/少一个）→ 不报错**，整串按字面显示 | `_unmatched_dollar.png` 把 `坏串 $ \sigma` 原样显示（`\sigma` 未解析）——**静默错误，比报错更坑** | 交付前数 `$`，必须成对（偶数） |
| 5 | SVG（`fonttype=path`）**零字体依赖** | 探针 E：输出 SVG 里 `font-family` 出现 **0** 次、`<path` 143 个（含 mathtext 也转路径） | SVG 可直接分发，查看方无需装字体 |
| 6 | GBK 控制台能打印的符号有限 | `stdout=gbk`：希腊字母 σ τ α Δ φ、`°`、`≤`、`→` **可编码**；但 `₁ ²` 等**上下标 unicode 不可编码**（`UnicodeEncodeError`） | `print` 保持 ASCII 转写，尤其**不要打印上下标 unicode** |
| 7 | **mathtext 不支持 `\le` / `\ge` 简写 → 硬报错** | 第 16 讲绘图实测：mathtext 里用 `\le` 构造"绝对值不等式"时，savefig 渲染抛 `ValueError: ParseFatalException: Unknown symbol: \le`（图完全出不来）；改用 `\leq` / `\geq` 后正常 | mathtext 内不等式**一律写 `\leq` / `\geq`**（md 正文可用 `\le`，matplotlib 图内不可） |
| 8 | **mathtext 不支持 `\displaystyle` → 硬报错** | 第 18 讲绘图实测：`$\displaystyle\int...$` 在 savefig 渲染时抛 `ParseFatalException: Unknown symbol: \displaystyle`；去掉后正常 | mathtext 内不要写 `\displaystyle`（`\dfrac`、`\int` 本身可用，积分号大小由字体自身决定） |

## 最该记住的两条

- **③ `%` → `\%`**：唯一会**硬报错**的写法。
- **④ `$` 必须配对**：**不报错却静默变字面**，比报错更危险——交付前务必数一遍。

## 对本课程的现实影响

- 更正了此前"控制台禁所有非 ASCII"的过严判断：GBK 实际能打希腊字母与 `→/°`，真正不行的是上下标 unicode。
- lec01–05 的 15 张图已由 ASCII 转写统一改为 mathtext；lec06 起默认沿用；`print` 控制台输出保持 ASCII。
- 多行标签用 `r"$...$" + "\n" + r"$...$"` 拼接（原始串不能含真换行，普通串里 mathtext 反斜杠又要转义）。

## 证据文件

| 文件 | 看什么 |
|---|---|
| `mathtext_probe.py` | 探针脚本（头部含本结论摘要，可复跑） |
| `mathtext_probe.png` | 各类语法 + 各类 artist + 负号刻度，全部正常 |
| `_cjk_in_math.png` | 中文进数学模式 → 空框替身符号 |
| `_unmatched_dollar.png` | `$` 未配对 → 整串字面显示 |
| `_percent_ok.png` | `$50\%$` 转义写法 → 正常显示 `50%` |
