# =====================================================================
# lec02-02 元件档案扫描：四类元件的伏安关系取样（第 02 讲 §1 / §2）
# 规模纪律：总耗时 < 5 秒（纯算术 + 一张四联小图）。
# 方法：
#   实验 1：四类档案取样表——电阻（线性）、理想电压源（水平）、
#           理想电流源（竖直）、实际电池（下垂）。
#   实验 2：实际电池下垂量差分核对（每 +0.5 A 端电压恰好掉 -0.25 V）。
#   并生成 figures/lec02_fig2_iv_profiles.svg 与 .png（2×2 档案总览）。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
# =====================================================================
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../electric_circuits
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# ---------------------------------------------------------------------
print("=== 实验 1：四类元件档案取样 ===")
print("  1) 电阻 R = 1 kΩ：u = R i（线性——比例档案）")
for i_mA in [0, 1, 2, 3, 4, 5]:
    print("     i = %d mA  ->  u = %.1f V" % (i_mA, i_mA * 1.0))
print("  2) 理想电压源 U_S = 9 V：u 恒 9 V（与 i 无关）")
for i_mA in [0, 1, 5, 20]:
    print("     i = %d mA  ->  u = 9 V（电流由外电路定）" % i_mA)
print("  3) 理想电流源 I_S = 2 mA：i 恒 2 mA（与 u 无关）")
for u_V in [0, 1, 5, 20]:
    print("     u = %d V  ->  i = 2 mA（电压由外电路定）" % u_V)
print("  4) 实际电池 U_S = 3 V, R_i = 0.5 Ω：u = U_S - R_i i（下垂档案）")
for i_A in [0.0, 0.5, 1.0, 2.0]:
    print("     i = %.1f A  ->  u = %.2f V" % (i_A, 3.0 - 0.5 * i_A))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：实际电池下垂量差分核对 ===")
U_S, R_i = 3.0, 0.5
is_ = [0.0, 0.5, 1.0, 2.0]
us = [U_S - R_i * i for i in is_]
for k in range(1, len(is_)):
    du = us[k] - us[k - 1]
    di = is_[k] - is_[k - 1]
    print("  i: %.1f -> %.1f A：端电压 %+.2f V（= -R_i x %.1f A = %+.2f V）"
          % (is_[k - 1], is_[k], du, di, -R_i * di))
res = max(abs(u - (U_S - R_i * i)) for u, i in zip(us, is_))
print("  回代残差（表值与公式的最大偏差）= %.2e V" % res)
print("  -> 下垂档案核对一致：每 +0.5 A，端电压恰好掉 0.25 V。")

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：四类档案总览（2x2） ===")
fig, axes = plt.subplots(2, 2, figsize=(6.8, 5.4), dpi=120)
C1, C2 = "#2471a3", "#c0392b"

ax = axes[0][0]
ax.plot([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], color=C1, lw=2.2)
ax.set_title("电阻（1 kΩ）：u = Ri", fontsize=11)
ax.annotate("i、u 互推，取哪一点都行", xy=(2.6, 2.2), fontsize=9, color=C1)
ax.set_xlim(0, 5.6)
ax.set_ylim(0, 5.6)

ax = axes[0][1]
ax.plot([0, 10], [9, 9], color=C1, lw=2.2)
ax.set_title("理想电压源（9 V）：u 恒 9 V", fontsize=11)
ax.annotate("电压钉死，电流自由\n（i 由外电路定）", xy=(3.2, 5.6), fontsize=9, color=C1)
ax.set_xlim(0, 10.4)
ax.set_ylim(0, 10.6)

ax = axes[1][0]
ax.plot([2, 2], [0, 8], color=C1, lw=2.2)
ax.set_title("理想电流源（2 mA）：i 恒 2 mA", fontsize=11)
ax.annotate("电流钉死，电压自由\n（u 由外电路定）", xy=(2.5, 4.6), fontsize=9, color=C1)
ax.set_xlim(0, 6.4)
ax.set_ylim(0, 8.4)

ax = axes[1][1]
ii = [0.0, 0.5, 1.0, 1.5, 2.0]
uu = [U_S - R_i * i for i in ii]
ax.plot(ii, uu, color=C2, lw=2.2)
ax.set_title("实际电池（3 V，0.5 Ω）：下垂档案", fontsize=11)
ax.annotate("供流越大，端电压越低", xy=(0.12, 1.5), fontsize=9, color=C2)
ax.set_xlim(0, 2.2)
ax.set_ylim(0, 3.4)

for ax in axes.flat:
    ax.set_ylabel("电压 u / V", fontsize=9)
    ax.grid(True, alpha=0.3)
axes[0][0].set_xlabel("电流 i / mA", fontsize=9)
axes[0][1].set_xlabel("电流 i / mA", fontsize=9)
axes[1][0].set_xlabel("电流 i / mA", fontsize=9)
axes[1][1].set_xlabel("电流 i / A", fontsize=9)

fig.suptitle("元件档案总览：四种性格", fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec02_fig2_iv_profiles.svg"))
fig.savefig(os.path.join(FIGDIR, "lec02_fig2_iv_profiles.png"))
print("[OK] figures/lec02_fig2_iv_profiles.svg 与 .png 已生成。")