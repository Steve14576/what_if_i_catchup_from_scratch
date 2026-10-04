# =====================================================================
# lec04-01 支路电流法与回路电流法基础：引子电路全解、计数核对（第 04 讲 引子 / §1-§3）
# 规模纪律：总耗时 < 10 秒（纯算术 + 两张图）。
# 方法：
#   实验 1：引子电路（左 12V+2Ω、中 2Ω 负载、右 10V+1Ω）用 03 的手艺快捷解（电源互换）：
#           16 A 并 0.5 Ω -> V = 8 V；i1 = 2 A、i2 = 2 A、i3 = 4 A。
#   实验 2：支路电流法 3 方程解：KCL i1+i2-i3=0；KVL 2i1+2i3=12、i2+2i3=10；
#           解残差与功率账（44 = 32 + 8 + 4 W）。
#   实验 3：回路电流法 2 方程解：4I1-2I2=12、-2I1+3I2=-10 -> I1=2、I2=-2；
#           组合还原支路电流与实验 2 一致；并实测"外圈方程 = 两网孔方程之和"（独立性）
#           与系数矩阵秩 = 2（唯一性）。
#   实验 4：计数核对——两种电路规模下的 n/b 与方程数（引子电路与"田"字网络）。
#   实验 5：作业数字预验证（Q3-Q7 全部手算数字过一遍脚本）。
#   并生成 figures/lec04_fig1_parallel_supply.svg/.png 与 lec04_fig2_branch_vs_loop.svg/.png。
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


def draw_circuit(d, x0, left_v=12.0, left_r="2 Ω", right_v=10.0, right_r="1 Ω"):
    """画"日"字电路：左支路源+电阻、中支路电阻、右支路源+电阻（x0 为横向偏移）。"""
    d += elm.SourceV().at((x0, 0)).up().length(1.5)
    d += elm.Resistor().at((x0, 1.5)).up().length(1.2)
    d += elm.Line().at((x0, 2.7)).to((x0, 3.5))
    d += elm.Resistor().at((x0 + 3, 1.2)).up().length(1.4)
    d += elm.Line().at((x0 + 3, 0)).to((x0 + 3, 1.2))
    d += elm.Line().at((x0 + 3, 2.6)).to((x0 + 3, 3.5))
    d += elm.SourceV().at((x0 + 6, 0)).up().length(1.5)
    d += elm.Resistor().at((x0 + 6, 1.5)).up().length(1.2)
    d += elm.Line().at((x0 + 6, 2.7)).to((x0 + 6, 3.5))
    d += elm.Line().at((x0, 3.5)).to((x0 + 6, 3.5))
    d += elm.Line().at((x0, 0)).to((x0 + 6, 0))
    d += elm.Dot().at((x0 + 3, 3.5))
    d += elm.Dot().at((x0 + 3, 0))
    d += elm.Label().at((x0 - 1.05, 0.75)).label("%.0f V" % left_v)
    d += elm.Label().at((x0 - 0.85, 2.1)).label(left_r)
    d += elm.Label().at((x0 + 7.05, 0.75)).label("%.0f V" % right_v)
    d += elm.Label().at((x0 + 6.9, 2.1)).label(right_r)
    d += elm.Label().at((x0 + 3.8, 1.9)).label("2 Ω")


# ---------------------------------------------------------------------
print("=== 实验 1：引子电路——03 手艺快捷解（电源互换） ===")
# 左支路 12V+2Ω -> 6A 并 2Ω；右支路 10V+1Ω -> 10A 并 1Ω；与负载 2Ω 并联
I_comb = 6.0 + 10.0
G_total = 1 / 2 + 1 / 1 + 1 / 2
V_node = I_comb / G_total
i1 = (12.0 - V_node) / 2.0
i2 = (10.0 - V_node) / 1.0
i3 = V_node / 2.0
print("  合并：16 A 灌进 (2∥1∥2) = %.2f Ω：V = %.1f V" % (1 / G_total, V_node))
print("  i1 = (12-8)/2 = %.1f A；i2 = (10-8)/1 = %.1f A；i3 = 8/2 = %.1f A" % (i1, i2, i3))
print("  KCL 残差：i1 + i2 - i3 = %.2e A" % (i1 + i2 - i3))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：支路电流法（3 个方程） ===")
A_b = np.array([[1.0, 1.0, -1.0], [2.0, 0.0, 2.0], [0.0, 1.0, 2.0]])
b_b = np.array([0.0, 12.0, 10.0])
sol_b = np.linalg.solve(A_b, b_b)
print("  解：i1 = %.0f A，i2 = %.0f A，i3 = %.0f A" % tuple(sol_b))
print("  KVL 残差：2i1+2i3-12 = %.2e；i2+2i3-10 = %.2e"
      % (2 * sol_b[0] + 2 * sol_b[2] - 12, sol_b[1] + 2 * sol_b[2] - 10))
p_src = 12 * sol_b[0] + 10 * sol_b[1]
p_load = 2 * sol_b[2] ** 2
p_r1 = 2 * sol_b[0] ** 2
p_r2 = 1 * sol_b[1] ** 2
print("  功率账（W）：发出 %.0f = 负载 %.0f + %.0f + %.0f；残差 = %.2e"
      % (p_src, p_load, p_r1, p_r2, p_src - p_load - p_r1 - p_r2))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：回路电流法（2 个方程）+ 独立性实测 ===")
A_m = np.array([[4.0, -2.0], [-2.0, 3.0]])
b_m = np.array([12.0, -10.0])
I1, I2 = np.linalg.solve(A_m, b_m)
print("  解：I1 = %.0f A，I2 = %.0f A（I2 为负 = 实际环流与顺时针相反）" % (I1, I2))
i1_m, i2_m, i3_m = I1, -I2, I1 - I2
print("  组合还原：i1 = I1 = %.0f；i2 = -I2 = %.0f；i3 = I1-I2 = %.0f"
      % (i1_m, i2_m, i3_m))
print("  与支路法一致性差 = %.2e" % abs(i1_m - sol_b[0]))
# 独立性：外圈回路方程 = 两网孔方程之和（第 3 个方程是"推论"）
outer = A_m[0] + A_m[1]
rhs_outer = b_m[0] + b_m[1]
print("  外圈方程系数 = 网孔 1 + 网孔 2 =（%.0f, %.0f），右边 = %.0f"
      % (outer[0], outer[1], rhs_outer))
print("  （即 2I1 + I2 = 2——与 4I1-2I2=12、-2I1+3I2=-10 线性相关，不独立）")
print("  系数矩阵秩 = %d（= 未知量个数，解唯一）" % np.linalg.matrix_rank(A_m))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：计数核对 ===")
print("  引子电路：n = 2（上、下结点），b = 3：KCL n-1 = 1 条；KVL b-n+1 = 2 条")
print("  支路法方程数 = 3；回路法未知量/方程数 = 2")
print("  \"田\"字网络：n = 5（四个边中点 + 中心），b = 8（4 条辐条 + 4 条角路）")
print("    KCL = 4，KVL = b-n+1 = 4（恰好是 4 个网孔）")

# ---------------------------------------------------------------------
print()
print("=== 实验 5：作业数字预验证 ===")
# Q3: 左 12V+3Ω、右 11V+1Ω、负载 3Ω
G3 = 1 / 3 + 1 / 1 + 1 / 3
V3 = (12 / 3 + 11 / 1) / G3
q3 = ((12 - V3) / 3, (11 - V3) / 1, V3 / 3)
print("  Q3：V = %.0f V；i1 = %.0f、i2 = %.0f、i3 = %.0f A" % ((V3,) + q3))
print("      功率：源 %.0f W = 负载 %.0f + %.0f + %.0f"
      % (12 * q3[0] + 11 * q3[1], 3 * q3[2] ** 2, 3 * q3[0] ** 2, 1 * q3[1] ** 2))
# Q4: 同电路回路法
Aq4 = np.array([[6.0, -3.0], [-3.0, 4.0]])
I1q, I2q = np.linalg.solve(Aq4, np.array([12.0, -11.0]))
print("  Q4：I1 = %.0f，I2 = %.0f -> 支路 %.0f / %.0f / %.0f"
      % (I1q, I2q, I1q, -I2q, I1q - I2q))
# Q5: 中支路 3A 电流源（向下）的超网孔
# 外圈：3I1 + I2 = 12 - 11 = 1；约束 I1 - I2 = 3
I1q5 = (1.0 + 3.0) / 4.0
I2q5 = I1q5 - 3.0
print("  Q5：I1 = %.0f，I2 = %.0f；V = %.0f V（i1=%.0f、i2=%.0f、中 %.0f A）"
      % (I1q5, I2q5, 9.0, 1.0, 2.0, 3.0))
# Q6: 左 12V+3Ω、中 3Ω、右 1Ω+CCVS(u'=1Ω·i中)
Aq6 = np.array([[6.0, -3.0], [-2.0, 3.0]])
I1q6, I2q6 = np.linalg.solve(Aq6, np.array([12.0, 0.0]))
print("  Q6：I1 = %.0f，I2 = %.0f；u' = %.0f V；功率 %.0f = %.0f + %.0f + %.0f + %.0f"
      % (I1q6, I2q6, I1q6 - I2q6,
         12 * I1q6, 3 * I1q6 ** 2, 3 * (I1q6 - I2q6) ** 2, 1 * I2q6 ** 2,
         (I1q6 - I2q6) * I2q6))
# Q7: 左 18V+2Ω、右 6V+2Ω、负载 2Ω（右源被充电）
G7 = 1 / 2 + 1 / 2 + 1 / 2
V7 = (18 / 2 + 6 / 2) / G7
q7 = ((18 - V7) / 2, (6 - V7) / 2, V7 / 2)
print("  Q7：V = %.0f V；i1 = %.0f、i2 = %.0f（负=右源在吸收）、i3 = %.0f A" % ((V7,) + q7))
print("      功率：%.0f = %.0f + %.0f + %.0f + %.0f（含右源吸收 %.0f）"
      % (18 * q7[0], 2 * q7[2] ** 2, 2 * q7[0] ** 2, 2 * q7[1] ** 2,
         -6 * q7[1], -6 * q7[1]))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：两路电源并联供电 ===")
with schemdraw.Drawing(show=False) as d:
    draw_circuit(d, 0)
    d += elm.Label().at((3, -0.75)).label("两路电源并联供电：三条支路各是多少？")
save_stem = "lec04_fig1_parallel_supply"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("=== 生成图 2：支路电流 vs 回路电流（两种标注） ===")
with schemdraw.Drawing(show=False) as d:
    # (a) 支路电流标注
    draw_circuit(d, 0)
    d += elm.Arrow().at((0, 2.8)).to((0, 3.3))
    d += elm.Label().at((0.42, 3.02)).label("$i_1$")
    d += elm.Arrow().at((3, 1.1)).to((3, 0.55))
    d += elm.Label().at((3.38, 0.8)).label("$i_3$")
    d += elm.Arrow().at((6, 2.8)).to((6, 3.3))
    d += elm.Label().at((6.42, 3.02)).label("$i_2$")
    d += elm.Label().at((3, -0.75)).label("(a) 支路电流：每条支路一个")
    # (b) 回路电流标注
    draw_circuit(d, 10)
    d += elm.Arrow().at((10.6, 0.6)).to((10.6, 2.9))
    d += elm.Arrow().at((10.6, 2.9)).to((12.4, 2.9))
    d += elm.Arrow().at((12.4, 2.9)).to((12.4, 0.6))
    d += elm.Arrow().at((12.4, 0.6)).to((10.6, 0.6))
    d += elm.Label().at((11.45, 2.45)).label("$I_1$")
    d += elm.Arrow().at((13.6, 0.6)).to((13.6, 2.9))
    d += elm.Arrow().at((13.6, 2.9)).to((15.4, 2.9))
    d += elm.Arrow().at((15.4, 2.9)).to((15.4, 0.6))
    d += elm.Arrow().at((15.4, 0.6)).to((13.6, 0.6))
    d += elm.Label().at((14.6, 2.45)).label("$I_2$")
    d += elm.Label().at((13, -0.75)).label("(b) 回路电流：两个环流（都设顺时针）")
save_stem = "lec04_fig2_branch_vs_loop"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec04-01 完成。")