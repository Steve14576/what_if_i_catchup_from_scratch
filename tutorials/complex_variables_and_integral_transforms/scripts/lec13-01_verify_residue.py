# 规模纪律：数值积分与两张图，目标 < 5 秒。
# 验证第 13 讲：一阶/高阶极点留数、留数定理、无穷远留数与总和为零。
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

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


def residue_numeric(f, z0, radius=0.1, points=400000):
    t = np.linspace(0, 2 * np.pi, points)
    z = z0 + radius * np.exp(1j * t)
    dz = 1j * radius * np.exp(1j * t)
    return np.trapezoid(f(z) * dz, t) / (2j * np.pi)


def circle_integral(f, center, radius, points=400000):
    t = np.linspace(0, 2 * np.pi, points)
    z = center + radius * np.exp(1j * t)
    dz = 1j * radius * np.exp(1j * t)
    return np.trapezoid(f(z) * dz, t)


print("=== EXP1: simple pole ===")
print("Res[1/(z-1), 1] should be 1")
print(f"  numeric = {residue_numeric(lambda z: 1 / (z - 1), 1):.6f}")

print()
print("=== EXP2: higher-order poles ===")
print("Res[1/z^2, 0] should be 0")
print(f"  numeric = {residue_numeric(lambda z: 1 / z ** 2, 0):+.6f}")
print("Res[1/(z^2(z-1)), 0] should be -1")
print(f"  numeric = {residue_numeric(lambda z: 1 / (z ** 2 * (z - 1)), 0):+.6f}")

print()
print("=== EXP3: essential singularity ===")
print("Res[e^(1/z), 0] should be 1 (coefficient of 1/z)")
print(f"  numeric = {residue_numeric(lambda z: np.exp(1 / z), 0, radius=1.0):+.6f}")

print()
print("=== EXP4: residue theorem vs direct integration ===")
f = lambda z: (2 * z + 1) / (z * (z - 1))
direct = circle_integral(f, 0, 2)
res0 = -1
res1 = 3
print(f"direct integral       = {direct.real:+.6f}{direct.imag:+.6f}j")
print(f"2*pi*i*(res0 + res1)  = {2j*np.pi*(res0+res1)}")
print("expect: both 0 + 12.566371j")

print()
print("=== EXP5: residues of 1/(z^3-z) sum to zero ===")
g = lambda z: 1 / (z ** 3 - z)
r0 = residue_numeric(g, 0)
r1 = residue_numeric(g, 1)
rm1 = residue_numeric(g, -1)
print(f"Res at 0  = {r0:+.6f}")
print(f"Res at 1  = {r1:+.6f}")
print(f"Res at -1 = {rm1:+.6f}")
print(f"sum       = {r0 + r1 + rm1:+.3e}")
print("expect: 0; also Res at infinity = 0")

print()
print("=== EXP6: residue at infinity ===")
print("Res[1/z, inf] = -1, Res[z, inf] = 0, Res[1/z^2, inf] = 0")
for name, f in [("1/z", lambda z: 1 / z),
                ("z", lambda z: z),
                ("1/z^2", lambda z: 1 / z ** 2)]:
    # Res[f, inf] = -Res[f(1/t)/t^2, 0]
    def h(t, f=f):
        return f(1 / t) / t ** 2
    val = -residue_numeric(h, 0, radius=0.1)
    print(f"  Res[{name}, inf] = {val.real:+.6f}{val.imag:+.6f}j")
print("expect: -1, 0, 0")

# ---------------------------------------------------------------------------
# FIG1: residues inside a contour and the sum rule
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8))

theta = np.linspace(0, 2 * np.pi, 500)
axes[0].plot(2.2 * np.cos(theta), 2.2 * np.sin(theta), color=BLUE, lw=2.0)
axes[0].annotate("", xy=(2.2 * np.cos(0.25), 2.2 * np.sin(0.25)),
                 xytext=(2.2 * np.cos(0.05), 2.2 * np.sin(0.05)),
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.4))
for (cx, cy), r in [((-0.9, 0.5), 0.45), ((0.8, -0.6), 0.45), ((1.1, 0.9), 0.35)]:
    axes[0].plot(cx + r * np.cos(theta), cy + r * np.sin(theta),
                 color=RED, lw=1.2, ls="--")
    axes[0].plot(cx, cy, "o", color=RED, ms=7)
axes[0].text(-1.15, 0.55, "$z_1$", color=RED, fontsize=10)
axes[0].text(0.55, -0.68, "$z_2$", color=RED, fontsize=10)
axes[0].text(1.12, 0.95, "$z_3$", color=RED, fontsize=10)
axes[0].text(-1.3, 1.9, "$\\Gamma$", color=BLUE, fontsize=12)
axes[0].set_title("留数定理：$\\oint_\\Gamma f\\,dz=2\\pi i\\sum_k\\operatorname{Res}[f,z_k]$")
axes[0].set_xlim(-2.6, 2.6)
axes[0].set_ylim(-2.6, 2.6)

axes[1].bar([0, 1, 2], [-1.0, 0.5, 0.5], color=[RED, GREEN, BLUE], width=0.55)
axes[1].axhline(0, color=GREY, lw=1.0)
axes[1].set_xticks([0, 1, 2])
axes[1].set_xticklabels(["$z=0$", "$z=1$", "$z=-1$"])
axes[1].set_ylabel("留数")
axes[1].text(0.08, -0.78, "$-1$", color=RED, fontsize=10)
axes[1].text(1.08, 0.58, "$+0.5$", color=GREEN, fontsize=10)
axes[1].text(2.08, 0.58, "$+0.5$", color=BLUE, fontsize=10)
axes[1].text(0.55, -1.25, "总和 $=-1+0.5+0.5=0$", color="black", fontsize=10)
axes[1].set_title("留数之和为零：正负抵消")
axes[1].set_ylim(-1.6, 1.1)
axes[1].grid(alpha=0.2, axis="y")

axes[0].set_aspect("equal")
axes[0].axis("off")
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec13_fig1_residue.svg"))
fig.savefig(os.path.join(FIGDIR, "lec13_fig1_residue.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
