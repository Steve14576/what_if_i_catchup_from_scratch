# 规模纪律：一张静态 SVG, 目标 < 1 秒。
# 第 06 讲图 1：复合函数 z=f(u,v), u=u(x,y), v=v(x,y) 的依赖树。
# 图内文字只用 ASCII 与 mathtext（不用 \lvert），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(6.8, 4.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis("off")

nodes = {
    "z": (5.0, 6.0, r"$z=f(u,v)$"),
    "u": (2.8, 4.0, r"$u(x,y)$"),
    "v": (7.2, 4.0, r"$v(x,y)$"),
}
for key, (x, y, text) in nodes.items():
    ax.text(x, y, text, ha="center", va="center", fontsize=12,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="black", lw=1.2))

# leaves of u and v
leaves = [("ux", 1.4, 1.8, "x"), ("uy", 4.2, 1.8, "y"),
          ("vx", 5.8, 1.8, "x"), ("vy", 8.6, 1.8, "y")]
for _, x, y, text in leaves:
    ax.text(x, y, r"$%s$" % text, ha="center", va="center", fontsize=12,
            bbox=dict(boxstyle="round,pad=0.3", fc="#f2f2f2", ec="black", lw=1.0))

def arrow(p, q, color="black", lw=1.4):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                shrinkA=24, shrinkB=18))

arrow((5.0, 6.0), (2.8, 4.0))
arrow((5.0, 6.0), (7.2, 4.0))
arrow((2.8, 4.0), (1.4, 1.8))
arrow((2.8, 4.0), (4.2, 1.8))
arrow((7.2, 4.0), (5.8, 1.8))
arrow((7.2, 4.0), (8.6, 1.8))

# highlight the two paths to x
arrow((5.0, 6.0), (2.8, 4.0), color="tab:red", lw=2.4)
arrow((2.8, 4.0), (1.4, 1.8), color="tab:red", lw=2.4)
arrow((5.0, 6.0), (7.2, 4.0), color="tab:blue", lw=2.4)
arrow((7.2, 4.0), (5.8, 1.8), color="tab:blue", lw=2.4)

ax.text(2.1, 3.0, "path 1", color="tab:red", fontsize=9, ha="right")
ax.text(7.9, 3.0, "path 2", color="tab:blue", fontsize=9, ha="left")
ax.text(5.0, 0.5,
        r"$\partial z/\partial x = f_u\,u_x + f_v\,v_x$  (two paths -> two terms)",
        ha="center", fontsize=10)
ax.set_title("dependency tree and the chain rule", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "lec06_fig1_tree.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: implicit curve, tangent and normal ----------------
fig, ax = plt.subplots(figsize=(5.6, 5.0))
t = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(t), np.sin(t), color="tab:blue", lw=2.0)
px, py = 0.6, 0.8
ax.scatter([px], [py], color="k", s=22)
ax.text(px + 0.05, py + 0.05, r"$P$", fontsize=11)
# normal vector (F_x, F_y) = (2x, 2y)
nx, ny = 2 * px, 2 * py
scale = 0.45 / np.hypot(nx, ny)
ax.annotate("", xy=(px + nx * scale, py + ny * scale), xytext=(px, py),
            arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=2.2))
ax.text(px + nx * scale * 1.1, py + ny * scale * 1.1, r"$(F_x,F_y)$",
        color="tab:red", fontsize=10)
# tangent line: slope -x/y
slope = -px / py
tx = np.array([-0.5, 0.9]) * 0.9 + px
ax.plot(tx, py + slope * (tx - px), color="tab:green", lw=1.8)
ax.text(px + 0.35, py + slope * 0.35 - 0.18, r"tangent: slope $= -x/y$",
        color="tab:green", fontsize=9)
ax.set_aspect("equal")
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.grid(alpha=0.3)
ax.axhline(0, color="0.8", lw=0.6)
ax.axvline(0, color="0.8", lw=0.6)
ax.set_title(r"$x^2+y^2=1$: $(F_x,F_y)$ is perpendicular to the tangent", fontsize=10)
fig.savefig(OUT / "lec06_fig2_implicit_geometry.svg", format="svg", bbox_inches="tight")
plt.close(fig)

# ---------------- fig 3: sphere equator: no single-valued z(x,y) ----------------
fig = plt.figure(figsize=(6.0, 5.2))
ax = fig.add_subplot(projection="3d")
u = np.linspace(0, np.pi, 41)
v = np.linspace(0, 2 * np.pi, 61)
U, V = np.meshgrid(u, v)
ax.plot_surface(np.sin(U) * np.cos(V), np.sin(U) * np.sin(V), np.cos(U),
                cmap="viridis", alpha=0.30, linewidth=0, antialiased=True,
                rstride=2, cstride=2)
t = np.linspace(0, 2 * np.pi, 300)
ax.plot(np.cos(t), np.sin(t), np.zeros_like(t), color="tab:red", lw=2.4)
# vertical line at (0.6,0.8,0): tangent to the sphere
ax.plot([0.6, 0.6], [0.8, 0.8], [-1.25, 1.25], color="tab:red", ls="--", lw=1.6)
ax.scatter([0.6], [0.8], [0.0], color="k", s=20)
ax.text(0.6, 0.8, 1.32, r"vertical line", color="tab:red", fontsize=9)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(-1.3, 1.3)
ax.view_init(elev=16, azim=-60)
ax.set_title("equator: one (x,y) meets two z values", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec06_fig3_sphere_equator.svg", format="svg")
plt.close(fig)

# helpers shared by the four form figures
def node(ax, xy, text, fc="white", fontsize=12):
    ax.text(xy[0], xy[1], text, ha="center", va="center", fontsize=fontsize,
            bbox=dict(boxstyle="round,pad=0.35", fc=fc, ec="black", lw=1.2), zorder=3)

def arrow(ax, p, q, color="black", lw=1.4, ls="-"):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color, ls=ls,
                                shrinkA=22, shrinkB=18), zorder=2)

# ---------------- fig 4: form 1, a three-level chain ----------------
fig, ax = plt.subplots(figsize=(5.8, 6.0))
ax.set_xlim(0, 7); ax.set_ylim(0, 7.4); ax.axis("off")
node(ax, (3.2, 6.4), r"$z=e^u$")
node(ax, (3.2, 4.8), r"$u=\sin s$")
node(ax, (3.2, 3.2), r"$s=t^2$")
node(ax, (3.2, 1.6), r"$t$", fc="#f2f2f2")
arrow(ax, (3.2, 6.4), (3.2, 4.8))
arrow(ax, (3.2, 4.8), (3.2, 3.2))
arrow(ax, (3.2, 3.2), (3.2, 1.6))
ax.text(3.5, 5.6, r"$dz/du=e^u$", fontsize=10)
ax.text(3.5, 4.0, r"$du/ds=\cos s$", fontsize=10)
ax.text(3.5, 2.4, r"$ds/dt=2t$", fontsize=10)
ax.text(3.2, 0.6, r"$dz/dt=e^u\cos s\cdot 2t$   (1 path, 3 factors)", ha="center", fontsize=10)
ax.set_title("form 1: three-level chain", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "lec06_fig4_three_level.svg", format="svg")
plt.close(fig)

# ---------------- fig 5: form 2, layered branching ----------------
fig, ax = plt.subplots(figsize=(8.2, 6.2))
ax.set_xlim(0, 8); ax.set_ylim(0, 7.6); ax.axis("off")
node(ax, (4.0, 6.8), r"$z=u^2+v$")
node(ax, (2.2, 5.1), r"$u=s^2+t$")
node(ax, (5.8, 5.1), r"$v=st$")
node(ax, (2.6, 3.3), r"$s=x+y$")
node(ax, (5.4, 3.3), r"$t=x-y$")
node(ax, (4.0, 1.7), r"$x$", fc="#f2f2f2")
arrow(ax, (4.0, 6.8), (2.2, 5.1), color="tab:blue", lw=1.9)
arrow(ax, (4.0, 6.8), (5.8, 5.1), color="tab:orange", lw=1.9)
arrow(ax, (2.2, 5.1), (2.6, 3.3), color="tab:blue", lw=1.9)
arrow(ax, (2.2, 5.1), (5.4, 3.3), color="tab:blue", lw=1.9)
arrow(ax, (5.8, 5.1), (2.6, 3.3), color="tab:orange", lw=1.9)
arrow(ax, (5.8, 5.1), (5.4, 3.3), color="tab:orange", lw=1.9)
arrow(ax, (2.6, 3.3), (4.0, 1.7))
arrow(ax, (5.4, 3.3), (4.0, 1.7))
ax.text(2.9, 5.95, r"$2u$", fontsize=10, color="tab:blue")
ax.text(4.9, 5.95, r"$1$", fontsize=10, color="tab:orange")
ax.text(1.6, 4.2, r"$2s$", fontsize=10, color="tab:blue")
ax.text(3.8, 4.35, r"$1$", fontsize=10, color="tab:blue")
ax.text(4.3, 4.35, r"$t$", fontsize=10, color="tab:orange")
ax.text(6.3, 4.2, r"$s$", fontsize=10, color="tab:orange")
ax.text(3.0, 2.5, r"$1$", fontsize=10)
ax.text(4.9, 2.5, r"$1$", fontsize=10)
ax.text(4.0, 0.6, r"4 paths: $96+16-1+3=114$", ha="center", fontsize=10)
ax.set_title("form 2: layered branching", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "lec06_fig5_branching.svg", format="svg")
plt.close(fig)

# ---------------- fig 6: form 3, direct + indirect ----------------
fig, ax = plt.subplots(figsize=(6.8, 5.4))
ax.set_xlim(0, 7); ax.set_ylim(0, 6.6); ax.axis("off")
node(ax, (3.4, 5.5), r"$z=x^2u$")
node(ax, (1.4, 3.6), r"$x$", fc="#f2f2f2")
node(ax, (5.4, 3.6), r"$u=x+y$")
node(ax, (5.4, 1.8), r"$y$", fc="#f2f2f2")
arrow(ax, (3.4, 5.5), (1.4, 3.6), color="tab:red", lw=2.3)
arrow(ax, (3.4, 5.5), (5.4, 3.6))
arrow(ax, (5.4, 3.6), (1.4, 3.6))
arrow(ax, (5.4, 3.6), (5.4, 1.8))
ax.text(1.9, 4.65, r"$f_x=2xu$ (direct)", color="tab:red", fontsize=10)
ax.text(4.2, 4.75, r"$f_u=x^2$", fontsize=10)
ax.text(3.4, 3.2, r"$u_x=1$", fontsize=10)
ax.text(5.6, 2.8, r"$u_y$", fontsize=10)
ax.text(3.4, 0.8, r"$z_x=2xu+x^2$; at $(1,2)$: $7$  (direct only: $6$)", ha="center", fontsize=9.5)
ax.set_title("form 3: direct + indirect", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "lec06_fig6_direct_indirect.svg", format="svg")
plt.close(fig)

# ---------------- fig 7: form 4, direct + indirect + layers ----------------
fig, ax = plt.subplots(figsize=(8.2, 6.2))
ax.set_xlim(0, 8); ax.set_ylim(0, 7.6); ax.axis("off")
node(ax, (4.0, 6.8), r"$z=x^2+y^2+u$")
node(ax, (2.2, 4.9), r"$y=x^2$")
node(ax, (6.0, 4.9), r"$u=xy$")
node(ax, (1.0, 3.0), r"$x$", fc="#f2f2f2")
arrow(ax, (4.0, 6.8), (1.0, 3.0), color="tab:red", lw=2.3)
arrow(ax, (4.0, 6.8), (2.2, 4.9))
arrow(ax, (4.0, 6.8), (6.0, 4.9))
arrow(ax, (2.2, 4.9), (1.0, 3.0), color="tab:blue", lw=1.9)
arrow(ax, (6.0, 4.9), (1.0, 3.0), color="tab:green", lw=1.9)
arrow(ax, (6.0, 4.9), (2.2, 4.9), color="tab:orange", lw=1.9)
ax.text(2.1, 5.75, r"$f_x=2x$", color="tab:red", fontsize=10)
ax.text(2.9, 5.55, r"$f_y=2y$", fontsize=10)
ax.text(5.0, 5.55, r"$f_u=1$", fontsize=10)
ax.text(1.2, 3.9, r"$y'=2x$", color="tab:blue", fontsize=10)
ax.text(3.0, 3.55, r"$u_x=y$", color="tab:green", fontsize=10)
ax.text(3.95, 4.55, r"$u_y=x$", color="tab:orange", fontsize=10)
ax.text(4.0, 0.8, r"4 paths: $2x+4xy+y+2x^2$; at $x=0.5$: $2.25$", ha="center", fontsize=10)
ax.set_title("form 4: direct + indirect + layers", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "lec06_fig7_combined.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec06_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)