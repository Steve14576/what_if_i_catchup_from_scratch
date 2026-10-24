# 课程配图：11 张示意图与曲线图（WIICUFS 1.5.0 绘图）
# 用法：uv run --offline --with matplotlib python scripts/make_figures.py
# 字体：Microsoft YaHei（探针确认覆盖中文与 U+2212）；刻度负号强制 ASCII
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
DPI = 170


def save(fig, name):
    path = os.path.join(FIG, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


def arrow(ax, x0, y0, x1, y1, color="k", lw=1.6, ls="-", text=None, tx=0, ty=0, fs=10, ha="center"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, linestyle=ls,
                                shrinkA=0, shrinkB=0))
    if text:
        ax.text((x0 + x1) / 2 + tx, (y0 + y1) / 2 + ty, text, color=color,
                fontsize=fs, ha=ha, va="center")


# ---------- 1. L01 受力图 ----------
fig, axes = plt.subplots(2, 1, figsize=(6.6, 4.6))
for ax in axes:
    ax.set_xlim(-0.5, 4.6)
    ax.set_ylim(-1.1, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")

ax = axes[0]
ax.plot([0, 4], [0, 0], color="k", lw=5, solid_capstyle="butt")
ax.text(2, -0.35, "梁 AB（长 4 m）", ha="center")
# supports
ax.plot([0, 0], [0, -0.45], color="k", lw=1.2)
ax.plot([-0.28, 0, 0.28], [-0.45, 0, -0.45], color="k", lw=1.2)
ax.text(-0.62, -0.5, "A 铰支座", fontsize=9)
ax.plot([4, 4], [0, -0.28], color="k", lw=1.2)
ax.plot([3.72, 4, 4.28], [-0.28, 0, -0.28], color="k", lw=1.2)
ax.plot(3.8, -0.4, "o", ms=4, color="k")
ax.plot(4.2, -0.4, "o", ms=4, color="k")
ax.text(4.55, -0.5, "B 辊轴", fontsize=9, ha="right")
# load P
arrow(ax, 1, 1.2, 1, 0.05, color="C3", text="$P$", ty=0.12)
# distributed load q
for x in np.linspace(0.3, 3.7, 9):
    arrow(ax, x, 0.55, x, 0.06, color="C0", lw=1.0)
ax.plot([0, 4], [0.55, 0.55], color="C0", lw=1.2)
ax.text(2, 0.72, "均布载荷 $q$", color="C0", ha="center")
ax.set_title("原结构：梁、支座与载荷", fontsize=10)

ax = axes[1]
ax.plot([0, 4], [0, 0], color="k", lw=4, solid_capstyle="butt")
arrow(ax, 0, 0, -0.55, 0, color="C2", text="$F_{Ax}$", ty=-0.18)
arrow(ax, 0, 0, 0, 0.85, color="C2", text="$F_{Ay}$", tx=-0.3)
arrow(ax, 4, 0, 4, 0.85, color="C2", text="$F_B$", tx=0.3)
arrow(ax, 1, 1.2, 1, 0.05, color="C3", text="$P$", ty=0.12)
ax.annotate("", xy=(2, 0.45), xytext=(2, 0.05),
            arrowprops=dict(arrowstyle="-|>", color="C0", lw=2.0))
ax.text(2.15, 0.5, "$q\\times 4$（作用于中点）", color="C0", fontsize=9)
ax.set_title("分离体图：只画外力（约束力按性质命名）", fontsize=10)
save(fig, "fig_l01_fbd.png")

# ---------- 2. L02 力线平移 ----------
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2))
for ax in axes:
    ax.set_xlim(-1.6, 2.2)
    ax.set_ylim(-1.4, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")

ax = axes[0]
ax.add_patch(plt.Rectangle((-1.0, -0.5), 2.0, 1.0, fill=False, lw=1.4))
arrow(ax, 0.7, 0.9, 0.7, 0.0, color="C3", text="$F$", tx=0.18)
ax.plot(0.7, 0.9, "o", ms=4, color="C3")
ax.text(0.78, 1.02, "A", fontsize=9)
ax.plot(0, 0, "o", ms=4, color="k")
ax.text(0.06, -0.16, "O", fontsize=9)
ax.annotate("", xy=(0.7, -0.75), xytext=(0, -0.75),
            arrowprops=dict(arrowstyle="<->", lw=0.9))
ax.text(0.35, -0.95, "$d$", ha="center")
ax.set_title("原状态：力作用于 A", fontsize=10)

ax = axes[1]
ax.add_patch(plt.Rectangle((-1.0, -0.5), 2.0, 1.0, fill=False, lw=1.4))
arrow(ax, 0, 0, 0, 0.9, color="C3", text="$F$", tx=0.2)
ax.plot(0, 0, "o", ms=4, color="k")
ax.text(0.06, -0.16, "O", fontsize=9)
ax.add_patch(plt.matplotlib.patches.Arc((0, 0), 0.7, 0.7, theta1=200, theta2=340,
                                        lw=1.6, color="C1"))
arrow(ax, -0.05, -0.5, -0.35, -0.32, color="C1", lw=1.2)
ax.text(-0.75, -0.68, "$M=Fd$", color="C1", fontsize=10)
ax.set_title("等效：力移到 O + 附加力偶 $M=Fd$", fontsize=10)
save(fig, "fig_l02_translation.png")

# ---------- 3. L05 摩擦角 ----------
fig, ax = plt.subplots(figsize=(5.4, 3.6))
ax.set_xlim(-0.2, 3.2)
ax.set_ylim(-0.2, 2.2)
ax.set_aspect("equal")
ax.axis("off")
th = np.deg2rad(20)
ax.plot([0, 3], [0, 3 * np.tan(th)], color="k", lw=1.6)
ax.plot([0, 3], [0, 0], color="k", lw=0.8, ls="--")
ax.text(2.5, 0.12, "水平", fontsize=9)
ax.text(2.45, 3 * np.tan(th) + 0.08, "斜面", fontsize=9)
ax.text(0.55, 0.25, "角 $\\theta$", fontsize=9)
# block on incline
cx, cy = 1.6, 1.6 * np.tan(th)
ax.add_patch(plt.Rectangle((cx - 0.28, cy), 0.56, 0.34, angle=20, fill=False, lw=1.2))
# normal & reaction at contact
nx, ny = np.sin(th), np.cos(th)
ax.annotate("", xy=(cx - 0.28 * np.cos(th) - 0.9 * nx, cy - 0.28 * np.sin(th) + 0.9 * ny - 0.1),
            xytext=(cx - 0.28 * np.cos(th), cy - 0.28 * np.sin(th)),
            arrowprops=dict(arrowstyle="-|>", color="C0", lw=1.4))
ax.text(cx - 0.4 - 0.9 * nx, cy + 0.9 * ny, "$N$", color="C0")
# full reaction R at angle phi from normal
phi = np.deg2rad(9)
ax.annotate("", xy=(cx - 0.28 * np.cos(th) + 1.0 * np.sin(th + phi),
                    cy - 0.28 * np.sin(th) + 1.0 * np.cos(th + phi)),
            xytext=(cx - 0.28 * np.cos(th), cy - 0.28 * np.sin(th)),
            arrowprops=dict(arrowstyle="-|>", color="C3", lw=2.0))
ax.text(cx - 0.28 * np.cos(th) + 1.1 * np.sin(th + phi),
        cy - 0.28 * np.sin(th) + 1.1 * np.cos(th + phi) - 0.06, "$R$", color="C3")
# cone
for sgn in (-1, 1):
    ax.plot([cx - 0.28 * np.cos(th), cx - 0.28 * np.cos(th) + 0.75 * np.sin(th + sgn * np.deg2rad(15))],
            [cy - 0.28 * np.sin(th), cy - 0.28 * np.sin(th) + 0.75 * np.cos(th + sgn * np.deg2rad(15))],
            color="C3", lw=0.8, ls=":")
ax.text(2.15, 0.95, "摩擦锥：$R$ 与法线夹角\n不超过摩擦角 $\\varphi_m$", fontsize=9, color="C3")
ax.text(1.95, 0.55, "自锁条件：$\\theta \\leq \\varphi_m$", fontsize=9)
save(fig, "fig_l05_friction_cone.png")

# ---------- 4. L09 速度瞬心 ----------
fig, ax = plt.subplots(figsize=(5.8, 4.2))
ax.set_xlim(-0.1, 0.44)
ax.set_ylim(-0.14, 0.63)
ax.set_aspect("equal")
ax.axis("off")
O = np.array([0, 0])
A = 0.1 * np.array([np.cos(np.pi / 3), np.sin(np.pi / 3)])
xB = A[0] + np.sqrt(0.3 ** 2 - A[1] ** 2)
B = np.array([xB, 0])
# ICR: line through A along OA (perpendicular to vA)  x  vertical line through B
tP = (xB - A[0]) / np.cos(np.pi / 3)
P = A + tP * np.array([np.cos(np.pi / 3), np.sin(np.pi / 3)])
ax.plot([O[0], A[0]], [O[1], A[1]], color="k", lw=2.2)
ax.plot([A[0], B[0]], [A[1], B[1]], color="k", lw=2.2)
ax.plot(0, 0, "o", ms=5, color="k")
ax.text(-0.012, -0.008, "O", fontsize=9)
ax.plot(*B, "s", ms=5, color="k")
ax.text(B[0] + 0.004, -0.02, "B", fontsize=9)
ax.plot(*A, "o", ms=5, color="k")
ax.text(A[0] - 0.014, A[1] + 0.006, "A", fontsize=9)
ax.plot(*P, "o", ms=6, color="C3")
ax.text(P[0] - 0.03, P[1] + 0.03, "P（瞬心）", fontsize=9, color="C3", ha="right")
ax.plot([A[0], P[0]], [A[1], P[1]], color="C3", lw=0.8, ls="--")
ax.plot([B[0], P[0]], [B[1], P[1]], color="C3", lw=0.8, ls="--")
# velocity arrows
arrow(ax, A[0], A[1], A[0] - 0.03 * np.sin(np.pi / 3), A[1] + 0.03 * np.cos(np.pi / 3), color="C0")
ax.text(A[0] - 0.042, A[1] + 0.012, "$v_A$", color="C0", fontsize=9)
arrow(ax, B[0], B[1], B[0], B[1] - 0.03, color="C0", text="$v_B$", tx=0.012, ty=-0.008, fs=9)
ax.add_patch(plt.matplotlib.patches.Arc(O, 0.05, 0.05, theta1=0, theta2=60, color="gray", lw=0.8))
ax.text(0.024, 0.012, "$60°$", fontsize=8, color="gray")
ax.set_title("曲柄滑块机构：杆 AB 的瞬心 P\n（$v_A$、$v_B$ 垂线的交点）", fontsize=10, pad=12)
save(fig, "fig_l09_icr.png")

# ---------- 5. L12 冲量 ----------
fig, ax = plt.subplots(figsize=(6.2, 3.0))
t = np.linspace(0, 4, 400)
pulse = np.where((t > 1) & (t < 3), np.sin(np.pi * (t - 1) / 2) ** 2, 0.0)
area = np.trapezoid(pulse, t)
pulse = pulse * (14500.0 / area)       # t in ms: area must be 14500 N*ms = 14.5 N*s
ax.plot(t, pulse, color="C0", lw=1.8, label="接触力 $F(t)$")
ax.fill_between(t, 0, pulse, color="C0", alpha=0.2)
ax.axhline(7.25, color="C3", ls="--", lw=1.2)
ax.text(3.05, 7600, "平均力 7250 N", color="C3", fontsize=9)
ax.annotate("面积 = 冲量 = $\\Delta p = 14.5$ N·s", xy=(2, 4000), xytext=(2.6, 11500),
            arrowprops=dict(arrowstyle="->", lw=0.9), fontsize=9)
ax.set_xlabel("时间 $t$ / ms（示意）")
ax.set_ylabel("力 $F$ / N")
ax.set_ylim(0, 16000)
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_yticks([0, 7000, 14000])
ax.set_yticklabels(["0", "7000", "14000"])
ax.grid(alpha=0.25)
ax.set_title("短时碰撞：力曲线未知，但曲线下的面积（冲量）由 $\\Delta p$ 定死", fontsize=10)
save(fig, "fig_l12_impulse.png")

# ---------- 6. L15 弹簧功与势能 ----------
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
k = 200.0
ax = axes[0]
x = np.linspace(-0.32, 0.32, 400)
F = -k * x
ax.plot(x, F, color="C0", lw=1.8)
xs = np.linspace(0, 0.3, 200)
ax.fill_between(xs, 0, -k * xs, color="C0", alpha=0.25)
ax.axhline(0, color="k", lw=0.7)
ax.axvline(0, color="k", lw=0.7)
ax.set_xlabel("位移 $x$ / m")
ax.set_ylabel("弹力 $F=-kx$ / N")
ax.text(0.16, -20, "面积 = 9 J\n（$x_0=0.3\\to 0$）", fontsize=9, color="C0")
ax.set_title("弹力做功：$F$–$x$ 图下的面积", fontsize=10)
ax = axes[1]
V = 0.5 * k * x ** 2
ax.plot(x, V, color="C1", lw=1.8, label="$V=\\frac{1}{2}kx^2$")
ax.axhline(9, color="C3", ls="--", lw=1.1)
ax.text(-0.31, 9.8, "$E=9$ J", color="C3", fontsize=9)
ax.plot([-0.3, 0.3], [9, 9], "o", ms=4, color="C3")
ax.text(0.31, 8.2, "转折点 $x=\\pm 0.3$ m", fontsize=8.5, color="C3", ha="right")
ax.set_xlabel("位移 $x$ / m")
ax.set_ylabel("势能 $V$ / J")
ax.set_title("势能曲线：动能与势能在此互换", fontsize=10)
ax.set_ylim(0, 11)
save(fig, "fig_l15_spring_energy.png")

# ---------- 7. L19 双摆 ----------
fig, ax = plt.subplots(figsize=(4.6, 4.2))
ax.set_xlim(-0.95, 0.95)
ax.set_ylim(-2.05, 0.18)
ax.set_aspect("equal")
ax.axis("off")
th1, th2 = np.deg2rad(35), np.deg2rad(-20)
O = np.array([0.0, 0.0])
A = O + np.array([np.sin(th1), -np.cos(th1)])
B = A + np.array([np.sin(th2), -np.cos(th2)])
# ceiling
ax.plot([-0.3, 0.3], [0, 0], color="k", lw=2.0)
for xs in np.linspace(-0.3, 0.3, 7):
    ax.plot([xs, xs - 0.04], [0, -0.06], color="k", lw=0.8)
# rods
ax.plot([O[0], A[0]], [O[1], A[1]], color="k", lw=2.2)
ax.plot([A[0], B[0]], [A[1], B[1]], color="k", lw=2.2)
ax.plot(*O, "o", ms=4, color="k")
ax.plot(*A, "o", ms=8, color="C0")
ax.plot(*B, "o", ms=8, color="C3")
ax.text(A[0] + 0.07, A[1] + 0.02, "$m_1$", fontsize=10)
ax.text(B[0] + 0.07, B[1] - 0.02, "$m_2$", fontsize=10)
# theta1 arc
ax.add_patch(plt.matplotlib.patches.Arc(O, 0.7, 0.7, theta1=270, theta2=270 + 35,
                                        color="gray", lw=1.0))
ax.plot([0, 0], [0, -0.75], color="gray", lw=0.8, ls="--")
a_mid = np.deg2rad(270 + 17)
ax.text(0.30 * np.cos(a_mid), 0.30 * np.sin(a_mid) - 0.10, "$\\theta_1$", fontsize=11, color="gray")
# theta2 arc at A
ax.add_patch(plt.matplotlib.patches.Arc(A, 0.5, 0.5, theta1=270 - 20, theta2=270,
                                        color="gray", lw=1.0))
ax.plot([A[0], A[0]], [A[1], A[1] - 0.55], color="gray", lw=0.8, ls="--")
b_mid = np.deg2rad(270 - 10)
ax.text(A[0] + 0.22, A[1] - 0.34, "$\\theta_2$", fontsize=11, color="gray")
# rod length labels (offset from rods)
ax.text(0.40, -0.30, "$l_1$", fontsize=11)
ax.text(0.53, -1.20, "$l_2$", fontsize=11)
ax.text(-0.12, -0.09, "O", fontsize=10)
ax.set_title("双摆：两个广义坐标 $(\\theta_1,\\theta_2)$", fontsize=11)
save(fig, "fig_l19_double_pendulum.png")

# ---------- 8. L20 阻尼三态 ----------
fig, ax = plt.subplots(figsize=(6.4, 3.2))
wn = 10.0
t = np.linspace(0, 1.2, 800)


def free(zeta):
    if zeta < 1:
        wd = wn * np.sqrt(1 - zeta ** 2)
        return np.exp(-zeta * wn * t) * (np.cos(wd * t) + zeta / np.sqrt(1 - zeta ** 2) * np.sin(wd * t))
    if abs(zeta - 1) < 1e-9:
        return (1 + wn * t) * np.exp(-wn * t)
    # overdamped: two real roots
    r1 = -wn * (zeta - np.sqrt(zeta ** 2 - 1))
    r2 = -wn * (zeta + np.sqrt(zeta ** 2 - 1))
    c1 = -r2 / (r1 - r2)
    c2 = r1 / (r1 - r2)
    return c1 * np.exp(r1 * t) + c2 * np.exp(r2 * t)


ax.plot(t, free(0.2), color="C0", lw=1.7, label="欠阻尼 $\\zeta=0.2$")
ax.plot(t, free(1.0), color="C2", lw=1.7, label="临界阻尼 $\\zeta=1$")
ax.plot(t, free(2.0), color="C3", lw=1.7, label="过阻尼 $\\zeta=2$")
ax.plot(t, np.exp(-0.2 * wn * t), color="C0", lw=0.8, ls="--")
ax.plot(t, -np.exp(-0.2 * wn * t), color="C0", lw=0.8, ls="--")
ax.axhline(0, color="k", lw=0.6)
ax.set_xlabel("时间 $t$ / s")
ax.set_ylabel("位移 $x$")
ax.set_xlim(0, 1.2)
ax.set_ylim(-1.05, 1.05)
ax.legend(frameon=False, fontsize=9, loc="upper right")
ax.set_title("初位移释放后的三种自由响应（$\\omega_n=10$ rad/s）", fontsize=10)
save(fig, "fig_l20_damping.png")

# ---------- 9. L20 幅频 ----------
fig, ax = plt.subplots(figsize=(6.4, 3.4))
lam = np.linspace(0.01, 2.5, 800)


def beta(l, z):
    return 1.0 / np.sqrt((1 - l ** 2) ** 2 + (2 * z * l) ** 2)


for z, c in [(0.05, "C3"), (0.1, "C1"), (0.3, "C0"), (0.7, "C4")]:
    ax.plot(lam, beta(lam, z), lw=1.6, color=c, label="ζ = %.2f" % z)
ax.axvline(1, color="gray", ls="--", lw=0.9)
ax.text(1.03, 11.3, "λ = 1（ω = ωn）", fontsize=8.5, color="gray")
ax.set_xlabel("频率比 $\\lambda=\\omega/\\omega_n$")
ax.set_ylabel("放大因子 $\\beta$")
ax.set_xlim(0, 2.5)
ax.set_ylim(0, 12)
ax.legend(frameon=False, fontsize=9)
ax.grid(alpha=0.2)
ax.set_title("幅频曲线：阻尼越小，共振峰越高（峰高约 $1/(2\\zeta)$）", fontsize=10)
save(fig, "fig_l20_response.png")

# ---------- 10. L21 拍振 ----------
fig, ax = plt.subplots(figsize=(7.0, 3.0))
m = 1.0
k_side, k_mid = 100.0, 5.0
w1 = np.sqrt(k_side / m)
w2 = np.sqrt((k_side + 2 * k_mid) / m)
t = np.linspace(0, 70, 4000)
X = 0.1
x1 = X / 2 * (np.cos(w1 * t) + np.cos(w2 * t))
x2 = X / 2 * (np.cos(w1 * t) - np.cos(w2 * t))
ax.plot(t, x1, color="C0", lw=1.0, label="$x_1$（初始被拉开的质量）")
ax.plot(t, x2, color="C3", lw=1.0, label="$x_2$（另一个质量）")
ax.plot(t, X * np.abs(np.cos((w2 - w1) * t / 2)), color="C0", lw=0.9, ls="--")
ax.plot(t, -X * np.abs(np.cos((w2 - w1) * t / 2)), color="C0", lw=0.9, ls="--")
ax.set_xlabel("时间 $t$ / s")
ax.set_ylabel("位移 $x$ / m")
ax.set_xlim(0, 70)
ax.set_ylim(-0.11, 0.11)
ax.legend(frameon=False, fontsize=9, loc="upper right")
ax.set_title("拍振：能量在两个质量间往复（$X=0.1$ m，软耦合 $k_2=0.05k$）", fontsize=10)
save(fig, "fig_l21_beating.png")

# ---------- 11. L22 课程地图 ----------
fig, ax = plt.subplots(figsize=(6.2, 5.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")
parts = [
    ("静力学  L01–L05", "受力图、力系简化、平衡与桁架、空间力系、摩擦", 8.7, "#DCE9F7"),
    ("运动学  L06–L09", "点的运动、平移与定轴、合成运动（科氏）、平面运动（瞬心）", 7.1, "#E3F2E1"),
    ("动力学  L10–L16", "牛二、非惯性系、动量、动量矩、动能、综合与碰撞", 5.5, "#FBE9D7"),
    ("分析力学  L17–L19", "达朗贝尔、虚功原理、第二类拉格朗日方程", 3.9, "#EDE3F5"),
    ("振动  L20–L21", "单自由度（三态/共振）、二自由度（模态/拍/吸振器）", 2.3, "#F7E1E6"),
]
for i, (title, sub, y, col) in enumerate(parts):
    ax.add_patch(plt.Rectangle((1.0, y - 0.62), 8.0, 1.15, facecolor=col, edgecolor="none"))
    ax.text(1.25, y + 0.18, title, fontsize=11, fontweight="bold")
    ax.text(1.25, y - 0.3, sub, fontsize=8.5, color="#333333")
    if i < len(parts) - 1:
        ax.annotate("", xy=(5, y - 0.95), xytext=(5, y - 0.72),
                    arrowprops=dict(arrowstyle="-|>", lw=1.2, color="gray"))
ax.text(1.0, 0.75, "接口 L22：理论力学的方法在机构原理中的调用（速度分析、受力分析、传动比、临界转速）",
        fontsize=9, color="#444444")
ax.set_title("全课程结构：五篇 21 讲 + 接口", fontsize=11)
save(fig, "fig_l22_map.png")

print("all figures done")



