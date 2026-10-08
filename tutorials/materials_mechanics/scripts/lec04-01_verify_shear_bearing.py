# =====================================================================
# lec04-01 第 04 讲《剪切与挤压的实用计算》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 铆钉剪切（单剪）：tau = F/A_s，A_s = pi*d^2/4
#   EXP2 铆钉挤压：sigma_bs = F/A_bs，A_bs = d*t（圆柱面投影）
#   EXP3 双剪（双盖板）：剪切面数 2，A_s = 2*pi*d^2/4
#   EXP4 平键：F = T/(d/2)；剪切面 A=b*l，挤压面 A=l*(h/2)
# 出图（编号按正文出现顺序）：
#   lec04_fig1_shear_bearing   搭接铆钉：剪切面与挤压面
#   lec04_fig2_single_double    单剪与双剪（剪切面数）
#   lec04_fig3_key             平键连接：剪切面与挤压面
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc, Polygon

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
print("=== 数字核对：第 04 讲 ===")

d = 16.0          # mm 铆钉直径
t = 10.0          # mm 板厚
Fs = 20.0e3       # N 单个剪力（搭接，单剪）

A_s = np.pi * d ** 2 / 4.0
tau = Fs / A_s
print("  EXP1 铆钉剪切（单剪）：d=%.0f mm -> A_s = pi*d^2/4 = %.2f mm^2" % (d, A_s))
print("        tau = F/A_s = %.0f N / %.2f mm^2 = %.1f MPa" % (Fs, A_s, tau))

A_bs = d * t
sig_bs = Fs / A_bs
print("  EXP2 铆钉挤压：A_bs = d*t = %.0f*%.0f = %.0f mm^2" % (d, t, A_bs))
print("        sigma_bs = F/A_bs = %.1f MPa" % sig_bs)

Fd = 40.0e3
A_s2 = 2 * A_s
tau2 = Fd / A_s2
print("  EXP3 双剪（双盖板）：剪切面 2 个 -> A_s = 2*%.2f = %.2f mm^2" % (A_s, A_s2))
print("        tau = %.0f N / %.2f mm^2 = %.1f MPa（与单剪同量级：Q 与面数同步翻倍）" % (Fd, A_s2, tau2))

# EXP4 平键
b, h, l = 12.0, 8.0, 50.0     # mm
D = 40.0                       # mm 轴径
T = 400.0                      # N·m 扭矩
Fk = T / (D / 2.0 / 1000.0)    # N （D/2 换算成 m）
A_k_shear = b * l
A_k_bs = l * (h / 2.0)
print("  EXP4 平键（b=%.0f, h=%.0f, l=%.0f mm；轴径 D=%.0f mm；T=%.0f N·m）：" % (b, h, l, D, T))
print("        键受力 F = T/(D/2) = %.0f N" % Fk)
print("        剪切面 A = b*l = %.0f mm^2 -> tau = %.1f MPa" % (A_k_shear, Fk / A_k_shear))
print("        挤压面 A = l*(h/2) = %.0f mm^2 -> sigma_bs = %.1f MPa" % (A_k_bs, Fk / A_k_bs))


# ---------------------------------------------------------------------
print()
print("=== 图 1：搭接铆钉的剪切面与挤压面 ===")
fig, ax = plt.subplots(figsize=(9.6, 4.6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis("off")

# 上板（左伸入）与下板（右伸入）
ax.add_patch(Rectangle((1.0, 3.1), 5.6, 0.7, fc="#cfe3f7", ec=BLUE))
ax.add_patch(Rectangle((4.6, 2.4), 6.0, 0.7, fc="#e7f0fb", ec=BLUE))
ax.text(2.0, 3.55, "上板", ha="center", fontsize=10, color=BLUE)
ax.text(9.0, 2.75, "下板", ha="center", fontsize=10, color=BLUE)

# 铆钉（跨在两板交界处）
ax.add_patch(Circle((5.4, 3.1), 0.34, fc="#fde9d9", ec=ORANGE))
ax.text(6.05, 3.5, "铆钉 d", fontsize=9.5, color=ORANGE)

# 两板外拉力
ax.annotate("", xy=(0.2, 3.45), xytext=(1.0, 3.45),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.annotate("", xy=(11.8, 2.75), xytext=(10.6, 2.75),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(0.5, 3.85, "F", fontsize=12, color=RED)
ax.text(11.2, 3.15, "F", fontsize=12, color=RED)

# 剪切面：两板交界面处，穿过铆钉（水平）
ax.plot([4.6, 6.2], [3.1, 3.1], color=GREEN, lw=2.6)
ax.annotate("剪切面（单剪，铆钉被上下两板错动剪开）", xy=(5.4, 3.1), xytext=(1.4, 4.9),
            fontsize=9.5, color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN, lw=1))

# 挤压面：铆钉与孔壁的接触（投影 d*t）
ax.annotate("挤压面（铆钉与孔壁接触，投影面积 = d x t）", xy=(5.74, 3.1), xytext=(6.6, 5.0),
            fontsize=9.5, color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1))
ax.text(4.6, 4.1, "t（板厚）", fontsize=9, color=GREY)
ax.plot([6.6, 6.6], [3.1, 3.8], color=GREY, lw=0.8)
ax.plot([6.6, 6.6], [2.4, 3.1], color=GREY, lw=0.8)

ax.text(6.0, 0.7, "搭接接头：铆钉同时受「剪切」（截面被剪开）与「挤压」（孔壁被压）",
        ha="center", fontsize=10, weight="bold")
savefig(fig, "lec04_fig1_shear_bearing")


# ---------------------------------------------------------------------
print()
print("=== 图 2：单剪与双剪 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.0))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

# (a) 单剪：两板搭接，1 个剪切面
a1.add_patch(Rectangle((0.8, 3.2), 4.4, 0.6, fc="#cfe3f7", ec=BLUE))
a1.add_patch(Rectangle((3.6, 2.6), 4.4, 0.6, fc="#e7f0fb", ec=BLUE))
a1.add_patch(Circle((4.2, 3.2), 0.3, fc="#fde9d9", ec=ORANGE))
a1.plot([3.6, 4.8], [3.2, 3.2], color=GREEN, lw=2.4)
a1.text(2.5, 4.15, "剪切面 x 1", fontsize=9.5, color=GREEN)
a1.text(5.0, 1.7, "(a) 单剪：2 板搭接，1 个剪切面", ha="center", fontsize=10, weight="bold")

# (b) 双剪：双盖板夹中间板，2 个剪切面
a2.add_patch(Rectangle((1.2, 3.9), 6.0, 0.5, fc="#cfe3f7", ec=BLUE))   # 上盖板
a2.add_patch(Rectangle((1.2, 3.0), 6.0, 0.9, fc="#fde9d9", ec=ORANGE)) # 主板
a2.add_patch(Rectangle((1.2, 2.1), 6.0, 0.5, fc="#cfe3f7", ec=BLUE))   # 下盖板
a2.add_patch(Circle((4.2, 3.2), 0.32, fc="#eef2f7", ec=GREY))
a2.plot([3.5, 4.9], [3.9, 3.9], color=GREEN, lw=2.4)
a2.plot([3.5, 4.9], [3.0, 3.0], color=GREEN, lw=2.4)
a2.text(5.1, 4.6, "剪切面 x 2", fontsize=9.5, color=GREEN)
a2.text(4.2, 1.3, "(b) 双剪：双盖板夹主板，2 个剪切面", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec04_fig2_single_double")


# ---------------------------------------------------------------------
print()
print("=== 图 3：平键连接 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.2))

# (a) 端面视图：轴、键、轮毂
a1.set_xlim(0, 8)
a1.set_ylim(0, 8)
a1.axis("off")
a1.add_patch(Circle((4, 4), 2.4, fc="#eef2f7", ec=GREY))        # 轮毂外圆
a1.add_patch(Circle((4, 4), 2.0, fc="#e7f0fb", ec=BLUE))        # 轴
a1.add_patch(Rectangle((3.7, 5.9), 0.6, 0.7, fc="#fde9d9", ec=ORANGE))  # 键
a1.text(4.8, 6.25, "键", fontsize=10, color=ORANGE)
a1.text(6.6, 4.0, "轮毂", fontsize=9.5, color=GREY)
a1.text(4.0, 1.4, "(a) 端面：轴-键-轮毂", ha="center", fontsize=10, weight="bold")

# (b) 键的受载与两个面（侧视）
a2.set_xlim(0, 12)
a2.set_ylim(0, 6)
a2.axis("off")
a2.add_patch(Rectangle((1.5, 1.8), 7.0, 0.7, fc="#e7f0fb", ec=BLUE))   # 轴顶
a2.add_patch(Rectangle((4.0, 2.5), 4.0, 1.0, fc="#fde9d9", ec=ORANGE)) # 键（长 l）
a2.add_patch(Rectangle((1.5, 3.5), 7.0, 0.7, fc="#eef2f7", ec=GREY))   # 轮毂底
a2.plot([4.0, 8.0], [3.0, 3.0], color=GREEN, lw=2.4)                   # 剪切面（b x l）
a2.annotate("", xy=(9.2, 3.0), xytext=(8.0, 3.0),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a2.text(9.3, 3.0, "F", fontsize=12, color=RED, va="center")
a2.text(5.0, 3.15, "剪切面 = b x l", fontsize=9, color=GREEN)
a2.annotate("挤压面 = l x (h/2)", xy=(4.0, 3.0), xytext=(1.3, 5.0),
            fontsize=9, color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1))
a2.text(6.0, 1.2, "(b) 键：受圆周力 F；沿 b x l 面剪切，沿侧面 (h/2) 挤压",
        ha="center", fontsize=10, weight="bold")
savefig(fig, "lec04_fig3_key")

print()
print("[DONE] 第 04 讲数字核对与三张图全部完成。")
