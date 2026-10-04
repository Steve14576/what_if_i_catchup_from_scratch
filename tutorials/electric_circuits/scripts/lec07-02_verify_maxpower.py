# =====================================================================
# lec07-02 最大功率传输：匹配条件、P_max、效率两本账 + 扫描曲线
#          （第 07 讲 §4；图 2 双面板曲线）
# 规模纪律：总耗时 < 10 秒（纯算术 + 一张双面板曲线图）。
# 方法：
#   实验 1：04 电路戴维南盒（U_oc = 32/3 V、R_th = 2/3 Ω）的功率扫描：
#           RL = 2/3 Ω 处 P_max = 128/3 ≈ 42.67 W；RL = 2 Ω（原负载）处 32 W；
#           对称点 0.5 与 8/9 同为 2048/49 ≈ 41.80 W；极点处有限差分斜率 ≈ 0。
#   实验 2：效率表：匹配点 η = 50%；RL = 2 Ω 时 η = 75%；强调"两本账"。
#   实验 3：作业 Q3 数字预验证（18V/3Ω + 6V/6Ω 的盒子：RL = 2 匹配 24.5 W、RL = 6 时 18.375 W）。
#   并生成 figures/lec07_fig2_maxpower.svg/.png（P(RL) 与 η(RL) 双面板）。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
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

U_oc = 32.0 / 3.0
R_th = 2.0 / 3.0
P = lambda RL: U_oc ** 2 * RL / (R_th + RL) ** 2
eta = lambda RL: RL / (R_th + RL)

# ---------------------------------------------------------------------
print("=== 实验 1：功率扫描（04 电路的戴维南盒） ===")
P_max = U_oc ** 2 / (4 * R_th)
print("  理论：RL = R_th = %.4f Ω 时 P_max = U_oc^2/(4 R_th) = %.4f W" % (R_th, P_max))
for RL in [0.1, 0.5, 2.0 / 3.0, 1.0, 2.0, 8.0 / 9.0, 4.0]:
    print("  RL = %.4f Ω：P = %.4f W，η = %.1f%%" % (RL, P(RL), 100 * eta(RL)))
print("  对称检查：P(0.5) = %.4f W，P(8/9) = %.4f W（RL·RL' = R_th^2 的对偶点相等）"
      % (P(0.5), P(8.0 / 9.0)))
# 极点有限差分
h = 1e-6
slope = (P(R_th + h) - P(R_th - h)) / (2 * h)
print("  极点斜率（中心差分）：%.2e -> 匹配点确为极值" % slope)

# ---------------------------------------------------------------------
print()
print("=== 实验 2：两本账（功率 vs 效率） ===")
print("  匹配点 RL = %.2f Ω：P = %.2f W（最大），η = %.0f%%（只有一半给了负载！）"
      % (R_th, P_max, 100 * eta(R_th)))
print("  原负载 RL = 2 Ω：P = %.0f W（比最大小 %.2f W），η = %.0f%%"
      % (P(2.0), P_max - P(2.0), 100 * eta(2.0)))
print("  高效率点 RL = 6 Ω：P = %.3f W，η = %.0f%%（效率上去、功率下来了）"
      % (P(6.0), 100 * eta(6.0)))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：作业 Q3 数字预验证（18V/3Ω + 6V/6Ω） ===")
U2, R2 = 14.0, 2.0
P2 = lambda RL: U2 ** 2 * RL / (R2 + RL) ** 2
print("  匹配点 RL = %.0f Ω：P_max = %.1f W，η = 50%%" % (R2, U2 ** 2 / (4 * R2)))
print("  RL = 6 Ω：P = %.3f W，η = %.0f%%" % (P2(6.0), 100 * 6 / (2 + 6)))

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：P(RL) 与 η(RL) 双面板 ===")
rl = np.linspace(0.02, 4.0, 600)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
ax1.plot(rl, P(rl), color="#1f5fa8", lw=2.2)
ax1.axvline(R_th, color="#999999", ls="--", lw=1)
ax1.plot([R_th], [P_max], "o", color="#c0392b", ms=6)
ax1.annotate("匹配点：$R_L$ = 2/3 Ω\n$P_{max}$ ≈ 42.67 W，η = 50%",
             xy=(R_th, P_max), xytext=(1.35, 40.0), fontsize=10,
             arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax1.plot([2.0], [P(2.0)], "s", color="#2e7d32", ms=6)
ax1.annotate("原负载 2 Ω：32 W，η = 75%",
             xy=(2.0, P(2.0)), xytext=(2.35, 34.0), fontsize=10,
             arrowprops=dict(arrowstyle="->", color="#2e7d32"))
ax1.set_xlabel("负载 $R_L$ / Ω")
ax1.set_ylabel("负载功率 $P$ / W")
ax1.set_title("功率曲线：匹配点才是最高")
ax1.grid(alpha=0.3)

ax2.plot(rl, 100 * eta(rl), color="#8e44ad", lw=2.2)
ax2.axvline(R_th, color="#999999", ls="--", lw=1)
ax2.plot([R_th], [50], "o", color="#c0392b", ms=6)
ax2.annotate("匹配点：η = 50%", xy=(R_th, 50), xytext=(1.15, 38), fontsize=10,
             arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax2.plot([2.0], [75], "s", color="#2e7d32", ms=6)
ax2.annotate("原负载 2 Ω：η = 75%", xy=(2.0, 75), xytext=(2.1, 60), fontsize=10,
             arrowprops=dict(arrowstyle="->", color="#2e7d32"))
ax2.set_xlabel("负载 $R_L$ / Ω")
ax2.set_ylabel("效率 $\\eta$ / %")
ax2.set_title("效率曲线：越高越好，但和功率不是一本账")
ax2.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec07_fig2_maxpower"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec07-02 完成。")