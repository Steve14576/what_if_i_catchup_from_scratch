# =====================================================================
# lec01-01 第 01 讲《绪论与基本概念》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张小图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 截面法平衡复核（取一段：内力与外力合力为零）
#   EXP2 平均正应力 sigma = N / A（同一轴力、不同截面 -> 应力不同）
#   EXP3 单位换算核对（1 MPa = 1 N/mm^2 = 1e6 Pa）
#   EXP4 平均线应变 eps = dL / L（无量纲）
# 出图（编号按正文出现顺序）：
#   lec01_fig1_section_method     截面法四步（截、取、代、平）
#   lec01_fig2_stress             正应力与切应力
#   lec01_fig3_four_deformations  杆件的四种基本变形
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / -> / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, Polygon

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../materials_mechanics
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

RED = "#c0392b"
BLUE = "#2b6cb0"
GREEN = "#2f855a"
ORANGE = "#c05621"
GREY = "#718096"


def savefig(fig, stem):
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, stem + ".svg"))
    fig.savefig(os.path.join(FIGDIR, stem + ".png"), dpi=200)
    plt.close(fig)
    print("[OK] figures/%s.svg 与 .png 已生成。" % stem)


# ---------------------------------------------------------------------
print("=== 数字核对：第 01 讲的核心量 ===")

# EXP1 截面法平衡复核：一根受轴向外力 F 的杆，取任意截面的左侧段
F = 20.0e3          # 外力 N
N = F               # 截面内力（拉为正）
res = N - F         # 取左段：外力 F 向右、内力 N 向左，平衡应有 N = F
print("  EXP1 截面法：取左段列平衡，N - F = %.3e（应为 0；即 N = F）" % res)

# EXP2 平均正应力 sigma = N / A
print("  EXP2 平均正应力 sigma = N / A（同一轴力 20 kN、不同截面）：")
for A in [100.0, 200.0, 400.0]:
    print("        A = %6.1f mm^2  ->  sigma = %6.1f N/mm^2 = %6.1f MPa"
          % (A, N / A, N / A))

# EXP3 单位换算核对
A0 = 200.0
sigma0 = N / A0
print("  EXP3 单位核对：1 MPa = 1 N/mm^2 = 1e6 Pa")
print("        sigma = %.1f MPa = %.1f N/mm^2 = %.3e Pa"
      % (sigma0, sigma0, sigma0 * 1e6))

# EXP4 平均线应变 eps = dL / L
L0 = 500.0
dL = 0.25
eps = dL / L0
print("  EXP4 平均线应变：eps = dL/L = %.2f mm / %.0f mm = %.3e（无量纲）"
      % (dL, L0, eps))
print("        对照：钢材弹性范围的应变常在 1e-3 以下，本例 %.1e 量级一致。" % eps)


# ---------------------------------------------------------------------
print()
print("=== 图 3：杆件的四种基本变形 ===")
fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.6))
for ax in axes.ravel():
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

# (a) 轴向拉压
ax = axes[0, 0]
ax.add_patch(Rectangle((2.5, 4.6), 5, 0.8, fc="#cfe3f7", ec=BLUE))
ax.annotate("", xy=(1.2, 5.0), xytext=(2.5, 5.0),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.annotate("", xy=(8.8, 5.0), xytext=(7.5, 5.0),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(5, 7.4, "(a) 轴向拉压", ha="center", fontsize=12, weight="bold")
ax.text(5, 2.4, "两端沿轴线受拉（或压）：\n杆沿轴线伸长（或缩短）",
        ha="center", fontsize=9.5)

# (b) 剪切
ax = axes[0, 1]
ax.add_patch(Rectangle((3.6, 3.6), 2.8, 2.8, fc="#fde9d9", ec=ORANGE))
ax.annotate("", xy=(8.2, 6.4), xytext=(6.4, 6.4),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.annotate("", xy=(1.8, 3.6), xytext=(3.6, 3.6),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(5, 7.4, "(b) 剪切", ha="center", fontsize=12, weight="bold")
ax.text(5, 2.2, "一对相距很近、方向相反的外力：\n相邻截面相互错动",
        ha="center", fontsize=9.5)

# (c) 扭转
ax = axes[1, 0]
ax.add_patch(Rectangle((4.5, 1.8), 1.0, 6.4, fc="#d7f0d7", ec=GREEN))
ax.add_patch(Arc((5, 8.2), 2.6, 1.1, theta1=15, theta2=200, color=RED, lw=2))
ax.annotate("", xy=(3.95, 8.55), xytext=(4.1, 8.5),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.add_patch(Arc((5, 1.8), 2.6, 1.1, theta1=195, theta2=380, color=RED, lw=2))
ax.annotate("", xy=(6.05, 1.45), xytext=(5.9, 1.5),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(7.6, 8.2, "T", fontsize=13, color=RED)
ax.text(7.6, 1.8, "T", fontsize=13, color=RED)
ax.text(5, 9.5, "(c) 扭转", ha="center", fontsize=12, weight="bold")
ax.text(5, 0.4, "两端受绕轴线的力偶：\n横截面绕轴相对转动",
        ha="center", fontsize=9.5)

# (d) 弯曲
ax = axes[1, 1]
ax.plot([1.6, 8.4], [6, 6], color=BLUE, lw=3)
ax.add_patch(Polygon([[2.2, 6], [1.75, 5.2], [2.65, 5.2]], closed=True, fc=GREY))
ax.add_patch(Polygon([[7.8, 6], [7.35, 5.2], [8.25, 5.2]], closed=True, fc=GREY))
ax.annotate("", xy=(5, 6), xytext=(5, 8.2),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(5.35, 8.15, "F", fontsize=13, color=RED)
xs = np.linspace(2.2, 7.8, 100)
ys = 6 - 0.95 * np.sin(np.pi * (xs - 2.2) / 5.6)
ax.plot(xs, ys, "--", color=RED, lw=1.6)
ax.text(5, 9.5, "(d) 弯曲", ha="center", fontsize=12, weight="bold")
ax.text(5, 0.4, "两端支承、横向受力：\n杆的轴线弯成曲线",
        ha="center", fontsize=9.5)

savefig(fig, "lec01_fig3_four_deformations")


# ---------------------------------------------------------------------
print()
print("=== 图 1：截面法四步 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.2, 3.8))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.4, 4.2)
    ax.axis("off")

# (a) 整体与所求截面
a1.add_patch(Rectangle((1.2, 1.8), 7.6, 0.8, fc="#cfe3f7", ec=BLUE))
# 左端固定支座（斜线阴影）
a1.plot([1.2, 1.2], [1.5, 2.9], color=GREY, lw=2)
for yy in np.arange(1.5, 3.0, 0.28):
    a1.plot([1.2, 1.2 - 0.25], [yy, yy - 0.2], color=GREY, lw=1)
# 右端外力 F
a1.annotate("", xy=(9.9, 2.2), xytext=(8.8, 2.2),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a1.text(9.0, 2.55, "F", fontsize=13, color=RED)
# 所求截面（截）
a1.plot([5.0, 5.0], [1.5, 2.9], color=RED, ls="--", lw=2)
a1.text(5.0, 3.35, "所求截面", ha="center", fontsize=10, color=RED)
a1.text(5.0, 0.7, "(a) 整根杆 + 想求内力的位置", ha="center", fontsize=10.5,
        weight="bold")

# (b) 取右段：截、取、代、平
a2.add_patch(Rectangle((5.0, 1.8), 3.8, 0.8, fc="#cfe3f7", ec=BLUE))
# 右端外力 F
a2.annotate("", xy=(9.9, 2.2), xytext=(8.8, 2.2),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a2.text(9.0, 2.55, "F", fontsize=13, color=RED)
# 截面上内力 N（从被截掉的左段传来）
a2.annotate("", xy=(4.1, 2.2), xytext=(5.0, 2.2),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2))
a2.text(4.35, 2.55, "N", fontsize=13, color=GREEN)
a2.plot([5.0, 5.0], [1.5, 2.9], color=RED, ls="--", lw=2)
a2.text(5.0, 3.35, "截面", ha="center", fontsize=10, color=RED)
a2.text(5.0, 0.7, "(b) 取右段：截 -> 取 -> 代 -> 平", ha="center", fontsize=10.5,
        weight="bold")
a2.text(7.0, 0.15, "由水平平衡 N = F 解出内力", ha="center", fontsize=9.5)

savefig(fig, "lec01_fig1_section_method")


# ---------------------------------------------------------------------
print()
print("=== 图 2：正应力与切应力 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

# 共同的截面：侧视成一条竖直的线
# (a) 正应力：垂直于截面（沿法线方向，水平指向截面外）
a1.plot([5.0, 5.0], [1.2, 5.0], color=BLUE, lw=2.6)
a1.text(5.0, 5.35, "截面", ha="center", fontsize=10, color=BLUE)
for yy in [1.9, 2.9, 3.9]:
    a1.annotate("", xy=(6.6, yy), xytext=(5.0, yy),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
a1.text(6.85, 2.9, r"$\sigma$", fontsize=12, color=RED, va="center")
a1.text(5.0, 0.35, r"(a) 正应力 $\sigma$：垂直于截面（沿法线）" + "\n" + r"$\sigma$ = 法向内力 / 面积",
        ha="center", fontsize=9.5)

# (b) 切应力：平行于截面（沿截面切向，竖直）
a2.plot([5.0, 5.0], [1.2, 5.0], color=BLUE, lw=2.6)
a2.text(5.0, 5.35, "截面", ha="center", fontsize=10, color=BLUE)
for y0 in [1.7, 3.1]:
    a2.annotate("", xy=(5.0, y0 + 1.05), xytext=(5.0, y0),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
a2.text(5.5, 2.9, r"$\tau$", fontsize=12, color=GREEN, va="center")
a2.text(5.0, 0.35, r"(b) 切应力 $\tau$：平行于截面（沿切向）" + "\n" + r"$\tau$ = 切向内力 / 面积",
        ha="center", fontsize=9.5)

savefig(fig, "lec01_fig2_stress")

print()
print("[DONE] 第 01 讲数字核对与三张图全部完成。")
