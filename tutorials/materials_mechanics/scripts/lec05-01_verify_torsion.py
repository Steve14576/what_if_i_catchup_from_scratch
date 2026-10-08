# =====================================================================
# lec05-01 第 05 讲《扭转的内力与应力》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 外力偶矩 M = 9550 P/n（kW、r/min -> N·m）
#   EXP2 扭矩图（三外力偶矩；某段扭矩 = 一侧外力偶矩代数和；突变 = 该处外力偶矩）
#   EXP3 极惯性矩、抗扭截面系数与最大切应力 tau_max = T/W_t
#   EXP4 剪切胡克定律 tau=G*gamma：表面切应变 gamma_max = tau_max/G；tau_rho 线性
# 出图（编号按正文出现顺序）：
#   lec05_fig1_torque_diagram   外扭矩与扭矩图
#   lec05_fig2_deformation      圆轴扭转变形假设与切应变
#   lec05_fig3_stress_dist      切应力沿半径线性分布
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc

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
print("=== 数字核对：第 05 讲 ===")

# EXP1 外力偶矩
P_kw, n_rpm = 15.0, 300.0
M1_ext = 9550.0 * P_kw / n_rpm
print("  EXP1 外力偶矩：P=%.0f kW, n=%.0f r/min -> M = 9550P/n = %.1f N·m" % (P_kw, n_rpm, M1_ext))

# EXP2 扭矩图（三个外力偶矩：输入 800、输出 500、输出 300，平衡）
M_in, M_out2, M_out3 = 800.0, 500.0, 300.0
print("  EXP2 外力偶矩平衡：输入 - 输出 = %.1f - %.1f - %.1f = %.1f（应为 0）"
      % (M_in, M_out2, M_out3, M_in - M_out2 - M_out3))
T_left = M_in
T_right = M_in - M_out2
print("        扭矩：左段 T = %.1f N·m；右段 T = %.1f N·m" % (T_left, T_right))
print("        突变 = T左 - T右 = %.1f N·m = 该处外力偶矩 %.1f N·m" % (T_left - T_right, M_out2))

# EXP3 截面几何量与最大切应力
d = 50.0
I_p = np.pi * d ** 4 / 32.0
W_t = np.pi * d ** 3 / 16.0
T_max = T_left
tau_max = T_max * 1e3 / W_t
print("  EXP3 圆轴 d=%.0f mm：I_p = pi*d^4/32 = %.0f mm^4；W_t = pi*d^3/16 = %.1f mm^3" % (d, I_p, W_t))
print("        tau_max = T/W_t = %.1f N·m / %.1f mm^3 = %.1f MPa" % (T_max, W_t, tau_max))

# EXP4 剪切胡克定律与线性分布
G = 80.0e3
gamma_max = tau_max / G
R = d / 2.0
print("  EXP4 剪切胡克定律 tau=G*gamma（G=%.0f MPa）：" % G)
print("        表面切应变 gamma_max = tau_max/G = %.3e" % gamma_max)
for rho in [0.0, R / 2, R]:
    tau_rho = T_max * 1e3 * rho / I_p
    print("        rho = %5.2f mm -> tau_rho = T*rho/I_p = %6.2f MPa" % (rho, tau_rho))
print("        核对：rho=R 处 tau_rho = %.2f MPa，与 tau_max = %.2f MPa 一致" % (T_max * 1e3 * R / I_p, tau_max))


# ---------------------------------------------------------------------
print()
print("=== 图 1：外扭矩与扭矩图 ===")
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.6, 5.6),
                             gridspec_kw={"height_ratios": [1.0, 1.25]})

# (a) 轴与外力偶矩（用弯箭头表示力偶矩）
a1.set_xlim(0, 11)
a1.set_ylim(-1.2, 3.0)
a1.axis("off")
a1.add_patch(Rectangle((1.0, 0.6), 9.0, 0.7, fc="#cfe3f7", ec=BLUE))
a1.plot([5.0, 5.0], [-0.2, 1.4], color=GREY, ls=":", lw=1.2)
# M1 输入（左端，逆时针）
a1.annotate("", xy=(1.0, 1.9), xytext=(2.0, 1.9),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2, connectionstyle="arc3,rad=0.7"))
a1.text(1.5, 2.5, r"$M_1=800$（输入）", ha="center", fontsize=9, color=RED)
# M2 输出（中间，顺时针）
a1.annotate("", xy=(6.0, 1.9), xytext=(4.0, 1.9),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2, connectionstyle="arc3,rad=-0.7"))
a1.text(5.0, 2.5, r"$M_2=500$（输出）", ha="center", fontsize=9, color=GREEN)
# M3 输出（右端，顺时针）
a1.annotate("", xy=(8.6, 1.9), xytext=(9.6, 1.9),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2, connectionstyle="arc3,rad=0.7"))
a1.text(9.1, 2.5, r"$M_3=300$（输出）", ha="center", fontsize=9, color=GREEN)
a1.text(5.5, -0.9, "(a) 传动轴上的三处外力偶矩（单位 N·m；弯箭头表示力偶矩）", ha="center", fontsize=10, weight="bold")

# (b) 扭矩图
a2.axhline(0, color=GREY, lw=1)
a2.fill_between([1, 5], 0, T_left, step="post", color="#d7f0d7", alpha=0.8)
a2.fill_between([5, 10], 0, T_right, step="post", color="#fde9d9", alpha=0.8)
a2.plot([1, 5], [T_left, T_left], color=GREEN, lw=2.4)
a2.plot([5, 10], [T_right, T_right], color=RED, lw=2.4)
a2.plot([5, 5], [T_left, T_right], color=GREY, ls="--", lw=1.4)
a2.plot([1, 5], [T_left, T_left], "o", color=GREEN, ms=5)
a2.plot([5, 10], [T_right, T_right], "o", color=RED, ms=5)
a2.text(3.0, T_left + 40, r"$T = 800$ N·m", ha="center", fontsize=10, color=GREEN)
a2.text(7.5, T_right - 120, r"$T = 300$ N·m", ha="center", fontsize=10, color=RED)
a2.annotate(r"突变 = $M_2$", xy=(5, 550), xytext=(5.6, 640), fontsize=9.5, color=GREY,
            arrowprops=dict(arrowstyle="->", color=GREY, lw=1))
a2.set_xlim(0, 11)
a2.set_ylim(-100, 950)
a2.set_xlabel("截面位置 x", fontsize=10)
a2.set_ylabel(r"扭矩 $T$ / (N·m)", fontsize=10)
a2.set_title("(b) 扭矩图：截面一侧外力偶矩的代数和；集中力偶处跳变", fontsize=10.5, weight="bold")
a2.set_xticks([1, 5, 10])
a2.set_xticklabels(["左端", r"$M_2$", "右端"], fontsize=9)
savefig(fig, "lec05_fig1_torque_diagram")


# ---------------------------------------------------------------------
print()
print("=== 图 2：圆轴扭转变形假设 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 3.8))

# (a) 横截面保持平面、半径保持直线（端面相对转过角 phi）
a1.set_xlim(0, 10)
a1.set_ylim(0, 6)
a1.axis("off")
a1.add_patch(Circle((2.2, 3.0), 1.3, fc="none", ec=BLUE, lw=1.6))
a1.add_patch(Circle((7.8, 3.0), 1.3, fc="none", ec=BLUE, lw=1.6))
a1.plot([2.2, 7.8], [4.3, 4.3], color=BLUE, lw=1.2)
a1.plot([2.2, 7.8], [1.7, 1.7], color=BLUE, lw=1.2)
a1.plot([2.2, 2.2], [3.0, 4.3], color=GREEN, lw=2)          # 左端半径（竖直）
a1.plot([7.8, 7.8 + 1.3 * np.sin(np.deg2rad(50))], [3.0, 3.0 + 1.3 * np.cos(np.deg2rad(50))],
        color=RED, lw=2)                                     # 右端半径（转 phi）
a1.add_patch(Arc((7.8, 3.0), 2.0, 2.0, theta1=40, theta2=90, color=ORANGE, lw=1.4))
a1.text(8.7, 3.6, r"$\varphi$", fontsize=11, color=ORANGE)
a1.text(5.0, 5.4, "(a) 横截面保持平面、半径保持直线", ha="center", fontsize=9.5, weight="bold")
a1.text(2.2, 1.2, "左端面", ha="center", fontsize=8.5, color=GREY)
a1.text(7.8, 1.2, "右端面", ha="center", fontsize=8.5, color=GREY)

# (b) 外表面纵线由直线变斜线：切应变 gamma
a2.set_xlim(0, 10)
a2.set_ylim(0, 6)
a2.axis("off")
a2.add_patch(Rectangle((2.0, 1.3), 6.0, 3.2, fc="#eef2f7", ec=GREY))
a2.plot([3.5, 3.5], [1.3, 3.2], color=GREY, ls="--", lw=1.4)          # 变形前纵线
a2.plot([3.5, 5.2], [1.3, 4.5], color=RED, lw=2)                       # 变形后纵线（倾斜）
a2.add_patch(Arc((3.5, 1.3), 1.0, 1.0, theta1=0, theta2=38, color=GREEN, lw=1.4))
a2.text(4.2, 1.55, r"$\gamma$", fontsize=10, color=GREEN)
a2.text(5.0, 5.4, r"(b) 外表面纵线的倾角 = 切应变 $\gamma$", ha="center", fontsize=9.5, weight="bold")
a2.text(5.0, 0.6, r"$\gamma = \rho\,\frac{\mathrm{d}\varphi}{\mathrm{d}x}$", ha="center", fontsize=10, color=BLUE)
savefig(fig, "lec05_fig2_deformation")


# ---------------------------------------------------------------------
print()
print("=== 图 3：切应力沿半径线性分布 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.0))

# (a) 横截面上的切应力（箭头沿切向，长度随 rho 线性增长）
a1.set_xlim(-3, 3)
a1.set_ylim(-3, 3)
a1.set_aspect("equal")
a1.axis("off")
a1.add_patch(Circle((0, 0), 2.5, fc="#eef2f7", ec=BLUE))
for rho in [0.5, 1.2, 1.9, 2.45]:
    ang = np.deg2rad(70)
    x0, y0 = rho * np.cos(ang), rho * np.sin(ang)
    dx, dy = -np.sin(ang), np.cos(ang)
    ln = 0.35 + 0.55 * rho
    a1.annotate("", xy=(x0 + ln * dx, y0 + ln * dy), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))
a1.text(0, -2.9, "(a) 切应力沿切向，越靠外越大", ha="center", fontsize=9.5, weight="bold")
a1.text(0, 0.0, "横截面", ha="center", va="center", fontsize=9, color=GREY)

# (b) tau_rho 随 rho 线性
rho = np.linspace(0, R, 50)
tau = T_max * 1e3 * rho / I_p
a2.plot(rho, tau, color=BLUE, lw=2.4)
a2.plot([R], [tau_max], "o", color=RED, ms=6)
a2.text(R * 0.5, tau_max * 0.55, r"$\tau_\rho = \dfrac{T\rho}{I_p}$", fontsize=10, color=BLUE)
a2.text(R * 0.62, tau_max * 1.03, r"$\tau_{\max}$（$\rho=R$）", fontsize=9, color=RED)
a2.set_xlim(0, R * 1.15)
a2.set_ylim(0, tau_max * 1.2)
a2.set_xlabel(r"到轴心的距离 $\rho$ / mm", fontsize=10)
a2.set_ylabel(r"切应力 $\tau$ / MPa", fontsize=10)
a2.set_title("(b) 切应力沿半径线性分布", fontsize=10.5, weight="bold")
savefig(fig, "lec05_fig3_stress_dist")

print()
print("[DONE] 第 05 讲数字核对与三张图全部完成。")
