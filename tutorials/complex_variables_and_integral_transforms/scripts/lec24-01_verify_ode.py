# 规模纪律：小网格方向场 + 解析解回代，目标 < 6 秒。
# 验证第 24 讲：一阶线性、可分离（含丢解）、二阶三种根、待定系数与共振、欧拉方程。
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


def max_residual(y, x, expr):
    return float(np.max(np.abs(expr(y, x))))


print("=== EXP1: verify y=C1 cos x + C2 sin x for y''+y=0 ===")
x = np.linspace(0.0, 6.0, 601)
y = np.cos(x)          # C1=1, C2=0, y(0)=1, y'(0)=0
res = np.max(np.abs((-y) + y))
print(f"  y=cos x: max|y''+y|={res:.2e}, y(0)={y[0]:.6f}, y'(0)={-np.sin(0.0):.6f}")
print("expect: residual 0; the two initial conditions fix C1=1, C2=0")

print()
print("=== EXP2: first-order linear y'+2y=e^-x, y(0)=2 ===")
y = np.exp(-x) + np.exp(-2 * x)
res = np.max(np.abs(((-np.exp(-x) - 2 * np.exp(-2 * x)) + 2 * y) - np.exp(-x)))
print(f"  y=e^-x+e^-2x: max residual={res:.2e}, y(0)={y[0]:.6f}")
print("expect: residual 0 and y(0)=2; integrating factor mu=e^{2x}")

print()
print("=== EXP3: separable y'=y(1-y), y(0)=1/2 ===")
y = 1 / (1 + np.exp(-x))
res = np.max(np.abs((np.exp(-x) / (1 + np.exp(-x)) ** 2) - y * (1 - y)))
print(f"  logistic: max residual={res:.2e}, y(0)={y[0]:.6f}")
for c in [0.0, 1.0]:
    print(f"  constant y={c:g}: y'=0, y(1-y)={c*(1-c):.1f} -> solution")
print("expect: logistic solves the IVP; y=0 and y=1 are the lost constant solutions")

print()
print("=== EXP4: distinct real roots y''+3y'+2y=0, y(0)=1, y'(0)=0 ===")
y = 2 * np.exp(-x) - np.exp(-2 * x)
res = np.max(np.abs((2 * np.exp(-x) - 4 * np.exp(-2 * x)) + 3 * (-2 * np.exp(-x) + 2 * np.exp(-2 * x)) + 2 * y))
print(f"  y=2e^-x-e^-2x: max residual={res:.2e}, y(0)={y[0]:.6f}, y'(0)={-2+2:.6f}")
print("expect: roots -1,-2; initial conditions give C1=2, C2=-1")

print()
print("=== EXP5: repeated root y''+2y'+y=0, y(0)=1, y'(0)=0 ===")
y = (1 + x) * np.exp(-x)
res = np.max(np.abs((x - 1) * np.exp(-x) + 2 * (-x) * np.exp(-x) + y))
print(f"  y=(1+x)e^-x: max residual={res:.2e}, y(0)={y[0]:.6f}, y'(0)={1-1:.6f}")
print("expect: root -1 double; initial conditions give C1=1, C2=1")

print()
print("=== EXP6: complex roots y''+2y'+5y=0, y(0)=1, y'(0)=0 ===")
y = np.exp(-x) * (np.cos(2 * x) + 0.5 * np.sin(2 * x))
yd = np.exp(-x) * (-np.cos(2 * x) - 0.5 * np.sin(2 * x) - 2 * np.sin(2 * x) + np.cos(2 * x))
ydd = np.exp(-x) * (2.5 * np.sin(2 * x) - 5 * np.cos(2 * x))
res = np.max(np.abs(ydd + 2 * yd + 5 * y))
print(f"  y=e^-x(cos2x+0.5sin2x): max residual={res:.2e}, y(0)={y[0]:.6f}, y'(0)={-1+1:.6f}")
print("expect: roots -1+-2i; initial conditions give C1=1, C2=0.5")

print()
print("=== EXP7: undetermined coefficients ===")
# (a) nonresonant exponential
y = np.exp(3 * x) / 20
res = np.max(np.abs((9 * y) + 3 * (3 * y) + 2 * y - np.exp(3 * x)))
print(f"  y''+3y'+2y=e^3x, Y=e^3x/20: max residual={res:.2e}")
# (b) resonance
y = -x * np.exp(x)
res = np.max(np.abs((-(x + 2) * np.exp(x)) - 3 * (-(x + 1) * np.exp(x)) + 2 * y - np.exp(x)))
print(f"  y''-3y'+2y=e^x, Y=-x e^x: max residual={res:.2e}")
# (c) trigonometric right-hand side
y = (-3 * np.cos(2 * x) + 2 * np.sin(2 * x)) / 13
yd = (6 * np.sin(2 * x) + 4 * np.cos(2 * x)) / 13
ydd = (12 * np.cos(2 * x) - 8 * np.sin(2 * x)) / 13
res = np.max(np.abs(ydd + yd + y - np.cos(2 * x)))
print(f"  y''+y'+y=cos2x, Y=(-3cos2x+2sin2x)/13: max residual={res:.2e}")
print("expect: all residuals 0; resonance needs the extra factor x")

print()
print("=== EXP8: homework checks: resonance and sine RHS ===")
y = 0.5 * x * np.exp(x)
res = np.max(np.abs((0.5 * (x + 2) * np.exp(x)) - y - np.exp(x)))
print(f"  y''-y=e^x, Y=0.5x e^x: max residual={res:.2e}")
y = (-2 * np.cos(2 * x) - 3 * np.sin(2 * x)) / 13
yd = (4 * np.sin(2 * x) - 6 * np.cos(2 * x)) / 13
ydd = (8 * np.cos(2 * x) + 12 * np.sin(2 * x)) / 13
res = np.max(np.abs(ydd + yd + y - np.sin(2 * x)))
print(f"  y''+y'+y=sin2x, Y=(-2cos2x-3sin2x)/13: max residual={res:.2e}")
print("expect: residuals 0")

print()
print("=== EXP9: Euler equation x^2 y'' - 2x y' + 2y = 0 ===")
y = 2 * x + 3 * x ** 2
res = np.max(np.abs(x ** 2 * (6) - 2 * x * (2 + 6 * x) + 2 * y))
print(f"  y=2x+3x^2: max residual={res:.2e}")
print("expect: y=x^r gives r(r-1)-2r+2=(r-1)(r-2)=0; residual 0")

# ---------------------------------------------------------------------------
# FIG1: direction fields and integral curves
# ---------------------------------------------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.6))

# (a) y' = x - y
xg, yg = np.meshgrid(np.linspace(-3, 3, 25), np.linspace(-3, 3, 25))
axs[0].streamplot(xg, yg, np.ones_like(xg), xg - yg, color=GREY, linewidth=0.7, density=1.1, arrowsize=0.8)
xs = np.linspace(-3, 3, 400)
for C, col in [(-2, "#a0aec0"), (-1, BLUE), (0, GREEN), (1, "#dd6b20"), (2, RED)]:
    axs[0].plot(xs, xs - 1 + C * np.exp(-xs), color=col, lw=1.4)
axs[0].set_xlim(-3, 3)
axs[0].set_ylim(-3, 3)
axs[0].set_xlabel("$x$")
axs[0].set_ylabel("$y$")
axs[0].set_title("$y'=x-y$：解是一族曲线 $y=x-1+Ce^{-x}$")
axs[0].grid(alpha=0.25)

# (b) y' = y(1-y)
xg, yg = np.meshgrid(np.linspace(0, 6, 25), np.linspace(-0.2, 1.6, 25))
axs[1].streamplot(xg, yg, np.ones_like(xg), yg * (1 - yg), color=GREY, linewidth=0.7, density=1.1, arrowsize=0.8)
xs = np.linspace(0, 6, 400)
for C, col in [(0.5, "#a0aec0"), (1, BLUE), (2, GREEN), (5, RED)]:
    axs[1].plot(xs, 1 / (1 + C * np.exp(-xs)), color=col, lw=1.4)
axs[1].axhline(0, color=RED, lw=1.2, ls="--")
axs[1].axhline(1, color=RED, lw=1.2, ls="--")
axs[1].text(4.2, 0.06, "$y=0$", color=RED)
axs[1].text(4.2, 1.04, "$y=1$", color=RED)
axs[1].set_xlim(0, 6)
axs[1].set_ylim(-0.2, 1.6)
axs[1].set_xlabel("$x$")
axs[1].set_ylabel("$y$")
axs[1].set_title("$y'=y(1-y)$：两条平衡解与 logistic 曲线")
axs[1].grid(alpha=0.25)

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec24_fig1_direction_field.svg"))
fig.savefig(os.path.join(FIGDIR, "lec24_fig1_direction_field.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)