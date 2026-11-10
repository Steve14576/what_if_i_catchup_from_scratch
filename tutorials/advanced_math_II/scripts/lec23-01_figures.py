# 规模纪律：3 张静态 SVG, 目标 < 5 秒。
# 第 23 讲图：部分和对比、调和分组、p 级数。
# 图内文字只用 ASCII 与 mathtext，不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: partial sums ----------------
n = np.arange(1, 61)
geo = np.cumsum(0.5 ** n)          # 1/2 + 1/4 + ...
sq = np.cumsum(1.0 / n ** 2)
harm = np.cumsum(1.0 / n)

fig, ax = plt.subplots(figsize=(7.0, 4.4))
ax.plot(n, geo, color="tab:blue", lw=2.0, label=r"$\sum 1/2^n \to 1$")
ax.plot(n, sq, color="tab:green", lw=2.0, label=r"$\sum 1/n^2 \to \pi^2/6 \approx 1.64$")
ax.plot(n, harm, color="tab:red", lw=2.0, label=r"$\sum 1/n$ (diverges)")
ax.axhline(1.0, color="tab:blue", lw=0.8, ls="--")
ax.axhline(np.pi ** 2 / 6, color="tab:green", lw=0.8, ls="--")
ax.set_xlabel("n"); ax.set_ylabel("partial sum")
ax.set_title("partial sums: convergent vs divergent", fontsize=10)
ax.legend(fontsize=8, loc="upper left")
fig.tight_layout()
fig.savefig(OUT / "lec23_fig2_partial_sums.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: harmonic grouping ----------------
fig, ax = plt.subplots(figsize=(7.0, 4.2))
# groups: {1}, {1/2}, {1/3,1/4}, {1/5..1/8}, ...
groups = [[1], [2], [3, 4], [5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15, 16]]
xs = []
heights = []
labels = []
pos = 0.0
for gi, g in enumerate(groups):
    for k in g:
        xs.append(pos + 0.5)
        heights.append(1.0 / k)
        pos += 1.0
    labels.append((gi, pos))
ax.bar(xs, heights, width=0.85, color="tab:red", alpha=0.75)
# horizontal half-line per group
for gi, end in labels:
    pass
for i, g in enumerate(groups):
    start = sum(len(gg) for gg in groups[:i])
    end = start + len(g)
    ax.plot([start + 0.1, end - 0.1], [0.5, 0.5], color="tab:blue", lw=1.2)
ax.axhline(0.5, color="tab:blue", lw=0.8, ls="--")
ax.set_xlabel("term index"); ax.set_ylabel("1/n")
ax.set_title(r"harmonic grouping: every block sums to at least 1/2", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec23_fig1_harmonic.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: p-series ----------------
n = np.arange(1, 201)
fig, ax = plt.subplots(figsize=(7.0, 4.4))
for p, c in [(0.5, "tab:red"), (1.0, "tab:orange"), (1.5, "tab:blue"), (2.0, "tab:green")]:
    ax.plot(n, np.cumsum(1.0 / n ** p), lw=1.8, color=c, label=f"p={p}")
ax.set_xlabel("n"); ax.set_ylabel("partial sum")
ax.set_title(r"$p$-series: converges for $p>1$, diverges for $p\leq 1$", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "lec23_fig3_p_series.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec23_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
