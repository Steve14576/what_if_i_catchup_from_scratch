# 规模纪律：部分和计算与两张图，目标 < 5 秒。
# 验证第 09 讲：调和级数发散、几何与 p 级数、收敛半径、边界行为。
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

BLUE = "#2b6cb0"
RED = "#c0392b"
GREEN = "#2f855a"
GREY = "#718096"

GAMMA = 0.5772156649015329


def harmonic_partial(n):
    return np.sum(1.0 / np.arange(1, n + 1))


print("=== EXP1: harmonic series grows like ln(n) ===")
for n in [10, 100, 1000, 10000, 1000000]:
    s = harmonic_partial(n)
    print(f"n={n:>7d}: S_n={s:.6f}, ln(n)+gamma={np.log(n)+GAMMA:.6f}, diff={s-(np.log(n)+GAMMA):+.6f}")
print("expect: S_n keeps growing; difference tends to a small constant")

print()
print("=== EXP2: geometric series ===")
for r in [0.5, 0.9, 1.0, 1.1]:
    n = 200
    s = np.sum(r ** np.arange(n + 1))
    print(f"r={r:.1f}: partial sum (n={n}) = {s:.6f}")
print("expect: r=0.5 -> 2, r=0.9 -> 10, r=1.0 -> n+1, r=1.1 -> grows")

print()
print("=== EXP3: p-series ===")
for p in [2.0, 1.5, 1.0, 0.5]:
    for n in [1000, 100000]:
        s = np.sum(np.arange(1, n + 1) ** (-p))
        print(f"p={p:.1f}, n={n:>6d}: S_n={s:.6f}")
print(f"expect: p=2 -> pi^2/6 = {np.pi**2/6:.6f}; p=1.5 converges slowly; p<=1 diverges")

print()
print("=== EXP4: radius of convergence, numerical probes ===")
print("sum z^n/n! at |z|=10:")

def exp_series(z, n_max):
    total = 0.0 + 0.0j
    term = 1.0 + 0.0j
    for k in range(n_max + 1):
        total += term
        term = term * z / (k + 1)
    return total

for n_max in [10, 20, 40]:
    print(f"  n_max={n_max}: exp_series(10)={exp_series(10, n_max):.6e}")
print("  expect: converges even at |z|=10 (R = infinity)")

print("sum n! z^n at |z|=0.1:")
def factorial_series(z, n_max):
    total = 0.0 + 0.0j
    term = 1.0 + 0.0j
    for k in range(n_max + 1):
        total += term
        term = term * z * (k + 1)
    return total

for n_max in [5, 15, 25, 35]:
    print(f"  n_max={n_max}: factorial_series(0.1)={factorial_series(0.1, n_max):.6e}")
print("  expect: diverges even at |z|=0.1 (R = 0)")

print()
print("=== EXP5: behavior on the circle |z|=1 ===")
for n_max in [1000, 10000, 100000]:
    s1 = np.sum(1.0 / np.arange(1, n_max + 1) ** 2)
    s2 = np.sum(1.0 / np.arange(1, n_max + 1))
    s3 = np.sum((-1.0) ** np.arange(1, n_max + 1) / np.arange(1, n_max + 1))
    print(f"n={n_max:>6d}: sum 1/n^2={s1:.6f}, sum 1/n={s2:.6f}, sum (-1)^n/n={s3:.6f}")
print("expect: 1/n^2 converges; 1/n diverges; alternating converges to -ln 2 = -0.693147")

print()
print("=== EXP6: complex series = sum of real and imaginary parts ===")
z = 0.6 + 0.8j
for n_max in [5, 10, 20, 40]:
    s = np.sum(z ** np.arange(n_max + 1))
    exact = 1 / (1 - z)
    print(f"n_max={n_max}: sum={s:.6f}, exact={exact:.6f}")
print("expect: |z|=1 exactly, so the series diverges; partial sums circle around without settling")

# ---------------------------------------------------------------------------
# FIG1: harmonic growth and convergence disk
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8))

n = np.arange(1, 20001)
partial = np.cumsum(1.0 / n)
axes[0].plot(n, partial, color=BLUE, lw=1.6, label="$S_n$")
axes[0].plot(n, np.log(n) + GAMMA, color=RED, ls="--", lw=1.2, label="$\\ln n+\\gamma$")
axes[0].set_xscale("log")
axes[0].set_xlabel("$n$（对数轴）")
axes[0].set_ylabel("部分和")
axes[0].set_title("调和级数：部分和随 $\\ln n$ 缓慢增长，没有上界")
axes[0].legend()
axes[0].grid(alpha=0.25)

theta = np.linspace(0, 2 * np.pi, 500)
axes[1].fill(2.0 * np.cos(theta), 2.0 * np.sin(theta), color=BLUE, alpha=0.12)
axes[1].plot(2.0 * np.cos(theta), 2.0 * np.sin(theta), color=BLUE, lw=2.0)
axes[1].plot(0, 0, "o", color=RED, ms=6)
axes[1].text(0.08, -0.28, "$z_0$", color=RED, fontsize=11)
axes[1].annotate("", xy=(2.0, 0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
axes[1].text(1.0, 0.12, "$R$", color=RED, fontsize=11)
axes[1].text(0.55, 1.45, "圆内：绝对收敛", color=BLUE, fontsize=9)
axes[1].text(2.25, 1.1, "圆外：发散", color=GREY, fontsize=9)
axes[1].text(-1.9, -1.75, "边界：逐个判断", color=GREEN, fontsize=9)
axes[1].set_xlim(-2.6, 3.2)
axes[1].set_ylim(-2.4, 2.4)

for ax in axes:
    if ax is axes[1]:
        ax.set_aspect("equal")
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec09_fig1_convergence.svg"))
fig.savefig(os.path.join(FIGDIR, "lec09_fig1_convergence.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
