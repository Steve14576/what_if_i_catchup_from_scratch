# =====================================================================
# lec10-01 换路与零输入响应：初始值、0+ 等效电路、指数衰减与 tau
#          （第 10 讲 全讲；图 1 换路前后、图 2 衰减曲线与 tau 扫描）
# 规模纪律：总耗时 < 10 秒（小步长 Euler + 两张图）。
# 方法：
#   实验 1：运行例——t<0：12V 源、R1=1k、结点 A、R2=1k 到地、R3=1k 串 C=1uF 到地
#           稳态 u_C(0-) = 6 V；t=0 断开干路后 C 经 R3+R2 放电：tau = 2 ms。
#           解析 u_C = 6e^(-t/tau) vs Euler 数值积分对照；1~5tau 残值表。
#   实验 2：0+ 等效电路求解：u_A(0+) = 3 V、u_R3(0+) = 3 V、i_C(0+) = -3 mA、KVL 核对。
#   实验 3：RL 对偶例——24V/R1=6Ω/(R2=12Ω ∥ L=12mH)：i_L(0-) = 4 A；
#           断源后 tau = L/R2 = 1 ms、i_L = 4e^(-t/tau)、u_L(0+) = -48 V（反击）。
#   实验 4：作业数字预验证（Q2-Q6）。
#   并生成 figures/lec10_fig1_switching.svg/.png 与 lec10_fig2_decay.svg/.png。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ->）。
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

# ---------------------------------------------------------------------
print("=== 实验 1：运行例——换路前稳态与断源后放电 ===")
E, R1, R2, R3, C = 12.0, 1e3, 1e3, 1e3, 1e-6
uC0 = E * R2 / (R1 + R2)          # 稳态：C 支路无电流，A 点分压；u_C = u_A
tau = (R2 + R3) * C               # 放电回路：R3 + R2
print("  换路前稳态：u_C(0-) = %.0f V（分压 %.0f*%.0f/%.0f）；tau = %.0f ms"
      % (uC0, E, R2, R1 + R2, tau * 1e3))
dt = 1e-6
t = np.arange(0, 6 * tau, dt)
u = np.zeros_like(t)
u[0] = uC0
# 电路方程：i = u/(R2+R3)（流出 C 正端），du/dt = -i/C
for k in range(1, len(t)):
    u[k] = u[k - 1] - (u[k - 1] / (R2 + R3)) * dt / C
u_exact = uC0 * np.exp(-t / tau)
print("  数值 vs 解析最大偏差 = %.2e V" % np.max(np.abs(u - u_exact)))
for kk in [1, 2, 3, 5]:
    print("  t = %.0ftau：u_C = %.4f V（残值 %.2f%%）"
          % (kk, uC0 * np.exp(-kk), 100 * np.exp(-kk)))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：0+ 等效电路求解 ===")
iC0 = -uC0 / (R2 + R3)
uA0 = uC0 * R2 / (R2 + R3)
uR3_0 = uC0 * R3 / (R2 + R3)
print("  换路定则：u_C(0+) = %.0f V（= 0- 值）" % uC0)
print("  0+ 电路：i_C(0+) = %.0f mA（流出 C 正端）；u_A(0+) = %.0f V；u_R3(0+) = %.0f V"
      % (iC0 * 1e3, uA0, uR3_0))
print("  KVL 核对：u_R3 + u_A - u_C = %.0f + %.0f - %.0f = %.2e" % (uR3_0, uA0, uC0, uR3_0 + uA0 - uC0))
print("  注意：源支路断开 -> R1 支路电流为 0 -> u_R1(0+) = 0（可以突变！）")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：RL 对偶例（电感反击） ===")
E2, R1b, R2b, L = 24.0, 6.0, 12.0, 12e-3
iL0 = E2 / R1b                    # 换路前 L 短路 -> 结点电压 0 -> 全部电流走 L
tauL = L / R2b
tL = np.arange(0, 5 * tauL, dt)
iL = np.zeros_like(tL)
iL[0] = iL0
for k in range(1, len(tL)):
    # 断源后：L 经 R2 放电，u_L = -R2*i -> di/dt = -R2*i/L
    iL[k] = iL[k - 1] - (R2b * iL[k - 1] / L) * dt
iL_exact = iL0 * np.exp(-tL / tauL)
print("  i_L(0-) = %.0f A；tau = L/R2 = %.0f ms；数值 vs 解析最大偏差 = %.2e A"
      % (iL0, tauL * 1e3, np.max(np.abs(iL - iL_exact))))
print("  u_L(0+) = -R2*i_L(0+) = %.0f V（断开瞬间的高压反击——09 讲口诀的现场）" % (-R2b * iL0))
print("  i_L(1tau) = %.4f A；到 0.4 A 需要 t = tau*ln10 = %.3f ms"
      % (iL0 * np.exp(-1), tauL * 1e3 * np.log(10)))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：作业数字预验证 ===")
# Q2/Q3：18V、R1=2k、R2=R3=1k、C=2uF
u2 = 18 * 1 / (2 + 1)
tau2 = (1e3 + 1e3) * 2e-6
print("  Q2：u_C(0-) = %.0f V；tau = %.0f ms；i_C(0+) = %.1f mA；u_A(0+) = %.1f V"
      % (u2, tau2 * 1e3, -u2 / 2e3 * 1e3, u2 / 2))
print("  Q3：u_C(4ms) = %.4f V；到 1 V 需 t = tau*ln6 = %.3f ms"
      % (u2 * np.exp(-1), tau2 * 1e3 * np.log(6)))
# Q4：RL 对偶 10mH/20 欧/1A
tau4 = 10e-3 / 20
print("  Q4：tau = %.1f ms；i(1tau) = %.4f A；u_L(0+) = %.0f V；到 0.1 A 需 t = tau*ln10 = %.3f ms"
      % (tau4 * 1e3, np.exp(-1), -20.0, tau4 * 1e3 * np.log(10)))
# Q6：与实验 3 同构
print("  Q6：i_L(t) = 4e^(-t/1ms) A；u_L(0+) = -48 V；到 0.4 A 需 t = %.3f ms"
      % (1.0 * np.log(10)))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：运行例换路前后 ===")
with schemdraw.Drawing(show=False) as d:
    def draw_t_neg(x0):
        global d
        # 12V 源（左）-> 开关 -> R1 -> 结点 A；A 右侧 R3 串 C 到地；R2 竖直
        d += elm.SourceV().at((x0, 0)).up().length(1.1)
        d += elm.Label().at((x0 - 0.95, 0.55)).label("12 V")
        d += elm.Line().at((x0, 1.1)).to((x0, 2.2))
        d += elm.Line().at((x0, 2.2)).to((x0 + 0.6, 2.2))
        # 闭合开关（两触点 + 横线）
        d += elm.Dot().at((x0 + 0.6, 2.2))
        d += elm.Dot().at((x0 + 1.6, 2.2))
        d += elm.Line().at((x0 + 0.6, 2.2)).to((x0 + 1.6, 2.2))
        d += elm.Line().at((x0 + 1.6, 2.2)).to((x0 + 2.0, 2.2))
        d += elm.Resistor().at((x0 + 2.0, 2.2)).right().length(1.2)
        d += elm.Label().at((x0 + 2.6, 2.75)).label("$R_1$")
        d += elm.Line().at((x0 + 3.2, 2.2)).to((x0 + 4.2, 2.2))
        d += elm.Dot().at((x0 + 4.2, 2.2))
        d += elm.Label().at((x0 + 4.3, 2.45)).label("A", fontsize=11)
        # R2 竖直
        d += elm.Resistor().at((x0 + 3.0, 0.7)).up().length(1.0)
        d += elm.Label().at((x0 + 2.15, 1.2)).label("$R_2$")
        d += elm.Line().at((x0 + 3.0, 2.2)).to((x0 + 3.0, 1.7))
        d += elm.Line().at((x0 + 3.0, 0.7)).to((x0 + 3.0, 0))
        # R3 + C 支路
        d += elm.Resistor().at((x0 + 4.2, 2.2)).right().length(0.9)
        d += elm.Label().at((x0 + 4.65, 2.75)).label("$R_3$")
        d += elm.Line().at((x0 + 5.1, 2.2)).to((x0 + 5.6, 2.2))
        d += elm.Line().at((x0 + 5.6, 2.2)).to((x0 + 5.6, 1.6))
        d += elm.Line().at((x0 + 5.1, 1.6)).to((x0 + 6.1, 1.6))
        d += elm.Line().at((x0 + 5.1, 1.4)).to((x0 + 6.1, 1.4))
        d += elm.Line().at((x0 + 5.6, 1.4)).to((x0 + 5.6, 0))
        d += elm.Label().at((x0 + 6.5, 1.5)).label("$C$", fontsize=11)
        # 底轨
        d += elm.Line().at((x0, 0)).to((x0 + 5.6, 0))
        d += elm.Label().at((x0 + 2.8, -0.7)).label("（a）$t<0$：稳态 $u_C = 6$ V", fontsize=10)

    def draw_t_pos(x0):
        global d
        # t>0：源与 R1 撤出（画断开的开关），A 处 R3 串 C(->6V 源) 到地、R2 到地
        d += elm.Dot().at((x0 + 0.6, 2.2))
        d += elm.Dot().at((x0 + 1.6, 2.2))
        d += elm.Line().at((x0 + 0.6, 2.2)).to((x0 + 1.35, 2.6))  # 断开的开关杆
        d += elm.Label().at((x0 + 0.75, 2.95)).label("断开", fontsize=10)
        d += elm.Line().at((x0 + 1.6, 2.2)).to((x0 + 2.0, 2.2))
        d += elm.Resistor().at((x0 + 2.0, 2.2)).right().length(1.2)
        d += elm.Label().at((x0 + 2.6, 2.75)).label("$R_1$")
        d += elm.Line().at((x0 + 3.2, 2.2)).to((x0 + 4.2, 2.2))
        d += elm.Dot().at((x0 + 4.2, 2.2))
        d += elm.Label().at((x0 + 4.3, 2.45)).label("A", fontsize=11)
        d += elm.Resistor().at((x0 + 3.0, 0.7)).up().length(1.0)
        d += elm.Label().at((x0 + 2.15, 1.2)).label("$R_2$")
        d += elm.Line().at((x0 + 3.0, 2.2)).to((x0 + 3.0, 1.7))
        d += elm.Line().at((x0 + 3.0, 0.7)).to((x0 + 3.0, 0))
        d += elm.Resistor().at((x0 + 4.2, 2.2)).right().length(0.9)
        d += elm.Label().at((x0 + 4.65, 2.75)).label("$R_3$")
        d += elm.Line().at((x0 + 5.1, 2.2)).to((x0 + 5.6, 2.2))
        d += elm.Line().at((x0 + 5.6, 2.2)).to((x0 + 5.6, 1.7))
        # C 换成 6V 电压源（+ 朝上：u_C(0+) 为正）
        d += elm.SourceV().at((x0 + 5.6, 0)).up().length(1.4)
        d += elm.Label().at((x0 + 6.55, 0.6)).label("6 V", fontsize=11)
        d += elm.Label().at((x0 + 6.5, 1.5)).label("$u_C(0\\!+)$", fontsize=10)
        d += elm.Line().at((x0 + 5.6, 1.4)).to((x0 + 5.6, 1.7))
        d += elm.Line().at((x0, 0)).to((x0 + 5.6, 0))
        d += elm.Label().at((x0 + 2.8, -0.7)).label("（b）$t>0$ 的 $0^+$ 等效电路：$C$ 换 6 V 源", fontsize=10)

    draw_t_neg(0.0)
    draw_t_pos(8.2)

save_stem = "lec10_fig1_switching"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：衰减曲线与 tau 扫描 ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
tt = np.linspace(0, 6 * tau, 500)
uu = uC0 * np.exp(-tt / tau)
ax1.plot(tt * 1e3, uu, color="#1f5fa8", lw=2.2)
for k in [1, 2, 3]:
    ax1.axvline(k * tau * 1e3, color="#999999", ls="--", lw=1)
    ax1.plot([k * tau * 1e3], [uC0 * np.exp(-k)], "o", color="#c0392b", ms=5)
# 初始切线：交横轴于 tau
ax1.plot([0, tau * 1e3], [uC0, 0], color="#2e7d32", lw=1.4, ls=":")
ax1.annotate("初始切线交横轴于 $\\tau$（= 2 ms）", xy=(5.3, 2.9), fontsize=10, color="#2e7d32")
ax1.annotate("$1\\tau$：2.21 V（36.8%）", xy=(2.0, 2.2073), xytext=(2.6, 3.4), fontsize=10,
             arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax1.annotate("$3\\tau$：0.30 V（4.98%）", xy=(6.0, 0.2987), xytext=(3.9, 1.6), fontsize=10,
             arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax1.set_xlabel("时间 $t$ / ms（$\\tau$ = 2 ms）")
ax1.set_ylabel("$u_C$ / V")
ax1.set_title("零输入响应：指数衰减，残值每过 $\\tau$ 乘 $e^{-1}$")
ax1.grid(alpha=0.3)

for tau_k, cc in [(1, "#c0392b"), (2, "#1f5fa8"), (4, "#2e7d32")]:
    ax2.plot(tt * 1e3, uC0 * np.exp(-tt / (tau_k * 1e-3)), lw=2.0, color=cc,
             label="$\\tau$ = %d ms" % tau_k)
ax2.legend(fontsize=10)
ax2.set_xlabel("时间 $t$ / ms")
ax2.set_ylabel("$u_C$ / V")
ax2.set_title("$\\tau$ 扫描：$\\tau$ 越大衰减越慢（初始斜率越平）")
ax2.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec10_fig2_decay"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec10-01 完成。")