# =====================================================================
# lec12-02 二阶电路：能量视角与作业预验证
#          （第 12 讲 §3-§4 数值实验；图 3 能量交换）
# 规模纪律：总耗时 < 10 秒（RK4 dt=1us + 一张图）。
#
# 运行例延续（欠阻尼 R = 28、L = 50 mH、C = 20 uF、u_C(0) = 10 V）：
#   实验 1：能量守恒核账——w_C + w_L + w_R耗散 = W(0) = 1000 uJ；
#           w_C 与 w_L 此消彼长；i=0 时有 w_L=0 的漂亮锚点。
#   实验 2：生成 figures/lec12_fig3_energy.svg/.png（能量交换双面板）。
#   实验 3：作业数字预验证（Q2-Q4、Q6-Q8）。
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

L, C, U0, R = 50e-3, 20e-6, 10.0, 28.0

def rk4_rlc(Rv, T=12e-3, dt=1e-6):
    n = int(round(T / dt)) + 1
    t = np.arange(n) * dt
    u = np.zeros(n)
    i = np.zeros(n)
    u[0] = U0
    for k in range(1, n):
        ku1, ki1 = -i[k - 1] / C, (u[k - 1] - Rv * i[k - 1]) / L
        ku2, ki2 = -(i[k - 1] + ki1 * dt / 2) / C, (u[k - 1] + ku1 * dt / 2 - Rv * (i[k - 1] + ki1 * dt / 2)) / L
        ku3, ki3 = -(i[k - 1] + ki2 * dt / 2) / C, (u[k - 1] + ku2 * dt / 2 - Rv * (i[k - 1] + ki2 * dt / 2)) / L
        ku4, ki4 = -(i[k - 1] + ki3 * dt) / C, (u[k - 1] + ku3 * dt - Rv * (i[k - 1] + ki3 * dt)) / L
        u[k] = u[k - 1] + (ku1 + 2 * ku2 + 2 * ku3 + ku4) * dt / 6
        i[k] = i[k - 1] + (ki1 + 2 * ki2 + 2 * ki3 + ki4) * dt / 6
    return t, u, i

print("=== 实验 1：能量守恒核账（欠阻尼 R=28） ===")
t, u, i = rk4_rlc(R)
wC = 0.5 * C * u ** 2
wL = 0.5 * L * i ** 2
wR = np.concatenate(([0.0], np.cumsum((i[1:] ** 2 + i[:-1] ** 2) / 2 * R * (t[1] - t[0]))))  # 梯形法
W0 = 0.5 * C * U0 ** 2
resid = np.max(np.abs(wC + wL + wR - W0))
print("  W(0) = 1/2 C U0^2 = %.0f uJ；全程最大残差 = %.2e uJ" % (W0 * 1e6, resid * 1e6))
print("  12 ms 末：w_C + w_L = %.4f uJ，w_R 耗散 = %.2f uJ" % ((wC[-1] + wL[-1]) * 1e6, wR[-1] * 1e6))
# 特征点 1：i 峰值（w_L 峰）
k_ipk = int(np.argmax(i))
print("  i 峰值 t = %.3f ms：w_L = %.0f uJ（峰）、w_C = %.0f uJ、w_R = %.0f uJ"
      % (t[k_ipk] * 1e3, wL[k_ipk] * 1e6, wC[k_ipk] * 1e6, wR[k_ipk] * 1e6))
# 特征点 2：首谷（i=0 -> w_L=0）
k_val = int(np.argmin(u))
print("  首谷 t = %.3f ms：i = %.1e A -> w_L = %.0f uJ、w_C = %.0f uJ、w_R = %.0f uJ"
      % (t[k_val] * 1e3, i[k_val], wL[k_val] * 1e6, wC[k_val] * 1e6, wR[k_val] * 1e6))
print("  -> 能量在 C、L 之间来回倒腾；总账（w_C+w_L+w_R）恒等于 1000 uJ")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：生成图 3（能量交换双面板） ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.3))
ax1.plot(t * 1e3, wC * 1e6, color="#1f5fa8", lw=2.2, label="$w_C = \\frac{1}{2}Cu_C^2$")
ax1.plot(t * 1e3, wL * 1e6, color="#c0392b", lw=2.2, label="$w_L = \\frac{1}{2}Li_L^2$")
ax1.plot([t[k_ipk] * 1e3], [wL[k_ipk] * 1e6], "o", color="#c0392b", ms=5)
ax1.annotate("$w_L$ 峰 472 $\\mu$J", xy=(t[k_ipk] * 1e3, wL[k_ipk] * 1e6), xytext=(2.2, 640),
             fontsize=10, color="#c0392b", arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax1.annotate("谷点 $i=0$：$w_L=0$", xy=(t[k_val] * 1e3, 0), xytext=(4.6, 210),
             fontsize=10, color="#1f5fa8", arrowprops=dict(arrowstyle="->", color="#1f5fa8"))
ax1.set_title("此消彼长：能量在 $C$ 与 $L$ 之间来回", fontsize=11)
ax1.set_xlabel("时间 $t$ / ms")
ax1.set_ylabel("能量 / $\\mu$J")
ax1.set_ylim(-30, 1080)
ax1.legend(fontsize=9, loc="upper right")
ax1.grid(alpha=0.3)

ax2.plot(t * 1e3, (wC + wL) * 1e6, color="#1f5fa8", lw=2.2, label="储能 $w_C + w_L$")
ax2.plot(t * 1e3, wR * 1e6, color="#c0392b", lw=2.2, label="耗散 $w_R = \\int i^2 R\\,dt$")
ax2.axhline(W0 * 1e6, color="#999999", ls="--", lw=1.2, label="总账 1000 $\\mu$J")
ax2.set_title("互补：储能单调转出，耗散单调收入", fontsize=11)
ax2.set_xlabel("时间 $t$ / ms")
ax2.set_ylabel("能量 / $\\mu$J")
ax2.set_ylim(-30, 1080)
ax2.legend(fontsize=9, loc="center right")
ax2.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec12_fig3_energy"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 实验 3：作业数字预验证 ===")
# Q2：过阻尼 R=125，u(1ms) = (40/3)e^(-0.5) - (10/3)e^(-2)
u2q = (40 / 3) * np.exp(-0.5) - (10 / 3) * np.exp(-2)
print("  Q2：u_C(1 ms) = (40/3)e^-0.5 - (10/3)e^-2 = %.3f V" % u2q)
# Q3：欠阻尼首谷/次峰/T_d（与实验 1 对照）
print("  Q3：首谷 -4.000 V @ 3.272 ms；次峰 +1.600 V @ 6.545 ms；T_d = 6.545 ms")
# Q4：临界 R=100，u(1ms) = 20e^-1；单调无超调
print("  Q4：u_C(1 ms) = 20 e^-1 = %.3f V；du/dt = -10^7 t e^(-1000t) <= 0（单调）"
      % (20 * np.exp(-1)))
# Q6：临界电阻
rc = 2 * np.sqrt(L / C)
print("  Q6：R_crit = 2 sqrt(L/C) = %.0f ohm" % rc)
# Q8：两种无振荡方案的收场速度（掉到 0.5 V 的时间）
t_c, u_c, _ = rk4_rlc(100.0)
t_o, u_o, _ = rk4_rlc(125.0)
t_c05 = t_c[int(np.argmax(u_c < 0.5))] * 1e3
t_o05 = t_o[int(np.argmax(u_o < 0.5))] * 1e3
print("  Q8：掉到 0.5 V 的时间——临界 R=100：%.1f ms；过阻尼 R=125：%.1f ms（都无振荡，过阻尼更慢）"
      % (t_c05, t_o05))

print()
print("[DONE] lec12-02 完成。")