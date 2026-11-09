# 规模纪律：4 张静态 SVG, 目标 < 4 秒。
# 第 10 讲图：圆盘上的最值、三角形上的最值、长方体、圆柱表面积曲线。
# 图内文字只用 ASCII 与 mathtext（Unicode ∇ √ 直接作字符），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: disk case ----------------
fig, ax = plt.subplots(figsize=(5.8, 5.2))
x = np.linspace(-2.4, 2.4, 300)
X, Y = np.meshgrid(x, x)
F = X ** 2 + Y ** 2 - 2 * X - 2 * Y
cs = ax.contour(X, Y, F, levels=[-1.5, -1.0, 0, 2, 5], colors="tab:blue", linewidths=1.1)
ax.clabel(cs, inline=True, fontsize=7)
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(2 * np.cos(th), 2 * np.sin(th), color="0.3", lw=2.2)
ax.scatter([1], [1], color="tab:red", s=45, zorder=3)
ax.text(1.08, 1.08, r"$(1,1)$, min $=-2$", color="tab:red", fontsize=9)
ax.scatter([-np.sqrt(2)], [-np.sqrt(2)], color="tab:green", s=45, zorder=3)
ax.text(-2.25, -2.55, r"$(-\sqrt{2},-\sqrt{2})$, max", color="tab:green", fontsize=8)
ax.set_aspect("equal")
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.8, 2.6)
ax.grid(alpha=0.2)
ax.set_title(r"$f=x^2+y^2-2x-2y$ on the disk $x^2+y^2 ≤ 4$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec10_fig1_disk.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: triangle case ----------------
fig, ax = plt.subplots(figsize=(5.8, 5.2))
x = np.linspace(-0.2, 2.3, 300)
X, Y = np.meshgrid(x, x)
F = X ** 2 + Y ** 2
cs = ax.contour(X, Y, F, levels=[0.5, 2, 4, 6], colors="tab:blue", linewidths=1.1)
ax.clabel(cs, inline=True, fontsize=7)
tri = np.array([[0, 0], [2, 0], [0, 2], [0, 0]])
ax.plot(tri[:, 0], tri[:, 1], color="0.3", lw=2.2)
ax.scatter([0], [0], color="tab:red", s=45, zorder=3)
ax.text(0.07, 0.07, "min $=0$", color="tab:red", fontsize=9)
ax.scatter([2, 0], [0, 2], color="tab:green", s=45, zorder=3)
ax.text(1.55, -0.28, "max $=4$", color="tab:green", fontsize=9)
ax.text(1.05, 1.05, r"$(1,1)$: $2$", fontsize=8)
ax.set_aspect("equal")
ax.set_xlim(-0.3, 2.4); ax.set_ylim(-0.4, 2.4)
ax.grid(alpha=0.2)
ax.set_title(r"$f=x^2+y^2$ on the triangle $x,y ≥ 0,\ x+y ≤ 2$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec10_fig2_triangle.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: box with fixed volume ----------------
fig = plt.figure(figsize=(5.6, 5.0))
ax = fig.add_subplot(projection="3d")
s = 1.0
edges = [
    ((0, 0, 0), (s, 0, 0)), ((0, 0, 0), (0, s, 0)), ((0, 0, 0), (0, 0, s)),
    ((s, 0, 0), (s, s, 0)), ((s, 0, 0), (s, 0, s)),
    ((0, s, 0), (s, s, 0)), ((0, s, 0), (0, s, s)),
    ((0, 0, s), (s, 0, s)), ((0, 0, s), (0, s, s)),
    ((s, s, 0), (s, s, s)), ((s, 0, s), (s, s, s)), ((0, s, s), (s, s, s)),
]
for a, b in edges:
    ax.plot([a[0], b[0]], [a[1], b[1]], [a[2], b[2]], color="tab:blue", lw=1.8)
ax.text(s / 2, -0.12, 0, "x", fontsize=10)
ax.text(-0.12, s / 2, 0, "y", fontsize=10)
ax.text(0, 0, s + 0.12, "z", fontsize=10)
ax.set_xlim(-0.2, 1.2); ax.set_ylim(-0.2, 1.2); ax.set_zlim(-0.2, 1.3)
ax.view_init(elev=18, azim=-55)
ax.set_title(r"V fixed: $x=y=z$ minimizes the surface", fontsize=9)
ax.set_axis_off()
fig.tight_layout()
fig.savefig(OUT / "lec10_fig3_box.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: cylinder surface area ----------------
fig, ax = plt.subplots(figsize=(6.2, 4.2))
r = np.linspace(0.15, 1.6, 400)
S = 2 * np.pi * r ** 2 + 2 / r
ax.plot(r, S, color="tab:blue", lw=2.2)
r_star = (1 / (2 * np.pi)) ** (1 / 3)
S_star = 2 * np.pi * r_star ** 2 + 2 / r_star
ax.scatter([r_star], [S_star], color="tab:red", s=45, zorder=3)
ax.annotate(rf"$r^*={r_star:.4f}$, $S^*={S_star:.3f}$" + "\n" + r"$h=2r$",
            xy=(r_star, S_star), xytext=(r_star + 0.25, S_star + 1.2), fontsize=9,
            color="tab:red")
ax.set_xlabel("r"); ax.set_ylabel("S(r)")
ax.set_ylim(0, 18)
ax.grid(alpha=0.25)
ax.set_title(r"$S(r)=2\pi r^2+2/r$ with $V=1$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec10_fig4_cylinder.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec10_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
