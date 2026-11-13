# 规模纪律：有限区间数值积分 + 一张双面板 ROC 图，目标 < 6 秒。
# 验证第 22 讲：时移、s 域平移、尺度、微分带初值、s 域微分、卷积、初值/终值。
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
    t = np.linspace(t0, T, n)
    return np.trapezoid(f(t) * np.exp(-s * t), t)


print("=== EXP1: time shift: u(t-2) -> e^{-2s}/s ===")
s1 = 0.5 + 1j
val = lap(lambda t: (t >= 2).astype(float), s1, T=80.0, n=800001)
exact = np.exp(-2 * s1) / s1
print(f"  numeric={val:.6f}, e^-2s/s={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: delay by 2 multiplies F by e^{-2s}; ROC unchanged (sigma>0)")

print()
print("=== EXP2: s-shift: e^{-2t} sin3t -> 3/((s+2)^2+9) ===")
val = lap(lambda t: np.exp(-2 * t) * np.sin(3 * t), s1, T=80.0, n=800001)
exact = 3 / ((s1 + 2) ** 2 + 9)
print(f"  numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: multiplying by e^{-2t} replaces s by s+2; ROC shifts to sigma>-2")

print()
print("=== EXP3: scaling: f(2t) for f=e^{-2t}u(t) -> 1/(s+4) ===")
val = lap(lambda t: np.exp(-4 * t), s1, T=80.0, n=800001)
half = 0.5 * (1 / (s1 / 2 + 2))
exact = 1 / (s1 + 4)
print(f"  numeric={val:.6f}, (1/2)F(s/2)={half:.6f}, 1/(s+4)={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: time compression by 2 scales the ROC and the pole by 2")

print()
print("=== EXP4: derivative with an initial jump ===")
f = lambda t: np.where(t >= 0, np.exp(-3 * t), 2.0)
# f(0^-)=2, f(0^+)=1; f' = -3 e^{-3t}u(t) - delta(t)
tau = 1e-3
dpart = lambda t: -3 * np.where(t >= 0, np.exp(-3 * t), 0.0) - ((np.abs(t) < tau / 2).astype(float) / tau)
val = lap(dpart, s1, T=80.0, n=800001, t0=-tau)
exact = s1 / (s1 + 3) - 2
print(f"  numeric={val:.6f}, sF-f(0^-)={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: L[f']=sF(s)-f(0^-); the 0^- value enters, not the 0^+ value")

print()
print("=== EXP5: s-derivative: t sin3t -> 6s/(s^2+9)^2 ===")
val = lap(lambda t: t * np.sin(3 * t), s1, T=80.0, n=800001)
exact = 6 * s1 / (s1 ** 2 + 9) ** 2
print(f"  numeric={val:.6f}, 6s/(s^2+9)^2={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: L[t f(t)] = -F'(s)")

print()
print("=== EXP6: convolution: e^{-2t}u * e^{-3t}u ===")
val = lap(lambda t: np.exp(-2 * t) - np.exp(-3 * t), s1, T=80.0, n=800001)
exact = 1 / ((s1 + 2) * (s1 + 3))
print(f"  numeric={val:.6f}, 1/((s+2)(s+3))={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: convolution in time multiplies the transforms; the result is e^-2t - e^-3t")

print()
print("=== EXP7: initial/final value and a composite lookup ===")
for s0 in [1e6, 1e-3]:
    print(f"  F=1/(s(s+2)), sF at s={s0:g}: {float((1/(s0*(s0+2))*s0).real):.6f}")
print("  f(0+)=0, f(inf)=0.5 (poles of sF: s=-2, in the left half-plane)")
print("  counterexample F=s/(s^2+1): sF=s^2/(s^2+1) -> 1 at inf, 0 at 0, but cos t has no limit")
val = lap(lambda t: np.exp(-2 * t) * (t + np.cos(3 * t)), s1, T=80.0, n=800001)
exact = 1 / (s1 + 2) ** 2 + (s1 + 2) / ((s1 + 2) ** 2 + 9)
print(f"  L[e^-2t(t+cos3t)] at s=0.5+i: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: composite uses s-shift after the table; ROC is sigma>-2")

# ---------------------------------------------------------------------------
# FIG1: ROC under an s-shift and under time scaling
# ---------------------------------------------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(11.0, 4.2))
for ax, poles, spans, title in [
    (axs[0], [-2.0, 1.0], [(-2.0, 4.0, BLUE), (1.0, 4.0, RED)], "s 域平移：$e^{3t}f$ 使极点与 ROC 右移 3"),
    (axs[1], [-2.0, -4.0], [(-2.0, 4.0, BLUE), (-4.0, 4.0, GREEN)], "尺度：$f(2t)$ 使极点与 ROC 按 2 缩放"),
]:
    for lo, hi, col in spans:
        ax.axvspan(lo, hi, color=col, alpha=0.10)
    ax.axhline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=RED, lw=1.0, ls="--")
    for p in poles:
        ax.plot([p], [0], "x", color=RED, ms=9, mew=2.0)
        ax.text(p, -0.55, f"$s={p:g}$", color=RED, ha="center", fontsize=9)
    ax.set_xlim(-6, 4)
    ax.set_ylim(-3, 3)
    ax.set_xlabel("$\\sigma$")
    ax.set_ylabel("$i\\omega$")
    ax.set_title(title)
    ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec22_fig1_roc_shift.svg"))
fig.savefig(os.path.join(FIGDIR, "lec22_fig1_roc_shift.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)