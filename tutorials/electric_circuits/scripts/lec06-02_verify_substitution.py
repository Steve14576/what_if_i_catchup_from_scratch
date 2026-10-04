# =====================================================================
# lec06-02 替代定理：把"已知的支路"换成源（两种换法）+ 05 回扣 + 图 2
#          （第 06 讲 §3；图 2 三面板）
# 规模纪律：总耗时 < 10 秒（纯算术 + 一张三面板图）。
# 方法：
#   实验 1：04 电路负载支路（已解出 u=8V、i=4A）两种替代：
#           (a) 换成 8 V 电压源 -> 两电源支路电流 2 A / 2 A（与原来一致）；
#           (b) 换成 4 A 电流源 -> 1 个方程得 V = 8 V（与原来一致）。
#   实验 2：三源电路（04 电路 + 2A 注入）的替代：9 V 电压源版 / 4.5 A 电流源版。
#   实验 3：05 讲回扣——把 R4 换成 2 V 源、R3 换成 4 V 源的两次替换，就是替代定理的日常。
#   并生成 figures/lec06_fig2_substitution.svg/.png（原电路 / 电压源版 / 电流源版）。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
# =====================================================================
import os

import matplotlib
matplotlib.use("Agg")

import schemdraw
import schemdraw.elements as elm

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../electric_circuits
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

elm.style(elm.STYLE_IEC)
schemdraw.config(font="Microsoft YaHei", fontsize=14)

# ---------------------------------------------------------------------
print("=== 实验 1：04 电路负载支路的两种替代 ===")
V_orig = 8.0
print("  原解核对：u = %.0f V、i = %.0f A" % (V_orig, V_orig / 2))
# (a) 换成 8 V 电压源（+ 朝上）：两条电源支路电流
i_left_a = (12 - 8.0) / 2.0
i_right_a = (8.0 - 10) / 1.0   # 结点->10V 源方向；负号表示实际自源流入结点
print("  (a) 8 V 电压源版：左 %.0f A（流入结点）、右 %.0f A（结点->源）；"
      "结点 KCL：%.0f + (%.0f) = %.0f A 全部流入替换源（= 原负载电流）"
      % (i_left_a, i_right_a, i_left_a, -i_right_a, i_left_a - i_right_a))
# (b) 换成 4 A 电流源（向下）
V_b = (12 / 2 + 10 / 1 - 4) / (1 / 2 + 1 / 1)   # (V-12)/2 + (V-10)/1 + 4 = 0
print("  (b) 4 A 电流源版：1 个方程 -> V = %.0f V（与原来一致）；差 = %.2e"
      % (V_b, abs(V_b - V_orig)))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：三源电路的替代（作业 Q5） ===")
# 三源电路：04 电路 + 2 A 注入；负载 4.5 A、结点 9 V
i_left_q = (12 - 9.0) / 2.0
i_right_q = (10 - 9.0) / 1.0
print("  (a) 负载换 9 V 源：左 %.1f + 右 %.0f + 注入 2 = %.1f A 流入替换源（= 原负载电流）"
      % (i_left_q, i_right_q, i_left_q + i_right_q + 2))
V_q_b = ((12 / 2 + 10 / 1 + 2 - 4.5 * 1) / (1 / 2 + 1 / 1))  # (V-12)/2 + (V-10)/1 = 2 - 4.5
print("  (b) 负载换 4.5 A 源：V = %.0f V（与原来一致）" % V_q_b)

# ---------------------------------------------------------------------
print()
print("=== 实验 3：05 讲回扣（两次替换都是替代定理） ===")
# 05 讲中：R4（0.5k，压 2V）-> 2V 源；R3（1k，压 4V）-> 4V 源，答案仍 6/2 V
print("  R4 -> 2 V 源：u1 = 6 V、u2 = 2 V（05 讲已实测）；")
print("  R3 -> 4 V 源（超级结点）：u1 = 6 V、u2 = 2 V（05 讲已实测）。")
print("  -> 当时说'数字挑得刚好'，现在可以正式给它名字：替代定理。")

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：替代定理三面板 ===")
with schemdraw.Drawing(show=False) as d:
    def panel(x0, title):
        global d
        # 左支路：12V + 2Ω
        d += elm.SourceV().at((x0, 0)).up().length(1.0)
        d += elm.Label().at((x0 - 0.85, 0.5)).label("12 V")
        d += elm.Resistor().at((x0, 1.0)).up().length(0.7)
        d += elm.Label().at((x0 - 0.9, 1.35)).label("2 Ω")
        d += elm.Line().at((x0, 1.7)).to((x0, 2.2))
        # 顶部横线 + 结点
        d += elm.Line().at((x0, 2.2)).to((x0 + 3.4, 2.2))
        d += elm.Dot().at((x0 + 1.7, 2.2))
        d += elm.Line().at((x0 + 1.7, 2.2)).to((x0 + 1.7, 1.7))
        d += elm.Line().at((x0 + 1.7, 0.5)).to((x0 + 1.7, 0))
        # 右支路：10V + 1Ω
        d += elm.SourceV().at((x0 + 3.4, 0)).up().length(1.0)
        d += elm.Label().at((x0 + 4.35, 0.5)).label("10 V")
        d += elm.Resistor().at((x0 + 3.4, 1.0)).up().length(0.7)
        d += elm.Label().at((x0 + 4.3, 1.35)).label("1 Ω")
        d += elm.Line().at((x0 + 3.4, 1.7)).to((x0 + 3.4, 2.2))
        # 底部公共线
        d += elm.Line().at((x0, 0)).to((x0 + 3.4, 0))
        d += elm.Label().at((x0 + 1.7, -0.55)).label(title, fontsize=10)

    def load_resistor(x0):
        global d
        d += elm.Resistor().at((x0 + 1.7, 0.5)).up().length(1.2)
        d += elm.Label().at((x0 + 2.45, 1.05)).label("2 Ω")
        d += elm.Label().at((x0 + 1.7, 2.75)).label("u = 8 V，i = 4 A")

    def load_vsource(x0):
        global d
        d += elm.SourceV().at((x0 + 1.7, 0.5)).up().length(1.2)
        d += elm.Label().at((x0 + 2.7, 1.05)).label("8 V")
        d += elm.Label().at((x0 + 1.7, 2.75)).label("替换为 8 V 电压源")

    def load_isource(x0):
        global d
        d += elm.SourceI().at((x0 + 1.7, 1.7)).down().length(1.2)
        d += elm.Label().at((x0 + 2.5, 1.05)).label("4 A")
        d += elm.Label().at((x0 + 1.7, 2.75)).label("替换为 4 A 电流源")

    # (a) 原电路：负载已解出
    x0 = 0.0
    panel(x0, "（a）原电路：负载支路的解已知")
    load_resistor(x0)

    # (b) 替换为 8 V 电压源
    x1 = 7.0
    panel(x1, "（b）换成 8 V 电压源")
    load_vsource(x1)

    # (c) 替换为 4 A 电流源
    x2 = 14.0
    panel(x2, "（c）换成 4 A 电流源")
    load_isource(x2)

save_stem = "lec06_fig2_substitution"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec06-02 完成。")