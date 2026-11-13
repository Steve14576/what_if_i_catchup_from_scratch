# 规模纪律：解析式 + 有限次数值积分 + FFT 卷积 + 一张三面板图，目标 < 8 秒。
# 验证第 19 讲：时移/频移、尺度、对偶、微分/积分/频域微分、卷积定理与对偶式、
# 帕塞瓦尔、非零均值积分的 delta 项演示，以及作业中的五个数值核对。
# 运行：uv run --with numpy --with matplotlib python <本文件>
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

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


def conv_same(a, b):
    """FFT-based linear convolution, 'same' mode (center crop), for long arrays."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    n = len(a) + len(b) - 1
    fa = np.fft.rfft(a, n)
    fb = np.fft.rfft(b, n)
    full = np.fft.irfft(fa * fb, n)
    start = (len(b) - 1) // 2
    return full[start:start + len(a)]


# signals: p = rect(t/2) (width 2), q = rect(t) (width 1), tri = Lambda
p = lambda t: (np.abs(t) < 1.0).astype(float)
q = lambda t: (np.abs(t) < 0.5).astype(float)
tri = lambda t: np.maximum(1.0 - np.abs(t), 0.0)
P = lambda w: 2 * sinc(w)
Q = lambda w: sinc(w / 2)

print("=== EXP1: time shift and frequency shift ===")
t0 = 3.0
for w in [0.7, 1.9, 3.3]:
    val = F_num(lambda t: p(t - t0), w)
    exact = P(w) * np.exp(-1j * w * t0)
    print(f"  delay t0=3, w={w}: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
w0 = 5.0
for w in [5.0, 0.0, 7.2]:
    val = F_num(lambda t: p(t) * np.cos(w0 * t), w)
    exact = (P(w - w0) + P(w + w0)) / 2
    print(f"  modulation w0=5, w={w}: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: delay multiplies by exp(-i w t0), |F| unchanged; cos moves spectrum to +-w0")

print()
print("=== EXP2: scaling f(at) <-> F(w/a)/|a| ===")
for w in [1.3, 2.7]:
    val = F_num(lambda t: p(2 * t), w)
    exact = P(w / 2) / 2
    print(f"  a=2 (p(2t)=q), w={w}: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
val = F_num(lambda t: np.where(t <= 0, np.exp(2 * t), 0.0), 1.3)
exact = 1 / (2 - 1.3j)
print(f"  a=-2 (e^{{2t}}u(-t)), w=1.3: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
val = F_num(lambda t: p(t / 2), 0.9)
exact = 2 * P(2 * 0.9)
print(f"  a=1/2 (rect(t/4)), w=0.9: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: 1/|a| factor present; a<0 handled by the same formula")

print()
print("=== EXP3: duality, checked by the inverse transform ===")
wgrid = np.linspace(-1, 1, 200001)
for t in [0.0, 0.7, 1.9]:
    rec = np.trapezoid(np.pi * np.exp(1j * wgrid * t), wgrid) / (2 * np.pi)
    exact = sinc(t)
    print(f"  inverse of pi*rect(w/2) at t={t}: {rec:.9f}, sinc(t)={float(exact.real):.9f}")
tq = np.linspace(-10000, 10000, 400001)
for w in [1.0, 2.0]:
    val = np.trapezoid(np.exp(-1j * w * tq) / (1 + tq ** 2), tq)
    exact = np.pi * np.exp(-abs(w))
    print(f"  1/(1+t^2) at w={w}: numeric={val.real:.9f}, pi*e^-|w|={exact:.9f}, diff={abs(val-exact):.2e}")
print("expect: sinc(t) <-> pi*rect(w/2); 1/(1+t^2) <-> pi*e^-|w| (duality of e^-|t|)")

print()
print("=== EXP4: differentiation, integration, frequency differentiation ===")
ftri = lambda t: q(t + 0.5) - q(t - 0.5)   # = tri'(t), zero mean
for w in [0.7, 1.9, 3.0]:
    val = F_num(tri, w)
    exact = Q(w) ** 2
    print(f"  tri via integration property, w={w}: numeric={val:.6f}, sinc^2(w/2)={exact:.6f}, diff={abs(val-exact):.2e}")
for w in [0.7, 1.9]:
    val = F_num(ftri, w)
    exact = 1j * w * Q(w) ** 2
    print(f"  differentiation property i*w*F[tri], w={w}: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
for w in [0.8, 1.5]:
    val = F_num(lambda t: np.where(t >= 0, t * np.exp(-2 * t), 0.0), w)
    exact = 1 / (2 + 1j * w) ** 2
    print(f"  t*e^-2t u(t), w={w}: numeric={val:.6f}, 1/(2+iw)^2={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: F[tri]=sinc^2(w/2); F[tri']=i*w*F[tri]; F[t e^-2t u]=1/(2+iw)^2")

print()
print("=== EXP5: convolution q*q = tri, and the dual formula ===")
tc = np.linspace(-3, 3, 6001)
dtc = tc[1] - tc[0]
conv = np.convolve(q(tc), q(tc), mode="same") * dtc
for t in [-0.6, 0.0, 0.6]:
    num = np.interp(t, tc, conv)
    print(f"  (q*q)({t}) numeric={num:.6f}, tri={tri(t):.6f}")
val = F_num(lambda t: np.interp(t, tc, conv), 1.1)
exact = Q(1.1) ** 2
print(f"  F[q*q] at w=1.1: numeric={val:.6f}, Q^2={exact:.6f}, diff={abs(val-exact):.2e}")
wg = np.linspace(-300, 300, 300001)
dwg = wg[1] - wg[0]
dual = conv_same(Q(wg).real, Q(wg).real) * dwg / (2 * np.pi)
for w in [0.0, 1.1, 2.5]:
    num = np.interp(w, wg, dual)
    print(f"  (Q*Q)/(2pi) at w={w}: numeric={num:.6f}, Q={float(Q(w).real):.6f}, diff={abs(num-Q(w)):.2e}")
print("expect: q*q=tri; F[q*q]=Q^2; (Q*Q)/(2pi)=Q (dual formula, window +-300, error ~3e-3)")

print()
print("=== EXP6: Parseval ===")
wp = np.linspace(-2000, 2000, 400001)
eq = np.trapezoid(np.abs(Q(wp)) ** 2, wp) / (2 * np.pi)
et = np.trapezoid(np.abs(Q(wp)) ** 4, wp) / (2 * np.pi)
print(f"  q: time energy=1.000000, freq energy={eq:.6f}; integral of sinc^2 = {eq*np.pi:.6f} (expect pi={np.pi:.6f})")
print(f"  tri: time energy={2/3:.6f}, freq energy={et:.6f}; integral of sinc^4 = {et*np.pi:.6f} (expect 2pi/3={2*np.pi/3:.6f})")
print("expect: both energies match; the two sinc integrals follow")

print()
print("=== EXP7: nonzero-mean integration, where the delta term comes from ===")
print("  f=q, F(0)=1, g(t)=integral of q up to t: g(0)=0.5, g(+inf)=1 (not L1)")
W = 400.0
ww = np.linspace(-W, W, 800001)
Qw = Q(ww)
for a in [0.5, 0.1, 0.02]:
    Ga = Qw / (a + 1j * ww)
    I = np.trapezoid(Ga, ww) / (2 * np.pi)
    print(f"  a={a}: symmetric integral of Q/(a+iw) / (2pi) = {I.real:.6f} (expect -> g(0)=0.5)")
Iodd = np.trapezoid((Qw / (1j * ww))[ww != 0], ww[ww != 0]) / (2 * np.pi)
print(f"  symmetric (PV) integral of Q/(iw) / (2pi) = {Iodd.real:.2e} (odd integrand -> 0)")
print(f"  delta term contribution: (1/2pi)*pi*F(0) = {0.5:.6f} -- exactly the missing piece")
print("expect: G = Q/(iw) + pi*delta(w); the delta term carries g(0)=0.5")

print()
print("=== EXP8: homework checks ===")
for w in [1.0, 2.0]:
    val = F_num(lambda t: t * p(t), w)
    exact = 2j * (w * np.cos(w) - np.sin(w)) / w ** 2
    print(f"  hw4 t*rect(t/2), w={w}: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
g5 = lambda t: np.where(t < -1.5, 0.0, np.where(t < -0.5, t + 1.5, np.where(t <= 0.5, 1.0, np.where(t <= 1.5, 1.5 - t, 0.0))))
val = F_num(g5, 1.3)
exact = 2 * np.sin(1.3) * Q(1.3) / 1.3
print(f"  hw5 trapezoid, w=1.3: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
h6 = lambda t: np.where(t <= -0.5, 0.0, np.where(t < 0.5, 1 - np.exp(-(t + 0.5)), np.exp(-t) * (np.exp(0.5) - np.exp(-0.5))))
print(f"  hw6 (q*h)(0.3) = {h6(0.3):.6f} (expect 1-e^-0.8={1-np.exp(-0.8):.6f})")
val = F_num(h6, 1.1)
exact = Q(1.1) / (1 + 1.1j)
print(f"  hw6 F[q*h], w=1.1: numeric={val:.6f}, Q/(1+iw)={exact:.6f}, diff={abs(val-exact):.2e}")
val = F_num(lambda t: tri(t) * np.cos(5 * t), 5.0)
exact = (Q(0.0) ** 2 + Q(10.0) ** 2) / 2
print(f"  hw8 tri*cos5t, w=5: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
val = F_num(lambda t: np.where(t >= 1, (t - 1) * np.exp(-(t - 1)), 0.0), 0.8)
exact = np.exp(-0.8j) / (1 + 0.8j) ** 2
print(f"  hw10 (t-1)e^-(t-1)u(t-1), w=0.8: numeric={val:.6f}, exact={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: all five match the closed forms")

print()
print("=== EXP9: repeated convolution q*q*q = Lambda*q, piecewise quadratic ===")
def triple(t):
    t = np.abs(np.asarray(t, dtype=float))
    return np.where(t <= 0.5, 0.75 - t ** 2, np.where(t <= 1.5, 0.5 * (1.5 - t) ** 2, 0.0))
tc2 = np.linspace(-3, 3, 12001)
dt2 = tc2[1] - tc2[0]
qq = np.convolve(q(tc2), q(tc2), mode="same") * dt2
qqq = np.convolve(qq, q(tc2), mode="same") * dt2
for t in [0.0, 0.4, 0.8, 1.2]:
    num = np.interp(t, tc2, qqq)
    print(f"  (q*q*q)({t}) numeric={num:.6f}, piecewise={triple(t):.6f}")
for w in [0.7, 1.9]:
    val = F_num(lambda t: np.interp(t, tc2, qqq), w)
    exact = Q(w) ** 3
    print(f"  F[Lambda*q] w={w}: numeric={val:.6f}, Q^3={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: triple convolution is piecewise quadratic (C1); spectrum Q^3 decays 1/w^3")

# ---------------------------------------------------------------------------
# FIG1: convolution of q with q -- sliding overlap, triangle, spectra
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4))

tau = np.linspace(-1.6, 1.6, 4000)
tshift = 0.6
axes[0].plot(tau, q(tau), color=BLUE, lw=2.0, label="$q(\\tau)$")
axes[0].plot(tau, q(tshift - tau), color=RED, lw=2.0, ls="--",
             label=f"$q({tshift}-\\tau)$")
ov = tau[(tau > tshift - 0.5) & (tau < 0.5)]
axes[0].fill_between(ov, 0, 1, color=GREEN, alpha=0.3)
axes[0].set_xlim(-1.6, 1.6)
axes[0].set_ylim(-0.1, 1.3)
axes[0].set_xlabel("$\\tau$")
axes[0].set_title(f"翻转—平移—相乘：$t={tshift}$ 时重叠长 $1-t=0.4$")
axes[0].legend(fontsize=9, loc="upper right")
axes[0].grid(alpha=0.25)

tt = np.linspace(-2, 2, 4000)
axes[1].plot(tt, tri(tt), color=GREEN, lw=2.2)
axes[1].plot([tshift], [1 - tshift], "o", color=RED, ms=7)
axes[1].annotate(f"$({tshift},\\ {1-tshift:.1f})$", (tshift, 1 - tshift),
                 textcoords="offset points", xytext=(10, 8), fontsize=10)
axes[1].set_xlim(-2, 2)
axes[1].set_ylim(-0.1, 1.3)
axes[1].set_xlabel("$t$")
axes[1].set_ylabel("$(q*q)(t)$")
axes[1].set_title("卷积结果：三角脉冲 $\\Lambda(t)=1-|t|$")
axes[1].grid(alpha=0.25)

w = np.linspace(-20, 20, 4000)
axes[2].plot(w, Q(w).real, color=BLUE, lw=1.8, label="$Q(\\omega)=\\mathrm{sinc}(\\omega/2)$")
axes[2].plot(w, (Q(w) ** 2).real, color=RED, lw=1.8, label="$Q^2(\\omega)$")
for z in [-2 * np.pi, 2 * np.pi]:
    axes[2].axvline(z, color=GREY, lw=0.7, ls=":")
axes[2].set_xlim(-20, 20)
axes[2].set_ylim(-0.35, 1.15)
axes[2].set_xlabel("$\\omega$")
axes[2].set_title("频谱：卷积定理 $\\mathcal{F}[q*q]=Q^2$")
axes[2].legend(fontsize=9)
axes[2].grid(alpha=0.25)

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec19_fig2_convolution_rect.svg"))
fig.savefig(os.path.join(FIGDIR, "lec19_fig2_convolution_rect.png"), dpi=160)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG2: modulation -- spectrum moved to +-carrier
# ---------------------------------------------------------------------------
fig2, ax2 = plt.subplots(1, 3, figsize=(13.5, 4.2))
tt = np.linspace(-4, 4, 4000)
ax2[0].plot(tt, p(tt), color=BLUE, lw=2.0, label="$p(t)$")
ax2[0].plot(tt, p(tt) * np.cos(5 * tt), color=RED, lw=1.2, label="$p(t)\\cos 5t$")
ax2[0].set_xlim(-4, 4)
ax2[0].set_ylim(-1.2, 1.4)
ax2[0].set_xlabel("$t$")
ax2[0].set_title("时域：乘载波 $\\cos 5t$")
ax2[0].legend(fontsize=9)
ax2[0].grid(alpha=0.25)
ww = np.linspace(-12, 12, 4000)
ax2[1].plot(ww, P(ww).real, color=BLUE, lw=1.8)
ax2[1].axvline(0, color=GREY, lw=0.7, ls=":")
ax2[1].set_xlim(-12, 12)
ax2[1].set_ylim(-0.6, 2.2)
ax2[1].set_xlabel("$\\omega$")
ax2[1].set_title("搬移前：$P(\\omega)=2\\,\\mathrm{sinc}\\,\\omega$")
ax2[1].grid(alpha=0.25)
ax2[2].plot(ww, (P(ww - 5) + P(ww + 5)).real / 2, color=RED, lw=1.8)
for z in [-5, 5]:
    ax2[2].axvline(z, color=GREY, lw=0.7, ls=":")
ax2[2].set_xlim(-12, 12)
ax2[2].set_ylim(-0.6, 2.2)
ax2[2].set_xlabel("$\\omega$")
ax2[2].set_title("搬移后：两个主瓣在 $\\pm 5$，峰值减半")
ax2[2].grid(alpha=0.25)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec19_fig1_modulation.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec19_fig1_modulation.png"), dpi=160)
plt.close(fig2)

# ---------------------------------------------------------------------------
# FIG3: smoothness ladder q -> Lambda -> Lambda*q and spectral decay
# ---------------------------------------------------------------------------
fig3, ax3 = plt.subplots(1, 2, figsize=(11.0, 4.2))
tt3 = np.linspace(-2.5, 2.5, 4000)
ax3[0].plot(tt3, q(tt3), color=BLUE, lw=1.8, label="$q$（有跳变）")
ax3[0].plot(tt3, tri(tt3), color=GREEN, lw=1.8, label="$\\Lambda=q*q$（有折点）")
ax3[0].plot(tt3, triple(tt3), color=RED, lw=1.8, label="$\\Lambda*q$（光滑）")
ax3[0].set_xlim(-2.5, 2.5)
ax3[0].set_ylim(-0.1, 1.2)
ax3[0].set_xlabel("$t$")
ax3[0].set_title("时域：每卷一次光滑一档")
ax3[0].legend(fontsize=9)
ax3[0].grid(alpha=0.25)
ww3 = np.linspace(-30, 30, 6000)
ax3[1].plot(ww3, np.abs(Q(ww3)), color=BLUE, lw=1.5, label="$|Q|\\sim 1/\\omega$")
ax3[1].plot(ww3, np.abs(Q(ww3)) ** 2, color=GREEN, lw=1.5, label="$|Q|^2\\sim 1/\\omega^2$")
ax3[1].plot(ww3, np.abs(Q(ww3)) ** 3, color=RED, lw=1.5, label="$|Q|^3\\sim 1/\\omega^3$")
ax3[1].set_yscale("log")
ax3[1].yaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{v:.0e}"))
ax3[1].set_ylim(1e-4, 2)
ax3[1].set_xlim(-30, 30)
ax3[1].set_xlabel("$\\omega$")
ax3[1].set_title("频谱：衰减逐档加快（log 纵轴）")
ax3[1].legend(fontsize=9)
ax3[1].grid(alpha=0.25, which="both")
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec19_fig3_smoothness.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec19_fig3_smoothness.png"), dpi=160)
plt.close(fig3)

print()
print("[OK] figures written to", FIGDIR)