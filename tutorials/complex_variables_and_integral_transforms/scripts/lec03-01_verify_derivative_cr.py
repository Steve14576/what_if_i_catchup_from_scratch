# 规模纪律：常数级运算与两张图，目标 < 5 秒。
# 验证第 03 讲：复可导的差商、柯西-黎曼条件、可导点判定、由实部求虚部。
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


def diff_quotient(f, z0, dz):
    return (f(z0 + dz) - f(z0)) / dz


print("=== EXP1: difference quotient of z^2 is direction independent ===")
z0 = 1 + 1j
for deg in range(0, 360, 45):
    dz = 1e-6 * np.exp(1j * np.deg2rad(deg))
    q = diff_quotient(lambda z: z ** 2, z0, dz)
    print(f"dir={deg:3d} deg: q={q.real:+.9f}{q.imag:+.9f}j")
print(f"expect: all values approach 2*z0 = {2*z0}")
print("note: the residual is O(|dz|)")

print()
print("=== EXP2: difference quotient of conj(z) depends on direction ===")
for deg in range(0, 360, 45):
    dz = 1e-6 * np.exp(1j * np.deg2rad(deg))
    q = diff_quotient(np.conj, z0, dz)
    print(f"dir={deg:3d} deg: q={q.real:+.6f}{q.imag:+.6f}j, |q|={abs(q):.6f}")
print("expect: q = exp(-2i*theta), running around the unit circle")

print()
print("=== EXP3: Cauchy-Riemann check for z^2 ===")
for (x, y) in [(1.0, 2.0), (-1.5, 0.5), (0.0, 0.0), (2.0, -1.0)]:
    ux, uy = 2 * x, -2 * y
    vx, vy = 2 * y, 2 * x
    print(f"z={x:+.1f}{y:+.1f}j: ux={ux:+.4f}, vy={vy:+.4f}, uy={uy:+.4f}, -vx={-vx:+.4f}")
print("expect: ux = vy and uy = -vx at every point")

print()
print("=== EXP4: |z|^2 is differentiable only at the origin ===")
for zc, name in [(0 + 0j, "z0=0"), (1 + 0j, "z0=1")]:
    print(f"{name}:")
    for deg in [0, 45, 90, 180]:
        dz = 1e-6 * np.exp(1j * np.deg2rad(deg))
        q = diff_quotient(lambda z: z * np.conj(z), zc, dz)
        print(f"  dir={deg:3d}: q={q.real:+.6f}{q.imag:+.6f}j")
print("expect: at z0=0 all values near 0; at z0=1 values differ by direction")

print()
print("=== EXP5: recover v from u = x^2 - y^2 ===")
print("C-R gives v_y = u_x = 2x, v_x = -u_y = 2y, so v = 2xy + C")
for (x, y) in [(1.0, 3.0), (-2.0, 1.0)]:
    u = x ** 2 - y ** 2
    v = 2 * x * y
    ux, uy = 2 * x, -2 * y
    vx, vy = 2 * y, 2 * x
    print(f"z={x:+.1f}{y:+.1f}j: u={u:+.3f}, v={v:+.3f}, ux={ux:+.3f}, vy={vy:+.3f}, uy={uy:+.3f}, -vx={-vx:+.3f}")
print("expect: f(z)=z^2+C; C-R holds at every point")

# ---------------------------------------------------------------------------
# FIG1: the difference quotient either wanders or stays put
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6))

angles = np.linspace(0, 2 * np.pi, 73)
qs_conj = [diff_quotient(np.conj, z0, 1e-4 * np.exp(1j * a)) for a in angles]
qs_square = [diff_quotient(lambda z: z ** 2, z0, 1e-2 * np.exp(1j * a)) for a in angles]

axes[0].plot([q.real for q in qs_conj], [q.imag for q in qs_conj], "o", ms=3, color=BLUE)
axes[0].set_title("$f(z)=\\bar z$：差商绕单位圆跑")
axes[0].set_xlim(-1.25, 1.25)
axes[0].set_ylim(-1.25, 1.25)

axes[1].plot([q.real for q in qs_square], [q.imag for q in qs_square], "o", ms=3, color=GREEN)
axes[1].plot([2.0], [2.0], "*", ms=12, color=RED)
axes[1].annotate("$2z_0=2+2i$", xy=(2.0, 2.0), xytext=(2.006, 2.006),
                 fontsize=10, color=RED)
axes[1].set_title("$f(z)=z^2$：差商挤在 $2z_0$ 附近")
axes[1].set_xlim(1.985, 2.015)
axes[1].set_ylim(1.985, 2.015)

for ax in axes:
    ax.set_aspect("equal")
    ax.grid(alpha=0.25)
    ax.set_xlabel("实部 Re")
    ax.set_ylabel("虚部 Im")
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec03_fig1_difference_quotient.svg"))
fig.savefig(os.path.join(FIGDIR, "lec03_fig1_difference_quotient.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
