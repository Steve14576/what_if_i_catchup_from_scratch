# =====================================================================
# lec23-01 二端口网络 I：Y/Z 参数定义法互证、Y·Z=I、互易/对称、非互易与存在性
#          （第 23 讲 §1-§4 数值实验；图 1 二端口一般画面、图 2 两种测量法、图 3 非互易示意）
# 规模纪律：总耗时 < 10 秒（矩阵运算 + schemdraw 三图）。
#
# 主例：T 型电阻网络 R1 = 10、R2 = 10、R3 = 5（对称）：
#   Z = [[15,5],[5,15]] 欧（开路口径：Z11=R1+R3、Z12=R3、Z22=R2+R3）
#   Y = Z^{-1} = [[75,-25],[-25,75]] mS（短路口径：Y11=1/(R1+R2||R3)=1/13.333）
#   核对：Y·Z = I；Y12 = -0.025（互导纳为负——与 05 讲结点法"互导纳负"呼应）
# 非对称：R1=10、R2=20、R3=5 -> Y11=0.07143、Y22=0.04286、Y12=Y21=-0.01429（仍互易）
# 非互易：T 型 + VCCS（g_m = 0.05 S）-> Y21 - Y12 = g_m = 0.05
# 存在性：串联型 Z=[[5,5],[5,5]]（det=0）-> Y 不存在；并联型 Y 奇异 -> Z 不存在
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
schemdraw.config(font="Microsoft YaHei", fontsize=12)

# ---------------------------------------------------------------------
print("=== 实验 1：主例 T 型网络的 Z 与 Y（定义法互证） ===")
R1, R2, R3 = 10.0, 10.0, 5.0
Z = np.array([[R1 + R3, R3], [R3, R2 + R3]], float)
Y = np.linalg.inv(Z)
print("  Z = [[%.0f, %.0f], [%.0f, %.0f]] 欧" % (Z[0, 0], Z[0, 1], Z[1, 0], Z[1, 1]))
print("  Y = Z^-1 = [[%.4f, %.4f], [%.4f, %.4f]] S"
      % (Y[0, 0], Y[0, 1], Y[1, 0], Y[1, 1]))
# 短路法独立核对 Y11、Y12
Rpar = R2 * R3 / (R2 + R3)
Y11_chk = 1 / (R1 + Rpar)
Rpar13 = R1 * R3 / (R1 + R3)
Y12_chk = -(Rpar13 / (R2 + Rpar13)) / R1
print("  短路法核对：Y11 = 1/(R1+R2||R3) = %.5f；Y12 = %.5f（U1=0 时 VA=%0.4f）"
      % (Y11_chk, Y12_chk, Rpar13 / (R2 + Rpar13)))
print("  Y*Z = I 核对：最大偏差 %.2e" % np.max(np.abs(Y @ Z - np.eye(2))))

print()
print("=== 实验 2：非对称 T 型（R1=10、R2=20、R3=5）仍互易 ===")
R1b, R2b = 10.0, 20.0
Zb = np.array([[R1b + R3, R3], [R3, R2b + R3]], float)
Yb = np.linalg.inv(Zb)
print("  Z = [[%.0f, %.0f], [%.0f, %.0f]]；Y = [[%.5f, %.5f], [%.5f, %.5f]]"
      % (Zb[0, 0], Zb[0, 1], Zb[1, 0], Zb[1, 1], Yb[0, 0], Yb[0, 1], Yb[1, 0], Yb[1, 1]))
print("  不对称（Y11 %.5f != Y22 %.5f）；互易（Y12 %.5f == Y21 %.5f）"
      % (Yb[0, 0], Yb[1, 1], Yb[0, 1], Yb[1, 0]))

print()
print("=== 实验 3：含 VCCS 的非互易网络 ===")
gm = 0.05
Ync = Y.copy()
Ync[1, 0] += gm          # 端 1 电压控制流入端 2 的电流源
print("  Y21 - Y12 = %.4f（= g_m = %.2f，非互易）" % (Ync[1, 0] - Ync[0, 1], gm))
print("  对照：无受控源时 Y21 - Y12 = %.1e（互易）" % (Y[1, 0] - Y[0, 1]))

print()
print("=== 实验 4：Z/Y 的存在性（退化） ===")
Zser = np.array([[5.0, 5.0], [5.0, 5.0]])
Ypar = np.array([[0.2, -0.2], [-0.2, 0.2]])
print("  串联型：Z = [[5,5],[5,5]]，det = %.1f -> Z 奇异，Y 不存在（数值求逆失败）" % np.linalg.det(Zser))
try:
    np.linalg.inv(Zser)
    ok = True
except np.linalg.LinAlgError:
    ok = False
print("    np.linalg.inv(Zser) %s" % ("成功（意外）" if ok else "抛出 LinAlgError（符合预期）"))
print("  并联型：Y = [[0.2,-0.2],[-0.2,0.2]]，det = %.1e -> Y 奇异，Z 不存在" % np.linalg.det(Ypar))
print("  （工程选择：串联结构用 Z、并联结构用 Y）")

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：二端口网络一般画面 ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.Line().at((0, 0)).to((3, 0))
    d += elm.Line().at((0, 0)).to((0, 1.8))
    d += elm.Line().at((3, 0)).to((3, 1.8))
    d += elm.Line().at((0, 1.8)).to((3, 1.8))
    d += elm.Label().at((1.5, 0.9)).label("线性网络 $N$", fontsize=11)
    # 端口 1（左侧）
    d += elm.Line().at((0, 1.8)).to((-1.0, 1.8))
    d += elm.Line().at((0, 0.0)).to((-1.0, 0.0))
    d += elm.Label().at((-0.5, 2.1)).label("端口 1", fontsize=10)
    d += elm.Arrow().at((-2.0, 1.8)).to((-1.1, 1.8))
    d += elm.Label().at((-2.2, 2.1)).label("$I_1$", fontsize=11)
    d += elm.Label().at((-1.4, 1.35)).label("$+$", fontsize=11)
    d += elm.Label().at((-1.4, 0.45)).label("$-$", fontsize=11)
    d += elm.Label().at((-2.1, 1.05)).label("$U_1$", fontsize=11)
    # 端口 2（右侧）
    d += elm.Line().at((3, 1.8)).to((4.0, 1.8))
    d += elm.Line().at((3, 0.0)).to((4.0, 0.0))
    d += elm.Label().at((3.4, 2.1)).label("端口 2", fontsize=10)
    d += elm.Arrow().at((5.0, 1.8)).to((4.1, 1.8))
    d += elm.Label().at((5.2, 2.1)).label("$I_2$", fontsize=11)
    d += elm.Label().at((3.55, 1.35)).label("$+$", fontsize=11)
    d += elm.Label().at((3.55, 0.45)).label("$-$", fontsize=11)
    d += elm.Label().at((4.35, 1.05)).label("$U_2$", fontsize=11)

save_stem = "lec23_fig1_port"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：主例 T 型网络与两种测量口径 ===")
def tnet(d, x0):
    """T 型：端 1 上线 -> R1 -> A -> R2 -> 端 2；A 经 R3 到公共下线（端口不短路）"""
    d += elm.Line().at((x0 - 0.9, 2.4)).to((x0, 2.4))
    d += elm.Resistor().at((x0, 2.4)).to((x0 + 1.4, 2.4)).label("$R_1$", fontsize=10)
    d += elm.Resistor().at((x0 + 1.4, 2.4)).to((x0 + 2.8, 2.4)).label("$R_2$", fontsize=10)
    d += elm.Line().at((x0 + 2.8, 2.4)).to((x0 + 3.7, 2.4))
    d += elm.Resistor().at((x0 + 1.4, 2.4)).down().length(1.4).label("$R_3$", loc="right", fontsize=10)
    d += elm.Line().at((x0 - 0.9, 1.0)).to((x0 + 3.7, 1.0))
    # 端口 1 标注
    d += elm.Label().at((x0 - 0.55, 2.15)).label("$+$", fontsize=10)
    d += elm.Label().at((x0 - 0.55, 1.25)).label("$-$", fontsize=10)
    d += elm.Label().at((x0 - 1.5, 1.7)).label("$U_1$", fontsize=10)
    d += elm.Arrow().at((x0 - 2.3, 2.4)).to((x0 - 1.05, 2.4))
    d += elm.Label().at((x0 - 2.5, 2.7)).label("$I_1$", fontsize=10)

with schemdraw.Drawing(show=False) as d:
    tnet(d, 0.0)
    d += elm.Label().at((1.3, 3.3)).label("Y 参数：端 2 短路（$U_2 = 0$）", fontsize=11)
    # 端 2 短接
    d += elm.Line().at((2.8, 2.4)).to((3.7, 2.4))
    d += elm.Line().at((3.7, 2.4)).to((3.7, 1.0))
    d += elm.Label().at((4.15, 1.7)).label("短接", fontsize=10)
    tnet(d, 6.6)
    d += elm.Label().at((7.9, 3.3)).label("Z 参数：端 2 开路（$I_2 = 0$）", fontsize=11)
    d += elm.Label().at((10.6, 2.7)).label("开路", fontsize=10)

save_stem = "lec23_fig2_tnetwork"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：含受控源的非互易网络示意 ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.Line().at((0, 0)).to((4, 0))
    d += elm.Line().at((0, 0)).to((0, 2.2))
    d += elm.Line().at((4, 0)).to((4, 2.2))
    d += elm.Line().at((0, 2.2)).to((4, 2.2))
    d += elm.Label().at((2, 1.8)).label("网络 $N$", fontsize=11)
    # 内部受控源符号（菱形）
    d += elm.SourceControlledI().at((1.4, 0.9)).to((2.6, 0.9))
    d += elm.Label().at((2.0, 0.5)).label("$g_m U_1$", fontsize=10)
    # 端口 1
    d += elm.Line().at((0, 2.2)).to((-0.8, 2.2))
    d += elm.Line().at((0, 0)).to((-0.8, 0))
    d += elm.Line().at((-0.8, 2.2)).to((-0.8, 0))
    d += elm.Arrow().at((-1.6, 2.2)).to((-0.9, 2.2))
    d += elm.Label().at((-1.75, 2.5)).label("$I_1$", fontsize=10)
    d += elm.Label().at((-1.15, 1.55)).label("$U_1$", fontsize=10)
    # 端口 2
    d += elm.Line().at((4, 2.2)).to((4.8, 2.2))
    d += elm.Line().at((4, 0)).to((4.8, 0))
    d += elm.Line().at((4.8, 2.2)).to((4.8, 0))
    d += elm.Arrow().at((5.6, 2.2)).to((4.9, 2.2))
    d += elm.Label().at((5.75, 2.5)).label("$I_2$", fontsize=10)
    d += elm.Label().at((4.4, 1.55)).label("$U_2$", fontsize=10)

save_stem = "lec23_fig3_nonreciprocal"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec23-01 完成。")