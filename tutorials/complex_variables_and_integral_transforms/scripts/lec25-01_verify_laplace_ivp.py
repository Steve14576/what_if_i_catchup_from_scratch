# 规模纪律：解析解回代 + 一张 1x2 极点/阶跃图，目标 < 6 秒。
# 验证第 25 讲：三步法、RLC 三种阻尼、冲激输入、延迟输入、经典法对照。
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
ORANGE = "#dd6b20"
GREY = "#718096"
S1 = 0.5 + 1j


def lap(f, s=S1, T=80.0, n=800001, t0=0.0):
    t = np.linspace(t0, T, n)
    return np.trapezoid(f(t) * np.exp(-s * t), t)


print("=== EXP1: y'+2y=e^-t, y(0)=2 via Laplace ===")
t = np.linspace(0.0, 6.0, 601)
y = np.exp(-t) + np.exp(-2 * t)
res = np.max(np.abs(-np.exp(-t) - 2 * np.exp(-2 * t) + 2 * y - np.exp(-t)))
print(f"  y=e^-t+e^-2t: max residual={res:.2e}, y(0)={y[0]:.6f}")
print("  Y=(2+1/(s+1))/(s+2)=1/(s+1)+1/(s+2)")
print("expect: residual 0 and y(0)=2; the initial value entered at the transform step")

print()
print("=== EXP2: y''+3y'+2y=0, y(0)=1, y'(0)=0 via Laplace ===")
y = 2 * np.exp(-t) - np.exp(-2 * t)
res = np.max(np.abs((2 * np.exp(-t) - 4 * np.exp(-2 * t)) + 3 * (-2 * np.exp(-t) + 2 * np.exp(-2 * t)) + 2 * y))
print(f"  y=2e^-t-e^-2t: max residual={res:.2e}, y(0)={y[0]:.6f}, y'(0)={-2+2:.6f}")
print("  Y=(s+3)/((s+1)(s+2))=2/(s+1)-1/(s+2)")
print("expect: residual 0 and both initial conditions satisfied")

print()
print("=== EXP3: RLC step response, L=C=1, E=1, three damping cases ===")


def step_response(R, t):
    if R > 2:
        r1 = (-R + np.sqrt(R ** 2 - 4)) / 2
        r2 = (-R - np.sqrt(R ** 2 - 4)) / 2
        A = 1 / (r1 * (r1 - r2))
        B = 1 / (r2 * (r2 - r1))
        return 1 + A * np.exp(r1 * t) + B * np.exp(r2 * t)
    if abs(R - 2) < 1e-12:
        return 1 - np.exp(-t) * (1 + t)
    zeta = R / 2
    wd = np.sqrt(1 - zeta ** 2)
    return 1 - np.exp(-zeta * t) * (np.cos(wd * t) + zeta / wd * np.sin(wd * t))


for R in [4.0, 2.0, 0.4]:
    y = step_response(R, t)
    yd = np.gradient(y, t)
    ydd = np.gradient(yd, t)
    res = np.max(np.abs((ydd + R * yd + y - 1)[2:-2]))
    label = "over" if R > 2 else ("critical" if R == 2 else "under")
    print(f"  R={R}: {label}, max ODE residual={res:.2e}, y(6)={y[-1]:.6f}")
y_under = step_response(0.4, t)
print(f"  underdamped overshoot: max y={y_under.max():.4f}, peak t={t[y_under.argmax()]:.3f}")

print()
print("=== EXP4: impulse input y''+3y'+2y=delta(t), zero initial ===")
y = np.exp(-t) - np.exp(-2 * t)
yd = -np.exp(-t) + 2 * np.exp(-2 * t)
print(f"  y(0+)={y[0]:.6f}, y'(0+)={yd[0]:.6f}; forward transform={lap(lambda tt: np.exp(-tt) - np.exp(-2 * tt)):.6f}")
print(f"  1/((s+1)(s+2)) at s=0.5+i = {1/((S1+1)*(S1+2)):.6f}")
print("expect: zero initial state, but the impulse creates y'(0+)=1; Y=H(s)")

print()
print("=== EXP5: delayed step y'+2y=u(t-2), y(0)=0 ===")
y = lambda tt: np.where(tt >= 2, 0.5 * (1 - np.exp(-2 * (tt - 2))), 0.0)
print(f"  y(1)={float(y(1.0)):.6f}, y(3)={float(y(3.0)):.6f}, y(6)={float(y(6.0)):.6f}")
val = lap(lambda tt: y(tt), T=80.0)
exact = np.exp(-2 * S1) / (S1 * (S1 + 2))
print(f"  forward transform={val:.6f}, e^-2s/[s(s+2)]={exact:.6f}, diff={abs(val-exact):.2e}")
print("expect: zero before t=2; after t=2 rises to 0.5; inverse carries u(t-2)")

print()
print("=== EXP6: classic vs Laplace, same IVP y'+2y=e^-t, y(0)=2 ===")
print("  classic: y=e^-t+Ce^-2t; y(0)=2 -> C=1 -> e^-t+e^-2t")
print("  Laplace: Y=(2+1/(s+1))/(s+2)=1/(s+1)+1/(s+2) -> e^-t+e^-2t")
print("expect: identical coefficients; Laplace folds the initial condition into algebra")

print()
print("=== EXP7: homework checks ===")
y = np.cos(2 * t) + np.sin(2 * t)
res = np.max(np.abs(-4 * y + 4 * y))
print(f"  y''+4y=0, y=cos2t+sin2t: max residual={res:.2e}, y(0)={y[0]:.6f}, y'(0)={2*np.cos(0.0):.6f}")
y = t * np.exp(-2 * t)
res = np.max(np.abs((4 * t - 4) * np.exp(-2 * t) + 4 * (-2 * t + 1) * np.exp(-2 * t) + 4 * y))
print(f"  y''+4y'+4y=0, y=t e^-2t: max residual={res:.2e}")

# ---------------------------------------------------------------------------
# FIG1: poles (left) and step responses (right) for the three damping cases
# ---------------------------------------------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.6))
t_fig = np.linspace(0.0, 15.0, 1500)

ax = axs[0]
for R, col in [(4.0, BLUE), (2.0, GREEN), (0.4, RED)]:
    if R > 2:
        r1 = (-R + np.sqrt(R ** 2 - 4)) / 2
        r2 = (-R - np.sqrt(R ** 2 - 4)) / 2
        ax.plot([r1, r2], [0, 0], "x", color=col, ms=9, mew=2.0, label=f"R={R:g}")
    elif R == 2:
        ax.plot([-1.0], [0], "x", color=col, ms=11, mew=2.5, label=f"R={R:g}")
    else:
        zeta = R / 2
        wd = np.sqrt(1 - zeta ** 2)
        ax.plot([-zeta, -zeta], [wd, -wd], "x", color=col, ms=9, mew=2.0, label=f"R={R:g}")
ax.axhline(0, color=GREY, lw=0.6)
ax.axvline(0, color=GREY, lw=0.6)
ax.axvline(0, color=GREY, lw=1.0, ls="--")
ax.set_xlim(-4.5, 0.5)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel("$\\sigma$")
ax.set_ylabel("$i\\omega$")
ax.set_title("三种阻尼的极点")
ax.legend(fontsize=9, loc="lower left")
ax.grid(alpha=0.25)

ax2 = axs[1]
for R, col in [(4.0, BLUE), (2.0, GREEN), (0.4, RED)]:
    ax2.plot(t_fig, step_response(R, t_fig), color=col, lw=1.8, label=f"R={R:g}")
ax2.axhline(1.0, color=GREY, lw=0.8, ls=":")
ax2.set_xlim(0, 15)
ax2.set_ylim(0, 1.7)
ax2.set_xlabel("$t$")
ax2.set_ylabel("$u_C(t)$")
ax2.set_title("单位阶跃响应：过阻尼 / 临界 / 欠阻尼")
ax2.legend(fontsize=9)
ax2.grid(alpha=0.25)

fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec25_fig1_damping.svg"))
fig.savefig(os.path.join(FIGDIR, "lec25_fig1_damping.png"), dpi=160)
plt.close(fig)

print()
print("[OK] figures written to", FIGDIR)