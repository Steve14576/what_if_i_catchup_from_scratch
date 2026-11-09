# 规模纪律：三张静态 SVG, 目标 < 3 秒。
# 第 02 讲图 1-3：点法式平面 / 点到平面距离的投影 / 线面角与法向量的夹角。
# 图内文字只用 ASCII 与 mathtext（不用 \lvert，mathtext 不支持），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: plane by point + normal ----------------
fig = plt.figure(figsize=(6.2, 5.2))
ax = fig.add_subplot(projection="3d")

# plane x + y + z = 1, show triangle with vertices on axes
V = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
ax.add_collection3d(Poly3DCollection([V.tolist()], alpha=0.18,
                                     facecolor="tab:blue", edgecolor="tab:blue", lw=1.2))

M0 = np.array([1.0, 0.0, 0.0])       # point on plane
M = np.array([0.0, 1.0, 0.0])        # another point on plane
n = np.array([1.0, 1.0, 1.0])        # normal (scaled for display)
n_show = 0.55 * n
ax.quiver(*M0, *n_show, color="tab:red", lw=2.2)
ax.quiver(*M0, *(M - M0), color="tab:green", lw=2.0)
ax.scatter(*M0, color="k", s=18)
ax.text(*(M0 + 0.06), r"$M_0$", fontsize=11)
ax.text(*(M - 0.18), r"$M$", fontsize=11)
ax.text(*(M0 + n_show * 1.02), r"$\mathbf{n}$", color="tab:red", fontsize=12)
ax.text(*(M0 + 0.5 * (M - M0) + np.array([0.0, 0.0, 0.08])),
        r"$M_0M$", color="tab:green", fontsize=11)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_xlim(-0.1, 1.5)
ax.set_ylim(-0.1, 1.5)
ax.set_zlim(-0.1, 1.5)
ax.view_init(elev=24, azim=-56)
ax.set_title(r"plane: $\mathbf{n}\cdot\overrightarrow{M_0M}=0$", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "lec02_fig1_plane_normal.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: distance = projection on normal (2D section) ----------------
fig, ax = plt.subplots(figsize=(6.4, 3.8))
# plane seen edge-on: a line through (0, 0) with small slope
xline = np.array([-1.0, 3.0])
ax.plot(xline, 0.25 * xline, color="tab:blue", lw=2.0)
ax.text(2.55, 0.25 * 2.55 + 0.08, r"plane $\Pi$", color="tab:blue", fontsize=10)

M1 = np.array([0.4, 0.1])            # point on plane
P = np.array([2.1, 2.2])             # external point
n_hat = np.array([-0.25, 1.0]) / np.linalg.norm([-0.25, 1.0])
foot = P - np.dot(P - M1, n_hat) * n_hat

ax.plot([M1[0], P[0]], [M1[1], P[1]], color="tab:green", lw=1.6)
ax.plot([P[0], foot[0]], [P[1], foot[1]], ":", color="tab:red", lw=1.4)
ax.plot([M1[0], M1[0] + 0.75 * n_hat[0]], [M1[1], M1[1] + 0.75 * n_hat[1]],
        color="tab:red", lw=2.0)
ax.scatter(*M1, color="k", s=16)
ax.scatter(*P, color="k", s=16)
ax.scatter(*foot, color="tab:red", s=16)
ax.text(M1[0] - 0.12, M1[1] + 0.08, r"$M_1$", fontsize=11)
ax.text(P[0] + 0.05, P[1] + 0.05, r"$P$", fontsize=11)
ax.text(foot[0] - 0.05, foot[1] - 0.22, r"foot", fontsize=9, color="tab:red")
ax.text(M1[0] + 0.78 * n_hat[0], M1[1] + 0.78 * n_hat[1], r"$\mathbf{n}$",
        color="tab:red", fontsize=12)
ax.text(1.05, 1.28, r"$d=\frac{|\mathbf{n}\cdot\overrightarrow{M_1P}|}{|\mathbf{n}|}$",
        fontsize=11)
ax.set_aspect("equal")
ax.set_xlim(-0.8, 3.0)
ax.set_ylim(-0.6, 2.6)
ax.axis("off")
ax.set_title("distance from a point to a plane: projection on the normal", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec02_fig2_distance_projection.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: line-plane angle vs angle with the normal ----------------
fig, ax = plt.subplots(figsize=(6.2, 3.8))
ax.plot(xline, np.zeros_like(xline), color="tab:blue", lw=2.0)
ax.text(2.45, 0.06, r"plane", color="tab:blue", fontsize=10)

O = np.array([0.9, 0.0])
s_hat = np.array([0.86, 0.51]) / np.linalg.norm([0.86, 0.51])   # line direction
n_hat = np.array([0.0, 1.0])                                     # plane normal

ax.plot([O[0] - 0.9 * s_hat[0], O[0] + 1.5 * s_hat[0]],
        [O[1] - 0.9 * s_hat[1], O[1] + 1.5 * s_hat[1]], color="tab:green", lw=1.8)
ax.plot([O[0], O[0] + 0.95 * n_hat[0]], [O[1], O[1] + 0.95 * n_hat[1]],
        color="tab:red", lw=2.0)
ax.text(O[0] + 0.03, O[1] + 0.98, r"$\mathbf{n}$", color="tab:red", fontsize=12)
ax.text(O[0] + 1.45 * s_hat[0], O[1] + 1.45 * s_hat[1], r"$\mathbf{s}$",
        color="tab:green", fontsize=12)
# angle arc between s and plane
import matplotlib.patches as mpatches
ax.add_patch(mpatches.Arc(O, 0.7, 0.7, theta1=0, theta2=30.5, color="k", lw=1.0))
ax.text(O[0] + 0.38, O[1] + 0.10, r"$\theta$", fontsize=11)
# angle between s and n
ax.add_patch(mpatches.Arc(O, 0.5, 0.5, theta1=30.5, theta2=90, color="tab:red", lw=1.0))
ax.text(O[0] + 0.12, O[1] + 0.30, r"$\varphi$", color="tab:red", fontsize=11)
ax.text(-0.6, 1.55, r"$\sin\theta=|\mathbf{s}\cdot\mathbf{n}|/(|\mathbf{s}||\mathbf{n}|)$",
        fontsize=11)
ax.set_aspect("equal")
ax.set_xlim(-0.8, 2.6)
ax.set_ylim(-0.5, 2.0)
ax.axis("off")
ax.set_title(r"line-plane angle: $\theta+\varphi=90^\circ$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec02_fig3_line_plane_angle.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec02_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
