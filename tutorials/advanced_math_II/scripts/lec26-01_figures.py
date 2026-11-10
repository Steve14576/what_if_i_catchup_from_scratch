# 规模纪律：3 张静态 SVG, 目标 < 5 秒。
# 第 26 讲图：收敛区间、逐项求导/积分、端点行为。
# 图内文字只用 ASCII 与 mathtext，不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: interval of convergence ----------------
fig, ax = plt.subplots(figsize=(7.4, 2.8))
x0, R = 1.0, 2.0
ax.axhline(0, color="0.6", lw=1.0)
ax.plot([x0 - R, x0 + R], [0, 0], color="tab:blue", lw=5, solid_capstyle="butt", alpha=0.5)
ax.plot([x0], [0], "o", color="tab:blue", ms=6)
ax.plot([x0 - R, x0 + R], [0, 0], "o", mfc="white", mec="tab:red", mew=2, ms=8)
ax.text(x0, 0.18, r"$x_0$", ha="center", fontsize=10)
ax.text(x0 - R, -0.28, r"$x_0-R$", ha="center", fontsize=9)
ax.text(x0 + R, -0.28, r"$x_0+R$", ha="center", fontsize=9)
ax.text(x0 - R / 2, 0.18, "absolutely convergent", ha="center", fontsize=9, color="tab:blue")
ax.text(x0 + R + 0.55, 0.18, "divergent", fontsize=9, color="0.35")
ax.text(x0 + R + 0.55, -0.22, "endpoints: check separately", fontsize=8, color="tab:red")
ax.set_xlim(x0 - R - 1.0, x0 + R + 2.4)
ax.set_ylim(-0.5, 0.5)
ax.set_yticks([])
ax.set_xlabel("x")
ax.set_title("interval of convergence: center x0, radius R", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec26_fig1_interval.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: derivative and integral ----------------
x = np.linspace(-0.95, 0.95, 400)
fig, ax = plt.subplots(figsize=(6.8, 4.4))
ax.plot(x, 1.0 / (1 - x), color="tab:blue", lw=2.0, label=r"$1/(1-x)$")
ax.plot(x, 1.0 / (1 - x) ** 2, color="tab:red", lw=2.0, label=r"$1/(1-x)^2$ (termwise derivative)")
ax.plot(x, -np.log(1 - x), color="tab:green", lw=2.0, label=r"$-\ln(1-x)$ (termwise integral)")
ax.set_xlim(-0.95, 0.95); ax.set_ylim(0, 6)
ax.set_xlabel("x"); ax.set_ylabel("value")
ax.set_title("termwise derivative / integral of the geometric series", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "lec26_fig3_deriv_integ.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: endpoint behavior of sum x^n/n ----------------
Nmax = 200
n = np.arange(1, Nmax + 1)
at_pos = np.cumsum(1.0 / n)                 # x = 1 (diverges)
at_neg = np.cumsum((-1.0) ** n / n)         # x = -1 (converges)

fig, ax = plt.subplots(figsize=(7.0, 4.2))
ax.plot(n, at_pos, color="tab:red", lw=2.0, label=r"$x=1$: $\sum 1/n$ (diverges)")
ax.plot(n, at_neg, color="tab:blue", lw=2.0, label=r"$x=-1$: $\sum(-1)^n/n$ (converges)")
ax.axhline(-np.log(2), color="tab:blue", lw=0.8, ls="--")
ax.set_xlabel("n"); ax.set_ylabel("partial sum")
ax.set_title(r"endpoints of $\sum x^n/n$: one diverges, one converges", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "lec26_fig2_endpoints.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec26_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
