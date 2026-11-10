# 规模纪律：3 张静态 SVG, 目标 < 5 秒。
# 第 27 讲图：e^x 逼近、sin 逼近、慢/快收敛。
# 图内文字只用 ASCII 与 mathtext，不放中文。
from pathlib import Path
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: Taylor polynomials of e^x ----------------
x = np.linspace(-2, 2, 400)
fig, ax = plt.subplots(figsize=(6.8, 4.4))
ax.plot(x, np.exp(x), color="black", lw=2.4, label=r"$e^x$")
for n, c in [(1, "tab:blue"), (2, "tab:green"), (3, "tab:orange"), (5, "tab:red")]:
    p = sum(x ** k / math.factorial(k) for k in range(n + 1))
    ax.plot(x, p, color=c, lw=1.6, label=fr"$n={n}$")
ax.set_ylim(-1, 8)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"Taylor polynomials of $e^x$ (Maclaurin)", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "lec27_fig1_exp.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: Taylor polynomials of sin x ----------------
x = np.linspace(-6, 6, 500)
fig, ax = plt.subplots(figsize=(6.8, 4.4))
ax.plot(x, np.sin(x), color="black", lw=2.4, label=r"$\sin x$")
for n, c in [(1, "tab:blue"), (3, "tab:green"), (5, "tab:orange"), (7, "tab:red")]:
    p = sum(((-1) ** k) * x ** (2 * k + 1) / math.factorial(2 * k + 1) for k in range(n // 2 + 1))
    ax.plot(x, p, color=c, lw=1.6, label=fr"$n={n}$")
ax.set_ylim(-3, 3)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"Taylor polynomials of $\sin x$: wider range as $n$ grows", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "lec27_fig2_sin.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: slow (ln2) vs fast (pi/4) ----------------
N = 5000
n = np.arange(0, N)
ln2_partial = np.cumsum(((-1.0) ** n) / (n + 1))          # ln(1+x) at x=1
pi4_partial = np.cumsum(((-1.0) ** n) / (2 * n + 1))      # arctan x at x=1

fig, ax = plt.subplots(figsize=(7.0, 4.2))
ax.plot(n, ln2_partial, color="tab:red", lw=1.6, label=r"$\ln 2$: $\sum(-1)^{n-1}/n$")
ax.plot(n, pi4_partial, color="tab:blue", lw=1.6, label=r"$\pi/4$: $\sum(-1)^n/(2n+1)$")
ax.axhline(np.log(2), color="tab:red", lw=0.8, ls="--")
ax.axhline(np.pi / 4, color="tab:blue", lw=0.8, ls="--")
ax.set_xlabel("number of terms"); ax.set_ylabel("partial sum")
ax.set_title(r"at the endpoint: $\ln 2$ converges slowly, $\pi/4$ much faster", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "lec27_fig3_slow_fast.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec27_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
