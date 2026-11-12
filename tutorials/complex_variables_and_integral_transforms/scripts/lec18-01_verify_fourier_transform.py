# 规模纪律：解析式 + 有限次数值积分 + 一张双面板图，目标 < 8 秒。
# 验证第 18 讲：级数到变换的过渡、矩形脉冲的 sinc、单边指数、绝对可积的反例、
# 共轭对称与实虚性、时宽频宽，以及作业中的双边指数、时移矩形、1/(1+t^2)。
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


def sinc(x):
    """sin(x)/x with the removable singularity at 0 filled in (scalar or array)."""
    x = np.asarray(x, dtype=complex)
    safe = np.abs(x) > 1e-12
    denom = np.where(safe, x, 1.0 + 0j)
    return np.where(safe, np.sin(x) / denom, 1.0 + 0j)


def F_num(f, w, span=40.0, n=400001):
    """Numerical Fourier transform at a scalar or array of angular frequencies."""
    t = np.linspace(-span, span, n)
    vals = np.atleast_1d(w)
    out = np.array([np.trapezoid(f(t) * np.exp(-1j * wi * t), t) for wi in vals])
    return out if np.ndim(w) else out[0]


print("=== EXP1: from Fourier series to the transform (T -> infinity) ===")
print("  single pulse of width 1: F(w) = 2 sin(w/2)/w; periodic train: c_n = F(n w0)/T")
for T in [10.0, 20.0, 40.0]:
    w0 = 2 * np.pi / T
    print(f"  T={T:4.0f}: line spacing dw = 2*pi/T = {w0:.6f}")
    for n in [1, 2, 3]:
        wn = n * w0
        cn = F_num(lambda t: ((np.abs(t) < 0.5).astype(float)), wn, span=T) / T
        print(f"    n={n}: T*c_n={T*cn:.6f}, F(n*w0)={2*np.sin(wn/2)/wn:.6f}")
print("expect: T*c_n equals F at the sample frequencies; spacing shrinks as T grows")

print()
print("=== EXP2: rectangular pulse tau=2, F(w)=tau*sinc(w*tau/2) ===")
rect2 = lambda t: ((np.abs(t) < 1.0).astype(float))
for w in [0.0, 0.5, 1.0, np.pi / 2, np.pi, 2 * np.pi]:
    val = F_num(rect2, w)
    exact = 2 * sinc(w * 2 / 2) if w != 0 else 2.0
    print(f"  w={w:7.4f}: numeric={val.real:+.9f}{val.imag:+.2e}j, "
          f"2*sinc(w)={exact.real if np.ndim(exact) else exact:+.9f}")
print(f"  F(0)={F_num(rect2, 0.0).real:.6f} (expect tau=2); first zeros at w=+-pi={np.pi:.6f}")
print("expect: real, even, peak 2, zeros at multiples of pi")

print()
print("=== EXP3: single-sided exponential e^{-3t}u(t), F=1/(3+iw) ===")
f1 = lambda t: np.where(t >= 0, np.exp(-3 * t), 0.0)
for w in [0.0, 1.0, 2.0, 5.0]:
    val = F_num(f1, w)
    exact = 1 / (3 + 1j * w)
    print(f"  w={w:.1f}: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: matches 1/(3+iw); |F| decreases, phase goes to -90 deg")

print()
print("=== EXP4: existence needs absolute integrability ===")
for R in [10.0, 100.0, 1000.0]:
    print(f"  f=1: integral of |f| over [-R,R] = {2*R:.1f}")
t100 = np.linspace(-100, 100, 400001)
print(f"  f=cos t: integral of |cos t| over [-100,100] = {np.trapezoid(np.abs(np.cos(t100)), t100):.1f}")
print(f"  rect(t/2): integral of |f| over [-100,100] = {np.trapezoid(np.abs(rect2(t100)), t100):.1f}")
print("expect: 1 and cos have divergent absolute integrals; the pulse has finite integral 2")

print()
print("=== EXP5: conjugate symmetry and real/imaginary parity ===")
for w in [0.7, 1.9]:
    a = F_num(rect2, w)
    b = F_num(rect2, -w)
    print(f"  rect: F(w)={a:.6f}, F(-w)={b:.6f}, conj symmetry diff={abs(F_num(rect2, w)-np.conj(F_num(rect2, -w))):.2e}")
odd = lambda t: t * np.exp(-np.abs(t))
for w in [0.7, 1.9]:
    val = F_num(odd, w)
    exact = -4j * w / (1 + w ** 2) ** 2
    print(f"  odd f=t*exp(-|t|): w={w}: F={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: real f gives F(-w)=conj F(w); real even -> real even; real odd -> purely imaginary odd")

print()
print("=== EXP6: time width vs frequency width ===")
for tau in [0.5, 1.0, 2.0]:
    print(f"  tau={tau}: F(0)={tau}, first zero=2*pi/tau={2*np.pi/tau:.6f}, "
          f"main-lobe width=4*pi/tau={4*np.pi/tau:.6f}, product tau*width={tau*4*np.pi/tau:.6f}")
print("expect: narrower pulse -> lower peak, wider main lobe; product is always 4*pi")

print()
print("=== EXP7: homework checks ===")
bi = lambda t: np.exp(-2 * np.abs(t))
for w in [0.0, 1.0, 2.0]:
    val = F_num(bi, w)
    exact = 4 / (4 + w ** 2)
    print(f"  e^-2|t| at w={w}: numeric={val.real:.9f}, exact={exact:.9f}, diff={abs(val-exact):.2e}")
shift = lambda t: ((np.abs(t - 2) < 1).astype(float))
for w in [0.0, 1.0]:
    val = F_num(shift, w)
    exact = 2 * sinc(w) * np.exp(-2j * w)
    print(f"  rect((t-2)/2) at w={w}: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
tq = np.linspace(-10000, 10000, 400001)
for w in [0.0, 1.0, 2.0]:
    val = np.trapezoid(np.exp(-1j * w * tq) / (1 + tq ** 2), tq)
    exact = np.pi * np.exp(-abs(w))
    print(f"  1/(1+t^2) at w={w}: numeric={val.real:.9f}, exact={exact:.9f}, diff={abs(val-exact):.2e}")
print("expect: all three match the closed forms")

# ---------------------------------------------------------------------------
# FIG1: three rectangular pulses and their sinc spectra
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.6))

t = np.linspace(-3, 3, 4000)
for tau, col in [(2.0, BLUE), (1.0, GREEN), (0.5, RED)]:
    axes[0].plot(t, (np.abs(t) < tau / 2).astype(float), color=col, lw=2.0,
                 label=f"$\\tau={tau}$")
axes[0].set_xlim(-3, 3)
axes[0].set_ylim(-0.1, 1.35)
axes[0].set_xlabel("$t$")
axes[0].set_ylabel("$f(t)$")
axes[0].set_title("矩形脉冲：脉宽 $\\tau$ 越小，越窄")
axes[0].legend(fontsize=9)
axes[0].grid(alpha=0.25)

w = np.linspace(-20, 20, 4000)
for tau, col in [(2.0, BLUE), (1.0, GREEN), (0.5, RED)]:
    spec = tau * sinc(w * tau / 2)
    axes[1].plot(w, spec.real, color=col, lw=1.8, label=f"$\\tau={tau}$")
axes[1].axhline(0, color=GREY, lw=0.6)
axes[1].set_xlim(-20, 20)
axes[1].set_ylim(-1.0, 2.2)
axes[1].set_xlabel("$\\omega$")
axes[1].set_ylabel("$F(\\omega)$")
axes[1].set_title("频谱：$F(\\omega)=\\tau\\,\\sin(\\omega\\tau/2)/(\\omega\\tau/2)$")
axes[1].legend(fontsize=9)
axes[1].grid(alpha=0.25)

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec18_fig1_rect_sinc.svg"))
fig.savefig(os.path.join(FIGDIR, "lec18_fig1_rect_sinc.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
