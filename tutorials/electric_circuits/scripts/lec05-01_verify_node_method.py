# =====================================================================
# lec05-01 结点电压法基础：引子 1 方程、两级采样网络全解、观察法与程序化组装
#          （第 05 讲 引子 / §1-§2）
# 规模纪律：总耗时 < 10 秒（纯算术 + 一张图）。
# 方法：
#   实验 1：04 电路（12V+2Ω ∥ 2Ω ∥ 10V+1Ω）结点法 1 个方程：(V-12)/2 + (V-10)/1 + V/2 = 0
#           -> V = 8 V；与 04 讲回路法 2 个方程对照。
#   实验 2：两级采样网络（16V + 1k 串, 结点1 接 1k 到参考, 结点1-结点2 串 1k, 结点2 接 0.5k）
#           基础列法 2 个方程 -> u1 = 6 V、u2 = 2 V；支路电流与功率账 160 = 100+36+16+8 mW。
#   实验 3：观察法矩阵 [3,-1;-1,3][u1,u2] = [16,0]（单位 mS/mA）核对；矩阵对称性。
#   实验 4：换参考结点（参考点移到原结点 2）：方程与解整体平移，差值不变。
#   实验 5：程序化组装对照——从支路清单自动组装 G 与右端，与手写矩阵逐项一致（埋 24 讲钩子）。
#   并生成 figures/lec05_fig1_ladder.svg/.png（两级采样网络）。
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
print("=== 实验 1：04 电路的结点法版（1 个方程） ===")
# 对顶部结点列 KCL（把底部公共点选为参考结点 0 V）
V = (12 / 2 + 10 / 1) / (1 / 2 + 1 / 1 + 1 / 2)
print("  (V-12)/2 + (V-10)/1 + V/2 = 0  ->  V = %.0f V" % V)
print("  支路电流：左 %.0f A、右 %.0f A、负载 %.0f A（与 04 讲回路法 2 个方程同答案）"
      % ((12 - V) / 2, (10 - V) / 1, V / 2))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：两级采样网络（基础列法，2 个方程） ===")
# 结点 1： (u1-16)/1 + u1/1 + (u1-u2)/1 = 0  -> 3u1 - u2 = 16
# 结点 2： (u2-u1)/1 + u2/0.5 = 0            -> -u1 + 3u2 = 0
A = np.array([[3.0, -1.0], [-1.0, 3.0]])
u = np.linalg.solve(A, np.array([16.0, 0.0]))
u1, u2 = u
print("  解：u1 = %.0f V，u2 = %.0f V" % (u1, u2))
i_r1 = (16 - u1) / 1.0
i_r2 = u1 / 1.0
i_r3 = (u1 - u2) / 1.0
i_r4 = u2 / 0.5
print("  支路电流（mA）：R1 %.0f、R2 %.0f、R3 %.0f、R4 %.0f"
      % (i_r1, i_r2, i_r3, i_r4))
print("  KCL 残差：结点1 %.2e；结点2 %.2e mA"
      % (i_r1 - i_r2 - i_r3, i_r3 - i_r4))
p_src = 16 * i_r1
p_r1, p_r2 = 1 * i_r1 ** 2, u1 ** 2 / 1
p_r3, p_r4 = 1 * i_r3 ** 2, u2 ** 2 / 0.5
print("  功率账（mW）：源 %.0f = R1 %.0f + R2 %.0f + R3 %.0f + R4 %.0f；残差 = %.2e"
      % (p_src, p_r1, p_r2, p_r3, p_r4, p_src - p_r1 - p_r2 - p_r3 - p_r4))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：观察法矩阵核对 ===")
G = np.array([[1.0 / 1 + 1.0 / 1 + 1.0 / 1, -1.0 / 1],
              [-1.0 / 1, 1.0 / 1 + 1.0 / 0.5]])
Is = np.array([16.0 / 1, 0.0])
u_obs = np.linalg.solve(G, Is)
print("  G = [[%.0f, %.0f], [%.0f, %.0f]]（mS），右端 = [%.0f, %.0f]（mA）"
      % (G[0, 0], G[0, 1], G[1, 0], G[1, 1], Is[0], Is[1]))
print("  观察法解：u1 = %.0f、u2 = %.0f；与基础列法差 = %.2e"
      % (u_obs[0], u_obs[1], abs(u_obs[0] - u1) + abs(u_obs[1] - u2)))
print("  对称性核对：G12 = %.1f，G21 = %.1f -> 相等：%s"
      % (G[0, 1], G[1, 0], G[0, 1] == G[1, 0]))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：换参考结点（参考点移到原结点 2） ===")
# 新的未知量：a = 结点 1 的电位、b = 原参考结点的电位（都以原结点 2 为 0）
# 结点 1：(a-b) 经 R2 到原参考、(a) 经 R3 到新参考、R1+源支路
A2 = np.array([[3.0, -2.0], [-1.0, 2.0]])
b2 = np.array([16.0, -8.0])
a, b = np.linalg.solve(A2, b2)
print("  解：结点1 电位 a = %.0f V、原参考结点电位 b = %.0f V" % (a, b))
print("  差值核对：a - 0 = %.0f（= 原 u1-u2）；0 - b = %.0f（= 原 u2）；差 = %.2e"
      % (a, -b, abs(a - (u1 - u2)) + abs(-b - u2)))
print("  -> 换参考点：解整体平移，差值（真实支路电压）不变；方程数仍为 n-1 = 2")

# ---------------------------------------------------------------------
print()
print("=== 实验 5：程序化组装对照（埋 24 讲的钩子） ===")
# 支路清单：(起点, 终点, 电导 mS, 串联电压源 V)（仅演示组装思路）
branches = [
    ("源", "n1", 1.0, 16.0),    # 16 V 源 + 1 kΩ 串，方向从源到 n1
    ("n1", "0", 1.0, 0.0),      # R2
    ("n1", "n2", 1.0, 0.0),     # R3
    ("n2", "0", 2.0, 0.0),      # R4（0.5 kΩ）
]
nodes = ["n1", "n2"]
Gp = np.zeros((2, 2))
Ip = np.zeros(2)
for (a1, a2, g, us) in branches:
    # 每条电阻支路：两端结点各在对角线 +g；若两端都是未知结点，互项 -g
    for p in (a1, a2):
        if p in nodes:
            Gp[nodes.index(p), nodes.index(p)] += g
    if a1 in nodes and a2 in nodes:
        Gp[nodes.index(a1), nodes.index(a2)] -= g
        Gp[nodes.index(a2), nodes.index(a1)] -= g
    # 串联电压源（"+"端朝 a2 侧）：向 a2 注入 g*us
    if us != 0.0:
        if a2 in nodes:
            Ip[nodes.index(a2)] += g * us
        if a1 in nodes:
            Ip[nodes.index(a1)] -= g * us
print("  程序组装 G = [[%.0f, %.0f], [%.0f, %.0f]]" % (Gp[0, 0], Gp[0, 1], Gp[1, 0], Gp[1, 1]))
print("  手写矩阵   G = [[%.0f, %.0f], [%.0f, %.0f]]" % (G[0, 0], G[0, 1], G[1, 0], G[1, 1]))
print("  逐项一致：%s（右端 = [%.0f, %.0f] -> 解 = [%.1f, %.1f]）"
      % (np.allclose(Gp, G), Ip[0], Ip[1],
         *np.linalg.solve(Gp, Ip)))
print("  -> 观察法的'矩阵'可以完全由支路清单自动拼出来——这正是仿真软件的日常")

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：两级采样网络 ===")
with schemdraw.Drawing(show=False) as d:
    # 左：16 V 源（+ 在上）+ 顶部横线上的 R1
    d += elm.SourceV().at((0, 0)).up().length(1.5)
    d += elm.Label().at((-1.05, 0.75)).label("16 V")
    d += elm.Line().at((0, 1.5)).to((0, 2.8))
    d += elm.Line().at((0, 2.8)).to((0.4, 2.8))
    d += elm.Resistor().at((0.4, 2.8)).right().length(2.0)
    d += elm.Label().at((1.4, 3.35)).label("$R_1$ = 1 kΩ")
    d += elm.Line().at((2.4, 2.8)).to((3, 2.8))
    # 结点 1：R2 到参考、R3 到结点 2
    d += elm.Dot().at((3, 2.8))
    d += elm.Resistor().at((3, 2.2)).down().length(1.4)
    d += elm.Label().at((4.55, 1.5)).label("$R_2$ = 1 kΩ")
    d += elm.Line().at((3, 2.8)).to((3, 2.2))
    d += elm.Line().at((3, 0.8)).to((3, 0))
    d += elm.Line().at((3, 2.8)).to((3.6, 2.8))
    d += elm.Resistor().at((3.6, 2.8)).right().length(1.8)
    d += elm.Label().at((4.5, 3.35)).label("$R_3$ = 1 kΩ")
    d += elm.Line().at((5.4, 2.8)).to((6, 2.8))
    # 结点 2：R4 到参考
    d += elm.Dot().at((6, 2.8))
    d += elm.Resistor().at((6, 2.2)).down().length(1.4)
    d += elm.Label().at((7.55, 1.5)).label("$R_4$ = 0.5 kΩ")
    d += elm.Line().at((6, 2.8)).to((6, 2.2))
    d += elm.Line().at((6, 0.8)).to((6, 0))
    # 底部公共线与参考
    d += elm.Line().at((0, 0)).to((6, 0))
    d += elm.Label().at((3, -0.6)).label("参考结点（电位 0）")
    d += elm.Label().at((3.2, 2.98)).label("①")
    d += elm.Label().at((6.2, 2.98)).label("②")
save_stem = "lec05_fig1_ladder"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec05-01 完成。")