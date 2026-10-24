# 配图补遗：L04 组合形体重心、L07 定轴转动速度场
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 10
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(BASE, "figures")


def save(fig, name):
    fig.savefig(os.path.join(FIG, name), dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


def arr(ax, x0, y0, x1, y1, color="k", lw=1.4, text=None, tx=0, ty=0, fs=9):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0))
    if text:
        ax.text((x0 + x1) / 2 + tx, (y0 + y1) / 2 + ty, text, color=color, fontsize=fs)


# ---------- L04-2 组合形体重心 ----------
fig, ax = plt.subplots(figsize=(4.8, 3.6))
ax.set_xlim(-0.2, 5.2)
ax.set_ylim(-0.6, 4.8)
ax.set_aspect("equal")
ax.axis("off")
# T shape: bottom flange 4x1 at y0..1, web 1.2x2 at x=1.4..2.6, y=1..3
ax.add_patch(plt.Rectangle((0, 0), 4.0, 1.0, fill=False, lw=1.6))
ax.add_patch(plt.Rectangle((1.4, 1.0), 1.2, 2.0, fill=False, lw=1.6))
ax.plot(2.0, 0.5, "o", ms=6, color="C0")
ax.text(2.1, 0.35, "$C_1$", color="C0", fontsize=10)
ax.plot(2.0, 2.0, "o", ms=6, color="C3")
ax.text(2.1, 2.1, "$C_2$", color="C3", fontsize=10)
ax.plot(2.0, 1.05, "o", ms=7, color="C2")
ax.text(2.14, 1.22, "$C$（整体）", color="C2", fontsize=9)
ax.text(-0.1, 4.45, "$A_1=4\\times1$，$y_1=0.5$；$A_2=1.2\\times2$，$y_2=2$", fontsize=9)
ax.text(-0.1, 3.95, "$y_C=\\dfrac{A_1y_1+A_2y_2}{A_1+A_2}=\\dfrac{2+4.8}{6.4}=1.06$", fontsize=9)
ax.text(-0.1, -0.45, "组合形体重心：拆成规则块，按面积加权", fontsize=9)
ax.set_title("组合形体的重心（T 形截面）", fontsize=10)
save(fig, "fig_l04_centroid.png")

# ---------- L07-2 定轴转动速度场 ----------
fig, ax = plt.subplots(figsize=(4.6, 4.0))
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_aspect("equal")
ax.axis("off")
R = 1.35
ax.add_patch(plt.Circle((0, 0), R, fill=False, lw=1.4))
ax.plot(0, 0, "o", ms=5, color="k")
ax.text(-0.18, -0.18, "O", fontsize=9)
for ang in [20, 70, 110, 160, 200, 250, 290, 340]:
    a = np.deg2rad(ang)
    x, y = R * np.cos(a), R * np.sin(a)
    # v = omega x r: for CCW, direction = (-sin, cos)
    vx, vy = -np.sin(a), np.cos(a)
    L = 0.45 * R
    arr(ax, x, y, x + L * vx, y + L * vy, color="C0", lw=1.1)
ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 0.8, 0.8, theta1=20, theta2=110, color="C1", lw=1.5))
ax.text(-0.55, 0.62, "$\\omega$", color="C1", fontsize=11)
ax.text(-1.5, -1.5, "各点速度 $v=\\omega r$、方向垂直半径；$a_n=\\omega^2r$ 指向轴心", fontsize=9)
ax.set_title("定轴转动：速度场与加速度分布", fontsize=10)
save(fig, "fig_l07_rotation_field.png")

print("batch C done")
