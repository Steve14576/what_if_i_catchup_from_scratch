# 规模纪律：部分和与两张图，目标 < 5 秒。
# 验证第 10 讲：泰勒多项式逼近、收敛半径与最近奇点的关系、常用展开。
import os
import math

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


def sin_taylor(z, n_terms):
    total = 0.0 + 0.0j
    term = z * 1.0
    for k in range(n_terms):
        total += term
        term = -term * z * z / ((2 * k + 2) * (2 * k + 3))
    return total


print("=== EXP1: Taylor polynomials of sin z ===")
for z in [1.0, 2.0, 3.0, 5.0]:
    exact = np.sin(z)
    row = [abs(sin_taylor(z, n) - exact) for n in [1, 2, 3, 5, 8]]
    print(f"z={z:.1f}: errors N=1,2,3,5,8 -> " + ", ".join(f"{e:.3e}" for e in row))
print("expect: error shrinks as N grows; near z=5 it is slower")

print()
print("=== EXP2: geometric series and its remainder ===")
for z in [0.3, 0.8, 0.95]:
    N = 20
    partial = sum(z ** n for n in range(N + 1))
    exact = 1 / (1 - z)
    print(f"z={z}: partial={partial:.9f}, exact={exact:.9f}, error={partial-exact:+.3e}")
print("expect: error is z^(N+1)/(1-z); small z converges much faster")

print()
print("=== EXP3: 1/(1-z) expanded about z0=2 ===")
print("series: sum (-1)^(n+1) (z-2)^n, radius 1 (nearest singularity at z=1)")
for z in [1.5, 1.9, 2.1, 2.5]:
    N = 40
    partial = sum(((-1) ** (n + 1)) * (z - 2) ** n for n in range(N + 1))
    exact = 1 / (1 - z)
    print(f"z={z}: partial={partial:.9f}, exact={exact:.9f}, error={partial-exact:+.3e}")
print("expect: converges for |z-2|<1, i.e. 1<z<3")

print()
print("=== EXP4: radius equals distance to the nearest singularity ===")
print("1/(z^2+1): singularities at +i and -i")
print("center 0: distance 1")
print("center 1: distance sqrt(2) = 1.414214")
print("center 2: distance sqrt(5) = 2.236068")
for center in [0, 1, 2]:
    d = min(abs(complex(center) - 1j), abs(complex(center) + 1j))
    print(f"center={center}: nearest distance={d:.6f}")

print()
print("=== EXP5: coefficients of 1/(z^2+1) about 0 ===")
print("series: 1 - z^2 + z^4 - z^6 + ...")
for z in [0.4, 0.9, 0.99]:
    N = 30
    partial = sum(((-1) ** n) * z ** (2 * n) for n in range(N + 1))
    exact = 1 / (z * z + 1)
    print(f"z={z}: partial={partial:.9f}, exact={exact:.9f}, error={partial-exact:+.3e}")
print("expect: converges for |z|<1, fails beyond")

print()
print("=== EXP6: e^z series about 0 ===")
for z in [1.0, 2.0, 3.0]:
    N = 20
    partial = sum(z ** n / math.factorial(n) for n in range(N + 1))
    print(f"z={z}: partial={partial:.9f}, exp={math.exp(z):.9f}, error={partial-math.exp(z):+.3e}")
print("expect: converges everywhere; radius is infinite")

# ---------------------------------------------------------------------------
# FIG1: Taylor polynomial approximation and convergence disk
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8))

x = np.linspace(-2 * np.pi, 2 * np.pi, 800)
axes[0].plot(x, np.sin(x), color="black", lw=2.0, label=r"$\sin x$")
for n, color in [(1, BLUE), (2, GREEN), (3, RED), (5, "#805ad5")]:
    axes[0].plot(x, [sin_taylor(complex(v), n).real for v in x],
                 color=color, lw=1.2, ls="--", label=f"$N={2*n-1}$")
axes[0].set_ylim(-3, 3)
axes[0].set_xlabel("$x$")
axes[0].set_ylabel("$y$")
axes[0].set_title("$\\sin x$ 的泰勒多项式：阶数越高，逼近区间越宽")
axes[0].legend(fontsize=8, ncol=2)
axes[0].grid(alpha=0.25)

theta = np.linspace(0, 2 * np.pi, 500)
axes[1].plot(np.cos(theta), np.sin(theta), color=BLUE, lw=1.5, ls="--")
axes[1].plot(1 + np.sqrt(2) * np.cos(theta), np.sqrt(2) * np.sin(theta),
             color=GREEN, lw=1.5, ls=":")
axes[1].plot([0], [1], "x", color=RED, ms=9, mew=2)
axes[1].plot([0], [-1], "x", color=RED, ms=9, mew=2)
axes[1].plot([0], [0], "o", color=BLUE, ms=5)
axes[1].plot([1], [0], "o", color=GREEN, ms=5)
axes[1].annotate("", xy=(1, 0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))
axes[1].text(0.45, 0.1, "$R=1$", color=BLUE, fontsize=9)
axes[1].text(1.05, 0.62, "$R=\\sqrt{2}$", color=GREEN, fontsize=9)
axes[1].text(0.08, 1.02, "$i$", color=RED, fontsize=11)
axes[1].text(0.08, -1.12, "$-i$", color=RED, fontsize=11)
axes[1].text(0.02, -0.22, "$0$", color=BLUE, fontsize=9)
axes[1].text(1.02, -0.22, "$1$", color=GREEN, fontsize=9)
axes[1].set_title("$1/(z^2+1)$：收敛半径 = 到最近奇点的距离")
axes[1].set_xlim(-1.8, 2.8)
axes[1].set_ylim(-1.8, 1.8)

for ax in axes:
    if ax is axes[1]:
        ax.set_aspect("equal")
    ax.grid(alpha=0.2)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec10_fig1_taylor.svg"))
fig.savefig(os.path.join(FIGDIR, "lec10_fig1_taylor.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
