# =====================================================================
# lec18-01 第 18 讲《能量法》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对（简支梁跨中集中力：P=20 kN，L=4000 mm，E=2e5 MPa，I=5e6 mm^4）：
#   EXP1 弯曲应变能 V=P^2 L^3/(96 E I)，并与 (1/2)P*w_max 互证
#   EXP2 单位载荷法（莫尔积分数值积分）求跨中挠度，与 PL^3/(48EI) 一致
#   EXP3 图形互乘法 (L/3)*M_max*Mbar_max/EI，与 EXP2 一致（三法互证）
#   EXP4 位移互等定理 delta_12 = delta_21 数值验证
#   EXP5 卡氏定理 w = dV/dP = PL^3/(48EI)，与查表一致
# 出图（编号按正文出现顺序）：
#   lec18_fig1_strain_energy    三种基本变形的应变能
#   lec18_fig2_unit_load        单位载荷法与莫尔积分
#   lec18_fig3_graph_mult       图形互乘法
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


def savefig(fig, stem):
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, stem + ".svg"))
    fig.savefig(os.path.join(FIGDIR, stem + ".png"), dpi=200)
    plt.close(fig)
    print("[OK] figures/%s.svg 与 .png 已生成。" % stem)


P, L, E, I = 20.0e3, 4000.0, 2.0e5, 5.0e6
EI = E * I

# ---------------------------------------------------------------------
print("=== 数字核对：第 18 讲（P=%.0f kN, L=%.0f mm, EI=%.3e）===" % (P / 1e3, L, EI))

w_max = P * L ** 3 / (48.0 * EI)
V = P ** 2 * L ** 3 / (96.0 * EI)
print("  EXP1 弯曲应变能：V=P^2 L^3/(96EI)=%.2f N·mm=%.2f J" % (V, V / 1e3))
print("        互证：(1/2)*P*w_max=%.2f N·mm（应一致）" % (0.5 * P * w_max))

# EXP2 单位载荷法（数值积分）
xs = np.linspace(0, L, 2001)


def M_P(x):
    return P * x / 2.0 * (x <= L / 2) + P * (L - x) / 2.0 * (x > L / 2)


def M_unit_mid(x):
    return x / 2.0 * (x <= L / 2) + (L - x) / 2.0 * (x > L / 2)


w_mohr = np.trapezoid(M_P(xs) * M_unit_mid(xs) / EI, xs)
print("  EXP2 单位载荷法（莫尔积分数值积分）：w=%.4f mm（查表 PL^3/(48EI)=%.4f）"
      % (w_mohr, w_max))

# EXP3 图形互乘
M_max = P * L / 4.0
Mbar_max = L / 4.0
w_graph = (L / 3.0) * M_max * Mbar_max / EI
print("  EXP3 图形互乘：(L/3)*M_max*Mbar_max/EI=%.4f mm（与上一致）" % w_graph)

# EXP4 位移互等
x1, x2 = L / 3.0, 2.0 * L / 3.0


def M_unit_at(x, xp):
    """单位力作用于 xp 时的弯矩图（简支梁）。"""
    b = L - xp
    return np.where(x <= xp, b * x / L, xp * (L - x) / L)


d12 = np.trapezoid(M_unit_at(xs, x2) * M_unit_at(xs, x1) / EI, xs)
d21 = np.trapezoid(M_unit_at(xs, x1) * M_unit_at(xs, x2) / EI, xs)
print("  EXP4 位移互等：delta_12=%.6e mm/N, delta_21=%.6e mm/N（应相等，差 %.2e）"
      % (d12, d21, abs(d12 - d21)))

# EXP5 卡氏定理
w_cast = 2.0 * P * L ** 3 / (96.0 * EI)
print("  EXP5 卡氏定理：w=dV/dP=%.4f mm（与查表一致）" % w_cast)

# EXP6 图形互乘的二次抛物线特例（均布载荷，跨中单位力）
q = 10.0
M_par_peak = q * L ** 2 / 8.0
Omega_par = 2.0 / 3.0 * L * M_par_peak
w_par_58 = (5.0 / 8.0) * Omega_par * Mbar_max / EI
w_par_true = 5.0 * q * L ** 4 / (384.0 * EI)
print("  EXP6 抛物线特例（q=%.0f N/mm）：Omega=%.4e, Mbar_中点=%.1f" % (q, Omega_par, Mbar_max))
print("        (5/8)*Omega*Mbar/EI=%.4f mm；查表 5qL^4/(384EI)=%.4f mm（应一致）"
      % (w_par_58, w_par_true))


# ---------------------------------------------------------------------
print()
print("=== 图 1：三种基本变形的应变能 ===")
fig, axes = plt.subplots(1, 3, figsize=(11.8, 4.2))
for ax in axes:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")

# (a) 拉压
axes[0].add_patch(Rectangle((3.2, 3.2), 3.6, 1.4, fc="#e7f0fb", ec=BLUE))
axes[0].annotate("", xy=(2.4, 3.9), xytext=(3.2, 3.9), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
axes[0].annotate("", xy=(7.6, 3.9), xytext=(6.8, 3.9), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
axes[0].text(5.0, 5.6, r"$V_\varepsilon=\dfrac{N^2L}{2EA}$", ha="center", fontsize=13, color=BLUE)
axes[0].text(5.0, 2.2, "(a) 轴向拉压", ha="center", fontsize=10.5, weight="bold")

# (b) 扭转
axes[1].add_patch(Rectangle((2.8, 3.2), 4.4, 1.4, fc="#fde9d9", ec=ORANGE))
axes[1].annotate("", xy=(4.2, 5.2), xytext=(4.8, 4.8), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
axes[1].annotate("", xy=(6.2, 4.8), xytext=(5.6, 5.2), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
axes[1].text(5.0, 5.9, r"$T$", ha="center", fontsize=12, color=GREEN)
axes[1].text(5.0, 2.2, r"$V_\varepsilon=\dfrac{T^2L}{2GI_p}$", ha="center", fontsize=13, color=ORANGE)
axes[1].text(5.0, 1.2, "(b) 扭转", ha="center", fontsize=10.5, weight="bold")

# (c) 弯曲
axes[2].plot([1.6, 8.4], [4.4, 4.4], color=GREY, ls=":", lw=1)
xs2 = np.linspace(1.6, 8.4, 60)
axes[2].plot(xs2, 4.4 - 1.2 * np.sin(np.pi * (xs2 - 1.6) / 6.8), color=BLUE, lw=2.4)
axes[2].annotate("", xy=(5.0, 4.4), xytext=(5.0, 5.6), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
axes[2].text(5.3, 5.6, r"$P$", fontsize=12, color=RED)
axes[2].text(5.0, 1.9, r"$V_\varepsilon=\int\dfrac{M^2(x)}{2EI}\mathrm{d}x$", ha="center", fontsize=11, color=BLUE)
axes[2].text(5.0, 0.9, "(c) 弯曲", ha="center", fontsize=10.5, weight="bold")
savefig(fig, "lec18_fig1_strain_energy")


# ---------------------------------------------------------------------
print()
print("=== 图 2：单位载荷法与莫尔积分 ===")
fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(12.0, 4.0))
for ax in (a1, a2, a3):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")


def draw_mdiag(ax, peak, color, title, sym):
    ax.plot([1.5, 8.5], [4.6, 4.6], color=GREY, lw=2)
    ax.add_patch(Polygon([[1.5, 4.6], [5.0, 4.6 + peak], [8.5, 4.6]],
                         closed=True, fc="#e7f0fb", ec=color, lw=1.8))
    ax.text(5.0, 4.6 + peak + 0.5, sym, ha="center", fontsize=11, color=color)
    ax.text(5.0, 1.8, title, ha="center", fontsize=10.5, weight="bold")


draw_mdiag(a1, 2.1, RED, "(a) 实际载荷的 M 图", r"$M(x)$")
a1.annotate("", xy=(5.0, 6.9), xytext=(5.0, 6.65), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a1.text(5.3, 6.85, r"$P$", fontsize=11, color=RED)

draw_mdiag(a2, 1.3, GREEN, r"(b) 单位载荷的 $\bar{M}$ 图", r"$\bar{M}(x)$")
a2.annotate("", xy=(5.0, 6.1), xytext=(5.0, 5.85), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2))
a2.text(5.3, 6.05, r"$1$", fontsize=11, color=GREEN)

a3.text(5.0, 5.4, r"$\Delta=\int\dfrac{M(x)\bar{M}(x)}{EI}\mathrm{d}x$",
        ha="center", fontsize=13, color=BLUE)
a3.text(5.0, 3.4, "（莫尔积分）", ha="center", fontsize=10, color=GREY)
a3.text(5.0, 2.2, "(c) 莫尔积分", ha="center", fontsize=10.5, weight="bold")
savefig(fig, "lec18_fig2_unit_load")


# ---------------------------------------------------------------------
print()
print("=== 图 3：图形互乘法 ===")
fig, ax = plt.subplots(figsize=(9.4, 5.2))
ax.set_xlim(-0.5, 10.5)
ax.set_ylim(-1.2, 7.2)
ax.axis("off")
# 共同基线
ax.plot([1, 9], [3.0, 3.0], color=GREY, lw=1.6)
# M 图（基线上方）
ax.add_patch(Polygon([[1, 3.0], [5, 5.6], [9, 3.0]], closed=True, fc="#e7f0fb", ec=BLUE, lw=1.8))
ax.text(5, 5.85, r"$M$ 图（面积 $\Omega$）", ha="center", fontsize=10, color=BLUE)
ax.plot([5], [3.0 + (5.6 - 3.0) / 3.0], "o", color=RED, ms=6)
ax.text(5.15, 3.72, r"形心 $C$", fontsize=9.5, color=RED)
# Mbar 图（基线下方）
ax.add_patch(Polygon([[1, 3.0], [5, 1.4], [9, 3.0]], closed=True, fc="#e8f5e9", ec=GREEN, lw=1.8))
ax.text(5, 0.8, r"$\bar{M}$ 图", ha="center", fontsize=10, color=GREEN)
# 形心处的竖标（自基线量起）
ax.plot([5, 5], [3.0 + (5.6 - 3.0) / 3.0, 1.4], color=GREY, ls=":", lw=1.2)
ax.annotate("", xy=(5, 1.4), xytext=(5, 3.0), arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.4))
ax.text(5.15, 2.05, r"$\bar{M}_C$（形心处的竖标）", fontsize=9.5, color=ORANGE)
ax.text(5, 6.7, r"$\Delta=\dfrac{\Omega\cdot\bar{M}_C}{EI}$", ha="center", fontsize=14, color=BLUE)
savefig(fig, "lec18_fig3_graph_mult")

print()
print("[DONE] 第 18 讲数字核对与三张图全部完成。")