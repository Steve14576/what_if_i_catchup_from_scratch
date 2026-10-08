# =====================================================================
# lec11-01 第 11 讲《弯曲变形：挠度与转角》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 简支梁跨中集中力：w_max = P L^3/(48 E I)
#   EXP2 简支梁均布载荷：w_max = 5 q L^4/(384 E I)
#   EXP3 悬臂梁端部集中力：w_max = P L^3/(3 E I)
#   EXP4 叠加法：跨中集中力 + 均布，w_max 相加
#   EXP5 积分法互证：简支均布梁积分两次 + 边界条件，跨中挠度 = 5qL^4/384EI
# 出图（编号按正文出现顺序）：
#   lec11_fig1_deflect_slope    挠度与转角
#   lec11_fig2_integration      挠曲线近似微分方程与积分法
#   lec11_fig3_superposition    叠加法求挠度
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

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


def savefig(fig, stem):
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, stem + ".svg"))
    fig.savefig(os.path.join(FIGDIR, stem + ".png"), dpi=200)
    plt.close(fig)
    print("[OK] figures/%s.svg 与 .png 已生成。" % stem)


# ---------------------------------------------------------------------
print("=== 数字核对：第 11 讲 ===")

E = 2.0e5     # MPa
I = 5.0e6     # mm^4
L = 4000.0    # mm
P = 20.0e3    # N
q = 10.0      # N/mm

w1 = P * L ** 3 / (48.0 * E * I)
w2 = 5.0 * q * L ** 4 / (384.0 * E * I)
theta1 = P * L ** 2 / (16.0 * E * I)
print("  EXP1 简支梁跨中集中力 P=%.0f kN,L=%.0f mm：w_max = PL^3/(48EI) = %.2f mm" % (P / 1e3, L, w1))
print("        端部转角 theta = PL^2/(16EI) = %.4f rad = %.4f deg" % (theta1, np.rad2deg(theta1)))
print("  EXP2 简支梁均布 q=%.0f kN/m：w_max = 5qL^4/(384EI) = %.2f mm" % (q, w2))

Lc = 1000.0
w3 = P * Lc ** 3 / (3.0 * E * I)
print("  EXP3 悬臂梁（L=%.0f mm）端部 P：w_max = PL^3/(3EI) = %.2f mm" % (Lc, w3))

w_sum = w1 + w2
print("  EXP4 叠加（跨中集中力 + 均布，简支梁）：w_max = %.2f + %.2f = %.2f mm" % (w1, w2, w_sum))

# EXP5 积分法互证（简支均布）：w(x) = (q x /(24EI))(L^3 - 2 L x^2 + x^3)
xx = np.linspace(0, L, 101)
wx = (q * xx / (24.0 * E * I)) * (L ** 3 - 2 * L * xx ** 2 + xx ** 3)
w_mid = (q * (L / 2) / (24.0 * E * I)) * (L ** 3 - 2 * L * (L / 2) ** 2 + (L / 2) ** 3)
print("  EXP5 积分法互证：w(跨中) = %.4f mm（应为 5qL^4/384EI = %.4f）；w(L)=%.3e（边界应为 0）"
      % (w_mid, w2, wx[-1]))


# ---------------------------------------------------------------------
print()
print("=== 图 1：挠度与转角 ===")
fig, ax = plt.subplots(figsize=(9.6, 4.4))
ax.set_xlim(0, 12)
ax.set_ylim(-3.2, 2.6)
ax.axis("off")
# 支座
ax.add_patch(Polygon([[1, 1.2], [0.65, 0.6], [1.35, 0.6]], closed=True, fc=GREY))
ax.add_patch(Polygon([[11, 1.2], [10.65, 0.6], [11.35, 0.6]], closed=True, fc=GREY))
# 变形前（水平）
ax.plot([1, 11], [1.2, 1.2], color=GREY, ls=":", lw=1.2)
# 变形后（下凸）
xs = np.linspace(1, 11, 120)
ys = 1.2 - 1.4 * np.sin(np.pi * (xs - 1) / 10.0)
ax.plot(xs, ys, color=BLUE, lw=2.6)
# 挠度 w（跨中向下）
ax.annotate("", xy=(6.0, ys[np.argmin(np.abs(xs - 6.0))]), xytext=(6.0, 1.2),
            arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6))
ax.text(6.2, 0.1, r"$w$（挠度）", fontsize=11, color=RED)
# 转角 theta（端点切线与水平夹角）
ax.plot([1, 2.6], [1.2, 1.2 - 1.4 * np.sin(np.pi * 1.6 / 10.0)], color=GREEN, lw=1.4)
ax.text(2.7, 0.55, r"$\theta$（转角，$\theta=\dfrac{\mathrm{d}w}{\mathrm{d}x}$）", fontsize=10, color=GREEN)
ax.text(6.0, 2.2, "挠度 w：横截面形心的竖向位移（本课取 w 向上为正）", ha="center", fontsize=9.5)
ax.text(6.0, -2.9, r"约定：$x$ 向右为正、$w$ 向上为正；$\theta=\dfrac{\mathrm{d}w}{\mathrm{d}x}$（小变形）",
        ha="center", fontsize=9.5, color=BLUE)
savefig(fig, "lec11_fig1_deflect_slope")


# ---------------------------------------------------------------------
print()
print("=== 图 2：挠曲线近似微分方程与积分法 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.2))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

# (a) 方程建立
a1.plot([1, 9], [3.6, 3.6], color=GREY, ls=":", lw=1)
xs = np.linspace(1, 9, 100)
ys = 3.6 - 1.4 * np.sin(np.pi * (xs - 1) / 8.0)
a1.plot(xs, ys, color=BLUE, lw=2.4)
a1.text(5, 5.3, r"$EI_z\,w'' = M(x)$", ha="center", fontsize=15, color=RED)
a1.text(5, 4.5, "（挠曲线近似微分方程）", ha="center", fontsize=9.5, color=GREY)
a1.text(5, 0.8, "(a) 建立方程", ha="center", fontsize=11, weight="bold")

# (b) 积分两次 + 边界条件
a2.plot([1, 9], [3.6, 3.6], color=GREY, ls=":", lw=1)
a2.plot(xs, ys, color=BLUE, lw=2.4)
a2.plot([1], [3.6], "o", color=GREEN, ms=7)
a2.plot([9], [3.6], "o", color=GREEN, ms=7)
a2.text(1, 3.95, "w=0", ha="center", fontsize=9, color=GREEN)
a2.text(9, 3.95, "w=0", ha="center", fontsize=9, color=GREEN)
a2.text(5, 5.0, r"积分两次：$EI\,w'=\int M\mathrm{d}x+C_1$", ha="center", fontsize=9.5, color=BLUE)
a2.text(5, 4.4, r"$EI\,w=\iint M\mathrm{d}x^2+C_1 x+C_2$", ha="center", fontsize=9.5, color=BLUE)
a2.text(5, 0.8, "(b) 积分 + 边界条件定常数", ha="center", fontsize=11, weight="bold")
savefig(fig, "lec11_fig2_integration")


# ---------------------------------------------------------------------
print()
print("=== 图 3：叠加法求挠度 ===")
fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(11.6, 4.0))
for ax in (a1, a2, a3):
    ax.set_xlim(0, 10)
    ax.set_ylim(-2.2, 2.2)
    ax.axis("off")


def draw_beam(ax, load="P", defl=1.0):
    ax.plot([1, 9], [1.0, 1.0], color=GREY, ls=":", lw=1)
    xs = np.linspace(1, 9, 100)
    ys = 1.0 - defl * np.sin(np.pi * (xs - 1) / 8.0)
    ax.plot(xs, ys, color=BLUE, lw=2.2)
    ax.add_patch(Polygon([[1, 1.0], [0.75, 0.6], [1.25, 0.6]], closed=True, fc=GREY))
    ax.add_patch(Polygon([[9, 1.0], [8.75, 0.6], [9.25, 0.6]], closed=True, fc=GREY))
    if load == "P":
        ax.annotate("", xy=(5, 1.0), xytext=(5, 1.9), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
        ax.text(5.3, 1.85, r"$P$", fontsize=10, color=RED)
    else:
        for xx in np.linspace(1.4, 8.6, 7):
            ax.annotate("", xy=(xx, 1.0), xytext=(xx, 1.7), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.0))
        ax.plot([1.4, 8.6], [1.7, 1.7], color=ORANGE, lw=1.0)


draw_beam(a1, "P", 1.0)
a1.text(5, -1.9, r"(a) 集中力：$w_1=\dfrac{PL^3}{48EI}$", ha="center", fontsize=9.5)
draw_beam(a2, "q", 1.25)
a2.text(5, -1.9, r"(b) 均布：$w_2=\dfrac{5qL^4}{384EI}$", ha="center", fontsize=9.5)
draw_beam(a3, "P", 1.0)
xs = np.linspace(1, 9, 100)
ys2 = 1.0 - 1.25 * np.sin(np.pi * (xs - 1) / 8.0)
a3.plot(xs, ys2, color=ORANGE, lw=1.2, ls="--")
a3.annotate("", xy=(5, 1.0), xytext=(5, 1.9), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))
a3.text(5, -1.9, r"(c) 叠加：$w=w_1+w_2$", ha="center", fontsize=9.5)
savefig(fig, "lec11_fig3_superposition")

print()
print("[DONE] 第 11 讲数字核对与三张图全部完成。")
