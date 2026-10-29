# 规模纪律：若干次 quad 与两张图，目标 < 10 秒。
# 验证第 14 讲：三类实积分的留数结果、大圆弧积分趋于零、约当引理、主值积分。
# 运行：uv run --with numpy --with scipy --with matplotlib python <本文件>
import os

import numpy as np
from scipy.integrate import quad
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


def arc_integral(f, R, lower=False, points=200000):
    """Integral of f along the semicircle |z|=R, counterclockwise from R to -R
    (upper half) or clockwise from R to -R through the lower half."""
    if lower:
        t = np.linspace(0, -np.pi, points)
    else:
        t = np.linspace(0, np.pi, points)
    z = R * np.exp(1j * t)
    dz = 1j * R * np.exp(1j * t)
    return np.trapezoid(f(z) * dz, t)


print("=== EXP1: type I, rational functions on the real line ===")
cases = [
    ("1/(x^2+1)", lambda x: 1 / (x ** 2 + 1), np.pi),
    ("1/(x^2+1)^2", lambda x: 1 / (x ** 2 + 1) ** 2, np.pi / 2),
    ("1/(x^4+1)", lambda x: 1 / (x ** 4 + 1), np.pi / np.sqrt(2)),
]
for name, f, exact in cases:
    val, err = quad(f, -np.inf, np.inf)
    print(f"{name:12s}: quad={val:.9f}, residue={exact:.9f}, diff={val-exact:+.2e}")

print()
print("=== EXP2: the arc integral of 1/(z^2+1) tends to zero ===")
for R in [2, 5, 10, 50, 200]:
    val = arc_integral(lambda z: 1 / (z ** 2 + 1), R)
    bound = np.pi * R / (R ** 2 - 1)
    print(f"R={R:4d}: |arc|={abs(val):.6e}, ML bound={bound:.6e}")
print("expect: both shrink like pi/R")

print()
print("=== EXP3: type II, trigonometric integrals on [0, 2*pi] ===")
val, _ = quad(lambda t: 1 / (2 + np.cos(t)), 0, 2 * np.pi)
print(f"1/(2+cos t)       : quad={val:.9f}, residue 2*pi/sqrt(3)={2*np.pi/np.sqrt(3):.9f}")
val, _ = quad(lambda t: 1 / (5 + 3 * np.sin(t)), 0, 2 * np.pi)
print(f"1/(5+3 sin t)     : quad={val:.9f}, residue 2*pi/4={2*np.pi/4:.9f}")
p = 0.5
val, _ = quad(lambda t: 1 / (1 - 2 * p * np.cos(t) + p ** 2), 0, 2 * np.pi)
print(f"1/(1-2p cos t+p^2): quad={val:.9f}, residue 2*pi/(1-p^2)={2*np.pi/(1-p**2):.9f}  (p=0.5)")

print()
print("=== EXP4: type III, integrals with e^{iax} ===")
# cos x/(x^2+1) is even: integral over R = 2 * integral over [0, inf)
val, _ = quad(lambda x: 1 / (x ** 2 + 1), 0, np.inf, weight="cos", wvar=1.0)
print(f"cos x/(x^2+1)   : quad={2*val:.9f}, residue pi/e={np.pi/np.e:.9f}")
val, _ = quad(lambda x: x / (x ** 2 + 1), 0, np.inf, weight="sin", wvar=1.0)
print(f"x sin x/(x^2+1) : quad={2*val:.9f}, residue pi/e={np.pi/np.e:.9f}")
val, _ = quad(lambda x: 1 / (x ** 2 + 1), 0, np.inf, weight="cos", wvar=2.0)
print(f"cos 2x/(x^2+1)  : quad={2*val:.9f}, residue pi/e^2={np.pi/np.e**2:.9f}")

print()
print("=== EXP5: Jordan lemma, upper arc vs lower arc for z e^{iz}/(z^2+1) ===")
g = lambda z: z * np.exp(1j * z) / (z ** 2 + 1)
lower_limit = -1j * np.pi * (np.e + 1 / np.e)
print(f"predicted lower-arc limit = -i*pi*(e+1/e) = {lower_limit.imag:+.6f}j, |.|={abs(lower_limit):.6f}")
print("upper arc:")
for R in [5, 10, 20, 40, 80, 160]:
    up = arc_integral(g, R, points=400000)
    print(f"  R={R:3d}: |upper arc|={abs(up):.6e}  (2|cos R|/R={2*abs(np.cos(R))/R:.3e})")
print("lower arc (only moderate R; integrand peaks near e^R):")
for R in [5, 10, 15, 20, 30]:
    low = arc_integral(g, R, lower=True, points=400000)
    roundoff = np.exp(R) * 2.2e-16
    print(f"  R={R:3d}: lower arc={low.real:+.4f}{low.imag:+.4f}j  "
          f"(peak e^R={np.exp(R):.2e}, roundoff scale={roundoff:.1e})")
print("expect: upper arc -> 0 (Jordan), oscillating within about 2|cos R|/R;")
print("        lower arc stays bounded but tends to -i*pi*(e+1/e), NOT to 0;")
print("        for R >= 40 double precision cannot resolve the cancellation (roundoff > 1)")

print()
print("=== EXP6: principal value, integral of sin x / x ===")
val, _ = quad(lambda x: 1 / x, 1e-12, np.inf, weight="sin", wvar=1.0)
print(f"2 * int_0^inf sin x/x dx = {2*val:.9f}, residue/indent result pi = {np.pi:.9f}")
# small semicircle above 0, clockwise, for e^{iz}/z: should tend to -pi*i
for eps in [1e-1, 1e-2, 1e-3]:
    t = np.linspace(np.pi, 0, 200000)
    z = eps * np.exp(1j * t)
    dz = 1j * eps * np.exp(1j * t)
    small = np.trapezoid(np.exp(1j * z) / z * dz, t)
    print(f"eps={eps:.0e}: small semicircle integral = {small.real:+.6f}{small.imag:+.6f}j")
print("expect: tends to -pi*i = -3.141593j")

print()
print("=== EXP7: a case where the arc does NOT vanish ===")
for R in [5, 50, 500]:
    val = arc_integral(lambda z: z / (z ** 2 + 1), R)
    print(f"R={R:4d}: arc integral of z/(z^2+1) = {val.real:+.6f}{val.imag:+.6f}j")
print("expect: tends to pi*i, not 0; deg Q - deg P = 1 is not enough for type I")

print()
print("=== EXP8: homework answers ===")
hw = []
v, _ = quad(lambda x: 1 / (x ** 2 + 4), -np.inf, np.inf)
hw.append(("HW1 1/(x^2+4)", v, np.pi / 2))
v, _ = quad(lambda t: 1 / (3 + np.cos(t)), 0, 2 * np.pi)
hw.append(("HW2 1/(3+cos t)", v, np.pi / np.sqrt(2)))
v, _ = quad(lambda x: 1 / (x ** 2 + 4), 0, np.inf, weight="cos", wvar=1.0)
hw.append(("HW3 cos x/(x^2+4)", 2 * v, np.pi * np.exp(-2) / 2))
v, _ = quad(lambda x: 1 / ((x ** 2 + 1) * (x ** 2 + 4)), -np.inf, np.inf)
hw.append(("HW5 1/((x^2+1)(x^2+4))", v, np.pi / 6))
a_, b_ = 5.0, 3.0
v, _ = quad(lambda t: 1 / (a_ + b_ * np.cos(t)), 0, 2 * np.pi)
hw.append(("HW6 1/(5+3cos t)", v, 2 * np.pi / np.sqrt(a_ ** 2 - b_ ** 2)))
v, _ = quad(lambda x: x / (x ** 2 + 4), 0, np.inf, weight="sin", wvar=1.0)
hw.append(("HW7 x sin x/(x^2+4)", 2 * v, np.pi * np.exp(-2)))
# sin x / x is smooth at 0 (removable). Split: [0,1] with sinc (smooth), [1,inf) with sin weight.
v1, _ = quad(lambda x: np.sinc(x / np.pi) / (x ** 2 + 1), 0, 1)
v2, _ = quad(lambda x: 1 / (x * (x ** 2 + 1)), 1, np.inf, weight="sin", wvar=1.0)
hw.append(("HW8 sin x/(x(x^2+1))", 2 * (v1 + v2), np.pi * (1 - 1 / np.e)))
a_, b_ = 2.0, 3.0
v, _ = quad(lambda x: 1 / (x ** 2 + b_ ** 2), 0, np.inf, weight="cos", wvar=a_)
hw.append(("HW10 int_0^inf cos2x/(x^2+9)", v, np.pi * np.exp(-a_ * b_) / (2 * b_)))
for w in [-1.5, 0.0, 1.5]:
    v, _ = quad(lambda t: 1 / (1 + t ** 2), 0, np.inf, weight="cos", wvar=abs(w)) if w != 0 else quad(lambda t: 1 / (1 + t ** 2), 0, np.inf)
    hw.append((f"HW11 F(w={w:+.1f})", 2 * v, np.pi * np.exp(-abs(w))))
for name, v, exact in hw:
    print(f"{name:32s}: quad={v:.9f}, answer={exact:.9f}, diff={v-exact:+.1e}")

# ---------------------------------------------------------------------------
# FIG1: the semicircular contour and arc decay
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.8))

R = 2.4
t = np.linspace(0, np.pi, 300)
axes[0].plot([-R, R], [0, 0], color=BLUE, lw=2.0)
axes[0].plot(R * np.cos(t), R * np.sin(t), color=GREEN, lw=2.0)
axes[0].annotate("", xy=(0.6, 0), xytext=(-0.2, 0),
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.6))
axes[0].annotate("", xy=(R * np.cos(1.0), R * np.sin(1.0)),
                 xytext=(R * np.cos(0.75), R * np.sin(0.75)),
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.6))
axes[0].plot([0], [1], "x", color=RED, ms=10, mew=2.2)
axes[0].plot([0], [-1], "x", color=GREY, ms=10, mew=2.2)
axes[0].text(0.12, 1.05, "$i$（在内部）", color=RED, fontsize=10)
axes[0].text(0.12, -1.15, "$-i$（在外部）", color=GREY, fontsize=10)
axes[0].text(1.0, -0.32, "实轴段 $[-R,R]$", color=BLUE, fontsize=10)
axes[0].text(1.55, 2.3, "大半圆 $C_R$", color=GREEN, fontsize=10)
axes[0].set_xlim(-3.0, 3.0)
axes[0].set_ylim(-1.6, 2.9)
axes[0].set_aspect("equal")
axes[0].axhline(0, color=GREY, lw=0.5)
axes[0].axvline(0, color=GREY, lw=0.5)
axes[0].set_title("上半平面闭路：实轴段 + 大半圆")
axes[0].set_xlabel("实轴 Re")
axes[0].set_ylabel("虚轴 Im")

Rs = np.array([2, 3, 5, 8, 12, 20, 35, 60, 100, 200])
vals = [abs(arc_integral(lambda z: 1 / (z ** 2 + 1), r)) for r in Rs]
bound = np.pi * Rs / (Rs ** 2 - 1)
vals_bad = [abs(arc_integral(lambda z: z / (z ** 2 + 1), r)) for r in Rs]
axes[1].loglog(Rs, vals, "o-", color=BLUE, lw=1.6, ms=4, label="$1/(z^2+1)$ 的弧积分")
axes[1].loglog(Rs, bound, "--", color=GREY, lw=1.2, label="ML 上界 $\\pi R/(R^2-1)$")
axes[1].loglog(Rs, vals_bad, "s-", color=RED, lw=1.6, ms=4, label="$z/(z^2+1)$ 的弧积分")
axes[1].set_xlabel("$R$")
axes[1].set_ylabel("弧积分的模")
axes[1].set_title("分母高两次：弧积分趋于零；只高一次：不趋于零")
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.25, which="both")

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec14_fig1_semicircle.svg"))
fig.savefig(os.path.join(FIGDIR, "lec14_fig1_semicircle.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
