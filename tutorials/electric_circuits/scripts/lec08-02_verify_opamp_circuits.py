# =====================================================================
# lec08-02 运放的缓冲应用与作业数字预验证 + 图 3（加法/减法）
#          （第 08 讲 §3 后半与作业；图 3 双面板）
# 规模纪律：总耗时 < 10 秒（纯算术 + 一张双面板图）。
# 方法：
#   实验 1：缓冲演示——分压器（10V、1k/1k）直接带 1k 负载掉到 3.33 V；
#           经跟随器后负载上稳拿 5 V（分压器本身只给理想运放"看电压"，电流 0）。
#   实验 2：作业数字预验证：Q2 反相（2k/10k、0.4V -> -2V）；Q3 同相（2k/8k、0.6V -> 3V）；
#           Q4 加法（-1.8V）；Q5 减法（匹配版：1k/1k 输入侧、2k/3k? -> 见代码注释）；
#           Q6 有限增益（A=1e4）误差与 uN 残留。
#   并生成 figures/lec08_fig3_add_sub.svg/.png（反相加法器、差分减法器）。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ->）。
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
print("=== 实验 1：分压器直接带载 vs 跟随器缓冲 ===")
V_open = 10 * 1 / (1 + 1)
V_loaded = 10 * (1 * 1 / (1 + 1)) / (1 + 1 * 1 / (1 + 1))
print("  分压器开路 5 V；直接带 1 kΩ 负载：%.4f V（= 10/3，掉了 %.2f V）"
      % (V_loaded, V_open - V_loaded))
print("  经跟随器：负载上 %.1f V（分压器只需输出 0 A 给运放输入）——塌陷被隔离"
      % V_open)

# ---------------------------------------------------------------------
print()
print("=== 实验 2：作业数字预验证 ===")
# Q2 反相：R1=2k、Rf=10k、ui=0.4
print("  Q2：u_o = -(10/2)*0.4 = %.1f V；输入电流 = %.1f mA；输入电阻 = 2 kΩ"
      % (-(10 / 2) * 0.4, 0.4 / 2))
# Q3 同相：R1=2k、Rf=8k、ui=0.6
print("  Q3：u_o = (1 + 8/2)*0.6 = %.1f V" % ((1 + 8 / 2) * 0.6))
# Q4 加法：Rf=3k；u1=0.3/R1=1k、u2=0.9/R2=3k
print("  Q4：u_o = -3k*(0.3/1k + 0.9/3k) = %.1f V" % (-(0.3 * 3 + 0.9)))
# Q5 减法（匹配版）：R1=1k(u1->N)、Rf=3k；R2=2k(u2->P)、R3=6k（R3/R2 = Rf/R1 = 3）
R1s, Rfs = 1e3, 3e3
R2s, R3s = 2e3, 6e3
u1s, u2s = 0.2, 0.9
uPs = u2s * R3s / (R2s + R3s)
uNs = uPs
iNs = (u1s - uNs) / R1s
uOs = uNs - iNs * Rfs
print("  Q5：uP = uN = %.3f V；经 R1 电流 = %.4f mA；u_o = %.2f V（= 3*(u2-u1)）"
      % (uPs, iNs * 1e3, uOs))
# Q6 有限增益：Q2 配置 A=1e4
A = 1e4
uo6 = -0.4 * 10e3 * A / (10e3 + 2e3 * (1 + A))
print("  Q6：A=1e4 时 u_o = %.4f V（理想 -2 V，误差 %.2e V）；uN 残留 = %.4f mV"
      % (uo6, abs(uo6 + 2.0), abs(uo6) / A * 1e3))

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：反相加法器与差分减法器 ===")
with schemdraw.Drawing(show=False) as d:
    def add_panel(x0, title):
        global d
        op = elm.Opamp().at((x0 + 3.0, 1.7))
        d += op
        yN = op.in1[1]
        # u1 支路：源 -> R1 -> N 行
        d += elm.SourceV().at((x0, 0)).up().length(1.0)
        d += elm.Label().at((x0 - 0.85, 0.5)).label("$u_1$")
        d += elm.Line().at((x0, 1.0)).to((x0, yN))
        d += elm.Resistor().at((x0, yN)).right().length(0.9)
        d += elm.Label().at((x0 + 0.45, yN + 0.5)).label("$R_1$")
        d += elm.Line().at((x0 + 0.9, yN)).to((x0 + 2.0, yN))
        # u2 支路：源 -> 上到 N 行，junction
        d += elm.SourceV().at((x0 + 2.0, 0)).up().length(1.0)
        d += elm.Line().at((x0 + 2.0, 1.0)).to((x0 + 2.0, yN))
        d += elm.Label().at((x0 + 1.2, 0.5)).label("$u_2$", fontsize=11)
        d += elm.Dot().at((x0 + 2.0, yN))
        d += elm.Resistor().at((x0 + 2.0, yN)).right().length(0.8)
        d += elm.Label().at((x0 + 2.45, yN + 0.5)).label("$R_2$")
        d += elm.Line().at((x0 + 2.8, yN)).to(op.in1)
        # 反馈 Rf：从 N 上方绕行到输出
        d += elm.Line().at((x0 + 2.0, yN)).to((x0 + 2.0, yN + 1.0))
        d += elm.Resistor().at((x0 + 2.0, yN + 1.0)).right().length(1.2)
        d += elm.Label().at((x0 + 2.6, yN + 1.55)).label("$R_f$")
        d += elm.Line().at((x0 + 3.2, yN + 1.0)).to((x0 + 5.4, yN + 1.0))
        d += elm.Line().at((x0 + 5.4, yN + 1.0)).to((x0 + 5.4, op.out[1]))
        # + 端接地 + 输出 + 底轨
        d += elm.Line().at(op.in2).to((x0 + 2.3, op.in2[1]))
        d += elm.Line().at((x0 + 2.3, op.in2[1])).to((x0 + 2.3, 0))
        d += elm.Line().at(op.out).to((x0 + 5.4, op.out[1]))
        d += elm.Dot().at((x0 + 5.4, op.out[1]))
        d += elm.Line().at((x0 + 5.4, op.out[1])).to((x0 + 6.1, op.out[1]))
        d += elm.Label().at((x0 + 6.4, op.out[1] + 0.4)).label("$u_o$")
        d += elm.Line().at((x0, 0)).to((x0 + 5.4, 0))
        d += elm.Label().at((x0 + 2.8, -0.6)).label(title, fontsize=10)

    def sub_panel(x0, title):
        global d
        op = elm.Opamp().at((x0 + 3.0, 1.7))
        d += op
        yN = op.in1[1]
        # u1 支路 -> R1 -> in1（上）
        d += elm.SourceV().at((x0, 0)).up().length(1.0)
        d += elm.Label().at((x0 - 0.85, 0.5)).label("$u_1$")
        d += elm.Line().at((x0, 1.0)).to((x0, yN))
        d += elm.Resistor().at((x0, yN)).right().length(1.1)
        d += elm.Label().at((x0 + 0.55, yN + 0.5)).label("$R_1$")
        d += elm.Line().at((x0 + 1.1, yN)).to(op.in1)
        d += elm.Dot().at((x0 + 1.1, yN))
        # Rf 反馈
        d += elm.Line().at((x0 + 1.1, yN)).to((x0 + 1.1, yN + 1.0))
        d += elm.Resistor().at((x0 + 1.1, yN + 1.0)).right().length(1.3)
        d += elm.Label().at((x0 + 1.75, yN + 1.55)).label("$R_f$")
        d += elm.Line().at((x0 + 2.4, yN + 1.0)).to((x0 + 5.4, yN + 1.0))
        d += elm.Line().at((x0 + 5.4, yN + 1.0)).to((x0 + 5.4, op.out[1]))
        # u2 支路：源 -> R2 -> P 节点；R3 下地
        d += elm.SourceV().at((x0 + 0.95, 0)).up().length(0.6)
        d += elm.Label().at((x0 + 1.0, 1.05)).label("$u_2$", fontsize=11)
        d += elm.Line().at((x0 + 0.95, 0.6)).to((x0 + 1.2, 0.6))
        d += elm.Resistor().at((x0 + 1.2, 0.6)).right().length(0.8)
        d += elm.Label().at((x0 + 1.6, 1.15)).label("$R_2$", fontsize=11)
        d += elm.Line().at((x0 + 2.0, 0.6)).to((x0 + 2.35, 0.6))
        d += elm.Dot().at((x0 + 2.35, 0.6))
        d += elm.Line().at((x0 + 2.35, 0.6)).to((x0 + 2.35, op.in2[1]))
        d += elm.Line().at((x0 + 2.35, op.in2[1])).to(op.in2)
        d += elm.Resistor().at((x0 + 2.35, 0.0)).up().length(0.6)
        d += elm.Label().at((x0 + 2.95, 0.3)).label("$R_3$", fontsize=11)
        # 输出 + 底轨
        d += elm.Line().at(op.out).to((x0 + 5.4, op.out[1]))
        d += elm.Dot().at((x0 + 5.4, op.out[1]))
        d += elm.Line().at((x0 + 5.4, op.out[1])).to((x0 + 6.1, op.out[1]))
        d += elm.Label().at((x0 + 6.4, op.out[1] + 0.4)).label("$u_o$")
        d += elm.Line().at((x0, 0)).to((x0 + 5.4, 0))
        d += elm.Label().at((x0 + 2.8, -0.6)).label(title, fontsize=10)

    add_panel(0.0, "（a）反相加法器：u_o = -Rf(u1/R1 + u2/R2)")
    sub_panel(8.2, "（b）差分减法器：匹配时 u_o = (Rf/R1)(u2 - u1)")

save_stem = "lec08_fig3_add_sub"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec08-02 完成。")