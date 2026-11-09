# 规模纪律：两张静态 SVG, 目标 < 2 秒。
# 第 05 讲图 1-2：强弱关系图 / sqrt(|xy|) 的比值随方向变化。
# 图内文字只用 ASCII 与 mathtext（不用 \lvert），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: relations among continuity / partials / differentiability ----------------
fig, ax = plt.subplots(figsize=(7.2, 4.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.4)
ax.axis("off")

boxes = {
    "pc": (2.0, 5.0, "partials\ncontinuous"),
    "df": (5.0, 3.4, "differentiable"),
    "ct": (8.0, 5.0, "continuous"),
    "pe": (5.0, 1.2, "partials exist"),
}
for key, (x, y, text) in boxes.items():
    ax.text(x, y, text, ha="center", va="center", fontsize=11,
            bbox=dict(boxstyle="round,pad=0.45", fc="white", ec="black", lw=1.2))

def arrow(a, b, style="-", color="black", label=None, dy=0.0):
    xa, ya, _ = boxes[a]
    xb, yb, _ = boxes[b]
    ax.annotate("", xy=(xb, yb), xytext=(xa, ya),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, linestyle=style, color=color,
                                shrinkA=26, shrinkB=26))
    if label:
        ax.text((xa + xb) / 2, (ya + yb) / 2 + dy, label, fontsize=9, color=color,
                ha="center")

arrow("pc", "df", label="sufficient")
arrow("df", "ct", label="yes")
arrow("df", "pe", label="yes")
arrow("ct", "pe", style=":", color="tab:red", label=r"no: $\sqrt{x^2+y^2}$", dy=0.25)
arrow("pe", "ct", style=":", color="tab:red", label=r"no: piecewise", dy=-0.25)
arrow("pe", "df", style=":", color="tab:red", label=r"no: $\sqrt{|xy|}$", dy=0.0)
ax.set_title("solid: implication; dotted: implication fails (counterexample)", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec05_fig1_relations.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: sqrt(|xy|)/rho depends on direction ----------------
fig, ax = plt.subplots(figsize=(6.0, 3.8))
th = np.linspace(0, 2 * np.pi, 720)
ratio = np.sqrt(np.abs(np.cos(th) * np.sin(th)))
ax.plot(np.degrees(th), ratio, color="tab:blue", lw=1.8)
ax.axhline(1 / np.sqrt(2), color="tab:red", ls="--", lw=1.0)
ax.text(200, 1 / np.sqrt(2) + 0.04, r"$1/\sqrt{2}$", color="tab:red", fontsize=10)
ax.set_xlabel(r"direction angle $\theta$ (degrees)")
ax.set_ylabel(r"$f/\rho$ along the ray")
ax.set_xlim(0, 360)
ax.set_ylim(-0.03, 0.8)
ax.grid(alpha=0.3)
ax.set_title(r"$f=\sqrt{|xy|}$: $f/\rho$ depends on the direction", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec05_fig2_nonDiff.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: partial derivatives as section-curve slopes ----------------
fig = plt.figure(figsize=(6.4, 5.2))
ax = fig.add_subplot(projection="3d")
u = np.linspace(-1.2, 1.6, 41)
v = np.linspace(-1.2, 1.6, 41)
U, V = np.meshgrid(u, v)
ax.plot_surface(U, V, U ** 2 + V ** 2, cmap="viridis", alpha=0.5,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
xs = np.linspace(-1.2, 1.6, 120)
ax.plot(xs, np.ones_like(xs), xs ** 2 + 1, color="tab:blue", lw=2.2)   # y = 1
ys = np.linspace(-1.2, 1.6, 120)
ax.plot(np.ones_like(ys), ys, 1 + ys ** 2, color="tab:green", lw=2.2)  # x = 1
# tangent lines at (1,1,2)
t = np.linspace(-0.6, 0.6, 50)
ax.plot(1 + t, np.ones_like(t), 2 + 2 * t, color="tab:red", lw=2.6)
ax.plot(np.ones_like(t), 1 + t, 2 + 2 * t, color="tab:orange", lw=2.6)
ax.scatter([1], [1], [2], color="k", s=22)
ax.text(1.05, 1.0, 2.1, r"$(1,1,2)$", fontsize=9)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-1.2, 1.6); ax.set_ylim(-1.2, 1.6); ax.set_zlim(0, 4.5)
ax.view_init(elev=22, azim=-60)
ax.set_title("partial derivatives: slopes of the two section curves", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec05_fig3_partials_geometry.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: differentiability = local plane approximation ----------------
fig = plt.figure(figsize=(6.4, 5.2))
ax = fig.add_subplot(projection="3d")
u = np.linspace(0.2, 1.8, 31)
v = np.linspace(0.2, 1.8, 31)
U, V = np.meshgrid(u, v)
ax.plot_surface(U, V, U ** 2 + V ** 2, cmap="viridis", alpha=0.55,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.plot_surface(U, V, 2 * U + 2 * V - 2, color="tab:red", alpha=0.28,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.scatter([1], [1], [2], color="k", s=22)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0.2, 1.8); ax.set_ylim(0.2, 1.8); ax.set_zlim(0.5, 7.0)
ax.view_init(elev=20, azim=-60)
ax.set_title(r"differentiable: surface and its approximating plane" "\n"
             r"$z=2+2(x-1)+2(y-1)$ near $(1,1,2)$", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec05_fig4_linear_approx.svg", format="svg")
plt.close(fig)

# ---------------- fig 5: surface of sqrt(|xy|) ----------------
fig = plt.figure(figsize=(6.2, 5.0))
ax = fig.add_subplot(projection="3d")
u = np.linspace(-1.0, 1.0, 81)
v = np.linspace(-1.0, 1.0, 81)
U, V = np.meshgrid(u, v)
ax.plot_surface(U, V, np.sqrt(np.abs(U * V)), cmap="coolwarm", alpha=0.9,
                linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(0, 1)
ax.view_init(elev=24, azim=-58)
ax.set_title(r"$z=\sqrt{|xy|}$: a ridge at the origin (not a plane)", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec05_fig5_sqrt_abs_xy.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec05_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
