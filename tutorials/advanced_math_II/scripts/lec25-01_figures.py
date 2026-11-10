# 规模纪律：3 张静态 SVG, 目标 < 5 秒。
# 第 25 讲图：莱布尼茨子列、交错 vs 绝对值、余项上界。
# 图内文字只用 ASCII 与 mathtext，不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: even/odd subsequences squeeze ----------------
N = 30
n = np.arange(1, N + 1)
a = 1.0 / n
partial = np.cumsum((-1) ** (n - 1) * a)
S = np.log(2.0)
even = partial[1::2]
odd = partial[0::2]

fig, ax = plt.subplots(figsize=(7.0, 4.4))
ax.plot(np.arange(2, N + 1, 2), even, "o-", color="tab:blue", ms=3, lw=1.2, label=r"$S_{2k}$ (increasing)")
ax.plot(np.arange(1, N + 1, 2), odd, "s-", color="tab:orange", ms=3, lw=1.2, label=r"$S_{2k-1}$ (decreasing)")
ax.axhline(S, color="tab:green", lw=1.2, ls="--", label=r"$\ln 2$")
ax.set_xlabel("n"); ax.set_ylabel("partial sum")
ax.set_title("Leibniz: even and odd subsequences squeeze to the same limit", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "lec25_fig1_leibniz.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: alternating vs absolute ----------------
N = 200
n = np.arange(1, N + 1)
alt = np.cumsum((-1) ** (n - 1) / n)
abs_harm = np.cumsum(1.0 / n)
abs_sq = np.cumsum(1.0 / n ** 2)

fig, ax = plt.subplots(figsize=(7.0, 4.4))
ax.plot(n, alt, color="tab:blue", lw=2.0, label=r"$\sum(-1)^{n-1}/n$ (converges)")
ax.plot(n, abs_harm, color="tab:red", lw=2.0, label=r"$\sum 1/n$ (diverges)")
ax.plot(n, abs_sq, color="tab:green", lw=1.6, label=r"$\sum 1/n^2$ (converges)")
ax.axhline(np.log(2), color="tab:blue", lw=0.8, ls="--")
ax.set_xlabel("n"); ax.set_ylabel("partial sum")
ax.set_title("alternating can converge while its absolute series diverges", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "lec25_fig3_abs_vs_cond.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: remainder bound ----------------
N = 40
n = np.arange(1, N + 1)
partial = np.cumsum((-1) ** (n - 1) / n)
S = np.log(2.0)
err = np.abs(S - partial)
bound = 1.0 / (n + 1)

fig, ax = plt.subplots(figsize=(7.0, 4.2))
ax.plot(n, err, "o-", color="tab:red", ms=3, lw=1.2, label=r"$|S-S_n|$")
ax.plot(n, bound, color="tab:blue", lw=1.6, label=r"$a_{n+1}=1/(n+1)$")
ax.set_xlabel("n"); ax.set_ylabel("error")
ax.set_title(r"remainder bound: $|S-S_n|\leq a_{n+1}$", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "lec25_fig2_remainder.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec25_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
