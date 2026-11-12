# 规模纪律：解析求和 + 一次数值积分扫描 + 一张双面板图，目标 < 8 秒。
# 验证第 17 讲：三角函数系正交性、方波系数、部分和与吉布斯过冲、
# 复指数系数、单边与双边幅度谱、帕塞瓦尔，以及作业中三个波形的系数。
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


print("=== EXP1: orthogonality of {1, cos nt, sin nt} on [0, 2*pi] ===")
th = np.linspace(0, 2 * np.pi, 200001)
for n, m in [(1, 1), (1, 2), (3, 5)]:
    c = np.trapezoid(np.cos(n * th) * np.cos(m * th), th)
    s = np.trapezoid(np.sin(n * th) * np.sin(m * th), th)
    cs = np.trapezoid(np.cos(n * th) * np.sin(m * th), th)
    print(f"  n={n}, m={m}: int cos*cos={c:+.6f}, int sin*sin={s:+.6f}, int cos*sin={cs:+.6f}")
print(f"  n=1: int sin^2 = {np.trapezoid(np.sin(th) ** 2, th):.6f} (expect pi = {np.pi:.6f})")
print(f"  n=1: int cos^2 = {np.trapezoid(np.cos(th) ** 2, th):.6f} (expect pi = {np.pi:.6f})")
print("expect: different indices give 0; equal indices give pi")

print()
print("=== EXP2: square wave (amplitude 1), Fourier coefficients ===")
T = 2 * np.pi
f_sq = np.sign(np.sin(th))
for n in [1, 2, 3, 4, 5]:
    an = (2 / T) * np.trapezoid(f_sq * np.cos(n * th), th)
    bn = (2 / T) * np.trapezoid(f_sq * np.sin(n * th), th)
    print(f"  n={n}: a_n={an:+.6f}, b_n={bn:+.6f}, 4/(n*pi)={4/(n*np.pi):.6f}")
print("expect: a_n = 0; b_n = 4/(n*pi) for odd n, 0 for even n")

print()
print("=== EXP3: partial sums and the Gibbs overshoot ===")
def square_partial(x, N):
    out = np.zeros_like(x)
    for n in range(1, N + 1, 2):
        out += 4 / (n * np.pi) * np.sin(n * x)
    return out

xs = np.linspace(1e-6, np.pi - 1e-6, 20001)
for N in [1, 3, 9, 25, 99, 199]:
    y = square_partial(xs, N)
    err = np.sqrt(np.mean((y - 1.0) ** 2))
    print(f"  N={N:3d}: max={y.max():.6f}, overshoot={y.max()-1:+.6f}, RMS error={err:.6f}")
xg = np.linspace(1e-9, np.pi, 200001)
gibbs = (2 / np.pi) * np.trapezoid(np.sin(xg) / xg, xg)
print(f"  Gibbs constant 2/pi * Si(pi) = {gibbs:.6f}")
print("expect: overshoot stays near 0.179 (about 9% of the jump 2), RMS error decreases")

print()
print("=== EXP4: complex coefficients c_n of the square wave ===")
for n in [1, 2, 3, 5]:
    cn = (1 / T) * np.trapezoid(f_sq * np.exp(-1j * n * th), th)
    predicted = (1 - (-1) ** n) / (np.pi * 1j * n)
    print(f"  n={n}: c_n={cn:.6f}, predicted={predicted:.6f}, |c_n|={abs(cn):.6f}")
print("expect: c_n = -2i/(n*pi) for odd n; c_n = 0 for even n")

print()
print("=== EXP5: single-sided vs double-sided amplitude spectrum ===")
for n in [1, 3, 5]:
    A_n = 4 / (n * np.pi)
    print(f"  n={n}: single-sided A_n={A_n:.6f}, 2*|c_n|={2*2/(n*np.pi):.6f}, phase={np.degrees(np.angle(-2j/(n*np.pi))):.2f} deg")
print("expect: A_n = 2|c_n| for n >= 1; phase = -90 deg")

print()
print("=== EXP6: Parseval for the square wave ===")
power_time = (1 / T) * np.trapezoid(f_sq ** 2, th)
partial = 0.0
for n in range(1, 20001):
    if n % 2 == 1:
        partial += 2 * (2 / (n * np.pi)) ** 2
print(f"  time-domain mean square = {power_time:.9f}")
print(f"  sum over +-n of |c_n|^2 (20000 terms) = {partial:.9f}")
print(f"  single-sided form A0^2/4 + sum A_n^2/2 = {sum((4/(n*np.pi))**2/2 for n in range(1,20001,2)):.9f}")
print("expect: all three equal 1")

print()
print("=== EXP7: homework waveform checks ===")
t = np.linspace(-np.pi, np.pi, 200001)
saw = t.copy()
for n in [1, 2, 3, 4]:
    bn = (1 / np.pi) * np.trapezoid(saw * np.sin(n * t), t)
    print(f"  sawtooth n={n}: b_n={bn:+.6f}, 2*(-1)^(n+1)/n={2*(-1)**(n+1)/n:+.6f}")
half = np.abs(np.sin(t))
for n in [1, 2, 3]:
    an = (1 / np.pi) * np.trapezoid(half * np.cos(2 * n * t), t)
    print(f"  |sin t| n={n}: a_n={an:+.6f}, -4/(pi*(4n^2-1))={-4/(np.pi*(4*n*n-1)):+.6f}")
tri = 1 - np.abs(t) / np.pi
for n in [0, 1, 2, 3]:
    an = (1 / np.pi) * np.trapezoid(tri * np.cos(n * t), t)
    predicted = 1.0 if n == 0 else (4 / (np.pi ** 2 * n ** 2) if n % 2 == 1 else 0.0)
    print(f"  triangle n={n}: a_n={an:+.6f}, predicted={predicted:+.6f}")
print("expect: all three match the closed forms")

# ---------------------------------------------------------------------------
# FIG1: square wave partial sums and its amplitude spectrum
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.6))

x = np.linspace(-np.pi, np.pi, 2000)
axes[0].plot(x, np.sign(np.sin(x)), color=GREY, lw=2.4, label="方波")
for N, col in [(1, BLUE), (3, GREEN), (9, RED)]:
    axes[0].plot(x, square_partial(x, N), color=col, lw=1.6, label=f"N={N}")
axes[0].axhline(1.0, color=GREY, lw=0.6, ls="--")
peak = square_partial(xs, 9)
axes[0].plot([xs[np.argmax(peak)]], [peak.max()], "o", color=RED, ms=4)
axes[0].text(xs[np.argmax(peak)] + 0.12, peak.max() + 0.03, "过冲", color=RED, fontsize=8.5)
axes[0].set_xlim(-np.pi, np.pi)
axes[0].set_ylim(-1.45, 1.45)
axes[0].set_xlabel("$t$")
axes[0].set_ylabel("部分和")
axes[0].set_title("方波与部分和：跳变处有过冲")
axes[0].legend(fontsize=8, loc="upper left", framealpha=0.9)
axes[0].grid(alpha=0.25)

ns = np.arange(1, 16)
A = np.where(ns % 2 == 1, 4 / (ns * np.pi), 0.0)
c = np.where(ns % 2 == 1, 2 / (ns * np.pi), 0.0)
axes[1].vlines(ns, 0, A, color=BLUE, lw=1.8, label="单边幅度 $A_n$")
axes[1].plot(ns, A, "o", color=BLUE, ms=4)
axes[1].vlines(-ns, 0, c, color=RED, lw=1.8, label="双边幅度 $|c_n|$")
axes[1].plot(-ns, c, "o", color=RED, ms=4)
axes[1].axhline(0, color=GREY, lw=0.6)
axes[1].set_xlim(-16, 16)
axes[1].set_ylim(0, 1.45)
axes[1].set_xlabel("谐波次数 $n$")
axes[1].set_ylabel("幅度")
axes[1].set_title("方波幅度谱：只含奇次谐波")
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.25)

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec17_fig1_square_spectrum.svg"))
fig.savefig(os.path.join(FIGDIR, "lec17_fig1_square_spectrum.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)
