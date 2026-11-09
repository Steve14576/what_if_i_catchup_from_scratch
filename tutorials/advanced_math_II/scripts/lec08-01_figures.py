# 规模纪律：4 张静态 SVG, 目标 < 3 秒。
# 第 08 讲图：方向导数的截面切线、梯度垂直等值线、方向导数随角度、最速上升。
# 图内文字只用 ASCII 与 mathtext（Unicode ∇ θ α 直接作字符），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: directional derivative = slope of the section curve ----------------
fig = plt.figure(figsize=(6.6, 5.4))
ax = fig.add_subplot(projection="3d")
u = np.linspace(0, 2, 31)
U, V = np.meshgrid(u, u)
ax.plot_surface(U, V, U ** 2 + V ** 2, cmap="viridis", alpha=0.40,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
ex, ey = 0.6, 0.8
s = np.linspace(-0.9, 0.9, 60)
xs, ys = 1 + s * ex, 1 + s * ey
ax.plot(xs, ys, xs ** 2 + ys ** 2, color="tab:blue", lw=2.2)
slope = 2 * 1 * ex + 2 * 1 * ey
ax.plot(1 + s * ex, 1 + s * ey, 2 + s * slope, color="tab:red", lw=2.6)
ax.plot([1, 1 + 0.8 * ex], [1, 1 + 0.8 * ey], [2, 2], color="k", lw=1.8)
ax.scatter([1], [1], [2], color="k", s=22)
ax.text(1.6, 1.7, 2.1, r"$e=(0.6,0.8)$", fontsize=9)
ax.text(0.1, 1.2, 3.0, r"section curve", color="tab:blue", fontsize=8)
ax.text(1.3, 0.4, 2.6, r"tangent: slope $=∇f·e$", color="tab:red", fontsize=8)
ax.set_xlim(0, 2); ax.set_ylim(0, 2); ax.set_zlim(0, 6)
ax.view_init(elev=20, azim=-62)
ax.set_title("directional derivative: slope of the vertical section", fontsize=9)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
fig.tight_layout()
fig.savefig(OUT / "lec08_fig1_section_slope.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: gradient is perpendicular to the level curve ----------------
fig, ax = plt.subplots(figsize=(5.8, 5.2))
th = np.linspace(0, 2 * np.pi, 400)
for r in [0.8, 1.2, np.sqrt(2), 1.8]:
    ax.plot(r * np.cos(th), r * np.sin(th), color="0.75", lw=1.0)
ax.plot(np.sqrt(2) * np.cos(th), np.sqrt(2) * np.sin(th), color="tab:blue", lw=2.2)
P = np.array([1.0, 1.0])
g = np.array([2.0, 2.0]); g = g / np.linalg.norm(g)
t = np.array([-1.0, 1.0]); t = t / np.linalg.norm(t)
ax.annotate("", xy=P + 0.85 * g, xytext=P,
            arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=2.4))
ax.annotate("", xy=P + 0.9 * t, xytext=P,
            arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=2.0))
ax.annotate("", xy=P - 0.9 * t, xytext=P,
            arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=2.0))
ax.scatter([1], [1], color="k", s=22)
ax.text(1.75, 1.75, r"$∇f$", color="tab:red", fontsize=11)
ax.text(1.6, 0.25, "tangent: derivative 0", color="tab:green", fontsize=9)
ax.text(1.05, 1.05, r"$P$", fontsize=10)
ax.set_aspect("equal")
ax.set_xlim(-2, 2.2); ax.set_ylim(-2, 2.2)
ax.grid(alpha=0.25)
ax.axhline(0, color="0.85", lw=0.6); ax.axvline(0, color="0.85", lw=0.6)
ax.set_title(r"grad f is perpendicular to the level curve $x^2+y^2=2$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec08_fig3_level_normal.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: directional derivative as a function of the angle ----------------
fig, ax = plt.subplots(figsize=(6.4, 4.2))
th = np.linspace(0, 2 * np.pi, 500)
g = 2 * np.sqrt(2) * np.cos(th - np.pi / 4)
ax.plot(th, g, color="tab:blue", lw=2.2)
for th0, lab in [(np.pi / 4, "max = |grad f|"), (3 * np.pi / 4, "zero"), (5 * np.pi / 4, "min = -|grad f|")]:
    val = 2 * np.sqrt(2) * np.cos(th0 - np.pi / 4)
    ax.scatter([th0], [val], color="tab:red", s=28, zorder=3)
    ax.annotate(lab, xy=(th0, val), xytext=(th0 + 0.15, val + 0.5),
                fontsize=8, color="tab:red")
ax.axhline(0, color="0.8", lw=0.8)
ax.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi, 5 * np.pi / 4, 3 * np.pi / 2, 7 * np.pi / 4, 2 * np.pi])
ax.set_xticklabels(["0", "pi/4", "pi/2", "3pi/4", "pi", "5pi/4", "3pi/2", "7pi/4", "2pi"], fontsize=8)
ax.set_xlabel("theta")
ax.set_ylabel("directional derivative")
ax.set_title(r"$\partial f/\partial l = |\nabla f|\cos(\theta-\pi/4)$", fontsize=10)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(OUT / "lec08_fig2_angle_scan.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: steepest ascent on a contour map ----------------
fig, ax = plt.subplots(figsize=(5.8, 5.2))
th = np.linspace(0, 2 * np.pi, 400)
for r, c in [(0.7, "0.5"), (1.0, "1"), (np.sqrt(2), "2"), (1.6, "2.56")]:
    ax.plot(r * np.cos(th), r * np.sin(th), color="0.78", lw=1.0)
    ax.text(r * 0.72, r * 0.72, "c=" + c, fontsize=7, color="0.45")
P = np.array([1.0, 1.0])
gf = np.array([2.0, 2.0])
for k in range(8):
    th_k = k * np.pi / 4
    e = np.array([np.cos(th_k), np.sin(th_k)])
    val = gf.dot(e)
    if val > 1e-9:
        ax.annotate("", xy=P + 0.22 * val * e, xytext=P,
                    arrowprops=dict(arrowstyle="-|>", color="tab:blue", lw=1.2, alpha=0.8))
ax.annotate("", xy=P + 0.62 * gf / np.linalg.norm(gf), xytext=P,
            arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=2.6))
ax.scatter([1], [1], color="k", s=22)
ax.text(1.72, 1.72, "steepest ascent", color="tab:red", fontsize=9)
ax.text(1.05, 1.05, r"$P$", fontsize=10)
ax.set_aspect("equal")
ax.set_xlim(-1.9, 2.1); ax.set_ylim(-1.9, 2.1)
ax.grid(alpha=0.2)
ax.axhline(0, color="0.85", lw=0.6); ax.axvline(0, color="0.85", lw=0.6)
ax.set_title("arrow length = directional derivative in that direction", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec08_fig4_steepest.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec08_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
