# =====================================================================
# lec05-02 结点法的修正情形：无伴电压源两招、含受控源 + 作业数字预验证
#          （第 05 讲 §3；图 2/图 3）
# 规模纪律：总耗时 < 10 秒（纯算术 + 两张图）。
# 方法：
#   实验 1：无伴电压源（一端接参考）：把 R4（0.5k）换成 2 V 无伴电压源——
#           结点 2 被钉死在 2 V，只剩 1 个方程：3u1 = 18 -> u1 = 6（与引子同答案）。
#   实验 2：无伴电压源（夹在两结点之间）：把 R3 换成 4 V 无伴电压源——
#           超级结点：外圈 KCL u1 + u2 = 8；约束 u1 - u2 = 4 -> u1 = 6、u2 = 2。
#   实验 3：含受控源：把 R2 换成 VCCS（i = 3 mS x u2）——控制量恰是结点电压：
#           u1 + u2 = 8、u1 = 3u2 -> u1 = 6、u2 = 2；功率账 160 = 100+36+16+8 mW。
#   实验 4：作业数字预验证（Q2-Q5 全部手算数字过一遍脚本）。
#   并生成 figures/lec05_fig2_supernode.svg/.png 与 lec05_fig3_vccs.svg/.png。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
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
print("=== 实验 1：无伴电压源——一端接参考（R4 换成 2 V 源） ===")
# 结点 2 被钉死：u2 = 2；结点 1： (16-u1)/1 = u1/1 + (u1-2)/1 -> 3u1 = 18
u1a = (16.0 + 2.0) / 3.0
print("  3u1 = 16 + 2  ->  u1 = %.0f V（u2 = 2 V 已知，方程从 2 个减为 1 个）" % u1a)
print("  新电压源支路电流 = 原 R3 电流 = %.0f mA（电压源不像电阻那样按欧姆定律分流，它的电流由外圈定）"
      % ((u1a - 2.0) / 1.0))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：无伴电压源——夹在两结点之间（R3 换成 4 V 源） ===")
# 超级结点（结点1+结点2）：外圈 KCL：(16-u1)/1 = u1/1 + u2/0.5 -> u1 + u2 = 8
# 约束方程：u1 - u2 = 4
A_s = np.array([[1.0, 1.0], [1.0, -1.0]])
u1b, u2b = np.linalg.solve(A_s, np.array([8.0, 4.0]))
print("  超级结点 + 约束：u1 + u2 = 8、u1 - u2 = 4  ->  u1 = %.0f、u2 = %.0f" % (u1b, u2b))
print("  核对：新电压源支路电流 = 原 R3 电流 = %.0f mA（答案与引子完全一致）"
      % ((u1b - u2b) / 1.0))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：含受控源——R2 换成 VCCS（i = 3 mS x u2） ===")
# 结点 1：(16-u1)/1 = 3*u2 + (u1-u2)/1  -> u1 + u2 = 8
# 结点 2：(u1-u2)/1 = u2/0.5            -> u1 = 3u2
u2c = 8.0 / 4.0
u1c = 3.0 * u2c
i_vccs = 3.0 * u2c
print("  u1 + u2 = 8、u1 = 3u2  ->  u1 = %.0f、u2 = %.0f；受控源电流 = %.0f mA"
      % (u1c, u2c, i_vccs))
p_src = 16 * (16 - u1c) / 1.0
p_r1 = 1 * ((16 - u1c) / 1.0) ** 2
p_vccs = u1c * i_vccs
p_r3 = (u1c - u2c) ** 2 / 1.0
p_r4 = u2c ** 2 / 0.5
print("  功率账（mW）：源 %.0f = R1 %.0f + 受控源 %.0f + R3 %.0f + R4 %.0f；残差 = %.2e"
      % (p_src, p_r1, p_vccs, p_r3, p_r4, p_src - p_r1 - p_vccs - p_r3 - p_r4))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：作业数字预验证 ===")
# Q2/Q3：12V + R1=1k 串 -> n1；n1 接 R2=2k 到参考；n1-n2 串 R3=1k；n2 接 R4=1k
A_q = np.array([[2.5, -1.0], [-1.0, 2.0]])   # mS：G11 = 1 + 1/2 + 1
u_q = np.linalg.solve(A_q, np.array([12.0, 0.0]))
print("  Q2/Q3：u1 = %.0f V，u2 = %.0f V；电流（mA）：R1 %.0f、R2 %.0f、R3 %.0f、R4 %.0f"
      % (u_q[0], u_q[1], (12 - u_q[0]) / 1, u_q[0] / 2, (u_q[0] - u_q[1]) / 1, u_q[1] / 1))
print("        功率（mW）：源 %.0f = %.0f + %.0f + %.0f + %.0f"
      % (12 * (12 - u_q[0]) / 1, 1 * ((12 - u_q[0]) / 1) ** 2, u_q[0] ** 2 / 2,
         1 * (u_q[0] - u_q[1]) ** 2, 1 * u_q[1] ** 2))
# Q4：R3 换成 3 V 无伴源（夹心）-> 超级结点 + 约束
u2_q4 = (12.0 - 3.0) / 3.0  # 推导：(12-u2-3) = (u2+3)/2 + u2
u1_q4 = u2_q4 + 3.0
print("  Q4：超级结点 -> u1 = %.0f、u2 = %.0f（与原电路同答案）" % (u1_q4, u2_q4))
# Q5：R2 换成 VCCS（i = 1 mS x u2）-> u1 = 2u2、12 - u1 = u1 -> u1 = 6
A_q5 = np.array([[2.0, 0.0], [1.0, -2.0]])   # 2u1 = 12；u1 - 2u2 = 0
u1_q5, u2_q5 = np.linalg.solve(A_q5, np.array([12.0, 0.0]))
print("  Q5：VCCS（1 mS x u2）-> u1 = %.0f、u2 = %.0f；受控源电流 = %.0f mA"
      % (u1_q5, u2_q5, 1.0 * u2_q5))
# Q6：04 电路结点法 1 个方程
V_q6 = (12 / 2 + 10 / 1) / (1 / 2 + 1 / 1 + 1 / 2)
print("  Q6：V = %.0f V；功率账 44 = 32 + 8 + 4 W（04 讲已验）" % V_q6)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：超级结点（R3 换成 4 V 无伴电压源） ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.SourceV().at((0, 0)).up().length(1.5)
    d += elm.Label().at((-1.05, 0.75)).label("16 V")
    d += elm.Line().at((0, 1.5)).to((0, 2.8))
    d += elm.Line().at((0, 2.8)).to((0.4, 2.8))
    d += elm.Resistor().at((0.4, 2.8)).right().length(2.0)
    d += elm.Label().at((1.4, 3.35)).label("$R_1$ = 1 kΩ")
    d += elm.Line().at((2.4, 2.8)).to((3, 2.8))
    dot1 = elm.Dot().at((3, 2.8))
    d += dot1
    d += elm.Resistor().at((3, 2.2)).down().length(1.4)
    d += elm.Label().at((3.2, 2.98)).label("①")
    d += elm.Label().at((6.2, 2.98)).label("②")
    d += elm.Label().at((4.55, 1.5)).label("$R_2$ = 1 kΩ")
    d += elm.Line().at((3, 2.8)).to((3, 2.2))
    d += elm.Line().at((3, 0.8)).to((3, 0))
    # R3 位置换成 4 V 无伴电压源（+ 端朝结点①：u1 - u2 = 4）
    d += elm.Line().at((3, 2.8)).to((3.6, 2.8))
    src4 = elm.SourceV().at((5.4, 2.8)).left().length(1.8)
    d += src4
    d += elm.Label().at((4.5, 3.9)).label("4 V")
    d += elm.Line().at((5.4, 2.8)).to((6, 2.8))
    dot2 = elm.Dot().at((6, 2.8))
    d += dot2
    d += elm.Resistor().at((6, 2.2)).down().length(1.4)
    d += elm.Label().at((7.55, 1.5)).label("$R_4$ = 0.5 kΩ")
    d += elm.Line().at((6, 2.8)).to((6, 2.2))
    d += elm.Line().at((6, 0.8)).to((6, 0))
    d += elm.Line().at((0, 0)).to((6, 0))
    d += elm.Label().at((3, -0.6)).label("参考结点（电位 0）")
    # 超级结点：用虚线椭圆把①②和它们之间的电压源圈起来
    d += elm.Encircle([dot1, dot2, src4], padx=0.35, pady=0.3).linestyle("--")
    d += elm.Label().at((4.4, -1.25)).label("超级结点：①②合并（绕开电压源列 KCL）")
    d += elm.Label().at((4.4, -1.8)).label("约束方程：$u_1 - u_2$ = 4 V")
save_stem = "lec05_fig2_supernode"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("=== 生成图 3：含受控源（R2 换成 VCCS：i = 3 mS x u2） ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.SourceV().at((0, 0)).up().length(1.5)
    d += elm.Label().at((-1.05, 0.75)).label("16 V")
    d += elm.Line().at((0, 1.5)).to((0, 2.8))
    d += elm.Line().at((0, 2.8)).to((0.4, 2.8))
    d += elm.Resistor().at((0.4, 2.8)).right().length(2.0)
    d += elm.Label().at((1.4, 3.35)).label("$R_1$ = 1 kΩ")
    d += elm.Line().at((2.4, 2.8)).to((3, 2.8))
    d += elm.Dot().at((3, 2.8))
    # R2 位置换成受控电流源（向下）
    d += elm.Line().at((3, 2.8)).to((3, 2.2))
    d += elm.SourceControlledI().at((3, 2.2)).down().length(1.4)
    d += elm.Line().at((3, 0.8)).to((3, 0))
    d += elm.Label().at((4.6, 1.55)).label("受控电流源")
    d += elm.Label().at((4.6, 1.05)).label("$i = 3\\,\\mathrm{mS} \\cdot u_2$")
    d += elm.Line().at((3, 2.8)).to((3.6, 2.8))
    d += elm.Resistor().at((3.6, 2.8)).right().length(1.8)
    d += elm.Label().at((4.5, 3.35)).label("$R_3$ = 1 kΩ")
    d += elm.Line().at((5.4, 2.8)).to((6, 2.8))
    d += elm.Dot().at((6, 2.8))
    d += elm.Resistor().at((6, 2.2)).down().length(1.4)
    d += elm.Label().at((7.55, 1.5)).label("$R_4$ = 0.5 kΩ")
    d += elm.Line().at((6, 2.8)).to((6, 2.2))
    d += elm.Line().at((6, 0.8)).to((6, 0))
    d += elm.Line().at((0, 0)).to((6, 0))
    d += elm.Label().at((3, -0.6)).label("参考结点（电位 0）")
    d += elm.Label().at((3.2, 2.98)).label("①")
    d += elm.Label().at((6.2, 2.98)).label("②")
    d += elm.Label().at((3, -1.25)).label("控制量 $u_2$ 恰是②的结点电压——直接写进①的 KCL")
save_stem = "lec05_fig3_vccs"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec05-02 完成。")