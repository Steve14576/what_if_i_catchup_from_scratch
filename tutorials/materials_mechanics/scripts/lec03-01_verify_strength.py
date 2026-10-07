# =====================================================================
# lec03-01 第 03 讲《拉压变形、材料力学性能与强度计算》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 胡克定律：deltaL = N*L/(E*A)，并与 sigma=E*eps 互证
#   EXP2 横向变形与泊松比：eps' = -mu*eps，直径改变量
#   EXP3 理想化低碳钢拉伸曲线的特征点与许用应力
#   EXP4 强度条件三类问题（校核、设计截面、求许用载荷）
# 出图（编号按正文出现顺序）：
#   lec03_fig1_stress_strain_curve   低碳钢拉伸 sigma-eps 曲线（四阶段 + 特征点）
#   lec03_fig2_hooke_law             胡克定律：杆件伸长与 sigma-eps 线性段
#   lec03_fig3_ductile_vs_brittle    塑性材料与脆性材料的拉压性能对比
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
print("=== 数字核对：第 03 讲 ===")

# EXP1 胡克定律：一根钢杆
N = 20.0e3        # N
L = 500.0         # mm
A = 200.0         # mm^2
E = 2.0e5         # MPa（钢的弹性模量 200 GPa）
dL = N * L / (E * A)
eps = dL / L
sigma = N / A
print("  EXP1 胡克定律（钢杆 N=%.0f kN, L=%.0f mm, A=%.0f mm^2, E=%.0f MPa）：" % (N / 1e3, L, A, E))
print("        deltaL = N*L/(E*A) = %.4f mm；eps = deltaL/L = %.3e" % (dL, eps))
print("        互证：sigma = N/A = %.1f MPa；E*eps = %.1f MPa（应相等）" % (sigma, E * eps))

# EXP2 横向变形与泊松比
mu = 0.30
eps_lat = -mu * eps
d = 20.0          # mm 直径
dd = eps_lat * d
print("  EXP2 横向变形（泊松比 mu = %.2f）：eps' = -mu*eps = %.3e；直径改变 %.5f mm" % (mu, eps_lat, dd))

# EXP3 理想化低碳钢拉伸曲线特征点
sig_p, sig_e, sig_s, sig_b = 200.0, 210.0, 240.0, 400.0   # MPa
print("  EXP3 低碳钢特征应力（理想化值）：比例极限 %.0f、弹性极限 %.0f、屈服极限 %.0f、强度极限 %.0f MPa"
      % (sig_p, sig_e, sig_s, sig_b))
for n in [1.5, 2.0]:
    print("        安全系数 n = %.1f -> 许用应力 [sigma] = sigma_s/n = %.1f MPa" % (n, sig_s / n))

# EXP4 强度条件三类问题（sigma_max = N/A <= [sigma]）
sg_allow = 160.0  # MPa
print("  EXP4 强度条件 sigma_max = N/A <= [sigma]（取 [sigma] = %.0f MPa）：" % sg_allow)
N1, A1 = 30.0e3, 200.0
print("        (校核)   N=%.0f kN, A=%.0f mm^2 -> sigma = %.1f MPa <= %.0f ? %s"
      % (N1 / 1e3, A1, N1 / A1, sg_allow, "安全" if N1 / A1 <= sg_allow else "不合格"))
N2 = 40.0e3
print("        (设计截面) N=%.0f kN -> A >= N/[sigma] = %.1f mm^2" % (N2 / 1e3, N2 / sg_allow))
A3 = 200.0
print("        (求许用载荷) A=%.0f mm^2 -> N <= [sigma]*A = %.1f kN" % (A3, sg_allow * A3 / 1e3))


# ---------------------------------------------------------------------
print()
print("=== 图 1：低碳钢拉伸曲线 ===")
# 理想化分段点（eps 为横坐标，单位 1e-3 便于阅读）
eps_pts = np.array([0.0, 1.0, 1.5, 2.0, 20.0, 60.0, 100.0, 150.0, 175.0, 210.0])
sig_pts = np.array([0.0, 200.0, 210.0, 240.0, 250.0, 300.0, 355.0, 400.0, 392.0, 340.0])
fig, ax = plt.subplots(figsize=(9.6, 5.6))
ax.plot(eps_pts, sig_pts, color=BLUE, lw=2.4)
ax.axhline(0, color=GREY, lw=0.8)
ax.axvline(0, color=GREY, lw=0.8)
ax.fill_betweenx([0, 200], 0, 1.0, color="#e7f0fb", alpha=0.5)
pts = {"p": (1.0, 200.0), "e": (1.5, 210.0), "s": (2.0, 240.0), "b": (150.0, 400.0)}
for key, (xx, yy) in pts.items():
    ax.plot([xx], [yy], "o", color=RED, ms=6)
ax.annotate("比例极限 sigma_p", xy=(1.0, 200.0), xytext=(20, 150),
            fontsize=9.5, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=1))
ax.annotate("弹性极限 sigma_e", xy=(1.5, 210.0), xytext=(20, 230),
            fontsize=9.5, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=1))
ax.annotate("屈服极限 sigma_s", xy=(2.0, 240.0), xytext=(30, 90),
            fontsize=9.5, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=1))
ax.annotate("强度极限 sigma_b", xy=(150.0, 400.0), xytext=(95, 430),
            fontsize=9.5, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=1))
ax.text(6, 185, "(1) 弹性阶段\nsigma = E*eps", fontsize=9, color=BLUE)
ax.text(6, 70, "(2) 屈服阶段\n应力几乎不增、应变猛增", fontsize=9, color=BLUE)
ax.text(70, 210, "(3) 强化阶段", fontsize=9, color=BLUE)
ax.text(168, 250, "(4) 颈缩阶段", fontsize=9, color=BLUE)
ax.annotate("断裂", xy=(210, 340), xytext=(200, 300),
            fontsize=9.5, color=GREY, arrowprops=dict(arrowstyle="->", color=GREY, lw=1))
ax.set_xlim(0, 230)
ax.set_ylim(0, 460)
ax.set_xlabel("线应变 eps（单位 1e-3；断裂处 eps 远大于弹性段）", fontsize=10)
ax.set_ylabel("应力 sigma / MPa", fontsize=10)
ax.set_title("低碳钢拉伸时的应力-应变曲线（示意，特征点为理想化值）", fontsize=11, weight="bold")
savefig(fig, "lec03_fig1_stress_strain_curve")


# ---------------------------------------------------------------------
print()
print("=== 图 2：胡克定律 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 3.6))

# (a) 杆件伸长
a1.set_xlim(0, 10)
a1.set_ylim(0, 4)
a1.axis("off")
a1.add_patch(Rectangle((1.2, 1.6), 6.0, 0.8, fc="#cfe3f7", ec=BLUE))
a1.add_patch(Rectangle((7.2, 1.6), 1.0, 0.8, fc="none", ec=GREEN, ls="--"))
a1.annotate("", xy=(0.3, 2.0), xytext=(1.2, 2.0),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a1.annotate("", xy=(9.2, 2.0), xytext=(8.2, 2.0),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
a1.annotate("", xy=(1.2, 2.75), xytext=(7.2, 2.75),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.2))
a1.text(4.2, 2.85, "原长 L", ha="center", fontsize=10, color=GREY)
a1.annotate("", xy=(7.2, 1.25), xytext=(8.2, 1.25),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.2))
a1.text(8.4, 1.2, "deltaL", ha="left", fontsize=10, color=GREEN)
a1.text(4.5, 0.5, "(a) 杆受轴力 N：伸长 deltaL = N*L/(E*A)（变形已放大）", ha="center", fontsize=9.5, weight="bold")

# (b) sigma-eps 线性段
eps2 = np.linspace(0, 1.0, 50)
a2.plot(eps2, 200.0 * eps2, color=BLUE, lw=2.4)
a2.fill_between(eps2, 0, 200.0 * eps2, color="#e7f0fb", alpha=0.5)
a2.plot([1.0], [200.0], "o", color=RED, ms=6)
a2.text(0.60, 120, "斜率 = E\nsigma = E*eps", fontsize=10, color=BLUE)
a2.text(1.02, 198, "比例极限 sigma_p", fontsize=9, color=RED)
a2.set_xlim(0, 1.35)
a2.set_ylim(0, 260)
a2.set_xlabel("线应变 eps（1e-3）", fontsize=10)
a2.set_ylabel("应力 sigma / MPa", fontsize=10)
a2.set_title("(b) 弹性范围内 sigma 与 eps 成正比", fontsize=10, weight="bold")
savefig(fig, "lec03_fig2_hooke_law")


# ---------------------------------------------------------------------
print()
print("=== 图 3：塑性材料与脆性材料对比 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.0))

# (a) 塑性材料（低碳钢）：拉伸与压缩相近
e1 = np.array([0.0, 1.0, 1.5, 2.0, 15.0, 40.0, 70.0])
s_ten = np.array([0.0, 200.0, 210.0, 240.0, 250.0, 320.0, 380.0])
a1.plot(e1, s_ten, color=BLUE, lw=2.2, label="拉伸")
a1.plot(e1, -s_ten, color=GREEN, lw=2.2, label="压缩")
a1.axhline(0, color=GREY, lw=0.8)
a1.axvline(0, color=GREY, lw=0.8)
a1.set_xlim(0, 90)
a1.set_ylim(-420, 420)
a1.set_xlabel("eps（1e-3）", fontsize=9.5)
a1.set_ylabel("sigma / MPa", fontsize=9.5)
a1.set_title("(a) 塑性材料（低碳钢）：拉、压性能接近", fontsize=10, weight="bold")
a1.legend(fontsize=9, loc="center right")

# (b) 脆性材料（铸铁）：抗压远强于抗拉
e2 = np.array([0.0, 0.3, 0.6])
s_ten_b = np.array([0.0, 120.0, 150.0])
e3 = np.array([0.0, 1.0, 3.0, 8.0, 15.0])
s_com_b = np.array([0.0, 300.0, 550.0, 700.0, 760.0])
a2.plot(e2, s_ten_b, color=BLUE, lw=2.2, label="拉伸（强度低、脆断）")
a2.plot(e3, -s_com_b, color=GREEN, lw=2.2, label="压缩（强度高得多）")
a2.axhline(0, color=GREY, lw=0.8)
a2.axvline(0, color=GREY, lw=0.8)
a2.set_xlim(0, 20)
a2.set_ylim(-820, 820)
a2.set_xlabel("eps（1e-3）", fontsize=9.5)
a2.set_ylabel("sigma / MPa", fontsize=9.5)
a2.set_title("(b) 脆性材料（铸铁）：抗压远强于抗拉", fontsize=10, weight="bold")
a2.legend(fontsize=9, loc="center right")
savefig(fig, "lec03_fig3_ductile_vs_brittle")

print()
print("[DONE] 第 03 讲数字核对与三张图全部完成。")
