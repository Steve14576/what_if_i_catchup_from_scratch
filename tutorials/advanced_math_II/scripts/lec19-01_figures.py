# 规模纪律：4 张静态 SVG, 目标 < 5 秒。
# 第 19 讲图：面元投影、参数曲面、球面面元、投影重叠。
# 图内文字只用 ASCII 与 mathtext（≤ 用 Unicode；不用 \mathbf / \oint），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: surface patch vs its projection ----------------
fig = plt.figure(figsize=(6.4, 5.2))
ax = fig.add_subplot(projection="3d")
u = np.linspace(0, 1, 21)
U, V = np.meshgrid(u, u)
Z = 0.3 + 0.45 * U + 0.30 * V
ax.plot_surface(U, V, Z, color="tab:blue", alpha=0.35, linewidth=0)
ax.plot_surface(U, V, np.zeros_like(U), color="0.85", alpha=0.35, linewidth=0)
# highlight a small patch
u0, v0, s = 0.45, 0.40, 0.22
ax.plot([u0, u0 + s, u0 + s, u0, u0], [v0, v0, v0 + s, v0 + s, v0],
        [0.3 + 0.45 * a + 0.30 * b for a, b in
         [(u0, v0), (u0 + s, v0), (u0 + s, v0 + s), (u0, v0 + s), (u0, v0)]],
        color="tab:red", lw=1.6)
# projection patch
ax.plot([u0, u0 + s, u0 + s, u0, u0], [v0, v0, v0 + s, v0 + s, v0],
        [0, 0, 0, 0, 0], color="tab:red", lw=1.4, ls="--")
for a, b in [(u0, v0), (u0 + s, v0), (u0 + s, v0 + s), (u0, v0 + s)]:
    ax.plot([a, a], [b, b], [0, 0.3 + 0.45 * a + 0.30 * b], color="0.5", lw=0.8)
ax.text(u0 + s + 0.05, v0 + s + 0.05, 0.3 + 0.45 * (u0 + s) + 0.30 * (v0 + s), r"$dS$",
        color="tab:red", fontsize=10)
ax.text(u0 + 0.02, v0 - 0.12, 0.0, r"$d\sigma$", color="tab:red", fontsize=9)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1.2)
ax.set_box_aspect((1, 1, 1.2))
ax.view_init(elev=22, azim=-58)
ax.set_title(r"patch $dS$ projects to $d\sigma=dS\,|\cos\gamma|$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec19_fig1_projection.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: parametric patch, r_u x r_v ----------------
fig = plt.figure(figsize=(6.2, 5.0))
ax = fig.add_subplot(projection="3d")
u = np.linspace(0, 1, 21)
U, V = np.meshgrid(u, u)
Z = 0.3 + 0.6 * U ** 2 + 0.3 * V
ax.plot_surface(U, V, Z, color="tab:green", alpha=0.30, linewidth=0)
u0, v0 = 0.5, 0.4
p = np.array([u0, v0, 0.3 + 0.6 * u0 ** 2 + 0.3 * v0])
ru = np.array([0.25, 0, 0.6 * 2 * u0 * 0.25])
rv = np.array([0, 0.25, 0.3 * 0.25])
ax.quiver(*p, *ru, color="tab:red", lw=2.0, arrow_length_ratio=0.12)
ax.quiver(*p, *rv, color="tab:orange", lw=2.0, arrow_length_ratio=0.12)
poly = [p, p + ru, p + ru + rv, p + rv, p]
ax.plot([q[0] for q in poly], [q[1] for q in poly], [q[2] for q in poly], color="tab:red", lw=1.2)
ax.text(*(p + ru * 0.6), r"$r_u$", color="tab:red", fontsize=10)
ax.text(*(p + rv * 0.6), r"$r_v$", color="tab:orange", fontsize=10)
ax.text(*(p + 0.5 * (ru + rv)), r"$dS$", fontsize=10)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1.15)
ax.set_box_aspect((1, 1, 1.15))
ax.view_init(elev=22, azim=-58)
ax.set_title(r"parametric patch: $dS=|r_u\times r_v|\,du\,dv$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec19_fig2_param.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: spherical area element ----------------
fig = plt.figure(figsize=(6.0, 5.0))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi, 41); ph = np.linspace(0, 2 * np.pi, 61)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH),
                color="tab:purple", alpha=0.18, linewidth=0, rstride=2, cstride=2)
# patch at phi0, theta0
phi0, theta0, dp, dt = np.pi / 3, np.pi / 6, 0.25, 0.3
pp = np.linspace(phi0, phi0 + dp, 20)
tt = np.linspace(theta0, theta0 + dt, 20)
for a in [phi0, phi0 + dp]:
    ax.plot(np.sin(a) * np.cos(tt), np.sin(a) * np.sin(tt), np.full_like(tt, np.cos(a)),
            color="tab:red", lw=1.6)
for b in [theta0, theta0 + dt]:
    ax.plot(np.sin(pp) * np.cos(b), np.sin(pp) * np.sin(b), np.cos(pp),
            color="tab:red", lw=1.6)
ax.text(0.15, 0.05, 0.95, r"$dS=R^2\sin\varphi\,d\varphi\,d\theta$", fontsize=10)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1)
ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=18, azim=-58)
ax.set_title(r"sphere: area element from latitude radius $R\sin\varphi$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec19_fig3_sphere.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: projection overlap (whole sphere) ----------------
fig = plt.figure(figsize=(6.0, 5.0))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi, 41); ph = np.linspace(0, 2 * np.pi, 61)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH),
                color="tab:purple", alpha=0.12, linewidth=0, rstride=3, cstride=3)
tt = np.linspace(0, 2 * np.pi, 100)
ax.plot(np.cos(tt), np.sin(tt), np.zeros_like(tt), color="tab:red", lw=2.0)
for a in [0.2, 1.8, 3.4, 5.0]:
    b = a + 0.4
    ax.plot([np.cos(a), np.cos(b)], [np.sin(a), np.sin(b)], [0, 0], color="tab:red", lw=2.0)
ax.text(-0.9, 0.7, 0.65, "upper half", fontsize=9)
ax.text(-0.9, 0.55, -0.75, "lower half", fontsize=9)
ax.text(-1.05, -1.15, 0.05, r"same disk: overlap", fontsize=9, color="tab:red")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1)
ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=18, azim=-58)
ax.set_title(r"whole sphere: upper and lower halves share one projection", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec19_fig4_overlap.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec19_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
