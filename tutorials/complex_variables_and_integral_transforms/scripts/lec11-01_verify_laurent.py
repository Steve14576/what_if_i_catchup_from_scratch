# 规模纪律：部分和与两张图，目标 < 5 秒。
# 验证第 11 讲：洛朗展开的两个圆环、负幂项、e^{1/z}、sin z/z。
import os
import math

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge

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


print("=== EXP1: 1/(z(z-1)) in the annulus 0<|z|<1 ===")
print("series: -1/z - 1 - z - z^2 - ...")
for z in [0.3, 0.5, 0.8]:
    N = 60
    partial = -sum(z ** n for n in range(-1, N + 1))
    exact = 1 / (z * (z - 1))
    print(f"z={z}: partial={partial:.9f}, exact={exact:.9f}, error={partial-exact:+.3e}")
print("expect: converges for |z|<1")

print()
print("=== EXP2: 1/(z(z-1)) in the annulus 1<|z|<inf ===")
print("series: 1/z^2 + 1/z^3 + 1/z^4 + ...")
for z in [1.5, 2.0, 3.0]:
    N = 80
    partial = sum(z ** (-n) for n in range(2, N + 1))
    exact = 1 / (z * (z - 1))
    print(f"z={z}: partial={partial:.9f}, exact={exact:.9f}, error={partial-exact:+.3e}")
print("expect: converges for |z|>1")

print()
print("=== EXP3: e^(1/z) has infinitely many negative powers ===")
print("series: sum_{n=0}^{inf} 1/(n! z^n)")
for z in [1.0, 2.0, -3.0]:
    N = 30
    partial = sum(1 / (math.factorial(n) * z ** n) for n in range(N + 1))
    exact = math.exp(1 / z)
    print(f"z={z}: partial={partial:.9f}, exact={exact:.9f}, error={partial-exact:+.3e}")
print("expect: converges for all z != 0")

print()
print("=== EXP4: sin(z)/z has no negative powers ===")
print("series: 1 - z^2/3! + z^4/5! - ...")
for z in [0.5, 1.0, 2.0]:
    N = 25
    series = []
    for n in range(N):
        series.append(((-1) ** n) * z ** (2 * n) / math.factorial(2 * n + 1))
    partial = sum(series)
    exact = math.sin(z) / z
    print(f"z={z}: partial={partial:.9f}, exact={exact:.9f}, error={partial-exact:+.3e}")
print("expect: converges for all z; the singularity at 0 is removable")

print()
print("=== EXP5: 1/(z^2(z-1)) in 0<|z|<1 ===")
print("series: -1/z^2 - 1/z - 1 - z - z^2 - ...")
for z in [0.3, 0.5]:
    N = 50
    partial = -sum(z ** n for n in range(-2, N + 1))
    exact = 1 / (z ** 2 * (z - 1))
    print(f"z={z}: partial={partial:.9f}, exact={exact:.9f}, error={partial-exact:+.3e}")
print("expect: converges for 0<|z|<1")

print()
print("=== EXP6: 1/(z^2+1) in |z|>1 ===")
print("series: 1/z^2 - 1/z^4 + 1/z^6 - ...")
for z in [1.5, 2.0, 4.0]:
    N = 60
    partial = sum(((-1) ** n) * z ** (-2 * n - 2) for n in range(N + 1))
    exact = 1 / (z * z + 1)
    print(f"z={z}: partial={partial:.9f}, exact={exact:.9f}, error={partial-exact:+.3e}")
print("expect: converges for |z|>1")

# ---------------------------------------------------------------------------
# FIG1: the two annuli determined by the singularities 0 and 1
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8))

theta = np.linspace(0, 2 * np.pi, 500)
axes[0].add_patch(Circle((0, 0), 1.0, facecolor="#dbeafe", edgecolor=BLUE, lw=2.0))
axes[0].add_patch(Circle((0, 0), 1.0, facecolor="#fef3c7", edgecolor=BLUE, lw=0))
axes[0].add_patch(Circle((0, 0), 1.0, facecolor="none", edgecolor=BLUE, lw=2.0))
axes[0].plot([0], [0], "o", color=RED, ms=8)
axes[0].plot([1], [0], "o", color=RED, ms=8)
axes[0].text(0.05, -0.22, "$0$", color=RED, fontsize=11)
axes[0].text(1.05, -0.22, "$1$", color=RED, fontsize=11)
axes[0].text(-0.55, 0.45, "$0<|z|<1$", color="#92400e", fontsize=10)
axes[0].text(1.3, 0.9, "$1<|z|<\\infty$", color=BLUE, fontsize=10)
axes[0].annotate("", xy=(1.0, 0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
axes[0].set_title("奇点 $0,1$ 把平面分成两个圆环")
axes[0].set_xlim(-1.6, 3.0)
axes[0].set_ylim(-1.6, 1.8)

axes[1].add_patch(Wedge((0, 0), 1.5, 0, 360, width=0.8, facecolor="#dbeafe", edgecolor=BLUE, lw=1.5))
axes[1].plot(0, 0, "o", color=RED, ms=6)
axes[1].annotate("", xy=(1.5, 0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))
axes[1].annotate("", xy=(-0.7, 0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))
axes[1].text(1.05, 0.12, "$R$", color=BLUE, fontsize=11)
axes[1].text(-0.62, 0.12, "$r$", color=GREY, fontsize=11)
axes[1].text(0.25, 1.05, "$r<|z-z_0|<R$", color=BLUE, fontsize=10)
axes[1].text(0.05, -0.25, "$z_0$", color=RED, fontsize=11)
axes[1].set_title("一般圆环：洛朗级数的展开域")
axes[1].set_xlim(-1.8, 1.8)
axes[1].set_ylim(-1.8, 1.8)

for ax in axes:
    ax.set_aspect("equal")
    ax.axis("off")
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec11_fig1_annulus.svg"))
fig.savefig(os.path.join(FIGDIR, "lec11_fig1_annulus.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
