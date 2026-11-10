# 规模纪律：3 张静态 SVG, 目标 < 5 秒。
# 第 28 讲图：正交性、方波逼近、锯齿逼近。
# 图内文字只用 ASCII 与 mathtext，不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: orthogonality ----------------
x = np.linspace(-np.pi, np.pi, 800)
fig, ax = plt.subplots(figsize=(6.8, 4.0))
ax.plot(x, np.sin(x) * np.sin(2 * x), color="tab:blue", lw=1.8)
ax.fill_between(x, 0, np.sin(x) * np.sin(2 * x), where=(np.sin(x) * np.sin(2 * x) > 0),
                color="tab:blue", alpha=0.25)
ax.fill_between(x, 0, np.sin(x) * np.sin(2 * x), where=(np.sin(x) * np.sin(2 * x) < 0),
                color="tab:red", alpha=0.25)
ax.axhline(0, color="0.5", lw=0.8)
ax.set_xlabel("x"); ax.set_ylabel(r"$\sin x\cdot\sin 2x$")
ax.set_title(r"orthogonality: positive and negative areas cancel", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec28_fig1_orthogonal.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: square wave partial sums ----------------
x = np.linspace(-np.pi, np.pi, 1200)


def square(x):
    return np.where(np.sin(x) >= 0, 1.0, -1.0)


fig, ax = plt.subplots(figsize=(7.0, 4.2))
ax.plot(x, square(x), color="black", lw=2.0, label="square wave")
for n_terms, c in [(1, "tab:blue"), (3, "tab:green"), (5, "tab:orange"), (9, "tab:red")]:
    s = np.zeros_like(x)
    for k in range(n_terms):
        m = 2 * k + 1
        s += np.sin(m * x) / m
    ax.plot(x, 4 / np.pi * s, color=c, lw=1.2, label=f"N={n_terms}")
ax.set_xlabel("x"); ax.set_ylabel("partial sum")
ax.set_title("square wave: Fourier partial sums (Gibbs overshoot)", fontsize=10)
ax.legend(fontsize=8, loc="lower right")
fig.tight_layout()
fig.savefig(OUT / "lec28_fig2_square.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: sawtooth f(x)=x ----------------
fig, ax = plt.subplots(figsize=(7.0, 4.2))
ax.plot(x, x, color="black", lw=2.0, label=r"$f(x)=x$")
for n_terms, c in [(1, "tab:blue"), (3, "tab:green"), (5, "tab:orange"), (9, "tab:red")]:
    s = np.zeros_like(x)
    for n in range(1, n_terms + 1):
        s += ((-1) ** (n - 1)) / n * np.sin(n * x)
    ax.plot(x, 2 * s, color=c, lw=1.2, label=f"N={n_terms}")
ax.set_xlabel("x"); ax.set_ylabel("partial sum")
ax.set_title(r"sawtooth $f(x)=x$: Fourier partial sums", fontsize=10)
ax.legend(fontsize=8, loc="upper left")
fig.tight_layout()
fig.savefig(OUT / "lec28_fig3_sawtooth.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec28_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
