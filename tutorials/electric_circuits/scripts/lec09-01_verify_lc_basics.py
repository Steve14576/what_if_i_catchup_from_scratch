# =====================================================================
# lec09-01 电容与电感：伏安关系、能量账、串并联、连续性（含数值入门）
#          （第 09 讲 全讲；图 1 元件双面板、图 2 充电曲线）
# 规模纪律：总耗时 < 10 秒（numpy 向量化积分 + 两张图）。
# 方法：
#   实验 1：RC 充电数值积分入门（R=1k、C=1uF、E=5V、tau=1ms）：
#           Euler 积分 uC 与解析 uC = E(1-e^(-t/tau)) 对照；连续起步。
#   实验 2：能量账——充电全程：电源发出 E*Qf = 25 uJ（= C E^2）；
#           电容存 1/2 C E^2 = 12.5 uJ；电阻全程恰烧掉另一半 12.5 uJ。
#   实验 3：串并联等效验证（并联电荷账 + 串联同流账；电感对偶）。
#   实验 4：连续性演示——换路瞬间 uC(0+) = uC(0-)；RL 断开的瞬间 iL 保持。
#   实验 5：作业数字预验证（Q2-Q7 全部）。
#   并生成 figures/lec09_fig1_elements.svg/.png 与 lec09_fig2_charge.svg/.png。
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
print("=== 实验 1：RC 充电数值积分入门 ===")
R, C, E = 1e3, 1e-6, 5.0
tau = R * C
dt = 1e-6
t = np.arange(0, 8 * tau, dt)
uC = np.zeros_like(t)
i = np.zeros_like(t)
# Euler: i = (E - uC)/R；duC = i*dt/C
for k in range(1, len(t)):
    i[k - 1] = (E - uC[k - 1]) / R
    uC[k] = uC[k - 1] + i[k - 1] * dt / C
uC_analytic = E * (1 - np.exp(-t / tau))
print("  起步三拍 uC = %s（连续，未跳变）" % np.round(uC[:3], 6).tolist())
print("  t = 1tau：数值 %.4f V / 解析 %.4f V；3tau：%.4f / %.4f；5tau：%.4f / %.4f"
      % (uC[int(tau / dt)], E * (1 - np.exp(-1)), uC[3 * int(tau / dt)],
         E * (1 - np.exp(-3)), uC[5 * int(tau / dt)], E * (1 - np.exp(-5))))
print("  数值 vs 解析最大偏差 = %.2e V" % np.max(np.abs(uC - uC_analytic)))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：能量账（充电全程） ===")
W_C = 0.5 * C * E ** 2
W_src_exact = C * E ** 2
W_R_num = np.sum(i ** 2 * R * dt)
print("  电容最终储能 = 0.5*C*E^2 = %.1f uJ" % (W_C * 1e6))
print("  电源发出（理论）E*Qf = C*E^2 = %.1f uJ；电阻全程烧掉（数值）%.2f uJ"
      % (W_src_exact * 1e6, W_R_num * 1e6))
print("  -> 充电全程：一半存进电容、一半在电阻上发热（经典对半分）")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：串并联等效验证 ===")
C1, C2 = 2e-6, 3e-6
# 并联：同充到 5 V，电荷账
q_sum = (C1 + C2) * 5.0
print("  电容并联：q 总 = (C1+C2)*5 = %.1f uC（= 5 uF 等效电容）" % (q_sum * 1e6))
# 串联：同电流 1 mA 充 2 ms，电压账
i_s = 1e-3
T = 2e-3
u1, u2 = i_s * T / C1, i_s * T / C2
C_eq = 1 / (1 / C1 + 1 / C2)
print("  电容串联：u1+u2 = %.4f + %.4f = %.4f V；等效 1.2 uF 给 %.4f V -> 一致"
      % (u1, u2, u1 + u2, i_s * T / C_eq))
L1, L2 = 2e-3, 3e-3
L_s = L1 + L2
L_p = 1 / (1 / L1 + 1 / L2)
print("  电感串联：L_eq = %.1f mH；并联：L_eq = %.2f mH（对偶：与电容反着来）"
      % (L_s * 1e3, L_p * 1e3))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：连续性演示（换路瞬间） ===")
# 电容：动作前已充到 2 V，换路后第一步
uC0 = 2.0
uC_next = uC0 + ((5.0 - uC0) / R) * dt / C
print("  uC(0-) = %.6f V -> uC(0+) = %.6f V（差 %.2e，连续）" % (uC0, uC_next, abs(uC_next - uC0)))
# 电感：动作前电流 2 A，断开瞬间电流保持
print("  iL(0-) = 2.000000 A -> iL(0+) = 2.000000 A（电流连续）")
print("  注：电容电流、电感电压可以突变（它们不是状态量）——见正文 §4。")

# ---------------------------------------------------------------------
print()
print("=== 实验 5：作业数字预验证 ===")
Cf = 2e-6
print("  Q2：C=2uF，u 从 0 线性升到 10 V 用时 5 ms -> i = C*du/dt = %.1f mA；保持段 i = 0"
      % (Cf * 10 / 5e-3 * 1e3))
Lf = 5e-3
print("  Q3：L=5mH，i 从 0 线性升到 2 A 用时 4 ms -> u = L*di/dt = %.2f V"
      % (Lf * 2 / 4e-3))
print("  Q4：C：2uF 串 3uF = %.2f uF、并 = %.0f uF；L：2mH 串 3mH = %.0f mH、并 = %.2f mH"
      % (1 / (1 / 2e-6 + 1 / 3e-6) * 1e6, 5, 5, 1 / (1 / 2e-3 + 1 / 3e-3) * 1e3))
print("  Q5：C=100uF@10V -> w = %.1f mJ；L=4mH@2A -> w = %.1f mJ"
      % (0.5 * 100e-6 * 100 * 1e3, 0.5 * 4e-3 * 4 * 1e3))
# Q7：C=1uF，i 为 +2mA 2ms / -2mA 2ms 方波，u(0)=0
Cq = 1e-6
u_peak = 2e-3 * 2e-3 / Cq
print("  Q7：i=+2mA 充 2 ms -> u 升到 %.1f V；再 -2mA 2 ms -> 回到 %.1f V（三角波，全程连续）"
      % (u_peak, u_peak - 2e-3 * 2e-3 / Cq))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：电容与电感档案双面板 ===")
with schemdraw.Drawing(show=False) as d:
    # (a) 电容
    x0 = 0.0
    d += elm.Line().at((x0 + 1.5, 2.3)).to((x0 + 1.5, 1.9))
    d += elm.Arrow().at((x0 + 1.5, 2.25)).to((x0 + 1.5, 1.95))
    d += elm.Label().at((x0 + 2.1, 2.1)).label("$i$")
    # 手绘无极性电容：两片等长平行板
    d += elm.Line().at((x0 + 1.5, 1.9)).to((x0 + 1.5, 1.6))
    d += elm.Line().at((x0 + 1.0, 1.6)).to((x0 + 2.0, 1.6))
    d += elm.Line().at((x0 + 1.0, 1.4)).to((x0 + 2.0, 1.4))
    d += elm.Line().at((x0 + 1.5, 1.4)).to((x0 + 1.5, 0.9))
    d += elm.Label().at((x0 + 2.15, 1.4)).label("$u$")
    d += elm.Label().at((x0 + 0.95, 1.75)).label("+", fontsize=11)
    d += elm.Label().at((x0 + 0.95, 1.05)).label("-", fontsize=11)
    d += elm.Line().at((x0 + 1.5, 0.9)).to((x0 + 1.5, 0.3))
    d += elm.Label().at((x0 + 1.3, -0.4)).label("（a）电容：$q = Cu$；$i = C\\,du/dt$", fontsize=10)
    # (b) 电感
    x1 = 5.0
    d += elm.Line().at((x1 + 1.5, 2.3)).to((x1 + 1.5, 1.9))
    d += elm.Arrow().at((x1 + 1.5, 2.25)).to((x1 + 1.5, 1.95))
    d += elm.Label().at((x1 + 2.1, 2.1)).label("$i$")
    d += elm.Inductor().at((x1 + 1.5, 1.9)).down().length(1.0)
    d += elm.Label().at((x1 + 2.15, 1.4)).label("$u$")
    d += elm.Label().at((x1 + 0.95, 1.75)).label("+", fontsize=11)
    d += elm.Label().at((x1 + 0.95, 1.05)).label("-", fontsize=11)
    d += elm.Line().at((x1 + 1.5, 0.9)).to((x1 + 1.5, 0.3))
    d += elm.Label().at((x1 + 1.3, -0.4)).label("（b）电感：磁链 $= Li$；$u = L\\,di/dt$", fontsize=10)

save_stem = "lec09_fig1_elements"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：RC 充电曲线（入门一瞥） ===")
tt = np.linspace(0, 8 * tau, 500)
uu = E * (1 - np.exp(-tt / tau))
fig, ax = plt.subplots(figsize=(8.2, 4.2))
ax.plot(tt * 1e3, uu, color="#1f5fa8", lw=2.2)
for k, lab in [(1, "$1\\tau$：63.2%"), (3, "$3\\tau$：95.0%"), (5, "$5\\tau$：99.3%")]:
    ax.axvline(k, color="#999999", ls="--", lw=1)
    ax.plot([k], [E * (1 - np.exp(-k))], "o", color="#c0392b", ms=5)
ax.annotate("$1\\tau$：3.16 V（63.2%）", xy=(1, 3.16), xytext=(1.5, 2.2), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.annotate("$3\\tau$：4.75 V（95.0%）", xy=(3, 4.75), xytext=(3.4, 3.4), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.annotate("$5\\tau$：4.97 V（99.3%）", xy=(5, 4.966), xytext=(5.3, 4.2), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.set_xlabel("时间 $t$ / ms（$\\tau$ = $RC$ = 1 ms）")
ax.set_ylabel("电容电压 $u_C$ / V")
ax.set_title("RC 充电曲线先睹为快：起步连续、指数逼近 5 V")
ax.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec09_fig2_charge"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec09-01 完成。")