# 规模纪律：数值积分与两张图，目标 < 5 秒。
# 验证第 08 讲：柯西积分公式、高阶导数公式、平均值定理。
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


def circle_integral(f, center, radius, n=400000):
    t = np.linspace(0, 2 * np.pi, n)
    z = center + radius * np.exp(1j * t)
    dz = 1j * radius * np.exp(1j * t)
    return np.trapezoid(f(z) * dz, t)


print("=== EXP1: Cauchy formula for exp(z) at z0=0 ===")
val = circle_integral(lambda z: np.exp(z) / z, 0, 1)
print(f"integral = {val.real:+.6f}{val.imag:+.6f}j")
print(f"2*pi*i*f(0) = 0+{2*np.pi:.6f}j")
print("expect: equal")

print()
print("=== EXP2: Cauchy formula at z0=1+i ===")
z0 = 1 + 1j
val = circle_integral(lambda z: (z ** 2 + 1) / (z - z0), z0, 1)
print(f"integral = {val.real:+.6f}{val.imag:+.6f}j")
print(f"2*pi*i*f(z0) = {2*np.pi*1j*((z0**2)+1)}")
print("expect: equal")

print()
print("=== EXP3: higher derivative formula, second derivative of exp ===")
val = circle_integral(lambda z: np.exp(z) / z ** 3, 0, 1)
print(f"integral = {val.real:+.6f}{val.imag:+.6f}j")
print(f"2*pi*i/2! * f''(0) = 0+{np.pi:.6f}j")
print("expect: equal (f''(0)=1)")

print()
print("=== EXP4: third derivative of sin at 0 ===")
val = circle_integral(lambda z: np.sin(z) / z ** 4, 0, 1)
print(f"integral = {val.real:+.6f}{val.imag:+.6f}j")
print(f"expected = 0+{-np.pi/3:.6f}j")
print("expect: sin'''(0) = -cos(0) = -1, so integral = 2*pi*i/6 * (-1)")

print()
print("=== EXP5: mean value theorem ===")
r = 1.0
theta = np.linspace(0, 2 * np.pi, 200001)
vals = np.exp(r * np.exp(1j * theta))
mean = np.trapezoid(vals, theta) / (2 * np.pi)
print(f"average on circle = {mean.real:+.9f}{mean.imag:+.9f}j")
print(f"f(0) = {np.exp(0):.9f}")
print("expect: average equals f(0)=1")

print()
print("=== EXP6: z0 outside the contour gives zero ===")
val = circle_integral(lambda z: np.exp(z) / (z - 2), 0, 1)
print(f"integral = {val.real:+.3e}{val.imag:+.3e}j")
print("expect: 0")

print()
print("=== EXP7: mean value theorem on a non-circular function ===")
z0 = 0.5 + 0.3j
r = 0.4
vals = (z0 + r * np.exp(1j * theta)) ** 3
mean = np.trapezoid(vals, theta) / (2 * np.pi)
print(f"average of (z0+r*exp(i*theta))^3 = {mean.real:+.9f}{mean.imag:+.9f}j")
print(f"z0^3 = {z0**3}")
print("expect: equal")

# ---------------------------------------------------------------------------
# FIG1: Cauchy formula geometry and mean value property
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8))

theta = np.linspace(0, 2 * np.pi, 500)
outer = 1.7 * np.cos(theta) + 1j * (0.85 * np.sin(theta))
axes[0].plot(outer.real, outer.imag, color=BLUE, lw=2.0)
axes[0].annotate("", xy=(outer[20].real, outer[20].imag),
                 xytext=(outer[5].real, outer[5].imag),
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.4))
z0 = 0.2 + 0.05j
rr = 0.32
axes[0].plot(z0.real + rr * np.cos(theta), z0.imag + rr * np.sin(theta),
             color=RED, lw=1.5, ls="--")
axes[0].plot(z0.real, z0.imag, "o", color=RED, ms=7)
axes[0].text(z0.real + 0.05, z0.imag - 0.18, "$z_0$", color=RED, fontsize=11)
axes[0].text(1.45, 0.6, "$\\Gamma$", color=BLUE, fontsize=13)
axes[0].text(z0.real + rr + 0.05, z0.imag + 0.12, "$\\gamma$", color=RED, fontsize=11)
axes[0].set_title("柯西公式：把大边界 $\\Gamma$ 换成小圆 $\\gamma$")
axes[0].set_xlim(-2.0, 2.0)
axes[0].set_ylim(-1.3, 1.3)

axes[1].plot(np.cos(theta), np.sin(theta), color=BLUE, lw=1.6)
sample = np.linspace(0, 2 * np.pi, 13)[:-1]
for a in sample:
    axes[1].plot(np.cos(a), np.sin(a), "o", color=GREEN, ms=5)
    axes[1].plot([0, np.cos(a)], [0, np.sin(a)], color=GREY, lw=0.5, alpha=0.5)
axes[1].plot(0, 0, "o", color=RED, ms=7)
axes[1].text(0.05, -0.18, "$z_0$", color=RED, fontsize=11)
axes[1].set_title("平均值定理：圆周上的平均值等于圆心处的值")
axes[1].set_xlim(-1.4, 1.4)
axes[1].set_ylim(-1.3, 1.4)

for ax in axes:
    ax.set_aspect("equal")
    ax.axis("off")
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec08_fig1_cauchy_formula.svg"))
fig.savefig(os.path.join(FIGDIR, "lec08_fig1_cauchy_formula.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
