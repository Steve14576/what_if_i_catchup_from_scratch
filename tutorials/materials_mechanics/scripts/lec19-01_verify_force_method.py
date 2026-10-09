# =====================================================================
# lec19-01 第 19 讲《超静定结构的力法与正则方程》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对（一次超静定梁：固支+简支，q=10 N/mm，L=4000 mm，EI=1e12）：
#   EXP1 柔度系数 delta_11=L^3/(3EI) 与自由项 Delta_1P=qL^4/(8EI)
#   EXP2 解 X1=Delta_1P/delta_11=3qL/8=15 kN（与第 12 讲变形比较法一致）
#   EXP3 残差检查 delta_11*X1-Delta_1P（应约为 0）
#   EXP4 对称性利用：两端固定梁受均布 -> M_固=-qL^2/12、M_跨中=qL^2/24
#   EXP5 柔度矩阵对称性 delta_12=delta_21 数值验证（两单位力偶于 L/3、2L/3）
# 出图（编号按正文出现顺序）：
#   lec19_fig1_primary_system  力法与基本体系
#   lec19_fig2_flexibility     柔度系数与自由项的物理意义
#   lec19_fig3_canonical_eq    正则方程与对称性的利用
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

RED = "#c0392b"
BLUE = "#2b6cb0"
GREEN = "#2f855a"
GREY = "#718096"
ORANGE = "#c05621"

q, L, EI = 10.0, 4000.0, 1.0e12


def savefig(fig, stem):
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, stem + ".svg"))
    fig.savefig(os.path.join(FIGDIR, stem + ".png"), dpi=200)
    plt.close(fig)
    print("[OK] figures/%s.svg 与 .png 已生成。" % stem)


# ---------------------------------------------------------------------
print("=== 数字核对：第 19 讲（一次超静定梁 q=%.0f N/mm, L=%.0f mm, EI=%.3e）===" % (q, L, EI))

d11 = L ** 3 / (3.0 * EI)
D1P = q * L ** 4 / (8.0 * EI)
print("  EXP1 柔度系数与自由项：delta_11=L^3/(3EI)=%.6f mm/N；Delta_1P=qL^4/(8EI)=%.2f mm" % (d11, D1P))

X1 = D1P / d11
print("  EXP2 解正则方程：X1=Delta_1P/delta_11=%.1f N=%.2f kN；3qL/8=%.2f kN（与第 12 讲一致）"
      % (X1, X1 / 1e3, 3 * q * L / 8 / 1e3))

res = d11 * X1 - D1P
print("  EXP3 残差检查：delta_11*X1-Delta_1P=%.3e mm（应约为 0）" % res)

M_fix = -q * L ** 2 / 12.0
M_mid = q * L ** 2 / 24.0
print("  EXP4 对称性（两端固定梁受均布）：M_固定=-qL^2/12=%.4f N·mm=%.2f kN·m；"
      "M_跨中=qL^2/24=%.4f N·mm=%.2f kN·m" % (M_fix, M_fix / 1e6, M_mid, M_mid / 1e6))
# 用弯矩方程核对跨中
xs = np.linspace(0, L, 101)
R = q * L / 2.0
Mx = M_fix + R * xs - q * xs ** 2 / 2.0
print("        核对：由弯矩方程算 M(L/2)=%.2f N·mm（应等于 M_跨中）" % np.interp(L / 2, xs, Mx))

# EXP5 柔度矩阵对称（两个单位力偶作用于 L/3 与 2L/3）
def M_unit_moment(x, xp):
    """单位力偶作用于 xp 时的弯矩图（简支梁，左端反力 = -1/L）。"""
    return np.where(x <= xp, -x / L, 1.0 - x / L)


d12 = np.trapezoid(M_unit_moment(xs, L / 3) * M_unit_moment(xs, 2 * L / 3) / EI, xs)
d21 = np.trapezoid(M_unit_moment(xs, 2 * L / 3) * M_unit_moment(xs, L / 3) / EI, xs)
print("  EXP5 柔度矩阵对称：delta_12=%.6e, delta_21=%.6e rad/(N·mm)（差 %.2e）"
      % (d12, d21, abs(d12 - d21)))


# ---------------------------------------------------------------------
print()
print("=== 图 1：力法与基本体系 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 4.4))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")


def fixed_end(ax, x, y0=2.2, y1=3.4):
    ax.plot([x, x], [y0, y1], color=GREY, lw=2)
    for yy in np.linspace(y0, y1, 5):
        ax.plot([x, x - 0.22], [yy, yy - 0.16], color=GREY, lw=1)


# (a) 原结构
a1.plot([2.0, 8.0], [3.4, 3.4], color=BLUE, lw=4)
fixed_end(a1, 2.0)
for xx in np.linspace(2.4, 7.6, 6):
    a1.annotate("", xy=(xx, 3.4), xytext=(xx, 4.2), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.1))
a1.plot([2.4, 7.6], [4.2, 4.2], color=ORANGE, lw=1.1)
a1.add_patch(Polygon([[8.0, 3.4], [7.72, 2.95], [8.28, 2.95]], closed=True, fc=ORANGE))
a1.text(5.0, 5.0, "(a) 原结构（1 次超静定）", ha="center", fontsize=10.5, weight="bold")
a1.text(5.0, 1.7, "多余约束：右支座", ha="center", fontsize=9.5, color=ORANGE)

# (b) 基本体系 + 多余未知力
a2.plot([2.0, 8.0], [3.4, 3.4], color=GREY, ls=":", lw=1.2)
ys = 3.4 - 0.9 * (1 - (1 - (np.linspace(2.0, 8.0, 60) - 2.0) / 6.0) ** 2)
a2.plot(np.linspace(2.0, 8.0, 60), ys, color=BLUE, lw=2.6)
fixed_end(a2, 2.0)
a2.annotate("", xy=(8.0, 3.4), xytext=(8.0, 4.4), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a2.text(8.2, 4.3, r"$X_1$", fontsize=13, color=RED)
for xx in np.linspace(2.4, 7.6, 6):
    a2.annotate("", xy=(xx, 3.4), xytext=(xx, 4.0), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=0.9))
a2.text(5.0, 5.0, "(b) 基本体系 + 多余未知力", ha="center", fontsize=10.5, weight="bold")
a2.text(5.0, 1.7, r"协调条件：$\Delta_1=0$", ha="center", fontsize=9.5, color=GREEN)
savefig(fig, "lec19_fig1_primary_system")


# ---------------------------------------------------------------------
print()
print("=== 图 2：柔度系数与自由项的物理意义 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 4.2))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

# (a) delta_11：单位力引起的同点位移
a1.plot([2.0, 8.0], [3.6, 3.6], color=GREY, ls=":", lw=1.2)
ys1 = 3.6 + 0.8 * (1 - (1 - (np.linspace(2.0, 8.0, 60) - 2.0) / 6.0) ** 2)
a1.plot(np.linspace(2.0, 8.0, 60), ys1, color=GREEN, lw=2.4)
a1.plot([2.0, 2.6], [2.6, 3.6], color=GREY, lw=1.6)
a1.annotate("", xy=(8.0, 3.6), xytext=(8.0, 4.6), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a1.text(8.2, 4.5, r"$X_1=1$", fontsize=12, color=RED)
a1.text(5.0, 5.2, r"$\delta_{11}$：单位多余力引起的同点位移", ha="center", fontsize=10, color=GREEN)
a1.text(5.0, 1.5, "(a) 柔度系数", ha="center", fontsize=10.5, weight="bold")

# (b) Delta_1P：实际载荷引起的位移
a2.plot([2.0, 8.0], [3.6, 3.6], color=GREY, ls=":", lw=1.2)
ys2 = 3.6 - 0.9 * (1 - (1 - (np.linspace(2.0, 8.0, 60) - 2.0) / 6.0) ** 2)
a2.plot(np.linspace(2.0, 8.0, 60), ys2, color=BLUE, lw=2.4)
a2.plot([2.0, 2.6], [2.6, 3.6], color=GREY, lw=1.6)
for xx in np.linspace(2.4, 7.6, 6):
    a2.annotate("", xy=(xx, 3.6), xytext=(xx, 4.3), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.0))
a2.plot([2.4, 7.6], [4.3, 4.3], color=ORANGE, lw=1.0)
a2.text(5.0, 5.2, r"$\Delta_{1P}$：实际载荷引起的位移", ha="center", fontsize=10, color=BLUE)
a2.text(5.0, 1.5, "(b) 自由项", ha="center", fontsize=10.5, weight="bold")
savefig(fig, "lec19_fig2_flexibility")


# ---------------------------------------------------------------------
print()
print("=== 图 3：正则方程与对称性的利用 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.4, 4.6))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

a1.text(5.0, 5.3, "n 次超静定的正则方程", ha="center", fontsize=11, weight="bold")
a1.text(1.0, 4.0, r"$\delta_{11}X_1+\delta_{12}X_2+\cdots+\Delta_{1P}=0$", fontsize=11, color=BLUE)
a1.text(1.0, 3.0, r"$\delta_{21}X_1+\delta_{22}X_2+\cdots+\Delta_{2P}=0$", fontsize=11, color=BLUE)
a1.text(3.4, 2.15, r"$\vdots$", fontsize=12, color=BLUE)
a1.text(2.0, 1.2, r"$\delta_{ij}=\delta_{ji}$（位移互等，第 18 讲）", fontsize=10, color=GREEN)
a1.text(5.0, 0.35, "(a) 正则方程", ha="center", fontsize=10.5, weight="bold")

# (b) 对称性：两端固定梁 -> 半结构
a2.plot([1.4, 8.6], [4.2, 4.2], color=BLUE, lw=4)
for x in (1.4, 8.6):
    a2.plot([x, x], [3.2, 4.2], color=GREY, lw=2)
    for yy in np.linspace(3.2, 4.2, 5):
        d = -0.22 if x < 5 else 0.22
        a2.plot([x, x + d], [yy, yy - 0.16], color=GREY, lw=1)
for xx in np.linspace(1.8, 8.2, 7):
    a2.annotate("", xy=(xx, 4.2), xytext=(xx, 4.9), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.0))
a2.plot([5.0, 5.0], [3.0, 4.2], color=RED, ls="--", lw=1.6)
a2.text(5.0, 2.6, "对称轴（跨中转角为零）", ha="center", fontsize=9.5, color=RED)
a2.text(5.0, 5.6, "(b) 对称性：取半结构（一端固定、一端滑动）", ha="center", fontsize=10, weight="bold")
a2.text(5.0, 1.7, "半结构为 1 次超静定 -> 解得固定端弯矩", ha="center", fontsize=9.5, color=GREEN)
savefig(fig, "lec19_fig3_canonical_eq")

print()
print("[DONE] 第 19 讲数字核对与三张图全部完成。")