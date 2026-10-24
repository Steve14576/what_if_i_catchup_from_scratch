# 规模纪律：数值积分与两张图，目标 < 5 秒。
# 验证第 07 讲：复合闭路定理、多洞分解、闭路变形、原函数存在性。
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


def circle(f, center, radius, clockwise=False):
    sign = -1 if clockwise else 1
    return integrate(f,
                     lambda t: center + radius * np.exp(1j * t),
                     lambda t: sign * 1j * radius * np.exp(1j * t),
                     0, 2 * np.pi)


print("=== EXP1: outer and inner boundaries give the same integral ===")
f = lambda z: 1 / z
outer = circle(f, 0, 2)
inner = circle(f, 0, 1)
print(f"outer |z|=2: {outer.real:+.6f}{outer.imag:+.6f}j")
print(f"inner |z|=1: {inner.real:+.6f}{inner.imag:+.6f}j")
print("expect: both 2*pi*i")

print()
print("=== EXP2: (2z+1)/(z(z-1)) around |z|=2 ===")
g = lambda z: (2 * z + 1) / (z * (z - 1))
val = circle(g, 0, 2)
print(f"integral = {val.real:+.6f}{val.imag:+.6f}j")
print("expect: 4*pi*i = 0+12.566371j")

print()
print("=== EXP3: outer boundary equals the sum of inner boundaries ===")
outer_g = circle(g, 0, 2)
inner0 = circle(g, 0.0, 0.4)
inner1 = circle(g, 1.0, 0.4)
print(f"outer        = {outer_g.real:+.6f}{outer_g.imag:+.6f}j")
print(f"inner z=0    = {inner0.real:+.6f}{inner0.imag:+.6f}j")
print(f"inner z=1    = {inner1.real:+.6f}{inner1.imag:+.6f}j")
print(f"sum of inner = {(inner0 + inner1).real:+.6f}{(inner0 + inner1).imag:+.6f}j")
print("expect: outer = sum of inner")

print()
print("=== EXP4: deformation from circle to square preserves the integral ===")
square = [2 + 2j, -2 + 2j, -2 - 2j, 2 - 2j, 2 + 2j]
total = 0
for k in range(len(square) - 1):
    z0, z1 = square[k], square[k + 1]
    total += integrate(lambda z: 1 / z,
                       lambda t, z0=z0, z1=z1: z0 + (z1 - z0) * t,
                       lambda t, z0=z0, z1=z1: (z1 - z0) + 0 * t,
                       0, 1)
print(f"square path = {total.real:+.6f}{total.imag:+.6f}j")
print(f"circle path = {outer.real:+.6f}{outer.imag:+.6f}j")
print("expect: both 2*pi*i")

print()
print("=== EXP5: 1/z has no primitive, 1/z^2 does ===")
v1 = circle(lambda z: 1 / z, 0, 1)
v2 = circle(lambda z: 1 / z ** 2, 0, 1)
print(f"closed integral of 1/z   = {v1.real:+.6f}{v1.imag:+.6f}j")
print(f"closed integral of 1/z^2 = {v2.real:+.3e}{v2.imag:+.3e}j")
print("expect: first nonzero, second zero")

# ---------------------------------------------------------------------------
# FIG1: compound contour directions
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.8))

# left: annulus
axes[0].add_patch(Wedge((0, 0), 1.6, 0, 360, width=0.7, facecolor="#e2e8f0", edgecolor="none"))
theta = np.linspace(0, 2 * np.pi, 500)
axes[0].plot(1.6 * np.cos(theta), 1.6 * np.sin(theta), color=BLUE, lw=2.0)
axes[0].plot(0.9 * np.cos(theta), 0.9 * np.sin(theta), color=RED, lw=2.0)
axes[0].annotate("", xy=(1.6 * np.cos(0.25), 1.6 * np.sin(0.25)),
                 xytext=(1.6 * np.cos(0.0), 1.6 * np.sin(0.0)),
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))
axes[0].annotate("", xy=(0.9 * np.cos(-0.25), 0.9 * np.sin(-0.25)),
                 xytext=(0.9 * np.cos(0.0), 0.9 * np.sin(0.0)),
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))
axes[0].text(0.55, 1.35, "外边界：逆时针", color=BLUE, fontsize=9)
axes[0].text(-0.55, -1.35, "内边界：顺时针", color=RED, fontsize=9)
axes[0].set_title("圆环区域：外边界与内边界方向相反")
axes[0].set_xlim(-2.0, 2.0)
axes[0].set_ylim(-2.0, 2.0)

# right: two holes
axes[1].add_patch(Circle((0, 0), 2.2, fill=False, color=BLUE, lw=2.0))
for cx in (-0.8, 0.8):
    axes[1].add_patch(Circle((cx, 0), 0.5, facecolor="white", edgecolor=RED, lw=1.8))
axes[1].annotate("", xy=(2.2 * np.cos(0.3), 2.2 * np.sin(0.3)),
                 xytext=(2.2 * np.cos(0.05), 2.2 * np.sin(0.05)),
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))
axes[1].text(-0.8, 0, "洞 1", ha="center", va="center", color=RED, fontsize=9)
axes[1].text(0.8, 0, "洞 2", ha="center", va="center", color=RED, fontsize=9)
axes[1].annotate("", xy=(-0.8 + 0.5 * np.cos(-0.4), 0.5 * np.sin(-0.4)),
                 xytext=(-0.3, 0),
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
axes[1].set_title("两个洞：外边界积分等于两个内边界积分之和")
axes[1].set_xlim(-2.5, 2.5)
axes[1].set_ylim(-2.5, 2.5)

for ax in axes:
    ax.set_aspect("equal")
    ax.axis("off")
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec07_fig1_compound_contour.svg"))
fig.savefig(os.path.join(FIGDIR, "lec07_fig1_compound_contour.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
