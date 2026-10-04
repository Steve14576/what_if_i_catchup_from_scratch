# =====================================================================
# lec13-02 RL 电路的相量法全流程与作业预验证
#          （第 13 讲 §3 数值实验；图 3 电路、图 4 波形与相量图）
# 规模纪律：总耗时 < 10 秒（RK4 dt=1us + 两张图）。
#
# 运行例：u_S = 10*sqrt(2) cos(1000t) V（有效值 10 V）、R = 3 ohm、
#   L = 4 mH（wL = 4 ohm）。相量法：Z = 3+4j = 5∠53.13°；
#   I = 2∠-53.13° A；U_R = 6∠-53.13°；U_L = 8∠36.87°；核账 6+8j = 10。
#   全解（含暂态）：i(t) = 2*sqrt(2)cos(1000t-53.13°) - 1.6971 e^(-t/tau)，
#   tau = L/R = 1.333 ms。
# 实验 1：相量法求解与 KVL 相量核账。
# 实验 2：RK4 数值解 vs 全解（含暂态）与稳态段对照。
# 实验 3：作业数字预验证（Q2-Q6、Q8）。
# 并生成 figures/lec13_fig3_circuit.svg/.png 与 lec13_fig4_rl.svg/.png。
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
Us = 10.0          # 有效值
R, L = 3.0, 4e-3

# ---------------------------------------------------------------------
print("=== 实验 1：相量法求解与 KVL 相量核账 ===")
Z = R + 1j * w * L
Idot = Us / Z                      # U 取 10∠0°
UR = R * Idot
UL = 1j * w * L * Idot
print("  Z = %.0f + j%.0f ohm = %.0f∠%.4f°" % (Z.real, Z.imag, abs(Z), np.degrees(np.angle(Z))))
print("  I = %.0f∠%.4f° A；U_R = %.0f∠%.4f° V；U_L = %.0f∠%.4f° V"
      % (abs(Idot), np.degrees(np.angle(Idot)), abs(UR), np.degrees(np.angle(UR)),
         abs(UL), np.degrees(np.angle(UL))))
print("  KVL 核账：|U_R + U_L - U| = %.2e V" % abs(UR + UL - Us))
print("  时域：i(t) = 2*sqrt(2) cos(1000t - 53.13°) A（有效值 2 A）")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：RK4 数值解 vs 全解（含暂态）与稳态段 ===")
tau = L / R
I_mag = abs(Idot)
I_ph = np.angle(Idot)

def i_ss(tt):
    return I_mag * np.sqrt(2) * np.cos(w * tt + I_ph)

T, dt = 15e-3, 1e-6
n = int(T / dt) + 1
t = np.arange(n) * dt
i = np.zeros(n)
for k in range(1, n):
    k1 = (Us * np.sqrt(2) * np.cos(w * t[k - 1]) - R * i[k - 1]) / L
    k2 = (Us * np.sqrt(2) * np.cos(w * (t[k - 1] + dt / 2)) - R * (i[k - 1] + k1 * dt / 2)) / L
    k3 = (Us * np.sqrt(2) * np.cos(w * (t[k - 1] + dt / 2)) - R * (i[k - 1] + k2 * dt / 2)) / L
    k4 = (Us * np.sqrt(2) * np.cos(w * (t[k - 1] + dt)) - R * (i[k - 1] + k3 * dt)) / L
    i[k] = i[k - 1] + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6
K = -i_ss(np.array([0.0]))[0]
i_full = i_ss(t) + K * np.exp(-t / tau)
print("  tau = L/R = %.3f ms；暂态系数 K = -i_ss(0) = %.4f A" % (tau * 1e3, K))
print("  RK4 vs 全解（0-15 ms）max 偏差 = %.2e A" % np.max(np.abs(i - i_full)))
seg = t > 10 * tau
print("  稳态段（t > 10tau）RK4 vs 相量解 max 偏差 = %.2e A" % np.max(np.abs(i[seg] - i_ss(t[seg]))))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：作业数字预验证 ===")
# Q2：8*sqrt(2) sin(1000t+30°) -> 8∠-60°
print("  Q2：u = 8*sqrt(2) sin(1000t+30°) -> U = 8∠-60° V（sin 先转 cos）")
# Q3：相位差
print("  Q3：u 10∠45° 与 i 2∠-15°：phi = 45 - (-15) = 60°，u 超前 i 60°")
# Q4：RC：U=20V、R=6、C=125uF（1/wC = 8 ohm）
Z4 = 6 - 1j / (w * 125e-6)
I4 = 20 / Z4
UC4 = I4 * (-1j / (w * 125e-6))
print("  Q4：Z = %.0f - j%.0f = %.0f∠%.4f°；I = %.0f∠%.4f°；U_C = %.0f∠%.4f°；核账 %.1e"
      % (Z4.real, -Z4.imag, abs(Z4), np.degrees(np.angle(Z4)), abs(I4),
         np.degrees(np.angle(I4)), abs(UC4), np.degrees(np.angle(UC4)),
         abs(6 * I4 + UC4 - 20)))
# Q5：有效值
print("  Q5：方波±10 V -> RMS 10 V；半波整流（Um=10）-> 5 V；三角波（Um=10）-> %.2f V"
      % (10 / np.sqrt(3)))
# Q6：i = 5*sqrt(2) sin(1000t+20°) -> I = 5∠-70°；di/dt 相量 5000∠20°
print("  Q6：I = 5∠-70° A；di/dt 相量 = jw I = 5000∠20° -> di/dt = 5000*sqrt(2) cos(1000t+20°) A/s")
# Q8：L 换 C = 250uF（1/wC = 4 ohm）
Z8 = 3 - 1j / (w * 250e-6)
I8 = 10 / Z8
UR8 = 3 * I8
UC8 = I8 * (-1j / (w * 250e-6))
print("  Q8：Z = %.0f - j%.0f = %.0f∠%.4f°；I = %.0f∠%.4f° A（超前电压）；核账 %.1e"
      % (Z8.real, -Z8.imag, abs(Z8), np.degrees(np.angle(Z8)), abs(I8), np.degrees(np.angle(I8)),
         abs(UR8 + UC8 - 10)))

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：运行例电路（RL 串联） ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.Line().at((0, 2.2)).to((0.9, 2.2))
    d += elm.Resistor().at((0.9, 2.2)).right().length(1.2)
    d += elm.Label().at((1.5, 2.75)).label("$R$")
    d += elm.Line().at((2.1, 2.2)).to((3.0, 2.2))
    d += elm.Line().at((3.0, 2.2)).to((3.0, 0))
    d += elm.Line().at((3.0, 0)).to((2.2, 0))
    d += elm.Inductor().at((2.2, 0)).left().length(1.2)
    d += elm.Label().at((1.6, -0.55)).label("$L$")
    d += elm.Line().at((1.0, 0)).to((0, 0))
    d += elm.SourceV().at((0, 0)).up().length(1.4)
    d += elm.Line().at((0, 1.4)).to((0, 2.2))
    d += elm.Label().at((0.75, 1.85)).label("$u_S$", fontsize=12)

save_stem = "lec13_fig3_circuit"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 4：时域波形与相量图 ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))
tt = np.linspace(0, 2 * 2 * np.pi / w, 1500)
us = 10 * np.sqrt(2) * np.cos(w * tt)
ii = 2 * np.sqrt(2) * np.cos(w * tt - np.arctan(4 / 3))
ax1.plot(tt * 1e3, us, color="#c0392b", lw=2.2, label="$u_S$（峰值 14.14 V）")
ax1b = ax1.twinx()
ax1b.plot(tt * 1e3, ii, color="#1f5fa8", lw=2.2, label="$i$（峰值 2.83 A）")
dx_ms = np.arctan(4 / 3) / w * 1e3
ax1.annotate("", xy=(dx_ms, 15.6), xytext=(0, 15.6),
             arrowprops=dict(arrowstyle="<->", color="#333333", lw=1.2))
ax1.text(0.12, 16.3, "$\\Delta t$ = %.3f ms（53.13°）" % dx_ms, fontsize=10)
ax1.axvline(0, color="#bbbbbb", ls=":", lw=1)
ax1.axvline(dx_ms, color="#bbbbbb", ls=":", lw=1)
ax1v = ax1.get_legend_handles_labels()
ax1bv = ax1b.get_legend_handles_labels()
ax1.legend(ax1v[0] + ax1bv[0], ax1v[1] + ax1bv[1], fontsize=9, loc="lower right")
ax1.set_xlabel("时间 $t$ / ms")
ax1.set_ylabel("$u_S$ / V", color="#c0392b")
ax1b.set_ylabel("$i$ / A", color="#1f5fa8")
ax1.set_title("时域：$i$ 滞后 $u_S$ 53.13°（峰值滞后 0.927 ms）", fontsize=11)
ax1.set_ylim(-18, 18)
ax1b.set_ylim(-3.6, 3.6)
ax1.grid(alpha=0.3)

ax2.annotate("", xy=(3.6, -4.8), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=2.2))
ax2.annotate("", xy=(10, 0), xytext=(3.6, -4.8), arrowprops=dict(arrowstyle="->", color="#c0392b", lw=2.2))
ax2.annotate("", xy=(10, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#1f5fa8", lw=2.4))
ax2.annotate("", xy=(1.2, -1.6), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#888888", lw=1.6, ls="--"))
ax2.text(4.6, -4.4, "$\\dot U_R$ = 6 V", fontsize=10, color="#2e7d32")
ax2.text(5.6, 1.2, "$\\dot U_L$ = 8 V", fontsize=10, color="#c0392b")
ax2.text(7.4, -2.2, "$\\dot U$ = 10 V", fontsize=10, color="#1f5fa8")
ax2.text(1.35, -2.0, "$\\dot I$ = 2 A", fontsize=10, color="#888888")
ax2.axhline(0, color="#444444", lw=0.8)
ax2.axvline(0, color="#444444", lw=0.8)
ax2.set_aspect("equal")
ax2.set_xlim(-1.2, 11.6)
ax2.set_ylim(-6.2, 3.2)
ax2.set_xlabel("实轴 / V")
ax2.set_title("相量图：$\\dot U_R + \\dot U_L = \\dot U$（6∠-53.13° + 8∠36.87° = 10∠0°）", fontsize=11)
ax2.grid(alpha=0.3)

plt.tight_layout()
save_stem = "lec13_fig4_rl"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec13-02 完成。")