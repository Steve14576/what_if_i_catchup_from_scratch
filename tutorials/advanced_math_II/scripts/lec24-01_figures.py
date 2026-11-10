# 规模纪律：2 张静态 SVG, 目标 < 5 秒。
# 第 24 讲图：积分判别的面积夹逼、1/(n ln n) 的增长。
# 图内文字只用 ASCII 与 mathtext，不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: rectangles vs curve ----------------
fig, ax = plt.subplots(figsize=(6.8, 4.4))
x = np.linspace(0.6, 5.4, 400)
ax.plot(x, 1.0 / x, color="tab:blue", lw=2.2, label=r"$f(x)=1/x$")
for n in range(1, 5):
    ax.add_patch(plt.Rectangle((n, 0), 1, 1.0 / n, facecolor="tab:blue", alpha=0.18,
                               edgecolor="tab:blue", lw=0.8))
    ax.text(n + 0.5, 1.0 / n + 0.04, rf"$f({n})$", ha="center", fontsize=8)
ax.set_xlim(0.6, 5.4); ax.set_ylim(0, 1.15)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"integral test: each rectangle of height $f(n)$ covers $[n,n+1]$", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "lec24_fig1_integral.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: 1/(n ln n) grows like ln ln N ----------------
N = 10000
n = np.arange(2, N + 1, dtype=float)
s_nlnn = np.cumsum(1.0 / (n * np.log(n)))
s_sq = np.cumsum(1.0 / n ** 2)
nn = np.arange(2, N + 1)

fig, ax = plt.subplots(figsize=(7.0, 4.4))
ax.plot(nn, s_nlnn, color="tab:red", lw=2.0, label=r"$\sum 1/(n\ln n)$")
ax.plot(nn, np.log(np.log(nn)), color="tab:orange", lw=1.4, ls="--", label=r"$\ln\ln n$")
ax.plot(nn, s_sq, color="tab:green", lw=2.0, label=r"$\sum 1/n^2$")
ax.set_xlabel("n"); ax.set_ylabel("partial sum")
ax.set_title(r"$\sum 1/(n\ln n)$ grows like $\ln\ln n$; $\sum 1/n^2$ converges", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "lec24_fig2_nlnn.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec24_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
