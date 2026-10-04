# =====================================================================
# lec11-01 全响应与三套分解口径：三要素法 vs 数值解
#          （第 11 讲 §1-§3 数值实验；图 1 运行例电路、图 2 分解三面板）
# 规模纪律：总耗时 < 10 秒（dt = 1 us 的 Euler 积分 + 两张图）。
#
# 运行例（全讲主线）：
#   t<0：开关位 1，C 由 4 V 源预充 -> u_C(0-) = 4 V；
#   t=0：拨到位 2 接入网络：12 V 源、R1=2k（源->A）、R2=2k（A->地）、
#        R3=1k 串 C=1uF（A->地）。
#   换路后：u_C(inf) = 12*R2/(R1+R2) = 6 V；
#           tau = (R1||R2 + R3)*C = 2 ms；u_C(t) = 6 - 2 e^(-t/tau)。
#
# 实验 1：全响应解析 vs Euler 数值积分（最大偏差、1/2/3 tau 读数）。
# 实验 2：三套分解口径逐点回加残差：
#         零输入 4e^(-t/tau) + 零状态 6(1-e^(-t/tau))；
#         稳态 6 + 暂态 -2e^(-t/tau)。
# 实验 3：0+ 电路复核：u_A(0+) = 5 V、i_C(0+) = 1 mA、KCL 核账；
#         三要素通吃：u_A 与 i_C 用同一 tau 的 ODE 数值积分 vs 解析。
# 实验 4：作业数字预验证（Q2-Q4、Q8）。
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

# ---------------------------------------------------------------------
print("=== 实验 1：全响应解析 vs Euler 数值积分 ===")
U, R1, R2, R3, C = 12.0, 2e3, 2e3, 1e3, 1e-6
uC0, uCinf = 4.0, U * R2 / (R1 + R2)          # 初值 4 V；终值 6 V
Req = R1 * R2 / (R1 + R2) + R3                # C 两端看进去的等效电阻
tau = Req * C                                  # 2 ms
print("  三要素：u_C(0+) = %.0f V；u_C(inf) = %.0f V；tau = %.0f ms" % (uC0, uCinf, tau * 1e3))
dt = 1e-6
t = np.arange(0, 5 * tau, dt)
u = np.zeros_like(t)
u[0] = uC0
# 一阶标准形方程：tau*du/dt + u = u_C(inf)  ->  du/dt = (inf - u)/tau
for k in range(1, len(t)):
    u[k] = u[k - 1] + (uCinf - u[k - 1]) / tau * dt
u_exact = uCinf - (uCinf - uC0) * np.exp(-t / tau)
print("  数值 vs 解析最大偏差 = %.2e V" % np.max(np.abs(u - u_exact)))
for kk in [1, 2, 3]:
    print("  t = %.0ftau：u_C = %.4f V（距终值 = %.4f V）"
          % (kk, uCinf - (uCinf - uC0) * np.exp(-kk), (uCinf - uC0) * np.exp(-kk)))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：三套分解口径逐点回加残差 ===")
zi = uC0 * np.exp(-t / tau)                    # 零输入成分
zs = uCinf * (1 - np.exp(-t / tau))            # 零状态成分
steady = np.full_like(t, uCinf)                # 稳态分量
trans = -(uCinf - uC0) * np.exp(-t / tau)      # 暂态分量
print("  零输入 + 零状态 回加：最大偏差 = %.2e V" % np.max(np.abs(zi + zs - u_exact)))
print("  稳态 + 暂态 回加：  最大偏差 = %.2e V" % np.max(np.abs(steady + trans - u_exact)))
print("  两种口径在 t = 1tau 的读数：零输入 %.4f + 零状态 %.4f = %.4f"
      % (zi[int(1 * tau / dt)], zs[int(1 * tau / dt)], u_exact[int(1 * tau / dt)]))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：0+ 电路复核与三要素通吃 ===")
# 0+ 电路：C 换成 4 V 源；结点 A 方程（mA/kV 单位下伏/k欧=毫安）：
# (u_A-12)/2 + u_A/2 + (u_A-4)/1 = 0  ->  4 u_A = 20  ->  u_A = 5 V
uA0 = 5.0
iC0 = (uA0 - uC0) / R3                          # 1 mA 流入 C 正端
iR1 = (U - uA0) / R1
iR2 = uA0 / R2
print("  0+ 电路：u_A(0+) = %.0f V；i_C(0+) = %.3f mA；i_R1 = %.1f mA；i_R2 = %.1f mA"
      % (uA0, iC0 * 1e3, iR1 * 1e3, iR2 * 1e3))
print("  KCL 核账：i_R1 - i_R2 - i_C = %.1f - %.1f - %.1f = %.2e mA"
      % (iR1 * 1e3, iR2 * 1e3, iC0 * 1e3, (iR1 - iR2 - iC0) * 1e3))
# 三要素通吃：u_A、i_C 与 u_C 共享同一个 tau
uA = np.zeros_like(t); uA[0] = uA0
iC = np.zeros_like(t); iC[0] = iC0
for k in range(1, len(t)):
    uA[k] = uA[k - 1] + (uCinf - uA[k - 1]) / tau * dt      # 终值也是 6 V
    iC[k] = iC[k - 1] + (0.0 - iC[k - 1]) / tau * dt        # 终值 0
uA_exact = uCinf - (uCinf - uA0) * np.exp(-t / tau)          # 6 - 1 e^(-t/tau)
iC_exact = iC0 * np.exp(-t / tau)                            # 1 mA e^(-t/tau)
print("  u_A 三要素 t=1tau 读数：%.4f V（解析 %.4f）" % (uA[int(tau / dt)], uA_exact[int(tau / dt)]))
print("  u_A 数值 vs 解析最大偏差 = %.2e V；i_C 最大偏差 = %.2e mA"
      % (np.max(np.abs(uA - uA_exact)), np.max(np.abs(iC - iC_exact)) * 1e3))
print("  三个变量的 ODE 只差初值与终值，tau 完全相同 -> 三要素通吃")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：作业数字预验证 ===")
# Q2：20 V、R1=R2=2k、R3=1k、C=1uF、u_C(0-) = 2 V
U2, u20 = 20.0, 2.0
u2inf = U2 * R2 / (R1 + R2)                  # 10 V
uA2_0 = (U2 / R1 + u20 / R3) / (1 / R1 + 1 / R2 + 1 / R3)   # 0+ 结点解 4u_A=24
iC2_0 = (uA2_0 - u20) / R3
slope2 = (u2inf - u20) / tau                 # 4 kV/s
print("  Q2：u_C(inf) = %.0f V；tau = %.0f ms；u_A(0+) = %.0f V；i_C(0+) = %.1f mA"
      % (u2inf, tau * 1e3, uA2_0, iC2_0 * 1e3))
print("      u_C(2ms) = %.4f V；斜率核账 i_C = C*du/dt = %.1f mA（两口径一致）"
      % (u2inf - (u2inf - u20) * np.exp(-1), slope2 * C * 1e3))
# Q3：同例 u_A(t) = 10 - 4 e^(-t/tau)、i_C(t) = 4 mA e^(-t/tau)
print("  Q3：u_A(0+) = %.0f V / u_A(inf) = %.0f V -> u_A(t) = 10 - 4 e^(-t/2ms)；"
      "i_C(t) = 4 mA e^(-t/2ms)" % (uA2_0, u2inf))
# Q4：RL 全响应：12 V、R=6 欧、L=3 H、i_L(0-) = 0.5 A
E4, R4, L4, i40 = 12.0, 6.0, 3.0, 0.5
tau4 = L4 / R4
i4inf = E4 / R4
uL4_0 = E4 - R4 * i40                        # KVL 直读 9 V
print("  Q4：tau = %.1f s；i_L(inf) = %.1f A；i_L(t) = %.1f - %.1f e^(-t/%.1fs)；u_L(0+) = %.1f V"
      % (tau4, i4inf, i4inf, i4inf - i40, tau4, uL4_0))
# Q8：上电延时：5 V 阶跃、R=100k、C=1uF、阈值 3.5 V
tau8 = 100e3 * 1e-6
t8 = tau8 * np.log(5.0 / (5.0 - 3.5))
print("  Q8：tau = %.2f s；到 3.5 V 需 t = tau*ln(5/1.5) = %.4f s (= %.1f ms)"
      % (tau8, t8, t8 * 1e3))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：运行例电路（双掷开关两状态） ===")
with schemdraw.Drawing(show=False) as d:
    def draw_panel(x0, pos):
        global d
        # 4 V 源（左）
        d += elm.SourceV().at((x0, 0)).up().length(1.4)
        d += elm.Label().at((x0 - 0.95, 0.6)).label("4 V")
        d += elm.Line().at((x0, 1.4)).to((x0, 2.2))
        d += elm.Line().at((x0, 2.2)).to((x0 + 1.6, 2.2))
        # 双掷开关：触点 1 / 2，公共点 P 的斜杆
        d += elm.Dot().at((x0 + 1.6, 2.2))
        d += elm.Dot().at((x0 + 3.2, 2.2))
        d += elm.Label().at((x0 + 1.35, 2.5)).label("1", fontsize=10)
        d += elm.Label().at((x0 + 3.25, 2.5)).label("2", fontsize=10)
        if pos == 1:
            d += elm.Line().at((x0 + 2.4, 1.75)).to((x0 + 1.7, 2.17))
        else:
            d += elm.Line().at((x0 + 2.4, 1.75)).to((x0 + 3.1, 2.17))
        d += elm.Dot().at((x0 + 2.4, 1.75))
        # P 向下：R3 竖直、C 双板、接地
        d += elm.Line().at((x0 + 2.4, 1.75)).to((x0 + 2.4, 1.45))
        d += elm.Resistor().at((x0 + 2.4, 0.65)).up().length(0.8)
        d += elm.Label().at((x0 + 1.55, 1.0)).label("$R_3$")
        d += elm.Line().at((x0 + 2.4, 0.65)).to((x0 + 2.4, 0.55))
        d += elm.Line().at((x0 + 2.15, 0.55)).to((x0 + 2.65, 0.55))
        d += elm.Line().at((x0 + 2.15, 0.35)).to((x0 + 2.65, 0.35))
        d += elm.Line().at((x0 + 2.4, 0.35)).to((x0 + 2.4, 0))
        d += elm.Label().at((x0 + 2.78, 0.45)).label("$C$", fontsize=11)
        # 12 V 网络：触点 2 -> R1 -> A -> 12 V 源；R2 竖直
        d += elm.Line().at((x0 + 3.2, 2.2)).to((x0 + 3.7, 2.2))
        d += elm.Resistor().at((x0 + 3.7, 2.2)).right().length(1.1)
        d += elm.Label().at((x0 + 4.25, 2.75)).label("$R_1$")
        d += elm.Line().at((x0 + 4.8, 2.2)).to((x0 + 5.9, 2.2))
        d += elm.Dot().at((x0 + 5.9, 2.2))
        d += elm.Label().at((x0 + 6.0, 2.45)).label("A", fontsize=11)
        d += elm.Line().at((x0 + 5.9, 2.2)).to((x0 + 5.9, 1.7))
        d += elm.Resistor().at((x0 + 5.9, 0.7)).up().length(1.0)
        d += elm.Label().at((x0 + 5.0, 1.2)).label("$R_2$")
        d += elm.Line().at((x0 + 5.9, 0.7)).to((x0 + 5.9, 0))
        d += elm.SourceV().at((x0 + 7.0, 0)).up().length(1.4)
        d += elm.Label().at((x0 + 7.5, 0.6)).label("12 V")
        d += elm.Line().at((x0 + 7.0, 1.4)).to((x0 + 7.0, 2.2))
        d += elm.Line().at((x0 + 5.9, 2.2)).to((x0 + 7.0, 2.2))
        # 底轨
        d += elm.Line().at((x0, 0)).to((x0 + 7.0, 0))

    draw_panel(0.0, 1)
    draw_panel(9.6, 2)
    d += elm.Label().at((2.4, -0.75)).label("（a）$t<0$：位 1，$u_C = 4$ V", fontsize=10)
    d += elm.Label().at((12.0, -0.75)).label("（b）$t>0$：位 2，接入 12 V 网络", fontsize=10)

save_stem = "lec11_fig1_circuit"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：全响应与三套分解口径（三面板） ===")
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.0))
tt = np.linspace(0, 5 * tau, 500)
uc = uCinf - (uCinf - uC0) * np.exp(-tt / tau)

ax = axes[0]
ax.plot(tt * 1e3, uc, color="#1f5fa8", lw=2.4)
ax.axhline(uCinf, color="#999999", ls="--", lw=1.2)
ax.plot([tau * 1e3], [uCinf - (uCinf - uC0) * np.exp(-1)], "o", color="#c0392b", ms=5)
ax.annotate("1$\\tau$：%.2f V" % (uCinf - (uCinf - uC0) * np.exp(-1)),
            xy=(tau * 1e3, uCinf - (uCinf - uC0) * np.exp(-1)),
            xytext=(2.6, 4.6), fontsize=10, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.annotate("终值 $u_C(\\infty)$ = 6 V", xy=(4.3, 6.0), xytext=(2.9, 6.35), fontsize=10, color="#666666")
ax.set_title("全响应：4 V 起、6 V 终\n（$\\tau$ = 2 ms）", fontsize=11)
ax.set_xlabel("时间 $t$ / ms")
ax.set_ylabel("$u_C$ / V")
ax.set_ylim(3.4, 6.8)
ax.grid(alpha=0.3)

ax = axes[1]
ax.plot(tt * 1e3, uC0 * np.exp(-tt / tau), color="#2e7d32", lw=2.0, label="零输入成分 $4e^{-t/\\tau}$")
ax.plot(tt * 1e3, uCinf * (1 - np.exp(-tt / tau)), color="#c0392b", lw=2.0, label="零状态成分 $6(1-e^{-t/\\tau})$")
ax.plot(tt * 1e3, uc, color="#1f5fa8", lw=2.4, ls=":", label="全响应（两者之和）")
ax.legend(fontsize=9, loc="center right")
ax.set_title("分解口径一：零输入 + 零状态", fontsize=11)
ax.set_xlabel("时间 $t$ / ms")
ax.set_ylim(-0.3, 7.0)
ax.grid(alpha=0.3)

ax = axes[2]
ax.axhline(uCinf, color="#999999", ls="--", lw=1.4, label="稳态分量 6 V")
ax.plot(tt * 1e3, -(uCinf - uC0) * np.exp(-tt / tau), color="#c0392b", lw=2.0,
        label="暂态分量 $-2e^{-t/\\tau}$")
ax.plot(tt * 1e3, uc, color="#1f5fa8", lw=2.4, ls=":", label="全响应（两者之和）")
ax.legend(fontsize=9, loc="center right")
ax.set_title("分解口径二：稳态 + 暂态", fontsize=11)
ax.set_xlabel("时间 $t$ / ms")
ax.set_ylim(-2.4, 7.0)
ax.grid(alpha=0.3)

plt.tight_layout()
save_stem = "lec11_fig2_decompose"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec11-01 完成。")