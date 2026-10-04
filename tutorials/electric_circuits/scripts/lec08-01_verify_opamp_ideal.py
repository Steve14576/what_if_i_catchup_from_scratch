# =====================================================================
# lec08-01 理想运放四类电路：虚短虚断 vs 有限增益直接解
#          （第 08 讲 §2–§3；图 1 引子双面板、图 2 反相/同相）
# 规模纪律：总耗时 < 10 秒（纯算术 + 两张图）。
# 方法：
#   实验 1：反相放大器（R1=1k、Rf=10k、ui=0.5V）：理想 u_o = -5 V；
#           有限增益 A=1e5 直接解线性方程对照（含 uN 残留 ≈ -u_o/A）。
#   实验 2：同相放大器（R1=1k、Rf=9k、ui=0.3V）：理想 3 V；有限增益对照。
#   实验 3：有限增益误差表（A = 1e2..1e6）与饱和警示（|理想输出| 超电源轨）。
#   实验 4：加法器（Rf=2k；u1=0.5V/R1=1k、u2=0.4V/R2=2k）：理想 -1.4 V；有限对照。
#   实验 5：减法器（R1=R3=1k、R2=Rf=2k；u1=0.3V、u2=1.1V）：理想 1.6 V；有限对照。
#   并生成 figures/lec08_fig1_divider_buffer.svg/.png 与 lec08_fig2_inv_noninv.svg/.png。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ->）。
# =====================================================================
import os

import numpy as np
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
print("=== 运放符号锚点探针（首次使用 elm.Opamp） ===")
with schemdraw.Drawing(show=False) as dprobe:
    op = elm.Opamp().at((2, 2))
    dprobe += op
    print("  in1 =", op.in1, "；in2 =", op.in2, "；out =", op.out)

# ---------------------------------------------------------------------
print()
print("=== 实验 1：反相放大器（理想 vs 有限增益） ===")
R1, Rf, ui = 1e3, 10e3, 0.5
u_ideal = -ui * Rf / R1
A = 1e5
# 有限增益：KCL(uN)：(uN-ui)/R1 + (uN-uo)/Rf = 0；uo = -A*uN
uN_fin = ui * Rf / (Rf + R1 * (1 + A))
uo_fin = -A * uN_fin
print("  理想：u_o = %.1f V（uN = 0 虚地）；有限 A=%.0e：uN = %.4f mV、u_o = %.6f V；"
      "误差 = %.2e V" % (u_ideal, A, uN_fin * 1e3, uo_fin, abs(uo_fin - u_ideal)))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：同相放大器（理想 vs 有限增益） ===")
R1b, Rfb, uib = 1e3, 9e3, 0.3
u_ideal_b = uib * (1 + Rfb / R1b)
k = R1b / (R1b + Rfb)
uo_b = A * uib / (1 + A * k)
print("  理想：u_o = %.1f V；有限 A=%.0e：u_o = %.6f V；误差 = %.2e V"
      % (u_ideal_b, A, uo_b, abs(uo_b - u_ideal_b)))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：有限增益误差表与饱和警示 ===")
for A_test in [1e2, 1e3, 1e4, 1e5, 1e6]:
    uo_t = -ui * Rf * A_test / (Rf + R1 * (1 + A_test))
    print("  A = %.0e：u_o = %.6f V（理想 -5 V），相对误差 = %.4f%%"
          % (A_test, uo_t, 100 * abs(uo_t - (-5.0)) / 5.0))
print("  饱和警示：若 ui = 2 V -> 理想 u_o = -20 V，超过 ±12 V 电源轨——")
print("  实际电路会钳位在 -12 V 附近（饱和），虚短失效（§4 细说）。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：反相加法器（理想 vs 有限增益） ===")
Rf2, R1c, R2c, u1c, u2c = 2e3, 1e3, 2e3, 0.5, 0.4
u_ideal_c = -Rf2 * (u1c / R1c + u2c / R2c)
uN_c = (u1c / R1c + u2c / R2c) / (1 / R1c + 1 / R2c + (1 + A) / Rf2)
uo_c = -A * uN_c
print("  理想：u_o = -Rf(u1/R1 + u2/R2) = %.2f V；有限 A=%.0e：u_o = %.6f V；"
      "误差 = %.2e V" % (u_ideal_c, A, uo_c, abs(uo_c - u_ideal_c)))

# ---------------------------------------------------------------------
print()
print("=== 实验 5：差分（减法）放大器（理想 vs 有限增益） ===")
# 匹配条件：R3(接地侧)/R2(输入侧) = Rf/R1，即四个电阻"对边同比"
R1d = R2d = 1e3   # u1 -> N 的 R1；u2 -> P 的 R2
R3d = Rfd = 2e3   # P -> 地的 R3；N -> 输出的 Rf
u1d, u2d = 0.3, 1.1
u_ideal_d = (Rfd / R1d) * (u2d - u1d)
uP_d = u2d * R3d / (R2d + R3d)
uN_d = (u1d / R1d + A * uP_d / Rfd) / (1 / R1d + (1 + A) / Rfd)
uo_d = A * (uP_d - uN_d)
print("  理想：u_o = (Rf/R1)(u2-u1) = %.2f V；有限 A=%.0e：uP = %.6f V、uN = %.6f V、"
      "u_o = %.6f V；误差 = %.2e V"
      % (u_ideal_d, A, uP_d, uN_d, uo_d, abs(uo_d - u_ideal_d)))
print("  叠加视角（06 讲客串）：u1 一路给负向贡献、u2 一路经分压给正向贡献，")
print("  两贡献在输出叠加成 (u2-u1)——公式不必背，两条路各自推一遍即可。")

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：分压器带载塌陷 vs 跟随器缓冲 ===")
with schemdraw.Drawing(show=False) as d:
    def divider(x0, with_load, title, rail_to=None):
        global d
        d += elm.SourceV().at((x0, 0)).up().length(1.0)
        d += elm.Label().at((x0 - 1.0, 0.5)).label("10 V")
        d += elm.Line().at((x0, 1.0)).to((x0, 2.2))
        d += elm.Line().at((x0, 2.2)).to((x0 + 1.0, 2.2))
        d += elm.Resistor().at((x0 + 1.0, 2.2)).right().length(1.2)
        d += elm.Label().at((x0 + 1.6, 2.75)).label("5 kΩ")
        d += elm.Line().at((x0 + 2.2, 2.2)).to((x0 + 3.0, 2.2))
        d += elm.Dot().at((x0 + 2.6, 2.2))
        # R2 支路（分压点 -> 参考）
        d += elm.Resistor().at((x0 + 1.4, 0.7)).up().length(1.0)
        d += elm.Label().at((x0 + 0.55, 1.2)).label("5 kΩ")
        d += elm.Line().at((x0 + 1.4, 2.2)).to((x0 + 1.4, 1.7))
        d += elm.Line().at((x0 + 1.4, 0.7)).to((x0 + 1.4, 0))
        rail_end = rail_to if rail_to is not None else x0 + 3.0
        d += elm.Line().at((x0, 0)).to((rail_end, 0))
        if with_load:
            d += elm.Resistor().at((x0 + 2.6, 0.7)).up().length(1.0)
            d += elm.Label().at((x0 + 3.35, 1.2)).label("5 kΩ")
            d += elm.Line().at((x0 + 2.6, 2.2)).to((x0 + 2.6, 1.7))
            d += elm.Line().at((x0 + 2.6, 0.7)).to((x0 + 2.6, 0))
        d += elm.Label().at((x0 + 1.5, -0.6)).label(title, fontsize=10)

    # (a) 采样点直接带载：5 V 塌成 3.33 V
    divider(0.0, True, "（a）采样点直接带载：5 V 塌成 3.33 V")

    # (b) 空载分压 + 跟随器 + 负载（一条信号链）
    x0 = 6.4
    op = elm.Opamp().at((x0 + 4.6, 1.7))
    divider(x0, False, "（b）空载分压 + 跟随器：负载上稳稳 5 V",
            rail_to=x0 + 6.6)
    d += op
    # 分压点 -> + 输入（in2）
    d += elm.Line().at((x0 + 3.0, 2.2)).to((x0 + 3.7, 2.2))
    d += elm.Line().at((x0 + 3.7, 2.2)).to((x0 + 3.7, op.in2[1]))
    d += elm.Line().at((x0 + 3.7, op.in2[1])).to(op.in2)
    # 反馈：out -> in1（上环路）
    d += elm.Line().at(op.out).to((x0 + 6.6, op.out[1]))
    d += elm.Line().at((x0 + 6.6, op.out[1])).to((x0 + 6.6, op.in1[1] + 1.0))
    d += elm.Line().at((x0 + 6.6, op.in1[1] + 1.0)).to((x0 + 3.5, op.in1[1] + 1.0))
    d += elm.Line().at((x0 + 3.5, op.in1[1] + 1.0)).to((x0 + 3.5, op.in1[1]))
    d += elm.Line().at((x0 + 3.5, op.in1[1])).to(op.in1)
    # 输出接负载
    d += elm.Line().at((x0 + 6.6, op.out[1])).to((x0 + 6.6, 0.9))
    d += elm.Resistor().at((x0 + 6.6, 0.2)).up().length(0.7)
    d += elm.Label().at((x0 + 6.05, 0.55)).label("5 kΩ")
    d += elm.Line().at((x0 + 6.6, 0.2)).to((x0 + 6.6, 0))

save_stem = "lec08_fig1_divider_buffer"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：反相放大器与同相放大器 ===")
with schemdraw.Drawing(show=False) as d:
    def inv_panel(x0, title):
        global d
        op = elm.Opamp().at((x0 + 3.0, 1.7))
        d += op
        # 输入支路：ui 源 -> R1 -> in1（上输入，负端）
        d += elm.SourceV().at((x0, 0)).up().length(1.0)
        d += elm.Label().at((x0 - 0.85, 0.5)).label("$u_i$")
        d += elm.Line().at((x0, 1.0)).to((x0, op.in1[1]))
        d += elm.Resistor().at((x0, op.in1[1])).right().length(1.2)
        d += elm.Label().at((x0 + 0.6, op.in1[1] + 0.55)).label("$R_1$")
        d += elm.Line().at((x0 + 1.2, op.in1[1])).to(op.in1)
        d += elm.Dot().at((x0 + 1.2, op.in1[1]))
        d += elm.Label().at((x0 + 1.7, op.in1[1] - 0.5)).label("N（虚地）", fontsize=10)
        # 反馈 Rf：N 上方绕行到输出
        d += elm.Line().at((x0 + 1.2, op.in1[1])).to((x0 + 1.2, op.in1[1] + 1.0))
        d += elm.Resistor().at((x0 + 1.2, op.in1[1] + 1.0)).right().length(1.6)
        d += elm.Label().at((x0 + 2.0, op.in1[1] + 1.55)).label("$R_f$")
        d += elm.Line().at((x0 + 2.8, op.in1[1] + 1.0)).to((x0 + 5.4, op.in1[1] + 1.0))
        d += elm.Line().at((x0 + 5.4, op.in1[1] + 1.0)).to((x0 + 5.4, op.out[1]))
        # 输出引线
        d += elm.Line().at(op.out).to((x0 + 5.4, op.out[1]))
        d += elm.Dot().at((x0 + 5.4, op.out[1]))
        d += elm.Line().at((x0 + 5.4, op.out[1])).to((x0 + 6.1, op.out[1]))
        d += elm.Label().at((x0 + 6.4, op.out[1] + 0.4)).label("$u_o$")
        # + 端接地
        d += elm.Line().at(op.in2).to((x0 + 2.3, op.in2[1]))
        d += elm.Line().at((x0 + 2.3, op.in2[1])).to((x0 + 2.3, 0))
        # 底轨
        d += elm.Line().at((x0, 0)).to((x0 + 5.4, 0))
        d += elm.Label().at((x0 + 2.8, -0.6)).label(title, fontsize=10)

    def non_panel(x0, title):
        global d
        op = elm.Opamp().at((x0 + 3.0, 1.7))
        d += op
        # 输入直接进 + 端（in2）
        d += elm.SourceV().at((x0, 0)).up().length(0.7)
        d += elm.Label().at((x0 - 0.85, 0.35)).label("$u_i$")
        d += elm.Line().at((x0, 0.7)).to((x0 + 2.4, 0.7))
        d += elm.Line().at((x0 + 2.4, 0.7)).to((x0 + 2.4, op.in2[1]))
        d += elm.Line().at((x0 + 2.4, op.in2[1])).to(op.in2)
        # R1：从 in1（-端）向下到参考
        d += elm.Line().at(op.in1).to((x0 + 1.6, op.in1[1]))
        d += elm.Resistor().at((x0 + 1.6, op.in1[1])).down().length(0.9)
        d += elm.Label().at((x0 + 1.02, op.in1[1] - 0.45)).label("$R_1$", fontsize=11)
        d += elm.Line().at((x0 + 1.6, op.in1[1] - 0.9)).to((x0 + 1.6, 0))
        d += elm.Dot().at((x0 + 1.6, op.in1[1]))
        # 反馈 Rf：in1 处向上绕行到输出
        d += elm.Line().at((x0 + 1.6, op.in1[1])).to((x0 + 1.6, op.in1[1] + 1.0))
        d += elm.Resistor().at((x0 + 1.6, op.in1[1] + 1.0)).right().length(1.6)
        d += elm.Label().at((x0 + 2.4, op.in1[1] + 1.55)).label("$R_f$")
        d += elm.Line().at((x0 + 3.2, op.in1[1] + 1.0)).to((x0 + 5.4, op.in1[1] + 1.0))
        d += elm.Line().at((x0 + 5.4, op.in1[1] + 1.0)).to((x0 + 5.4, op.out[1]))
        d += elm.Line().at(op.out).to((x0 + 5.4, op.out[1]))
        d += elm.Dot().at((x0 + 5.4, op.out[1]))
        d += elm.Line().at((x0 + 5.4, op.out[1])).to((x0 + 6.1, op.out[1]))
        d += elm.Label().at((x0 + 6.4, op.out[1] + 0.4)).label("$u_o$")
        d += elm.Line().at((x0, 0)).to((x0 + 5.4, 0))
        d += elm.Label().at((x0 + 2.8, -0.6)).label(title, fontsize=10)

    inv_panel(0.0, "（a）反相放大器：u_o = -(Rf/R1) ui")
    non_panel(8.0, "（b）同相放大器：u_o = (1 + Rf/R1) ui")

save_stem = "lec08_fig2_inv_noninv"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec08-01 完成。")