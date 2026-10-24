# 规模纪律：数值积分与两张图，目标 < 5 秒。
# 验证第 12 讲：三类孤立奇点、极限判据、零点极点关系、无穷远点。
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

# e^(1/z) intentionally blows up near the origin; silence the overflow noise.
np.seterr(over="ignore", invalid="ignore")


def laurent_coeff(f, n, radius=1.0, points=200000):
    """a_n = (1/2*pi*i) * closed integral of f(z)/z^(n+1) on |z|=radius."""
    t = np.linspace(0, 2 * np.pi, points)
    z = radius * np.exp(1j * t)
    dz = 1j * radius * np.exp(1j * t)
    return np.trapezoid(f(z) / z ** (n + 1) * dz, t) / (2j * np.pi)


print("=== EXP1: principal parts of three singularities at 0 ===")
print("sin(z)/z should have no negative powers:")
for n in [-1, -2, -3]:
    print(f"  a_{n} = {laurent_coeff(lambda z: np.sin(z) / z, n):+.6f}")
print("expect: all zero -> removable")

print("1/z^2 should have a_{-2}=1 and no lower powers:")
for n in [-1, -2, -3]:
    print(f"  a_{n} = {laurent_coeff(lambda z: 1 / z ** 2, n):+.6f}")
print("expect: a_{-2}=1, others 0 -> pole of order 2")

print("e^(1/z) should have a_{-n}=1/n!:")
for n in [-1, -2, -3, -4]:
    val = laurent_coeff(lambda z: np.exp(1 / z), n)
    print(f"  a_{n} = {val.real:+.6f}{val.imag:+.6f}j, 1/{abs(n)}! = {1/np.math.factorial(abs(n)) if hasattr(np, 'math') else 1/np.prod(np.arange(1, abs(n)+1)):.6f}")
print("expect: nonzero for every n -> essential singularity")

print()
print("=== EXP2: limiting behavior along directions ===")
for name, f in [("sin(z)/z", lambda z: np.sin(z) / z),
                ("1/z^2", lambda z: 1 / z ** 2),
                ("e^(1/z)", lambda z: np.exp(1 / z))]:
    print(f"{name}:")
    for deg in [0, 90, 180, 270]:
        r = 1e-6
        z = r * np.exp(1j * np.deg2rad(deg))
        val = f(z)
        print(f"  dir={deg:3d}: |f|={abs(val):.6e}, f={val:.6e}")
print("expect: sin(z)/z -> 1 everywhere; 1/z^2 -> infinity everywhere; e^(1/z) depends on direction")

print()
print("=== EXP3: zeros and poles ===")
print("z^2+1 has simple zeros at +i and -i")
for z0 in [1j, -1j]:
    print(f"  f(z0)={z0**2+1}, f'(z0)={2*z0} -> simple zero")
    print(f"  1/f near z0: residue-like coefficient |1/f'(z0)|={abs(1/(2*z0)):.6f} -> simple pole")

print()
print("=== EXP4: behavior at infinity via t=1/z ===")
print("f(z)=z: f(1/t)=1/t -> pole of order 1 at t=0 -> pole at infinity")
print("f(z)=1/z: f(1/t)=t -> removable at t=0 -> removable at infinity (simple zero)")
print("f(z)=1/z^2: f(1/t)=t^2 -> removable at t=0 -> removable at infinity (zero of order 2)")
print("f(z)=e^z: f(1/t)=e^(1/t) -> essential at t=0 -> essential at infinity")
for name, f in [("z", lambda t: 1 / t),
                ("1/z", lambda t: t),
                ("1/z^2", lambda t: t ** 2),
                ("e^z", lambda t: np.exp(1 / t))]:
    print(f"  {name}: f(1/t) at t=1e-6 -> {f(1e-6):.6e}")

# ---------------------------------------------------------------------------
# FIG1: pole vs essential: modulus along different directions
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8))

r = np.logspace(-2, 0, 400)
axes[0].plot(r, 1 / r ** 2, color=BLUE, lw=2.0, label="$|1/z^2|$")
for deg, color in [(0, BLUE), (90, GREEN), (180, RED)]:
    axes[0].plot(r, 1 / r ** 2, color=color, lw=1.0, ls="--", alpha=0.7)
axes[0].set_xscale("log")
axes[0].set_yscale("log")
axes[0].set_xlabel("$r=|z|$")
axes[0].set_ylabel("$|f|$")
axes[0].set_title("二阶极点：所有方向都以 $1/r^2$ 爆炸")
axes[0].grid(alpha=0.25)

angles = {0: (BLUE, "$\\theta=0$"), 45: (GREEN, "$\\theta=\\pi/4$"),
          90: (GREY, "$\\theta=\\pi/2$"), 180: (RED, "$\\theta=\\pi$")}
for deg, (color, label) in angles.items():
    theta = np.deg2rad(deg)
    vals = np.abs(np.exp(1 / (r * np.exp(1j * theta))))
    axes[1].plot(r, vals, color=color, lw=1.6, label=label)
axes[1].set_xscale("log")
axes[1].set_yscale("log")
axes[1].set_xlabel("$r=|z|$")
axes[1].set_ylabel("$|e^{1/z}|$")
axes[1].set_title("本性奇点：不同方向行为完全不同")
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.25)

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec12_fig1_singularities.svg"))
fig.savefig(os.path.join(FIGDIR, "lec12_fig1_singularities.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
