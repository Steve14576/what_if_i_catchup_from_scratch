# 规模纪律：三张静态 SVG, 目标 < 3 秒。
# 第 01 讲图 1-3：向量加法 / 数量积投影 / 向量积的面积与法向。
# 图内文字只用 ASCII 与 mathtext（不放中文），避开中文字体缺字形与 U+2212 方块的已知问题。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def arrow(ax, start, vec, color, label=None, lw=1.8):
    ax.annotate("", xy=(start[0] + vec[0], start[1] + vec[1]), xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0))
    if label:
        ax.text(start[0] + vec[0] * 0.55 + 0.08, start[1] + vec[1] * 0.55 + 0.08, label,
                color=color, fontsize=11)


# ---------------- fig 1: vector addition ----------------
fig, ax = plt.subplots(figsize=(4.6, 4.0))
a = np.array([2.0, 1.0])
b = np.array([1.0, 2.0])
arrow(ax, (0, 0), a, "tab:blue", r"$\mathbf{a}$")
arrow(ax, (0, 0), b, "tab:green", r"$\mathbf{b}$")
arrow(ax, (0, 0), a + b, "tab:red", r"$\mathbf{a}+\mathbf{b}$")
arrow(ax, (0, 0), 2 * a, "tab:blue", r"$2\mathbf{a}$", lw=1.0)
arrow(ax, (0, 0), -0.5 * b, "tab:green", r"$-\frac{1}{2}\mathbf{b}$", lw=1.0)
ax.plot([b[0], a[0] + b[0]], [b[1], a[1] + b[1]], "--", color="tab:red", lw=0.9)
ax.plot([a[0], a[0] + b[0]], [a[1], a[1] + b[1]], "--", color="tab:red", lw=0.9)
ax.set_xlim(-1.3, 3.9)
ax.set_ylim(-1.4, 3.6)
ax.set_aspect("equal")
ax.grid(alpha=0.3)
ax.axhline(0, color="0.7", lw=0.6)
ax.axvline(0, color="0.7", lw=0.6)
ax.set_title(r"vector addition: $\mathbf{a}+\mathbf{b}$", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "lec01_fig1_vector_add.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: projection (acute and obtuse) ----------------
fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6))
cases = [("acute: projection > 0", np.array([3.0, 0.6]), np.array([1.6, 1.9])),
         ("obtuse: projection < 0", np.array([3.0, 0.6]), np.array([-1.6, 1.9]))]
for ax, (title, a, b) in zip(axes, cases):
    ea = a / np.linalg.norm(a)
    t = np.dot(b, ea)                      # signed scalar projection of b on a
    foot = t * ea
    arrow(ax, (0, 0), a, "tab:blue", r"$\mathbf{a}$")
    arrow(ax, (0, 0), b, "tab:green", r"$\mathbf{b}$")
    ax.plot([b[0], foot[0]], [b[1], foot[1]], ":", color="0.4", lw=1.0)
    ax.plot([foot[0]], [foot[1]], "o", color="tab:red", ms=4)
    ax.plot([0, foot[0]], [0, foot[1]], "-", color="tab:red", lw=2.2, alpha=0.55)
    ax.text(0.03, -0.55, rf"$\mathrm{{Prj}}={t:.2f}$", color="tab:red", fontsize=10)
    ax.set_title(title, fontsize=10)
    ax.set_xlim(-2.4, 3.6)
    ax.set_ylim(-1.0, 2.9)
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    ax.axhline(0, color="0.7", lw=0.6)
    ax.axvline(0, color="0.7", lw=0.6)
fig.suptitle(r"scalar projection of $\mathbf{b}$ on $\mathbf{a}$", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "lec01_fig2_projection.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: cross product: area and normal ----------------
fig = plt.figure(figsize=(6.4, 5.4))
ax = fig.add_subplot(projection="3d")
a = np.array([2.0, 0.4, 0.0])
b = np.array([0.8, 2.0, 0.0])
c = np.cross(a, b)
scale = 0.45 * np.linalg.norm(c)
cn = c / np.linalg.norm(c) * scale

origin = np.zeros(3)
for vec, color, label in [(a, "tab:blue", r"$\mathbf{a}$"),
                          (b, "tab:green", r"$\mathbf{b}$"),
                          (cn, "tab:red", r"$\mathbf{a}\times\mathbf{b}$")]:
    ax.quiver(*origin, *vec, color=color, arrow_length_ratio=0.12, lw=2)
    ax.text(*(vec * 1.08), label, color=color, fontsize=11)

poly = Poly3DCollection(
    [[tuple(origin), tuple(a), tuple(a + b), tuple(b)]],
    alpha=0.18, facecolor="tab:red", edgecolor="tab:red", lw=1.2)
ax.add_collection3d(poly)

ax.set_xlim(-0.2, 3.2)
ax.set_ylim(-0.2, 3.2)
ax.set_zlim(-0.2, 3.0)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.view_init(elev=22, azim=-58)
ax.set_title(r"$|\mathbf{a}\times\mathbf{b}|$ = parallelogram area;"
             "\n" r"direction perpendicular to both (right hand rule)", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec01_fig3_cross_product.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec01_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
