# 规模纪律：七张 3D SVG, 网格控制在 ~30x30, 目标 < 20 秒。
# 第 03 讲图 1-7：抛物柱面 / 旋转抛物面+母线 / 椭球 / 单叶双曲面 / 马鞍面 / 锥面 / 螺旋线与投影柱面。
# 图内文字只用 ASCII，不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

def new_ax(figsize=(4.8, 4.2)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(projection="3d")
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    return fig, ax

def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, format="svg")
    plt.close(fig)

# ---------------- fig 1: parabolic cylinder y = x^2 ----------------
fig, ax = new_ax()
u = np.linspace(-1.5, 1.5, 31)
v = np.linspace(0.0, 3.0, 21)
U, V = np.meshgrid(u, v)
ax.plot_surface(U, U ** 2, V, cmap="viridis", alpha=0.75, linewidth=0, antialiased=True)
ax.set_xlim(-1.6, 1.6); ax.set_ylim(-0.2, 2.4); ax.set_zlim(0, 3)
ax.view_init(elev=18, azim=-62)
ax.set_title(r"parabolic cylinder $y=x^2$", fontsize=10)
save(fig, "lec03_fig1_parabolic_cylinder.svg")

# ---------------- fig 2: paraboloid of revolution + generating curve ----------------
fig, ax = new_ax((5.2, 4.4))
r = np.linspace(0, 1.6, 31)
th = np.linspace(0, 2 * np.pi, 49)
R, TH = np.meshgrid(r, th)
ax.plot_surface(R * np.cos(TH), R * np.sin(TH), R ** 2, cmap="viridis",
                alpha=0.65, linewidth=0, antialiased=True, rstride=2, cstride=2)
y = np.linspace(-1.6, 1.6, 80)
ax.plot(np.zeros_like(y), y, y ** 2, color="tab:green", lw=2.4)
ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8); ax.set_zlim(0, 2.8)
ax.view_init(elev=20, azim=-60)
ax.set_title(r"$z=x^2+y^2$ from $z=y^2$ (green) about the z-axis", fontsize=9)
save(fig, "lec03_fig2_paraboloid_of_revolution.svg")

# ---------------- fig 3: ellipsoid x^2/4 + y^2 + z^2 = 1 ----------------
fig, ax = new_ax()
u = np.linspace(0, np.pi, 31)
v = np.linspace(0, 2 * np.pi, 49)
U, V = np.meshgrid(u, v)
ax.plot_surface(2 * np.sin(U) * np.cos(V), np.sin(U) * np.sin(V), np.cos(U),
                cmap="viridis", alpha=0.8, linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(-1.2, 1.2)
ax.view_init(elev=20, azim=-60)
ax.set_title(r"ellipsoid $x^2/4+y^2+z^2=1$", fontsize=10)
save(fig, "lec03_fig3_ellipsoid.svg")

# ---------------- fig 4: one-sheet hyperboloid x^2+y^2-z^2=1 ----------------
fig, ax = new_ax()
t = np.linspace(-1.8, 1.8, 31)
v = np.linspace(0, 2 * np.pi, 49)
T, V = np.meshgrid(t, v)
rad = np.sqrt(1 + T ** 2)
ax.plot_surface(rad * np.cos(V), rad * np.sin(V), T, cmap="viridis",
                alpha=0.7, linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.set_xlim(-2.8, 2.8); ax.set_ylim(-2.8, 2.8); ax.set_zlim(-1.9, 1.9)
ax.view_init(elev=18, azim=-58)
ax.set_title(r"one-sheet hyperboloid $x^2+y^2-z^2=1$", fontsize=9)
save(fig, "lec03_fig4_hyperboloid_one_sheet.svg")

# ---------------- fig 5: saddle z = x^2 - y^2 ----------------
fig, ax = new_ax()
x = np.linspace(-1.4, 1.4, 31)
y = np.linspace(-1.4, 1.4, 31)
X, Y = np.meshgrid(x, y)
ax.plot_surface(X, Y, X ** 2 - Y ** 2, cmap="coolwarm", alpha=0.85,
                linewidth=0, antialiased=True)
ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4); ax.set_zlim(-2, 2)
ax.view_init(elev=22, azim=-62)
ax.set_title(r"saddle $z=x^2-y^2$", fontsize=10)
save(fig, "lec03_fig5_saddle.svg")

# ---------------- fig 6: cone z^2 = x^2 + y^2 (two sheets) ----------------
fig, ax = new_ax()
r = np.linspace(0, 1.5, 21)
th = np.linspace(0, 2 * np.pi, 49)
R, TH = np.meshgrid(r, th)
ax.plot_surface(R * np.cos(TH), R * np.sin(TH), R, cmap="viridis",
                alpha=0.7, linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.plot_surface(R * np.cos(TH), R * np.sin(TH), -R, cmap="viridis",
                alpha=0.7, linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.set_zlim(-1.6, 1.6)
ax.view_init(elev=18, azim=-60)
ax.set_title(r"cone $z^2=x^2+y^2$ (two sheets)", fontsize=10)
save(fig, "lec03_fig6_cone.svg")

# ---------------- fig 7: helix + projection cylinder ----------------
fig, ax = new_ax((5.2, 4.4))
t = np.linspace(0, 4 * np.pi, 300)
ax.plot(np.cos(t), np.sin(t), t, color="tab:red", lw=2.0)
th = np.linspace(0, 2 * np.pi, 49)
z = np.linspace(0, 4 * np.pi, 25)
TH, Z = np.meshgrid(th, z)
ax.plot_surface(np.cos(TH), np.sin(TH), Z, color="tab:blue", alpha=0.12,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.plot(np.cos(th), np.sin(th), 0 * th, color="tab:blue", lw=1.4, ls="--")
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_zlim(0, 4 * np.pi)
ax.view_init(elev=20, azim=-62)
ax.set_title(r"helix $(\cos t,\sin t,t)$ and cylinder $x^2+y^2=1$", fontsize=9)
save(fig, "lec03_fig7_helix_projection.svg")

for p in sorted(OUT.glob("lec03_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
