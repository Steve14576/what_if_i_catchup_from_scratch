# =====================================================================
# lec04-02 特殊支路：电流源三招与受控源三步（第 04 讲 §4）
# 规模纪律：总耗时 < 10 秒（纯算术 + 两张图）。
# 方法：
#   实验 1：含受控源变体（左 12V+2Ω、中 2Ω、右 1Ω+CCVS，u' = 1Ω·i中）：
#           网孔方程结合控制量表达式 -> I1 = 4、I2 = 2、u' = 2 V；
#           功率账 48 = 32 + 8 + 4 + 4 W。
#   实验 2：含电流源变体：
#           (a) 右支路换成 4 A 无伴电流源（向上）——回路电流被直接钉死：I2 = -4、I1 = 1；
#               核对 V = 10 V、功率 12 + 40 = 50 + 2 W。
#           (b) 中支路换成 4 A 无伴电流源（向下）——超网孔：外圈 2I1 + I2 = 2、
#               约束 I1 - I2 = 4 -> I1 = 2、I2 = -2；核对 V = 8 V、功率 44 = 8 + 4 + 32 W。
#   并生成 figures/lec04_fig3_supermesh.svg/.png 与 lec04_fig4_controlled.svg/.png。
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
print("=== 实验 1：含受控源变体（CCVS：u' = 1Ω x i中） ===")
# 网孔 1：4I1 - 2I2 = 12；网孔 2：-2I1 + 3I2 = -u'；控制量表达式：u' = 1 x (I1 - I2)
# 代入后网孔 2 变为 -I1 + 2I2 = 0
A_c = np.array([[4.0, -2.0], [-1.0, 2.0]])
Ic1, Ic2 = np.linalg.solve(A_c, np.array([12.0, 0.0]))
u_ctrl = (Ic1 - Ic2) * 1.0
print("  解得：I1 = %.0f A，I2 = %.0f A；u' = %.0f V" % (Ic1, Ic2, u_ctrl))
print("  支路电流：左 %.0f、中 %.0f、右 %.0f A" % (Ic1, Ic1 - Ic2, Ic2))
p = (12 * Ic1, 2 * Ic1 ** 2, 2 * (Ic1 - Ic2) ** 2, 1 * Ic2 ** 2, u_ctrl * Ic2)
print("  功率账（W）：源 %.0f = 左阻 %.0f + 中阻 %.0f + 右阻 %.0f + 受控源吸收 %.0f；残差 = %.2e"
      % (p[0], p[1], p[2], p[3], p[4], p[0] - p[1] - p[2] - p[3] - p[4]))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：含电流源变体 ===")
print("-- (a) 右支路 = 4 A 无伴电流源（向上）：回路电流被直接钉死 --")
I2a = -4.0                        # 顺时针回路电流 = 右支路向下为正；源向上 4A -> I2 = -4
I1a = (12.0 + 2.0 * I2a) / 4.0    # 4I1 - 2I2 = 12
V_a = 12.0 - 2.0 * I1a
print("  I2 = -4 A；4I1 - 2(-4) = 12 -> I1 = %.0f A" % I1a)
print("  核对：V = %.0f V；负载电流 = %.0f A；KCL：%.0f + 4 = %.0f"
      % (V_a, V_a / 2, I1a, I1a + 4))
print("  功率账（W）：源 12x1 = %.0f，电流源 4x10 = %.0f；消耗：负载 %.0f + 左阻 %.0f；残差 = %.2e"
      % (12 * I1a, 4 * V_a, V_a ** 2 / 2, 2 * I1a ** 2,
         (12 * I1a + 4 * V_a) - (V_a ** 2 / 2 + 2 * I1a ** 2)))

print("-- (b) 中支路 = 4 A 无伴电流源（向下）：超网孔 --")
# 外圈：2I1 + I2 = 12 - 10 = 2；约束：I1 - I2 = 4
A_s = np.array([[2.0, 1.0], [1.0, -1.0]])
I1b, I2b = np.linalg.solve(A_s, np.array([2.0, 4.0]))
V_b = 12.0 - 2.0 * I1b
print("  超网孔解得：I1 = %.0f A，I2 = %.0f A" % (I1b, I2b))
print("  核对：V = %.0f V；左路 %.0f A、右路 %.0f A（向上）、中支路 4 A 向下"
      % (V_b, (12 - V_b) / 2, (10 - V_b) / 1))
print("  功率账（W）：%.0f + %.0f = 左阻 %.0f + 右阻 %.0f + 电流源 %.0f；残差 = %.2e"
      % (12 * 2, 10 * 2, 2 * 2 ** 2, 1 * 2 ** 2, 4 * 8,
         (12 * 2 + 10 * 2) - (2 * 2 ** 2 + 1 * 2 ** 2 + 4 * 8)))

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：超网孔（中支路 = 无伴电流源） ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.SourceV().at((0, 0)).up().length(1.5)
    d += elm.Resistor().at((0, 1.5)).up().length(1.2)
    d += elm.Line().at((0, 2.7)).to((0, 3.5))
    d += elm.SourceI().at((3, 2.6)).down().length(1.4)
    d += elm.Line().at((3, 0)).to((3, 1.2))
    d += elm.Line().at((3, 2.6)).to((3, 3.5))
    d += elm.SourceV().at((6, 0)).up().length(1.5)
    d += elm.Resistor().at((6, 1.5)).up().length(1.2)
    d += elm.Line().at((6, 2.7)).to((6, 3.5))
    d += elm.Line().at((0, 3.5)).to((6, 3.5))
    d += elm.Line().at((0, 0)).to((6, 0))
    d += elm.Dot().at((3, 3.5))
    d += elm.Dot().at((3, 0))
    d += elm.Label().at((-1.05, 0.75)).label("12 V")
    d += elm.Label().at((-0.85, 2.1)).label("2 Ω")
    d += elm.Label().at((7.05, 0.75)).label("10 V")
    d += elm.Label().at((6.9, 2.1)).label("1 Ω")
    d += elm.Label().at((3.8, 1.9)).label("4 A")
    d += elm.Arrow().at((0.5, 0.55)).to((0.5, 2.95))
    d += elm.Arrow().at((0.5, 2.95)).to((5.5, 2.95))
    d += elm.Arrow().at((5.5, 2.95)).to((5.5, 0.55))
    d += elm.Arrow().at((5.5, 0.55)).to((0.5, 0.55))
    d += elm.Label().at((1.5, 1.75)).label("$I_1$")
    d += elm.Label().at((4.5, 1.75)).label("$I_2$")
    d += elm.Label().at((3, -0.75)).label("外圈合并成\u201c超级回路\u201d：绕大圈列 KVL（跳过电流源，不写它的压降）")
    d += elm.Label().at((3, -1.3)).label("约束方程：$I_1 - I_2 = 4$ A")
save_stem = "lec04_fig3_supermesh"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("=== 生成图 4：含受控源变体（右支路 = 1Ω + CCVS） ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.SourceV().at((0, 0)).up().length(1.5)
    d += elm.Resistor().at((0, 1.5)).up().length(1.2)
    d += elm.Line().at((0, 2.7)).to((0, 3.5))
    d += elm.Resistor().at((3, 1.2)).up().length(1.4)
    d += elm.Line().at((3, 0)).to((3, 1.2))
    d += elm.Line().at((3, 2.6)).to((3, 3.5))
    d += elm.SourceControlledV().at((6, 0)).up().length(1.5)
    d += elm.Resistor().at((6, 1.5)).up().length(1.2)
    d += elm.Line().at((6, 2.7)).to((6, 3.5))
    d += elm.Line().at((0, 3.5)).to((6, 3.5))
    d += elm.Line().at((0, 0)).to((6, 0))
    d += elm.Dot().at((3, 3.5))
    d += elm.Dot().at((3, 0))
    d += elm.Label().at((-1.05, 0.75)).label("12 V")
    d += elm.Label().at((-0.85, 2.1)).label("2 Ω")
    d += elm.Label().at((3.8, 1.9)).label("2 Ω")
    d += elm.Label().at((6.9, 2.1)).label("1 Ω")
    d += elm.Label().at((7.9, 0.95)).label("受控电压源 CCVS")
    d += elm.Label().at((7.9, 0.45)).label("$u' = 1\\,\\Omega \\cdot i_3$")
    d += elm.Arrow().at((3, 1.1)).to((3, 0.55))
    d += elm.Label().at((3.38, 0.8)).label("$i_3$")
    d += elm.Label().at((3, -0.75)).label("控制量 = 中支路电流：$i_3 = I_1 - I_2$")
save_stem = "lec04_fig4_controlled"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec04-02 完成。")