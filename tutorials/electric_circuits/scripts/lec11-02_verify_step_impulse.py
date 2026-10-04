# =====================================================================
# lec11-02 阶跃与冲激：两个标准激励与两种标准响应
#          （第 11 讲 §4 数值实验；图 3 阶跃、图 4 冲激逼近）
# 规模纪律：总耗时 < 10 秒（小步长 Euler 若干次 + 两张图）。
#
# 运行例延续：12 V 网络（戴维南等效：6 V 源 + Req = 2k、tau = 2 ms），
#   C = 1 uF。
# 实验 1：阶跃响应——12 V * eps(t) 接入的零状态响应 6(1-e^(-t/tau))；
#          Euler vs 解析；1 tau 读数与初始斜率。
# 实验 2：冲激逼近——电流窄脉冲（面积恒为 Q = 1 uC，宽度 Delta 递减）
#          注入并联 RC（R = 2k、C = 1 uF）；峰值 -> Q/C = 1 V。
# 实验 3：全曲线对照——Delta = 1 us 数值响应 vs 理想冲激响应 e^(-t/tau)。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../electric_circuits
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

tau = 2e-3          # 运行例时间常数 2 ms
uc_inf = 6.0        # 12 V 接入的零状态终值 6 V

# ---------------------------------------------------------------------
print("=== 实验 1：阶跃响应（12 V * eps(t) 接入，零状态） ===")
dt = 1e-6
t = np.arange(0, 5 * tau, dt)
u = np.zeros_like(t)
for k in range(1, len(t)):
    u[k] = u[k - 1] + (uc_inf - u[k - 1]) / tau * dt
u_exact = uc_inf * (1 - np.exp(-t / tau))
print("  数值 vs 解析最大偏差 = %.2e V" % np.max(np.abs(u - u_exact)))
print("  t = 1tau：u_C = %.4f V（= 6 x 0.632 = 稳态的 63.2%%）" % (uc_inf * (1 - np.exp(-1))))
print("  初始斜率 du/dt(0+) = %.0f V/s（= 6 V / 2 ms，从 0 直指稳态的切线）"
      % (uc_inf / tau))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：冲激逼近——窄脉冲峰值收敛 ===")
Q, R, C = 1e-6, 2e3, 1e-6
print("  理想冲激：u_C 跳变 Q/C = %.1f V，随后按 e^(-t/tau) 衰减" % (Q / C))
print("  Delta / us   数值峰值 / V   解析 (Q/C)(1-Delta/2tau)   偏差")
for D in [4e-6, 2e-6, 1e-6, 0.5e-6]:
    I0 = Q / D
    dts = 5e-9
    n = int(round(1.2 * D / dts))
    tt = np.arange(n) * dts
    uu = np.zeros(n)
    for k in range(1, n):
        ik = I0 if tt[k - 1] < D else 0.0
        uu[k] = uu[k - 1] + (ik - uu[k - 1] / R) / C * dts
    peak = uu.max()
    theory = I0 * R * (1 - np.exp(-D / tau))
    print("  %.1f          %.6f       %.6f                 %.1e"
          % (D * 1e6, peak, theory, abs(peak - theory)))
print("  -> Delta 越小峰值越接近 1 V：窄脉冲在极限里'干净地'交出 Q/C")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：全曲线对照（Delta = 1 us） ===")
D = 1e-6
I0 = Q / D
dt3 = 1e-7
t3 = np.arange(0, 3 * tau, dt3)
u3 = np.zeros_like(t3)
for k in range(1, len(t3)):
    ik = I0 if t3[k - 1] < D else 0.0
    u3[k] = u3[k - 1] + (ik - u3[k - 1] / R) / C * dt3
upk = I0 * R * (1 - np.exp(-D / tau))
u3_exact = np.where(t3 <= D, I0 * R * (1 - np.exp(-t3 / tau)),
                    upk * np.exp(-(t3 - D) / tau))
print("  数值 vs 分段解析最大偏差 = %.2e V" % np.max(np.abs(u3 - u3_exact)))
print("  峰值 %.6f V（理想 1 V，差 %.3f%%）；3tau 处 %.4f V"
      % (upk, (1 - upk) * 100, upk * np.exp(-3)))
print("  理想冲激响应 h(t) = (Q/C) e^(-t/tau) 与窄脉冲结果在图上几乎重合")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：作业数字预验证（Q6、Q7） ===")
# Q6：6 V 阶跃、R = 2k、C = 2 uF
tau6 = 2e3 * 2e-6
print("  Q6：tau = %.0f ms；1tau 值 = 6(1-e^-1) = %.3f V" % (tau6 * 1e3, 6 * (1 - np.exp(-1))))
# Q7：Q = 2 uC 注入 C = 0.5 uF
print("  Q7：冲激跳变 du = Q/C = %.0f V" % (2e-6 / 0.5e-6))

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：阶跃函数与阶跃响应 ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

ax1.plot([-2, 0], [0, 0], color="#1f5fa8", lw=2.4)
ax1.plot([0, 0], [0, 1], color="#1f5fa8", lw=2.4)
ax1.plot([0, 6], [1, 1], color="#1f5fa8", lw=2.4)
ax1.annotate("$t=0$：从 0 跳到 1", xy=(0.1, 0.5), xytext=(1.2, 0.38), fontsize=10,
             arrowprops=dict(arrowstyle="->", color="#c0392b"), color="#c0392b")
ax1.set_title("单位阶跃 $\\varepsilon(t)$：0 前为 0，0 后恒为 1", fontsize=11)
ax1.set_xlabel("时间 $t$（示意）")
ax1.set_ylabel("$\\varepsilon$")
ax1.set_ylim(-0.15, 1.3)
ax1.set_xlim(-2, 6)
ax1.grid(alpha=0.3)

ax2.plot(t * 1e3, u_exact, color="#1f5fa8", lw=2.4)
ax2.axhline(uc_inf, color="#999999", ls="--", lw=1.2)
ax2.plot([tau * 1e3], [uc_inf * (1 - np.exp(-1))], "o", color="#c0392b", ms=5)
ax2.annotate("1$\\tau$：%.2f V（63.2%%）" % (uc_inf * (1 - np.exp(-1))),
             xy=(tau * 1e3, uc_inf * (1 - np.exp(-1))), xytext=(2.8, 2.6), fontsize=10,
             color="#c0392b", arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax2.annotate("终值 6 V", xy=(4.2, 6.0), xytext=(3.4, 6.35), fontsize=10, color="#666666")
ax2.plot([0, tau * 1e3], [0, uc_inf], color="#2e7d32", lw=1.3, ls=":")
ax2.set_title("阶跃响应：$6(1-e^{-t/\\tau})$（12 V 阶跃接入）", fontsize=11)
ax2.set_xlabel("时间 $t$ / ms")
ax2.set_ylabel("$u_C$ / V")
ax2.set_ylim(-0.3, 6.8)
ax2.grid(alpha=0.3)

plt.tight_layout()
save_stem = "lec11_fig3_step"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 4：冲激的脉冲逼近与冲激响应 ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

# (a) 三个脉冲叠在起点：宽 2/1/0.5 us，高 0.5/1/2 A，面积恒为 1 uC
for D_us, h, cc in [(2.0, 0.5, "#2e7d32"), (1.0, 1.0, "#1f5fa8"), (0.5, 2.0, "#c0392b")]:
    ax1.plot([0, D_us, D_us, 0, 0], [0, 0, h, h, 0], lw=2.2, color=cc,
             label="宽 %.1f us，高 %.1f A" % (D_us, h))
ax1.legend(fontsize=9, loc="center right")
ax1.annotate("三条脉冲面积都 = 1 $\\mu$C\n宽度 → 0 的极限就是 $\\delta(t)$", xy=(0.35, 2.1),
             xytext=(1.15, 1.75), fontsize=10, color="#333333")
ax1.set_title("$\\delta(t)$ 的逼近：越窄越高，面积恒 1", fontsize=11)
ax1.set_xlabel("时间 $t$ / $\\mu$s")
ax1.set_ylabel("电流 $i$ / A")
ax1.set_xlim(-0.3, 3.2)
ax1.set_ylim(0, 2.5)
ax1.grid(alpha=0.3)

# (b) 冲激响应：理想 e^(-t/tau) 与 1 us 窄脉冲数值
ax2.plot(t3 * 1e3, np.exp(-t3 / tau), color="#1f5fa8", lw=2.4, label="理想冲激：$e^{-t/\\tau}$")
ax2.plot(t3 * 1e3, u3, color="#c0392b", lw=1.5, ls="--", label="窄脉冲（$\\Delta$ = 1 $\\mu$s）数值")
ax2.plot([0], [1.0], "o", color="#2e7d32", ms=6)
ax2.annotate("跳变 $Q/C$ = 1 V（宽度越窄越贴近）", xy=(0.06, 1.0), xytext=(1.1, 0.82),
             fontsize=10, color="#2e7d32", arrowprops=dict(arrowstyle="->", color="#2e7d32"))
ax2.legend(fontsize=9, loc="upper right")
ax2.set_title("冲激响应：$u_C$ 一步顶上 1 V，再按 $\\tau$ 衰减", fontsize=11)
ax2.set_xlabel("时间 $t$ / ms")
ax2.set_ylabel("$u_C$ / V")
ax2.set_ylim(-0.05, 1.15)
ax2.grid(alpha=0.3)

plt.tight_layout()
save_stem = "lec11_fig4_impulse"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec11-02 完成。")