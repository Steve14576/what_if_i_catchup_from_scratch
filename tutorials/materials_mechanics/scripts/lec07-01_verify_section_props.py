# =====================================================================
# lec07-01 第 07 讲《截面的几何性质》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 矩形：形心与惯性矩 I_z=bh^3/12、抗弯截面系数 W
#   EXP2 平行移轴定理：以底边为轴 I=bh^3/3，验证 = bh^3/12+(h/2)^2*A
#   EXP3 组合截面（T 形分两块）：形心 y_c 与 I_zc、上/下 W
#   EXP4 圆与圆环：I=pi d^4/64、I_p=2I
#   EXP5 极惯性矩与惯性矩关系 I_p=I_z+I_y（圆：I_z=I_y）
# 出图（编号按正文出现顺序）：
#   lec07_fig1_centroid       形心、静矩与参考轴
#   lec07_fig2_parallel_axis  平行移轴定理
#   lec07_fig3_composite      组合截面分块计算（T 形）
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

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
print("=== 数字核对：第 07 讲 ===")

# EXP1 矩形
b, h = 60.0, 100.0
A = b * h
y_c = h / 2.0
I_zc = b * h ** 3 / 12.0
W_z = I_zc / (h / 2.0)
print("  EXP1 矩形 b=%.0f, h=%.0f：A=%.0f mm^2；形心 y_c=%.1f mm" % (b, h, A, y_c))
print("        I_zc = b*h^3/12 = %.4e mm^4；W_z = I_zc/(h/2) = %.4e mm^3" % (I_zc, W_z))

# EXP2 平行移轴
I_bottom = b * h ** 3 / 3.0
I_check = I_zc + (h / 2.0) ** 2 * A
print("  EXP2 平行移轴（以底边为轴）：I = b*h^3/3 = %.4e；" % I_bottom)
print("        验证 I_zc+(h/2)^2*A = %.4e + %.4e = %.4e（应相等）" % (I_zc, (h / 2.0) ** 2 * A, I_check))

# EXP3 组合截面 T 形
bf, tf = 120.0, 20.0      # 翼缘
bw, hw = 20.0, 80.0       # 腹板
A1 = bw * hw
y1 = hw / 2.0
A2 = bf * tf
y2 = hw + tf / 2.0
A_tot = A1 + A2
y_cT = (A1 * y1 + A2 * y2) / A_tot
I1 = bw * hw ** 3 / 12.0 + A1 * (y1 - y_cT) ** 2
I2 = bf * tf ** 3 / 12.0 + A2 * (y2 - y_cT) ** 2
I_T = I1 + I2
H_tot = hw + tf
print("  EXP3 组合截面 T 形（腹板 %gx%g，翼缘 %gx%g）：" % (bw, hw, bf, tf))
print("        分块1(腹板)：A=%.0f, y=%.1f；分块2(翼缘)：A=%.0f, y=%.1f" % (A1, y1, A2, y2))
print("        形心 y_c = ΣA_i y_i / ΣA_i = %.1f mm；I_zc = Σ(Ii0+Ai di^2) = %.4e mm^4" % (y_cT, I_T))
print("        W_下 = I/y_c = %.4e mm^3；W_上 = I/(H-y_c) = %.4e mm^3（上大下小，下缘更危险）"
      % (I_T / y_cT, I_T / (H_tot - y_cT)))

# EXP4 圆与圆环
d = 50.0
I_c = np.pi * d ** 4 / 64.0
I_p_c = np.pi * d ** 4 / 32.0
D0, di = 60.0, 40.0
I_ho = np.pi * (D0 ** 4 - di ** 4) / 64.0
I_p_ho = np.pi * (D0 ** 4 - di ** 4) / 32.0
print("  EXP4 圆 d=%.0f：I=pi d^4/64=%.4e；I_p=pi d^4/32=%.4e（=2I）" % (d, I_c, I_p_c))
print("        圆环 D=%.0f,d=%.0f：I=%.4e；I_p=%.4e" % (D0, di, I_ho, I_p_ho))

# EXP5 I_p = I_z + I_y
print("  EXP5 关系核对：I_p = I_z + I_y。圆截面 I_z=I_y=I -> I_p=2I：%.4e = 2*%.4e，偏差 %.2e"
      % (I_p_c, I_c, abs(I_p_c - 2 * I_c)))


# ---------------------------------------------------------------------
print()
print("=== 图 1：形心、静矩与参考轴 ===")
fig, ax = plt.subplots(figsize=(7.6, 5.2))
ax.set_xlim(-15, 135)
ax.set_ylim(-20, 115)
ax.set_aspect("equal")
ax.axis("off")
# T 形
ax.add_patch(Rectangle((0, 80), 120, 20, fc="#cfe3f7", ec=BLUE))
ax.add_patch(Rectangle((50, 0), 20, 80, fc="#cfe3f7", ec=BLUE))
# 参考轴（底边）
ax.plot([-10, 130], [0, 0], color=GREY, lw=1.2)
ax.text(132, 0, "参考轴", fontsize=9, color=GREY, va="center")
# 形心
ax.plot([60], [70], marker="o", color=RED, ms=7)
ax.text(66, 72, r"形心 $C$", fontsize=11, color=RED)
ax.plot([-10, 130], [70, 70], color=GREEN, ls="--", lw=1.2)
ax.text(-14, 70, r"$z$", fontsize=11, color=GREEN, ha="right")
# y_c 标注
ax.annotate("", xy=(15, 0), xytext=(15, 70),
            arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.4))
ax.text(18, 34, r"$y_c$", fontsize=12, color=ORANGE)
ax.text(0, -14, r"静矩 $S_z=\int_A y\,\mathrm{d}A=y_c A$；$y_c=S_z/A$", fontsize=11, color=BLUE)
ax.text(60, 112, "形心是截面的几何中心（面积矩的平衡点）", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec07_fig1_centroid")


# ---------------------------------------------------------------------
print()
print("=== 图 2：平行移轴定理 ===")
fig, ax = plt.subplots(figsize=(7.6, 4.6))
ax.set_xlim(-15, 90)
ax.set_ylim(-30, 120)
ax.set_aspect("equal")
ax.axis("off")
ax.add_patch(Rectangle((0, 0), 60, 100, fc="#cfe3f7", ec=BLUE))
# 形心轴 zc
ax.plot([-10, 70], [50, 50], color=GREEN, lw=1.6)
ax.text(-12, 50, r"$z_c$", fontsize=11, color=GREEN, ha="right", va="center")
ax.plot([30], [50], marker="o", color=RED, ms=6)
# 平行轴 z（距形心轴 a）
ax.plot([-10, 70], [10, 10], color=ORANGE, lw=1.6)
ax.text(-12, 10, r"$z$", fontsize=11, color=ORANGE, ha="right", va="center")
ax.annotate("", xy=(45, 10), xytext=(45, 50),
            arrowprops=dict(arrowstyle="<->", color=RED, lw=1.4))
ax.text(47, 30, r"$a$", fontsize=12, color=RED)
ax.text(30, -20, r"$I_z = I_{z_c} + a^2 A$", ha="center", fontsize=14, color=BLUE)
ax.text(30, 112, "平行移轴：轴越远，惯性矩越大（加 a 平方项）", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec07_fig2_parallel_axis")


# ---------------------------------------------------------------------
print()
print("=== 图 3：组合截面分块计算（T 形）===")
fig, ax = plt.subplots(figsize=(7.6, 5.2))
ax.set_xlim(-15, 135)
ax.set_ylim(-20, 118)
ax.set_aspect("equal")
ax.axis("off")
ax.add_patch(Rectangle((0, 80), 120, 20, fc="#fde9d9", ec=ORANGE))
ax.add_patch(Rectangle((50, 0), 20, 80, fc="#e7f0fb", ec=BLUE))
# 分块标注
ax.text(60, 90, r"分块2：翼缘 $120\times20$", ha="center", fontsize=9.5, color=ORANGE)
ax.text(86, 56, r"分块1：腹板 $20\times80$", ha="left", fontsize=9.5, color=BLUE)
ax.text(86, 46, r"$A_1=1600,\ y_1=40$", ha="left", fontsize=9, color=BLUE)
ax.text(86, 34, r"$A_2=2400,\ y_2=90$", ha="left", fontsize=9, color=ORANGE)
# 形心
ax.plot([60], [70], marker="o", color=RED, ms=7)
ax.plot([-10, 130], [70, 70], color=GREEN, ls="--", lw=1.2)
ax.text(-14, 70, r"$z$", fontsize=11, color=GREEN, ha="right")
ax.text(60, 112, r"组合截面：$y_c=\frac{\sum A_i y_i}{\sum A_i}=70$ mm；$I_z=\sum(I_{i0}+A_i d_i^2)$",
        ha="center", fontsize=9.5, weight="bold")
savefig(fig, "lec07_fig3_composite")

print()
print("[DONE] 第 07 讲数字核对与三张图全部完成。")
