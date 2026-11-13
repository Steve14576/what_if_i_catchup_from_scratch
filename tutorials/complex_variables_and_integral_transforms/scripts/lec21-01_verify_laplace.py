# 规模纪律：有限区间数值积分 + 一张双面板 ROC 图，目标 < 6 秒。
# 验证第 21 讲：e^{2t} 的收敛条件、u(t) 与 e^{-3t}u(t) 的 1/s 型变换、
# t^2/sin/cos/delta 的表值、s=iω 回到傅里叶的条件、ROC 边界、作业查表。
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


def lap(f, s, T=60.0, n=400001, t0=0.0):
    """Numerical unilateral Laplace transform at a scalar complex s."""
    t = np.linspace(t0, T, n)
    return np.trapezoid(f(t) * np.exp(-s * t), t)


print("=== EXP1: e^{2t}u(t) -- convergence needs Re s > 2 ===")
for sigma in [1.0, 2.5, 3.0]:
    for T in [5.0, 10.0]:
        t = np.linspace(0.0, T, 200001)
        val = np.trapezoid(np.exp(2 * t) * np.exp(-sigma * t), t)
        print(f"  sigma={sigma}, T={T}: integral={val:.6f}", end="")
        if sigma > 2:
            print(f", 1/(sigma-2)={1/(sigma-2):.6f}")
        else:
            print("  (diverges as T grows)")
print("expect: sigma>2 gives 1/(sigma-2); sigma<2 grows without bound")

print()
print("=== EXP2: u(t) and e^{-3t}u(t), with ROC ===")
for sigma in [0.5, 1.0, 2.0, 5.0]:
    val = lap(lambda t: np.ones_like(t), complex(sigma, 0.0), T=60.0)
    print(f"  u(t), sigma={sigma}: numeric={val.real:.6f}, 1/sigma={1/sigma:.6f}, ROC: sigma>0")
for sigma in [-2.0, 0.0, 1.0]:
    val = lap(lambda t: np.exp(-3 * t), complex(sigma, 0.0), T=60.0)
    print(f"  e^-3t u(t), sigma={sigma}: numeric={val.real:.6f}, 1/(sigma+3)={1/(sigma+3):.6f}, ROC: sigma>-3")
print("expect: both match 1/(s-a); ROC is the half-plane to the right of the pole")

print()
print("=== EXP3: table values (t^2, sin, cos, delta) ===")
s1 = 1 + 2j
val = lap(lambda t: t ** 2, s1, T=80.0, n=800001)
exact = 2 / s1 ** 3
print(f"  t^2 at s=1+2i: numeric={val:.6f}, 2/s^3={exact:.6f}, diff={abs(val-exact):.2e}")
val = lap(lambda t: np.sin(3 * t), s1, T=80.0, n=800001)
exact = 3 / (s1 ** 2 + 9)
print(f"  sin3t at s=1+2i: numeric={val:.6f}, 3/(s^2+9)={exact:.6f}, diff={abs(val-exact):.2e}")
val = lap(lambda t: np.cos(3 * t), s1, T=80.0, n=800001)
exact = s1 / (s1 ** 2 + 9)
print(f"  cos3t at s=1+2i: numeric={val:.6f}, s/(s^2+9)={exact:.6f}, diff={abs(val-exact):.2e}")
tau = 1e-3
dt = lambda t: ((np.abs(t) < tau / 2).astype(float) / tau)
val0 = lap(dt, s1, T=10.0, n=400001, t0=0.0)
valm = lap(dt, s1, T=10.0, n=400001, t0=-tau)
print(f"  delta at s=1+2i, integrate from 0^+: {val0:.6f} (misses the left half)")
print(f"  delta at s=1+2i, integrate from 0^-: {valm:.6f} (expect 1)")
print("expect: t^2 -> 2/s^3, sin -> 3/(s^2+9), cos -> s/(s^2+9); delta needs the 0^- lower limit")

print()
print("=== EXP4: s=i*omega returns Fourier only if ROC contains the imaginary axis ===")
val = lap(lambda t: np.exp(-3 * t), 1j * 1.0, T=80.0, n=800001)
exact = 1 / (3 + 1j)
print(f"  e^-3t u(t) at s=i: numeric={val:.6f}, Fourier 1/(3+i)={exact:.6f}, diff={abs(val-exact):.2e}")
for T in [5.0, 10.0]:
    t = np.linspace(0.0, T, 200001)
    val = np.trapezoid(np.exp(2 * t) * np.exp(-0.0 * t), t)
    print(f"  e^2t u(t) at sigma=0, T={T}: integral={val:.6f} (grows; no Fourier)")
print("expect: ROC of e^-3t u contains i-axis -> Fourier exists; e^2t u does not")

print()
print("=== EXP5: the ROC boundary is excluded ===")
for T in [10.0, 100.0]:
    t = np.linspace(0.0, T, 200001)
    val = np.trapezoid(np.exp(-3 * t) * np.exp(3 * t), t)
    print(f"  e^-3t u(t) at sigma=-3, T={T}: integral={val:.6f} (grows linearly)")
print("expect: on sigma=sigma0 the integral diverges, so the boundary is not in the ROC")

print()
print("=== EXP6: table lookup check (homework) ===")
s1 = 1 + 1j
f = lambda t: 3 * np.exp(-2 * t) + 2 * np.sin(5 * t)
val = lap(f, s1, T=80.0, n=800001)
exact = 3 / (s1 + 2) + 10 / (s1 ** 2 + 25)
print(f"  L[3e^-2t + 2 sin5t] at s=1+i: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: linearity + table; ROC is sigma > 0 (intersection of sigma > -2 and sigma > 0)")

# ---------------------------------------------------------------------------
# FIG1: ROC in the s-plane -- containing vs excluding the imaginary axis
# ---------------------------------------------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(11.0, 4.4))
for ax, pole, lo, hi, title in [
    (axs[0], -3.0, -3.0, 6.0, "$e^{-3t}u(t)$：ROC $\\sigma>-3$，含虚轴"),
    (axs[1], 2.0, 2.0, 6.0, "$e^{2t}u(t)$：ROC $\\sigma>2$，不含虚轴"),
]:
    ax.axvspan(lo, hi, color=BLUE, alpha=0.12)
    ax.axhline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=RED, lw=1.0, ls="--")
    ax.plot([pole], [0], "x", color=RED, ms=10, mew=2.0)
    ax.text(pole, -0.6, f"$s={pole:g}$", color=RED, ha="center", fontsize=10)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-4, 4)
    ax.set_xlabel("$\\sigma$")
    ax.set_ylabel("$i\\omega$")
    ax.set_title(title)
    ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec21_fig1_roc.svg"))
fig.savefig(os.path.join(FIGDIR, "lec21_fig1_roc.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)