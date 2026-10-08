# =====================================================================
# lec13-01 第 13 讲《应力状态分析》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对（取 sigma_x=100, sigma_y=50, tau_xy=40 MPa）：
#   EXP1 解析法：任意斜截面 sigma_a、tau_a
#   EXP2 主应力 sigma_1,2 = C ± R（C=(sx+sy)/2, R=sqrt(A^2+B^2)）
#   EXP3 最大切应力 tau_max = R = (sigma_1-sigma_2)/2
#   EXP4 应力圆：圆心 (C,0)、半径 R；圆上点与斜截面一一对应（转角 2a）
# 出图（编号按正文出现顺序）：
#   lec13_fig1_element        一点应力状态的单元体
#   lec13_fig2_inclined       斜截面上的应力（解析法）
#   lec13_fig3_mohr_circle     应力圆（莫尔圆）
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc

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


def sa(sx, sy, txy, a):
    """斜截面正应力（a 为弧度）。"""
    return (sx + sy) / 2.0 + (sx - sy) / 2.0 * np.cos(2 * a) - txy * np.sin(2 * a)


def ta(sx, sy, txy, a):
    """斜截面切应力。"""
    return (sx - sy) / 2.0 * np.sin(2 * a) + txy * np.cos(2 * a)


# ---------------------------------------------------------------------
print("=== 数字核对：第 13 讲（sigma_x=100, sigma_y=50, tau_xy=40 MPa）===")
sx, sy, txy = 100.0, 50.0, 40.0
C = (sx + sy) / 2.0
A = (sx - sy) / 2.0
B = txy
R = np.sqrt(A ** 2 + B ** 2)
s1 = C + R
s2 = C - R
print("  EXP2 主应力：C=(sx+sy)/2=%.1f；R=sqrt(A^2+B^2)=%.2f -> sigma_1=%.2f, sigma_2=%.2f MPa"
      % (C, R, s1, s2))
print("  EXP3 最大切应力：tau_max = R = %.2f MPa（=(sigma_1-sigma_2)/2 = %.2f）" % (R, (s1 - s2) / 2.0))
alpha_p = np.rad2deg(0.5 * np.arctan2(-2.0 * txy, (sx - sy)))
print("        主方向：alpha_p = %.1f deg（该面上 tau=0）" % alpha_p)
print("  EXP1 解析法（各角度斜截面，单位：deg / MPa）：")
print("        alpha=  0 : sigma_a=%6.2f , tau_a=%6.2f" % (sa(sx, sy, txy, 0), ta(sx, sy, txy, 0)))
for d in [30, 45, 60, 90]:
    a = np.deg2rad(d)
    print("        alpha=%3d : sigma_a=%6.2f , tau_a=%6.2f" % (d, sa(sx, sy, txy, a), ta(sx, sy, txy, a)))
# 极值核对
al = np.linspace(-np.pi, np.pi, 720)
print("  EXP4 圆不变式核对：max|(sigma_a-C)^2+tau_a^2 - R^2| = %.2e（应为 0）"
      % np.max(np.abs((sa(sx, sy, txy, al) - C) ** 2 + ta(sx, sy, txy, al) ** 2 - R ** 2)))


# ---------------------------------------------------------------------
print()
print("=== 图 1：一点应力状态的单元体 ===")
fig, ax = plt.subplots(figsize=(6.6, 6.0))
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)
ax.set_aspect("equal")
ax.axis("off")
ax.add_patch(Rectangle((-1, -1), 2, 2, fc="#e7f0fb", ec=BLUE, lw=1.6))
# sigma_x（右面带正）
ax.annotate("", xy=(2.0, 0.5), xytext=(1.0, 0.5), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(2.1, 0.5, r"$\sigma_x$", fontsize=12, color=RED, va="center")
# sigma_y（上面带正）
ax.annotate("", xy=(0.5, 2.0), xytext=(0.5, 1.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(0.55, 2.1, r"$\sigma_y$", fontsize=12, color=RED)
# tau_xy（右面向上）
ax.annotate("", xy=(1.0, 0.7), xytext=(1.0, -0.7), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
ax.text(1.25, 0.0, r"$\tau_{xy}$", fontsize=11, color=GREEN)
# tau_yx（上面向右）
ax.annotate("", xy=(0.7, 1.0), xytext=(-0.7, 1.0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
ax.text(0.0, 1.2, r"$\tau_{yx}$", fontsize=11, color=GREEN)
ax.text(0, -2.1, r"一点应力状态：单元体上的 $\sigma_x,\sigma_y,\tau_{xy}$；$\tau_{xy}=\tau_{yx}$（切应力互等）",
        ha="center", fontsize=9.5)
ax.text(0, 2.4, "微元（单元体）：表示一点的应力状态", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec13_fig1_element")


# ---------------------------------------------------------------------
print()
print("=== 图 2：斜截面上的应力（解析法）===")
fig, ax = plt.subplots(figsize=(7.6, 5.4))
ax.set_xlim(-2.6, 2.8)
ax.set_ylim(-2.4, 2.8)
ax.set_aspect("equal")
ax.axis("off")
ax.add_patch(Rectangle((-1, -1), 2, 2, fc="#eef2f7", ec=GREY))
# 斜截面（与 x 轴成 alpha）
ax.plot([-1, 1], [1, -1], color=RED, lw=2.2)
ax.text(1.05, -1.05, r"$\alpha$", fontsize=12, color=RED)
# 斜截面上的 sigma_a, tau_a（示意方向）
ax.annotate("", xy=(0.85, -0.15), xytext=(0.0, 0.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
ax.text(0.9, -0.35, r"$\sigma_\alpha$", fontsize=11, color=RED)
ax.annotate("", xy=(-0.7, 0.25), xytext=(0.0, 0.0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
ax.text(-0.95, 0.15, r"$\tau_\alpha$", fontsize=11, color=GREEN)
ax.text(0, 2.5, "斜截面（法线与 x 成 alpha）上的应力", ha="center", fontsize=10, weight="bold")
ax.text(0, -2.15, r"$\sigma_\alpha=C+A\cos2\alpha-B\sin2\alpha$，$\tau_\alpha=A\sin2\alpha+B\cos2\alpha$",
        ha="center", fontsize=9.5, color=BLUE)
ax.text(0, -1.95, "（C=(sx+sy)/2、A=(sx-sy)/2、B=tau_xy）", ha="center", fontsize=8.5, color=GREY)
savefig(fig, "lec13_fig2_inclined")


# ---------------------------------------------------------------------
print()
print("=== 图 3：应力圆（莫尔圆）===")
fig, ax = plt.subplots(figsize=(8.6, 6.0))
ax.set_xlim(-10, 140)
ax.set_ylim(-62, 62)
ax.set_aspect("equal")
ax.axis("off")
# 坐标轴
ax.annotate("", xy=(138, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.2))
ax.annotate("", xy=(75, 58), xytext=(75, -58), arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.2))
ax.text(138, -8, r"$\sigma$", fontsize=11, color=GREY)
ax.text(78, 56, r"$\tau$", fontsize=11, color=GREY)
# 圆
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(C + R * np.cos(th), R * np.sin(th), color=BLUE, lw=2)
ax.plot([C], [0], "o", color=GREY, ms=5)
ax.text(C, -9, "圆心 C", ha="center", fontsize=9, color=GREY)
# 主应力点
ax.plot([s1], [0], "o", color=RED, ms=6)
ax.plot([s2], [0], "o", color=RED, ms=6)
ax.text(s1, 6, r"$\sigma_1$", ha="center", fontsize=11, color=RED)
ax.text(s2, 6, r"$\sigma_2$", ha="center", fontsize=11, color=RED)
# 最大切应力点
ax.plot([C], [R], "o", color=GREEN, ms=6)
ax.text(C + 3, R + 2, r"$\tau_{\max}=R$", fontsize=10, color=GREEN)
# sigma_x 点（2alpha=0）
ax.plot([sx], [txy], "o", color=ORANGE, ms=6)
ax.text(sx + 2, txy + 3, r"$(\sigma_x,\tau_{xy})$", fontsize=9.5, color=ORANGE)
ax.plot([C, sx], [0, txy], color=ORANGE, ls="--", lw=1.2)
# 一条一般半径（2alpha=60deg）
a2 = np.deg2rad(60)
px = C + R * np.cos(a2)
py = R * np.sin(a2)
ax.plot([C, px], [0, py], color=GREEN, ls=":", lw=1.4)
ax.plot([px], [py], "o", color=GREEN, ms=5)
ax.add_patch(Arc((C, 0), 40, 40, theta1=0, theta2=60, color=GREEN, lw=1.2))
ax.text(C + 22, 8, r"$2\alpha$", fontsize=10, color=GREEN)
ax.text(70, -55, "圆上每点对应一个斜截面；斜截面转 alpha，圆上转 2*alpha", ha="center", fontsize=9.5)
ax.text(70, 66, "应力圆：圆心 (C, 0)、半径 R", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec13_fig3_mohr_circle")

print()
print("[DONE] 第 13 讲数字核对与三张图全部完成。")
