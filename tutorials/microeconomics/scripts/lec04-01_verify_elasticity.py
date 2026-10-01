# =====================================================================
# lec04-01 弹性、总收入与丰收悖论（第 04 讲 §2 / §4 / §7）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   实验 1：中点法 vs 普通百分比法。预期：普通法两个方向给不同答案
#           （1.500 vs 2.571），中点法两个方向都给 1.941。
#   实验 2：沿直线需求 Qd = 100 - 2P 扫描点弹性与总收入。
#           预期：E=1 出现在 P=25（Q=50），恰是 TR 的最大点（1250）。
#   实验 3：丰收悖论双市场对照（供给右移 +40）：
#           市场 A（缺弹性，E~0.45）：收入 1100 -> 960（减收）；
#           市场 B（富弹性，E~1.67）：收入 1350 -> 1430（增收）。
#   生成 figures/lec04_fig1_three_cases.svg/.png、
#        figures/lec04_fig2_tr_elasticity.svg/.png、
#        figures/lec04_fig3_harvest.svg/.png。
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

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../microeconomics
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# ---------------------------------------------------------------------
print("=== 实验 1：中点法 vs 普通百分比法（奶茶：10 元->12 元；100 杯->70 杯） ===")
P1, Q1 = 10.0, 100.0
P2, Q2 = 12.0, 70.0
e_ab = abs(((Q2 - Q1) / Q1) / ((P2 - P1) / P1))
e_ba = abs(((Q1 - Q2) / Q2) / ((P1 - P2) / P2))
print("  普通法 A->B：价格 +%.2f%%，数量 %.2f%%，|E| = %.3f" %
      ((P2 - P1) / P1 * 100, (Q2 - Q1) / Q1 * 100, e_ab))
print("  普通法 B->A：价格 %.2f%%，数量 +%.2f%%，|E| = %.3f" %
      ((P1 - P2) / P2 * 100, (Q1 - Q2) / Q2 * 100, e_ba))
e_mid = abs(((Q2 - Q1) / ((Q1 + Q2) / 2)) / ((P2 - P1) / ((P1 + P2) / 2)))
print("  中点法（两向相同）：价格 %.2f%%，数量 %.2f%%，|E| = %.3f" %
      ((P2 - P1) / ((P1 + P2) / 2) * 100, (Q2 - Q1) / ((Q1 + Q2) / 2) * 100, e_mid))
print("  -> 结论：普通法同一个来回给出两个答案（1.500 vs 2.571）；中点法给出唯一的 1.941。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：沿直线需求 Qd = 100 - 2P 扫描点弹性与总收入 ===")
print("   P  |   Q  | 点弹性 E | 总收入 TR=P*Q")
best_P, best_TR = 0, 0.0
rows = []
for P in range(5, 50, 5):
    Q = 100 - 2 * P
    E = 2 * P / Q          # |dQ/dP| * P/Q，|dQ/dP|=2
    TR = P * Q
    rows.append((P, Q, E, TR))
    if TR > best_TR:
        best_P, best_TR = P, TR
for P, Q, E, TR in rows:
    print("  %3d | %4d |  %6.3f  |  %6d" % (P, Q, E, TR))
print("  总收入最大点在 P = %d（TR = %d 元），对应点弹性 E = %.3f = 1" % (best_P, best_TR, 2 * best_P / (100 - 2 * best_P)))
print("  -> 结论：E=1 的位置恰好是 TR 的峰顶；E>1 的上段涨价减收、E<1 的下段涨价增收。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：丰收悖论双市场对照（供给在每个价位 +40） ===")


def eq(A_d, B_d, A_s, B_s):
    P = (A_d - A_s) / (B_d + B_s)
    return P, A_d - B_d * P


print("  市场 A（小麦：需求缺乏弹性 Qd = 160 - 5P；Qs = 15P - 40）")
Pa1, Qa1 = eq(160, 5, -40, 15)
Pa2, Qa2 = eq(160, 5, 0, 15)   # 丰收：Qs = 15P - 40 + 40 = 15P
Ea = 5 * Pa1 / Qa1
print("    原均衡：P=%.0f，Q=%.0f，收入=%.0f，均衡点弹性 E=%.3f" % (Pa1, Qa1, Pa1 * Qa1, Ea))
print("    丰收后：P=%.0f，Q=%.0f，收入=%.0f" % (Pa2, Qa2, Pa2 * Qa2))
print("    价格 %.1f%%，数量 +%.1f%%，收入 %.1f%%" %
      ((Pa2 - Pa1) / Pa1 * 100, (Qa2 - Qa1) / Qa1 * 100, (Pa2 * Qa2 - Pa1 * Qa1) / (Pa1 * Qa1) * 100))

print("  市场 B（对照：需求富有弹性 Qd = 240 - 10P；Qs = 10P - 60）")
Pb1, Qb1 = eq(240, 10, -60, 10)
Pb2, Qb2 = eq(240, 10, -20, 10)   # 丰收：Qs = 10P - 60 + 40 = 10P - 20
Eb = 10 * Pb1 / Qb1
print("    原均衡：P=%.0f，Q=%.0f，收入=%.0f，均衡点弹性 E=%.3f" % (Pb1, Qb1, Pb1 * Qb1, Eb))
print("    丰收后：P=%.0f，Q=%.0f，收入=%.0f" % (Pb2, Qb2, Pb2 * Qb2))
print("    价格 %.1f%%，数量 +%.1f%%，收入 +%.1f%%" %
      ((Pb2 - Pb1) / Pb1 * 100, (Qb2 - Qb1) / Qb1 * 100, (Pb2 * Qb2 - Pb1 * Qb1) / (Pb1 * Qb1) * 100))
print("  -> 结论：同样的丰收（价格都跌），缺弹性市场收入跌、富弹性市场收入涨。")

# ---------------------------------------------------------------------
# 图 1：三个极端档位
fig, ax = plt.subplots(figsize=(6.8, 4.6), dpi=120)
ax.plot([80, 80], [1, 9], color="#c0392b", lw=2.4)
ax.annotate("完全无弹性 E=0\n（价格怎么变，量都不变）", xy=(80, 7.6), xytext=(84, 7.0), fontsize=10, color="#c0392b")
ax.plot([12, 128], [4, 4], color="#2471a3", lw=2.4)
ax.annotate("完全弹性 E 无穷大\n（价格稍高就没人买）", xy=(80, 4), xytext=(93, 5.2), fontsize=10, color="#2471a3")
qq = [200 / p for p in [x / 10 for x in range(22, 91)]]
pp = [x / 10 for x in range(22, 91)]
ax.plot(qq, pp, color="#2c3e50", lw=2.0, ls="--")
ax.annotate("单位弹性 E=1\n（沿曲线处处相等）", xy=(40, 5), xytext=(24, 8.2), fontsize=10, color="#2c3e50")
ax.set_xlabel("数量 Q")
ax.set_ylabel("价格 P")
ax.set_title("需求弹性的三个极端档位")
ax.set_xlim(0, 140)
ax.set_ylim(0, 10)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec04_fig1_three_cases.svg"))
fig.savefig(os.path.join(FIGDIR, "lec04_fig1_three_cases.png"))

# ---------------------------------------------------------------------
# 图 2：总收入与点弹性（上下双联）
fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.8, 6.4), dpi=120)
Ps = [x / 10 for x in range(0, 501)]
ax1.plot([100 - 2 * p for p in Ps], Ps, color="#c0392b", lw=2, label="需求 Q = 100 - 2P")
ax1.plot([50], [25], "ko", ms=9)
ax1.annotate("E = 1（中点）", xy=(50, 25), xytext=(56, 27.5), fontsize=10)
ax1.plot([50, 50], [0, 25], color="#7f8c8d", ls="--", lw=1)
ax1.plot([0, 50], [25, 25], color="#7f8c8d", ls="--", lw=1)
ax1.annotate("E > 1：富有弹性", xy=(30, 40), fontsize=10.5, color="#c0392b")
ax1.annotate("E < 1：缺乏弹性", xy=(70, 10), fontsize=10.5, color="#2471a3")
ax1.set_ylabel("价格 P")
ax1.set_xlabel("数量 Q")
ax1.set_xlim(0, 105)
ax1.set_ylim(0, 52)
ax1.legend(loc="upper right", fontsize=9)
ax1.set_title("同一条需求曲线：上段富有弹性、中点单位弹性、下段缺乏弹性", fontsize=11)

ax2.plot(Ps, [p * (100 - 2 * p) for p in Ps], color="#27ae60", lw=2.2)
ax2.plot([25], [1250], "ko", ms=9)
ax2.annotate("TR 峰顶 = 1250", xy=(25, 1250), xytext=(28, 900), fontsize=10)
ax2.plot([25, 25], [0, 1250], color="#7f8c8d", ls="--", lw=1)
ax2.set_xlabel("价格 P")
ax2.set_ylabel("总收入 TR")
ax2.set_xlim(0, 50)
ax2.set_ylim(0, 1400)
ax2.set_title("总收入曲线：涨价先增收、过了 E=1 反而减收", fontsize=11)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec04_fig2_tr_elasticity.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec04_fig2_tr_elasticity.png"))

# ---------------------------------------------------------------------
# 图 3：丰收悖论双市场对照
fig3, axes = plt.subplots(1, 2, figsize=(10.6, 4.4), dpi=120)
for ax3, tag, A_d, B_d, A_s1, B_s, A_s2, (Q1x, P1x), (Q2x, P2x), note in [
    (axes[0], "A", 160, 5, -40, 15, 0, (Qa1, Pa1), (Qa2, Pa2), "E~0.45：收入 1100 -> 960（减收）"),
    (axes[1], "B", 240, 10, -60, 10, -20, (Qb1, Pb1), (Qb2, Pb2), "E~1.67：收入 1350 -> 1430（增收）"),
]:
    ax3.plot([A_d - B_d * p for p in Ps], Ps, color="#c0392b", lw=2, label="需求 D")
    ax3.plot([A_s1 + B_s * p for p in Ps], Ps, color="#bdc3c7", lw=1.8, ls="--", label="原供给 S1")
    ax3.plot([A_s2 + B_s * p for p in Ps], Ps, color="#2471a3", lw=2, label="丰收后供给 S2")
    ax3.plot([Q1x], [P1x], "o", color="#7f8c8d", ms=8)
    ax3.plot([Q2x], [P2x], "ko", ms=8)
    ax3.annotate("(%.0f, %.0f)" % (Q1x, P1x), xy=(Q1x, P1x), xytext=(Q1x + 6, P1x + 1.4), fontsize=9, color="#7f8c8d")
    ax3.annotate("(%.0f, %.0f)" % (Q2x, P2x), xy=(Q2x, P2x), xytext=(Q2x + 6, P2x - 2.2), fontsize=9)
    ax3.set_title("市场 %s 丰收：%s" % (tag, note), fontsize=11)
    ax3.set_xlabel("数量 Q")
    ax3.set_ylabel("价格 P")
    ax3.set_xlim(0, 210)
    ax3.set_ylim(0, 22)
    ax3.legend(loc="upper right", fontsize=8)
fig3.suptitle("同样的丰收，两种命运：弹性决定果农收入", fontsize=12)
fig3.tight_layout(rect=[0, 0, 1, 0.94])
fig3.savefig(os.path.join(FIGDIR, "lec04_fig3_harvest.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec04_fig3_harvest.png"))

print()
print("[OK] figures/lec04_fig1_three_cases、lec04_fig2_tr_elasticity、lec04_fig3_harvest 已生成。")