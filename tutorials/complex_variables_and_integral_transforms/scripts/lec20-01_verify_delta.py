# 规模纪律：解析式 + 有限次数值积分 + 三张多面板图，目标 < 8 秒。
# 验证第 20 讲：单位面积脉冲极限、筛选与尺度、余弦谱的冲激面积、
# 周期脉冲串的 2*pi*c_n、抽样混叠、理想低通插值性质。
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
    t = np.linspace(-span, span, n)
    vals = np.atleast_1d(w)
    out = np.array([np.trapezoid(f(t) * np.exp(-1j * wi * t), t) for wi in vals])
    return out if np.ndim(w) else out[0]


def p_tau(tau):
    """Unit-area rectangle: height 1/tau, width tau."""
    return lambda t: (np.abs(t) < tau / 2).astype(float) / tau


print("=== EXP1: unit-area rectangle -> delta ===")
print("  tau -> 0: area stays 1, height 1/tau grows, spectrum sinc(w*tau/2) -> 1")
for tau in [1.0, 0.5, 0.2, 0.05]:
    val = F_num(p_tau(tau), 3.0)
    exact = sinc(3.0 * tau / 2)
    print(f"  tau={tau:4.2f}: height={1/tau:7.2f}, F(3)={val.real:.6f}, sinc(3tau/2)={float(exact.real):.6f}, diff={abs(val-exact):.2e}")
print("expect: F(3) -> 1 as tau -> 0 (the delta has a flat spectrum)")

print()
print("=== EXP2: sifting and scaling ===")
tt = np.linspace(-10, 10, 1000001)
for tau in [0.1, 0.02]:
    d = p_tau(tau)(tt - 2.0)
    val = np.trapezoid((tt ** 2 + 1) * d, tt)
    print(f"  tau={tau}: integral of (t^2+1) delta(t-2) = {val:.6f} (expect 5)")
for tau in [0.1, 0.02]:
    d2 = p_tau(tau)(2 * tt - 4.0)
    val = np.trapezoid(d2, tt)
    print(f"  tau={tau}: integral of delta(2t-4) = {val:.6f} (expect 0.5 = 1/|2|)")
print("expect: sifting picks the value at t=2; delta(2t-4)=delta(t-2)/2")

print()
print("=== EXP3: cosine spectrum, impulse area pi at +-w0 ===")
w0 = 3.0
for a in [0.5, 0.1, 0.02]:
    wl = np.linspace(w0 - 1, w0 + 1, 200001)
    G = a / (a ** 2 + (wl - w0) ** 2) + a / (a ** 2 + (wl + w0) ** 2)
    area = np.trapezoid(G, wl)
    wt = np.linspace(-6, 6, 240001)
    Gt = a / (a ** 2 + (wt - w0) ** 2) + a / (a ** 2 + (wt + w0) ** 2)
    total = np.trapezoid(Gt, wt)
    print(f"  a={a}: lobe area={area:.6f} (expect pi={np.pi:.6f}), total={total:.6f} (expect 2pi={2*np.pi:.6f})")
print("expect: e^{-a|t|}cos(w0 t) -> cosine; its spectrum converges to pi[delta(w-w0)+delta(w+w0)]")

print()
print("=== EXP4: periodic rectangular pulse train, 2*pi*c_n ===")
T0 = 2 * np.pi
f1 = lambda t: (np.abs(t) < np.pi / 2).astype(float)
for n in [1, 3, 5]:
    cn = F_num(f1, n, span=np.pi) / T0
    exact = np.sin(n * np.pi / 2) / (n * np.pi)
    print(f"  n={n}: c_n={cn.real:.6f}, exact={exact:.6f}, 2*pi*c_n={2*np.pi*cn.real:.6f}, pi*sinc(n*pi/2)={float((np.pi*sinc(n*np.pi/2)).real):.6f}")
print("expect: 2*pi*c_n = pi*sinc(n*pi/2): 2, -2/3, 2/5 ...")

print()
print("=== EXP5: sampling and aliasing ===")
f0, fs = 10.0, 15.0
print("  f0=10 Hz, fs=15 Hz (< 2*f0):")
for n in range(5):
    x1 = np.cos(2 * np.pi * f0 * n / fs)
    x2 = np.cos(2 * np.pi * 5.0 * n / fs)
    print(f"    n={n}: cos(2pi*10*n/15)={x1:+.6f}, cos(2pi*5*n/15)={x2:+.6f}, same={abs(x1-x2)<1e-12}")
print(f"  alias frequency = |f0 - fs| = {abs(f0-fs):.1f} Hz")
print("  f0=10 Hz, fs=25 Hz (> 2*f0): Nyquist=12.5 Hz, no aliasing")
print("expect: samples of 10 Hz at 15 Hz coincide with samples of 5 Hz at 15 Hz")

print()
print("=== EXP6: ideal low-pass interpolation property ===")
wc = 12.5
h = lambda t: sinc(wc * t)
for n in [-2, -1, 0, 1, 2]:
    tn = n * np.pi / wc
    print(f"  h(n*pi/wc), n={n}: {float(h(tn).real):.9f} (expect 1 at n=0, 0 otherwise)")
print("expect: sinc(wc t) interpolates exactly at the sample points (Ts=pi/wc)")

# ---------------------------------------------------------------------------
# FIG1: unit-area rectangle -> delta, and spectra -> 1
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.2))
t = np.linspace(-0.6, 0.6, 6000)
for tau, col in [(1.0, BLUE), (0.5, GREEN), (0.2, RED)]:
    axes[0].plot(t, p_tau(tau)(t), color=col, lw=1.8, label=f"$\\tau={tau}$")
axes[0].set_xlim(-0.6, 0.6)
axes[0].set_ylim(0, 5.6)
axes[0].set_xlabel("$t$")
axes[0].set_ylabel("$p_\\tau(t)$")
axes[0].set_title("单位面积矩形：宽 $\\tau$，高 $1/\\tau$")
axes[0].legend(fontsize=9)
axes[0].grid(alpha=0.25)

w = np.linspace(-20, 20, 4000)
for tau, col in [(1.0, BLUE), (0.5, GREEN), (0.2, RED)]:
    axes[1].plot(w, sinc(w * tau / 2).real, color=col, lw=1.6, label=f"$\\tau={tau}$")
axes[1].axhline(1, color=GREY, lw=0.7, ls=":")
axes[1].set_xlim(-20, 20)
axes[1].set_ylim(-0.3, 1.15)
axes[1].set_xlabel("$\\omega$")
axes[1].set_title("频谱：$F[p_\\tau]=\\mathrm{sinc}(\\omega\\tau/2)\\to1$")
axes[1].legend(fontsize=9)
axes[1].grid(alpha=0.25)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec20_fig1_delta_limit.svg"))
fig.savefig(os.path.join(FIGDIR, "lec20_fig1_delta_limit.png"), dpi=160)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG2: periodic pulse train -- impulse strengths 2*pi*c_n
# ---------------------------------------------------------------------------
fig2, ax = plt.subplots(figsize=(9.6, 4.4))
ns = np.arange(-7, 8)
strengths = np.array([float((np.pi * sinc(n * np.pi / 2)).real) for n in ns])
mask = np.abs(strengths) > 1e-9
ax.stem(ns[mask], strengths[mask], linefmt="C0-", markerfmt="C0o", basefmt="k-")
we = np.linspace(-7.5, 7.5, 3000)
ax.plot(we, (np.pi * sinc(we * np.pi / 2)).real, color=RED, lw=1.2, ls="--", label="包络 $\\pi\\,\\mathrm{sinc}(\\omega\\pi/2)$")
ax.axhline(0, color=GREY, lw=0.7)
ax.set_xlim(-7.5, 7.5)
ax.set_ylim(-3.6, 3.6)
ax.set_xlabel("$\\omega$")
ax.set_ylabel("$2\\pi c_n$")
ax.set_title("周期矩形脉冲串：等间隔冲激，强度 $2\\pi c_n$")
ax.legend(fontsize=9)
ax.grid(alpha=0.25)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec20_fig2_periodic_train.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec20_fig2_periodic_train.png"), dpi=160)
plt.close(fig2)

# ---------------------------------------------------------------------------
# FIG3: sampling spectra -- no overlap vs aliasing
# ---------------------------------------------------------------------------
fig3, axs = plt.subplots(1, 2, figsize=(12.0, 4.2))


def copies(w, ws, n_max=3):
    total = np.zeros_like(w)
    for n in range(-n_max, n_max + 1):
        total += (np.abs(w - n * ws) <= 10).astype(float)
    return total


ww = np.linspace(-45, 45, 9000)
axs[0].plot(ww, copies(ww, 25.0), color=BLUE, lw=1.6)
for z in [-25, 0, 25]:
    axs[0].axvline(z, color=GREY, lw=0.7, ls=":")
axs[0].set_xlim(-45, 45)
axs[0].set_ylim(-0.1, 1.4)
axs[0].set_xlabel("$\\omega$")
axs[0].set_title("$f_s=25>2f_m=20$：副本不重叠，可恢复")
axs[0].grid(alpha=0.25)

axs[1].plot(ww, copies(ww, 15.0), color=RED, lw=1.6)
for z in [-30, -15, 0, 15, 30]:
    axs[1].axvline(z, color=GREY, lw=0.7, ls=":")
for z in [-10, 10]:
    axs[1].axvline(z, color=GREEN, lw=0.8, ls="--")
axs[1].annotate("10 的像折到 5", xy=(5, 2.0), xytext=(8, 2.25), fontsize=10,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
axs[1].set_xlim(-45, 45)
axs[1].set_ylim(-0.1, 2.6)
axs[1].set_xlabel("$\\omega$")
axs[1].set_title("$f_s=15<2f_m$：副本重叠，混叠")
axs[1].grid(alpha=0.25)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec20_fig3_sampling.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec20_fig3_sampling.png"), dpi=160)
plt.close(fig3)

print()
print("[OK] figures written to", FIGDIR)