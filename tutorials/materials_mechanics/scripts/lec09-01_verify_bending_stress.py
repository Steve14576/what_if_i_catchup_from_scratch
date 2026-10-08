# =====================================================================
# lec09-01 第 09 讲《平面弯曲的正应力》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 矩形截面：W_z=I/(h/2)，sigma_max=M/W_z
#   EXP2 圆截面：W_z=pi d^3/32，sigma_max=M/W_z；并与 sigma=My/I 互证
#   EXP3 不对称 T 形：上下缘应力（W 分别算），危险点在下缘
#   EXP4 线性分布：sigma(y)=My/I 沿高度线性，中性轴处为零
#   EXP5 强度条件设计：W >= M/[sigma]（矩形 定比例求尺寸）
# 出图（编号按正文出现顺序）：
#   lec09_fig1_pure_bending     纯弯曲与梁的变形（中性层）
#   lec09_fig2_three_steps      三步推导（几何-物理-静力）
#   lec09_fig3_stress_dist      横截面正应力线性分布
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

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
print("=== 数字核对：第 09 讲 ===")

# EXP1 矩形 60x100
b, h = 60.0, 100.0
I = b * h ** 3 / 12.0
W = I / (h / 2.0)
M = 10.0e6          # N·mm = 10 kN·m
sig_max = M / W
print("  EXP1 矩形 b=%.0f, h=%.0f：I=%.4e mm^4；W=I/(h/2)=%.4e mm^3" % (b, h, I, W))
print("        M=%.0f kN·m -> sigma_max = M/W = %.1f MPa" % (M / 1e6, sig_max))

# EXP2 圆 d=50
d = 50.0
I_c = np.pi * d ** 4 / 64.0
W_c = np.pi * d ** 3 / 32.0
M2 = 2.0e6
print("  EXP2 圆 d=%.0f：I=%.4e；W=pi d^3/32=%.4e" % (d, I_c, W_c))
print("        M=%.0f kN·m -> sigma_max = M/W = %.1f MPa" % (M2 / 1e6, M2 / W_c))

# EXP3 T 形（与 07 讲同一截面）120x20 翼缘 + 20x80 腹板
bf, tf, bw, hw = 120.0, 20.0, 20.0, 80.0
A1, y1 = bw * hw, hw / 2.0
A2, y2 = bf * tf, hw + tf / 2.0
A_tot = A1 + A2
y_c = (A1 * y1 + A2 * y2) / A_tot
It = bw * hw ** 3 / 12.0 + A1 * (y1 - y_c) ** 2 + bf * tf ** 3 / 12.0 + A2 * (y2 - y_c) ** 2
H = hw + tf
W_bot = It / y_c
W_top = It / (H - y_c)
M3 = 10.0e6
print("  EXP3 不对称 T 形（y_c=%.0f, I=%.4e）：" % (y_c, It))
print("        W_下=I/y_c=%.4e -> sigma_下 = M/W_下 = %.1f MPa（受拉，危险）" % (W_bot, M3 / W_bot))
print("        W_上=I/(H-y_c)=%.4e -> sigma_上 = M/W_上 = %.1f MPa（受压）" % (W_top, M3 / W_top))

# EXP4 线性分布核对（矩形，M=10 kN·m）
print("  EXP4 线性分布 sigma(y)=My/I（矩形，M=%.0f kN·m）：" % (M / 1e6))
for yv in [50.0, 25.0, 0.0, -25.0, -50.0]:
    print("        y=%+5.1f mm -> sigma = %.1f MPa" % (yv, M * yv / I))

# EXP5 强度条件设计（矩形 h=2b，[sigma]=160）
sg = 160.0
Wreq = 12.0e6 / sg
bb = (3 * Wreq / 2.0) ** (1.0 / 3.0)
print("  EXP5 强度设计：M=12 kN·m, [sigma]=%.0f MPa -> W>=M/[sigma]=%.4e mm^3" % (sg, Wreq))
print("        矩形 h=2b：W=2b^3/3 >= %.0f -> b >= %.1f mm, 取 h=2b=%.1f mm" % (Wreq, bb, 2 * bb))


# ---------------------------------------------------------------------
print()
print("=== 图 1：纯弯曲与梁的变形 ===")
fig, ax = plt.subplots(figsize=(9.6, 4.4))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5)
ax.axis("off")
# 支撑与载荷（四点弯曲：中间段为纯弯曲）
for x in [1.0, 10.0]:
    ax.add_patch(Polygon([[x, 1.6], [x - 0.35, 1.0], [x + 0.35, 1.0]], closed=True, fc=GREY))
ax.plot([0.4, 11.6], [1.6, 1.6], color=BLUE, lw=4)
for x in [2.6, 8.4]:
    ax.annotate("", xy=(x, 1.6), xytext=(x, 2.9), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
    ax.text(x, 3.05, r"$P$", ha="center", fontsize=11, color=RED)
# 纯弯曲区间框
ax.plot([2.6, 8.4], [1.25, 1.25], color=ORANGE, lw=1.4)
ax.text(5.5, 0.85, "纯弯曲段（中间段 Q=0、M=常数）", ha="center", fontsize=9.5, color=ORANGE)
# 变形后的梁（虚线，下凸）
xs = np.linspace(0.4, 11.6, 120)
ys = 1.6 - 0.5 * (1 - ((xs - 6.0) / 6.0) ** 2)
ax.plot(xs, ys, color=GREEN, ls="--", lw=1.6)
# 中性层（变形前后中性轴近似）
ax.plot([2.6, 8.4], [1.6, 1.6], color=RED, ls=":", lw=1.2)
ax.text(5.5, 2.6, "上缘受压（缩短）", ha="center", fontsize=9.5, color="#2b6cb0")
ax.text(5.5, 0.3, "下缘受拉（伸长）；中性层长度不变", ha="center", fontsize=9.5, color=GREEN)
ax.text(5.5, 4.6, "四点弯曲：中段为纯弯曲（只有 M、没有 Q）", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec09_fig1_pure_bending")


# ---------------------------------------------------------------------
print()
print("=== 图 2：三步推导（几何-物理-静力）===")
fig, axes = plt.subplots(1, 3, figsize=(11.5, 4.0))
for ax in axes:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

# (a) 几何：弯曲后平面假设，ε=y/rho
ax = axes[0]
th = np.linspace(-0.7, 0.7, 60)
cx, cy, R = 5.0, 8.2, 5.0
ax.plot(cx + (R + 0.6) * np.sin(th), cy - (R + 0.6) * np.cos(th), color=BLUE, lw=1.6)
ax.plot(cx + (R - 0.6) * np.sin(th), cy - (R - 0.6) * np.cos(th), color=BLUE, lw=1.6)
ax.plot(cx + R * np.sin(th), cy - R * np.cos(th), color=RED, ls="--", lw=1.4)
ax.annotate("", xy=(cx + 0.15, cy - R - 0.6), xytext=(cx + 0.15, cy - R),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.4))
ax.text(cx + 0.35, cy - R - 0.4, r"$y$", fontsize=11, color=GREEN)
ax.text(cx + 1.7, cy - R + 0.05, "中性层", ha="left", fontsize=9, color=RED, va="center")
ax.text(5, 5.5, r"平面假设：$\varepsilon=\dfrac{y}{\rho}$", ha="center", fontsize=11, color=BLUE)
ax.text(5, 0.4, "(a) 几何", ha="center", fontsize=11, weight="bold")

# (b) 物理：sigma=E*eps=E*y/rho
ax = axes[1]
ax.annotate("", xy=(3, 1.2), xytext=(3, 4.8), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.annotate("", xy=(7, 4.8), xytext=(7, 1.2), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.plot([3, 7], [3, 3], color=GREY, ls="--")
ax.text(5.0, 5.3, r"$\sigma=E\varepsilon=\dfrac{Ey}{\rho}$", ha="center", fontsize=11, color=RED)
ax.text(5, 0.8, "(b) 物理", ha="center", fontsize=11, weight="bold")

# (c) 静力：中性轴过形心
ax = axes[2]
ax.add_patch(Rectangle((3, 1.5), 4, 3, fc="#eef2f7", ec=GREY))
ax.plot([2.6, 7.4], [3, 3], color=GREEN, lw=1.8)
ax.plot([5], [3], marker="o", color=RED, ms=6)
ax.text(7.5, 3, r"中性轴", fontsize=9.5, color=GREEN, va="center")
ax.text(5, 5.3, r"$\int_A\sigma\,\mathrm{d}A=0 \Rightarrow$ 中性轴过形心", ha="center", fontsize=10, color=GREEN)
ax.text(5, 0.8, "(c) 静力", ha="center", fontsize=11, weight="bold")
savefig(fig, "lec09_fig2_three_steps")


# ---------------------------------------------------------------------
print()
print("=== 图 3：横截面正应力线性分布 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.6))

# (a) 截面上的应力箭头（线性，箭头长度正比于 |y|）
a1.set_xlim(-1.9, 1.9)
a1.set_ylim(-60, 60)
a1.axis("off")
a1.add_patch(Rectangle((-0.35, -50), 0.7, 100, fc="#eef2f7", ec=GREY))
for yv in [-50, -25, 25, 50]:
    L = 1.1 * abs(yv) / 50.0
    if yv > 0:
        a1.annotate("", xy=(0.35 + L, yv), xytext=(0.35, yv),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
    else:
        a1.annotate("", xy=(-0.35 - L, yv), xytext=(-0.35, yv),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.8))
a1.text(0, 54, r"$+\sigma_{\max}$（受拉）", ha="center", fontsize=9, color=RED)
a1.text(0, -58, r"$-\sigma_{\max}$（受压）", ha="center", fontsize=9, color=BLUE)
a1.text(0, 0, "中性轴", ha="center", va="center", fontsize=8.5, color=GREY)
a1.set_title("(a) 沿高度线性：中性轴为零", fontsize=10, weight="bold")

# (b) sigma(y) 直线
yv = np.linspace(-50, 50, 50)
sig = M * yv / I
a2.set_xlim(-120, 120)
a2.set_ylim(-60, 60)
a2.plot(sig, yv, color=BLUE, lw=2.4)
a2.axhline(0, color=GREY, lw=0.8)
a2.axvline(0, color=GREY, lw=0.8)
a2.plot([sig_max, -sig_max], [50, -50], "o", color=RED, ms=5)
a2.text(sig_max, 54, r"$+\sigma_{\max}$", ha="center", fontsize=9, color=RED)
a2.text(-sig_max, 54, r"$-\sigma_{\max}$", ha="center", fontsize=9, color=BLUE)
a2.set_xlabel(r"正应力 $\sigma$ / MPa", fontsize=10)
a2.set_ylabel(r"到中性轴距离 $y$ / mm", fontsize=10)
a2.set_title(r"(b) $\sigma = \dfrac{My}{I_z}$", fontsize=10, weight="bold")
savefig(fig, "lec09_fig3_stress_dist")

print()
print("[DONE] 第 09 讲数字核对与三张图全部完成。")
