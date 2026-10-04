# =====================================================================
# lec18-01 耦合电感与变压器：互感相量电路、去耦等效对照、理想变压器逼近
#          （第 18 讲 §1-§4 数值实验；图 1 耦合线圈、图 2 同名端判断、图 3 T 型去耦）
# 规模纪律：总耗时 < 10 秒（复数线性求解 + 解析计算 + 三张图）。
#
# 运行例：Us = 90 角 0 度；Z1 = 6+j4（R1=6、wL1=4）；jwM = j5；Z2 = 3+j4（R2=3、wL2=4）。
#   方程（两电流都从同名端流入为正方向）：
#     Z1*I1 + jwM*I2 = Us；jwM*I1 + Z2*I2 = 0
#   -> I1 = 10 角 0 度；I2 = 10 角 -143.13 度（= -8-j6）；引入阻抗 Z_ref = (wM)^2/Z2 = 3-j4；
#      Z_in = Z1 + Z_ref = 9 -> I1 = 90/9 = 10 角 0 度。
# 去耦数字：L1 = 8、L2 = 5、M = 2（k = 2/sqrt(40) = 0.3162）。
#   顺串 8+5+4 = 17 H；反串 13-4 = 9 H；T 型（同名端共端）6/3/2；异侧 10/7/-2。
# 理想变压器逼近：k=1、n=10、Z_L = 8 -> Z_in = n^2 Z_L/(1+Z_L/(jwL2))；
#   wL2 = 9/90/900 -> Z_in 的模 597.7 -> 803.2 -> 800.03，角 41.6 -> 5.08 -> 0.51 度 -> 极限 800。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import schemdraw
import schemdraw.elements as elm

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

elm.style(elm.STYLE_IEC)
schemdraw.config(font="Microsoft YaHei", fontsize=13)

def ph(z):
    return "%.4g 角 %.4g 度" % (abs(z), np.degrees(np.angle(z)))

# ---------------------------------------------------------------------
print("=== 实验 1：互感相量电路运行例 ===")
Z1 = complex(6, 4)
Z2 = complex(3, 4)
ZwM = complex(0, 5)
Us = 90.0
A = np.array([[Z1, ZwM], [ZwM, Z2]], dtype=complex)
b = np.array([Us, 0.0], dtype=complex)
sol = np.linalg.solve(A, b)
I1, I2 = sol[0], sol[1]
print("  I1 = %s；I2 = %s" % (ph(I1), ph(I2)))
r1 = Z1 * I1 + ZwM * I2 - Us
r2 = ZwM * I1 + Z2 * I2
print("  KVL 残差：|r1| = %.2e，|r2| = %.2e（expect ~0）" % (abs(r1), abs(r2)))
Zref = (abs(ZwM) ** 2) / Z2
print("  引入阻抗 Z_ref = (wM)^2/Z2 = %s；Z_in = Z1+Z_ref = %s" % (ph(Zref), ph(Z1 + Zref)))
print("  核对：Us/Z_in = %s（expect 10 角 0 度）" % ph(Us / (Z1 + Zref)))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：串联去耦——顺串与反串 ===")
L1, L2, M = 8.0, 5.0, 2.0
k = M / np.sqrt(L1 * L2)
Lfwd, Lrev = L1 + L2 + 2 * M, L1 + L2 - 2 * M
print("  k = M/sqrt(L1 L2) = %.4f" % k)
print("  顺串 L_eq = %.0f H；反串 L_eq = %.0f H" % (Lfwd, Lrev))
# 正弦电流驱动下的端电压对照（w = 1，I = 1 角 0 度）：
w, I = 1.0, 1.0
u_coupled = 1j * w * (L1 + L2 + 2 * M) * I   # 两线圈耦合模型：u = jwL1 I + jwM I + jwM I + jwL2 I
u_equiv = 1j * w * Lfwd * I
print("  耦合模型端电压 = %s；等效电感模型 = %s；差 = %.2e"
      % (ph(u_coupled), ph(u_equiv), abs(u_coupled - u_equiv)))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：T 型去耦端口等效对照（同名端共端） ===")
# T 型网络：LA = L1-M 接端 1-内节点 A；LB = L2-M 接端 2-A；LC = M 接 A-端 3。
# 端口电流 I1、I2 注入；节点 A 电位 UA = jw LC (I1+I2)。
LA, LB, LC = L1 - M, L2 - M, M
I1p, I2p = 2.0 + 1j, 1.0 - 3j
UA = 1j * w * LC * (I1p + I2p)
U1_t = 1j * w * LA * I1p + UA
U2_t = 1j * w * LB * I2p + UA
U1_o = 1j * w * (L1 * I1p + M * I2p)   # 原始互感网络的端口电压
U2_o = 1j * w * (M * I1p + L2 * I2p)
print("  T 型支路：LA = %.0f H、LB = %.0f H、LC = %.0f H" % (LA, LB, LC))
print("  U1：T 型 %s vs 原始 %s，差 %.2e" % (ph(U1_t), ph(U1_o), abs(U1_t - U1_o)))
print("  U2：T 型 %s vs 原始 %s，差 %.2e" % (ph(U2_t), ph(U2_o), abs(U2_t - U2_o)))
print("  异侧接法（共端为异名端）：支路 10/7/-2 H（负电感只是等效参数）")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：理想变压器的极限逼近（k=1、n=10、Z_L=8） ===")
n = 10.0
ZL = 8.0
print("  理想极限：Z_in = n^2 Z_L = %.0f" % (n ** 2 * ZL))
for wL2 in [9.0, 90.0, 900.0]:
    Zin = (n ** 2 * ZL) / (1 + ZL / (1j * wL2))
    print("  wL2 = %.6g：Z_in = %.1f 角 %.2f 度（模 -> 800、角 -> 0）"
          % (wL2, abs(Zin), np.degrees(np.angle(Zin))))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：耦合线圈与同名端 ===")
with schemdraw.Drawing(show=False) as d:
    # 矩形铁心
    d += elm.Line().at((0, 0)).to((3, 0))
    d += elm.Line().at((3, 0)).to((3, 2))
    d += elm.Line().at((3, 2)).to((0, 2))
    d += elm.Line().at((0, 2)).to((0, 0))
    # 左臂线圈 1（竖放）与右臂线圈 2
    d += elm.Inductor().at((0, 1.4)).down().length(0.8)
    d += elm.Inductor().at((3, 1.4)).down().length(0.8)
    # 同名端：两线圈的"上端"各引出一小段，端头为同名端（实心点）
    d += elm.Line().at((0, 1.4)).to((-0.65, 1.4))
    d += elm.Line().at((3, 1.4)).to((3.65, 1.4))
    d += elm.Dot().at((-0.65, 1.4))
    d += elm.Dot().at((3.65, 1.4))
    d += elm.Label().at((-0.65, 1.72)).label("同名端", fontsize=10)
    d += elm.Label().at((3.65, 1.72)).label("同名端", fontsize=10)
    # 电流箭头
    d += elm.Arrow().at((-1.45, 1.4)).to((-0.85, 1.4))
    d += elm.Label().at((-1.6, 1.65)).label("$i_1$")
    d += elm.Arrow().at((3.85, 1.4)).to((4.45, 1.4))
    d += elm.Label().at((4.5, 1.65)).label("$i_2$")
    # 线圈标号与主磁通
    d += elm.Label().at((-0.55, 0.95)).label("$N_1$", fontsize=11)
    d += elm.Label().at((3.55, 0.95)).label("$N_2$", fontsize=11)
    d += elm.Arrow().at((1.1, 2.0)).to((1.9, 2.0))
    d += elm.Label().at((1.5, 2.3)).label("$\\Phi$", fontsize=12)
    d += elm.Label().at((1.5, 1.0)).label("铁心", fontsize=11)

save_stem = "lec18_fig1_coupled"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：绕向与同名端（两格对比） ===")
def draw_magnetic_core(d, x0, wind1, wind2, tag):
    """口字型铁心（中心线画法）+ 两臂绕线斜线 + 端点。wind: 'down' 或 'up'。"""
    w0, h0 = 2.4, 1.9
    # 铁心矩形环
    d += elm.Line().at((x0, 0)).to((x0 + w0, 0))
    d += elm.Line().at((x0 + w0, 0)).to((x0 + w0, h0))
    d += elm.Line().at((x0 + w0, h0)).to((x0, h0))
    d += elm.Line().at((x0, h0)).to((x0, 0))
    # 左臂绕线（3 条斜线）与右臂绕线
    for j, yb in enumerate([0.42, 0.87, 1.32]):
        if wind1 == "down":
            d += elm.Line().at((x0 - 0.22, yb + 0.26)).to((x0 + 0.22, yb))
        else:
            d += elm.Line().at((x0 - 0.22, yb)).to((x0 + 0.22, yb + 0.26))
    for j, yb in enumerate([0.42, 0.87, 1.32]):
        if wind2 == "down":
            d += elm.Line().at((x0 + w0 - 0.22, yb + 0.26)).to((x0 + w0 + 0.22, yb))
        else:
            d += elm.Line().at((x0 + w0 - 0.22, yb)).to((x0 + w0 + 0.22, yb + 0.26))
    d += elm.Label().at((x0 - 0.55, 1.05)).label("$N_1$", fontsize=10)
    d += elm.Label().at((x0 + w0 + 0.55, 1.05)).label("$N_2$", fontsize=10)
    d += elm.Label().at((x0 + w0 / 2, 2.25)).label(tag, fontsize=10)

with schemdraw.Drawing(show=False) as d:
    draw_magnetic_core(d, 0.0, "down", "down", "绕向相同")
    draw_magnetic_core(d, 4.6, "down", "up", "绕向相反")
    # 相同绕向：两线圈顶端为同名端
    d += elm.Dot().at((0 - 0.22, 1.58 + 0.26))
    d += elm.Dot().at((2.4 + 0.22, 1.58 + 0.26))
    d += elm.Label().at((1.2, -0.42)).label("顶端两端子为同名端", fontsize=10)
    # 相反绕向：左上端与右下端为同名端
    d += elm.Dot().at((4.6 - 0.22, 1.58 + 0.26))
    d += elm.Dot().at((7.0 + 0.22, 0.42))
    d += elm.Label().at((5.8, -0.42)).label("左上端与右下端为同名端", fontsize=10)

save_stem = "lec18_fig2_dots"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：T 型去耦等效 ===")
with schemdraw.Drawing(show=False) as d:
    # 原始网络：两线圈，同名端（下端）相连为端 3
    d += elm.Inductor().at((0.4, 1.6)).down().length(0.8)
    d += elm.Inductor().at((1.9, 1.6)).down().length(0.8)
    d += elm.Line().at((0.4, 1.6)).to((0.4, 2.2))
    d += elm.Line().at((1.9, 1.6)).to((1.9, 2.2))
    d += elm.Label().at((0.4, 2.42)).label("1", fontsize=11)
    d += elm.Label().at((1.9, 2.42)).label("2", fontsize=11)
    d += elm.Line().at((0.4, 0.8)).to((0.4, 0.4))
    d += elm.Line().at((1.9, 0.8)).to((1.9, 0.4))
    d += elm.Line().at((0.4, 0.4)).to((1.9, 0.4))
    d += elm.Line().at((1.15, 0.4)).to((1.15, -0.1))
    d += elm.Label().at((1.15, -0.35)).label("3", fontsize=11)
    d += elm.Dot().at((0.4, 0.8))
    d += elm.Dot().at((1.9, 0.8))
    d += elm.Label().at((-0.15, 1.15)).label("$L_1$", fontsize=11)
    d += elm.Label().at((2.45, 1.15)).label("$L_2$", fontsize=11)
    d += elm.Arrow().at((2.85, 1.05)).to((3.75, 1.05))
    d += elm.Label().at((3.3, 1.35)).label("去耦等效", fontsize=10)
    # T 型网络：端 1、端 2 分别经 LA、LB 汇到内节点 A；A 经 LC 到端 3
    d += elm.Line().at((4.3, 2.0)).to((4.3, 1.6))
    d += elm.Line().at((4.3, 1.6)).to((5.0, 1.6))
    d += elm.Label().at((4.15, 2.2)).label("1", fontsize=11)
    d += elm.Inductor().at((5.0, 1.6)).down().length(0.7)
    d += elm.Label().at((4.35, 1.28)).label("$L_1-M$", fontsize=10)
    d += elm.Line().at((5.0, 0.9)).to((5.0, 0.15))
    d += elm.Line().at((7.2, 2.0)).to((7.2, 1.6))
    d += elm.Line().at((7.2, 1.6)).to((6.4, 1.6))
    d += elm.Label().at((7.35, 2.2)).label("2", fontsize=11)
    d += elm.Inductor().at((6.4, 1.6)).down().length(0.7)
    d += elm.Label().at((6.95, 1.35)).label("$L_2-M$", fontsize=10)
    d += elm.Line().at((6.4, 0.9)).to((6.4, 0.15))
    d += elm.Line().at((5.0, 0.15)).to((6.4, 0.15))
    d += elm.Dot().at((5.7, 0.15))
    d += elm.Label().at((5.45, 0.45)).label("A", fontsize=10)
    d += elm.Inductor().at((5.7, 0.15)).down().length(0.7)
    d += elm.Label().at((6.1, -0.32)).label("$M$", fontsize=10)
    d += elm.Line().at((5.7, -0.55)).to((5.7, -0.75))
    d += elm.Label().at((5.7, -1.0)).label("3", fontsize=11)

save_stem = "lec18_fig3_tdecouple"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec18-01 完成。")