# =====================================================================
# lec06-01 第 06 讲《圆轴扭转的变形与强度刚度设计》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 扭转变形：phi = T*L/(G*I_p)；单位长度扭转角 theta = phi/L（度/米）
#   EXP2 强度条件设计：W_t >= T/[tau] -> d
#   EXP3 刚度条件设计：I_p >= T/(G*[theta]) -> d；与强度比，判控制条件
#   EXP4 空心轴 vs 实心轴：同外径的 W_t/A 材料利用率；同 W_t 时的省料比
#   EXP5 非圆截面扭转（认识层）：同面积的圆 vs 方，W_t 对照
# 出图（编号按正文出现顺序）：
#   lec06_fig1_twist_deformation  扭转变形与扭转角
#   lec06_fig2_hollow_vs_solid    空心轴 vs 实心轴
#   lec06_fig3_noncircular        非圆截面扭转（认识层）
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc, Wedge

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
print("=== 数字核对：第 06 讲 ===")

G = 80.0e3          # MPa
d = 50.0            # mm
T = 800.0e3         # N·mm
L = 1000.0          # mm
I_p = np.pi * d ** 4 / 32.0
W_t = np.pi * d ** 3 / 16.0
phi = T * L / (G * I_p)                      # rad
phi_deg = np.rad2deg(phi)
theta_per_m = phi / L * 1000.0 * 180.0 / np.pi   # deg/m
print("  EXP1 扭转变形（G=%.0f MPa, d=%.0f mm, T=%.1f N·m, L=%.0f mm）：" % (G, d, T / 1e3, L))
print("        I_p = %.0f mm^4；phi = T*L/(G*I_p) = %.5f rad = %.4f deg" % (I_p, phi, phi_deg))
print("        单位长度扭转角 theta = %.4f deg/m" % theta_per_m)

tau_allow = 40.0        # MPa
d_strength = (16.0 * (T / tau_allow) / np.pi) ** (1.0 / 3.0)
print("  EXP2 强度条件（[tau]=%.0f MPa）：W_t >= T/[tau] = %.1f mm^3 -> d >= %.1f mm"
      % (tau_allow, T / tau_allow, d_strength))

theta_allow_m = 0.5     # deg/m
theta_allow = np.deg2rad(theta_allow_m) / 1000.0   # rad/mm
I_req = T / (G * theta_allow)
d_stiff = (32.0 * I_req / np.pi) ** 0.25
print("  EXP3 刚度条件（[theta]=%.1f deg/m）：I_p >= T/(G*[theta]) = %.0f mm^4 -> d >= %.1f mm"
      % (theta_allow_m, I_req, d_stiff))
print("        控制条件 = %s（%.1f vs %.1f mm，取大者）"
      % ("刚度" if d_stiff > d_strength else "强度", d_stiff, d_strength))

# EXP4 空心 vs 实心（同外径 D=50, 内径 d0=40, 即 alpha=0.8）
D0, di = 50.0, 40.0
alpha = di / D0
I_ho = np.pi * (D0 ** 4 - di ** 4) / 32.0
W_ho = I_ho / (D0 / 2.0)
A_so = np.pi / 4.0 * D0 ** 2
A_ho = np.pi / 4.0 * (D0 ** 2 - di ** 2)
print("  EXP4 空心 vs 实心（同外径 D=%.0f, 空心内径 d0=%.0f, alpha=%.1f）：" % (D0, di, alpha))
print("        实心：A=%.0f mm^2, W_t=%.0f mm^3, W_t/A=%.2f" % (A_so, W_t, W_t / A_so))
print("        空心：A=%.0f mm^2, W_t=%.0f mm^3, W_t/A=%.2f" % (A_ho, W_ho, W_ho / A_ho))
print("        单位面积抗扭：空心/实心 = %.2f（空心更省料）" % ((W_ho / A_ho) / (W_t / A_so)))
# 同 W_t 时空心所需外径与用料
D_eq = (W_t * 16.0 / (np.pi * (1.0 - alpha ** 4))) ** (1.0 / 3.0)
A_eq = np.pi / 4.0 * D_eq ** 2 * (1.0 - alpha ** 2)
print("        同 W_t=%.0f：空心需 D=%.1f mm，用料 %.0f mm^2，为实心的 %.1f%%（省 %.1f%%）"
      % (W_t, D_eq, A_eq, A_eq / A_so * 100.0, (1 - A_eq / A_so) * 100.0))

# EXP5 非圆截面（认识层）：同面积的圆 vs 方
a_sq = np.sqrt(A_so)
W_sq = 0.208 * a_sq ** 3
print("  EXP5 非圆截面（认识层）：同面积 A=%.0f mm^2 下，圆 W_t=%.0f；方(边长%.1f) W_t~%.0f"
      % (A_so, W_t, a_sq, W_sq))
print("        圆形抗扭能力约为方形 %.2f 倍（圆形截面抗扭最优）" % (W_t / W_sq))


# ---------------------------------------------------------------------
print()
print("=== 图 1：扭转变形与扭转角 ===")
fig, ax = plt.subplots(figsize=(9.6, 4.2))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5)
ax.axis("off")
# 轴
ax.add_patch(Rectangle((2.0, 1.8), 7.5, 1.2, fc="#cfe3f7", ec=BLUE))
# 左端固定（斜线）
ax.plot([2.0, 2.0], [1.6, 3.2], color=GREY, lw=2)
for yy in np.arange(1.6, 3.3, 0.3):
    ax.plot([2.0, 1.7], [yy, yy - 0.22], color=GREY, lw=1)
# 右端外力偶矩（弯箭头）
ax.annotate("", xy=(9.3, 2.9), xytext=(9.9, 2.9),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2, connectionstyle="arc3,rad=-0.7"))
ax.text(9.9, 3.25, r"$T$", fontsize=12, color=RED)
# 左端面半径（竖直）与右端面半径（转过 phi）
ax.plot([2.0, 2.0], [2.4, 3.0], color=GREEN, lw=2)
ax.plot([9.5, 9.5 + 0.6 * np.sin(np.deg2rad(55))], [2.4, 2.4 + 0.6 * np.cos(np.deg2rad(55))],
        color=ORANGE, lw=2)
ax.add_patch(Arc((9.5, 2.4), 1.2, 1.2, theta1=35, theta2=90, color=RED, lw=1.4))
ax.text(10.0, 2.55, r"$\varphi$", fontsize=12, color=RED)
# L 与公式
ax.annotate("", xy=(2.0, 3.6), xytext=(9.5, 3.6),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.2))
ax.text(5.75, 3.75, r"$L$", ha="center", fontsize=12, color=GREY)
ax.text(6.0, 1.0, r"$\varphi = \dfrac{T L}{G I_p}$（扭转角）；$\theta = \dfrac{\varphi}{L} = \dfrac{T}{G I_p}$（单位长度扭转角）",
        ha="center", fontsize=12, color=BLUE)
ax.text(6.0, 4.5, r"圆轴扭转：右端面相对左端面转过角 $\varphi$", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec06_fig1_twist_deformation")


# ---------------------------------------------------------------------
print()
print("=== 图 2：空心轴 vs 实心轴 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.2))

# (a) 截面：实心圆 与 空心圆环
a1.set_xlim(0, 10)
a1.set_ylim(0, 5)
a1.set_aspect("equal")
a1.axis("off")
a1.add_patch(Circle((2.6, 2.6), 1.6, fc="#cfe3f7", ec=BLUE))
a1.text(2.6, 0.6, r"实心：$D$", ha="center", fontsize=10)
a1.add_patch(Circle((7.4, 2.6), 1.6, fc="#e7f0fb", ec=BLUE))
a1.add_patch(Circle((7.4, 2.6), 1.28, fc="white", ec=BLUE))
a1.text(7.4, 0.6, r"空心：$D$、$d_0$", ha="center", fontsize=10)
a1.text(5.0, 4.6, "(a) 同外径下，空心把轴心低应力材料移到外缘", ha="center", fontsize=10, weight="bold")

# (b) 材料利用率柱状：W_t/A（同外径）
labels = [r"实心", r"空心($\alpha$=0.8)"]
vals = [W_t / A_so, W_ho / A_ho]
bars = a2.bar([0, 1], vals, color=[BLUE, ORANGE], width=0.5)
a2.set_xticks([0, 1])
a2.set_xticklabels(labels, fontsize=10)
a2.set_ylabel(r"单位面积抗扭 $W_t/A$ / (mm)", fontsize=10)
a2.set_title(r"(b) 材料利用率：空心更高", fontsize=10.5, weight="bold")
for i, v in enumerate(vals):
    a2.text(i, v + 0.4, "%.1f" % v, ha="center", fontsize=10)
a2.set_ylim(0, max(vals) * 1.25)
savefig(fig, "lec06_fig2_hollow_vs_solid")


# ---------------------------------------------------------------------
print()
print("=== 图 3：非圆截面扭转（认识层）===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.2))

# (a) 矩形截面扭转后翘曲（示意）
a1.set_xlim(0, 10)
a1.set_ylim(0, 5)
a1.axis("off")
a1.add_patch(Rectangle((2.0, 1.6), 6.0, 2.2, fc="#eef2f7", ec=GREY, ls="--"))
xs = np.linspace(2.0, 8.0, 100)
ys = 1.6 + 2.2 + 0.25 * np.sin(np.pi * (xs - 2.0) / 6.0)
a1.plot(xs, ys, color=BLUE, lw=2)
a1.text(5.0, 4.3, "实线：翘曲后的截面（不再是平面）", ha="center", fontsize=9.5, color=BLUE)
a1.text(5.0, 1.0, "虚线：变形前的平面", ha="center", fontsize=9.5, color=GREY)
a1.text(5.0, 4.8, "(a) 非圆截面扭转后发生翘曲", ha="center", fontsize=10, weight="bold")

# (b) 同面积：圆 vs 方 的 W_t
labels = ["圆（d=50）", "方（a=44.3）"]
vals = [W_t, W_sq]
a2.bar([0, 1], vals, color=[BLUE, GREEN], width=0.5)
a2.set_xticks([0, 1])
a2.set_xticklabels(labels, fontsize=10)
a2.set_ylabel(r"抗扭截面系数 $W_t$ / mm$^3$", fontsize=10)
a2.set_title(r"(b) 同面积下，圆形抗扭最优", fontsize=10.5, weight="bold")
for i, v in enumerate(vals):
    a2.text(i, v + 400, "%.0f" % v, ha="center", fontsize=10)
a2.set_ylim(0, max(vals) * 1.25)
savefig(fig, "lec06_fig3_noncircular")

print()
print("[DONE] 第 06 讲数字核对与三张图全部完成。")
