# =====================================================================
# lec02-01 第 02 讲《轴向拉压的内力与应力》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP0 整体平衡（三力之和为零）
#   EXP1 轴力：某截面轴力 = 其左侧外力之和；突变 = 该处集中力
#   EXP2 横截面正应力 sigma = N / A
#   EXP3 斜截面应力 alpha 扫描：sigma_a = sigma*cos^2 a，tau_a = (sigma/2)sin2a
#   EXP4 应力圆不变式核对
# 出图（编号按正文出现顺序）：
#   lec02_fig1_axial_diagram      轴力与轴力图（含突变）
#   lec02_fig2_plane_assumption   平面假设：横截面变形后仍为平面
#   lec02_fig3_inclined_stress    斜截面应力及 alpha 曲线
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, FancyArrowPatch

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


def savefig(fig, stem):
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, stem + ".svg"))
    fig.savefig(os.path.join(FIGDIR, stem + ".png"), dpi=200)
    plt.close(fig)
    print("[OK] figures/%s.svg 与 .png 已生成。" % stem)


# ---------------------------------------------------------------------
print("=== 数字核对：第 02 讲 ===")

# 一根等直杆上作用三个集中力（规定向右为正）：
#   左端 P1 = 30 kN 向右；中间 P2 = 80 kN 向左（即 -80）；右端 P3 = 50 kN 向右。
P1, P2, P3 = 30.0, -80.0, 50.0
print("  EXP0 整体平衡：P1+P2+P3 = %.1f kN（应为 0）" % (P1 + P2 + P3))

# 轴力：某截面轴力 = 该截面左侧全部外力之和（向右为正 -> 拉为正）
N_left = P1               # 左段（P2 左侧）
N_right = P1 + P2         # 右段（P2 右侧）
print("  EXP1 轴力：左段 N = %.1f kN（拉）；右段 N = %.1f kN（压）" % (N_left, N_right))
print("        突变 = N右 - N左 = %.1f kN，恰等于该处集中力 P2 = %.1f kN" % (N_right - N_left, P2))

# 横截面正应力
A = 250.0                 # mm^2
print("  EXP2 正应力 sigma = N / A（A = %.0f mm^2）：" % A)
print("        左段 sigma = %.1f MPa；右段 sigma = %.1f MPa（危险截面在右段）"
      % (N_left * 1e3 / A, N_right * 1e3 / A))

# 斜截面应力：取材料内某点正应力 sigma = 100 MPa
sigma = 100.0
print("  EXP3 斜截面应力（取 sigma = 100 MPa）：")
for deg in [0, 30, 45, 60, 90]:
    a = np.deg2rad(deg)
    sa = sigma * np.cos(a) ** 2
    ta = 0.5 * sigma * np.sin(2 * a)
    print("        alpha = %2d deg : sigma_a = %6.1f MPa , tau_a = %6.1f MPa" % (deg, sa, ta))
al = np.linspace(0, np.pi, 721)
sa_all = sigma * np.cos(al) ** 2
ta_all = 0.5 * sigma * np.sin(2 * al)
print("        极值：sigma_a 最大 = %.1f MPa（alpha = 0）；tau_a 最大 = %.1f MPa（alpha = 45 deg）"
      % (sa_all.max(), ta_all.max()))

# 应力圆不变式：(sigma_a - sigma/2)^2 + tau_a^2 = (sigma/2)^2
c = sigma / 2.0
inv = (sa_all - c) ** 2 + ta_all ** 2
print("  EXP4 应力圆不变式：(sigma_a - sigma/2)^2 + tau_a^2 = (sigma/2)^2，最大偏差 = %.2e（应为 0）"
      % np.max(np.abs(inv - c ** 2)))


# ---------------------------------------------------------------------
print()
print("=== 图 1：轴力与轴力图 ===")
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.6, 5.8),
                             gridspec_kw={"height_ratios": [1.0, 1.25]})

# (a) 杆与外力
a1.set_xlim(0, 10.5)
a1.set_ylim(-1.4, 2.4)
a1.axis("off")
a1.add_patch(Rectangle((1.0, 0.6), 8.0, 0.8, fc="#cfe3f7", ec=BLUE))
a1.plot([5.0, 5.0], [0.5, 1.5], color=GREY, ls=":", lw=1.6)   # 分段位置
# P1（左端向右）
a1.annotate("", xy=(1.9, 1.9), xytext=(0.9, 1.9),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a1.text(1.35, 2.15, "P1 = 30 kN", ha="center", fontsize=10, color=RED)
# P2（中间向左）
a1.annotate("", xy=(4.1, -0.7), xytext=(5.9, -0.7),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a1.text(5.0, -1.15, "P2 = 80 kN", ha="center", fontsize=10, color=RED)
# P3（右端向右）
a1.annotate("", xy=(9.9, 1.9), xytext=(8.9, 1.9),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a1.text(9.4, 2.15, "P3 = 50 kN", ha="center", fontsize=10, color=RED)
a1.text(5.0, 1.55, "(a) 等直杆：三个沿轴线的集中力", ha="center", fontsize=10, weight="bold")

# (b) 轴力图
a2.axhline(0, color=GREY, lw=1)
a2.fill_between([1, 5], 0, N_left, step="post", color="#d7f0d7", alpha=0.8)
a2.fill_between([5, 9], 0, N_right, step="post", color="#fde9d9", alpha=0.8)
a2.plot([1, 5], [N_left, N_left], color=GREEN, lw=2.4)
a2.plot([5, 9], [N_right, N_right], color=RED, lw=2.4)
a2.plot([5, 5], [N_left, N_right], color=GREY, ls="--", lw=1.4)
a2.plot([1, 5], [N_left, N_left], "o", color=GREEN, ms=5)
a2.plot([5, 5], [N_left, N_right], "o", color=GREY, ms=4)
a2.plot([5, 9], [N_right, N_right], "o", color=RED, ms=5)
a2.text(3.0, N_left + 6, "N = +30 kN（拉）", ha="center", fontsize=10, color=GREEN)
a2.text(7.0, N_right - 14, "N = -50 kN（压）", ha="center", fontsize=10, color=RED)
a2.annotate("突变 = P2", xy=(5, 0), xytext=(5.9, 6),
            fontsize=9.5, color=GREY,
            arrowprops=dict(arrowstyle="->", color=GREY, lw=1))
a2.set_xlim(0, 10.5)
a2.set_ylim(-70, 50)
a2.set_xlabel("截面位置 x", fontsize=10)
a2.set_ylabel("轴力 N / kN", fontsize=10)
a2.set_title("(b) 轴力图：内力随截面变化，集中力处跳变", fontsize=10.5, weight="bold")
a2.set_xticks([1, 5, 9])
a2.set_xticklabels(["左端", "P2", "右端"], fontsize=9)

savefig(fig, "lec02_fig1_axial_diagram")


# ---------------------------------------------------------------------
print()
print("=== 图 2：平面假设 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.2, 2.7))
for ax in (a1, a2):
    ax.set_xlim(0, 12)
    ax.set_ylim(0.6, 3.8)
    ax.axis("off")

# (a) 变形前
a1.add_patch(Rectangle((1.5, 1.2), 6.0, 1.6, fc="#eef2f7", ec=BLUE))
for xx in np.linspace(1.5, 7.5, 7):
    a1.plot([xx, xx], [1.2, 2.8], color=BLUE, lw=0.9)
for yy in np.linspace(1.5, 2.5, 3):
    a1.plot([1.5, 7.5], [yy, yy], color=GREY, lw=0.7, ls=":")
a1.text(4.5, 3.35, "(a) 变形前：横截面是平面", ha="center", fontsize=10, weight="bold")

# (b) 变形后（沿轴向拉长，横截面仍为平面）
a2.add_patch(Rectangle((1.5, 1.2), 8.2, 1.6, fc="#e7f6e7", ec=GREEN))
for xx in np.linspace(1.5, 9.7, 7):
    a2.plot([xx, xx], [1.2, 2.8], color=GREEN, lw=0.9)
for yy in np.linspace(1.5, 2.5, 3):
    a2.plot([1.5, 9.7], [yy, yy], color=GREY, lw=0.7, ls=":")
a2.text(5.6, 3.35, "(b) 变形后：拉长，横截面仍是平面", ha="center", fontsize=10, weight="bold")

savefig(fig, "lec02_fig2_plane_assumption")


# ---------------------------------------------------------------------
print()
print("=== 图 3：斜截面应力 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.0))

# (a) 几何：横截面（竖直线）与斜截面（与竖直线成 alpha 角）
a1.set_xlim(0.4, 7.0)
a1.set_ylim(0.6, 4.6)
a1.axis("off")
a1.add_patch(Rectangle((1.0, 2.0), 5.4, 2.0, fc="#f4f7fb", ec=BLUE, lw=1.0))
# 横截面（竖直线）
a1.plot([3.2, 3.2], [1.8, 4.2], color=GREY, ls="--", lw=1.6)
a1.text(2.55, 4.3, "横截面", ha="center", fontsize=9.5, color=GREY)
# 斜截面
a1.plot([2.6, 3.9], [2.0, 4.0], color=RED, lw=2.0)
a1.text(3.85, 4.15, "斜截面", ha="left", fontsize=9.5, color=RED)
# 夹角 arc（两线交点约 (3.2, 2.923)）
a1.add_patch(Arc((3.2, 2.923), 1.3, 1.3, theta1=57, theta2=90, color=GREEN, lw=1.6))
a1.text(3.42, 3.12, "alpha", fontsize=10, color=GREEN)
# 斜截面上的应力方向示意（M 为斜线上一点）
mx, my = 3.25, 3.0
a1.annotate("", xy=(mx + 0.84, my - 0.55), xytext=(mx, my),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
a1.text(mx + 1.0, my - 0.78, "sigma_a", fontsize=10, color=RED)
a1.annotate("", xy=(mx + 0.44, my + 0.67), xytext=(mx, my),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
a1.text(mx + 0.5, my + 0.8, "tau_a", fontsize=10, color=GREEN)
a1.text(3.7, 1.15, "(a) 斜截面与横截面成 alpha 角", ha="center", fontsize=10, weight="bold")

# (b) sigma_a、tau_a 随 alpha 的变化曲线
deg = np.linspace(0, 180, 361)
a = np.deg2rad(deg)
a2.plot(deg, 100 * np.cos(a) ** 2, color=RED, lw=2, label="sigma_a = sigma*cos^2(alpha)")
a2.plot(deg, 50 * np.sin(2 * a), color=GREEN, lw=2, label="tau_a = (sigma/2)*sin(2 alpha)")
a2.axhline(0, color=GREY, lw=0.8)
a2.axvline(45, color=GREY, ls=":", lw=1)
a2.plot([45], [50], "o", color=GREEN, ms=6)
a2.text(47, 52, "tau_max = sigma/2\n(alpha = 45 deg)", fontsize=9, color=GREEN)
a2.plot([0], [100], "o", color=RED, ms=6)
a2.text(3, 92, "sigma_max = sigma\n(alpha = 0)", fontsize=9, color=RED)
a2.set_xlim(0, 180)
a2.set_ylim(-60, 115)
a2.set_xlabel("alpha / deg", fontsize=10)
a2.set_ylabel("应力 / MPa（取 sigma = 100 MPa）", fontsize=10)
a2.set_title("(b) 斜截面应力随角度变化", fontsize=10.5, weight="bold")
a2.legend(fontsize=8.5, loc="lower center")

savefig(fig, "lec02_fig3_inclined_stress")

print()
print("[DONE] 第 02 讲数字核对与三张图全部完成。")
