# 配图第二批：L12-L21（17 张）
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 10
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(BASE, "figures")
os.makedirs(FIG, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(FIG, name), dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


def arr(ax, x0, y0, x1, y1, color="k", lw=1.5, text=None, tx=0, ty=0, fs=9, ha="center", ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0))
    if text:
        ax.text((x0 + x1) / 2 + tx, (y0 + y1) / 2 + ty, text, color=color, fontsize=fs, ha=ha, va="center")


# ---------- L12-2 空爆与质心 ----------
fig, ax = plt.subplots(figsize=(6.2, 3.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis("off")
x = np.linspace(0, 9, 200)
y = 4.2 * (x / 9) - 0.40 * (x / 9) ** 2 * 4.2
ax.plot(x, y, color="gray", lw=1.4, ls="--")
ax.text(6.6, 2.4, "原抛物线（质心轨迹）", color="gray", fontsize=9, rotation=-18)
xb = 5.0
yb = 4.2 * (xb / 9) - 0.40 * (xb / 9) ** 2 * 4.2
ax.plot(xb, yb, "o", ms=7, color="C3")
ax.text(xb - 0.6, yb + 0.35, "爆炸点", fontsize=9, color="C3")
# fragments
for (dx, dy, c) in [(-2.2, -1.2, "C0"), (-1.5, 1.0, "C0"), (0.6, 1.4, "C1"), (1.6, -0.6, "C1")]:
    ax.annotate("", xy=(xb + dx, yb + dy), xytext=(xb, yb),
                arrowprops=dict(arrowstyle="-|>", lw=1.1, color=c))
ax.text(xb + 0.4, yb - 1.4, "碎片各飞各的", fontsize=9, color="C1")
ax.plot(x[x > xb / 9 * 9], y[x > xb / 9 * 9], color="C3", lw=1.2)
ax.text(7.4, 3.4, "质心仍走原抛物线", color="C3", fontsize=9)
ax.annotate("", xy=(xb, yb), xytext=(xb, 0), arrowprops=dict(arrowstyle="-", lw=0.7, ls=":"))
ax.text(0.2, 0.2, "内力再大也改不了质心轨迹（水平无外力）", fontsize=9)
ax.set_title("空爆：碎片轨迹乱、质心轨迹不变", fontsize=10)
save(fig, "fig_l12_explosion.png")

# ---------- L12-3 走船 ----------
fig, axes = plt.subplots(2, 1, figsize=(6.4, 3.4))
for ax in axes:
    ax.set_xlim(0, 8)
    ax.set_ylim(-0.6, 2.0)
    ax.axis("off")
ax = axes[0]
ax.plot([4.0, 6.4], [0.2, 0.2], color="k", lw=3)
ax.plot([4.0, 4.2, 4.2, 4.0], [0.2, 0.2, 0.9, 0.9], color="k", lw=0.8)
ax.plot(4.6, 0.75, "o", ms=7, color="C0")
ax.text(4.55, 0.95, "人", fontsize=9)
ax.plot(5.2, 0.05, "|", ms=8, color="C3")
ax.text(5.0, -0.35, "初始质心", fontsize=8, color="C3")
ax.text(0.2, 1.5, "人从船左端走到右端", fontsize=9)
ax = axes[1]
ax.plot([3.0, 5.4], [0.2, 0.2], color="k", lw=3)
ax.plot([3.0, 3.2, 3.2, 3.0], [0.2, 0.2, 0.9, 0.9], color="k", lw=0.8)
ax.plot(4.9, 0.75, "o", ms=7, color="C0")
ax.text(4.85, 0.95, "人", fontsize=9)
ax.plot(5.2, 0.05, "|", ms=8, color="C3")
ax.text(5.0, -0.35, "质心位置不变", fontsize=8, color="C3")
ax.annotate("", xy=(0.9, 1.3), xytext=(1.5, 1.3), arrowprops=dict(arrowstyle="-|>", lw=1.0, color="C1"))
ax.text(1.2, 1.45, "船左移", fontsize=9, color="C1")
ax.set_title("走船：人船位移与质量成反比，质心不动", fontsize=10)
save(fig, "fig_l12_boat.png")

# ---------- L13-1 常见形体的转动惯量 ----------
fig, axes = plt.subplots(1, 4, figsize=(9.4, 2.8))
for ax, title in zip(axes, ["细杆（绕中点）", "圆盘（绕中心轴）", "圆环（绕中心轴）", "实心球（绕直径）"]):
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=9)
# rod
ax = axes[0]
ax.plot([-1, 1], [0, 0], color="k", lw=4)
ax.plot(0, 0, "o", ms=4, color="C3")
ax.plot([0, 0], [-0.55, 0.55], color="gray", lw=0.9, ls="--")
ax.text(-0.9, -0.45, "$J=\\frac{1}{12}ml^2$", fontsize=9)
# disk
ax = axes[1]
ax.add_patch(plt.Circle((0, 0), 0.85, fill=False, lw=2))
ax.plot(0, 0, "o", ms=4, color="C3")
ax.text(-0.75, -1.0, "$J=\\frac{1}{2}mR^2$", fontsize=9)
# ring
ax = axes[2]
ax.add_patch(plt.Circle((0, 0), 0.85, fill=False, lw=2))
ax.add_patch(plt.Circle((0, 0), 0.62, fill=False, lw=1.2, ls="--"))
ax.text(-0.75, -1.0, "$J=mR^2$", fontsize=9)
# sphere
ax = axes[3]
ax.add_patch(plt.Circle((0, 0), 0.85, fill=False, lw=2))
ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 1.2, 1.7, theta1=0, theta2=360, lw=0.8, ls=":"))
ax.text(-0.78, -1.0, "$J=\\frac{2}{5}mR^2$", fontsize=9)
save(fig, "fig_l13_inertia_shapes.png")

# ---------- L13-2 平行轴 ----------
fig, ax = plt.subplots(figsize=(4.8, 3.4))
ax.set_xlim(-0.4, 3.6)
ax.set_ylim(-1.6, 1.6)
ax.set_aspect("equal")
ax.axis("off")
ax.add_patch(plt.Circle((1.6, 0), 1.2, fill=False, lw=1.6))
ax.plot(1.6, 0, "o", ms=5, color="C3")
ax.text(1.68, 0.1, "$C$（质心）", fontsize=9, color="C3")
ax.plot([1.6, 1.6], [-1.4, 1.4], color="C3", lw=1.2, ls="--")
ax.plot(0.2, 0, "o", ms=5, color="C0")
ax.text(-0.2, -0.25, "$O$", fontsize=9, color="C0")
ax.plot([0.2, 0.2], [-1.4, 1.4], color="C0", lw=1.2, ls="--")
ax.annotate("", xy=(1.6, -1.15), xytext=(0.2, -1.15), arrowprops=dict(arrowstyle="<->", lw=0.9))
ax.text(0.8, -1.45, "$d$", fontsize=10)
ax.text(-0.3, 1.1, "$J_O=J_C+md^2$", fontsize=10)
ax.set_title("平行轴定理：轴越远，转动惯量越大", fontsize=10)
save(fig, "fig_l13_parallel_axis.png")

# ---------- L14-1 斜面轮受力 ----------
fig, ax = plt.subplots(figsize=(5.4, 3.4))
ax.set_xlim(-0.3, 5.0)
ax.set_ylim(-0.3, 2.6)
ax.set_aspect("equal")
ax.axis("off")
th = np.deg2rad(28)
ax.plot([0, 4.6], [0, 4.6 * np.tan(th)], color="k", lw=1.6)
ax.plot([0, 4.6], [0, 0], color="k", lw=0.8, ls="--")
C = np.array([2.3, 2.3 * np.tan(th) + 0.65])
R = 0.55
ax.add_patch(plt.Circle(C, R, fill=False, lw=1.8))
ax.plot(*C, "o", ms=4, color="k")
arr(ax, C[0], C[1], C[0], C[1] - 0.95, color="C3", text="$mg$", tx=0.12)
Ndir = np.array([-np.sin(th), np.cos(th)])
arr(ax, C[0] - R * np.sin(th), C[1] + R * np.cos(th), C[0] - R * np.sin(th) + 0.8 * Ndir[0],
    C[1] + R * np.cos(th) + 0.8 * Ndir[1], color="C0", text="$N$", tx=-0.1)
tdir = np.array([np.cos(th), np.sin(th)])
arr(ax, C[0] - R * np.sin(th), C[1] + R * np.cos(th), C[0] - R * np.sin(th) + 0.7 * tdir[0],
    C[1] + R * np.cos(th) + 0.7 * tdir[1], color="C1", text="$F$", tx=0.1, ty=0.12)
arr(ax, C[0], C[1], C[0] + 0.8 * tdir[0], C[1] + 0.8 * tdir[1], color="C2", text="$a$", tx=0.05, ty=0.14)
ax.add_patch(plt.matplotlib.patches.Arc(C, 0.5, 0.5, theta1=-40, theta2=20, color="C4", lw=1.3))
ax.text(C[0] + 0.28, C[1] - 0.35, "$\\alpha$", color="C4", fontsize=9)
ax.text(0.2, 2.2, "纯滚动约束：$a=\\alpha R$；静摩擦 $F$ 向上", fontsize=9)
ax.set_title("斜面滚轮：重力、法向、静摩擦与运动量", fontsize=10)
save(fig, "fig_l14_incline_wheel.png")

# ---------- L14-2 线团 ----------
fig, ax = plt.subplots(figsize=(4.8, 3.4))
ax.set_xlim(-0.4, 3.6)
ax.set_ylim(-0.5, 3.0)
ax.set_aspect("equal")
ax.axis("off")
R, r = 1.0, 0.5
C = np.array([1.5, 1.1])
ax.add_patch(plt.Circle(C, R, fill=False, lw=1.8))
ax.add_patch(plt.Circle(C, r, fill=False, lw=1.0, ls="--"))
ax.plot(*C, "o", ms=4, color="k")
h = 0.55
arr(ax, C[0] + r, C[1] + h, C[0] + r + 1.2, C[1] + h, color="C3", text="$P$", tx=0.35, ty=0.12)
ax.plot([C[0], C[0] + r], [C[1] + h, C[1] + h], color="C3", lw=1.2)
ax.annotate("", xy=(C[0], C[1] + h), xytext=(C[0], C[1]), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.text(C[0] + 0.06, C[1] + h / 2, "$h$", fontsize=9)
ax.plot([C[0] - R, C[0] + R], [0, 0], color="k", lw=1.8)
ax.plot(C[0], 0, "o", ms=4, color="C2")
ax.text(C[0] - 0.7, -0.3, "接地点（瞬心）", fontsize=8.5, color="C2")
ax.text(-0.35, 2.65, "拉力在轴上方 $h$ 处：$a=\\dfrac{2P(1-h/R)}{3m}$", fontsize=9)
ax.set_title("线团悖论：拉力位置决定前进还是后退", fontsize=10)
save(fig, "fig_l14_spool.png")

# ---------- L15-2 路径相关 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.2))
ax = axes[0]
ax.set_xlim(-0.2, 5.0)
ax.set_ylim(-0.2, 3.6)
ax.axis("off")
ax.plot([0, 0], [3, 0.6], color="k", lw=1.0, ls=":")
ax.text(-0.45, 3.0, "$A$", fontsize=10)
ax.text(-0.45, 0.45, "$B$", fontsize=10)
ax.plot([0, 2.2, 4.2], [3, 0.6, 0.6], color="C0", lw=1.6)
ax.plot([0, 4.2], [3, 0.6], color="C3", lw=1.4, ls="--")
ax.text(1.4, 2.0, "路径 1", color="C0", fontsize=9)
ax.text(1.5, 1.25, "路径 2（直下）", color="C3", fontsize=9)
ax.text(0.1, -0.1, "重力：两条路径做功都是 $mg(h_A-h_B)$", fontsize=9)
ax.set_title("重力：只看高差，与路径无关", fontsize=10)
ax = axes[1]
ax.set_xlim(-0.2, 5.0)
ax.set_ylim(-0.2, 3.6)
ax.axis("off")
ax.plot([0, 4.2], [2.8, 2.8], color="k", lw=3)
ax.plot([0, 0], [2.8, 0.3], color="gray", lw=0.8, ls=":")
BL = np.array([0.3, 0.3])
TL = np.array([3.9, 2.5])
ax.annotate("", xy=TL, xytext=BL, arrowprops=dict(arrowstyle="-|>", lw=1.2, color="C3"))
ax.annotate("", xy=(3.9, 0.3), xytext=(0.3, 0.3), arrowprops=dict(arrowstyle="-|>", lw=1.2, color="C0"))
ax.annotate("", xy=(3.9, 2.5), xytext=(3.9, 0.3), arrowprops=dict(arrowstyle="-|>", lw=1.2, color="C0"))
ax.text(1.5, 1.7, "斜线 $L_1$", color="C3", fontsize=9)
ax.text(1.4, 0.1, "折线 $L_1+L_2$", color="C0", fontsize=9)
ax.text(0.1, -0.1, "摩擦功 $-fN\\times$ 路程：折线更长，耗得更多", fontsize=9)
ax.set_title("摩擦：路程越长，耗散越多（路径有关）", fontsize=10)
save(fig, "fig_l15_paths.png")

# ---------- L16-1 选型流程 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")


def box(x, y, w, h, text, fc="#DCE9F7"):
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=fc, edgecolor="none"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.5)


box(3.4, 8.6, 3.2, 0.9, "要求什么量？", "#F3E1D7")
box(0.3, 6.6, 2.9, 1.1, "时间 / 平均力\n→ 动量定理")
box(3.55, 6.6, 2.9, 1.1, "转角 / 角速度\n→ 动量矩定理")
box(6.8, 6.6, 2.9, 1.1, "速度 / 位移\n→ 动能定理")
box(0.3, 4.5, 2.9, 1.1, "加速度 / 约束力\n→ 牛二、三件套")
box(3.55, 4.5, 2.9, 1.1, "碰后速度\n→ 守恒 + 恢复系数")
box(0.3, 2.3, 9.4, 1.2, "先扫守恒三关：主矢零 → 动量；外矩零 → 动量矩；只有保守力做功 → 机械能", "#E3F2E1")
for x in (1.75, 5.0, 8.25):
    ax.annotate("", xy=(x, 7.75), xytext=(5.0, 8.55), arrowprops=dict(arrowstyle="-|>", lw=1.0, color="gray"))
for x in (1.75, 5.0):
    ax.annotate("", xy=(x, 5.65), xytext=(x, 6.55), arrowprops=dict(arrowstyle="-|>", lw=1.0, color="gray"))
ax.annotate("", xy=(5.0, 3.55), xytext=(5.0, 4.45), arrowprops=dict(arrowstyle="-|>", lw=1.0, color="gray"))
ax.set_title("三大定理选型：按所求量分流", fontsize=11)
save(fig, "fig_l16_selection.png")

# ---------- L16-2 对心正碰 ----------
fig, axes = plt.subplots(2, 1, figsize=(6.4, 3.2))
for ax in axes:
    ax.set_xlim(0, 7.4)
    ax.set_ylim(-0.6, 1.6)
    ax.axis("off")
ax = axes[0]
ax.add_patch(plt.Circle((1.5, 0.5), 0.4, fill=False, lw=1.4))
ax.text(1.3, 1.0, "$m_1$", fontsize=9)
arr(ax, 1.9, 0.5, 2.9, 0.5, color="C0", text="$v_1$", ty=0.16)
ax.add_patch(plt.Circle((4.6, 0.5), 0.55, fill=False, lw=1.4))
ax.text(4.45, 1.0, "$m_2$", fontsize=9)
arr(ax, 5.15, 0.5, 5.9, 0.5, color="C0", text="$v_2$", ty=0.16)
ax.text(3.0, -0.35, "碰前", fontsize=9, color="gray")
ax = axes[1]
ax.add_patch(plt.Circle((2.0, 0.5), 0.4, fill=False, lw=1.4))
ax.text(1.8, 1.0, "$m_1$", fontsize=9)
arr(ax, 1.6, 0.5, 0.8, 0.5, color="C3", text="$v_1'$", ty=0.16)
ax.add_patch(plt.Circle((4.6, 0.55), 0.55, fill=False, lw=1.4))
ax.text(4.45, 1.05, "$m_2$", fontsize=9)
arr(ax, 5.15, 0.55, 6.2, 0.55, color="C3", text="$v_2'$", ty=0.18)
ax.text(3.1, -0.35, "碰后：$e=\\dfrac{v_2'-v_1'}{v_1-v_2}$", fontsize=9, color="gray")
ax.set_title("对心正碰：动量守恒 + 恢复系数", fontsize=10)
save(fig, "fig_l16_collision.png")

# ---------- L17-1 惯性力系三形态 ----------
fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.0))
for ax, title in zip(axes, ["平移：合力过质心", "定轴转动：合力 + 力偶", "平面运动：合力过 C + 力偶"]):
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=9)
# translation
ax = axes[0]
ax.add_patch(plt.Rectangle((-0.9, -0.4), 1.8, 0.8, fill=False, lw=1.4))
ax.plot(0, 0, "o", ms=4, color="k")
arr(ax, 0, 0, 0, -0.9, color="C3")
ax.text(0.55, -0.55, "$-Ma_C$", fontsize=9, color="C3")
# fixed axis
ax = axes[1]
ax.add_patch(plt.Circle((0, 0), 0.9, fill=False, lw=1.4))
ax.plot(0, 0, "o", ms=5, color="C1")
ax.text(0.1, -0.2, "$O$", color="C1", fontsize=9)
ax.plot(0.35, 0.35, "o", ms=4, color="k")
ax.text(0.42, 0.45, "$C$", fontsize=9)
arr(ax, 0, 0, 0, -0.85, color="C3")
ax.text(0.5, -0.55, "$-Ma_C$", fontsize=9, color="C3")
ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 0.7, 0.7, theta1=200, theta2=340, color="C4", lw=1.4))
ax.text(-1.15, -0.62, "$-J_O\\alpha$", color="C4", fontsize=8.5)
# planar
ax = axes[2]
ax.add_patch(plt.Rectangle((-0.9, -0.35), 1.8, 0.7, fill=False, lw=1.4))
ax.plot(0, 0, "o", ms=4, color="k")
ax.text(0.1, 0.12, "$C$", fontsize=9)
arr(ax, 0, 0, 0, -0.8, color="C3")
ax.text(0.5, -0.5, "$-Ma_C$", fontsize=9, color="C3")
ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 0.62, 0.62, theta1=200, theta2=340, color="C4", lw=1.4))
ax.text(-1.05, -0.6, "$-J_C\\alpha$", color="C4", fontsize=8.5)
save(fig, "fig_l17_inertial_systems.png")

# ---------- L17-2 偏心转子 ----------
fig, ax = plt.subplots(figsize=(4.4, 3.8))
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_aspect("equal")
ax.axis("off")
ax.add_patch(plt.Circle((0, 0), 1.25, fill=False, lw=1.5))
ax.plot(0, 0, "o", ms=5, color="C1")
ax.text(-0.18, -0.18, "$O$", color="C1", fontsize=9)
e = 0.35
ax.plot(e, 0, "o", ms=6, color="C3")
ax.text(e + 0.08, 0.1, "$C$（偏心 $e$）", fontsize=9, color="C3")
ax.annotate("", xy=(e, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=1.0))
ax.text(e / 2, 0.08, "$e$", fontsize=9)
arr(ax, e, 0, e + 0.55, 0, color="C0", text="$me\\omega^2$", tx=0.1, ty=0.18)
arr(ax, 0, 0, -0.45, 0, color="C4", text="$R$", tx=-0.15, ty=0.18)
ax.text(-1.55, -1.35, "动反力 $R\\approx me\\omega^2$；转速翻倍，反力变 4 倍", fontsize=9)
ax.set_title("偏心转子：动反力的来源", fontsize=10)
save(fig, "fig_l17_eccentric.png")

# ---------- L18-1 虚位移 ----------
fig, ax = plt.subplots(figsize=(4.8, 3.6))
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.7, 0.3)
ax.set_aspect("equal")
ax.axis("off")
O = np.array([0, 0])
L = 1.3
th0 = np.deg2rad(35)
B0 = O + L * np.array([-np.sin(th0), -np.cos(th0)])
th1 = th0 + np.deg2rad(8)
B1 = O + L * np.array([-np.sin(th1), -np.cos(th1)])
ax.plot([-0.5, 0.5], [0, 0], color="k", lw=2)
ax.plot([O[0], B0[0]], [O[1], B0[1]], color="k", lw=1.6)
ax.add_patch(plt.Circle(B0, 0.1, color="C0"))
ax.plot([O[0], B1[0]], [O[1], B1[1]], color="C3", lw=1.4, ls="--")
ax.add_patch(plt.Circle(B1, 0.1, fill=False, lw=1.2, ls="--", edgecolor="C3"))
ax.add_patch(plt.matplotlib.patches.Arc(O, 1.0, 1.0, theta1=270 + 35, theta2=270 + 43, color="C3", lw=1.0))
ax.text(O[0] - 0.28, O[1] - 0.5, "$\\delta\\theta$", color="C3", fontsize=9)
ax.annotate("", xy=(B1[0], B1[1]), xytext=(B0[0], B0[1]),
            arrowprops=dict(arrowstyle="-|>", lw=1.2, color="C1"))
ax.text(B1[0] - 0.55, B1[1] - 0.1, "$\\delta r$（虚位移）", color="C1", fontsize=9)
ax.text(-1.5, 0.15, "时间冻结：只沿约束允许的方向挪，不问实际发生与否", fontsize=8.8)
ax.set_title("虚位移：同一时刻的假想微小位移", fontsize=10)
save(fig, "fig_l18_virtual.png")

# ---------- L18-2 解除约束 ----------
fig, ax = plt.subplots(figsize=(5.6, 3.0))
ax.set_xlim(-0.4, 5.2)
ax.set_ylim(-0.7, 1.6)
ax.set_aspect("equal")
ax.axis("off")
ax.plot([0, 4.2], [0, 0], color="k", lw=3)
ax.plot([0, 0], [0, -0.45], color="k", lw=1.2)
ax.plot([-0.22, 0, 0.22], [-0.45, 0, -0.45], color="k", lw=1.0)
arr(ax, 1.0, 1.0, 1.0, 0.05, color="C3", text="$P$", tx=0.1)
ax.plot(4.2, 0, "o", ms=5, color="gray")
ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 0.7, 0.7, theta1=0, theta2=12, color="C1", lw=1.2))
ax.text(0.62, -0.25, "$\\delta\\theta$", color="C1", fontsize=9)
arr(ax, 4.2, 0, 4.2, 0.75, color="C0", text="$R_B$（升格为主动力）", tx=0.0, ty=0.1)
ax.text(0.1, -0.62, "解除 B 支座：梁绕 A 转，用虚功求 $R_B$", fontsize=9)
ax.set_title("解除约束技巧：求谁就放开谁", fontsize=10)
save(fig, "fig_l18_release.png")

# ---------- L19-2 拉格朗日流程 ----------
fig, ax = plt.subplots(figsize=(6.4, 3.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")
steps = [
    ("① 选广义坐标", "数自由度，选 $q_1,\\dots,q_k$", 8.2),
    ("② 写动能与势能", "用 $q$、$\\dot q$ 表出 $T$、$V$", 5.9),
    ("③ 求广义力", "虚功法：$\\delta W=\\sum Q_j\\delta q_j$", 3.6),
    ("④ 代入方程", "$\\dfrac{d}{dt}\\dfrac{\\partial T}{\\partial\\dot q_j}-\\dfrac{\\partial T}{\\partial q_j}=Q_j$", 1.3),
]
for i, (t1, t2, y) in enumerate(steps):
    ax.add_patch(plt.Rectangle((1.0, y - 0.55), 8.0, 1.15, facecolor="#DCE9F7", edgecolor="none"))
    ax.text(1.25, y + 0.25, t1, fontsize=10.5, fontweight="bold")
    ax.text(1.25, y - 0.22, t2, fontsize=8.8, color="#333333")
    if i < 3:
        ax.annotate("", xy=(5, y - 0.75), xytext=(5, y - 0.5),
                    arrowprops=dict(arrowstyle="-|>", lw=1.1, color="gray"))
ax.set_title("拉格朗日方法：四步流水线（约束力不出现）", fontsize=10.5)
save(fig, "fig_l19_flow.png")

# ---------- L20-3 暂态与稳态 ----------
fig, ax = plt.subplots(figsize=(6.2, 3.0))
t = np.linspace(0, 12, 800)
zeta, wn = 0.12, 2.0
wd = wn * np.sqrt(1 - zeta ** 2)
trans = 0.9 * np.exp(-zeta * wn * t)
steady = 0.5 * np.sin(2.6 * t)
ax.plot(t, trans, color="C0", lw=0.9, ls="--", label="暂态包络")
ax.plot(t, steady, color="C2", lw=1.0, ls=":", label="稳态（激励频率）")
ax.plot(t, trans + steady + 0.35 * np.exp(-zeta * wn * t) * np.cos(wd * t),
        color="C3", lw=1.2, label="总响应")
ax.axhline(0, color="k", lw=0.5)
ax.set_xlabel("时间 $t$")
ax.set_ylabel("位移 $x$")
ax.set_xlim(0, 12)
ax.legend(frameon=False, fontsize=8.5)
ax.set_title("受迫振动：暂态衰减后只剩稳态", fontsize=10)
save(fig, "fig_l20_transient.png")

# ---------- L21-2 主振型 ----------
fig, axes = plt.subplots(2, 1, figsize=(6.6, 3.6))
for ax in axes:
    ax.set_xlim(0, 7.6)
    ax.set_ylim(-0.8, 1.8)
    ax.axis("off")
    ax.plot([0, 0.3], [0.5, 0.5], color="k", lw=2)
    ax.plot([6.9, 7.2], [0.5, 0.5], color="k", lw=2)
    ax.plot([0.3, 2.4], [0.5, 0.5], color="gray", lw=1.0, ls="--")
    ax.plot([3.2, 5.3], [0.5, 0.5], color="gray", lw=1.0, ls="--")
    ax.plot([6.1, 6.9], [0.5, 0.5], color="gray", lw=1.0, ls="--")
ax = axes[0]
ax.add_patch(plt.Rectangle((2.4, 0.1), 0.8, 0.8, fill=False, lw=1.4))
ax.add_patch(plt.Rectangle((5.3, 0.1), 0.8, 0.8, fill=False, lw=1.4))
ax.text(2.6, 1.2, "$m_1$", fontsize=9)
ax.text(5.5, 1.2, "$m_2$", fontsize=9)
arr(ax, 2.8, 0.5, 1.9, 0.5, color="C0")
arr(ax, 5.7, 0.5, 6.6, 0.5, color="C0")
ax.text(3.4, 1.3, "低阶模态：两质量同向", fontsize=9)
ax = axes[1]
ax.add_patch(plt.Rectangle((2.4, 0.1), 0.8, 0.8, fill=False, lw=1.4))
ax.add_patch(plt.Rectangle((5.3, 0.1), 0.8, 0.8, fill=False, lw=1.4))
ax.text(2.6, 1.2, "$m_1$", fontsize=9)
ax.text(5.5, 1.2, "$m_2$", fontsize=9)
arr(ax, 2.4, 0.5, 1.5, 0.5, color="C3")
arr(ax, 6.1, 0.5, 7.0, 0.5, color="C3")
ax.text(3.4, 1.28, "高阶模态：两质量反向（中间弹簧大幅伸缩）", fontsize=8.8)
ax.set_title("主振型：两种步调，两个固有频率", fontsize=10)
save(fig, "fig_l21_modes.png")

# ---------- L21-3 动力吸振器 ----------
fig, ax = plt.subplots(figsize=(5.6, 3.0))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.plot([0, 10], [0, 0], color="k", lw=2)
# main mass
ax.add_patch(plt.Rectangle((2.6, 2.2), 2.4, 1.2, fill=False, lw=1.6))
ax.text(3.0, 2.6, "$m_1$", fontsize=11)
# spring to ground
xs = np.linspace(2.6, 0.8, 50)
ys = 1.8 + 0.12 * np.sin(np.linspace(0, 10 * np.pi, 50))
ax.plot(xs, ys, color="C0", lw=1.2)
ax.plot([0.8, 0.8], [0, 1.8], color="k", lw=1.2)
ax.text(1.1, 1.2, "$k_1$", color="C0", fontsize=10)
# absorber
ax.add_patch(plt.Rectangle((3.2, 4.0), 1.2, 0.8, fill=False, lw=1.4))
ax.text(3.35, 4.25, "$m_2$", fontsize=10)
xs2 = np.linspace(3.2, 3.2, 2)
ax.plot([3.8, 3.8], [3.4, 4.0], color="C1", lw=1.0)
ax.plot([3.8, 3.8], [3.4, 4.0], color="C1", lw=1.0)
ys2 = np.linspace(3.4, 4.0, 40)
xs3 = 3.8 + 0.1 * np.sin(np.linspace(0, 8 * np.pi, 40))
ax.plot(xs3, ys2, color="C1", lw=1.2)
ax.text(3.95, 3.6, "$k_2$", color="C1", fontsize=10)
arr(ax, 5.0, 2.8, 6.2, 2.8, color="C3", text="$F(t)$", ty=0.2)
ax.text(0.2, 5.2, "主结构受激；吸振器调谐到 $\\omega=\\sqrt{k_2/m_2}=\\Omega$ 时，主质量振幅趋于零", fontsize=9)
ax.set_title("动力吸振器：振动转嫁给小振子", fontsize=10)
save(fig, "fig_l21_absorber.png")

print("batch B done")
