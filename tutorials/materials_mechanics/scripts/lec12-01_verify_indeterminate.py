# =====================================================================
# lec12-01 第 12 讲《简单超静定问题》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP0 静定梁：平衡方程数 = 未知反力数
#   EXP1 拉压超静定（两端固定杆受轴力 P）：R1=Pb/L、R2=Pa/L；变形协调
#   EXP2 一次超静定梁（固支+简支梁 propped cantilever，均布 q）：R_B=3qL/8、M_固=-qL^2/8
#   EXP3 温度应力：两端固定，升温 dT -> sigma = -E*alpha*dT（受压）
#   EXP4 装配应力：杆略长 delta，强行装配 -> sigma = E*delta/L
# 出图（编号按正文出现顺序）：
#   lec12_fig1_static_indet      静定与超静定（多余约束）
#   lec12_fig2_deformation_compat 变形比较法（一次超静定梁）
#   lec12_fig3_temp_assembly     温度应力与装配应力
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
print("=== 数字核对：第 12 讲 ===")

# EXP1 拉压超静定：两端固定杆，轴力 P 作用在距左端 a 处
P, a, b = 30.0e3, 1.0, 2.0
L = a + b
R1 = P * b / L
R2 = P * a / L
print("  EXP1 拉压超静定（两端固定，P=%.0f kN @ a=%.0f m, b=%.0f m）：" % (P / 1e3, a, b))
print("        平衡：R1+R2 = %.1f kN（= P）；变形协调 -> R1=Pb/L=%.1f kN, R2=Pa/L=%.1f kN"
      % ((R1 + R2) / 1e3, R1 / 1e3, R2 / 1e3))

# EXP2 一次超静定梁（固支+简支梁，均布 q）
q, Lb = 10.0, 4000.0    # N/mm, mm
RB = 3.0 * q * Lb / 8.0
Mfix = -q * Lb ** 2 / 8.0
print("  EXP2 一次超静定梁（固支+简支，q=%.0f kN/m, L=%.0f mm）：" % (q, Lb))
print("        多余约束反力 R_B = 3qL/8 = %.1f kN；固定端弯矩 M = -qL^2/8 = %.1f kN·m"
      % (RB / 1e3, Mfix / 1e6))

# EXP3 温度应力
E, alpha, dT = 2.0e5, 12.0e-6, 30.0
sigma_T = -E * alpha * dT
print("  EXP3 温度应力（两端固定，E=%.0f MPa, alpha=%.1e /deg, dT=%.0f deg）：" % (E, alpha, dT))
print("        sigma = -E*alpha*dT = %.1f MPa（受压）" % sigma_T)

# EXP4 装配应力
delta, L4 = 0.2, 2000.0
sigma_a = E * delta / L4
print("  EXP4 装配应力（杆略长 delta=%.1f mm，L=%.0f mm）：" % (delta, L4))
print("        sigma = E*delta/L = %.1f MPa" % sigma_a)


# ---------------------------------------------------------------------
print()
print("=== 图 1：静定与超静定 ===")
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.4, 5.6))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

# (a) 静定简支梁
a1.plot([1, 9], [2.0, 2.0], color=BLUE, lw=4)
a1.add_patch(Polygon([[1, 2.0], [0.7, 1.5], [1.3, 1.5]], closed=True, fc=GREY))
a1.add_patch(Polygon([[9, 2.0], [8.7, 1.5], [9.3, 1.5]], closed=True, fc=GREY))
a1.text(5, 3.2, "静定梁：2 个竖向反力，2 个平衡方程 -> 可解", ha="center", fontsize=10, color=BLUE)
a1.text(5, 0.5, "(a) 静定", ha="center", fontsize=11, weight="bold")

# (b) 超静定：加中间支座
a2.plot([1, 9], [2.0, 2.0], color=BLUE, lw=4)
a2.add_patch(Polygon([[1, 2.0], [0.7, 1.5], [1.3, 1.5]], closed=True, fc=GREY))
a2.add_patch(Polygon([[5, 2.0], [4.7, 1.5], [5.3, 1.5]], closed=True, fc=ORANGE))
a2.add_patch(Polygon([[9, 2.0], [8.7, 1.5], [9.3, 1.5]], closed=True, fc=GREY))
a2.text(5, 3.2, "超静定梁：3 个竖向反力 > 2 个方程 -> 有 1 个多余约束", ha="center", fontsize=10, color=ORANGE)
a2.text(5, 0.5, "(b) 一次超静定", ha="center", fontsize=11, weight="bold")
savefig(fig, "lec12_fig1_static_indet")


# ---------------------------------------------------------------------
print()
print("=== 图 2：变形比较法（一次超静定梁）===")
fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(11.6, 4.0))
for ax in (a1, a2, a3):
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.6, 3.2)
    ax.axis("off")


def fixed_end(ax, x, y0=0.8, y1=2.0):
    ax.plot([x, x], [y0, y1], color=GREY, lw=2)
    for yy in np.linspace(y0, y1, 5):
        ax.plot([x, x - 0.25], [yy, yy - 0.18], color=GREY, lw=1)


# (a) 原超静定梁：左固定 + 右支 + 均布 q
a1.plot([1, 9], [2.0, 2.0], color=BLUE, lw=4)
fixed_end(a1, 1)
a1.add_patch(Polygon([[9, 2.0], [8.7, 1.5], [9.3, 1.5]], closed=True, fc=ORANGE))
for xx in np.linspace(1.4, 8.6, 7):
    a1.annotate("", xy=(xx, 2.0), xytext=(xx, 2.8), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.0))
a1.plot([1.4, 8.6], [2.8, 2.8], color=ORANGE, lw=1.0)
a1.text(5, 3.15, "(a) 原结构（1 次超静定）", ha="center", fontsize=10, weight="bold")
a1.text(5, -1.3, r"多余约束 = 右支座", ha="center", fontsize=9.5, color=ORANGE)

# (b) 静定基 + 均布 q -> 自由端下挠
a2.plot([1, 9], [2.0, 2.0], color=GREY, ls=":", lw=1)
xs = np.linspace(1, 9, 100)
ys = 2.0 - 0.9 * (1 - (1 - (xs - 1) / 8.0) ** 2)
a2.plot(xs, ys, color=BLUE, lw=2.2)
fixed_end(a2, 1)
for xx in np.linspace(1.4, 8.6, 7):
    a2.annotate("", xy=(xx, 2.0), xytext=(xx, 2.7), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=0.9))
a2.text(5, 3.15, "(b) 静定基 + 载荷", ha="center", fontsize=10, weight="bold")
a2.text(5, -1.3, r"自由端下挠 $w_B^q$", ha="center", fontsize=9.5, color=BLUE)

# (c) 静定基 + 多余未知力 R_B（向上）
a3.plot([1, 9], [2.0, 2.0], color=GREY, ls=":", lw=1)
ys3 = 2.0 + 0.6 * (1 - (1 - (xs - 1) / 8.0) ** 2)
a3.plot(xs, ys3, color=GREEN, lw=2.2)
fixed_end(a3, 1)
a3.annotate("", xy=(9, 2.0), xytext=(9, 3.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a3.text(9.2, 2.9, r"$R_B$", fontsize=11, color=RED)
a3.text(5, 3.15, "(c) 静定基 + 多余未知力", ha="center", fontsize=10, weight="bold")
a3.text(5, -1.3, r"上挠 $w_B^R$；协调：$w_B^q = w_B^R$", ha="center", fontsize=9.5, color=GREEN)
savefig(fig, "lec12_fig2_deformation_compat")


# ---------------------------------------------------------------------
print()
print("=== 图 3：温度应力与装配应力 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.2))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

# (a) 温度应力：两端固定杆，升温
a1.add_patch(plt.Rectangle((2, 2.6), 6, 0.8, fc="#fde9d9", ec=ORANGE))
a1.plot([2, 2], [2.4, 3.6], color=GREY, lw=2)
for yy in np.linspace(2.4, 3.6, 5):
    a1.plot([2, 1.75], [yy, yy - 0.18], color=GREY, lw=1)
a1.plot([8, 8], [2.4, 3.6], color=GREY, lw=2)
for yy in np.linspace(2.4, 3.6, 5):
    a1.plot([8, 8.25], [yy, yy - 0.18], color=GREY, lw=1)
a1.annotate("", xy=(2.5, 4.3), xytext=(7.5, 4.3), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6))
a1.text(5, 4.5, "升温 dT", ha="center", fontsize=10, color=RED)
a1.text(5, 1.6, r"两端固定，热膨胀被阻止 -> 压应力 $\sigma=-E\alpha\Delta T$", ha="center", fontsize=9.5)
a1.text(5, 5.2, "(a) 温度应力", ha="center", fontsize=11, weight="bold")

# (b) 装配应力：杆略长，强行装配
a2.add_patch(plt.Rectangle((1.6, 2.6), 6.6, 0.8, fc="#e7f0fb", ec=BLUE))
a2.plot([1.6, 1.6], [2.4, 3.6], color=GREY, lw=2)
a2.plot([8.2, 8.2], [2.4, 3.6], color=GREY, lw=2)
a2.plot([1.6, 8.2], [4.6, 4.6], color=GREY, ls=":", lw=1.2)
a2.text(5, 4.75, "设计长度（略短）", ha="center", fontsize=9, color=GREY)
a2.annotate("", xy=(8.2, 3.0), xytext=(7.45, 3.0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6))
a2.text(7.0, 2.3, r"$\delta$", fontsize=11, color=GREEN)
a2.text(5, 1.6, r"杆略长 $\delta$，强行装配 -> 压应力 $\sigma=E\delta/L$", ha="center", fontsize=9.5)
a2.text(5, 5.2, "(b) 装配应力", ha="center", fontsize=11, weight="bold")
savefig(fig, "lec12_fig3_temp_assembly")

print()
print("[DONE] 第 12 讲数字核对与三张图全部完成。")
