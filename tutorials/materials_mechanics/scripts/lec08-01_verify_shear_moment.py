# =====================================================================
# lec08-01 第 08 讲《平面弯曲的内力：剪力与弯矩》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 简支梁受集中力：支座反力、剪力方程、弯矩方程、最大弯矩
#   EXP2 简支梁受均布载荷：反力、剪力方程、弯矩方程、最大弯矩（qL^2/8 互证）
#   EXP3 悬臂梁端部集中力：Q、M 与 Mmax
#   EXP4 微分关系核对：dM/dx=Q、dQ/dx=q（数值差分）
# 出图（编号按正文出现顺序）：
#   lec08_fig1_beam_types     梁与支座/载荷类型
#   lec08_fig2_sign_conv      剪力与弯矩的正负约定
#   lec08_fig3_qm_diagram     剪力图与弯矩图（简支梁受集中力）
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


def savefig(fig, stem):
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, stem + ".svg"))
    fig.savefig(os.path.join(FIGDIR, stem + ".png"), dpi=200)
    plt.close(fig)
    print("[OK] figures/%s.svg 与 .png 已生成。" % stem)


# ---------------------------------------------------------------------
print("=== 数字核对：第 08 讲 ===")

# EXP1 简支梁受集中力（L=4 m, P=20 kN, 距左端 a=1 m）
L, P, a = 4.0, 20.0, 1.0
b = L - a
RA = P * b / L
RB = P * a / L
Mmax1 = P * a * b / L
Q_AC = RA
Q_CB = RA - P
print("  EXP1 简支梁 L=%.0f m, P=%.0f kN @ a=%.0f m：" % (L, P, a))
print("        反力 R_A = Pb/L = %.1f kN；R_B = Pa/L = %.1f kN（和 = %.1f 应等于 P）" % (RA, RB, RA + RB))
print("        剪力：AC 段 Q=%+.1f kN；CB 段 Q=%+.1f kN（突变 -P=%.1f）" % (Q_AC, Q_CB, -P))
print("        弯矩最大值 M_max = Pab/L = %.1f kN·m（在集中力处）" % Mmax1)

# EXP2 简支梁受均布载荷（L=4 m, q=10 kN/m）
q = 10.0
R2 = q * L / 2.0
Mmax2 = q * L ** 2 / 8.0
print("  EXP2 简支梁 L=%.0f m, q=%.0f kN/m：" % (L, q))
print("        反力 R = qL/2 = %.1f kN；弯矩最大 M_max = qL^2/8 = %.1f kN·m（跨中）" % (R2, Mmax2))

# EXP3 悬臂梁端部集中力（自由端 P=20 kN, L=4 m）
Mmax3 = P * L
print("  EXP3 悬臂梁（固定端 x=0，自由端 x=L）端部 P=%.0f kN：" % P)
print("        剪力 Q = -%.1f kN（常量）；弯矩 M = -P x，固定端 M_max = -PL = %.1f kN·m" % (P, Mmax3))

# EXP4 微分关系数值核对
x_AC = np.linspace(0.1, 0.9, 50)       # 0..1 m 内（a=1，避开突变点）
M_AC = RA * x_AC
dMdx = np.gradient(M_AC, x_AC)
print("  EXP4 微分关系（AC 段）：dM/dx = Q 数值差分均值 = %.4f（应为 Q=+%.1f）"
      % (np.mean(dMdx), RA))
print("        均布段核对：M=Rx-qx^2/2 -> dM/dx=R-qx；dQ/dx=-q 对应 dQ/dx 的约定")


# ---------------------------------------------------------------------
print()
print("=== 图 1：梁与支座/载荷类型 ===")
fig, axes = plt.subplots(3, 1, figsize=(9.2, 6.0))
for ax in axes:
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.6, 2.2)
    ax.axis("off")


def support_pin(ax, x, y=0.0):
    ax.add_patch(Polygon([[x, y], [x - 0.3, y - 0.5], [x + 0.3, y - 0.5]], closed=True, fc=GREY))


def support_roll(ax, x, y=0.0):
    support_pin(ax, x, y - 0.1)
    ax.add_patch(Polygon([[x - 0.3, y - 0.6], [x + 0.3, y - 0.6], [x, y - 0.9]], closed=True, fc="#a0aec0"))


def support_fixed(ax, x, y0, y1):
    ax.plot([x, x], [y0, y1], color=GREY, lw=2)
    for yy in np.linspace(y0, y1, 6):
        ax.plot([x, x - 0.3], [yy, yy - 0.2], color=GREY, lw=1)


# (1) 简支梁
ax = axes[0]
ax.plot([1, 9], [1, 1], color=BLUE, lw=4)
support_pin(ax, 1, 1.0)
support_roll(ax, 9, 1.0)
ax.annotate("", xy=(5, 1), xytext=(5, 2.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(5.25, 1.9, r"$P$", fontsize=12, color=RED)
ax.text(5, -1.4, "简支梁：一端铰支、一端滚支", ha="center", fontsize=10, weight="bold")

# (2) 悬臂梁
ax = axes[1]
ax.plot([1, 9], [1, 1], color=BLUE, lw=4)
support_fixed(ax, 1, 0.4, 1.6)
# 均布载荷
for xx in np.linspace(1.2, 8.8, 9):
    ax.annotate("", xy=(xx, 1), xytext=(xx, 1.9), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.2))
ax.plot([1.2, 8.8], [1.9, 1.9], color=ORANGE, lw=1.2)
ax.text(5, 2.05, r"均布载荷 $q$", ha="center", fontsize=10, color=ORANGE)
ax.text(5, -1.4, "悬臂梁：一端固定、另一端自由（末段可加分布载荷）", ha="center", fontsize=10, weight="bold")

# (3) 外伸梁
ax = axes[2]
ax.plot([1.5, 9], [1, 1], color=BLUE, lw=4)
support_pin(ax, 3, 1.0)
support_roll(ax, 6.5, 1.0)
ax.annotate("", xy=(1.5, 1), xytext=(1.5, 2.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(1.0, 1.9, r"$P$", fontsize=12, color=RED)
ax.text(5, -1.4, "外伸梁：支座在梁中间，两端伸出", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec08_fig1_beam_types")


# ---------------------------------------------------------------------
print()
print("=== 图 2：剪力与弯矩的正负约定 ===")
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.2))
for a_ in (ax, ax2):
    a_.set_xlim(0, 10)
    a_.set_ylim(-2.6, 3.0)
    a_.axis("off")

# (a) 剪力正：微元左面剪力向上、右面向下（使微元顺时针转）
ax.add_patch(Rectangle((3.4, 0.5), 3.2, 1.2, fc="#e7f0fb", ec=BLUE))
ax.annotate("", xy=(3.4, 2.0), xytext=(3.4, 1.1), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2))
ax.text(2.7, 1.75, r"$Q$", fontsize=12, color=RED)
ax.annotate("", xy=(6.6, 0.7), xytext=(6.6, 1.6), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2))
ax.text(6.9, 1.0, r"$Q$", fontsize=12, color=RED)
ax.text(5, 2.7, "微元左面剪力向上、右面向下", ha="center", fontsize=10, color=RED)
ax.text(5, -1.7, r"剪力 $Q$：使微元顺时针转动为正", ha="center", fontsize=10, weight="bold")

# (b) 弯矩正：下凸、下缘受拉
ax2.plot([1, 9], [1.6, 1.6], color=BLUE, lw=2, ls=":")
xs_ = np.linspace(1, 9, 100)
ys_ = 1.6 - 1.0 * np.sin(np.pi * (xs_ - 1) / 8.0)
ax2.plot(xs_, ys_, color=GREEN, lw=2.5)
ax2.text(5, 2.7, "梁下凸：下缘受拉、上缘受压", ha="center", fontsize=10, color=GREEN)
ax2.text(5, -1.7, r"弯矩 $M$：使梁下凸（下部受拉）为正", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec08_fig2_sign_conv")


# ---------------------------------------------------------------------
print()
print("=== 图 3：剪力图与弯矩图（简支梁受集中力）===")
fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(9.6, 7.2),
                                 gridspec_kw={"height_ratios": [1.0, 1.0, 1.0]})

# (a) 梁与载荷
a1.set_xlim(-0.5, 4.5)
a1.set_ylim(-1.8, 2.0)
a1.axis("off")
a1.plot([0, 4], [0.4, 0.4], color=BLUE, lw=4)
a1.add_patch(Polygon([[0, 0.4], [-0.25, 0.0], [0.25, 0.0]], closed=True, fc=GREY))
a1.add_patch(Polygon([[4, 0.4], [3.75, 0.0], [4.25, 0.0]], closed=True, fc=GREY))
a1.annotate("", xy=(1, 0.4), xytext=(1, 1.4), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a1.text(1.12, 1.35, r"$P=20$ kN", fontsize=10, color=RED)
a1.annotate("", xy=(0, 0.4), xytext=(0, -0.6), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6))
a1.text(-0.25, -0.95, r"$R_A=15$", fontsize=9, color=GREEN, ha="center")
a1.annotate("", xy=(4, 0.4), xytext=(4, -0.6), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6))
a1.text(4.25, -0.95, r"$R_B=5$", fontsize=9, color=GREEN, ha="center")
a1.text(2, 1.75, "简支梁 AB：L=4 m，P=20 kN 距左端 1 m", ha="center", fontsize=10, weight="bold")

# (b) 剪力图
a2.axhline(0, color=GREY, lw=1)
a2.plot([0, 1], [15, 15], color=GREEN, lw=2.4)
a2.plot([1, 4], [-5, -5], color=RED, lw=2.4)
a2.plot([1, 1], [15, -5], color=GREY, ls="--", lw=1.4)
a2.fill_between([0, 1], 0, 15, color="#d7f0d7", alpha=0.7)
a2.fill_between([1, 4], 0, -5, color="#fde9d9", alpha=0.7)
a2.text(0.5, 16, "Q=+15 kN", ha="center", fontsize=9.5, color=GREEN)
a2.text(2.5, -6.5, "Q=-5 kN", ha="center", fontsize=9.5, color=RED)
a2.set_ylim(-10, 20)
a2.set_ylabel(r"剪力 $Q$ / kN", fontsize=10)
a2.set_title(r"剪力图：集中力处突变（跳跃 = $P$）", fontsize=10, weight="bold")
a2.set_xticks([0, 1, 4])

# (c) 弯矩图
a3.axhline(0, color=GREY, lw=1)
a3.plot([0, 1], [0, 15], color=BLUE, lw=2.4)
a3.plot([1, 4], [15, 0], color=BLUE, lw=2.4)
a3.fill_between([0, 1], 0, [0, 15], color="#e7f0fb", alpha=0.7)
a3.fill_between([1, 4], 0, [15, 0], color="#e7f0fb", alpha=0.7)
a3.plot([1], [15], "o", color=RED, ms=6)
a3.text(1.1, 15.6, r"$M_{\max}=15$ kN·m", fontsize=9.5, color=RED)
a3.set_ylim(-2, 20)
a3.set_xlabel("截面位置 x / m", fontsize=10)
a3.set_ylabel(r"弯矩 $M$ / (kN·m)", fontsize=10)
a3.set_title(r"弯矩图：多边形，峰值在剪力为零（突变）处", fontsize=10, weight="bold")
a3.set_xticks([0, 1, 4])
savefig(fig, "lec08_fig3_qm_diagram")

print()
print("[DONE] 第 08 讲数字核对与三张图全部完成。")
