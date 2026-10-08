# =====================================================================
# 秒级探针：matplotlib mathtext + 中文 + SVG + GBK 的边界行为
# 目的：把"图内 mathtext 书写"的经验从'靠运气'变成'有实测依据'。
# 只做测量，不改课程产物；输出写在本目录 _probe/ 下。
# 规模纪律：总耗时 < 10 秒。
# ---------------------------------------------------------------------
# 实测结论（2026-10-08；Windows / stdout=gbk / matplotlib Agg / svg.fonttype=path）：
#  [1] mathtext 在 text/title/xlabel/ylabel/legend/annotate/ticklabel 全支持：
#      希腊字母、上下标、\frac、\sin\cos\max、\sum\int、^\circ 均正常。
#  [2] 中文放进 $...$ 内 -> 缺字形，渲染成替身符号（空框），仅打印
#      "Font 'rm' does not have a glyph" 告警、不报错。规则：中文一律放 $...$ 之外。
#  [3] `%` 在 mathtext 内不转义 -> 直接 ValueError/ParseException（本次唯一硬报错）。
#      规则：mathtext 内写 \%。
#  [4] `$` 未配对（多/少一个）-> 不报错，整串按字面显示（\sigma 原样出现）——
#      静默错误，比报错更坑。规则：交付前数 $ 是否偶数。
#  [5] SVG(fonttype=path)：font-family 出现 0 次、全部转 <path>（含 mathtext）
#      -> 成品零字体依赖。
#  [6] GBK 控制台：希腊字母 σ τ α Δ φ 与 ° ≤ → 均可编码；但 ₁ ² 等上下标
#      unicode 不可编码（UnicodeEncodeError）。规则：print 保持 ASCII 转写，
#      尤其不打印上下标 unicode。
# 诊断图：mathtext_probe.png / _cjk_in_math.png（中文进数学模式）/ _unmatched_dollar.png
# =====================================================================
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

HERE = os.path.dirname(os.path.abspath(__file__))
print("stdout encoding =", sys.stdout.encoding)

# ---------------------------------------------------------------------
print("\n=== 探针 A：GBK 控制台能编码哪些符号（GBK 纪律的边界）===")
for s in ["sigma", "σ", "τ", "α", "Δ", "φ", "°", "≤", "→", "M₁", "x²"]:
    cp = "U+%04X" % ord(s[0])
    try:
        s.encode(sys.stdout.encoding)
        print("  [可编码]   %s  %s" % (cp, s))
    except UnicodeEncodeError:
        print("  [不可编码] %s  （当前控制台缺此字形）" % cp)

# ---------------------------------------------------------------------
print("\n=== 探针 B：未配对的 $ 会怎样 ===")
try:
    f = plt.figure()
    f.text(0.1, 0.5, r"坏串 $ \sigma")            # 单边 $
    f.savefig(os.path.join(HERE, "_unmatched_dollar.png"))
    plt.close(f)
    print("  未配对 $：渲染未抛异常（见 _unmatched_dollar.png）")
except Exception as e:
    print("  未配对 $：抛异常 -> %r" % e)

# ---------------------------------------------------------------------
print("\n=== 探针 C：中文放进 $...$ 内部会怎样 ===")
try:
    f = plt.figure()
    f.text(0.1, 0.5, r"$\sigma_{中文}$ 与 $\mathrm{中文}$")
    f.savefig(os.path.join(HERE, "_cjk_in_math.png"))
    plt.close(f)
    print("  中文进数学模式：渲染未抛异常（见 _cjk_in_math.png，看是否缺字形）")
except Exception as e:
    print("  中文进数学模式：抛异常 -> %r" % e)

# ---------------------------------------------------------------------
print("\n=== 探针 D：各类 artist + 各种 mathtext 语法 ===")
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11, 5))
ax.axis("off")
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
cases = [
    r"1) 混合：正应力 $\sigma_\alpha$，切应力 $\tau_\rho$",
    r"2) 分式函数：$\frac{\sigma}{2}\sin 2\alpha$、$\Delta L=\frac{NL}{EA}$",
    r"3) 上下标：$M_1\ P_2\ W_t\ I_p\ \tau_{\max}$",
    r"4) 度数：$\alpha=45^\circ$",
    r"5) 希腊全套：$\sigma\tau\gamma\rho\varphi\alpha\varepsilon\mu$",
    r"6) 求和/积分：$\sum N_i L_i$、$\int_0^L \frac{M}{EI}\mathrm{d}x$",
    r"7) 百分号：外部 100%，mathtext 内 $50\%$",
    r"8) 中文在 $: 之外没问题，内部 $\sigma$ 没问题",
]
y = 9.3
for c in cases:
    ax.text(0.3, y, c, fontsize=12)
    y -= 1.15
ax.set_title(r"探针 D：图内文字 mathtext（title/xlabel/legend/annotate 各测一处）", fontsize=11)
ax.set_xlabel(r"x 轴：$\sigma$ / MPa")
ax.set_ylabel(r"y 轴：$\tau$ / MPa")

# ax2：负号刻度 + legend + annotate
import numpy as np
xs = np.linspace(0, 6, 50)
ax2.plot(xs, -2.5 * xs, color="#c0392b", lw=2, label=r"$\tau_\rho = -\frac{T\rho}{I_p}$（负值）")
ax2.legend(fontsize=10)
ax2.annotate(r"点：$\sigma=100$", xy=(3, -7.5), xytext=(1, -12), fontsize=10,
             arrowprops=dict(arrowstyle="->"))
ax2.set_title(r"探针 D2：负号刻度 + legend + annotate", fontsize=11)
ax2.set_xlabel(r"$\alpha$ / deg")
ax2.set_ylabel(r"$\sigma$ / MPa（含负值）")

for stem in ["mathtext_probe", "mathtext_probe"]:
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, stem + ".png"), dpi=150)
    fig.savefig(os.path.join(HERE, stem + ".svg"))
plt.close(fig)
print("  已保存 mathtext_probe.png / .svg")

# ---------------------------------------------------------------------
print("\n=== 探针 E：SVG(fonttype=path) 里是否仍引用字体 ===")
svg_txt = open(os.path.join(HERE, "mathtext_probe.svg"), encoding="utf-8").read()
print("  font-family 出现次数：", svg_txt.count("font-family"))
print("  <path 元素数量（文字转路径的旁证）：", svg_txt.count("<path"))

# ---------------------------------------------------------------------
print("\n=== 探针 F：`%` 在 mathtext 内是否需要转义 ===")
# 正确写法：转义 \%
f = plt.figure()
f.text(0.1, 0.6, r"正确（转义）：$50\%$")
f.savefig(os.path.join(HERE, "_percent_ok.png"))
plt.close(f)
print("  已保存 _percent_ok.png（转义写法，供目检）")
# 错误写法：不转义 -> 硬报错（在 savefig 渲染时抛，故无法出图）
try:
    f = plt.figure()
    f.text(0.1, 0.6, r"错误（未转义）：$50%$")
    f.savefig(os.path.join(HERE, "_percent_bad.png"))
    plt.close(f)
    print("  未转义：未报错（？？）")
except Exception as e:
    print("  未转义：抛异常 -> %r（无法出图，这正是问题所在）" % e)

print("\n[DONE] 探针完成。")
