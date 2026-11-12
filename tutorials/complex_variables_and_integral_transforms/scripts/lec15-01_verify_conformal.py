# 规模纪律：若干次数值微分与两张网格图，目标 < 8 秒。
# 验证第 15 讲：导数的伸缩率与旋转角、保角条件 f'(z0)!=0、z^2 在 0 的角放大、
# 分式线性映射的四步分解、保圆性、保对称性、不动点、三对点定映射与交比不变性。
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


def angle_deg(z):
    return np.degrees(np.angle(z))


print("=== EXP1: derivative = local scale factor + local rotation ===")
f = lambda z: z ** 2
z0 = 1 + 1j
fp = 2 * z0
print(f"f=z^2, z0=1+i: f'(z0)={fp:.6f}, |f'|={abs(fp):.6f} (=2*sqrt2={2*np.sqrt(2):.6f}), "
      f"arg f'={angle_deg(fp):.4f} deg")
for a_deg in [0.0, 30.0, 60.0, 90.0]:
    h = 1e-6
    dz = h * np.exp(1j * np.radians(a_deg))
    ratio = (f(z0 + dz) - f(z0)) / dz
    print(f"  direction {a_deg:5.1f} deg: difference quotient = {ratio:.6f}, "
          f"|q|={abs(ratio):.6f}, arg q={angle_deg(ratio):.4f} deg")
print("expect: all four quotients agree with f'(z0); the direction drops out")

print()
print("=== EXP2: angle between two curves is preserved when f'(z0)!=0 ===")
z0 = 1 + 1j
alphas = [0.0, 40.0]
out_angles = []
for a_deg in alphas:
    # tangent of the image curve: divide the image increment by the real step t,
    # not by dz = t*exp(i*a), otherwise the direction cancels out.
    t = 1e-6
    dz = t * np.exp(1j * np.radians(a_deg))
    tangent = (f(z0 + dz) - f(z0)) / t
    out_angles.append(angle_deg(tangent))
    print(f"  incoming direction {a_deg:5.1f} deg -> image tangent {angle_deg(tangent):8.4f} deg, "
          f"|tangent|={abs(tangent):.6f}")
print(f"incoming angle difference = {alphas[1]-alphas[0]:.1f} deg; "
      f"measured image angle difference = {out_angles[1]-out_angles[0]:.4f} deg")
print("expect: same difference (40 deg), both lengths scaled by |f'|")

print()
print("=== EXP3: at f'(z0)=0 the angle is multiplied by the order ===")
for n in [2, 3]:
    a1, a2 = 0.0, 30.0
    out1 = n * a1
    out2 = n * a2
    print(f"f=z^{n} at 0: incoming {a1:.0f} and {a2:.0f} deg -> outgoing {out1:.0f} and {out2:.0f} deg; "
          f"incoming gap {a2-a1:.0f} deg, outgoing gap {out2-out1:.0f} deg")
print("expect: outgoing gap = n * incoming gap")

print()
print("=== EXP4: Mobius map w=(2z+1)/(z-1) = 2 + 3/(z-1) ===")
M = lambda z: (2 * z + 1) / (z - 1)
steps = lambda z: 2 + 3 / (z - 1)
for z in [-2, 0, 2, 3, 1 + 1j]:
    print(f"  z={z:>8}: direct={M(z):.10f}, four-step={steps(z):.10f}, "
          f"diff={abs(M(z)-steps(z)):.2e}")
print(f"  ad-bc = 2*(-1) - 1*1 = {2*(-1)-1*1}")
print(f"  z=1 (=-d/c) maps to |w|={abs(M(1+1e-9)):.3e} (grows like 1/eps)")
print(f"  z=infinity maps to a/c = {2/1:.6f}")
print("expect: direct and four-step agree; pole at z=1; infinity -> 2")

print()
print("=== EXP5: circles map to circles or lines (w=(z-1)/(z+1)) ===")
W = lambda z: (z - 1) / (z + 1)
th = np.linspace(0, 2 * np.pi, 20001)
unit = np.exp(1j * th)
img = W(unit)
safe = np.abs(unit + 1) > 1e-6          # the unit circle passes through the pole z=-1
print(f"  image of |z|=1 away from z=-1: max |Re w| = {np.max(np.abs(img.real[safe])):.3e}")
print(f"  image of |z|=1: |Im w| reaches {np.max(np.abs(img.imag)):.3e} near z=-1 -> unbounded")
print("  so the image is the whole imaginary axis, not a bounded circle")
c2 = 2 + np.exp(1j * th)
img2 = W(c2)
# circle through three image points: w = center + R exp(i phi)
A, B, C = img2[0], img2[len(img2) // 3], img2[2 * len(img2) // 3]
def circle_from_three(a, b, c):
    ax, ay = a.real, a.imag
    bx, by = b.real, b.imag
    cx, cy = c.real, c.imag
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    return complex(ux, uy), abs(a - complex(ux, uy))
ctr, rad = circle_from_three(A, B, C)
resid = np.max(np.abs(np.abs(img2 - ctr) - rad))
print(f"  image of |z-2|=1: fitted center={ctr:.6f}, radius={rad:.6f}, "
      f"max |{chr(124)}w-c{chr(124)}-R| = {resid:.3e}")
print("expect: first image is the imaginary axis (Re=0, unbounded); second is a circle to 1e-15")

print()
print("=== EXP6: symmetry is preserved (unit circle -> imaginary axis) ===")
z_a, z_b = 2.0, 0.5
wa, wb = W(z_a), W(z_b)
print(f"  z={z_a} and 1/conj(z)={z_b}: w={wa:.6f} and {wb:.6f}")
print(f"  Re(w) values: {wa.real:.6f}, {wb.real:.6f}; sum={wa.real+wb.real:+.3e}")
print("expect: symmetric points about the unit circle map to points symmetric about Im axis "
      "(w -> -conj(w)), so their real parts cancel")

print()
print("=== EXP7: fixed points of w=(z-1)/(z+1) ===")
for z in [1j, -1j]:
    print(f"  z={z}: w={W(z):.3e}, |w-z|={abs(W(z)-z):.3e}")
print("expect: z=+i and z=-i are fixed; two fixed points")

print()
print("=== EXP8: three pairs determine the map (0,1,inf) -> (1,i,-1) ===")
Mw = lambda z: (1 + 1j * z) / (1 - 1j * z)
for z, target in [(0, 1), (1, 1j), (1e12, -1)]:
    print(f"  z={z:>10}: w={Mw(z):.9f}, target={target:.6f}, diff={abs(Mw(z)-target):.2e}")
print("  coefficients: a=i, b=1, c=-i, d=1; ad-bc =", (1j * 1 - 1 * (-1j)))
print("expect: the three images match; ad-bc = 2i != 0")

print()
print("=== EXP9: cross ratio is invariant ===")
def cross_ratio(z1, z2, z3, z4):
    return ((z4 - z1) * (z2 - z3)) / ((z4 - z3) * (z2 - z1))

pts = [0.3 + 0.2j, 1.5 - 0.4j, 2.0 + 1.0j, -0.5 + 0.7j]
cr_z = cross_ratio(*pts)
cr_w = cross_ratio(*[M(p) for p in pts])
print(f"  cross ratio in z-plane = {cr_z:.10f}")
print(f"  cross ratio in w-plane = {cr_w:.10f}")
print(f"  difference = {abs(cr_z - cr_w):.3e}")
print("expect: identical for the Mobius map w=(2z+1)/(z-1)")

# ---------------------------------------------------------------------------
# FIG1: angle doubling at z=0 under w=z^2
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6))

t = np.linspace(0, 1, 200)
for k, (a_deg, col) in enumerate([(0, BLUE), (45, RED)]):
    a = np.radians(a_deg)
    seg = t * 0.9 * np.exp(1j * a)
    axes[0].plot(seg.real, seg.imag, color=col, lw=2.2)
axes[0].text(0.72, 0.06, "0 deg", color=BLUE, fontsize=9)
axes[0].text(0.48, 0.56, "45 deg", color=RED, fontsize=9)
axes[0].text(0.02, -0.075, "两射线夹角 45 deg", color=GREY, fontsize=8.5)
axes[0].set_title("z 平面：以 0 为顶点的两条射线")
axes[0].set_xlim(-0.15, 1.05)
axes[0].set_ylim(-0.1, 1.0)
axes[0].set_aspect("equal")
axes[0].axhline(0, color=GREY, lw=0.5)
axes[0].axvline(0, color=GREY, lw=0.5)
axes[0].set_xlabel("Re z")
axes[0].set_ylabel("Im z")

t = np.linspace(0, 1, 200)
for a_deg, col in [(0, BLUE), (45, RED)]:
    a = np.radians(a_deg)
    seg = t * 0.8 * np.exp(1j * a)
    img = seg ** 2
    axes[1].plot(img.real, img.imag, color=col, lw=2.6)
axes[1].text(0.52, 0.035, "0 deg", color=BLUE, fontsize=9)
axes[1].text(-0.06, 0.52, "90 deg", color=RED, fontsize=9, ha="right")
axes[1].text(0.06, -0.115, "像的夹角 90 deg", color=GREY, fontsize=8.5)
axes[1].set_title("w 平面：$w=z^2$ 把夹角放大为 2 倍")
axes[1].set_xlim(-0.9, 0.9)
axes[1].set_ylim(-0.15, 0.95)
axes[1].set_aspect("equal")
axes[1].axhline(0, color=GREY, lw=0.5)
axes[1].axvline(0, color=GREY, lw=0.5)
axes[1].set_xlabel("Re w")
axes[1].set_ylabel("Im w")

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec15_fig1_angle_doubling.svg"))
fig.savefig(os.path.join(FIGDIR, "lec15_fig1_angle_doubling.png"), dpi=160)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG2: grid deformation under w=(z-1)/(z+1); unit circle -> imaginary axis
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.8))

xs = [-3.0, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
ys = [-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0]
yy = np.linspace(-3.0, 3.0, 800)
xx = np.linspace(-3.0, 3.0, 800)
for x in xs:
    axes[0].plot(np.full_like(yy, x), yy, color=GREY, lw=0.7, alpha=0.8)
for y in ys:
    axes[0].plot(xx, np.full_like(xx, y), color=GREY, lw=0.7, alpha=0.8)
circ = np.exp(1j * th)
axes[0].plot(circ.real, circ.imag, color=RED, lw=2.0, label="$|z|=1$")
axes[0].plot([-1], [0], "x", color=BLUE, ms=9, mew=2.0)
axes[0].text(-1.95, 0.34, "z=-1（极点）", color=BLUE, fontsize=8.5,
             bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))
axes[0].set_xlim(-3.2, 3.2)
axes[0].set_ylim(-2.4, 2.4)
axes[0].set_aspect("equal")
axes[0].set_title("z 平面：网格与单位圆")
axes[0].set_xlabel("Re z")
axes[0].set_ylabel("Im z")

big = 6.0
for x in xs:
    if abs(x + 1) < 1e-9:
        # the grid line through the pole: its image is the vertical line through w=1
        # geometric spacing so the image is drawn continuously through w=1
        tt = np.concatenate([-np.geomspace(0.01, 300, 600), np.geomspace(0.01, 300, 600)])
        wv = 1 + 2j / tt
        wv = np.where(np.abs(wv) > big, np.nan, wv)
        axes[1].plot(wv.real, wv.imag, color=PURPLE, lw=2.4, alpha=1.0, zorder=4)
        print(f"  grid line x=-1: finite image points = {np.sum(np.isfinite(wv.real))}, "
              f"Re w = {np.nanmin(wv.real):.3f}..{np.nanmax(wv.real):.3f}")
        continue
    wv = W(x + 1j * yy)
    wv = np.where(np.abs(wv) > big, np.nan, wv)
    axes[1].plot(wv.real, wv.imag, color=GREY, lw=0.7, alpha=0.8)
for y in ys:
    wv = W(xx + 1j * y)
    wv = np.where(np.abs(wv) > big, np.nan, wv)
    axes[1].plot(wv.real, wv.imag, color=GREY, lw=0.7, alpha=0.8)
img = W(circ)
axes[1].plot(img.real, img.imag, color=RED, lw=2.2, label="单位圆的像：虚轴")
axes[1].plot([1], [0], "o", color=GREEN, ms=6)
axes[1].text(1.15, -0.45, "z=inf 的像：w=1", color=GREEN, fontsize=8.5, ha="center",
             bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))
axes[1].text(-2.5, 2.05, "z=-1 的像：直线 Re w=1", color=PURPLE, fontsize=8.5,
             bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))
axes[1].set_xlim(-2.6, 2.6)
axes[1].set_ylim(-2.4, 2.4)
axes[1].set_aspect("equal")
axes[1].axhline(0, color=GREY, lw=0.5)
axes[1].axvline(0, color=GREY, lw=0.5)
axes[1].set_title("w 平面：$w=(z-1)/(z+1)$ 的像")
axes[1].set_xlabel("Re w")
axes[1].set_ylabel("Im w")

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec15_fig2_mobius_grid.svg"))
fig.savefig(os.path.join(FIGDIR, "lec15_fig2_mobius_grid.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
