# 配图第四批：替换 ASCII 示意图（11 张）
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


def arr(ax, x0, y0, x1, y1, color="k", lw=1.5, text=None, tx=0, ty=0, fs=9):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0))
    if text:
        ax.text((x0 + x1) / 2 + tx, (y0 + y1) / 2 + ty, text, color=color, fontsize=fs)


def ground(ax, x0, x1, y=0):
    ax.plot([x0, x1], [y, y], color="k", lw=2.0)
    for x in np.linspace(x0, x1, 9):
        ax.plot([x, x - 0.05], [y, y - 0.08], color="k", lw=0.7)


# ---------- L01 吊架装置 ----------
fig, ax = plt.subplots(figsize=(5.0, 3.6))
ax.set_xlim(0, 6)
ax.set_ylim(-0.2, 3.6)
ax.set_aspect("equal")
ax.axis("off")
ground(ax, 0.3, 5.8, 0)
# column at A
ax.plot([0.7, 0.7], [0, 2.2], color="k", lw=2.0)
ax.plot(0.7, 2.2, "o", ms=6, color="k")
ax.plot([0.7, 4.0], [2.2, 2.2], color="k", lw=3.0)
ax.text(2.0, 2.35, "横梁 AB", fontsize=9)
# strut B-C
ax.plot([4.0, 4.9], [2.2, 0], color="k", lw=2.2)
ax.text(4.55, 1.25, "撑杆 CB", fontsize=9, rotation=-67)
ax.plot(4.0, 2.2, "o", ms=5, color="k")
ax.text(4.08, 2.3, "B", fontsize=9)
ax.plot(4.9, 0, "o", ms=5, color="k")
ax.text(4.95, -0.18, "C（固定铰）", fontsize=8.5)
ax.text(0.35, -0.18, "A（固定铰）", fontsize=8.5)
# hanger
ax.plot([2.2, 2.2], [2.2, 1.2], color="k", lw=1.2)
ax.plot(2.2, 2.2, "o", ms=4, color="k")
ax.text(2.3, 1.8, "D（吊点）", fontsize=8.5)
ax.add_patch(plt.Rectangle((1.85, 0.65), 0.7, 0.55, fill=False, lw=1.2))
ax.text(2.2, 0.9, "W", ha="center", fontsize=10)
arr(ax, 2.2, 1.2, 2.2, 1.22, color="gray")
ax.set_title("吊架：横梁 AB + 撑杆 CB + 吊重 W", fontsize=10)
save(fig, "fig_l01_crane.png")

# ---------- L01 三力平衡判据 ----------
fig, axes = plt.subplots(3, 1, figsize=(5.2, 3.6))
tags = ["平衡：等值、反向、共线", "不平衡：共线同向", "不平衡：反向但不共线（形成力偶）"]
for k, ax in enumerate(axes):
    ax.set_xlim(0, 6)
    ax.set_ylim(-0.6, 1.2)
    ax.axis("off")
    if k == 0:
        ax.plot([0.6, 1.6], [0.5, 0.5], color="k", lw=1.2)
        ax.plot([3.2, 4.2], [0.5, 0.5], color="k", lw=1.2)
        arr(ax, 1.6, 0.5, 2.6, 0.5, color="C3")
        arr(ax, 3.2, 0.5, 2.2, 0.5, color="C3")
    elif k == 1:
        ax.plot([0.6, 1.6], [0.5, 0.5], color="k", lw=1.2)
        ax.plot([3.2, 4.2], [0.5, 0.5], color="k", lw=1.2)
        arr(ax, 1.6, 0.5, 2.6, 0.5, color="C3")
        arr(ax, 3.2, 0.5, 4.2, 0.5, color="C3")
    else:
        ax.plot([0.8, 4.0], [0.6, 0.6], color="k", lw=1.0, ls=":")
        arr(ax, 1.2, 0.5, 0.2, 0.9, color="C3")
        arr(ax, 3.6, 0.5, 4.6, 0.9, color="C3")
        ax.add_patch(plt.matplotlib.patches.Arc((2.4, 0.5), 0.6, 0.6, theta1=20, theta2=160, color="C1", lw=1.2))
    ax.text(0.3, 1.0, tags[k], fontsize=9)
axes[0].set_title("两力平衡判据：只在等值、反向、共线时平衡", fontsize=10)
save(fig, "fig_l01_three_force.png")

# ---------- L01 力的平行四边形 ----------
fig, ax = plt.subplots(figsize=(4.2, 3.4))
ax.set_xlim(-0.2, 4.4)
ax.set_ylim(-0.2, 3.4)
ax.set_aspect("equal")
ax.axis("off")
O = np.array([0.3, 0.4])
F1 = np.array([2.8, 0])
F2 = np.array([0.9, 2.2])
R = F1 + F2
arr(ax, *O, O[0] + F1[0], O[1] + F1[1], color="C0", text="$F_1$", ty=-0.18)
arr(ax, *O, O[0] + F2[0], O[1] + F2[1], color="C1", text="$F_2$", tx=-0.2, ty=0.12)
ax.plot([O[0] + F1[0], O[0] + R[0]], [O[1] + F1[1], O[1] + R[1]], color="gray", lw=0.9, ls="--")
ax.plot([O[0] + F2[0], O[0] + R[0]], [O[1] + F2[1], O[1] + R[1]], color="gray", lw=0.9, ls="--")
arr(ax, *O, O[0] + R[0], O[1] + R[1], color="C3", lw=2.0, text="$R=F_1+F_2$", tx=0.1, ty=0.18)
ax.text(0.3, 3.05, "合力由平行四边形对角线给出；分力顺序可交换", fontsize=9)
ax.set_title("力的平行四边形法则", fontsize=10)
save(fig, "fig_l01_parallelogram.png")

# ---------- L01 三铰拱：整体 + 两个半拱 ----------
fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.2))
for ax in axes:
    ax.set_xlim(-0.3, 4.3)
    ax.set_ylim(-0.6, 3.0)
    ax.set_aspect("equal")
    ax.axis("off")
A, B, C, D = np.array([0, 0]), np.array([4, 0]), np.array([2, 1.6]), np.array([2, 2.6])
ax = axes[0]
ax.plot([A[0], D[0]], [A[1], D[1]], color="k", lw=2.0)
ax.plot([D[0], B[0]], [D[1], B[1]], color="k", lw=2.0)
ax.plot([A[0], C[0]], [A[1], C[1]], color="k", lw=1.2, ls="--")
ax.plot([C[0], B[0]], [C[1], B[1]], color="k", lw=1.2, ls="--")
ax.plot(D[0], D[1], "o", ms=5, color="k")
arr(ax, 3.4, 2.6, 2.05, 2.6, color="C3")
ax.text(3.1, 2.75, "$P$", color="C3", fontsize=10)
ax.plot(*A, "o", ms=5, color="k")
ax.plot(*B, "o", ms=5, color="k")
ax.text(-0.12, -0.25, "A", fontsize=9)
ax.text(4.02, -0.25, "B", fontsize=9)
ax.text(2.05, 1.35, "C", fontsize=9)
ax.set_title("三铰拱（A、B 铰支，C 中间铰）", fontsize=9)
ax = axes[1]
ax.plot([C[0], B[0]], [C[1], B[1]], color="k", lw=2.0)
arr(ax, 2.0, 1.6, 1.3, 2.2, color="C3", text="$F_C$", tx=-0.15)
arr(ax, 4.0, 0, 3.0, 0.8, color="C0", text="$F_B$", tx=-0.05, ty=0.14)
ax.text(2.0, 0.7, "BC 段：两端铰、无外载\n→ 二力构件", fontsize=9, ha="center")
ax.set_title("拆开：半拱 BC", fontsize=9)
ax = axes[2]
ax.plot([A[0], D[0]], [A[1], D[1]], color="k", lw=2.0)
ax.plot([D[0], C[0]], [D[1], C[1]], color="k", lw=2.0)
arr(ax, 3.4, 2.6, 2.05, 2.6, color="C3", text="$P$", ty=0.15)
arr(ax, 2.0, 1.6, 3.0, 0.8, color="C1", text="$F_C'$", tx=0.1, ty=-0.12)
arr(ax, 0, 0, 0.7, 0, color="C0", text="$F_{Ax}$", ty=-0.16)
arr(ax, 0, 0, 0, 0.8, color="C0", text="$F_{Ay}$", tx=-0.18)
ax.set_title("拆开：半拱 AC", fontsize=9)
save(fig, "fig_l01_arch.png")

# ---------- L01 吊架三张图 ----------
fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.4))
for ax in axes:
    ax.set_xlim(0, 5.4)
    ax.set_ylim(-0.3, 3.6)
    ax.set_aspect("equal")
    ax.axis("off")
ax = axes[0]
ground(ax, 0.2, 5.2, 0)
ax.plot([0.7, 0.7], [0, 2.2], color="k", lw=2)
ax.plot([0.7, 4.0], [2.2, 2.2], color="k", lw=3)
ax.plot([4.0, 4.9], [2.2, 0], color="k", lw=2)
ax.plot([2.2, 2.2], [2.2, 1.3], color="k", lw=1.0)
ax.add_patch(plt.Rectangle((1.9, 0.75), 0.6, 0.5, fill=False, lw=1.0))
ax.text(2.2, 1.0, "W", ha="center", fontsize=8.5)
ax.set_title("装置", fontsize=9)
ax = axes[1]
ax.plot([1.0, 4.2], [2.8, 0.4], color="k", lw=2.4)
ax.plot(1.0, 2.8, "o", ms=5, color="k")
ax.plot(4.2, 0.4, "o", ms=5, color="k")
ax.text(0.85, 2.95, "B", fontsize=9)
ax.text(4.25, 0.25, "C", fontsize=9)
arr(ax, 1.0, 2.8, 0.4, 3.4, color="C3", text="$F_B$", tx=-0.1)
arr(ax, 4.2, 0.4, 4.8, 0.9, color="C0", text="$F_C$", tx=0.1)
ax.set_title("分离体：撑杆 CB（二力构件）", fontsize=9)
ax = axes[2]
ax.plot([0.6, 4.2], [2.4, 2.4], color="k", lw=3)
ax.plot(0.6, 2.4, "o", ms=5, color="k")
ax.plot(4.2, 2.4, "o", ms=5, color="k")
ax.plot([2.0, 2.0], [2.4, 1.5], color="k", lw=1.0)
arr(ax, 2.0, 1.5, 2.0, 2.38, color="C3", text="$F_D$", tx=0.12)
arr(ax, 0.6, 2.4, 0.6, 3.1, color="C0", text="$F_{Ay}$", tx=-0.2)
arr(ax, 0.6, 2.4, 1.3, 2.4, color="C0", text="$F_{Ax}$", ty=-0.16)
arr(ax, 4.2, 2.4, 4.7, 2.9, color="C1", text="$F_B'$", tx=0.05)
ax.set_title("分离体：横梁 AB", fontsize=9)
save(fig, "fig_l01_crane_fbd.png")

# ---------- L03 王柱桁架 ----------
fig, ax = plt.subplots(figsize=(5.0, 3.4))
ax.set_xlim(-0.4, 4.4)
ax.set_ylim(-0.5, 2.6)
ax.set_aspect("equal")
ax.axis("off")
A, B, C, D = np.array([0, 0]), np.array([2, 0]), np.array([4, 0]), np.array([2, 2])
for P, Q in [(A, D), (C, D), (B, D), (A, B), (B, C)]:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color="k", lw=2.0)
for P, name, off in [(A, "A", (-0.18, -0.2)), (B, "B", (-0.1, -0.25)), (C, "C", (0.08, -0.2)), (D, "D", (0.08, 0.12))]:
    ax.plot(*P, "o", ms=5, color="k")
    ax.text(P[0] + off[0], P[1] + off[1], name, fontsize=9)
arr(ax, 2.0, 2.5, 2.0, 2.05, color="C3", text="$P$", tx=0.12)
ground(ax, -0.3, 4.3, -0.15)
ax.plot([-0.22, 0, 0.22], [-0.15, 0, -0.15], color="k", lw=1.0)
ax.add_patch(plt.Circle((3.9, -0.2), 0.06, fill=False, lw=0.9))
ax.add_patch(plt.Circle((4.1, -0.2), 0.06, fill=False, lw=0.9))
ax.set_title("王柱桁架：AD、DC、BD 与下弦 AB、BC", fontsize=10)
save(fig, "fig_l03_kingpost.png")

# ---------- L05 物块受斜拉 ----------
fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.set_xlim(-0.4, 4.4)
ax.set_ylim(-0.4, 2.6)
ax.set_aspect("equal")
ax.axis("off")
ground(ax, -0.2, 4.2, 0)
ax.add_patch(plt.Rectangle((1.4, 0), 1.2, 1.0, fill=False, lw=1.6))
ax.text(2.0, 0.5, "W", ha="center", fontsize=10)
arr(ax, 2.6, 0.7, 3.7, 1.35, color="C3", text="$T$（30°）", tx=0.25, ty=0.15)
arr(ax, 2.0, 0, 2.0, -0.35, color="C1")
ax.text(2.0, -0.55, "$W$", ha="center", fontsize=9, color="C1")
arr(ax, 2.0, 0, 2.0, 0.9, color="C0", text="$N$", tx=0.12)
ax.text(0.2, 2.2, "底面 $f_s=0.4$；拉力的水平分量对抗摩擦", fontsize=9)
ax.set_title("物块受斜拉：分解与摩擦", fontsize=10)
save(fig, "fig_l05_block.png")

# ---------- L05 梯子 ----------
fig, ax = plt.subplots(figsize=(4.2, 3.8))
ax.set_xlim(-0.4, 4.0)
ax.set_ylim(-0.4, 3.8)
ax.set_aspect("equal")
ax.axis("off")
ax.plot([0, 0], [0, 3.6], color="k", lw=2.4)
ground(ax, -0.2, 3.8, 0)
A = np.array([1.8, 0])
B = np.array([0.12, 2.4])
ax.plot([A[0], B[0]], [A[1], B[1]], color="k", lw=2.2)
ax.plot(*A, "o", ms=5, color="k")
ax.plot(*B, "o", ms=5, color="k")
ax.text(A[0], -0.2, "A", fontsize=9)
ax.text(B[0] + 0.08, B[1], "B", fontsize=9)
arr(ax, 0, B[1], 0.5, B[1], color="C0", text="$N_B$", tx=0.1, ty=0.14)
arr(ax, A[0], 0, A[0], 0.6, color="C0", text="$N_A$", tx=0.12)
arr(ax, A[0], 0, A[0] - 0.55, 0, color="C3", text="$F_A$", ty=-0.16)
Pp = A + 0.4 * (B - A)
ax.plot(Pp[0], Pp[1], "o", ms=5, color="C2")
ax.text(Pp[0] + 0.1, Pp[1] + 0.1, "人", fontsize=9, color="C2")
ax.set_title("梯子：墙光滑、地面粗糙", fontsize=10)
save(fig, "fig_l05_ladder.png")

# ---------- L06 椭圆规机构 ----------
fig, ax = plt.subplots(figsize=(4.4, 4.0))
ax.set_xlim(-0.4, 3.8)
ax.set_ylim(-0.4, 3.8)
ax.set_aspect("equal")
ax.axis("off")
ax.annotate("", xy=(3.6, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=0.9))
ax.annotate("", xy=(0, 3.6), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=0.9))
ax.text(3.62, -0.12, "$x$", fontsize=9)
ax.text(-0.12, 3.62, "$y$", fontsize=9)
L = 2.6
phi = np.deg2rad(55)
A = np.array([0, L * np.cos(phi)])     # vertical slider
B = np.array([L * np.sin(phi), 0])     # horizontal slider
M = A + 0.7 * (B - A)
ax.plot([A[0], B[0]], [A[1], B[1]], color="k", lw=2.2)
ax.plot(*A, "s", ms=6, color="C0")
ax.plot(*B, "s", ms=6, color="C0")
ax.plot(*M, "o", ms=6, color="C3")
ax.text(A[0] + 0.1, A[1], "A（竖直滑槽）", fontsize=8.5)
ax.text(B[0], B[1] - 0.25, "B（水平滑槽）", fontsize=8.5)
ax.text(M[0] + 0.1, M[1] + 0.1, "M", fontsize=10, color="C3")
th = np.linspace(0, 2 * np.pi, 300)
ax.plot(0.7 * L * np.sin(th), 0.3 * L * np.cos(th), color="gray", lw=0.9, ls="--")
ax.text(1.55, 0.35, "M 的轨迹：椭圆", fontsize=8.5, color="gray")
ax.set_title("椭圆规：两滑块 + 定长杆", fontsize=10)
save(fig, "fig_l06_trammel.png")

# ---------- L07 卷扬机传动 ----------
fig, ax = plt.subplots(figsize=(7.2, 2.8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 4)
ax.axis("off")
# motor
ax.add_patch(plt.Rectangle((0.3, 1.2), 1.6, 1.4, fill=False, lw=1.6))
ax.text(1.1, 1.9, "电机", ha="center", fontsize=9)
ax.text(1.1, 0.8, "1440 r/min", ha="center", fontsize=8)
# gear pairs
ax.add_patch(plt.Circle((2.9, 2.0), 0.32, fill=False, lw=1.4))
ax.add_patch(plt.Circle((4.02, 2.0), 0.8, fill=False, lw=1.4))
ax.text(2.9, 1.5, "$z_1$", ha="center", fontsize=9)
ax.text(4.02, 1.05, "$z_2$", ha="center", fontsize=9)
ax.plot([2.3, 2.6], [2.0, 2.0], color="k", lw=2)
ax.plot([3.1, 3.5], [2.0, 2.0], color="k", lw=2)
ax.add_patch(plt.Circle((5.28, 2.0), 0.32, fill=False, lw=1.4))
ax.add_patch(plt.Circle((6.4, 2.0), 0.8, fill=False, lw=1.4))
ax.text(5.28, 1.5, "$z_3$", ha="center", fontsize=9)
ax.text(6.4, 1.05, "$z_4$", ha="center", fontsize=9)
ax.plot([4.82, 4.96], [2.0, 2.0], color="k", lw=2)
ax.plot([5.6, 5.6], [2.0, 2.0], color="k", lw=2)
# drum
ax.add_patch(plt.Circle((8.3, 2.0), 0.75, fill=False, lw=1.6))
ax.plot([7.2, 7.55], [2.0, 2.0], color="k", lw=2)
ax.text(8.3, 0.95, "滚筒 r=0.2 m", ha="center", fontsize=8)
ax.text(8.3, 2.0, "57.6 r/min", ha="center", fontsize=8)
# rope and load
ax.plot([9.05, 9.05], [2.0, 3.0], color="k", lw=1.2)
ax.plot([9.05, 10.6], [3.0, 3.0], color="k", lw=1.2)
ax.plot([10.6, 10.6], [3.0, 2.2], color="k", lw=1.0)
ax.add_patch(plt.Rectangle((10.3, 1.4), 0.6, 0.8, fill=False, lw=1.2))
ax.text(10.6, 1.8, "W", ha="center", fontsize=9)
ax.text(10.75, 2.5, "v=1.21 m/s", fontsize=8.5)
ax.text(4.6, 3.4, "二级齿轮减速：总传动比 $i=25$", fontsize=9)
ax.set_title("卷扬机传动链：电机 → 二级齿轮 → 滚筒 → 重物", fontsize=10)
save(fig, "fig_l07_hoist.png")

# ---------- L09 曲柄滑块机构 ----------
fig, ax = plt.subplots(figsize=(5.6, 3.0))
ax.set_xlim(-0.3, 4.4)
ax.set_ylim(-0.7, 2.0)
ax.set_aspect("equal")
ax.axis("off")
O = np.array([0.6, 0.8])
r, l = 0.9, 2.2
phi = np.deg2rad(60)
A = O + r * np.array([np.cos(phi), np.sin(phi)])
B = np.array([A[0] + np.sqrt(l ** 2 - (A[1] - O[1]) ** 2), O[1] - 0.02])
ax.plot([O[0], A[0]], [O[1], A[1]], color="k", lw=2.4)
ax.plot([A[0], B[0]], [A[1], B[1]], color="k", lw=2.4)
ax.plot(*O, "o", ms=5, color="k")
ax.plot(*A, "o", ms=5, color="k")
ax.plot(*B, "s", ms=6, color="k")
ax.text(O[0] - 0.2, O[1] - 0.2, "O", fontsize=9)
ax.text(A[0] - 0.05, A[1] + 0.12, "A", fontsize=9)
ax.text(B[0] + 0.05, B[1] - 0.28, "B（滑块）", fontsize=9)
ax.plot([B[0] - 0.2, B[0] + 0.8], [O[1] - 0.08, O[1] - 0.08], color="k", lw=1.5)
ax.add_patch(plt.matplotlib.patches.Arc(O, 0.7, 0.7, theta1=0, theta2=60, color="C1", lw=1.1))
ax.text(O[0] + 0.32, O[1] + 0.18, "$\\varphi$", color="C1", fontsize=10)
ax.text(O[0] + 0.35, O[1] - 0.35, "曲柄 $r$", fontsize=8.5)
ax.text((A[0] + B[0]) / 2, (A[1] + B[1]) / 2 + 0.15, "连杆 $l$", fontsize=8.5)
ax.set_title("曲柄滑块机构：曲柄定轴转动，连杆平面运动，滑块平移", fontsize=10)
save(fig, "fig_l09_crank_slider.png")

# ---------- L01 二力杆：直杆与弯杆 ----------
fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
for ax in axes:
    ax.set_xlim(-0.3, 3.3)
    ax.set_ylim(-0.6, 2.6)
    ax.set_aspect("equal")
    ax.axis("off")
ax = axes[0]
ax.plot([0.5, 2.5], [2.0, 0.4], color="k", lw=2.6)
ax.plot(0.5, 2.0, "o", ms=6, color="k")
ax.plot(2.5, 0.4, "o", ms=6, color="k")
arr(ax, 0.5, 2.0, 1.2, 2.55, color="C3", text="$F_A$", tx=-0.1)
arr(ax, 2.5, 0.4, 1.8, -0.15, color="C3", text="$F_B$", tx=-0.1)
ax.text(0.6, 0.2, "直杆：力沿杆轴", fontsize=9)
ax.set_title("直杆", fontsize=9)
ax = axes[1]
t = np.linspace(0, 1, 100)
x = 0.6 + 2.0 * t
y = 2.0 - 1.6 * t + 0.5 * np.sin(np.pi * t)
ax.plot(x, y, color="k", lw=2.6)
ax.plot(0.6, 2.0, "o", ms=6, color="k")
ax.plot(2.6, 0.4, "o", ms=6, color="k")
ax.plot([0.6, 2.6], [2.0, 0.4], color="gray", lw=0.9, ls="--")
arr(ax, 0.6, 2.0, 1.25, 2.6, color="C3", text="$F_A$", tx=-0.1)
arr(ax, 2.6, 0.4, 1.95, -0.2, color="C3", text="$F_B$", tx=-0.05)
ax.text(0.5, 0.2, "弯杆：力仍沿两端铰连线（虚线）", fontsize=9)
ax.set_title("弯杆", fontsize=9)
save(fig, "fig_l01_two_force.png")

# ---------- L01 撑杆 CB 分离体 ----------
fig, ax = plt.subplots(figsize=(4.4, 3.4))
ax.set_xlim(-0.6, 3.9)
ax.set_ylim(-0.9, 4.0)
ax.set_aspect("equal")
ax.axis("off")
B = np.array([0.7, 2.8])
C = np.array([2.9, 0.4])
ax.plot([B[0], C[0]], [B[1], C[1]], color="k", lw=3.0)
ax.plot(*B, "o", ms=6, color="k")
ax.plot(*C, "o", ms=6, color="k")
ax.text(B[0] - 0.28, B[1] - 0.18, "B", fontsize=10)
ax.text(C[0] + 0.08, C[1] - 0.12, "C", fontsize=10)
d = (C - B) / np.hypot(*(C - B))
arr(ax, B[0], B[1], B[0] - 0.75 * d[0], B[1] - 0.75 * d[1], color="C3")
ax.text(B[0] - 0.55 * d[0] - 0.35, B[1] - 0.55 * d[1] + 0.05, "$F_B$", color="C3", fontsize=9)
arr(ax, C[0], C[1], C[0] + 0.75 * d[0], C[1] + 0.75 * d[1], color="C0")
ax.text(C[0] + 0.55 * d[0] + 0.12, C[1] + 0.55 * d[1] - 0.05, "$F_C$", color="C0", fontsize=9)
ax.set_title("分离体：撑杆 CB 的成品受力图", fontsize=10)
save(fig, "fig_l01_cb.png")

# ---------- L01 滚动支座 ----------
fig, ax = plt.subplots(figsize=(4.2, 3.0))
ax.set_xlim(-0.3, 3.3)
ax.set_ylim(-0.5, 2.8)
ax.set_aspect("equal")
ax.axis("off")
# ground
ax.plot([-0.2, 3.2], [0, 0], color="k", lw=2.0)
for x in np.linspace(-0.1, 3.1, 8):
    ax.plot([x, x - 0.06], [0, -0.12], color="k", lw=0.7)
# beam
ax.plot([0.15, 2.75], [1.25, 1.25], color="k", lw=3.0)
# triangle
ax.plot([0.85, 1.45, 2.05, 0.85], [0.32, 1.25, 0.32, 0.32], color="k", lw=1.6)
# rollers
for x in (1.2, 1.45, 1.7):
    ax.add_patch(plt.Circle((x, 0.16), 0.16, fill=False, lw=1.1))
# reaction
arr(ax, 1.45, 1.3, 1.45, 2.15, color="C0", text="$N$", tx=0.12)
# sliding hint
arr(ax, 2.2, 0.55, 2.95, 0.55, color="C1")
ax.text(2.2, 0.32, "可沿支承面滑动", fontsize=9, color="C1")
ax.set_title("滚动（辊轴）支座：只有一个法向反力 $N$", fontsize=10)
save(fig, "fig_l01_roller.png")

# ---------- L03 三铰拱（例 2） ----------
fig, ax = plt.subplots(figsize=(5.6, 3.4))
ax.set_xlim(-0.6, 8.8)
ax.set_ylim(-0.6, 3.8)
ax.set_aspect("equal")
ax.axis("off")
A, B, C, D = np.array([0, 0]), np.array([8, 0]), np.array([4, 3]), np.array([2, 2])
ax.plot([A[0], D[0]], [A[1], D[1]], color="k", lw=2.4)
ax.plot([D[0], C[0]], [D[1], C[1]], color="k", lw=2.4)
ax.plot([C[0], B[0]], [C[1], B[1]], color="k", lw=2.4)
ax.plot([A[0], B[0]], [A[1], B[1]], color="gray", lw=0.8, ls=":")
for P, name, off in [(A, "A", (-0.3, -0.35)), (B, "B", (0.12, -0.35)), (C, "C", (0.12, 0.12)), (D, "D", (-0.12, 0.22))]:
    ax.plot(P[0], P[1], "o", ms=5.5, color="k")
    ax.text(P[0] + off[0], P[1] + off[1], name, fontsize=10)
arr(ax, D[0], D[1], D[0] + 1.3, D[1], color="C3")
ax.text(D[0] + 0.42, D[1] + 0.4, "$P=12$ kN", color="C3", fontsize=9)
ground(ax, -0.4, 8.4, -0.15)
ax.plot([-0.15, 0, 0.15], [-0.15, 0, -0.15], color="k", lw=1.0)
ax.plot([7.85, 8, 8.15], [-0.15, 0, -0.15], color="k", lw=1.0)
ax.annotate("", xy=(8, -0.45), xytext=(0, -0.45), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.text(3.9, -0.4, "8 m", fontsize=8.5)
ax.annotate("", xy=(4.15, 3), xytext=(4.15, 0), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.text(4.25, 1.4, "3 m", fontsize=8.5)
ax.set_title("三铰拱：A、B 固定铰，C 中间铰，D 点受水平力", fontsize=10)
save(fig, "fig_l03_arch.png")

print("batch D done")
