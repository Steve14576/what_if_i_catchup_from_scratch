# =====================================================================
# lec10-01 第 10 讲《弯曲切应力与提高弯曲强度的措施》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 矩形弯曲切应力：tau=Q*S_z*/(I_z b)，最大在中性轴 tau_max=3Q/(2A)
#   EXP2 互证：由 S_z* 公式在中性轴处的结果 = 3Q/(2A)
#   EXP3 工字形：腹板切应力最大（剪力主要由腹板承担）
#   EXP4 圆形截面：tau_max = 4Q/(3A)（认识层对照）
#   EXP5 切应力强度条件校核
# 出图（编号按正文出现顺序）：
#   lec10_fig1_shear_origin    弯曲切应力的来源（微段切应力互等）
#   lec10_fig2_rect_parabola   矩形截面切应力抛物线分布
#   lec10_fig3_i_circle        工字形切应力分布 + 圆形（认识层）
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
print("=== 数字核对：第 10 讲 ===")

# EXP1 矩形 60x100
b, h, Q = 60.0, 100.0, 20.0e3
A = b * h
I = b * h ** 3 / 12.0
tau_max_rect = 3.0 * Q / (2.0 * A)
print("  EXP1 矩形 b=%.0f,h=%.0f,Q=%.0f kN：A=%.0f mm^2" % (b, h, Q / 1e3, A))
print("        tau_max = 3Q/(2A) = %.2f MPa（中性轴处）" % tau_max_rect)

# EXP2 由 S_z* 公式互证
S_star_NA = b * (h / 2.0) ** 2 / 2.0
tau_NA = Q * S_star_NA / (I * b)
print("  EXP2 互证：S_z*(中性轴)=%.0f mm^3；tau=Q*S_z*/(I b)=%.2f MPa（应与 3Q/2A 一致）"
      % (S_star_NA, tau_NA))

# EXP3 工字形（上下翼缘 80x10，腹板 20x60）
bf, tf, bw, hw = 80.0, 10.0, 20.0, 60.0
Af, Aw = bf * tf, bw * hw
A_i = 2 * Af + Aw
H_i = 2 * tf + hw
It = 2 * (bf * tf ** 3 / 12.0 + Af * (hw / 2.0 + tf / 2.0) ** 2) + bw * hw ** 3 / 12.0
Sz_NA_i = Af * (hw / 2.0 + tf / 2.0) + bw * (hw / 2.0) * (hw / 4.0)
tau_max_i = Q * Sz_NA_i / (It * bw)
print("  EXP3 工字形（总高 %.0f, I=%.4e, 腹板面积占比 %.0f%%）：" % (H_i, It, Aw / A_i * 100))
print("        腹板内最大切应力（中性轴）tau_max = %.2f MPa（远大于翼缘）" % tau_max_i)
print("        结论：剪力主要由腹板承担")

# EXP4 圆形
d = 50.0
A_c = np.pi * d ** 2 / 4.0
tau_max_c = 4.0 * Q / (3.0 * A_c)
print("  EXP4 圆 d=%.0f：A=%.0f mm^2；tau_max = 4Q/(3A) = %.2f MPa" % (d, A_c, tau_max_c))

# EXP5 切应力强度条件
tau_all = 60.0
print("  EXP5 切应力强度条件：矩形 tau_max=%.2f MPa 是否 <= [tau]=%.1f MPa ? %s"
      % (tau_max_rect, tau_all, "安全" if tau_max_rect <= tau_all else "不合格"))


# ---------------------------------------------------------------------
print()
print("=== 图 1：弯曲切应力的来源 ===")
fig, ax = plt.subplots(figsize=(9.4, 4.4))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5)
ax.axis("off")
# 梁（两段示意，中间截面）
ax.add_patch(Rectangle((1.0, 2.0), 4.5, 1.2, fc="#cfe3f7", ec=BLUE))
ax.add_patch(Rectangle((6.5, 2.0), 4.5, 1.2, fc="#cfe3f7", ec=BLUE))
ax.plot([6.0, 6.0], [1.9, 3.3], color=GREY, ls="--")
ax.text(6.0, 3.5, "横截面", ha="center", fontsize=9.5, color=GREY)
# 横截面上的切应力（竖向箭头）
ax.annotate("", xy=(6.0, 3.0), xytext=(6.0, 2.2), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(6.3, 2.6, r"$\tau$", fontsize=12, color=RED)
# 顶面与底面的切应力（互等）
ax.annotate("", xy=(8.0, 3.2), xytext=(6.5, 3.2), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2))
ax.annotate("", xy=(5.5, 2.0), xytext=(1.5, 2.0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2))
ax.text(7.2, 3.45, r"$\tau'$（顶面）", ha="center", fontsize=9.5, color=GREEN)
ax.text(3.5, 1.65, r"$\tau'$（底面）", ha="center", fontsize=9.5, color=GREEN)
ax.text(6.0, 4.6, "横截面的切应力 = 由「上下相邻层」的切应力互等推出", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec10_fig1_shear_origin")


# ---------------------------------------------------------------------
print()
print("=== 图 2：矩形截面切应力抛物线分布 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.2, 4.4))
# (a) 截面箭头
a1.set_xlim(-2.4, 2.4)
a1.set_ylim(-60, 60)
a1.axis("off")
a1.add_patch(Rectangle((-0.5, -50), 1.0, 100, fc="#eef2f7", ec=GREY))
for yv in [-50, -40, -25, 0, 25, 40, 50]:
    t = 1 - (2 * yv / 100.0) ** 2     # 相对 tau (中性轴=1)
    L = 1.6 * t
    if L > 0.01:
        a1.annotate("", xy=(0.5 + L, yv), xytext=(0.5, yv),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))
a1.axvline(0, color=GREY, lw=0.6)
a1.text(0, 54, "上缘 tau=0", ha="center", fontsize=9, color=GREY)
a1.text(0, -58, "下缘 tau=0", ha="center", fontsize=9, color=GREY)
a1.text(0.5 + 1.75, 0, "中性轴 tau_max", ha="left", fontsize=9, color=RED, va="center")
a1.set_title("(a) 切应力沿高度变化", fontsize=10, weight="bold")

# (b) 抛物线 tau(y)
yv = np.linspace(-50, 50, 100)
tau = Q * (h ** 2 / 4 - yv ** 2) / (2 * I) / 1e0   # MPa
a2.set_xlim(0, tau_max_rect * 1.2)
a2.set_ylim(-60, 60)
a2.plot(tau, yv, color=BLUE, lw=2.4)
a2.axvline(0, color=GREY, lw=0.8)
a2.plot([tau_max_rect], [0], "o", color=RED, ms=6)
a2.text(tau_max_rect, 6, r"$\tau_{\max}=3Q/(2A)$", ha="left", fontsize=9, color=RED)
a2.set_xlabel(r"切应力 $\tau$ / MPa", fontsize=10)
a2.set_ylabel(r"到中性轴距离 $y$ / mm", fontsize=10)
a2.set_title(r"(b) 抛物线：中性轴处最大", fontsize=10, weight="bold")
savefig(fig, "lec10_fig2_rect_parabola")


# ---------------------------------------------------------------------
print()
print("=== 图 3：工字形切应力分布 + 圆形 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.6))

# (a) 工字形：腹板 tau 大、翼缘 tau 小（交界跳变）
a1.set_xlim(-60, 60)
a1.set_ylim(-60, 60)
a1.axis("off")
# 半个工字（右半）截面轮廓
a1.add_patch(Rectangle((0, 30), 40, 10, fc="#fde9d9", ec=ORANGE))   # 上翼缘
a1.add_patch(Rectangle((0, -30), 40, 10, fc="#fde9d9", ec=ORANGE))  # 下翼缘
a1.add_patch(Rectangle((0, -30), 10, 60, fc="#cfe3f7", ec=BLUE))    # 腹板
# tau 分布（水平箭头，腹板区大、翼缘区小）
for yv in np.linspace(-30, 30, 9):
    t = 1 - (yv / 40.0) ** 2 * 0.3
    a1.annotate("", xy=(10 + 45 * t, yv), xytext=(10, yv),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))
a1.annotate("", xy=(10 + 8, 35), xytext=(10, 35), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
a1.text(50, 35, "翼缘 tau 小", fontsize=9, color=ORANGE, va="center")
a1.text(56, 0, "腹板 tau 大", fontsize=9, color=RED, va="center")
a1.text(-55, 50, "(a) 工字形：腹板主要抗剪", fontsize=10, weight="bold")

# (b) 圆形 tau 抛物线
a2.set_xlim(-30, 30)
a2.set_ylim(-30, 30)
a2.set_aspect("equal")
a2.axis("off")
th = np.linspace(0, 2 * np.pi, 100)
a2.plot(25 * np.cos(th), 25 * np.sin(th), color=GREY)
for yv in [-25, -12, 0, 12, 25]:
    t = 1 - (yv / 25.0) ** 2
    L = 22 * t
    if L > 0.5:
        a2.annotate("", xy=(L, yv), xytext=(0, yv), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5))
a2.text(0, -33, r"圆形：$\tau_{\max}=4Q/(3A)$（认识层）", ha="center", fontsize=9.5)
a2.text(0, 31, "(b) 圆形截面切应力", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec10_fig3_i_circle")

print()
print("[DONE] 第 10 讲数字核对与三张图全部完成。")
