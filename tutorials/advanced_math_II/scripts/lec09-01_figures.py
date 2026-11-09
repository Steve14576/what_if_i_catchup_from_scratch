# 规模纪律：4 张静态 SVG, 目标 < 4 秒。
# 第 09 讲图：极小与鞍点、二次型分类、约束极值的相切、xyz 在平面上的最大。
# 图内文字只用 ASCII 与 mathtext（Unicode ∇ Δ λ 直接作字符），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: minimum vs saddle ----------------
fig = plt.figure(figsize=(10.2, 4.4))
u = np.linspace(-1.2, 1.2, 31)
U, V = np.meshgrid(u, u)

ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax1.plot_surface(U, V, U ** 2 + V ** 2, cmap="viridis", alpha=0.75,
                 linewidth=0, antialiased=True, rstride=2, cstride=2)
ax1.scatter([0], [0], [0], color="k", s=24)
ax1.set_title("minimum: z = x^2 + y^2", fontsize=10)
ax1.set_xlabel("x"); ax1.set_ylabel("y"); ax1.set_zlabel("z")
ax1.view_init(elev=22, azim=-60)
ax1.set_zlim(0, 3)

ax2 = fig.add_subplot(1, 2, 2, projection="3d")
ax2.plot_surface(U, V, U ** 2 - V ** 2, cmap="coolwarm", alpha=0.75,
                 linewidth=0, antialiased=True, rstride=2, cstride=2)
ax2.scatter([0], [0], [0], color="k", s=24)
ax2.set_title("saddle: z = x^2 - y^2", fontsize=10)
ax2.set_xlabel("x"); ax2.set_ylabel("y"); ax2.set_zlabel("z")
ax2.view_init(elev=22, azim=-60)
ax2.set_zlim(-2, 2)
fig.tight_layout()
fig.savefig(OUT / "lec09_fig1_min_saddle.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: sign patterns of the quadratic form ----------------
u = np.linspace(-1.5, 1.5, 200)
U, V = np.meshgrid(u, u)
forms = [(U ** 2 + V ** 2, "Delta > 0, A > 0: minimum"),
         (U ** 2 - V ** 2, "Delta < 0: saddle"),
         (U ** 2, "Delta = 0: test fails")]
fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.8))
for ax, (Z, title) in zip(axes, forms):
    ax.contour(U, V, Z, levels=[0.1, 0.35, 0.8, 1.4], colors="tab:blue", linewidths=1.3)
    ax.axhline(0, color="0.8", lw=0.7); ax.axvline(0, color="0.8", lw=0.7)
    ax.scatter([0], [0], color="k", s=18)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("u"); ax.set_ylabel("v")
fig.tight_layout()
fig.savefig(OUT / "lec09_fig2_quadform.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: constraint and level curve are tangent ----------------
fig, ax = plt.subplots(figsize=(5.6, 5.2))
t = np.linspace(-0.4, 1.6, 200)
ax.plot(t, 1 - t, color="tab:green", lw=2.2)
th = np.linspace(0, 2 * np.pi, 300)
for r in [0.45, 0.55, np.sqrt(0.5)]:
    ax.plot(r * np.cos(th), r * np.sin(th), color="0.75", lw=1.0)
ax.plot(np.sqrt(0.5) * np.cos(th), np.sqrt(0.5) * np.sin(th), color="tab:blue", lw=2.0)
P = np.array([0.5, 0.5])
ax.annotate("", xy=P + 0.55 * np.array([1, 1]) / np.sqrt(2), xytext=P,
            arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=2.4))
ax.annotate("", xy=P + 0.40 * np.array([1, 1]) / np.sqrt(2), xytext=P,
            arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=2.0))
ax.scatter([0.5], [0.5], color="k", s=22)
ax.text(0.62, 0.62, r"$P(1/2,1/2)$", fontsize=9)
ax.text(0.92, 0.75, r"$∇f$", color="tab:red", fontsize=10)
ax.text(0.86, 0.52, r"$∇g$", color="tab:green", fontsize=10)
ax.text(1.05, 0.05, "constraint x+y=1", color="tab:green", fontsize=9)
ax.text(0.0, 0.95, r"level curve $x^2+y^2=1/2$", color="tab:blue", fontsize=8)
ax.set_aspect("equal")
ax.set_xlim(-0.5, 1.7); ax.set_ylim(-0.5, 1.6)
ax.grid(alpha=0.2)
ax.axhline(0, color="0.85", lw=0.6); ax.axvline(0, color="0.85", lw=0.6)
ax.set_title(r"at the optimum: $∇f \parallel ∇g$ (tangency)", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec09_fig3_tangency.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: max of xyz on x+y+z=1 ----------------
fig, ax = plt.subplots(figsize=(6.0, 5.0))
x = np.linspace(1e-3, 0.999, 300)
y = np.linspace(1e-3, 0.999, 300)
X, Y = np.meshgrid(x, y)
Z = X * Y * (1 - X - Y)
Z = np.where(X + Y < 1, Z, np.nan)
cs = ax.contour(X, Y, Z, levels=[0.002, 0.01, 0.02, 0.03, 0.036],
                colors="tab:blue", linewidths=1.2)
ax.clabel(cs, inline=True, fontsize=7)
ax.plot([0, 1], [1, 0], color="tab:green", lw=2.0)
ax.plot([0, 1], [0, 0], color="0.4", lw=1.0)
ax.plot([0, 0], [0, 1], color="0.4", lw=1.0)
ax.scatter([1 / 3], [1 / 3], color="tab:red", s=40, zorder=3)
ax.text(0.36, 0.36, r"$(1/3,1/3)$, max $=1/27$", fontsize=9, color="tab:red")
ax.text(0.02, 0.02, "x", fontsize=10); ax.text(0.02, 0.9, "y", fontsize=10)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.set_title(r"max of $xyz$ on $x+y+z=1$ (z = 1 - x - y)", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec09_fig4_xyz.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec09_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
