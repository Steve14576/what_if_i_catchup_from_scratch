# 规模纪律：3 张静态 SVG, 目标 < 5 秒。
# 第 21 讲图：长方体高斯、闭合曲面散度源、斯托克斯右手法则。
# 图内文字只用 ASCII 与 mathtext（不用 \mathbf），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: box, top/bottom contribute R dxdy ----------------
fig = plt.figure(figsize=(6.2, 5.0))
ax = fig.add_subplot(projection="3d")
x0, y0, z0, a, b, c = 0.2, 0.2, 0.3, 0.9, 0.8, 0.7
# vertical edges
for x in [x0, x0 + a]:
    for y in [y0, y0 + b]:
        ax.plot([x, x], [y, y], [z0, z0 + c], color="0.4", lw=1.0)
# top and bottom rectangles (highlighted)
for z, col in [(z0 + c, "tab:blue"), (z0, "tab:orange")]:
    ax.plot([x0, x0 + a, x0 + a, x0, x0], [y0, y0, y0 + b, y0 + b, y0], [z] * 5,
            color=col, lw=2.0)
# faint side edges at top/bottom
for z in [z0, z0 + c]:
    ax.plot([x0, x0 + a], [y0, y0], [z, z], color="0.6", lw=0.8)
    ax.plot([x0 + a, x0 + a], [y0, y0 + b], [z, z], color="0.6", lw=0.8)
    ax.plot([x0 + a, x0], [y0 + b, y0 + b], [z, z], color="0.6", lw=0.8)
    ax.plot([x0, x0], [y0 + b, y0], [z, z], color="0.6", lw=0.8)
# normals
ax.quiver(x0 + a / 2, y0 + b / 2, z0 + c, 0, 0, 0.28, color="tab:blue", lw=2.0, arrow_length_ratio=0.2)
ax.quiver(x0 + a / 2, y0 + b / 2, z0, 0, 0, -0.28, color="tab:orange", lw=2.0, arrow_length_ratio=0.2)
ax.text(x0 + a / 2 + 0.03, y0 + b / 2, z0 + c + 0.32, r"top $+$", color="tab:blue", fontsize=9)
ax.text(x0 + a / 2 + 0.03, y0 + b / 2, z0 - 0.42, r"bottom $-$", color="tab:orange", fontsize=9)
ax.text(x0 + a + 0.08, y0 + b + 0.05, z0 + c / 2, r"$\Omega$", fontsize=11)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1.4); ax.set_ylim(0, 1.3); ax.set_zlim(0, 1.3)
ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=20, azim=-58)
ax.set_title(r"Gauss: only top/bottom contribute $R\,dx\,dy$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec21_fig1_box.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: closed surface, divergence sources ----------------
fig = plt.figure(figsize=(6.0, 5.0))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi, 41); ph = np.linspace(0, 2 * np.pi, 61)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH),
                color="tab:purple", alpha=0.12, linewidth=0, rstride=3, cstride=3)
# outward arrows from inside (sources)
for (x, y, z) in [(0, 0, 0), (0.35, -0.25, 0.2), (-0.3, 0.3, -0.15), (0.1, 0.4, -0.3)]:
    v = np.array([x, y, z])
    v = v / (np.linalg.norm(v) + 1e-9) * 0.35
    ax.quiver(x, y, z, *v, color="tab:red", lw=1.6, arrow_length_ratio=0.18)
ax.text(0.0, 0.0, 1.5, r"$\iint F\cdot dS=\iiint \mathrm{div}\,F\,dV$", fontsize=10)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(-1.1, 1.6)
ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=18, azim=-58)
ax.set_title(r"closed surface: flux = total divergence inside", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec21_fig2_divergence.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: Stokes, surface + boundary + right hand ----------------
fig = plt.figure(figsize=(6.2, 5.2))
ax = fig.add_subplot(projection="3d")
u = np.linspace(0, 1, 25)
U, V = np.meshgrid(u, u)
Z = 0.35 + 0.25 * U + 0.15 * V
ax.plot_surface(U, V, Z, color="tab:green", alpha=0.28, linewidth=0)
# boundary of the parametric patch
b = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float)
bx = b[:, 0]; by = b[:, 1]; bz = 0.35 + 0.25 * bx + 0.15 * by
ax.plot(bx, by, bz, color="tab:red", lw=2.4)
# direction arrows along two edges
ax.quiver(0.55, 0, 0.35 + 0.25 * 0.55, 0.22, 0, 0.25 * 0.22, color="tab:red",
          lw=1.8, arrow_length_ratio=0.2)
ax.quiver(1.0, 0.5, 0.35 + 0.25 + 0.15 * 0.5, 0, 0.2, 0.15 * 0.2, color="tab:red",
          lw=1.8, arrow_length_ratio=0.2)
# normal
n = np.array([-0.25, -0.15, 1.0]); n = n / np.linalg.norm(n)
ax.quiver(0.5, 0.5, 0.35 + 0.125 + 0.075, *(n * 0.55), color="tab:blue",
          lw=2.0, arrow_length_ratio=0.15)
ax.text(0.55, 0.55, 0.9, r"$\Gamma$ and $n$: right-hand rule", fontsize=9)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1.2); ax.set_ylim(0, 1.2); ax.set_zlim(0.1, 1.3)
ax.set_box_aspect((1, 1, 1.1))
ax.view_init(elev=22, azim=-58)
ax.set_title(r"Stokes: circulation along boundary = curl flux through surface", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec21_fig3_stokes.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec21_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
