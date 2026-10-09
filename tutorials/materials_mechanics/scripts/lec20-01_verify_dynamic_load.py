# =====================================================================
# lec20-01 第 20 讲《动载荷》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 等加速构件：k_d=1+a/g（a=2 m/s^2）与动应力
#   EXP2 自由落体冲击：k_d=1+sqrt(1+2h/Delta_st)（h=100, Delta_st=2）与 h=0 的特例
#   EXP3 冲击动应力 sigma_d=k_d*sigma_st
#   EXP4 反直觉核对：刚度大（Delta_st 小）-> k_d 更大 -> 动应力更大
#   EXP5 能量方程核对：mg(h+Delta_d)=0.5*k*Delta_d^2
# 出图（编号按正文出现顺序）：
#   lec20_fig1_two_types     动载荷的两类：等加速与冲击
#   lec20_fig2_kd_curve      冲击动荷系数曲线
#   lec20_fig3_measures      提高抗冲击能力的措施
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

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
g = 9.8


def savefig(fig, stem):
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, stem + ".svg"))
    fig.savefig(os.path.join(FIGDIR, stem + ".png"), dpi=200)
    plt.close(fig)
    print("[OK] figures/%s.svg 与 .png 已生成。" % stem)


# ---------------------------------------------------------------------
print("=== 数字核对：第 20 讲 ===")

a, sig_st = 2.0, 100.0
kd_acc = 1.0 + a / g
print("  EXP1 等加速构件（a=%.1f m/s^2, g=%.1f）：k_d=1+a/g=%.4f" % (a, g, kd_acc))
print("        静应力 sigma_st=%.1f MPa -> 动应力 sigma_d=k_d*sigma_st=%.2f MPa" % (sig_st, kd_acc * sig_st))

h, d_st = 100.0, 2.0
kd_imp = 1.0 + np.sqrt(1.0 + 2.0 * h / d_st)
d_d = kd_imp * d_st
print("  EXP2 自由落体冲击（h=%.0f mm, Delta_st=%.1f mm）：k_d=1+sqrt(1+2h/Delta_st)=%.4f" % (h, d_st, kd_imp))
print("        动变形 Delta_d=k_d*Delta_st=%.2f mm；h=0（突加载荷）时 k_d=%.1f" % (d_d, 2.0))

sig_st2 = 30.0
print("  EXP3 冲击动应力：sigma_st=%.1f MPa -> sigma_d=%.4f*%.1f=%.2f MPa" % (sig_st2, kd_imp, sig_st2, kd_imp * sig_st2))

kd_a = 1.0 + np.sqrt(1.0 + 2.0 * h / 1.0)
kd_b = 1.0 + np.sqrt(1.0 + 2.0 * h / 4.0)
print("  EXP4 反直觉核对（同一落差 h=%.0f）：" % h)
print("        刚性件 Delta_st=1.0 mm -> k_d=%.4f；柔性件 Delta_st=4.0 mm -> k_d=%.4f" % (kd_a, kd_b))
print("        结论：Delta_st 越小（越刚）-> k_d 越大 -> 动应力越大")

P_st, k_spring = 1000.0, 500.0
lhs = P_st * (h + d_d)
rhs = 0.5 * k_spring * d_d ** 2
print("  EXP5 能量方程核对：mg(h+Delta_d)=%.1f N·mm；0.5*k*Delta_d^2=%.1f N·mm（应相等）" % (lhs, rhs))


# ---------------------------------------------------------------------
print()
print("=== 图 1：动载荷的两类 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.2, 4.6))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

# (a) 等加速起吊
a1.plot([5.0, 5.0], [1.0, 4.6], color=GREY, lw=2.4)
a1.add_patch(Rectangle((3.9, 0.2), 2.2, 0.8, fc="#e7f0fb", ec=BLUE))
a1.text(5.0, 0.6, "重物", ha="center", fontsize=9.5)
a1.annotate("", xy=(5.0, 5.6), xytext=(5.0, 4.6), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2))
a1.text(5.35, 5.45, r"$a$（向上加速）", fontsize=10, color=RED)
a1.annotate("", xy=(4.0, 1.0), xytext=(4.0, 2.2), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.6))
a1.text(3.7, 1.5, r"$g$", fontsize=11, color=GREY)
a1.text(5.0, 6.5, "(a) 等加速运动构件", ha="center", fontsize=10.5, weight="bold")
a1.text(7.4, 3.0, r"$k_d=1+\dfrac{a}{g}$", fontsize=13, color=BLUE)

# (b) 自由落体冲击
a2.add_patch(Rectangle((4.1, 4.6), 1.8, 1.0, fc="#fde9d9", ec=ORANGE))
a2.text(5.0, 5.1, "落锤", ha="center", fontsize=9.5)
a2.annotate("", xy=(5.0, 3.6), xytext=(5.0, 4.55), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
a2.text(5.35, 4.05, r"$v$（下落）", fontsize=10, color=RED)
a2.plot([1.6, 8.4], [3.2, 3.2], color=BLUE, lw=4)
a2.plot([3.0, 3.0], [2.0, 3.2], color=GREY, lw=1.6)
a2.plot([7.0, 7.0], [2.0, 3.2], color=GREY, lw=1.6)
a2.annotate("", xy=(5.4, 3.2), xytext=(5.4, 2.0), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.4))
a2.text(5.7, 2.5, r"$\Delta_{st}$", fontsize=11, color=GREEN)
a2.text(5.0, 6.5, "(b) 自由落体冲击", ha="center", fontsize=10.5, weight="bold")
a2.text(5.0, 1.2, r"$k_d=1+\sqrt{1+\dfrac{2h}{\Delta_{st}}}$", fontsize=13, color=BLUE)
savefig(fig, "lec20_fig1_two_types")


# ---------------------------------------------------------------------
print()
print("=== 图 2：冲击动荷系数曲线 ===")
fig, ax = plt.subplots(figsize=(8.6, 5.0))
hh = np.linspace(0, 200, 300)
for d0, col, lab in [(1.0, RED, r"$\Delta_{st}=1$ mm（刚）"), (4.0, GREEN, r"$\Delta_{st}=4$ mm（柔）")]:
    ax.plot(hh, 1.0 + np.sqrt(1.0 + 2.0 * hh / d0), color=col, lw=2.2, label=lab)
ax.axhline(2.0, color=GREY, ls=":", lw=1.2)
ax.text(196, 2.4, r"$h=0$ 时 $k_d=2$", ha="right", fontsize=9, color=GREY)
ax.set_xlabel(r"落差 $h$ / mm", fontsize=11)
ax.set_ylabel(r"动荷系数 $k_d$", fontsize=11)
ax.set_ylim(0, 20)
ax.set_xlim(0, 200)
ax.legend(fontsize=10)
ax.set_title(r"$k_d=1+\sqrt{1+2h/\Delta_{st}}$：$\Delta_{st}$ 越小（越刚），$k_d$ 越大", fontsize=10.5)
savefig(fig, "lec20_fig2_kd_curve")


# ---------------------------------------------------------------------
print()
print("=== 图 3：提高抗冲击能力的措施 ===")
fig, ax = plt.subplots(figsize=(9.6, 4.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis("off")
items = [
    ("增大静变形 $\\Delta_{st}$", "加缓冲垫、弹性支座、长而柔的构件", GREEN),
    ("避免应力集中", "圆角过渡、避免缺口与陡变", BLUE),
    ("降低 $E$（选低弹性模量材料）", "橡木缓冲块、橡胶垫", ORANGE),
    ("避免脆性材料", "脆性材料抗冲击差，宜用塑性材料", RED),
]
for i, (t1, t2, col) in enumerate(items):
    y = 5.8 - i * 1.45
    ax.add_patch(Rectangle((0.6, y - 0.45), 8.8, 1.05, fc="#f7fafc", ec=col, lw=1.4))
    ax.text(0.9, y + 0.15, t1, fontsize=11, color=col, weight="bold")
    ax.text(0.9, y - 0.3, t2, fontsize=9.5, color=GREY)
ax.text(5.0, 6.6, "提高构件抗冲击能力的措施", ha="center", fontsize=11.5, weight="bold")
savefig(fig, "lec20_fig3_measures")

print()
print("[DONE] 第 20 讲数字核对与三张图全部完成。")