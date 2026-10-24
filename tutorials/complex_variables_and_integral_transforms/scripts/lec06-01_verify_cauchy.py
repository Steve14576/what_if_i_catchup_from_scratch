# 规模纪律：数值积分与两张图，目标 < 5 秒。
# 验证第 06 讲：柯西积分定理、条件缺失的反例、路径无关与牛顿-莱布尼茨公式。
import os

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


def integrate(f, zfun, dzfun, a, b, n=200000):
    t = np.linspace(a, b, n)
    return np.trapezoid(f(zfun(t)) * dzfun(t), t)


def integrate_polyline(f, vertices, n_per_seg=50000):
    total = 0
    for k in range(len(vertices) - 1):
        z0, z1 = vertices[k], vertices[k + 1]
        total += integrate(f,
                           lambda t, z0=z0, z1=z1: z0 + (z1 - z0) * t,
                           lambda t, z0=z0, z1=z1: (z1 - z0) + 0 * t,
                           0, 1, n_per_seg)
    return total


print("=== EXP1: analytic z^2 around the unit circle ===")
val = integrate(lambda z: z ** 2,
                lambda t: np.exp(1j * t),
                lambda t: 1j * np.exp(1j * t),
                0, 2 * np.pi)
print(f"integral = {val.real:+.3e}{val.imag:+.3e}j")
print("expect: 0")

print()
print("=== EXP2: analytic exp(z) around the unit circle ===")
val = integrate(np.exp,
                lambda t: np.exp(1j * t),
                lambda t: 1j * np.exp(1j * t),
                0, 2 * np.pi)
print(f"integral = {val.real:+.3e}{val.imag:+.3e}j")
print("expect: 0")

print()
print("=== EXP3: 1/z around a circle enclosing the origin ===")
val = integrate(lambda z: 1 / z,
                lambda t: np.exp(1j * t),
                lambda t: 1j * np.exp(1j * t),
                0, 2 * np.pi)
print(f"integral = {val.real:+.6f}{val.imag:+.6f}j")
print("expect: 2*pi*i; Cauchy theorem does not apply because 1/z is not analytic at 0")

print()
print("=== EXP4: 1/z around a circle not enclosing the origin ===")
val = integrate(lambda z: 1 / z,
                lambda t: 2 + np.exp(1j * t),
                lambda t: 1j * np.exp(1j * t),
                0, 2 * np.pi)
print(f"integral = {val.real:+.3e}{val.imag:+.3e}j")
print("expect: 0")

print()
print("=== EXP5: z^2 around a square and a triangle ===")
square = [1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j, 1 + 1j]
triangle = [1 + 0j, np.exp(1j * 2 * np.pi / 3), np.exp(1j * 4 * np.pi / 3), 1 + 0j]
print(f"square   = {integrate_polyline(lambda z: z ** 2, square):+.3e}")
print(f"triangle = {integrate_polyline(lambda z: z ** 2, triangle):+.3e}")
print("expect: both zero")

print()
print("=== EXP6: path independence of an analytic function ===")
z0, z1 = 0 + 0j, 1 + 1j
line = integrate(np.exp,
                 lambda t: z0 + (z1 - z0) * t,
                 lambda t: (z1 - z0) + 0 * t,
                 0, 1)
broken_vertices = [0 + 0j, 1 + 0j, 1 + 1j]
broken = integrate_polyline(np.exp, broken_vertices)
exact = np.exp(z1) - np.exp(z0)
print(f"straight = {line.real:+.6f}{line.imag:+.6f}j")
print(f"broken   = {broken.real:+.6f}{broken.imag:+.6f}j")
print(f"F(z1)-F(z0) = {exact.real:+.6f}{exact.imag:+.6f}j")
print("expect: all three agree")

# ---------------------------------------------------------------------------
# FIG1: simply connected vs multiply connected
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.8))

axes[0].add_patch(Circle((0, 0), 1.0, fill=False, color=BLUE, lw=2.0))
for r, alpha in [(0.75, 0.8), (0.5, 0.6), (0.25, 0.4)]:
    theta = np.linspace(0, 2 * np.pi, 300)
    axes[0].plot(r * np.cos(theta), r * np.sin(theta), ls="--", color=GREY, lw=0.9, alpha=alpha)
axes[0].annotate("", xy=(0.05, 0.05), xytext=(0.55, 0.35),
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.4))
axes[0].plot(0, 0, "o", color=RED, ms=5)
axes[0].text(0.02, -0.18, "收缩到一点", color=GREEN, fontsize=10)
axes[0].set_title("单连通：闭曲线可以在区域内缩成一点")
axes[0].set_xlim(-1.25, 1.25)
axes[0].set_ylim(-1.25, 1.25)

axes[1].add_patch(Wedge((0, 0), 1.0, 0, 360, width=0.45, facecolor="#e2e8f0", edgecolor=BLUE, lw=1.5))
theta = np.linspace(0, 2 * np.pi, 400)
axes[1].plot(0.72 * np.cos(theta), 0.72 * np.sin(theta), color=RED, lw=2.0)
axes[1].annotate("", xy=(0.72 * np.cos(0.35), 0.72 * np.sin(0.35)),
                 xytext=(0.72 * np.cos(0.05), 0.72 * np.sin(0.05)),
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
axes[1].text(0.38, 0.02, "绕洞", color=RED, fontsize=10)
axes[1].text(0, 0, "洞", color=BLUE, fontsize=11, ha="center", va="center")
axes[1].set_title("多连通：绕洞的闭曲线收缩不过去")
axes[1].set_xlim(-1.25, 1.25)
axes[1].set_ylim(-1.25, 1.25)

for ax in axes:
    ax.set_aspect("equal")
    ax.axis("off")
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec06_fig1_connectedness.svg"))
fig.savefig(os.path.join(FIGDIR, "lec06_fig1_connectedness.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
