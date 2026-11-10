# 规模纪律：4 张静态 SVG, 目标 < 5 秒。
# 第 20 讲图：通量点积、有向面元三分量、上下侧定号、球面外侧。
# 图内文字只用 ASCII 与 mathtext（不用 \mathbf），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: flux through a patch ----------------
fig = plt.figure(figsize=(6.4, 5.0))
ax = fig.add_subplot(projection="3d")
u = np.linspace(0, 1, 2)
U, V = np.meshgrid(u, u)
Z = 0.55 + 0.25 * U
ax.plot_surface(U, V, Z, color="tab:blue", alpha=0.35, linewidth=0)
p = np.array([0.45, 0.45, 0.55 + 0.25 * 0.45])
n = np.array([-0.25, 0, 1.0]); n = n / np.linalg.norm(n)
v = np.array([0.55, 0.25, 0.75]); v = v / np.linalg.norm(v) * 0.55
ax.quiver(*p, *n * 0.55, color="tab:green", lw=2.0, arrow_length_ratio=0.12)
ax.quiver(*p, *v, color="tab:red", lw=2.0, arrow_length_ratio=0.12)
# projection of v onto n
proj = np.dot(v, n) * n
ax.quiver(*p, *proj, color="tab:orange", lw=2.0, arrow_length_ratio=0.15)
ax.text(*(p + n * 0.58), "n", color="tab:green", fontsize=10)
ax.text(*(p + v * 0.62), "v", color="tab:red", fontsize=10)
ax.text(*(p + proj * 0.55 + np.array([0.04, 0.0, 0.02])), "v.n", color="tab:orange", fontsize=9)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1.4)
ax.set_box_aspect((1, 1, 1.3))
ax.view_init(elev=20, azim=-58)
ax.set_title(r"flux: only the normal component $v\cdot n$ crosses $dS$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec20_fig1_flux.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: oriented patch and three projections ----------------
fig = plt.figure(figsize=(6.4, 5.2))
ax = fig.add_subplot(projection="3d")
p0 = np.array([0.3, 0.3, 0.8])
e1 = np.array([0.45, 0.0, 0.18])
e2 = np.array([0.0, 0.4, 0.16])
poly = [p0, p0 + e1, p0 + e1 + e2, p0 + e2, p0]
ax.plot([q[0] for q in poly], [q[1] for q in poly], [q[2] for q in poly], color="tab:blue", lw=1.8)
# projection rectangle drawn as a 3D closed line (Axes3D does not accept 2D patches)
rx = [0.3, 0.75, 0.75, 0.3, 0.3]
ry = [0.3, 0.3, 0.7, 0.7, 0.3]
ax.plot(rx, ry, [0, 0, 0, 0, 0], color="tab:red", lw=1.2, ls="--")
ax.text(0.55, 0.72, 0.02, r"$dx\,dy$", color="tab:red", fontsize=9)
ax.text(0.32, 0.30, 0.95, r"$dS$", color="tab:blue", fontsize=10)
ax.quiver(*(p0 + 0.5 * (e1 + e2)), *np.array([0.0, 0.0, 0.35]), color="tab:green",
          lw=1.8, arrow_length_ratio=0.12)
ax.text(*(p0 + 0.5 * (e1 + e2) + np.array([0.0, 0.0, 0.38])), "n", color="tab:green", fontsize=10)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0.1, 1.0); ax.set_ylim(0.1, 1.0); ax.set_zlim(0, 1.5)
ax.set_box_aspect((1, 1, 1.4))
ax.view_init(elev=20, azim=-58)
ax.set_title(r"$dS$: oriented element; $dx\,dy=\cos\gamma\,dS$ is its projection", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec20_fig2_components.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: upper vs lower side sign ----------------
fig, ax = plt.subplots(figsize=(6.0, 4.2))
x = np.linspace(0, 2, 100)
y = 0.8 + 0.6 * np.sin(np.pi * x / 2)
ax.plot(x, y, color="tab:blue", lw=2.2)
ax.fill_between([0.4, 1.6], 0.0, 0.0, color="0.8")
ax.annotate("", xy=(1.0, 1.55), xytext=(1.0, 0.95),
            arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=2.0))
ax.annotate("", xy=(1.0, 0.35), xytext=(1.0, 0.95),
            arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=2.0))
ax.text(1.05, 1.55, r"upper side: $\cos\gamma>0$ -> $+$", fontsize=9, color="tab:green")
ax.text(1.05, 0.28, r"lower side: $\cos\gamma<0$ -> $-$", fontsize=9, color="tab:red")
ax.plot([0.4, 0.4, 1.6, 1.6], [0, 0, 0, 0], color="0.4", lw=1.0)
ax.text(1.0, -0.18, r"same projection $D$", fontsize=9, ha="center")
ax.set_xlim(0, 2.2); ax.set_ylim(-0.3, 1.8)
ax.set_xlabel("x"); ax.set_ylabel("z")
ax.set_title(r"same patch, opposite sides: $dx\,dy$ changes sign", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec20_fig3_sign.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: closed sphere, outward normals ----------------
fig = plt.figure(figsize=(6.0, 5.0))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi, 41); ph = np.linspace(0, 2 * np.pi, 61)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH),
                color="tab:purple", alpha=0.15, linewidth=0, rstride=3, cstride=3)
for (t0, p0) in [(0.6, 0.4), (0.6, 2.4), (2.5, 1.2), (2.5, 4.2)]:
    p = np.array([np.sin(t0) * np.cos(p0), np.sin(t0) * np.sin(p0), np.cos(t0)])
    ax.quiver(*p, *p * 0.45, color="tab:green", lw=1.8, arrow_length_ratio=0.15)
ax.text(0.2, 0.05, 1.35, "outward normals", fontsize=9, color="tab:green")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(-1.2, 1.4)
ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=18, azim=-58)
ax.set_title(r"closed surface: outward normals (the usual choice)", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec20_fig4_closed.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec20_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
