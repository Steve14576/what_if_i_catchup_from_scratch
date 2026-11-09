# 规模纪律：5 张静态 SVG, 目标 < 4 秒。
# 第 07 讲图：切平面/法线、法向与切线、曲线切线/法平面、交线叉积、退化边界。
# 图内文字只用 ASCII 与 mathtext（Unicode 符号 ∇ × ∥ θ 直接作字符），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def clean(ax):
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")


# ---------------- fig 1: tangent plane and normal of z = x^2+y^2 at (1,1,2) ----------------
fig = plt.figure(figsize=(6.6, 5.4))
ax = fig.add_subplot(projection="3d")
u = np.linspace(0, 2, 31)
U, V = np.meshgrid(u, u)
ax.plot_surface(U, V, U ** 2 + V ** 2, cmap="viridis", alpha=0.45,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.plot_surface(U, V, 2 * U + 2 * V - 2, color="tab:red", alpha=0.30,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
t = np.linspace(-0.9, 0.9, 40)
ax.plot(1 + 2 * t, 1 + 2 * t, 2 - t, color="k", lw=2.2)
ax.scatter([1], [1], [2], color="k", s=22)
ax.text(1.1, 1.0, 2.2, r"$P_0(1,1,2)$", fontsize=9)
ax.text(1.9, 1.1, 3.6, r"$∇F=(2,2,-1)$", fontsize=9)
ax.set_xlim(0, 2); ax.set_ylim(0, 2); ax.set_zlim(0, 6)
ax.view_init(elev=20, azim=-62)
ax.set_title("tangent plane and normal (surface + plane + line)", fontsize=10)
clean(ax)
fig.tight_layout()
fig.savefig(OUT / "lec07_fig1_tangent_plane.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: normal is perpendicular to two curve tangents ----------------
fig = plt.figure(figsize=(6.4, 5.4))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi, 41); ph = np.linspace(0, 2 * np.pi, 61)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH),
                cmap="viridis", alpha=0.25, linewidth=0, antialiased=True,
                rstride=2, cstride=2)
# latitude circle at z = sqrt2/2
phi = np.linspace(0, 2 * np.pi, 200); r0 = np.sqrt(0.5)
ax.plot(r0 * np.cos(phi), r0 * np.sin(phi), np.full_like(phi, np.sqrt(0.5)),
        color="tab:blue", lw=2.0)
# meridian through (0.5,0.5,0.707)
tt = np.linspace(0, np.pi, 200)
ax.plot(np.sin(tt) * np.cos(np.pi / 4), np.sin(tt) * np.sin(np.pi / 4), np.cos(tt),
        color="tab:green", lw=2.0)
P = np.array([0.5, 0.5, np.sqrt(0.5)])
n = P / np.linalg.norm(P)
ax.quiver(*P, *(0.55 * n), color="k", lw=2.2, arrow_length_ratio=0.12)
T1 = np.array([-np.sin(np.pi / 4), np.cos(np.pi / 4), 0.0]) * 0.5
T2 = np.array([np.cos(np.pi / 4) * np.cos(np.pi / 4),
               np.cos(np.pi / 4) * np.sin(np.pi / 4), -np.sin(np.pi / 4)]) * 0.5
ax.quiver(*P, *T1, color="tab:blue", lw=2.0, arrow_length_ratio=0.15)
ax.quiver(*P, *T2, color="tab:green", lw=2.0, arrow_length_ratio=0.15)
ax.scatter(*P, color="k", s=20)
ax.text(0.75, 0.6, 0.95, r"$∇F$", fontsize=10)
ax.text(0.2, 0.85, 0.55, "tangent 1", color="tab:blue", fontsize=8)
ax.text(0.95, 0.4, 0.45, "tangent 2", color="tab:green", fontsize=8)
ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
ax.view_init(elev=18, azim=-55)
ax.set_title("normal is perpendicular to tangents of all curves", fontsize=9)
clean(ax)
fig.tight_layout()
fig.savefig(OUT / "lec07_fig2_normal_perp.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: helix tangent line and normal plane ----------------
fig = plt.figure(figsize=(6.6, 5.6))
ax = fig.add_subplot(projection="3d")
t = np.linspace(-0.4, 2.2, 300)
ax.plot(np.cos(t), np.sin(t), t, color="tab:blue", lw=2.0)
t0 = np.pi / 4
P0 = np.array([np.cos(t0), np.sin(t0), t0])
T = np.array([-np.sin(t0), np.cos(t0), 1.0]); T = T / np.linalg.norm(T)
s = np.linspace(-0.8, 0.8, 20)
ax.plot(P0[0] + T[0] * s, P0[1] + T[1] * s, P0[2] + T[2] * s, color="tab:red", lw=2.4)
# normal plane through P0 with normal T
e1 = np.array([1.0, 1.0, 0.0]); e1 = e1 / np.linalg.norm(e1)
e2 = np.cross(T, e1)
c = P0
q = np.array([[c + 0.55 * e1 + 0.55 * e2, c + 0.55 * e1 - 0.55 * e2,
               c - 0.55 * e1 - 0.55 * e2, c - 0.55 * e1 + 0.55 * e2]])
ax.add_collection3d(Poly3DCollection(q, alpha=0.25, facecolor="tab:green",
                                     edgecolor="tab:green"))
ax.scatter(*P0, color="k", s=22)
ax.text(P0[0] + 0.1, P0[1] + 0.1, P0[2] + 0.15, r"$P_0$", fontsize=9)
ax.text(-1.3, 0.4, 1.9, "normal plane", color="tab:green", fontsize=8)
ax.text(0.4, 1.1, 1.4, "tangent line", color="tab:red", fontsize=8)
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_zlim(-0.5, 2.4)
ax.view_init(elev=18, azim=-60)
ax.set_title("space curve: tangent line + normal plane", fontsize=10)
clean(ax)
fig.tight_layout()
fig.savefig(OUT / "lec07_fig4_curve_tangent.svg", format="svg")
plt.close(fig)

# ---------------- fig 5: intersection curve, T = grad F x grad G ----------------
fig = plt.figure(figsize=(6.6, 5.4))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi, 41); ph = np.linspace(0, 2 * np.pi, 61)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sqrt(6) * np.sin(TH) * np.cos(PH), np.sqrt(6) * np.sin(TH) * np.sin(PH),
                np.sqrt(6) * np.cos(TH), cmap="viridis", alpha=0.16,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
r = np.linspace(0, 1.5, 25); a = np.linspace(0, 2 * np.pi, 61)
R, A = np.meshgrid(r, a)
ax.plot_surface(R * np.cos(A), R * np.sin(A), R ** 2, cmap="coolwarm", alpha=0.18,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
ph2 = np.linspace(0, 2 * np.pi, 200)
ax.plot(np.sqrt(2) * np.cos(ph2), np.sqrt(2) * np.sin(ph2), np.full_like(ph2, 2.0),
        color="k", lw=2.4)
P = np.array([1.0, 1.0, 2.0])
ax.quiver(*P, 0.7, 0.7, 1.4, color="tab:red", lw=2.0, arrow_length_ratio=0.15)
ax.quiver(*P, 0.7, 0.7, -0.35, color="tab:blue", lw=2.0, arrow_length_ratio=0.15)
ax.quiver(*P, -0.9, 0.9, 0.0, color="k", lw=2.4, arrow_length_ratio=0.12)
ax.scatter(*P, color="k", s=22)
ax.text(0.4, 1.5, 3.2, r"$∇F$", color="tab:red", fontsize=10)
ax.text(1.2, 1.3, 1.3, r"$∇G$", color="tab:blue", fontsize=10)
ax.text(0.0, 1.5, 1.9, r"$T=∇F×∇G$", fontsize=10)
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6); ax.set_zlim(-1, 3.6)
ax.view_init(elev=14, azim=-64)
ax.set_title("intersection curve: tangent is the cross product", fontsize=9)
clean(ax)
fig.tight_layout()
fig.savefig(OUT / "lec07_fig5_intersection.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: F_z = 0 case: vertical tangent plane at the equator ----------------
fig = plt.figure(figsize=(6.0, 5.2))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi, 41); ph = np.linspace(0, 2 * np.pi, 61)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH),
                cmap="viridis", alpha=0.22, linewidth=0, antialiased=True,
                rstride=2, cstride=2)
q = np.array([[[1, -1.3, -1.3], [1, 1.3, -1.3], [1, 1.3, 1.3], [1, -1.3, 1.3]]])
ax.add_collection3d(Poly3DCollection(q, alpha=0.25, facecolor="tab:red",
                                     edgecolor="tab:red"))
ax.plot([0, 1.6], [0, 0], [0, 0], color="k", lw=2.4)
ax.scatter([1], [0], [0], color="k", s=22)
ax.text(1.05, 0.05, 0.12, r"$P_0(1,0,0)$", fontsize=9)
ax.text(1.5, 0.1, 0.2, r"$∇F=(2,0,0)$", fontsize=9)
ax.set_xlim(-1.2, 1.8); ax.set_ylim(-1.3, 1.3); ax.set_zlim(-1.3, 1.3)
ax.view_init(elev=12, azim=-50)
ax.set_title("equator: tangent plane is vertical (F_z = 0)", fontsize=9)
clean(ax)
fig.tight_layout()
fig.savefig(OUT / "lec07_fig3_vertical_plane.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec07_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
