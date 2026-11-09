# 规模纪律：两张静态 SVG, 目标 < 2 秒。
# 第 04 讲图 1-2：趋近原点的两条路径（直线族与抛物线） / 沿两条路径的函数值。
# 图内文字只用 ASCII 与 mathtext（不用 \lvert），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: paths to the origin ----------------
fig, ax = plt.subplots(figsize=(5.6, 4.6))
x = np.linspace(-1.0, 1.0, 400)
for k, c in [(0.0, "tab:gray"), (0.5, "tab:blue"), (1.0, "tab:green"), (2.0, "tab:purple")]:
    ax.plot(x, k * x, color=c, lw=1.3, label=rf"$y={k:g}x$")
ax.plot(x, x ** 2, color="tab:red", lw=2.4, label=r"$y=x^2$")
ax.scatter([0], [0], color="k", s=28, zorder=5)
ax.annotate("origin", xy=(0, 0), xytext=(0.12, 0.18), fontsize=9,
            arrowprops=dict(arrowstyle="->", lw=0.8))
ax.set_xlim(-1.0, 1.0)
ax.set_ylim(-1.0, 1.0)
ax.set_aspect("equal")
ax.grid(alpha=0.3)
ax.axhline(0, color="0.8", lw=0.6)
ax.axvline(0, color="0.8", lw=0.6)
ax.legend(fontsize=8, loc="upper left")
ax.set_title("paths approaching the origin: lines vs parabola", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec04_fig1_paths.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: function values along the paths ----------------
fig, ax = plt.subplots(figsize=(6.0, 4.2))
xs = np.linspace(0.02, 1.0, 400)
for k, c in [(0.5, "tab:blue"), (1.0, "tab:green"), (2.0, "tab:purple")]:
    ax.plot(xs, k * xs / (xs ** 2 + k ** 2), color=c, lw=1.4,
            label=rf"$y={k:g}x$: $kx/(x^2+k^2)$")
ax.plot(xs, 0.5 * np.ones_like(xs), color="tab:red", lw=2.4,
        label=r"$y=x^2$: constantly $1/2$")
ax.set_xlabel("x")
ax.set_ylabel("f(x, y(x))")
ax.set_ylim(-0.05, 0.6)
ax.grid(alpha=0.3)
ax.legend(fontsize=8)
ax.set_title(r"$f=x^2y/(x^4+y^2)$: lines -> 0, parabola -> 1/2", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec04_fig2_path_values.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec04_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figure written:", OUT)
