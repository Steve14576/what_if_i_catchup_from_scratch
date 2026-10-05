# =====================================================================
# lec24-01 二端口网络 II：四套参数全算与换算、级联乘法、T/Π 等效、串联/并联规则
#          （第 24 讲 §1-§4 数值实验；图 1 级联、图 2 T/Π 等效、图 3 三种连接）
# 规模纪律：总耗时 < 15 秒（矩阵运算 + 结点法直解 + schemdraw 三图）。
#
# 主例沿用 23 讲 T 型网络 R1 = R2 = 10、R3 = 5：
#   Z = [[15,5],[5,15]] 欧；Y = Z^-1 = [[0.075,-0.025],[-0.025,0.075]] S
#   T（由 Z）：A = Z11/Z21 = 3、B = detZ/Z21 = 40 欧、C = 1/Z21 = 0.2 S、D = 3
#     互易 AD-BC = 1；对称 A = D
#   H（由 Z）：h11 = detZ/Z22 = 13.333 欧、h12 = Z12/Z22 = 1/3、
#     h21 = -Z21/Z22 = -1/3、h22 = 1/Z22 = 1/15 S；互易 h12 = -h21；对称 det H = 1
#   级联：T^2 = [[17,240],[1.2,17]]；接 20 欧负载：Zin = 580/41 = 14.1463
#     （与逐级递归、直接结点法互证）
#   等效回读：T 型 10/5/10；Π 型 20/40/20
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

def rect(d, x0, y0, w, h):
    d += elm.Line().at((x0, y0)).to((x0 + w, y0))
    d += elm.Line().at((x0 + w, y0)).to((x0 + w, y0 + h))
    d += elm.Line().at((x0 + w, y0 + h)).to((x0, y0 + h))
    d += elm.Line().at((x0, y0 + h)).to((x0, y0))

R1, R2, R3 = 10.0, 10.0, 5.0

# ---------------------------------------------------------------------
print("=== 实验 1：主例四套参数全算与互换核对 ===")
Z = np.array([[R1 + R3, R3], [R3, R2 + R3]], float)
Y = np.linalg.inv(Z)
A, B, C, D = Z[0, 0] / Z[1, 0], np.linalg.det(Z) / Z[1, 0], 1 / Z[1, 0], Z[1, 1] / Z[1, 0]
T = np.array([[A, B], [C, D]])
h11, h12, h21, h22 = np.linalg.det(Z) / Z[1, 1], Z[0, 1] / Z[1, 1], -Z[1, 0] / Z[1, 1], 1 / Z[1, 1]
print("  Z = [[%.0f,%.0f],[%.0f,%.0f]] 欧；Y = [[%.3f,%.3f],[%.3f,%.3f]] S"
      % (Z[0, 0], Z[0, 1], Z[1, 0], Z[1, 1], Y[0, 0], Y[0, 1], Y[1, 0], Y[1, 1]))
print("  T = [[%.1f,%.1f],[%.1f,%.1f]]（B=%.0f 欧、C=%.1f S）" % (A, B, C, D, B, C))
print("  H = [[%.3f,%.3f],[%.3f,%.3f]]（欧/无量纲/无量纲/S）" % (h11, h12, h21, h22))
print("  互易核对：AD-BC = %.1f（expect 1）；h12 = %.4f，-h21 = %.4f（相等）" % (A * D - B * C, h12, -h21))
print("  对称核对：A = D = %.1f；det H = %.1f（expect 1）" % (A, h11 * h22 - h12 * h21))

print()
print("=== 实验 2：级联的三路互证（两个主例级联，端 2 接 20 欧） ===")
T2 = T @ T
print("  T^2 = [[%.0f,%.0f],[%.1f,%.0f]]" % (T2[0, 0], T2[0, 1], T2[1, 0], T2[1, 1]))
RL = 20.0
Zin_T = (T2[0, 0] * RL + T2[0, 1]) / (T2[1, 0] * RL + T2[1, 1])
# 逐级递归：第二级输入阻抗（单级 + 20 欧）→ 再作为第一级负载
Zin_stage2 = 10 + (5 * (10 + RL)) / (5 + (10 + RL))
Zin_rec = 10 + (5 * (10 + Zin_stage2)) / (5 + (10 + Zin_stage2))
# 直接结点法：5 个内部节点（端口1, A1, 中继 M, A2, 端口2），端 2 接 20 欧，端 1 注 1 A
G = 1.0 / 20
n = 5
M = np.zeros((n, n))
b = np.zeros(n)
idx = {name: i for i, name in enumerate(["n1", "A1", "M", "A2", "n2"])}
def stamp(i, j, g):
    M[i, i] += g
    if j is not None:
        M[j, j] += g
        M[i, j] -= g
        M[j, i] -= g
stamp(idx["n1"], idx["A1"], 1 / R1)          # R1: n1 - A1
stamp(idx["A1"], None, 1 / R3)               # R3: A1 - 地
stamp(idx["A1"], idx["M"], 1 / R2)           # R2: A1 - M
stamp(idx["M"], idx["A2"], 1 / R1)           # 第二级 R1: M - A2
stamp(idx["A2"], None, 1 / R3)               # 第二级 R3: A2 - 地
stamp(idx["A2"], idx["n2"], 1 / R2)          # 第二级 R2: A2 - n2
stamp(idx["n2"], None, G)                    # 负载 20 欧: n2 - 地
b[idx["n1"]] = 1.0
U = np.linalg.solve(M, b)
Zin_direct = U[idx["n1"]]
print("  三路核对：T^2 公式 %.4f 欧；逐级递归 %.4f 欧；直接结点法 %.4f 欧"
      % (Zin_T, Zin_rec, Zin_direct))

print()
print("=== 实验 3：T 型/Π 型等效电路回读 ===")
print("  T 型回读：Z11-Z12 = %.0f、Z12 = %.0f、Z22-Z12 = %.0f（与原网络 R1/R3/R2 一致）"
      % (Z[0, 0] - Z[0, 1], Z[0, 1], Z[1, 1] - Z[0, 1]))
Yp11, Yp12 = Y[0, 0] + Y[0, 1], -Y[0, 1]
print("  Π 型回读：Y11+Y12 = %.3f S（%.0f 欧）、-Y12 = %.3f S（%.0f 欧）、Y22+Y12 = %.3f S"
      % (Yp11, 1 / Yp11, Yp12, 1 / Yp12, Y[1, 1] + Y[0, 1]))
# 用 Π 型元件反算 Y 参数验证
Rpa, Rpb, Rpc = 1 / Yp11, 1 / Yp12, 1 / (Y[1, 1] + Y[0, 1])
Y_check = np.array([[1 / Rpa + 1 / Rpb, -1 / Rpb], [-1 / Rpb, 1 / Rpb + 1 / Rpc]])
print("  Π 型反算 Y 偏差：%.1e" % np.max(np.abs(Y_check - Y)))

print()
print("=== 实验 4：连接方式——并联 Y 相加、串联 Z 相加 ===")
# 网络 B：T 型 R1=R2=10、R3=10 -> Z_B = [[20,10],[10,20]]
ZB = np.array([[20.0, 10.0], [10.0, 20.0]])
YB = np.linalg.inv(ZB)
print("  并联：Y_A + Y_B 与直接结点法核对")
Ypar = Y + YB
print("  Y 并联相加 = [[%.4f,%.4f],[%.4f,%.4f]] S" % (Ypar[0, 0], Ypar[0, 1], Ypar[1, 0], Ypar[1, 1]))
# 直接结点法验证并联：端口并接（共享节点 1、2），内部节点 A1、A2
n2 = 4
M2 = np.zeros((n2, n2))
b2 = np.zeros(n2)
idx2 = {name: i for i, name in enumerate(["p1", "p2", "A1", "A2"])}
def stamp2(i, j, g):
    M2[i, i] += g
    if j is not None:
        M2[j, j] += g
        M2[i, j] -= g
        M2[j, i] -= g
# 求 Y11 定义：U2 = 0（p2 接地为参考、去掉 p2 节点）-> 用 3 节点 (p1, A1, A2)
n3 = 3
M3 = np.zeros((n3, n3))
b3 = np.zeros(n3)
i1_, iA1, iA2 = 0, 1, 2
# 网络 A：p1-A1 (R1)、A1-地 (R3)、A1-p2(接地) (R2)
def st3(i, j, g):
    M3[i, i] += g
    if j is not None:
        M3[j, j] += g
        M3[i, j] -= g
        M3[j, i] -= g
st3(i1_, iA1, 1 / 10); st3(iA1, None, 1 / 5); st3(iA1, None, 1 / 10)
# 网络 B：p1-A2 (R1)、A2-地 (R3)、A2-p2(接地) (R2)
st3(i1_, iA2, 1 / 10); st3(iA2, None, 1 / 10); st3(iA2, None, 1 / 10)
b3[i1_] = 1.0
U3 = np.linalg.solve(M3, b3)
Y11_direct = 1.0 / U3[i1_]
print("  并联 Y11 核对：相加 %.4f S vs 直接解 %.4f S" % (Ypar[0, 0], Y11_direct))
# 串联特例：端口 1 串 R=5 的网络 -> Z = [[5,5],[5,5]] + Z
Zser = np.array([[5.0, 5.0], [5.0, 5.0]]) + Z
print("  串联特例（端口 1 串 5 欧元件）：Z 相加 = [[%.0f,%.0f],[%.0f,%.0f]]；直接解 Z11 = %.0f"
      % (Zser[0, 0], Zser[0, 1], Zser[1, 0], Zser[1, 1], 5 + Z[0, 0]))
print("  边界（认识层）：串联有效要求两网络的公共端不共地——否则连接无效、Z 不能相加")

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：级联与 T 矩阵相乘 ===")
with schemdraw.Drawing(show=False) as d:
    rect(d, 0, 0, 1.8, 1.4)
    d += elm.Label().at((0.9, 0.7)).label("$T_1$", fontsize=13)
    d += elm.Line().at((1.8, 1.1)).to((2.6, 1.1))
    d += elm.Line().at((1.8, 0.3)).to((2.6, 0.3))
    rect(d, 2.6, 0, 1.8, 1.4)
    d += elm.Label().at((3.5, 0.7)).label("$T_2$", fontsize=13)
    d += elm.Line().at((0, 1.1)).to((-0.8, 1.1))
    d += elm.Line().at((0, 0.3)).to((-0.8, 0.3))
    d += elm.Line().at((4.4, 1.1)).to((5.2, 1.1))
    d += elm.Line().at((4.4, 0.3)).to((5.2, 0.3))
    d += elm.Label().at((-1.15, 0.7)).label("端口 1", fontsize=10)
    d += elm.Label().at((5.55, 0.7)).label("端口 2", fontsize=10)
    d += elm.Label().at((2.2, 1.9)).label("首尾相接", fontsize=10)
    d += elm.Label().at((2.2, -0.5)).label("$T = T_1 \\cdot T_2$（矩阵相乘）", fontsize=11)

save_stem = "lec24_fig1_cascade"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：主例的 T 型与 Π 型等效电路 ===")
with schemdraw.Drawing(show=False) as d:
    # T 型等效（10 / 5 / 10）：上线串联两元件、中点经 5 到公共端
    d += elm.Label().at((1.2, 3.2)).label("T 型等效：10 / 5 / 10 欧", fontsize=11)
    d += elm.Line().at((-0.9, 2.4)).to((0, 2.4))
    d += elm.Resistor().at((0, 2.4)).to((1.2, 2.4)).label("10", fontsize=10)
    d += elm.Resistor().at((1.2, 2.4)).to((2.4, 2.4)).label("10", fontsize=10)
    d += elm.Line().at((2.4, 2.4)).to((3.3, 2.4))
    d += elm.Resistor().at((1.2, 2.4)).down().length(1.4)
    d += elm.Label().at((1.55, 1.75)).label("5", fontsize=10)
    d += elm.Line().at((-0.9, 1.0)).to((3.3, 1.0))
    # Π 型等效（20 / 40 / 20）：两竖支路 20 并接在两端口、顶部横支路 40
    d += elm.Label().at((6.6, 3.2)).label("Π 型等效：20 / 40 / 20 欧", fontsize=11)
    d += elm.Line().at((4.1, 2.4)).to((5.0, 2.4))
    d += elm.Resistor().at((5.0, 2.4)).to((6.2, 2.4)).label("40", fontsize=10)
    d += elm.Line().at((6.2, 2.4)).to((7.4, 2.4))
    d += elm.Line().at((7.4, 2.4)).to((8.3, 2.4))
    d += elm.Resistor().at((5.0, 2.4)).down().length(1.4)
    d += elm.Label().at((4.6, 1.75)).label("20", fontsize=10)
    d += elm.Resistor().at((7.4, 2.4)).down().length(1.4)
    d += elm.Label().at((7.8, 1.75)).label("20", fontsize=10)
    d += elm.Line().at((4.1, 1.0)).to((8.3, 1.0))

save_stem = "lec24_fig2_equiv"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：三种连接方式（串联 / 并联 / 级联） ===")
with schemdraw.Drawing(show=False) as d:
    def box(d, x0, y0, tag):
        rect(d, x0, y0, 1.2, 0.9)
        d += elm.Label().at((x0 + 0.6, y0 + 0.45)).label(tag, fontsize=10)
    d += elm.Label().at((0.9, 3.15)).label("串联：$Z = Z_1 + Z_2$", fontsize=11)
    box(d, 0.3, 1.5, "$N_1$")
    box(d, 0.3, 0.35, "$N_2$")
    d += elm.Label().at((2.3, 1.5)).label("电流同、电压加", fontsize=9)
    d += elm.Label().at((4.6, 3.15)).label("并联：$Y = Y_1 + Y_2$", fontsize=11)
    box(d, 4.0, 1.7, "$N_1$")
    box(d, 4.0, 0.6, "$N_2$")
    d += elm.Label().at((6.0, 1.5)).label("电压同、电流加", fontsize=9)
    d += elm.Label().at((8.3, 3.15)).label("级联：$T = T_1 T_2$", fontsize=11)
    box(d, 7.4, 1.6, "$N_1$")
    box(d, 9.0, 1.6, "$N_2$")
    d += elm.Label().at((10.5, 1.6)).label("首尾相接", fontsize=9)

save_stem = "lec24_fig3_connections"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec24-01 完成。")