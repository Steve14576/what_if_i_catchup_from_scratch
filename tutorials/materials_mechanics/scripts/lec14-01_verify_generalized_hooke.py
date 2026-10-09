# =====================================================================
# lec14-01 第 14 讲《三向应力状态与广义胡克定律》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对（取三向主应力 s1=100, s2=50, s3=-20 MPa；E=2e5 MPa, mu=0.3）：
#   EXP1 三向最大切应力 tau_max = (s1-s3)/2，及三个主切应力
#   EXP2 广义胡克定律：eps_x, eps_y, eps_z
#   EXP3 体积应变 theta = (1-2mu)(s1+s2+s3)/E = eps_x+eps_y+eps_z（互证）
#   EXP4 三个弹性常数关系：G = E/[2(1+mu)]
#   EXP5 单向拉伸：eps_x=s/E, eps_y=eps_z=-mu*s/E；体积应变
# 出图（编号按正文出现顺序）：
#   lec14_fig1_triaxial_element   三向应力状态单元体
#   lec14_fig2_triaxial_circles   三向应力圆
#   lec14_fig3_generalized_hooke  广义胡克定律与体积应变
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
print("=== 数字核对：第 14 讲（s1=100, s2=50, s3=-20 MPa; E=2e5, mu=0.3）===")
s1, s2, s3 = 100.0, 50.0, -20.0
E, mu = 2.0e5, 0.3

t12 = (s1 - s2) / 2.0
t23 = (s2 - s3) / 2.0
t13 = (s1 - s3) / 2.0
print("  EXP1 三个主切应力：(s1-s2)/2=%.1f, (s2-s3)/2=%.1f, (s1-s3)/2=%.1f -> tau_max=%.1f MPa"
      % (t12, t23, t13, t13))

ex = (s1 - mu * (s2 + s3)) / E
ey = (s2 - mu * (s1 + s3)) / E
ez = (s3 - mu * (s1 + s2)) / E
print("  EXP2 广义胡克定律：eps_x=%.3e, eps_y=%.3e, eps_z=%.3e" % (ex, ey, ez))

theta_direct = ex + ey + ez
theta_formula = (1 - 2 * mu) * (s1 + s2 + s3) / E
print("  EXP3 体积应变：eps_x+eps_y+eps_z=%.4e；公式 (1-2mu)(sum)/E=%.4e（应一致）"
      % (theta_direct, theta_formula))

G = E / (2.0 * (1.0 + mu))
print("  EXP4 弹性常数关系：G=E/[2(1+mu)]=%.1f MPa" % G)

sig0 = 100.0
theta_h = 3.0 * (1 - 2 * mu) * sig0 / E
print("  EXP5 三向等压（s0=%.0f）：theta=3(1-2mu)s0/E=%.4e（无剪应变、无形状改变）" % (sig0, theta_h))
# 泊松比上界：体积不变 theta=0 -> mu=0.5
print("        泊松比上界：theta=0 -> (1-2mu)=0 -> mu=0.5（体积不可压缩的极限）")


# ---------------------------------------------------------------------
print()
print("=== 图 1：三向应力状态单元体 ===")
fig, ax = plt.subplots(figsize=(7.0, 6.2))
ax.set_xlim(-2.6, 3.0)
ax.set_ylim(-2.4, 3.0)
ax.set_aspect("equal")
ax.axis("off")
# 六面体（斜二测投影）
ox, oy = 0.0, 0.0
dx, dy = 1.8, 1.0
dz = 1.3
# 前面
ax.add_patch(Rectangle((ox, oy), dx, dy, fc="#e7f0fb", ec=BLUE, lw=1.5))
# 顶面
ax.add_patch(plt.Polygon([[ox, oy + dy], [ox + dx * 0.5, oy + dy + dz], [ox + dx * 1.5, oy + dy + dz], [ox + dx, oy + dy]],
                         closed=True, fc="#d5e6f7", ec=BLUE, lw=1.5))
# 右面
ax.add_patch(plt.Polygon([[ox + dx, oy], [ox + dx * 1.5, oy + dz], [ox + dx * 1.5, oy + dy + dz], [ox + dx, oy + dy]],
                         closed=True, fc="#cfe0f2", ec=BLUE, lw=1.5))
# sigma1（x 右）
ax.annotate("", xy=(ox + dx + 0.9, oy + dy * 0.5), xytext=(ox + dx + 0.1, oy + dy * 0.5),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(ox + dx + 1.0, oy + dy * 0.5, r"$\sigma_1$", fontsize=13, color=RED, va="center")
# sigma2（y 上）
ax.annotate("", xy=(ox + dx * 0.5, oy + dy + dz + 0.8), xytext=(ox + dx * 0.5, oy + dy + dz + 0.05),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(ox + dx * 0.5 + 0.1, oy + dy + dz + 0.85, r"$\sigma_2$", fontsize=13, color=RED)
# sigma3（z 斜向上）
ax.annotate("", xy=(ox + dx * 1.5 - 0.7, oy + dy + dz + 0.7), xytext=(ox + dx * 1.5 + 0.1, oy + dy + dz + 0.05),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(ox + dx * 1.5 - 0.9, oy + dy + dz + 0.8, r"$\sigma_3$", fontsize=13, color=RED)
ax.text(ox + dx * 0.7, oy - 1.6, "三向应力状态：三个主应力 $\\sigma_1,\\sigma_2,\\sigma_3$（切应力为零）",
        ha="center", fontsize=9.5)
ax.text(ox + dx * 0.7, oy + dy + dz + 1.7, "三向应力状态（单元体）", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec14_fig1_triaxial_element")


# ---------------------------------------------------------------------
print()
print("=== 图 2：三向应力圆 ===")
fig, ax = plt.subplots(figsize=(9.0, 5.6))
ax.set_xlim(-45, 125)
ax.set_ylim(-72, 72)
ax.set_aspect("equal")
ax.axis("off")
ax.annotate("", xy=(122, 0), xytext=(-42, 0), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.2))
ax.text(120, -9, r"$\sigma$", fontsize=11, color=GREY)
ax.annotate("", xy=(40, 70), xytext=(40, -70), arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.0))
ax.text(43, 68, r"$\tau$", fontsize=11, color=GREY)


def circle(cx, r, color, lw=1.8):
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(cx + r * np.cos(th), r * np.sin(th), color=color, lw=lw)


# 三个主切应力圆
circle((s2 + s3) / 2, (s2 - s3) / 2, GREEN)
circle((s1 + s3) / 2, (s1 - s3) / 2, BLUE)
circle((s1 + s2) / 2, (s1 - s2) / 2, ORANGE)
for s, name in [(s3, r"$\sigma_3$"), (s2, r"$\sigma_2$"), (s1, r"$\sigma_1$")]:
    ax.plot([s], [0], "o", color=RED, ms=6)
    ax.text(s, 6, name, ha="center", fontsize=11, color=RED)
# tau_max
ax.plot([(s1 + s3) / 2], [(s1 - s3) / 2], "o", color=BLUE, ms=6)
ax.text((s1 + s3) / 2 + 2, (s1 - s3) / 2 + 2, r"$\tau_{\max}=\dfrac{\sigma_1-\sigma_3}{2}$", fontsize=10, color=BLUE)
ax.text(40, -66, "三向应力圆：三个圆，最大切应力 = 最大圆的半径 = (sigma_1-sigma_3)/2",
        ha="center", fontsize=9.5)
ax.text(40, 76, "三向应力状态下的应力圆", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec14_fig2_triaxial_circles")


# ---------------------------------------------------------------------
print()
print("=== 图 3：广义胡克定律与体积应变 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 4.4))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

# (a) 单向拉伸的泊松效应
a1.add_patch(Rectangle((2.5, 2.4), 5.0, 1.2, fc="#e7f0fb", ec=BLUE, lw=1.6))
a1.annotate("", xy=(1.9, 3.0), xytext=(2.5, 3.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
a1.annotate("", xy=(8.1, 3.0), xytext=(7.5, 3.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
a1.text(5.0, 3.95, r"$\sigma_x$ 拉：纵向伸长 $\varepsilon_x>0$", ha="center", fontsize=9.5, color=RED)
a1.annotate("", xy=(5.0, 2.4), xytext=(5.0, 2.9), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6))
a1.annotate("", xy=(5.0, 3.6), xytext=(5.0, 3.1), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6))
a1.text(5.6, 2.1, r"横向收缩 $\varepsilon_y=\varepsilon_z=-\mu\sigma_x/E<0$", ha="center", fontsize=9.5, color=GREEN)
a1.text(5.0, 5.2, "(a) 泊松效应", ha="center", fontsize=11, weight="bold")

# (b) 体积应变
a2.add_patch(Rectangle((3.0, 2.0), 3.0, 3.0, fc="#eef2f7", ec=GREY))
a2.text(4.5, 3.5, "V", ha="center", fontsize=14, color=GREY)
a2.text(4.5, 5.4, "(b) 体积应变", ha="center", fontsize=11, weight="bold")
a2.text(4.5, 1.1, r"$\theta=\dfrac{1-2\mu}{E}(\sigma_1+\sigma_2+\sigma_3)$", ha="center", fontsize=11, color=BLUE)
a2.text(4.5, 0.4, "切应力不改变体积（只改变形状）", ha="center", fontsize=8.5, color=GREY)
savefig(fig, "lec14_fig3_generalized_hooke")

print()
print("[DONE] 第 14 讲数字核对与三张图全部完成。")
