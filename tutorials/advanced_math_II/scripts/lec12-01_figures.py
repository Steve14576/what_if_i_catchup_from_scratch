# 规模纪律：4 张静态 SVG, 目标 < 4 秒。
# 第 12 讲图：X 型区域、Y 型区域、换序、对称性。
# 图内文字只用 ASCII 与 mathtext，不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: X-type region with vertical strips ----------------
fig, ax = plt.subplots(figsize=(5.6, 5.0))
x = np.linspace(0, 1, 300)
ax.plot(x, x ** 2, color="tab:blue", lw=2.0, label=r"$y=x^2$")
ax.plot(x, x, color="tab:green", lw=2.0, label=r"$y=x$")
ax.fill_between(x, x ** 2, x, color="tab:blue", alpha=0.15)
for x0 in [0.2, 0.4, 0.6, 0.8]:
    ax.plot([x0, x0], [x0 ** 2, x0], color="tab:red", lw=1.4)
ax.annotate("", xy=(0.7, 0.7 ** 2), xytext=(0.7, 0.7),
            arrowprops=dict(arrowstyle="<->", color="tab:red", lw=1.2))
ax.text(0.72, 0.55, r"$x^2 ≤ y ≤ x$", color="tab:red", fontsize=9)
ax.text(0.55, 0.9, r"$0 ≤ x ≤ 1$", fontsize=9)
ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.05, 1.05)
ax.set_aspect("equal")
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.legend(fontsize=8, loc="upper left")
ax.set_title("X-type region: vertical strips, inner integral in y", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec12_fig1_xregion.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: same region, Y-type strips ----------------
fig, ax = plt.subplots(figsize=(5.6, 5.0))
ax.plot(x, x ** 2, color="tab:blue", lw=2.0)
ax.plot(x, x, color="tab:green", lw=2.0)
ax.fill_between(x, x ** 2, x, color="tab:blue", alpha=0.15)
for y0 in [0.2, 0.4, 0.6, 0.8]:
    ax.plot([y0, np.sqrt(y0)], [y0, y0], color="tab:orange", lw=1.4)
ax.annotate("", xy=(0.4, 0.4), xytext=(np.sqrt(0.4), 0.4),
            arrowprops=dict(arrowstyle="<->", color="tab:orange", lw=1.2))
ax.text(0.45, 0.42, r"$y ≤ x ≤ \sqrt{y}$", color="tab:orange", fontsize=9)
ax.text(0.02, 0.92, r"$0 ≤ y ≤ 1$", fontsize=9)
ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.05, 1.05)
ax.set_aspect("equal")
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title("same region, Y-type: horizontal strips, inner integral in x", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec12_fig2_yregion.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: reordering on the triangle ----------------
fig, ax = plt.subplots(figsize=(5.4, 4.8))
t = np.linspace(0, 1, 200)
ax.plot(t, t, color="tab:blue", lw=2.0)
ax.plot([0, 1], [1, 1], color="0.4", lw=1.0)
ax.plot([0, 0], [0, 1], color="0.4", lw=1.0)
ax.fill_between(t, t, 1, color="tab:blue", alpha=0.12)
for x0 in [0.25, 0.5, 0.75]:
    ax.plot([x0, x0], [x0, 1], color="tab:red", lw=1.3)
for y0 in [0.4, 0.7]:
    ax.plot([0, y0], [y0, y0], color="tab:green", lw=1.3, ls="--")
ax.text(0.42, 0.78, "vertical strips:\n" + r"$0 ≤ x ≤ 1,\ x ≤ y ≤ 1$", color="tab:red", fontsize=8)
ax.text(0.06, 0.28, "horizontal strips:\n" + r"$0 ≤ y ≤ 1,\ 0 ≤ x ≤ y$", color="tab:green", fontsize=8)
ax.set_xlim(-0.04, 1.04); ax.set_ylim(-0.04, 1.04)
ax.set_aspect("equal")
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title("reordering: same triangle, two ways of slicing", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec12_fig3_reorder.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: symmetry: x^3 y changes sign across the y-axis ----------------
fig, ax = plt.subplots(figsize=(5.4, 5.0))
u = np.linspace(-1, 1, 400)
X, Y = np.meshgrid(u, u)
Z = X ** 3 * Y
mask = X ** 2 + Y ** 2 <= 1
Z = np.where(mask, np.sign(Z), np.nan)
ax.contourf(X, Y, Z, levels=[-1.5, 0, 1.5], colors=["tab:blue", "tab:red"], alpha=0.45)
th = np.linspace(0, 2 * np.pi, 300)
ax.plot(np.cos(th), np.sin(th), color="k", lw=1.5)
ax.text(-0.9, 0.75, "sign of " + r"$x^3y$", fontsize=9)
ax.text(-0.35, 0.05, "0", fontsize=9)
ax.set_aspect("equal")
ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"$x^3y$ is odd in $x$: opposite signs cancel", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "lec12_fig4_symmetry.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec12_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
