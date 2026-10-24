# 规模纪律：常数级运算与两张图，目标 < 5 秒。
# 验证第 02 讲：复变函数的映射、路径极限、连续性与 Arg 的间断。
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

print("=== EXP1: limit of conj(z)/z depends on the approach direction ===")
print("f(z) = conj(z)/z = exp(-2i*theta) along z = r*exp(i*theta)")
for deg in [0, 30, 45, 60, 90, 135, 180]:
    theta = np.deg2rad(deg)
    r = 1e-6
    z = r * np.exp(1j * theta)
    f = np.conj(z) / z
    print(f"theta={deg:3d} deg: f={f.real:+.6f}{f.imag:+.6f}j")
print("expect: values run around the unit circle; no common limit")

print()
print("=== EXP2: limit of z^2 at z0 = 1+i is path independent ===")
z0 = 1 + 1j
target = z0 ** 2
print(f"f(z0) = z0^2 = {target}")
for deg, r in [(0, 1e-3), (45, 1e-3), (90, 1e-3), (180, 1e-3), (270, 1e-3), (0, 1e-9)]:
    theta = np.deg2rad(deg)
    z = z0 + r * np.exp(1j * theta)
    f = z ** 2
    print(f"dir={deg:3d} deg, r={r:.0e}: f={f.real:.9f}{f.imag:+.9f}j")
print("expect: every value approaches 0+2j")

print()
print("=== EXP3: Arg(z) jumps across the negative real axis ===")
for eps in [1e-3, 1e-6]:
    z_upper = -1 + 1j * eps
    z_lower = -1 - 1j * eps
    print(f"eps={eps:.0e}: Arg(-1+i*eps)={np.angle(z_upper):+.6f}, Arg(-1-i*eps)={np.angle(z_lower):+.6f}")
print("expect: upper approaches +pi, lower approaches -pi; no common limit at -1")

print()
print("=== EXP4: continuity of z^2 and 1/z ===")
z1 = 2 + 1j
print(f"z^2 at {z1}: direct={z1**2}, via limit along 3 directions:")
for deg in [0, 120, 240]:
    zz = z1 + 1e-8 * np.exp(1j * np.deg2rad(deg))
    print(f"  dir {deg:3d}: {zz**2:.9f}")
print("expect: all match 3+4j (=2^2-1^2 + 2*2*1 j)")
print(f"1/z at z=1+1j: {1/(1+1j)}")
print("expect: 0.5-0.5j; continuous everywhere except z=0")

# ---------------------------------------------------------------------------
# FIG1: w = z^2 maps the first quadrant onto the upper half-plane
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8))

for c in np.arange(0.0, 2.01, 0.5):
    y = np.linspace(0, 2, 240)
    axes[0].plot(c + 0 * y, y, color=BLUE, lw=0.9, alpha=0.75)
    x = np.linspace(0, 2, 240)
    axes[0].plot(x, c + 0 * x, color=GREEN, lw=0.9, alpha=0.75)

for c in np.arange(0.0, 2.01, 0.5):
    y = np.linspace(0, 2, 240)
    w = (c + 1j * y) ** 2
    axes[1].plot(w.real, w.imag, color=BLUE, lw=0.9, alpha=0.75)
    x = np.linspace(0, 2, 240)
    w = (x + 1j * c) ** 2
    axes[1].plot(w.real, w.imag, color=GREEN, lw=0.9, alpha=0.75)

axes[0].set_title("$z$ 平面：第一象限网格")
axes[0].set_xlabel("实轴 Re")
axes[0].set_ylabel("虚轴 Im")
axes[0].set_xlim(-0.3, 2.2)
axes[0].set_ylim(-0.3, 2.2)

axes[1].set_title("$w=z^2$ 的像：整个上半平面")
axes[1].set_xlabel("实轴 Re")
axes[1].set_ylabel("虚轴 Im")
axes[1].set_xlim(-4.4, 4.4)
axes[1].set_ylim(-0.4, 4.6)

for ax in axes:
    ax.set_aspect("equal")
    ax.grid(alpha=0.22)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec02_fig1_mapping_square.svg"))
fig.savefig(os.path.join(FIGDIR, "lec02_fig1_mapping_square.png"), dpi=160)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG2: w = 1/z maps lines to circles
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8))

for c in [1.0]:
    y = np.linspace(-2, 2, 400)
    axes[0].plot(c + 0 * y, y, color=BLUE, lw=1.4, label="$x=1$")
    x = np.linspace(-2, 2, 400)
    axes[0].plot(x, c + 0 * x, color=GREEN, lw=1.4, label="$y=1$")

for c in [1.0]:
    y = np.linspace(-2, 2, 800)
    w = 1 / (c + 1j * y)
    axes[1].plot(w.real, w.imag, color=BLUE, lw=1.6, label="$x=1$ 的像")
    x = np.linspace(-2, 2, 800)
    w = 1 / (x + 1j * c)
    axes[1].plot(w.real, w.imag, color=GREEN, lw=1.6, label="$y=1$ 的像")

axes[0].set_title("$z$ 平面：一条竖线、一条横线")
axes[0].set_xlabel("实轴 Re")
axes[0].set_ylabel("虚轴 Im")
axes[0].set_xlim(-2.2, 2.2)
axes[0].set_ylim(-2.2, 2.2)
axes[0].legend(loc="upper right")

axes[1].set_title("$w=1/z$ 的像：两个过原点的圆")
axes[1].set_xlabel("实轴 Re")
axes[1].set_ylabel("虚轴 Im")
axes[1].set_xlim(-1.2, 1.2)
axes[1].set_ylim(-1.2, 1.2)
axes[1].legend(loc="upper right")

for ax in axes:
    ax.set_aspect("equal")
    ax.grid(alpha=0.22)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec02_fig2_mapping_inverse.svg"))
fig.savefig(os.path.join(FIGDIR, "lec02_fig2_mapping_inverse.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
