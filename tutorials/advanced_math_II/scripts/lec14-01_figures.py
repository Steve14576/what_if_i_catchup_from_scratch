# 规模纪律：4 张静态 SVG, 目标 < 4 秒。
# 第 14 讲图：先一后二、先二后一、柱面坐标、球面坐标。
# 图内文字只用 ASCII 与 mathtext（≤ 用 Unicode），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: projection method ----------------
fig = plt.figure(figsize=(6.0, 5.2))
ax = fig.add_subplot(projection="3d")
u = np.linspace(0, 1, 21)
U, V = np.meshgrid(u, u)
ax.plot_surface(U, V, U + V, color="tab:blue", alpha=0.35, linewidth=0)
ax.plot_surface(U, V, np.zeros_like(U), color="0.85", alpha=0.35, linewidth=0)
t = np.linspace(0, 1, 60)
ax.plot(t, np.zeros_like(t), t, color="k", lw=1.2)
ax.plot(np.zeros_like(t), t, t, color="k", lw=1.2)
ax.plot(np.ones_like(t), t, 1 + t, color="k", lw=1.2)
ax.plot(t, np.ones_like(t), t + 1, color="k", lw=1.2)
ax.plot([0.4, 0.4], [0.6, 0.6], [0, 1.0], color="tab:red", lw=2.2)
ax.text(0.42, 0.62, 1.08, r"vertical line", color="tab:red", fontsize=8)
ax.text(0.05, 0.05, -0.25, r"$D$", fontsize=10)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 2.2)
ax.view_init(elev=20, azim=-58)
ax.set_title(r"projection method: $0 ≤ z ≤ x+y$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec14_fig1_projection.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: slicing method (upper half ball) ----------------
fig = plt.figure(figsize=(6.0, 5.2))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi, 41); ph = np.linspace(0, 2 * np.pi, 61)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH),
                cmap="viridis", alpha=0.20, linewidth=0, rstride=2, cstride=2)
z0 = 0.5
r0 = np.sqrt(1 - z0 ** 2)
ax.plot(r0 * np.cos(ph), r0 * np.sin(ph), np.full_like(ph, z0),
        color="tab:red", lw=2.0)
ax.plot([0, r0], [0, 0], [z0, z0], color="tab:red", lw=1.4)
ax.text(0.05, 0.05, z0 + 0.08, r"slice at $z$", color="tab:red", fontsize=9)
ax.text(0.15, -0.55, 0.05, r"$x^2+y^2 ≤ 1-z^2$", fontsize=8)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_zlim(-0.1, 1.1)
ax.view_init(elev=18, azim=-58)
ax.set_title(r"slicing: cross-section disk at height $z$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec14_fig2_slices.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: cylindrical coordinates ----------------
fig = plt.figure(figsize=(6.2, 5.6))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, 2 * np.pi, 61)
zz = np.linspace(0, 1.6, 20)
TH, ZZ = np.meshgrid(th, zz)
ax.plot_surface(np.cos(TH), np.sin(TH), ZZ, color="tab:green", alpha=0.14,
                linewidth=0, rstride=2, cstride=2)
r0, th0, z0 = 0.8, np.pi / 4, 1.2
P = np.array([r0 * np.cos(th0), r0 * np.sin(th0), z0])
# axes
ax.plot([0, 0], [0, 0], [0, 1.8], color="k", lw=1.3)
ax.plot([0, P[0]], [0, P[1]], [0, 0], color="k", lw=1.0, ls="--")
ax.plot([P[0], P[0]], [P[1], P[1]], [0, z0], color="k", lw=1.0, ls="--")
# r arrow, theta arc, z arrow
ax.quiver(0, 0, 0, P[0], P[1], 0, color="tab:red", lw=1.8, arrow_length_ratio=0.12)
ax.text(0.5 * P[0], 0.5 * P[1], 0.07, r"$r$", color="tab:red", fontsize=10)
tt = np.linspace(0, th0, 40)
ax.plot(0.55 * np.cos(tt), 0.55 * np.sin(tt), np.zeros_like(tt), color="tab:orange", lw=1.6)
ax.text(0.5, 0.12, 0.02, r"$\theta$", color="tab:orange", fontsize=10)
ax.quiver(P[0], P[1], 0, 0, 0, z0, color="tab:green", lw=1.6, arrow_length_ratio=0.1)
ax.text(P[0] - 0.12, P[1] - 0.12, z0 * 0.55, r"$z$", color="tab:green", fontsize=10)
# volume element edges at P
ax.quiver(*P, 0.18 * np.cos(th0), 0.18 * np.sin(th0), 0, color="tab:purple", lw=2.0, arrow_length_ratio=0.15)
ax.quiver(*P, -0.20 * r0 * np.sin(th0), 0.20 * r0 * np.cos(th0), 0, color="tab:brown", lw=2.0, arrow_length_ratio=0.15)
ax.quiver(*P, 0, 0, 0.22, color="tab:olive", lw=2.0, arrow_length_ratio=0.15)
ax.text(P[0] + 0.14, P[1] - 0.1, z0 + 0.12, r"$dr$", color="tab:purple", fontsize=9)
ax.text(P[0] - 0.3, P[1] + 0.16, z0 + 0.12, r"$r\,d\theta$", color="tab:brown", fontsize=9)
ax.text(P[0] + 0.05, P[1] + 0.05, z0 + 0.3, r"$dz$", color="tab:olive", fontsize=9)
ax.scatter(*P, color="k", s=24)
ax.text(P[0] + 0.03, P[1] + 0.03, z0 + 0.05, r"$P$", fontsize=9)
ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4); ax.set_zlim(0, 1.9)
ax.set_box_aspect((2.8, 2.8, 1.9))
ax.view_init(elev=20, azim=-58)
ax.set_title(r"cylindrical: $dV=r\,dr\,d\theta\,dz$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec14_fig3_cylindrical.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: spherical coordinates ----------------
fig = plt.figure(figsize=(6.2, 5.6))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi, 41); ph = np.linspace(0, 2 * np.pi, 61)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH),
                color="tab:purple", alpha=0.16, linewidth=0, rstride=2, cstride=2)
phi0, theta0 = np.pi / 3, np.pi / 6
P = np.array([np.sin(phi0) * np.cos(theta0), np.sin(phi0) * np.sin(theta0), np.cos(phi0)])
# axes and rho
ax.plot([0, 0], [0, 0], [0, 1.3], color="k", lw=1.2)
ax.plot([0, P[0]], [0, P[1]], [0, P[2]], color="tab:red", lw=2.2)
ax.text(P[0] * 0.6, P[1] * 0.6, P[2] * 0.6 + 0.08, r"$\rho$", color="tab:red", fontsize=10)
# phi arc in the meridian plane
tt = np.linspace(0, phi0, 40)
ax.plot(0.5 * np.sin(tt) * np.cos(theta0), 0.5 * np.sin(tt) * np.sin(theta0),
        0.5 * np.cos(tt), color="tab:blue", lw=1.8)
ax.text(0.12, 0.18, 0.46, r"$\phi$", color="tab:blue", fontsize=10)
# theta arc in the xy-plane
tt2 = np.linspace(0, theta0, 40)
ax.plot(0.62 * np.cos(tt2), 0.62 * np.sin(tt2), np.zeros_like(tt2), color="tab:orange", lw=1.8)
ax.text(0.58, 0.12, 0.02, r"$\theta$", color="tab:orange", fontsize=10)
# latitude circle dashed
ax.plot(np.sin(phi0) * np.cos(ph), np.sin(phi0) * np.sin(ph), np.full_like(ph, np.cos(phi0)),
        color="0.5", lw=1.0, ls="--")
ax.scatter(*P, color="k", s=24)
ax.text(P[0] + 0.03, P[1] + 0.03, P[2] + 0.06, r"$P$", fontsize=9)
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(-1.2, 1.2)
ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=18, azim=-58)
ax.set_title(r"spherical: $dV=\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec14_fig4_spherical.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec14_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
