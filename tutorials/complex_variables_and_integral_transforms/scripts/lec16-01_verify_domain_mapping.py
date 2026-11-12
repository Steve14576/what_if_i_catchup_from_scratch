# 规模纪律：若干次采样与两张图，目标 < 8 秒。
# 验证第 16 讲：上半平面到单位圆的标准映射、逆映射、角形域开角、带形域开带、
# 上半单位圆域的两步合成、儒可夫斯基映射把圆映成椭圆。
# 运行：uv run --with numpy --with matplotlib python <本文件>
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
PURPLE = "#6b46c1"


def circle_from_three(a, b, c):
    ax, ay = a.real, a.imag
    bx, by = b.real, b.imag
    cx, cy = c.real, c.imag
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    return complex(ux, uy), abs(a - complex(ux, uy))


print("=== EXP1: upper half-plane -> unit disk, w=(z-i)/(z+i) ===")
W = lambda z: (z - 1j) / (z + 1j)
t = np.linspace(-1e6, 1e6, 200001)
vals = W(t)
print(f"  real axis: max ||w|-1| = {np.max(np.abs(np.abs(vals) - 1)):.3e}")
for name, z in [("0", 0), ("1", 1), ("-1", -1), ("i", 1j), ("1e6", 1e6)]:
    w = W(complex(z))
    print(f"  z={name:>4s}: w={w:.6f}, |w|={abs(w):.6f}")
upper = np.array([0.5 + 0.3j, 1 + 2j, -3 + 0.1j, 0.2 + 5j])
print(f"  upper half-plane samples: max |w| = {np.max(np.abs(W(upper))):.6f} (< 1)")
print("expect: real axis -> |w|=1; i -> 0; upper half-plane -> disk interior")

print()
print("=== EXP2: grid lines under the same map ===")
for y in [0.5, 1.0, 2.0]:
    z = np.linspace(-6, 6, 4001) + 1j * y
    w = W(z)
    ctr, rad = circle_from_three(w[0], w[2000], w[4000])
    resid = np.max(np.abs(np.abs(w - ctr) - rad))
    print(f"  horizontal y={y}: image circle center={ctr:.6f}, radius={rad:.6f}, "
          f"max |{chr(124)}w-c{chr(124)}-R|={resid:.2e}")
for x in [0.0, 0.5, 2.0]:
    z = x + 1j * np.linspace(0.05, 6, 4001)
    w = W(z)
    if abs(x) < 1e-12:
        print(f"  vertical x=0: image is the real segment [{w.real.min():.6f}, {w.real.max():.6f}] "
              f"with max |Im w| = {np.max(np.abs(w.imag)):.2e}")
        continue
    ctr, rad = circle_from_three(w[0], w[2000], w[4000])
    resid = np.max(np.abs(np.abs(w - ctr) - rad))
    print(f"  vertical x={x}: image circle center={ctr:.6f}, radius={rad:.6f}, "
          f"max |{chr(124)}w-c{chr(124)}-R|={resid:.2e}")
print("expect: all grid lines become circles (or a line segment for x=0) inside the disk")

print()
print("=== EXP3: quadrant -> upper half-plane, w=z^2 ===")
for a_deg in [0, 30, 45, 60, 90]:
    z = 0.5 * np.exp(1j * np.radians(a_deg))
    w = z ** 2
    print(f"  ray {a_deg:2d} deg: w={w:.6f}, arg w={np.degrees(np.angle(w)):7.2f} deg")
z_in = 0.5 + 1j
print(f"  interior z=0.5+i: w={z_in**2:.6f}, Im w={(z_in**2).imag:.6f} (> 0)")
print("expect: rays at 0,45,90 deg become rays at 0,90,180 deg; interior -> upper half-plane")

print()
print("=== EXP4: strip 0<Im z<pi -> upper half-plane, w=e^z ===")
for y in [0.0, np.pi / 2, np.pi]:
    z = 1.0 + 1j * y
    w = np.exp(z)
    print(f"  y={y:.4f}: w={w:.6f}, Im w={w.imag:+.3e}")
z_in = 0.3 + 0.7j
print(f"  interior z=0.3+0.7i: Im e^z = {np.exp(z_in).imag:.6f} (> 0)")
print("expect: y=0 -> positive real axis; y=pi -> negative real axis; interior -> upper half-plane")

print()
print("=== EXP5: upper half disk -> first quadrant -> upper half-plane ===")
A = lambda z: (1 + z) / (1 - z)
B = lambda z: A(z) ** 2
print(f"  z=0 (diameter): A={A(0):.6f}, B={B(0):.6f}")
print(f"  z=0.9 (diameter): A={A(0.9):.6f}, B={B(0.9):.6f}")
z = np.exp(1j * np.pi / 2)
print(f"  z=i (semicircle): A={A(z):.6f}, B={B(z):.6f}")
z = np.exp(1j * np.pi / 4)
print(f"  z=e^(i pi/4): A={A(z):.6f}, B={B(z):.6f}")
z_in = 0.5j
print(f"  interior z=0.5i: A={A(z_in):.6f} (Re>0), B={B(z_in):.6f} (Im>0)")
print("expect: diameter -> positive real axis; semicircle -> positive imaginary axis -> negative real axis")

print()
print("=== EXP6: Joukowski map w=(z+1/z)/2 sends |z|=r to an ellipse ===")
for r in [1.5, 2.0, 3.0]:
    th = np.linspace(0, 2 * np.pi, 20001)
    w = (r * np.exp(1j * th) + np.exp(-1j * th) / r) / 2
    a = (r + 1 / r) / 2
    b = abs(r - 1 / r) / 2
    print(f"  r={r}: max Re={w.real.max():.6f}, max Im={w.imag.max():.6f}; "
          f"predicted semi-axes a={a:.6f}, b={b:.6f}")
print("expect: centred circles -> ellipses with semi-axes (r+1/r)/2 and |r-1/r|/2")

# ---------------------------------------------------------------------------
# FIG1: upper half-plane -> unit disk
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.8))

xs = [-3.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 3.0]
ys = [0.0, 0.3, 0.6, 1.0, 1.5, 2.0, 3.0]
xx = np.linspace(-3.2, 3.2, 1200)
yy = np.linspace(0.0, 3.2, 900)
for x in xs:
    axes[0].plot(np.full_like(yy, x), yy, color=GREY, lw=0.6, alpha=0.8)
for y in ys:
    axes[0].plot(xx, np.full_like(xx, y), color=GREY, lw=0.6, alpha=0.8)
axes[0].plot([-3.2, 3.2], [0, 0], color=RED, lw=2.2)
axes[0].plot([0], [1], "o", color=BLUE, ms=6)
axes[0].text(0.08, 1.08, "z=i", color=BLUE, fontsize=9)
axes[0].text(1.8, 0.1, "实轴", color=RED, fontsize=9)
axes[0].set_xlim(-3.3, 3.3)
axes[0].set_ylim(-0.2, 3.3)
axes[0].set_aspect("equal")
axes[0].set_title("上半平面与网格")
axes[0].set_xlabel("Re z")
axes[0].set_ylabel("Im z")

for x in xs:
    w = W(x + 1j * yy)
    w = np.where(np.abs(w) > 1.2, np.nan, w)
    axes[1].plot(w.real, w.imag, color=GREY, lw=0.6, alpha=0.8)
for y in ys[1:]:
    w = W(xx + 1j * y)
    w = np.where(np.abs(w) > 1.2, np.nan, w)
    axes[1].plot(w.real, w.imag, color=GREY, lw=0.6, alpha=0.8)
th = np.linspace(0, 2 * np.pi, 4000)
axes[1].plot(np.cos(th), np.sin(th), color=RED, lw=2.2)
for z, lab, col in [(0, "z=0", GREEN), (1, "z=1", GREEN), (-1, "z=-1", GREEN), (1e6, "z=inf", GREEN)]:
    w = W(complex(z))
    axes[1].plot([w.real], [w.imag], "o", color=col, ms=5)
    axes[1].text(w.real + 0.04, w.imag + 0.05, lab, color=col, fontsize=8.5)
axes[1].plot([0], [0], "o", color=BLUE, ms=6)
axes[1].text(0.06, 0.13, "z=i 的像", color=BLUE, fontsize=8.5)
axes[1].set_xlim(-1.25, 1.25)
axes[1].set_ylim(-1.25, 1.25)
axes[1].set_aspect("equal")
axes[1].axhline(0, color=GREY, lw=0.5)
axes[1].axvline(0, color=GREY, lw=0.5)
axes[1].set_title("单位圆盘：$w=(z-i)/(z+i)$ 的像")
axes[1].set_xlabel("Re w")
axes[1].set_ylabel("Im w")

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec16_fig1_halfplane_disk.svg"))
fig.savefig(os.path.join(FIGDIR, "lec16_fig1_halfplane_disk.png"), dpi=160)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG2: quadrant opened by z^2; strip opened by e^z
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(10.2, 9.0))

qgrid_x = np.linspace(0.0, 2.6, 600)
qgrid_y = np.linspace(0.0, 2.6, 600)
axes[0, 0].fill_between([0, 2.7], 0, 2.7, color=GREEN, alpha=0.07)
for c in [0.4, 0.8, 1.2, 1.8, 2.4]:
    axes[0, 0].plot(np.full_like(qgrid_y, c), qgrid_y, color=GREY, lw=0.6, alpha=0.8)
    axes[0, 0].plot(qgrid_x, np.full_like(qgrid_x, c), color=GREY, lw=0.6, alpha=0.8)
for a_deg, col in [(0, BLUE), (45, PURPLE), (90, RED)]:
    a = np.radians(a_deg)
    rr = np.linspace(0, 2.5, 400)
    axes[0, 0].plot(rr * np.cos(a), rr * np.sin(a), color=col, lw=2.0)
axes[0, 0].text(2.1, 0.06, "0 deg", color=BLUE, fontsize=8.5)
axes[0, 0].text(1.45, 1.02, "45 deg", color=PURPLE, fontsize=8.5)
axes[0, 0].text(0.06, 2.1, "90 deg", color=RED, fontsize=8.5)
axes[0, 0].set_xlim(-0.15, 2.7)
axes[0, 0].set_ylim(-0.15, 2.7)
axes[0, 0].set_aspect("equal")
axes[0, 0].set_title("角形域：$0<\\mathrm{arg}\\,z<\\pi/2$")
axes[0, 0].set_xlabel("Re z")
axes[0, 0].set_ylabel("Im z")

for c in [0.4, 0.8, 1.2, 1.8, 2.4]:
    w = (c + 1j * qgrid_y) ** 2
    axes[0, 1].plot(w.real, w.imag, color=GREY, lw=0.6, alpha=0.8)
    w = (qgrid_x + 1j * c) ** 2
    axes[0, 1].plot(w.real, w.imag, color=GREY, lw=0.6, alpha=0.8)
axes[0, 1].axhspan(0, 6.6, color=GREEN, alpha=0.07)
for a_deg, col in [(0, BLUE), (45, PURPLE), (90, RED)]:
    a = np.radians(2 * a_deg)
    rr = np.linspace(0, 7, 400)
    axes[0, 1].plot(rr * np.cos(a), rr * np.sin(a), color=col, lw=2.0)
axes[0, 1].text(4.2, 0.08, "0 deg", color=BLUE, fontsize=8.5)
axes[0, 1].text(-4.6, 0.08, "180 deg", color=RED, fontsize=8.5)
axes[0, 1].text(0.1, 5.0, "90 deg", color=PURPLE, fontsize=8.5)
axes[0, 1].set_xlim(-6.8, 6.8)
axes[0, 1].set_ylim(-0.3, 6.6)
axes[0, 1].set_aspect("equal")
axes[0, 1].set_title("$w=z^2$：像为上半平面")
axes[0, 1].set_xlabel("Re w")
axes[0, 1].set_ylabel("Im w")

sx = np.linspace(-3.0, 2.6, 800)
sy = np.linspace(0.0, np.pi, 600)
axes[1, 0].fill_between(sx, 0, np.pi, color=GREEN, alpha=0.07)
strip_levels = [k * np.pi / 8 for k in range(9)]
for y in strip_levels:
    axes[1, 0].plot(sx, np.full_like(sx, y), color=GREY, lw=0.6, alpha=0.8)
for x in [-2.0, -1.0, 0.0, 1.0, 2.0]:
    axes[1, 0].plot(np.full_like(sy, x), sy, color=GREY, lw=0.6, alpha=0.8)
axes[1, 0].plot(sx, np.full_like(sx, 0.0), color=BLUE, lw=2.0)
axes[1, 0].plot(sx, np.full_like(sx, np.pi), color=RED, lw=2.0)
axes[1, 0].text(1.6, 0.08, "y=0", color=BLUE, fontsize=8.5)
axes[1, 0].text(1.4, np.pi - 0.28, "y=pi", color=RED, fontsize=8.5)
axes[1, 0].set_xlim(-3.2, 2.8)
axes[1, 0].set_ylim(-0.3, np.pi + 0.3)
axes[1, 0].set_aspect("equal")
axes[1, 0].set_title("带形域：$0<\\mathrm{Im}\\,z<\\pi$")
axes[1, 0].set_xlabel("Re z")
axes[1, 0].set_ylabel("Im z")

for y in strip_levels:
    w = np.exp(sx + 1j * y)
    w = np.where(np.abs(w) > 12, np.nan, w)
    axes[1, 1].plot(w.real, w.imag, color=GREY, lw=0.6, alpha=0.8)
for x in [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]:
    w = np.exp(x + 1j * sy)
    axes[1, 1].plot(w.real, w.imag, color=GREY, lw=0.6, alpha=0.8)
axes[1, 1].axhspan(0, 6.6, color=GREEN, alpha=0.07)
axes[1, 1].plot([-12, 12], [0, 0], color=GREEN, lw=1.6)
axes[1, 1].set_xlim(-6.5, 6.5)
axes[1, 1].set_ylim(-0.3, 6.6)
axes[1, 1].set_aspect("equal")
axes[1, 1].set_title("$w=e^z$：像为上半平面")
axes[1, 1].set_xlabel("Re w")
axes[1, 1].set_ylabel("Im w")

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec16_fig2_open_domain.svg"))
fig.savefig(os.path.join(FIGDIR, "lec16_fig2_open_domain.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
