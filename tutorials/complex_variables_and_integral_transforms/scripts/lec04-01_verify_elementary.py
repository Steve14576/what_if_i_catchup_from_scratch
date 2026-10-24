# 规模纪律：常数级运算与两张图，目标 < 5 秒。
# 验证第 04 讲：复指数、复对数多值、复幂、三角函数无界性、分支切割。
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


print("=== EXP1: exp(z) is periodic with period 2*pi*i ===")
z = 0.7 + 0.4j
print(f"exp(z)        = {np.exp(z):.6f}")
print(f"exp(z+2*pi*i) = {np.exp(z + 2j*np.pi):.6f}")
print(f"exp(z-2*pi*i) = {np.exp(z - 2j*np.pi):.6f}")
print("expect: all three are equal")

print()
print("=== EXP2: |exp(z)| = exp(Re z) and Arg(exp(z)) = Im z mod 2*pi ===")
for (x, y) in [(0.0, 0.0), (1.0, np.pi/2), (-1.0, np.pi), (0.5, -np.pi/3)]:
    w = np.exp(complex(x, y))
    print(f"z={x:+.2f}{y:+.4f}j: |w|={abs(w):.6f}, exp(x)={np.exp(x):.6f}, "
          f"Arg(w)={np.angle(w):+.6f}, y={y:+.6f}")
print("expect: moduli match exp(x); arguments match y after wrapping into (-pi, pi]")

print()
print("=== EXP3: Ln(-1) has infinitely many values ===")
for k in range(-2, 3):
    w = np.log(abs(-1)) + 1j * (np.pi + 2 * np.pi * k)
    print(f"k={k:+d}: Ln(-1) = {w:.6f}")
print("expect: i*pi + 2*k*pi*i; principal value is i*pi")

print()
print("=== EXP4: i^i is real but multivalued ===")
for k in range(-2, 3):
    val = np.exp(-np.pi / 2 - 2 * np.pi * k)
    print(f"k={k:+d}: i^i = {val:.9f}")
print("expect: e^(-pi/2 - 2*k*pi); principal value e^(-pi/2) = 0.207879576")

print()
print("=== EXP5: principal ln(z) jumps across the negative real axis ===")
for eps in [1e-3, 1e-6]:
    z_up = -1 + 1j * eps
    z_down = -1 - 1j * eps
    print(f"eps={eps:.0e}: ln(-1+i*eps)={np.log(z_up):.6f}, ln(-1-i*eps)={np.log(z_down):.6f}")
print("expect: imaginary parts approach +pi and -pi; jump is 2*pi")

print()
print("=== EXP6: sin(z) is unbounded on the imaginary axis ===")
for y in [0.5, 1.0, 2.0, 3.0]:
    s = np.sin(1j * y)
    print(f"y={y:.1f}: sin(iy)={s:.6f}, |sin(iy)|={abs(s):.6f}, sinh(y)={np.sinh(y):.6f}")
print("expect: sin(iy) = i*sinh(y), modulus grows without bound")

# ---------------------------------------------------------------------------
# FIG1: three horizontal strips all map onto C minus the origin
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8))

strips = [(-np.pi, np.pi, BLUE, "$-\\pi<y<\\pi$"),
          (np.pi, 3 * np.pi, GREEN, "$\\pi<y<3\\pi$"),
          (-3 * np.pi, -np.pi, RED, "$-3\\pi<y<-\\pi$")]

for lo, hi, color, label in strips:
    axes[0].fill_between([-1, 1], lo, hi, color=color, alpha=0.12)
    axes[0].plot([-1, 1], [lo, lo], color=color, lw=1.2)
    axes[0].plot([-1, 1], [hi, hi], color=color, lw=1.2)
    axes[0].text(1.08, (lo + hi) / 2, label, color=color, va="center", fontsize=9)

axes[0].set_xlim(-1.3, 1.9)
axes[0].set_ylim(-3 * np.pi - 0.5, 3 * np.pi + 0.5)
axes[0].set_xlabel("实轴 Re")
axes[0].set_ylabel("虚轴 Im")
axes[0].set_title("$z$ 平面：以 $2\\pi$ 为周期重复的三个条带")

theta = np.linspace(0, 2 * np.pi, 400)
for radius in [0.4, 1.0, 2.0]:
    axes[1].plot(radius * np.cos(theta), radius * np.sin(theta), color=BLUE, lw=0.9, alpha=0.8)
for angle in np.arange(0, 2 * np.pi, np.pi / 6):
    axes[1].plot([0, 2.4 * np.cos(angle)], [0, 2.4 * np.sin(angle)], color=BLUE, lw=0.7, alpha=0.6)

axes[1].plot(0, 0, "o", color=RED, ms=6)
axes[1].set_xlim(-2.6, 2.6)
axes[1].set_ylim(-2.6, 2.6)
axes[1].set_aspect("equal")
axes[1].set_xlabel("实轴 Re")
axes[1].set_ylabel("虚轴 Im")
axes[1].set_title("$w=e^z$ 的像：一个条带就张满 $\\mathbb{C}\\setminus\\{0\\}$")

axes[0].grid(alpha=0.2)
axes[1].grid(alpha=0.2)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec04_fig1_exp_periodic.svg"))
fig.savefig(os.path.join(FIGDIR, "lec04_fig1_exp_periodic.png"), dpi=160)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG2: principal Arg jumps at the branch cut
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.6, 3.8))
theta = np.linspace(0, 4 * np.pi, 2000)
arg = np.angle(np.exp(1j * theta))

ax.plot(theta / np.pi, arg / np.pi, color=BLUE, lw=1.6)
for jump in [1, 3]:
    ax.axvline(jump, color=RED, ls="--", lw=1.1)
    ax.text(jump + 0.05, 0, "分支切割", color=RED, fontsize=9, va="center")

ax.set_xlabel("$\\theta/\\pi$（沿单位圆逆时针）")
ax.set_ylabel("$\\operatorname{Arg}(e^{i\\theta})/\\pi$")
ax.set_title("主值幅角沿单位圆绕行：在 $\\theta=\\pi$ 处从 $\\pi$ 跳到 $-\\pi$")
ax.set_xlim(0, 4)
ax.set_ylim(-1.25, 1.25)
ax.set_yticks([-1, -0.5, 0, 0.5, 1])
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec04_fig2_branch_cut.svg"))
fig.savefig(os.path.join(FIGDIR, "lec04_fig2_branch_cut.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
