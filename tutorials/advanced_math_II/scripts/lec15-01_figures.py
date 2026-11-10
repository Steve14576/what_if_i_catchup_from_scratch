# 规模纪律：3 张静态 SVG, 目标 < 4 秒。
# 第 15 讲图：曲顶体积、转动惯量权重、半球质心。
# 图内文字只用 ASCII 与 mathtext（≤ 用 Unicode），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: volume between paraboloid and z=4 ----------------
fig = plt.figure(figsize=(6.2, 5.4))
ax = fig.add_subplot(projection="3d")
r = np.linspace(0, 2, 31)
th = np.linspace(0, 2 * np.pi, 61)
R, TH = np.meshgrid(r, th)
ax.plot_surface(R * np.cos(TH), R * np.sin(TH), R ** 2, cmap="viridis", alpha=0.45,
                linewidth=0, rstride=2, cstride=2)
ax.plot_surface(R * np.cos(TH), R * np.sin(TH), np.full_like(R, 4.0),
                color="tab:red", alpha=0.20, linewidth=0, rstride=2, cstride=2)
ax.text(1.4, 1.2, 4.15, r"$z=4$", color="tab:red", fontsize=9)
ax.text(0.2, 0.2, 1.0, r"$z=x^2+y^2$", fontsize=9)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.2); ax.set_zlim(0, 4.4)
ax.set_box_aspect((4.4, 4.4, 4.4))
ax.view_init(elev=20, azim=-58)
ax.set_title(r"volume between $z=x^2+y^2$ and $z=4$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec15_fig1_volume.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: inertia weight r^2 ----------------
fig, ax = plt.subplots(figsize=(5.6, 5.2))
th = np.linspace(0, 2 * np.pi, 400)
ax.fill(np.cos(th), np.sin(th), color="tab:blue", alpha=0.12)
ax.plot(np.cos(th), np.sin(th), color="tab:blue", lw=1.8)
for rr in [0.33, 0.66]:
    ax.plot(rr * np.cos(th), rr * np.sin(th), color="0.75", lw=1.0)
for a in [0, np.pi / 6, np.pi / 3, np.pi / 2, 2 * np.pi / 3, 5 * np.pi / 6, np.pi]:
    ax.plot([0, np.cos(a)], [0, np.sin(a)], color="0.75", lw=0.8)
ax.quiver(0, 0, 0.85, 0.55, color="tab:red", angles="xy", scale_units="xy", scale=1, lw=2.0)
ax.text(0.55, 0.62, r"$r$", color="tab:red", fontsize=11)
ax.text(-0.95, 0.82, r"weight $=r^2$", fontsize=10)
ax.text(0, -0.12, "O", fontsize=9, ha="center")
ax.set_aspect("equal")
ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.15, 1.15)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"$I_z=\iint (x^2+y^2)\rho\,d\sigma$: farther cells weigh more", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec15_fig2_inertia.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: hemisphere centroid ----------------
fig = plt.figure(figsize=(6.2, 5.4))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi / 2, 41); ph = np.linspace(0, 2 * np.pi, 61)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH),
                color="tab:purple", alpha=0.22, linewidth=0, rstride=2, cstride=2)
zc = 8 / 15
ax.plot([0, 0], [0, 0], [0, 1.15], color="k", lw=1.2, ls="--")
ax.scatter([0], [0], [zc], color="tab:red", s=40, zorder=5)
ax.text(0.05, 0.05, zc + 0.06, r"centroid: $\bar z=8R/15$", color="tab:red", fontsize=9)
ax.plot([-0.35, 0.35], [0, 0], [zc, zc], color="tab:red", lw=1.2, ls=":")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(0, 1.25)
ax.set_box_aspect((2.2, 2.2, 2.4))
ax.view_init(elev=18, azim=-58)
ax.set_title(r"hemisphere with $\rho=z$: $\bar z=8R/15$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec15_fig3_centroid.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec15_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
