# 规模纪律：数值积分与两张图，目标 < 5 秒。
# 验证第 05 讲：复积分参数化、1/z 的闭路积分、路径相关性与积分估计。
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


def integrate(f, zfun, dzfun, a, b, n=200000):
    t = np.linspace(a, b, n)
    z = zfun(t)
    return np.trapezoid(f(z) * dzfun(t), t)


print("=== EXP1: closed integral of 1/z on the unit circle ===")
val = integrate(lambda z: 1 / z,
                lambda t: np.exp(1j * t),
                lambda t: 1j * np.exp(1j * t),
                0, 2 * np.pi)
print(f"integral = {val.real:+.6f}{val.imag:+.6f}j")
print(f"expected = 0+{2*np.pi:.6f}j")
print("expect: 2*pi*i")

print()
print("=== EXP2: the value does not depend on the radius ===")
for r in [0.5, 1.0, 2.0, 3.0]:
    val = integrate(lambda z: 1 / z,
                    lambda t, r=r: r * np.exp(1j * t),
                    lambda t, r=r: 1j * r * np.exp(1j * t),
                    0, 2 * np.pi)
    print(f"r={r:.1f}: integral = {val.real:+.6f}{val.imag:+.6f}j")
print("expect: all equal to 2*pi*i")

print()
print("=== EXP3: a circle not enclosing the origin gives zero ===")
val = integrate(lambda z: 1 / z,
                lambda t: 2 + np.exp(1j * t),
                lambda t: 1j * np.exp(1j * t),
                0, 2 * np.pi)
print(f"integral = {val.real:+.6e}{val.imag:+.6e}j")
print("expect: 0 (1/z is analytic inside |z-2|=1)")

print()
print("=== EXP4: integral of z dz is path independent ===")
z0, z1 = 0 + 0j, 1 + 1j

line = integrate(lambda z: z,
                 lambda t: z0 + (z1 - z0) * t,
                 lambda t: (z1 - z0) + 0 * t,
                 0, 1)

def broken(t):
    # first leg along the real axis, second leg vertical
    out = np.where(t <= 0.5,
                   (2 * t) + 0j,
                   1 + 1j * (2 * (t - 0.5)))
    return out

def broken_dz(t):
    return np.where(t <= 0.5, 2 + 0j, 2j + 0j)

broken_val = integrate(lambda z: z, broken, broken_dz, 0, 1)

exact = (z1 ** 2 - z0 ** 2) / 2
print(f"straight line = {line.real:+.6f}{line.imag:+.6f}j")
print(f"broken line  = {broken_val.real:+.6f}{broken_val.imag:+.6f}j")
print(f"exact (z1^2-z0^2)/2 = {exact.real:+.6f}{exact.imag:+.6f}j")
print("expect: all three agree")

print()
print("=== EXP5: integral of conj(z) dz is path dependent ===")
conj_line = integrate(lambda z: np.conj(z),
                      lambda t: (1 + 1j) * t,
                      lambda t: (1 + 1j) + 0 * t,
                      0, 1)

conj_broken = integrate(lambda z: np.conj(z), broken, broken_dz, 0, 1)
print(f"straight line = {conj_line.real:+.6f}{conj_line.imag:+.6f}j")
print(f"broken line  = {conj_broken.real:+.6f}{conj_broken.imag:+.6f}j")
print("expect: 1 vs 1+i; path dependent")

print()
print("=== EXP6: integral of z^2 dz along the straight line ===")
val = integrate(lambda z: z ** 2,
                lambda t: (1 + 1j) * t,
                lambda t: (1 + 1j) + 0 * t,
                0, 1)
exact6 = (1 + 1j) ** 3 / 3
print(f"numerical = {val.real:+.6f}{val.imag:+.6f}j")
print(f"(1+i)^3/3 = {exact6.real:+.6f}{exact6.imag:+.6f}j")
print("expect: agree")

print()
print("=== EXP7: ML estimate for 1/(z^2+1) on |z|=2 ===")
M = 1 / (2 ** 2 - 1)
L = 2 * np.pi * 2
print(f"M <= {M:.6f}, L = {L:.6f}, ML = {M*L:.6f}")
val = integrate(lambda z: 1 / (z ** 2 + 1),
                lambda t: 2 * np.exp(1j * t),
                lambda t: 2j * np.exp(1j * t),
                0, 2 * np.pi)
print(f"actual |integral| = {abs(val):.6e}")
print("expect: actual <= ML")

# ---------------------------------------------------------------------------
# FIG1: path division and oriented circle
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6))

t = np.linspace(0, 1, 400)
curve = t + 1j * (0.6 * t + 0.8 * t ** 2)
axes[0].plot(curve.real, curve.imag, color=BLUE, lw=2.0)

marks = np.linspace(0, 1, 7)
pts = marks + 1j * (0.6 * marks + 0.8 * marks ** 2)
axes[0].plot(pts.real, pts.imag, "o", color=RED, ms=5)
for k in range(len(pts) - 1):
    mid = (pts[k] + pts[k + 1]) / 2
    axes[0].annotate("", xy=(pts[k + 1].real, pts[k + 1].imag),
                     xytext=(pts[k].real, pts[k].imag),
                     arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
axes[0].text(pts[0].real - 0.06, pts[0].imag - 0.12, "$z_0$", fontsize=11)
axes[0].text(pts[-1].real - 0.06, pts[-1].imag + 0.08, "$z_n$", fontsize=11)
axes[0].set_title("把曲线 $\\Gamma$ 分成小段，$\\Delta z_k=z_k-z_{k-1}$")
axes[0].set_xlabel("实轴 Re")
axes[0].set_ylabel("虚轴 Im")
axes[0].set_xlim(-0.2, 1.2)
axes[0].set_ylim(-0.2, 1.6)

theta = np.linspace(0, 2 * np.pi, 400)
axes[1].plot(np.cos(theta), np.sin(theta), color=BLUE, lw=2.0)
axes[1].plot([0], [0], "o", color=RED, ms=6)
axes[1].annotate("", xy=(np.cos(0.35), np.sin(0.35)),
                 xytext=(np.cos(0.05), np.sin(0.05)),
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
axes[1].text(0.05, -0.2, "$z_0=0$", color=RED, fontsize=11)
axes[1].text(0.62, 0.55, "逆时针", color=GREEN, fontsize=11)
axes[1].set_title("闭路 $|z|=1$：方向取逆时针")
axes[1].set_xlabel("实轴 Re")
axes[1].set_ylabel("虚轴 Im")
axes[1].set_xlim(-1.4, 1.4)
axes[1].set_ylim(-1.4, 1.4)

for ax in axes:
    ax.set_aspect("equal")
    ax.grid(alpha=0.22)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec05_fig1_path_integral.svg"))
fig.savefig(os.path.join(FIGDIR, "lec05_fig1_path_integral.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
