# 规模纪律：4 张静态 SVG, 目标 < 4 秒。
# 第 11 讲图：曲顶柱体、分割与取点、黎曼和收敛、正负体积。
# 图内文字只用 ASCII 与 mathtext（Unicode ∇ 等直接作字符），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: solid under z = x^2+y^2 over the unit square ----------------
fig = plt.figure(figsize=(6.4, 5.4))
ax = fig.add_subplot(projection="3d")
u = np.linspace(0, 1, 31)
U, V = np.meshgrid(u, u)
ax.plot_surface(U, V, U ** 2 + V ** 2, cmap="viridis", alpha=0.55,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.plot_surface(U, V, np.zeros_like(U), color="0.85", alpha=0.35,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
for (x0, y0) in [(0, 0), (1, 0), (1, 1), (0, 1)]:
    ax.plot([x0, x0], [y0, y0], [0, x0 ** 2 + y0 ** 2], color="k", lw=1.3)
t = np.linspace(0, 1, 60)
ax.plot(t, np.zeros_like(t), t ** 2, color="k", lw=1.3)
ax.plot(np.ones_like(t), t, 1 + t ** 2, color="k", lw=1.3)
ax.plot(t, np.ones_like(t), t ** 2 + 1, color="k", lw=1.3)
ax.plot(np.zeros_like(t), t, t ** 2, color="k", lw=1.3)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 2.2)
ax.view_init(elev=20, azim=-58)
ax.set_title(r"solid under $z=x^2+y^2$ over $[0,1]^2$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec11_fig1_solid.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: partition and sample points ----------------
fig, ax = plt.subplots(figsize=(5.6, 5.2))
n = 4
for k in range(n + 1):
    ax.plot([k / n, k / n], [0, 1], color="0.6", lw=1.0)
    ax.plot([0, 1], [k / n, k / n], color="0.6", lw=1.0)
pts_x, pts_y = [], []
for i in range(1, n + 1):
    for j in range(1, n + 1):
        pts_x.append(i / n); pts_y.append(j / n)
ax.scatter(pts_x, pts_y, color="tab:red", s=26, zorder=3)
ax.text(0.06, 0.94, r"sample point $(\xi_i,\eta_i)$", color="tab:red", fontsize=9)
ax.text(0.05, 0.05, r"area $\Delta\sigma_i=1/16$", fontsize=9)
ax.set_aspect("equal")
ax.set_xlim(-0.05, 1.06); ax.set_ylim(-0.05, 1.06)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title("partition into 4x4 cells and pick one point per cell", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec11_fig2_partition.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: Riemann sums converge ----------------
ns = np.array([2, 4, 8, 16, 32, 64, 128, 256])
sn = (ns + 1) * (2 * ns + 1) / (3.0 * ns ** 2)  # for x^2+y^2, right endpoints
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.semilogx(ns, sn, "o-", color="tab:blue", lw=1.8)
ax.axhline(2 / 3, color="tab:red", lw=1.5, ls="--")
ax.text(2.2, 2 / 3 + 0.006, r"limit $= 2/3$", color="tab:red", fontsize=9)
ax.set_xlabel("n (grid is n x n)"); ax.set_ylabel(r"$S_n$")
ax.grid(alpha=0.25, which="both")
ax.set_title(r"Riemann sums for $x^2+y^2$ on $[0,1]^2$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec11_fig3_convergence.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: signed volume with z = x^2 - y^2 ----------------
fig = plt.figure(figsize=(6.4, 5.2))
ax = fig.add_subplot(projection="3d")
u = np.linspace(-1, 1, 41)
U, V = np.meshgrid(u, u)
ax.plot_surface(U, V, U ** 2 - V ** 2, cmap="coolwarm", alpha=0.75,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.plot_surface(U, V, np.zeros_like(U), color="0.7", alpha=0.25,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.text(-0.9, 0.6, 0.75, "positive", color="tab:red", fontsize=9)
ax.text(0.35, -0.9, -0.85, "negative", color="tab:blue", fontsize=9)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_zlim(-1.2, 1.2)
ax.view_init(elev=20, azim=-58)
ax.set_title(r"signed volume: $z=x^2-y^2$ over $[-1,1]^2$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec11_fig4_signed.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec11_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
