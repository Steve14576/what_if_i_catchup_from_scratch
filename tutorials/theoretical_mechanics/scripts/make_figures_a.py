# 配图第一批：L01-L11（17 张）
# 用法：uv run --offline --with matplotlib python scripts/make_figures_a.py
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


def arr(ax, x0, y0, x1, y1, color="k", lw=1.5, text=None, tx=0, ty=0, fs=9, ha="center"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0))
    if text:
        ax.text((x0 + x1) / 2 + tx, (y0 + y1) / 2 + ty, text, color=color, fontsize=fs, ha=ha, va="center")


# ---------- L01-2 约束类型 ----------
fig, axes = plt.subplots(1, 5, figsize=(9.6, 2.6))
titles = ["柔索（绳）", "光滑接触面", "圆柱铰链", "链杆（二力杆）", "固定端"]
for ax, t in zip(axes, titles):
    ax.set_xlim(-0.9, 0.9)
    ax.set_ylim(-0.9, 1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(t, fontsize=9)

ax = axes[0]
ax.plot([-0.5, 0.5], [0.9, 0.9], color="k", lw=2.0)
for xs in np.linspace(-0.5, 0.5, 6):
    ax.plot([xs, xs - 0.05], [0.9, 0.98], color="k", lw=0.7)
ball = np.array([0.22, 0.18])
ax.plot([0.0, ball[0]], [0.9, ball[1] + 0.13], color="k", lw=1.1)
ax.add_patch(plt.Circle(ball, 0.13, fill=False, lw=1.1))
d = np.array([-0.22, 0.72])
d = d / np.hypot(*d)
arr(ax, ball[0], ball[1], ball[0] + 0.5 * d[0], ball[1] + 0.5 * d[1], color="C3", text="$T$", tx=-0.08, ty=0.12)

ax = axes[1]
ax.plot([-0.8, 0.8], [-0.25, -0.25], color="k", lw=2.0)
for xs in np.linspace(-0.8, 0.8, 8):
    ax.plot([xs, xs - 0.05], [-0.25, -0.18], color="k", lw=0.7)
ax.add_patch(plt.Rectangle((-0.28, -0.25), 0.56, 0.34, fill=False, lw=1.1))
arr(ax, 0, -0.25, 0, 0.32, color="C0", text="$N$", tx=0.12, ty=0.02)

ax = axes[2]
ax.plot([-0.8, 0.8], [-0.45, -0.45], color="k", lw=2.0)
for xs in np.linspace(-0.8, 0.8, 8):
    ax.plot([xs, xs - 0.05], [-0.45, -0.38], color="k", lw=0.7)
ax.plot([-0.22, 0, 0.22], [-0.45, 0, -0.45], color="k", lw=1.0)
ax.plot(0, 0, "o", ms=6, color="k")
ax.plot([0, 0.75], [0, 0], color="k", lw=2.4)
arr(ax, 0, 0, 0.5, 0.36, color="C1", text="$F_x$", tx=0.08, ty=0.1)
arr(ax, 0, 0, 0, -0.32, color="C1", text="$F_y$", tx=0.12)

ax = axes[3]
ax.plot([-0.62, 0.62], [0.35, 0.35], color="k", lw=2.4)
ax.plot([-0.62, 0.62], [0.35, 0.35], "o", ms=5, color="k")
arr(ax, 0.62, 0.35, 0.85, 0.35, color="C2")
arr(ax, -0.62, 0.35, -0.85, 0.35, color="C2")
ax.text(0, 0.12, "力沿杆轴", fontsize=8.5, color="C2", ha="center")

ax = axes[4]
ax.plot([-0.45, -0.45], [-0.7, 0.7], color="k", lw=3.0)
for ys in np.linspace(-0.7, 0.7, 8):
    ax.plot([-0.45, -0.38], [ys, ys + 0.05], color="k", lw=0.7)
ax.plot([-0.45, 0.75], [0, 0], color="k", lw=3.0)
arr(ax, -0.45, 0, -0.45, 0.5, color="C3", text="$F_y$", tx=-0.2)
arr(ax, -0.45, 0, -0.05, 0, color="C3", text="$F_x$", ty=-0.16)
ax.add_patch(plt.matplotlib.patches.Arc((-0.45, 0), 0.3, 0.3, theta1=200, theta2=340, color="C1", lw=1.3))
ax.text(-0.15, 0.18, "$M$", color="C1", fontsize=9)
save(fig, "fig_l01_constraints.png")

# ---------- L02-2 分布载荷等效 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.0))
ax = axes[0]
ax.set_xlim(-0.2, 4.4)
ax.set_ylim(-0.2, 2.0)
ax.axis("off")
for x in np.linspace(0.1, 3.9, 12):
    arr(ax, x, 1.2, x, 0.05, color="C0", lw=0.9)
ax.plot([0, 4], [1.2, 1.2], color="C0", lw=1.2)
ax.plot([0, 4], [0, 0], color="k", lw=3)
arr(ax, 2, 1.6, 2, 0.05, color="C3", lw=2.0)
ax.text(2.15, 1.55, "$qL$", color="C3", fontsize=10)
ax.annotate("", xy=(2, -0.15), xytext=(0, -0.15), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.annotate("", xy=(4, -0.15), xytext=(2, -0.15), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.text(1.0, -0.33, "$L/2$", fontsize=9)
ax.text(3.0, -0.33, "$L/2$", fontsize=9)
ax.set_title("均布载荷：合力 $qL$，作用在中点", fontsize=10)

ax = axes[1]
ax.set_xlim(-0.2, 4.4)
ax.set_ylim(-0.2, 2.0)
ax.axis("off")
for x in np.linspace(0.05, 3.95, 14):
    arr(ax, x, 0.2 + 1.0 * x / 4, x, 0.05, color="C0", lw=0.8)
ax.plot([0, 4], [0.2, 1.2], color="C0", lw=1.2)
ax.plot([0, 4], [0, 0], color="k", lw=3)
arr(ax, 4 / 3, 1.35, 4 / 3, 0.05, color="C3", lw=2.0)
ax.text(4 / 3 + 0.12, 1.3, "$qL/2$", color="C3", fontsize=10)
ax.annotate("", xy=(4 / 3, -0.15), xytext=(0, -0.15), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.annotate("", xy=(4, -0.15), xytext=(4 / 3, -0.15), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.text(0.55, -0.33, "$L/3$", fontsize=9)
ax.text(2.6, -0.33, "$2L/3$", fontsize=9)
ax.set_title("三角形载荷：合力 $qL/2$，作用线过形心（距大端 $L/3$）", fontsize=10)
save(fig, "fig_l02_distributed.png")

# ---------- L03-1 桁架节点法 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.4))
ax = axes[0]
ax.set_xlim(-0.3, 2.6)
ax.set_ylim(-0.5, 1.8)
ax.set_aspect("equal")
ax.axis("off")
A, B, C = np.array([0, 0]), np.array([2.0, 0]), np.array([1.0, 1.2])
for P, Q in [(A, B), (A, C), (B, C)]:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color="k", lw=2.0)
for P, name, off in [(A, "A", (-0.12, -0.1)), (B, "B", (0.1, -0.1)), (C, "C", (-0.22, 1.12))]:
    ax.plot(*P, "o", ms=5, color="k")
    ax.text(P[0] + off[0], P[1] + off[1], name, fontsize=10)
# pin support A
ax.plot([-0.18, 0, 0.18], [-0.3, 0, -0.3], color="k", lw=1.0)
ax.plot([-0.26, 0.26], [-0.32, -0.32], color="k", lw=1.0)
# roller B
ax.plot([1.88, 2.0, 2.12], [-0.3, 0, -0.3], color="k", lw=1.0)
ax.add_patch(plt.Circle((1.95, -0.35), 0.05, fill=False, lw=0.9))
ax.add_patch(plt.Circle((2.05, -0.35), 0.05, fill=False, lw=0.9))
ax.plot([1.85, 2.15], [-0.41, -0.41], color="k", lw=1.0)
arr(ax, 1.0, 1.62, 1.0, 1.24, color="C3")
ax.text(1.1, 1.5, "$P$", color="C3", fontsize=10)
ax.set_title("简单桁架：先数未知量再解", fontsize=10)

ax = axes[1]
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect("equal")
ax.axis("off")
ax.plot(0, 0, "o", ms=9, color="C0")
ax.text(-0.28, -0.2, "节点 C", fontsize=9)
arr(ax, 0, 0, -0.75, -0.75, color="C1")
ax.text(-0.95, -0.7, "$N_{AC}$", color="C1", fontsize=9)
arr(ax, 0, 0, 0.75, -0.75, color="C1")
ax.text(0.62, -0.7, "$N_{BC}$", color="C1", fontsize=9)
arr(ax, 0, 0, 0, 0.85, color="C3")
ax.text(0.15, 0.55, "$P$", color="C3", fontsize=10)
ax.text(0, -1.05, "汇交力系：$\\sum F_x=0,\\ \\sum F_y=0$ 解两杆内力", fontsize=9, ha="center")
ax.set_title("节点法：把每个节点当汇交力系", fontsize=10)
save(fig, "fig_l03_truss_node.png")

# ---------- L03-2 零杆判别 ----------
fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2))
for k, ax in enumerate(axes):
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")
    ax.axis("off")
ax = axes[0]
ax.plot([-0.8, 0.8], [0, 0], color="k", lw=2)
ax.plot([0, 0], [0, -0.8], color="C3", lw=2, ls="--")
ax.plot(0, 0, "o", ms=7, color="C0")
ax.text(0.08, 0.08, "无载荷", fontsize=9)
ax.text(0.1, -0.55, "两杆汇交且无外力\n→ 两杆均为零杆", fontsize=9, color="C3")
ax.set_title("情形一：两杆节点", fontsize=10)
ax = axes[1]
ax.plot([-0.8, 0.8], [0, 0], color="k", lw=2)
ax.plot([0, 0], [0, -0.85], color="C3", lw=2, ls="--")
ax.plot(0, 0, "o", ms=7, color="C0")
ax.text(0.1, -0.55, "同一直线两杆 + 第三杆\n无外力 → 第三杆为零杆", fontsize=9, color="C3")
ax.set_title("情形二：三杆节点（两杆共线）", fontsize=10)
save(fig, "fig_l03_zero_force.png")

# ---------- L04-1 二次投影 ----------
fig, ax = plt.subplots(figsize=(4.8, 3.8))
ax.set_xlim(-0.2, 3.2)
ax.set_ylim(-0.4, 3.0)
ax.set_aspect("equal")
ax.axis("off")
O = np.array([0, 0])
ax.annotate("", xy=(2.6, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=1.0))
ax.annotate("", xy=(0, 2.4), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=1.0))
ax.annotate("", xy=(-0.9, -0.6), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=1.0))
ax.text(2.65, -0.05, "$x$", fontsize=10)
ax.text(-0.05, 2.45, "$y$", fontsize=10)
ax.text(-0.95, -0.72, "$z$", fontsize=10)
F = np.array([1.9, 1.5])
ax.annotate("", xy=F, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=2.0, color="C3"))
ax.text(F[0] + 0.08, F[1], "$F$", color="C3", fontsize=11)
ax.plot([F[0], F[0]], [0, F[1]], color="gray", lw=1.0, ls="--")
ax.plot([0, F[0]], [0, 0], color="C0", lw=1.6)
ax.plot([F[0], F[0]], [F[1], 0], color="C0", lw=0.8, ls=":")
ax.text(F[0] / 2, -0.18, "$F_{xy}$", color="C0", fontsize=9)
ax.text(F[0] - 0.55, F[1] / 2, "$F_z$", color="C0", fontsize=9)
ax.text(1.55, 0.75, "$\\varphi$（与 $x$ 轴）", fontsize=8.5, color="gray")
ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 0.9, 0.9, theta1=0, theta2=38, color="gray", lw=0.8))
ax.text(1.2, 2.2, "先投影到坐标面 $Oxy$\n再投影到两轴", fontsize=9)
ax.set_title("二次投影：一次得 $F_{xy}$，二次得 $F_x,F_y$", fontsize=10)
save(fig, "fig_l04_projection.png")

# ---------- L05-2 先滑还是先翻 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.0))
for ax in axes:
    ax.set_xlim(-0.2, 3.5)
    ax.set_ylim(-0.2, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.plot([0, 3.2], [0, 0], color="k", lw=1.5)
    ax.plot([0.4, 0.9, 0.9, 0.4, 0.4], [0, 0, 1.0, 1.0, 0], color="k", lw=1.2)
ax = axes[0]
arr(ax, 1.4, 0.9, 2.4, 0.9, color="C3", text="$P$", ty=0.12)
arr(ax, 0.4, 0.02, 0.4, 0.02, color="C0")
ax.annotate("", xy=(1.4, 0), xytext=(0.9, 0), arrowprops=dict(arrowstyle="-|>", lw=1.5, color="C0"))
ax.text(1.0, -0.2, "$F$", color="C0", fontsize=9)
ax.text(1.6, 1.45, "滑：$P > f_s N$", fontsize=10, color="C3")
ax.set_title("先滑：接触面先失效", fontsize=10)
ax = axes[1]
arr(ax, 1.4, 1.0, 2.2, 1.4, color="C3", text="$P$", tx=0.1, ty=0.05)
ax.add_patch(plt.matplotlib.patches.Arc((1.4, 0), 0.5, 0.5, theta1=30, theta2=100, color="C1", lw=1.4))
ax.annotate("", xy=(1.05, 0.35), xytext=(1.25, 0.15), arrowprops=dict(arrowstyle="-|>", lw=1.0, color="C1"))
ax.text(1.55, 1.6, "翻：绕右下角转动", fontsize=10, color="C1")
ax.set_title("先翻：绕棱边先失稳", fontsize=10)
save(fig, "fig_l05_slide_tip.png")

# ---------- L06-1 自然坐标三向量 ----------
fig, ax = plt.subplots(figsize=(5.0, 3.6))
ax.set_xlim(-0.3, 3.4)
ax.set_ylim(-1.3, 1.8)
ax.set_aspect("equal")
ax.axis("off")
t = np.linspace(0, 1, 200)
x = 0.3 + 2.8 * t
y = 0.8 * np.sin(np.pi * t)
ax.plot(x, y, color="k", lw=2.0)
i = 140
ax.plot(x[i], y[i], "o", ms=6, color="C0")
dx, dy = x[i + 1] - x[i], y[i + 1] - y[i]
n = np.hypot(dx, dy)
tx, ty = dx / n, dy / n
arr(ax, x[i], y[i], x[i] + 0.55 * tx, y[i] + 0.55 * ty, color="C3", text="$\\tau$", tx=0.1)
arr(ax, x[i], y[i], x[i] - 0.45 * ty, y[i] + 0.45 * tx, color="C1", text="$n$", tx=-0.08, ty=0.12)
# curvature circle (approx)
cx, cy = x[i] - 0.9 * ty, y[i] + 0.9 * tx
ax.add_patch(plt.Circle((cx, cy), 0.9, fill=False, ls="--", lw=0.9, color="gray"))
ax.plot(cx, cy, "+", ms=6, color="gray")
ax.text(cx + 0.1, cy + 0.05, "曲率中心", fontsize=8.5, color="gray")
ax.text(0.35, -0.95, "$s$ 沿轨迹增大方向；$\\tau$ 绑正方向，$n$ 指凹侧", fontsize=9)
ax.set_title("自然坐标：$\\tau$、$n$ 与曲率圆", fontsize=10)
save(fig, "fig_l06_natural_triad.png")

# ---------- L06-2 椭圆规 ----------
fig, ax = plt.subplots(figsize=(4.8, 3.6))
ax.set_xlim(-0.26, 0.26)
ax.set_ylim(-0.16, 0.16)
ax.set_aspect("equal")
ax.axis("off")
a, b = 0.2, 0.12
th = np.linspace(0, 2 * np.pi, 300)
ax.plot(a * np.cos(th), b * np.sin(th), color="k", lw=1.6)
phi = np.pi / 6
P = np.array([a * np.cos(phi), b * np.sin(phi)])
ax.plot(*P, "o", ms=6, color="C3")
ax.text(P[0] + 0.004, P[1] + 0.006, "$M$", fontsize=9)
arr(ax, P[0], P[1], P[0] - 0.035 * np.sin(phi), P[1] + 0.035 * np.cos(phi), color="C0")
ax.text(P[0] - 0.003, P[1] + 0.032, "$v$", color="C0", fontsize=9)
arr(ax, P[0], P[1], P[0] - 0.045 * np.cos(phi) * 0.7, P[1] - 0.045 * np.sin(phi) * 0.7, color="C1")
ax.text(P[0] - 0.04, P[1] - 0.018, "$a$", color="C1", fontsize=9)
ax.axhline(0, color="gray", lw=0.6, ls="--")
ax.axvline(0, color="gray", lw=0.6, ls="--")
ax.text(0.205, 0.003, "$a$", fontsize=9)
ax.text(0.003, 0.123, "$b$", fontsize=9)
ax.set_title("椭圆规：$x=a\\cos\\varphi,\\ y=b\\sin\\varphi$", fontsize=10)
save(fig, "fig_l06_ellipse.png")

# ---------- L07-1 齿轮传动 ----------
fig, ax = plt.subplots(figsize=(5.6, 3.2))
ax.set_xlim(-0.4, 5.2)
ax.set_ylim(-2.0, 2.0)
ax.set_aspect("equal")
ax.axis("off")
r1, r2 = 0.8, 3.0
c1, c2 = np.array([0.8, 0]), np.array([0.8 + r1 + r2, 0])
ax.add_patch(plt.Circle(c1, r1, fill=False, lw=2.0))
ax.add_patch(plt.Circle(c2, r2, fill=False, lw=2.0))
ax.plot(*c1, "o", ms=4, color="k")
ax.plot(*c2, "o", ms=4, color="k")
ax.plot([c1[0], c2[0]], [r1 * 0.75, r2 * 0.75], color="gray", lw=0.8, ls="--")
ax.text(0.8, -0.25, "主动轮 $z_1$", ha="center", fontsize=9)
ax.text(c2[0], -0.25, "从动轮 $z_2$", ha="center", fontsize=9)
ax.add_patch(plt.matplotlib.patches.Arc(c1, 0.9, 0.9, theta1=30, theta2=150, color="C0", lw=1.4))
ax.add_patch(plt.matplotlib.patches.Arc(c1, 0.9, 0.9, theta1=210, theta2=330, color="C0", lw=1.4))
ax.add_patch(plt.matplotlib.patches.Arc(c2, 1.4, 1.4, theta1=30, theta2=150, color="C3", lw=1.4))
ax.add_patch(plt.matplotlib.patches.Arc(c2, 1.4, 1.4, theta1=210, theta2=330, color="C3", lw=1.4))
ax.text(0.8, 1.05, "$\\omega_1$", color="C0", ha="center", fontsize=10)
ax.text(c2[0], 1.55, "$\\omega_2$", color="C3", ha="center", fontsize=10)
ax.text(2.3, -1.5, "$i=\\omega_1/\\omega_2=z_2/z_1=85/17=5$", fontsize=10)
ax.set_title("齿轮传动：转速与齿数成反比，转向相反", fontsize=10)
save(fig, "fig_l07_gears.png")

# ---------- L08-1 速度合成 ----------
fig, ax = plt.subplots(figsize=(4.8, 3.6))
ax.set_xlim(-0.3, 3.6)
ax.set_ylim(-0.3, 2.8)
ax.set_aspect("equal")
ax.axis("off")
ax.add_patch(plt.Rectangle((0.2, 0.2), 2.2, 1.6, fill=False, lw=1.2, ls="--"))
ax.text(0.25, 1.9, "动系（平移）", fontsize=9, color="gray")
P = np.array([1.6, 1.0])
ax.plot(*P, "o", ms=6, color="C3")
ax.text(P[0] + 0.08, P[1] + 0.04, "动点 $M$", fontsize=9)
ax.annotate("", xy=(2.6, 1.0), xytext=(0.4, 1.0), arrowprops=dict(arrowstyle="-|>", lw=1.0, ls=":"))
ax.text(2.35, 1.1, "$v_e$（牵连）", fontsize=9, color="C0")
ax.annotate("", xy=(1.6, 2.0), xytext=(1.6, 1.0), arrowprops=dict(arrowstyle="-|>", lw=1.6, color="C1"))
ax.text(1.68, 1.55, "$v_r$（相对）", fontsize=9, color="C1")
ax.annotate("", xy=(2.6, 2.0), xytext=(1.6, 1.0), arrowprops=dict(arrowstyle="-|>", lw=1.8, color="C3"))
ax.text(2.35, 1.75, "$v_a$（绝对）", fontsize=9, color="C3")
ax.text(2.35, 2.25, "$v_a=v_e+v_r$", fontsize=10)
ax.set_title("速度合成：三项构成矢量三角形", fontsize=10)
save(fig, "fig_l08_composite.png")

# ---------- L08-2 科氏加速度 ----------
fig, ax = plt.subplots(figsize=(4.6, 4.0))
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.set_aspect("equal")
ax.axis("off")
ax.add_patch(plt.Circle((0, 0), 2.0, fill=False, lw=1.4, color="k"))
ax.plot([0, 2.0], [0, 0], color="gray", lw=6, alpha=0.3)
ax.plot(0, 0, "o", ms=4, color="k")
ax.text(-0.25, -0.22, "O", fontsize=9)
M = np.array([1.1, 0])
ax.plot(*M, "s", ms=6, color="C0")
ax.text(M[0] - 0.05, M[1] - 0.3, "滑块", fontsize=9)
arr(ax, *M, M[0] + 0.75, 0, color="C1")
ax.text(M[0] + 0.25, M[1] + 0.14, "$v_r$", color="C1", fontsize=9)
arr(ax, *M, M[0], 0.7, color="C3")
ax.text(M[0] + 0.12, 0.35, "$a_c$", color="C3", fontsize=9)
ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 0.8, 0.8, theta1=20, theta2=120, color="C2", lw=1.5))
ax.annotate("", xy=(0.25, 0.55), xytext=(0.45, 0.4), arrowprops=dict(arrowstyle="-|>", lw=1.0, color="C2"))
ax.text(-1.1, 0.9, "$\\omega$（逆时针）", fontsize=9, color="C2")
ax.text(-2.0, -1.75, "滑块沿径向槽外滑：$a_c=2\\omega v_r$\n方向由 $\\omega\\times v_r$ 定（图中向上）", fontsize=9)
ax.set_title("科氏加速度：转动参考系的耦合项", fontsize=10)
save(fig, "fig_l08_coriolis.png")

# ---------- L09-2 平面运动分解 ----------
fig, ax = plt.subplots(figsize=(5.4, 3.2))
ax.set_xlim(-0.3, 4.8)
ax.set_ylim(-0.6, 2.4)
ax.set_aspect("equal")
ax.axis("off")
A = np.array([0.8, 0.6])
B = np.array([3.4, 1.4])
ax.plot([A[0], B[0]], [A[1], B[1]], color="k", lw=2.2)
ax.plot(*A, "o", ms=5, color="C0")
ax.text(A[0] - 0.1, A[1] - 0.2, "$A$（基点）", fontsize=9, color="C0")
ax.plot(*B, "o", ms=5, color="C3")
ax.text(B[0] + 0.08, B[1] + 0.05, "$B$", fontsize=9, color="C3")
# translated ghost
ax.plot([A[0] + 0.9, B[0] + 0.9], [A[1] + 0.5, B[1] + 0.5], color="gray", lw=1.6, ls="--")
ax.plot(A[0] + 0.9, A[1] + 0.5, "o", ms=4, color="C0", alpha=0.5)
arr(ax, A[0], A[1], A[0] + 0.9, A[1] + 0.5, color="C0", text="$v_A$", tx=-0.05, ty=0.12)
arr(ax, A[0] + 0.9, A[1] + 0.5, B[0] + 0.9, B[1] + 0.5, color="C1", text="$v_{BA}$", tx=0.2, ty=0.12)
ax.annotate("", xy=(B[0] + 0.35, B[1] + 0.25), xytext=(B[0] + 0.9, B[1] + 0.5),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color="gray", ls=":"))
ax.text(3.9, 0.2, "随 $A$ 平移 + 绕 $A$ 转动", fontsize=9, color="gray")
ax.set_title("平面运动分解：$v_B=v_A+v_{BA}$", fontsize=10)
save(fig, "fig_l09_decomposition.png")

# ---------- L09-3 纯滚动速度分布 ----------
fig, ax = plt.subplots(figsize=(5.0, 3.4))
ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.5, 1.7)
ax.set_aspect("equal")
ax.axis("off")
R = 1.0
ax.add_patch(plt.Circle((0, 0), R, fill=False, lw=1.6))
ax.plot([-1.6, 1.6], [-R, -R], color="k", lw=2.0)
ax.plot(0, 0, "o", ms=4, color="k")
arr(ax, 0, 0, 0.7, 0, color="C0", text="$v_C$", ty=-0.14)
arr(ax, 0, R, 1.4, R, color="C3", text="$2v_C$", ty=0.12)
arr(ax, 0, -R, 0.0, -R, color="gray")
ax.plot(0, -R, "o", ms=6, color="C2")
ax.text(0.12, -1.28, "接地点速度 = 0（瞬心）", fontsize=9, color="C2")
ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 0.6, 0.6, theta1=20, theta2=160, color="C1", lw=1.4))
ax.text(-0.1, 0.32, "$\\omega$", color="C1", fontsize=10)
ax.text(-1.6, 1.35, "$v_C=\\omega R$；顶点 $2v_C$；接地点 0", fontsize=9)
ax.set_title("纯滚动：速度按到接地点距离线性分布", fontsize=10)
save(fig, "fig_l09_rolling.png")

# ---------- L10-1 拱桥飞离 ----------
fig, ax = plt.subplots(figsize=(5.2, 3.2))
ax.set_xlim(-2.4, 2.4)
ax.set_ylim(-0.6, 2.0)
ax.set_aspect("equal")
ax.axis("off")
th = np.linspace(np.pi * 0.75, np.pi * 0.25, 100)
R = 2.0
ax.plot(R * np.cos(th), R * np.sin(th) - 0.9, color="k", lw=1.6)
ax.plot(0, 0, "s", ms=12, color="C0")
ax.text(0.12, 0.12, "车", fontsize=9)
arr(ax, 0, 0, 0, -0.75, color="C3", text="$mg$", tx=0.12)
arr(ax, 0, 0.12, 0, 0.85, color="C0", text="$N$", tx=0.12)
arr(ax, -0.35, 0.35, -0.75, 0.35, color="C1", text="$v$", tx=-0.05, ty=0.12)
ax.text(-2.2, -0.45, "桥顶：$N=mg-\\dfrac{mv^2}{R}$；$N=0$ 时飞离", fontsize=9)
ax.set_title("凸形桥顶：速度越大，支持力越小", fontsize=10)
save(fig, "fig_l10_bridge.png")

# ---------- L10-2 阻力下落 ----------
fig, ax = plt.subplots(figsize=(5.6, 3.0))
t = np.linspace(0, 6, 300)
vt, tau = 1.0, 1.0
v = vt * (1 - np.exp(-t / tau))
ax.plot(t, v, color="C0", lw=1.8)
ax.axhline(vt, color="C3", ls="--", lw=1.0)
ax.text(4.2, vt + 0.03, "终端速度 $v_t=mg/c$", color="C3", fontsize=9)
ax.axvline(tau, color="gray", ls=":", lw=1.0)
ax.text(tau + 0.08, 0.15, "$\\tau=m/c$", fontsize=9, color="gray")
ax.set_xlabel("时间 $t$")
ax.set_ylabel("速度 $v$")
ax.set_xlim(0, 6)
ax.set_ylim(0, 1.25)
ax.grid(alpha=0.2)
ax.set_title("线性阻力下落：速度指数逼近终端速度", fontsize=10)
save(fig, "fig_l10_drag.png")

# ---------- L11-1 加速车厢单摆 ----------
fig, ax = plt.subplots(figsize=(5.2, 3.4))
ax.set_xlim(-0.4, 3.4)
ax.set_ylim(-0.4, 2.9)
ax.set_aspect("equal")
ax.axis("off")
ax.plot([0.2, 2.8], [0.2, 0.2], color="k", lw=2.0)
ax.plot([0.2, 2.8], [2.4, 2.4], color="k", lw=1.0)
arr(ax, 1.5, 2.72, 2.55, 2.72, color="C1")
ax.text(2.65, 2.64, "$a$", color="C1", fontsize=10)
O = np.array([1.5, 2.4])
L = 1.4
theta = np.deg2rad(14)
B = O + np.array([-L * np.sin(theta), -L * np.cos(theta)])
ax.plot([O[0], B[0]], [O[1], B[1]], color="k", lw=1.6)
ax.add_patch(plt.Circle(B, 0.13, color="C0"))
ax.plot([O[0], O[0]], [O[1], O[1] - L], color="gray", lw=0.8, ls="--")
ax.add_patch(plt.matplotlib.patches.Arc(O, 0.7, 0.7, theta1=270, theta2=270 + 14, color="gray", lw=0.8))
ax.text(O[0] - 0.3, O[1] - 0.48, "$\\theta$", fontsize=9, color="gray")
arr(ax, B[0], B[1], B[0], B[1] - 0.45, color="C3")
ax.text(B[0] + 0.12, B[1] - 0.32, "$mg$", color="C3", fontsize=9)
arr(ax, B[0], B[1], B[0] + 0.45 * np.sin(theta), B[1] + 0.45 * np.cos(theta), color="C0")
ax.text(B[0] - 0.28, B[1] + 0.35, "$T$", color="C0", fontsize=9)
ax.annotate("", xy=(B[0] - 0.55, B[1]), xytext=(B[0], B[1]), arrowprops=dict(arrowstyle="-|>", lw=1.3, color="C1", linestyle="--"))
ax.text(B[0] - 0.62, B[1] + 0.12, "$-ma$", color="C1", fontsize=9)
ax.text(0.35, -0.25, "车厢系：摆受 $mg$、$T$ 与惯性力 $-ma$；平衡时 $\\tan\\theta=a/g$", fontsize=9)
ax.set_title("加速车厢中的单摆", fontsize=10)
save(fig, "fig_l11_car_pendulum.png")

# ---------- L11-2 转盘物块 ----------
fig, ax = plt.subplots(figsize=(4.4, 4.0))
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-2.0, 2.0)
ax.set_aspect("equal")
ax.axis("off")
ax.add_patch(plt.Circle((0, 0), 1.9, fill=False, lw=1.4))
ax.plot(0, 0, "o", ms=4, color="k")
M = np.array([1.1, 0])
ax.plot(*M, "s", ms=7, color="C0")
ax.text(M[0] + 0.1, M[1] + 0.1, "物块", fontsize=9)
arr(ax, *M, 0.15, 0, color="C1", text="$f_s$", ty=0.14)
arr(ax, *M, M[0] + 0.7, 0, color="C3", text="$m\\omega^2 r$", ty=0.14)
ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 0.7, 0.7, theta1=20, theta2=100, color="C2", lw=1.4))
ax.text(-0.75, 0.75, "$\\omega$", fontsize=10, color="C2")
ax.text(-1.9, -1.65, "随盘转动：静摩擦提供向心力，$f_{min}=m\\omega^2r$", fontsize=9)
ax.set_title("转盘上的物块（俯视）", fontsize=10)
save(fig, "fig_l11_turntable.png")

print("batch A done")
