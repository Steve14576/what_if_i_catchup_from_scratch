# =====================================================================
# lec14-01 阻抗与正弦稳态分析：并联主例、导纳核对、时域对照
#          （第 14 讲 §1-§2 数值实验；图 1 电路、图 2 相量图、图 3 阻抗三角形）
# 规模纪律：总耗时 < 10 秒（RK4 dt=1us + 三张图）。
#
# 主例：U = 50∠0° V（有效值 50 V，w = 1000）；
#   支路 1：R=3 + L=4 mH（wL = 4 ohm）-> Z1 = 3+4j = 5∠53.13°
#   支路 2：R=3 + C=250 uF（1/wC = 4 ohm）-> Z2 = 3-4j = 5∠-53.13°
#   两支并联：Z总 = Z1||Z2 = 25/6∠0°；I总 = 12∠0°；
#   分流：I1 = 10∠-53.13°、I2 = 10∠+53.13°；KCL 核账。
#   导纳法核对：Y1 = 0.2∠-53.13°、Y2 = 0.2∠53.13°（虚部相消）-> Y总 = 0.24。
# 实验 1：阻抗/导纳/电流全流程数字。
# 实验 2：RK4 时域积分（双支路状态）vs 相量稳态（三段对照）。
# 实验 3：生成图 1（电路）、图 2（相量图）、图 3（阻抗三角形）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import schemdraw
import schemdraw.elements as elm

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../electric_circuits
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

elm.style(elm.STYLE_IEC)
schemdraw.config(font="Microsoft YaHei", fontsize=14)

w = 1000.0
U = 50.0
R1, L, R2, C = 3.0, 4e-3, 3.0, 250e-6

# ---------------------------------------------------------------------
print("=== 实验 1：阻抗、导纳与电流全流程 ===")
Z1 = R1 + 1j * w * L
Z2 = R2 - 1j / (w * C)
Zt = Z1 * Z2 / (Z1 + Z2)
It = U / Zt
I1 = It * Z2 / (Z1 + Z2)          # 分流公式（相量版）
I2 = It * Z1 / (Z1 + Z2)
print("  Z1 = %.0f + j%.0f = %.0f∠%.4f° ohm" % (Z1.real, Z1.imag, abs(Z1), np.degrees(np.angle(Z1))))
print("  Z2 = %.0f - j%.0f = %.0f∠%.4f° ohm" % (Z2.real, -Z2.imag, abs(Z2), np.degrees(np.angle(Z2))))
print("  Z总 = Z1||Z2 = %.4f∠%.4f° ohm（= 25/6）" % (abs(Zt), np.degrees(np.angle(Zt))))
print("  I总 = %.0f∠%.4f° A；分流：I1 = %.0f∠%.4f° A、I2 = %.0f∠%.4f° A"
      % (abs(It), np.degrees(np.angle(It)), abs(I1), np.degrees(np.angle(I1)),
         abs(I2), np.degrees(np.angle(I2))))
print("  KCL 核账：|I1 + I2 - I总| = %.2e A" % abs(I1 + I2 - It))
# 导纳法核对
Y1, Y2 = 1 / Z1, 1 / Z2
Yt = Y1 + Y2
print("  导纳法：Y1 = %.4f∠%.4f°；Y2 = %.4f∠%.4f°（虚部相消）-> Y总 = %.4f -> 1/Y总 = %.4f"
      % (abs(Y1), np.degrees(np.angle(Y1)), abs(Y2), np.degrees(np.angle(Y2)), Yt.real, abs(1 / Yt)))
print("  -> 总电流与电压同相：两支路的电抗效果互相抵消")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：RK4 时域积分 vs 相量稳态 ===")
tau1 = L / R1
tau2 = R2 * C
T, dt = 15e-3, 1e-6
n = int(T / dt) + 1
t = np.arange(n) * dt
i1 = np.zeros(n)
uC = np.zeros(n)
us = lambda tt: U * np.sqrt(2) * np.cos(w * tt)
for k in range(1, n):
    # 状态 1：支路1 电流 i1（L 状态）：di1/dt = (us - R1 i1)/L
    k1 = (us(t[k - 1]) - R1 * i1[k - 1]) / L
    k2 = (us(t[k - 1] + dt / 2) - R1 * (i1[k - 1] + k1 * dt / 2)) / L
    k3 = (us(t[k - 1] + dt / 2) - R1 * (i1[k - 1] + k2 * dt / 2)) / L
    k4 = (us(t[k - 1] + dt) - R1 * (i1[k - 1] + k3 * dt)) / L
    i1[k] = i1[k - 1] + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6
    # 状态 2：支路2 电容电压 uC：duC/dt = (us - uC)/(R2 C)
    g1 = (us(t[k - 1]) - uC[k - 1]) / (R2 * C)
    g2 = (us(t[k - 1] + dt / 2) - (uC[k - 1] + g1 * dt / 2)) / (R2 * C)
    g3 = (us(t[k - 1] + dt / 2) - (uC[k - 1] + g2 * dt / 2)) / (R2 * C)
    g4 = (us(t[k - 1] + dt) - (uC[k - 1] + g3 * dt)) / (R2 * C)
    uC[k] = uC[k - 1] + (g1 + 2 * g2 + 2 * g3 + g4) * dt / 6
i2 = (us(t) - uC) / R2
itot = i1 + i2
ss1 = 10 * np.sqrt(2) * np.cos(w * t - np.arctan(4 / 3))
ss2 = 10 * np.sqrt(2) * np.cos(w * t + np.arctan(4 / 3))
sst = 12 * np.sqrt(2) * np.cos(w * t)
seg = t > 10 * tau1
print("  tau1 = %.3f ms、tau2 = %.3f ms；稳态段（t > 10*tau1）对照：" % (tau1 * 1e3, tau2 * 1e3))
print("  i1 偏差 = %.2e A；i2 偏差 = %.2e A；i总 偏差 = %.2e A"
      % (np.max(np.abs(i1[seg] - ss1[seg])), np.max(np.abs(i2[seg] - ss2[seg])),
         np.max(np.abs(itot[seg] - sst[seg]))))
print("  时域：i1 = 10*sqrt(2)cos(1000t-53.13°)；i2 = 10*sqrt(2)cos(1000t+53.13°)；i总 = 12*sqrt(2)cos(1000t)")

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：主例电路（双分支并联） ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.SourceV().at((0, 0)).up().length(1.4)
    d += elm.Line().at((0, 1.4)).to((0, 2.2))
    d += elm.Label().at((0.55, 1.9)).label("$u_S$", fontsize=12)
    d += elm.Line().at((0, 2.2)).to((2.4, 2.2))
    # 支路 1：R1 + L（x=1.2）
    d += elm.Line().at((1.2, 2.2)).to((1.2, 1.8))
    d += elm.Resistor().at((1.2, 0.9)).up().length(0.9)
    d += elm.Label().at((1.8, 1.35)).label("$R_1$")
    d += elm.Line().at((1.2, 0.9)).to((1.2, 0.8))
    d += elm.Inductor().at((1.2, 0.8)).down().length(0.6)
    d += elm.Label().at((0.62, 0.42)).label("$L$")
    d += elm.Line().at((1.2, 0.2)).to((1.2, 0))
    # 支路 2：R2 + C（x=2.4）
    d += elm.Line().at((2.4, 2.2)).to((2.4, 1.8))
    d += elm.Resistor().at((2.4, 0.9)).up().length(0.9)
    d += elm.Label().at((3.0, 1.35)).label("$R_2$")
    d += elm.Line().at((2.4, 0.9)).to((2.4, 0.62))
    d += elm.Line().at((2.15, 0.62)).to((2.65, 0.62))
    d += elm.Line().at((2.15, 0.42)).to((2.65, 0.42))
    d += elm.Line().at((2.4, 0.42)).to((2.4, 0))
    d += elm.Label().at((2.78, 0.5)).label("$C$", fontsize=11)
    # 底轨
    d += elm.Line().at((0, 0)).to((2.4, 0))

save_stem = "lec14_fig1_circuit"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：相量图（两支路电流合成） ===")
fig, ax = plt.subplots(figsize=(6.6, 5.2))
ax.annotate("", xy=(6, -8), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#1f5fa8", lw=2.4))
ax.annotate("", xy=(6, 8), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=2.4))
ax.annotate("", xy=(12, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#c0392b", lw=2.6))
ax.plot([6, 12], [-8, 0], ls="--", color="#1f5fa8", lw=1.2)
ax.plot([6, 12], [8, 0], ls="--", color="#2e7d32", lw=1.2)
ax.text(7.0, -8.2, "$\\dot I_1$ = 10∠-53.13°", fontsize=11, color="#1f5fa8")
ax.text(6.4, 8.6, "$\\dot I_2$ = 10∠+53.13°", fontsize=11, color="#2e7d32")
ax.text(8.6, -1.6, "$\\dot I$ = 12∠0°（与 $\\dot U$ 同向）", fontsize=11, color="#c0392b")
ax.axhline(0, color="#444444", lw=0.8)
ax.axvline(0, color="#444444", lw=0.8)
ax.set_aspect("equal")
ax.set_xlim(-1.2, 14.4)
ax.set_ylim(-10.2, 10.2)
ax.set_xlabel("实轴 / A")
ax.set_title("相量图：两条支路电流合成总电流", fontsize=11)
ax.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec14_fig2_phasor"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：阻抗三角形（感性/容性） ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.4))
for ax, sgn, cc, name in [(ax1, +1, "#c0392b", "感性：$Z$ = 3+j4"), (ax2, -1, "#1f5fa8", "容性：$Z$ = 3-j4")]:
    ax.annotate("", xy=(3, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=2.2))
    ax.annotate("", xy=(3, sgn * 4), xytext=(3, 0), arrowprops=dict(arrowstyle="->", color="#999999", lw=1.6))
    ax.annotate("", xy=(3, sgn * 4), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=cc, lw=2.4))
    ax.text(1.2, -0.85 if sgn > 0 else 0.55, "$R$ = 3 $\\Omega$", fontsize=11, color="#2e7d32")
    ax.text(3.2, sgn * 1.2, "$X$ = %s4 $\\Omega$" % ("+" if sgn > 0 else "-"), fontsize=11, color="#666666")
    ax.text(0.95, sgn * 2.3, "$|Z|$ = 5 $\\Omega$", fontsize=11, color=cc)
    ax.text(2.0, sgn * 0.75, "%s53.13°" % ("+" if sgn > 0 else "-"), fontsize=10, color=cc)
    ax.axhline(0, color="#444444", lw=0.8)
    ax.axvline(0, color="#444444", lw=0.8)
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 5.4)
    ax.set_ylim(-6.0, 6.0)
    ax.set_title(name + " $\\Omega$ 的阻抗三角形", fontsize=11)
    ax.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec14_fig3_ztriangle"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec14-01 完成。")