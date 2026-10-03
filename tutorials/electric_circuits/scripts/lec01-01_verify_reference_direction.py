# =====================================================================
# lec01-01 参考方向、参考极性与电位参考点（第 01 讲 §2 / §3）
# 规模纪律：总耗时 < 5 秒（纯算术 + 一张小图）。
# 方法：
#   实验 1：同一物理事实（真实电流 0.3 A 从 a 流向 b）在不同参考约定
#           下的记录值与读法对照表。
#   实验 2：电位参考点平移演示——换参考点后电位整体平移、电压不变。
#   并生成 figures/lec01_fig1_loop.svg 与 .png（引子回路的电路图，
#   带电流参考方向箭头与电压参考极性标注）。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
# =====================================================================
import os

import matplotlib
matplotlib.use("Agg")

import schemdraw
import schemdraw.elements as elm

plt_fonts = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.sans-serif"] = plt_fonts
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../electric_circuits
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# ---------------------------------------------------------------------
print("=== 实验 1：电流参考方向的记账对照表 ===")
print("  物理事实：某支路真实电流 0.3 A，从 a 流向 b（与参考设定无关）")
print("  参考方向设定         | 记录的电流值 | 读法")
print("  a -> b（与真实一致） |   +0.3 A     | 真实电流从 a 流向 b")
print("  b -> a（与真实相反） |   -0.3 A     | 负号 = 与假设相反，即真实方向仍是 a 流向 b")
i_case1, i_case2 = 0.3, -0.3
print("  核对：两种约定记录值之和 = %.1f（互为相反数；物理量本身只有一个）" % (i_case1 + i_case2))
print("  -> 结论：记录值 = 参考设定 + 符号；负号不是错误，是'与假设相反'的编码。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：换参考点——电位平移，电压不变 ===")
Va, Vb, Vc = 10.0, 6.0, 0.0  # 以 c 为参考点
Uab0, Ubc0 = Va - Vb, Vb - Vc
print("  以 c 为参考点：V_a = %.0f V, V_b = %.0f V, V_c = %.0f V" % (Va, Vb, Vc))
print("    U_ab = V_a - V_b = %.0f V;  U_bc = V_b - V_c = %.0f V" % (Uab0, Ubc0))
shift = Vb  # 参考点移到 b：全体电位减去 Vb
Va2, Vb2, Vc2 = Va - shift, Vb - shift, Vc - shift
Uab1, Ubc1 = Va2 - Vb2, Vb2 - Vc2
print("  以 b 为参考点：V_a = %.0f V, V_b = %.0f V, V_c = %.0f V" % (Va2, Vb2, Vc2))
print("    U_ab = %.0f V;  U_bc = %.0f V" % (Uab1, Ubc1))
print("  对照：U_ab 不变（%.0f vs %.0f）；U_bc 不变（%.0f vs %.0f）" % (Uab0, Uab1, Ubc0, Ubc1))
print("  -> 结论：换参考点 = 全体电位平移同一个常数；两点间电压（差值）不变。")

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：引子回路电路图（含参考方向标注） ===")
elm.style(elm.STYLE_IEC)
schemdraw.config(font="Microsoft YaHei", fontsize=14)

with schemdraw.Drawing(show=False) as d:
    d += elm.BatteryCell().up().label("1.5 V", loc="left")
    d += elm.Line().right().length(6)
    d += elm.Lamp2().down().label("0.3 A", loc="right")
    d += elm.Line().left().length(6)
    # 电压参考极性标注（+、-）
    d += elm.Label().at((0.45, 2.7)).label("+")
    d += elm.Label().at((0.45, 0.3)).label("-")
    # 电流参考方向箭头（顶部向右、底部向左，构成绕行方向）
    d += elm.Arrow().at((2.4, 3)).to((3.6, 3))
    d += elm.Arrow().at((3.6, 0)).to((2.4, 0))

d.save(os.path.join(FIGDIR, "lec01_fig1_loop.svg"), transparent=False)
d.save(os.path.join(FIGDIR, "lec01_fig1_loop.png"), transparent=False, dpi=200)
print("[OK] figures/lec01_fig1_loop.svg 与 .png 已生成。")