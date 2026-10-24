# 规模纪律：常数级运算与两张图，目标 < 5 秒。
# 验证第 01 讲：复数四则运算、模与辐角、乘法的几何意义、棣莫弗公式与方根。
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

print("=== EXP1: algebraic form and arithmetic ===")
z1 = 3 + 4j
z2 = 1 - 2j
print(f"z1 = {z1}, |z1| = {abs(z1):.4f}")
print(f"z2 = {z2}, |z2| = {abs(z2):.4f}")
print(f"z1 + z2 = {z1 + z2}")
print(f"z1 * z2 = {z1 * z2}")
print(f"z1 / z2 = {z1 / z2}")
print("expect: z1*z2 = 11-2i; z1/z2 = -1+2i")

print()
print("=== EXP2: multiplication multiplies moduli and adds arguments ===")
r1, t1 = abs(z1), np.angle(z1)
r2, t2 = abs(z2), np.angle(z2)
prod = z1 * z2
print(f"|z1| * |z2| = {r1 * r2:.6f}, |z1*z2| = {abs(prod):.6f}")
print(f"arg z1 + arg z2 = {t1 + t2:.6f} rad, arg(z1*z2) = {np.angle(prod):.6f} rad")
diff = np.angle(np.exp(1j * (t1 + t2 - np.angle(prod))))
print(f"method difference after wrapping = {abs(diff):.3e} rad")
print("expect: both moduli agree, arguments agree up to 2*pi wrapping")

print()
print("=== EXP3: conjugate and division check ===")
print(f"z1 * conj(z1) = {z1 * np.conj(z1):.6f} (real), |z1|^2 = {abs(z1) ** 2:.6f}")
print(f"(z1 / z2) * z2 = {z1 / z2 * z2:.6f}")
print("expect: first is real and equals |z1|^2; second returns z1")

print()
print("=== EXP4: de Moivre formula ===")
n = 5
r, theta = 2.0, np.pi / 6
z = r * np.exp(1j * theta)
print(f"z = 2*exp(i*pi/6)")
print(f"z^5 = {z ** n:.6f}")
print(f"2^5 * exp(i*5*pi/6) = {(r ** n) * np.exp(1j * n * theta):.6f}")
print("expect: identical")

print()
print("=== EXP5: five 5th roots of 32*exp(i*pi/6) ===")
w = 32 * np.exp(1j * np.pi / 6)
root_radius = abs(w) ** (1 / 5)
roots = [root_radius * np.exp(1j * (np.angle(w) + 2 * np.pi * k) / 5) for k in range(5)]
for k, rk in enumerate(roots):
    print(f"k={k}: root={rk:.6f}, root^5={rk ** 5:.6f}, |root|={abs(rk):.6f}")
print("expect: every root^5 equals w; all roots lie on the circle of radius 2")

print()
print("=== EXP6: triangle inequality ===")
s = z1 + z2
print(f"|z1 + z2| = {abs(s):.6f}")
print(f"||z1| - |z2|| = {abs(abs(z1) - abs(z2)):.6f}")
print(f"|z1| + |z2| = {abs(z1) + abs(z2):.6f}")
print("expect: lower bound <= |z1+z2| <= upper bound")

print()
print("=== EXP7: principal argument range ===")
for zz in [1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j, -1 + 0j]:
    print(f"z={zz}: Arg={np.angle(zz):.6f} rad = {np.degrees(np.angle(zz)):.2f} deg")
print("expect: all values in (-pi, pi]; note Arg(-1) = pi, not -pi")

# ---------------------------------------------------------------------------
# FIG1: a complex number as a point and a vector
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.6, 5.0))
ax.axhline(0, color=GREY, lw=0.8)
ax.axvline(0, color=GREY, lw=0.8)

x, y = 3.0, 4.0
ax.annotate("", xy=(x, y), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2))
ax.plot([x, x], [0, y], ls="--", color=GREY, lw=0.9)
ax.plot([0, x], [0, 0], color=GREY, lw=0.9)
ax.plot([x], [y], "o", color=RED, ms=7)
ax.text(x + 0.12, y + 0.12, r"$z=3+4i$", color=RED, fontsize=12)
ax.text(x / 2, -0.45, "3", ha="center", fontsize=11)
ax.text(-0.38, y / 2, "4", va="center", fontsize=11)
ax.text(1.1, 2.6, r"$|z|=5$", color=BLUE, fontsize=11, rotation=53)
ax.text(1.05, 0.28, r"$\theta$", color=GREEN, fontsize=13)

arc = np.linspace(0, np.arctan2(y, x), 40)
ax.plot(0.9 * np.cos(arc), 0.9 * np.sin(arc), color=GREEN, lw=1.4)

ax.set_xlim(-0.8, 5.2)
ax.set_ylim(-0.8, 5.2)
ax.set_aspect("equal")
ax.set_xlabel("实轴 Re")
ax.set_ylabel("虚轴 Im")
ax.set_title("复数 $z=3+4i$：点、向量、模与辐角")
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec01_fig1_complex_plane.svg"))
fig.savefig(os.path.join(FIGDIR, "lec01_fig1_complex_plane.png"), dpi=160)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG2: multiplication = scale + rotate
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.6, 5.0))
ax.axhline(0, color=GREY, lw=0.8)
ax.axvline(0, color=GREY, lw=0.8)

z_a = 1.5 * np.exp(1j * np.pi / 6)
z_b = 2.0 * np.exp(1j * np.pi / 3)
z_ab = z_a * z_b

for zz, color, label in [(z_a, BLUE, r"$z_1=1.5e^{i\pi/6}$"),
                         (z_b, GREEN, r"$z_2=2e^{i\pi/3}$"),
                         (z_ab, RED, r"$z_1z_2=3e^{i\pi/2}$")]:
    ax.annotate("", xy=(zz.real, zz.imag), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2))
    ax.text(zz.real + 0.08, zz.imag + 0.08, label, color=color, fontsize=10)

th1, th2 = np.angle(z_a), np.angle(z_ab)
arc1 = np.linspace(0, th1, 30)
arc2 = np.linspace(th1, th2, 30)
ax.plot(0.55 * np.cos(arc1), 0.55 * np.sin(arc1), color=BLUE, lw=1.3)
ax.plot(0.75 * np.cos(arc2), 0.75 * np.sin(arc2), color=RED, lw=1.3)

ax.set_xlim(-0.8, 3.6)
ax.set_ylim(-0.8, 3.6)
ax.set_aspect("equal")
ax.set_xlabel("实轴 Re")
ax.set_ylabel("虚轴 Im")
ax.set_title("乘法：模相乘，辐角相加")
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec01_fig2_multiplication.svg"))
fig.savefig(os.path.join(FIGDIR, "lec01_fig2_multiplication.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
