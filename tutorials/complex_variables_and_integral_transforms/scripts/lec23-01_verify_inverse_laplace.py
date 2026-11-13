# 规模纪律：有限区间数值积分 + 一张 2x3 极点/时域图，目标 < 6 秒。
# 验证第 23 讲：部分分式（单实/共轭复/重极点）、留数、卷积求逆、假分式。
# 每个逆变换结果都用正变换在 s=0.5+i 处回代核对。
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
S1 = 0.5 + 1j


def lap(f, s=S1, T=80.0, n=800001):
    t = np.linspace(0.0, T, n)
    return np.trapezoid(f(t) * np.exp(-s * t), t)


def check(name, f, F):
    val = lap(f)
    print(f"  {name}: forward={val:.6f}, F(s)={F:.6f}, diff={abs(val-F):.2e}")


print("=== EXP1: simple real poles ===")
print("  F=(3s+5)/((s+1)(s+2)) = 2/(s+1) + 1/(s+2)")
check("f=2e^-t+e^-2t", lambda t: 2 * np.exp(-t) + np.exp(-2 * t),
      (3 * S1 + 5) / ((S1 + 1) * (S1 + 2)))
print("expect: coefficients A=2 at s=-1, B=1 at s=-2")

print()
print("=== EXP2: complex conjugate pair ===")
print("  F=(2s+5)/(s^2+2s+5) = 2(s+1)/((s+1)^2+4) + (3/2)*2/((s+1)^2+4)")
check("f=e^-t(2cos2t+1.5sin2t)", lambda t: np.exp(-t) * (2 * np.cos(2 * t) + 1.5 * np.sin(2 * t)),
      (2 * S1 + 5) / (S1 ** 2 + 2 * S1 + 5))
print("expect: alpha=-1, beta=2; cos coefficient 2, sin coefficient 1.5")

print()
print("=== EXP3: repeated poles ===")
check("f=t e^-t (from 1/(s+1)^2)", lambda t: t * np.exp(-t), 1 / (S1 + 1) ** 2)
check("f=(t^2/2)e^-t (from 1/(s+1)^3)", lambda t: 0.5 * t ** 2 * np.exp(-t), 1 / (S1 + 1) ** 3)
check("f=e^-t+2t e^-t (from (s+3)/(s+1)^2)", lambda t: np.exp(-t) + 2 * t * np.exp(-t),
      (S1 + 3) / (S1 + 1) ** 2)
print("expect: a double pole contributes a t-multiplied term; a triple pole contributes t^2/2")

print()
print("=== EXP4: residue method ===")
F = lambda s: s / ((s + 1) * (s + 2))
res_m1 = -1.0 / (-1.0 + 2.0)
res_m2 = -2.0 / (-2.0 + 1.0)
print(f"  residues of F(s)e^(st) at s=-1 and s=-2: {res_m1:.6f} e^-t, {res_m2:.6f} e^-2t")
check("f=-e^-t+2e^-2t", lambda t: -np.exp(-t) + 2 * np.exp(-2 * t), F(S1))
print("expect: residue sum equals the partial-fraction inverse")

print()
print("=== EXP5: convolution inverse ===")
print("  F=1/((s+2)(s+3)) = L[e^-2t * e^-3t]")
check("f=e^-2t-e^-3t", lambda t: np.exp(-2 * t) - np.exp(-3 * t), 1 / ((S1 + 2) * (S1 + 3)))
print("expect: convolution of the two exponentials gives e^-2t - e^-3t")

print()
print("=== EXP6: improper fraction boundary ===")
print("  F=(2s^2+3s+3)/(s(s+1)) = 2 + 3/s - 2/(s+1)")
print("  inverse: 2 delta(t) + 3 - 2e^-t (the polynomial part gives delta)")
F_imp = (2 * S1 ** 2 + 3 * S1 + 3) / (S1 * (S1 + 1))
F_split = 2 + 3 / S1 - 2 / (S1 + 1)
print(f"  F(0.5+i)={F_imp:.6f}, split form={F_split:.6f}, diff={abs(F_imp-F_split):.2e}")
print("expect: polynomial part must be divided out first; it is not a rational tail")

# ---------------------------------------------------------------------------
# FIG1: pole locations (top) and the corresponding time responses (bottom)
# ---------------------------------------------------------------------------
fig, axs = plt.subplots(2, 3, figsize=(12.0, 6.4))
t = np.linspace(0.0, 4.0, 800)

cols = [
    ([-2.0], "单实极点 $s=-2$", np.exp(-2 * t), "$e^{-2t}$"),
    ([-1.0 + 3.0j, -1.0 - 3.0j], "共轭复极点 $-1\\pm3i$",
     np.exp(-t) * np.cos(3 * t), "$e^{-t}\\cos 3t$"),
    ([-1.0, -1.0], "二重极点 $s=-1$", t * np.exp(-t), "$t e^{-t}$"),
]
for j, (poles, title, resp, label) in enumerate(cols):
    ax = axs[0, j]
    lo = min(p.real for p in poles)
    ax.axvspan(lo, 2.0, color=BLUE, alpha=0.10)
    ax.axhline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=RED, lw=1.0, ls="--")
    for p in poles:
        ax.plot([p.real], [p.imag], "x", color=RED, ms=9, mew=2.0)
    ax.set_xlim(-5, 2)
    ax.set_ylim(-4, 4)
    ax.set_xlabel("$\\sigma$")
    ax.set_ylabel("$i\\omega$")
    ax.set_title(title)
    ax.grid(alpha=0.25)

    ax2 = axs[1, j]
    ax2.plot(t, resp, color=BLUE, lw=1.8)
    ax2.axhline(0, color=GREY, lw=0.6)
    ax2.set_xlim(0, 4)
    ax2.set_xlabel("$t$")
    ax2.set_title(label)
    ax2.grid(alpha=0.25)

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec23_fig1_poles_time.svg"))
fig.savefig(os.path.join(FIGDIR, "lec23_fig1_poles_time.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)