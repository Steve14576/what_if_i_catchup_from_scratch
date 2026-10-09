# =====================================================================
# lec16-01 第 16 讲《组合变形》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 拉弯组合（矩形柱 100x150，N=100 kN，M=10 kN·m）：sigma=N/A +/- M/W
#   EXP2 偏心压力（矩形 200x300，N=200 kN，e=50 mm=h/6）：应力零线正好在边缘（核心边界）
#   EXP3 截面核心（圆 d=200：e_core=d/8=25 mm，验证边缘应力为零）
#   EXP4 弯扭组合（圆轴 d=60，M=1.5 kN·m，T=1.2 kN·m）：sigma_r3、sigma_r4
# 出图（编号按正文出现顺序）：
#   lec16_fig1_decompose      组合变形的分解与叠加
#   lec16_fig2_eccentric_core  偏心拉压与截面核心
#   lec16_fig3_bend_twist      弯扭组合与危险点
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


# ---------------------------------------------------------------------
print("=== 数字核对：第 16 讲 ===")

# EXP1 拉弯组合
b1, h1, N1, M1 = 100.0, 150.0, 100.0e3, 10.0e6
A1 = b1 * h1
W1 = b1 * h1 ** 2 / 6.0
sN1 = N1 / A1
sM1 = M1 / W1
print("  EXP1 拉弯组合（b=%.0f, h=%.0f, N=%.0f kN, M=%.0f kN·m）：" % (b1, h1, N1 / 1e3, M1 / 1e6))
print("        A=%.0f mm^2, W=%.4e mm^3 -> sigma_N=%.3f, sigma_M=%.3f MPa" % (A1, W1, sN1, sM1))
print("        sigma_max=%.2f MPa（拉侧）, sigma_min=%.2f MPa（压侧）" % (sN1 + sM1, sN1 - sM1))

# EXP2 偏心压力（矩形，e=h/6）
b2, h2, N2, e2 = 200.0, 300.0, 200.0e3, 50.0
A2 = b2 * h2
W2 = b2 * h2 ** 2 / 6.0
sN2 = -N2 / A2
sM2 = -N2 * e2 / W2
print("  EXP2 偏心压力（b=%.0f,h=%.0f, N=%.0f kN 压, e=%.0f mm）：" % (b2, h2, N2 / 1e3, e2))
print("        sigma=-N/A +/- N*e/W = %.3f +/- %.3f -> %.3f / %.3f MPa（零线在边缘=核心边界 h/6=%.0f）"
      % (sN2, abs(sM2), sN2 + sM2, sN2 - sM2, h2 / 6.0))

# EXP3 截面核心（圆）
d3, N3 = 200.0, 100.0e3
A3 = np.pi * d3 ** 2 / 4.0
W3 = np.pi * d3 ** 3 / 32.0
ec = d3 / 8.0
sig_edge_c = -N3 / A3 + N3 * ec / W3
print("  EXP3 圆截面核心：e_core=d/8=%.1f mm；核边处边缘应力=-N/A+N*e/W=%.4f MPa（应约为 0）"
      % (ec, sig_edge_c))

# EXP4 弯扭组合
d4, M4, T4 = 60.0, 1.5e6, 1.2e6
W4 = np.pi * d4 ** 3 / 32.0
Wp4 = np.pi * d4 ** 3 / 16.0
sig4 = M4 / W4
tau4 = T4 / Wp4
sr3 = np.sqrt(sig4 ** 2 + 4 * tau4 ** 2)
sr4 = np.sqrt(sig4 ** 2 + 3 * tau4 ** 2)
print("  EXP4 弯扭组合（d=%.0f, M=%.2f kN·m, T=%.2f kN·m）：" % (d4, M4 / 1e6, T4 / 1e6))
print("        W=%.1f, Wp=%.1f -> sigma=%.2f MPa, tau=%.2f MPa" % (W4, Wp4, sig4, tau4))
print("        sigma_r3=sqrt(s^2+4t^2)=%.2f MPa; sigma_r4=sqrt(s^2+3t^2)=%.2f MPa" % (sr3, sr4))


# ---------------------------------------------------------------------
print()
print("=== 图 1：组合变形的分解与叠加 ===")
fig, axes = plt.subplots(1, 3, figsize=(11.6, 4.2))
for ax in axes:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

# (a) 原结构
axes[0].add_patch(Rectangle((2.0, 2.0), 4.0, 2.0, fc="#e7f0fb", ec=BLUE))
axes[0].add_patch(Polygon([[1.4, 2.0], [6.6, 2.0], [6.6, 1.6], [1.4, 1.6]], closed=True, fc=GREY))
axes[0].annotate("", xy=(6.0, 4.6), xytext=(6.0, 4.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
axes[0].text(6.2, 4.6, r"$F$（偏心/斜向）", fontsize=10, color=RED)
axes[0].text(5.0, 0.8, "(a) 原结构", ha="center", fontsize=11, weight="bold")

# (b) 分解为 N 与 M
axes[1].add_patch(Rectangle((2.0, 2.0), 4.0, 2.0, fc="#fde9d9", ec=ORANGE))
axes[1].annotate("", xy=(6.0, 4.6), xytext=(6.0, 4.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))
axes[1].annotate("", xy=(2.6, 4.6), xytext=(5.4, 4.6), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6))
axes[1].text(3.0, 4.8, r"$N$（轴力）", fontsize=9.5, color=BLUE)
axes[1].text(6.2, 4.6, r"$M$（弯矩）", fontsize=9.5, color=RED)
axes[1].text(5.0, 0.8, "(b) 分解：N + M", ha="center", fontsize=11, weight="bold")

# (c) 叠加应力
axes[2].plot([2, 8], [3.0, 3.0], color=GREY, ls=":", lw=1)
axes[2].plot([3.6, 3.6], [1.4, 4.6], color=BLUE, lw=1.4)
axes[2].plot([6.4, 6.4], [1.4, 4.6], color=BLUE, lw=1.4)
axes[2].text(5.0, 5.4, r"$\sigma=\dfrac{N}{A}\pm\dfrac{M}{W}$", ha="center", fontsize=12, color=BLUE)
axes[2].annotate("", xy=(6.4, 4.2), xytext=(6.4, 3.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5))
axes[2].annotate("", xy=(6.4, 1.8), xytext=(6.4, 3.0), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.5))
axes[2].text(3.4, 3.2, "拉侧", fontsize=9, color=RED)
axes[2].text(6.6, 2.0, "压侧", fontsize=9, color=BLUE)
axes[2].text(5.0, 0.8, "(c) 同一点叠加", ha="center", fontsize=11, weight="bold")
savefig(fig, "lec16_fig1_decompose")


# ---------------------------------------------------------------------
print()
print("=== 图 2：偏心拉压与截面核心 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 4.8))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect("equal")
    ax.axis("off")

# (a) 偏心压力 + 应力分布
a1.add_patch(Rectangle((3.0, 1.6), 3.0, 4.4, fc="#eef2f7", ec=GREY))
a1.annotate("", xy=(4.0, 6.6), xytext=(4.0, 6.1), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2))
a1.text(3.6, 6.8, r"$F$（压力）", fontsize=10, color=RED)
a1.plot([4.0, 4.0], [1.6, 6.0], color=ORANGE, ls="--", lw=1.2)
a1.text(4.1, 4.0, r"$e$", fontsize=11, color=ORANGE)
# 应力分布（线性；e=h/6 时一侧为零 -> 三角形）
a1.plot([6.0, 6.0], [1.6, 6.0], color=GREY, lw=1)
a1.add_patch(Polygon([[6.0, 6.0], [6.0, 1.6], [6.9, 1.6]], closed=True, fc="#dbe9f8", ec=BLUE, lw=1.6))
a1.text(7.05, 1.4, r"$\sigma$", fontsize=11, color=BLUE)
a1.text(5.75, 6.15, "0", fontsize=9, color=GREY)
a1.text(5.0, 0.8, "(a) 偏心压力：应力线性分布", ha="center", fontsize=11, weight="bold")

# (b) 截面核心
a2.add_patch(Rectangle((2.8, 2.0), 4.4, 4.0, fc="#eef2f7", ec=GREY))
h_core = 4.0 / 6.0 * 2      # 核心高度 = 2*(h/6) 的示意（h 对应 4.0）
b_core = 4.4 / 6.0 * 2
a2.add_patch(Polygon([[5.0, 2.0 + h_core / 2], [2.8 + 4.4 / 2 - b_core / 2, 4.0],
                      [5.0, 6.0 - h_core / 2], [2.8 + 4.4 / 2 + b_core / 2, 4.0]],
                     closed=True, fc="#fde9d9", ec=ORANGE))
a2.text(5.0, 4.0, "截面核心", ha="center", fontsize=10, color=ORANGE)
a2.text(5.0, 1.2, r"矩形：$|e|\leq h/6$（或 $b/6$）；圆：$e\leq d/8$", ha="center", fontsize=9.5, color=BLUE)
a2.text(5.0, 0.4, "(b) 截面核心（力作用在此区域内全截面受压）", ha="center", fontsize=9.5, weight="bold")
savefig(fig, "lec16_fig2_eccentric_core")


# ---------------------------------------------------------------------
print()
print("=== 图 3：弯扭组合与危险点 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 4.4))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect("equal")
    ax.axis("off")

# (a) 圆轴受 M 与 T
a1.add_patch(Rectangle((1.5, 2.2), 7.0, 1.6, fc="#e7f0fb", ec=BLUE))
a1.add_patch(Polygon([[1.5, 2.2], [1.5, 3.8], [1.0, 3.0]], closed=True, fc=GREY))
a1.annotate("", xy=(1.0, 3.6), xytext=(1.0, 2.4), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.8))
a1.text(0.3, 3.0, r"$M$", fontsize=12, color=RED, va="center")
a1.annotate("", xy=(5.0, 4.6), xytext=(4.2, 4.1), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
a1.annotate("", xy=(6.6, 3.9), xytext=(5.8, 4.4), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
a1.text(5.4, 4.9, r"$T$", fontsize=12, color=GREEN)
a1.plot([6.8], [3.0], "o", color=ORANGE, ms=7)
a1.text(7.0, 3.2, "危险点", fontsize=9.5, color=ORANGE)
a1.text(5.0, 0.9, "(a) 圆轴：弯矩 M + 扭矩 T", ha="center", fontsize=11, weight="bold")

# (b) 危险点单元体
a2.add_patch(Rectangle((3.6, 2.0), 2.8, 2.8, fc="#fde9d9", ec=ORANGE))
a2.annotate("", xy=(8.0, 3.4), xytext=(6.5, 3.4), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a2.text(8.2, 3.4, r"$\sigma$", fontsize=12, color=RED, va="center")
a2.annotate("", xy=(6.4, 4.9), xytext=(6.4, 3.5), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2))
a2.text(6.5, 5.1, r"$\tau$", fontsize=12, color=GREEN)
a2.text(5.0, 5.6, r"$\sigma_{r3}=\sqrt{\sigma^2+4\tau^2}$；$\sigma_{r4}=\sqrt{\sigma^2+3\tau^2}$",
        ha="center", fontsize=10, color=BLUE)
a2.text(5.0, 1.0, "(b) 危险点：弯曲正应力 + 扭转切应力", ha="center", fontsize=11, weight="bold")
savefig(fig, "lec16_fig3_bend_twist")

print()
print("[DONE] 第 16 讲数字核对与三张图全部完成。")