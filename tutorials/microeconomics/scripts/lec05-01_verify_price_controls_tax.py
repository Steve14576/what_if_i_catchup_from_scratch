# =====================================================================
# lec05-01 价格管制与税负归宿（第 05 讲 §1 / §3 / §4 / §5）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   实验 1：租金上限（Qd = 300-5P；Qs = 10P-300）。
#           预期：原均衡 (40, 100)；上限 35 -> 短缺 75（成交 50）；
#           上限 45 -> 无约束（结果不变）。
#   实验 2：最低工资（Ld = 120-4W；Ls = 6W-30）。
#           预期：原均衡 (15, 60)；下限 18 -> 就业 48、意愿 78、失业 30；
#           下限 12 -> 无约束。
#   实验 3：税收等价性（Qd = 200-10P；Qs = 10P-100；t=4）。
#           预期：两种征法同解：P_b=17, P_s=13, Q=30；各担 2。
#   实验 4：弹性决定归宿对照（t=2）：
#           甲（需求平、供给陡）：买 +0.5、卖 -1.5（卖方担 75%）；
#           乙（需求陡、供给平）：买 +1.5、卖 -0.5（买方担 75%）。
#   生成 figures/lec05_fig1_price_ceiling.svg/.png、
#        figures/lec05_fig2_min_wage.svg/.png、
#        figures/lec05_fig3_tax_incidence.svg/.png。
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


def eq(A_d, B_d, A_s, B_s):
    P = (A_d - A_s) / (B_d + B_s)
    return P, A_d - B_d * P


# ---------------------------------------------------------------------
print("=== 实验 1：租金上限（Qd = 300 - 5P；Qs = 10P - 300） ===")
P_eq, Q_eq = eq(300, 5, -300, 10)
print("  原均衡：P* = %.0f（百元/月），Q* = %.0f（百套）" % (P_eq, Q_eq))
for cap in [35.0, 45.0]:
    qd = 300 - 5 * cap
    qs = 10 * cap - 300
    if cap >= P_eq:
        print("  上限 %.0f：高于均衡价 -> 无约束，市场仍在 (%.0f, %.0f)" % (cap, P_eq, Q_eq))
    else:
        short = qd - qs
        print("  上限 %.0f：需求量 %.0f，供给量 %.0f -> 成交 = 供给量 %.0f，短缺 %.0f 套" %
              (cap, qd, qs, qs, short))
print("  -> 结论：上限只有低于均衡价才'有效'；有效的上限 = 短缺制造机。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：最低工资（Ld = 120 - 4W；Ls = 6W - 30） ===")
W_eq, L_eq = eq(120, 4, -30, 6)
print("  原均衡：W* = %.0f（元/小时），L* = %.0f（万人）" % (W_eq, L_eq))
for floorv in [18.0, 12.0]:
    ld = 120 - 4 * floorv
    ls = 6 * floorv - 30
    if floorv <= W_eq:
        print("  最低工资 %.0f：低于均衡 -> 无约束，仍在 (%.0f, %.0f)" % (floorv, W_eq, L_eq))
    else:
        print("  最低工资 %.0f：就业量(需求) %.0f，愿意工作(供给) %.0f -> 失业缺口 %.0f 万人" %
              (floorv, ld, ls, ls - ld))
print("  -> 结论：有约束的最低工资 = 劳动供给过剩（失业缺口）。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：税收等价性（Qd = 200 - 10P_b；Qs = 10P_s - 100；t = 4） ===")
P0, Q0 = eq(200, 10, -100, 10)
print("  无税均衡：P* = %.0f，Q* = %.0f" % (P0, Q0))
t = 4.0
# 路线 A：向卖者征（卖方到手 P_s = P_b - t）：解 Qd(P_b) = Qs(P_b - t)
# 200 - 10 P_b = 10 (P_b - 4) - 100  ->  340 = 20 P_b
Pb_a = (200 + 100 + 10 * t) / (10 + 10)
Ps_a = Pb_a - t
Q_a = 200 - 10 * Pb_a
# 路线 B：向买者征（买方支付 P_b = P_s + t）：解 Qd(P_s + t) = Qs(P_s)
# 200 - 10 (P_s + 4) = 10 P_s - 100  ->  260 = 20 P_s
Ps_b = (200 - 10 * t + 100) / (10 + 10)
Pb_b = Ps_b + t
Q_b = 200 - 10 * Pb_b
print("  A 向卖者征：P_b = %.1f（买者付），P_s = %.1f（卖者得），Q = %.0f" % (Pb_a, Ps_a, Q_a))
print("  B 向买者征：P_b = %.1f（买者付），P_s = %.1f（卖者得），Q = %.0f" % (Pb_b, Ps_b, Q_b))
print("  买方多付 = %.1f，卖方少收 = %.1f，两者之和 = %.1f = 税额 t" % (Pb_a - P0, P0 - Ps_a, t))
print("  -> 结论：向谁征完全等价；楔子由买卖双方按弹性分摊（本例各半）。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：弹性决定归宿（t = 2，两个市场原均衡都是 (10, 20)） ===")


def tax_incidence(A_d, B_d, A_s, B_s, t, label):
    P0, Q0 = eq(A_d, B_d, A_s, B_s)
    # Qd(Pb) = A_d - B_d*Pb ; Qs(Pb - t) = A_s + B_s*(Pb - t)
    # A_d - B_d Pb = A_s + B_s Pb - B_s t  ->  Pb = (A_d - A_s + B_s t)/(B_d + B_s)
    Pb = (A_d - A_s + B_s * t) / (B_d + B_s)
    Ps = Pb - t
    Q = A_d - B_d * Pb
    dP_b = Pb - P0
    dP_s = P0 - Ps
    share = dP_b / t * 100
    print("  %s：原均衡 (%.0f, %.0f) -> P_b = %.1f，P_s = %.1f，Q = %.0f" % (label, P0, Q0, Pb, Ps, Q))
    print("     买方多付 %+.1f，卖方少收 %+.1f -> 买方承担 %.0f%%、卖方承担 %.0f%%" %
          (dP_b, -dP_s, share, 100 - share))
    return P0, Q0, Pb, Ps, Q


Pa = tax_incidence(80, 6, 0, 2, 2.0, "甲市场（Qd=80-6P；Qs=2P）需求平、供给陡")
Pb_ = tax_incidence(40, 2, -40, 6, 2.0, "乙市场（Qd=40-2P；Qs=6P-40）需求陡、供给平")
print("  -> 结论：谁更缺乏弹性（跑不掉），谁就承担更多税负。")

# ---------------------------------------------------------------------
# 图 1：价格上限（租金市场）
fig, ax = plt.subplots(figsize=(6.8, 4.6), dpi=120)
Ps = list(range(15, 61))  # 租金价 P：15 到 60（百元/月）
ax.plot([300 - 5 * p for p in Ps], Ps, color="#c0392b", lw=2, label="需求 D")
ax.plot([10 * p - 300 for p in Ps], Ps, color="#2471a3", lw=2, label="供给 S")
ax.plot([Q_eq], [P_eq], "o", color="#7f8c8d", ms=8)
ax.annotate("均衡 (100, 40)", xy=(Q_eq, P_eq), xytext=(108, 45.5), fontsize=10, color="#7f8c8d")
ax.plot([0, 130], [35, 35], color="#e67e22", lw=2, ls="--")
ax.annotate("价格上限 35", xy=(6, 35), xytext=(6, 31), fontsize=10, color="#e67e22")
ax.annotate("", xy=(125, 33.4), xytext=(50, 33.4), arrowprops=dict(arrowstyle="<->", color="#e67e22", lw=1.6))
ax.annotate("短缺 75 套", xy=(87, 32.2), xytext=(75, 30.5), fontsize=10, color="#e67e22")
ax.set_xlabel("住房数量 Q（百套）")
ax.set_ylabel("租金 P（百元/月）")
ax.set_title("价格上限：横在均衡价下方的一根线")
ax.set_xlim(0, 180)
ax.set_ylim(0, 60)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec05_fig1_price_ceiling.svg"))
fig.savefig(os.path.join(FIGDIR, "lec05_fig1_price_ceiling.png"))

# ---------------------------------------------------------------------
# 图 2：最低工资（劳动市场）
fig2, ax2 = plt.subplots(figsize=(6.8, 4.6), dpi=120)
Ws = [x / 10 for x in range(50, 321)]
ax2.plot([120 - 4 * w for w in Ws], Ws, color="#c0392b", lw=2, label="劳动需求")
ax2.plot([6 * w - 30 for w in Ws], Ws, color="#2471a3", lw=2, label="劳动供给")
ax2.plot([L_eq], [W_eq], "o", color="#7f8c8d", ms=8)
ax2.annotate("均衡 (60, 15)", xy=(L_eq, W_eq), xytext=(64, 13.4), fontsize=10, color="#7f8c8d")
ax2.plot([0, 100], [18, 18], color="#e67e22", lw=2, ls="--")
ax2.annotate("最低工资 18", xy=(5, 18), xytext=(5, 14.5), fontsize=10, color="#e67e22")
ax2.annotate("", xy=(78, 19), xytext=(48, 19), arrowprops=dict(arrowstyle="<->", color="#e67e22", lw=1.6))
ax2.annotate("失业缺口 30 万人", xy=(40, 20), fontsize=10, color="#e67e22")
ax2.set_xlabel("劳动量 L（万人）")
ax2.set_ylabel("工资 W（元/小时）")
ax2.set_title("价格下限：横在均衡价上方的一根线")
ax2.set_xlim(0, 110)
ax2.set_ylim(5, 32)
ax2.legend(loc="upper right", fontsize=9)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec05_fig2_min_wage.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec05_fig2_min_wage.png"))

# ---------------------------------------------------------------------
# 图 3：税收归宿双联（甲 / 乙）
fig3, axes = plt.subplots(1, 2, figsize=(11.2, 4.5), dpi=120)
specs = [
    (axes[0], 80, 6, 0, 2, "甲：需求平、供给陡 -> 卖方担 75%"),
    (axes[1], 40, 2, -40, 6, "乙：需求陡、供给平 -> 买方担 75%"),
]
Px = [x / 10 for x in range(0, 281)]
for ax3, A_d, B_d, A_s, B_s, tt in specs:
    P0, Q0, Pbx, Psx, Qx = None, None, None, None, None
    P0, Q0 = eq(A_d, B_d, A_s, B_s)
    Pbx = (A_d - A_s + B_s * 2.0) / (B_d + B_s)
    Psx = Pbx - 2.0
    Qx = A_d - B_d * Pbx
    ax3.plot([A_d - B_d * p for p in Px], Px, color="#c0392b", lw=2, label="需求 D")
    ax3.plot([A_s + B_s * p for p in Px], Px, color="#bdc3c7", lw=1.8, ls="--", label="原供给 S")
    ax3.plot([A_s + B_s * (p - 2.0) for p in Px], Px, color="#2471a3", lw=2, label="征税后供给 S+t")
    ax3.plot([Qx], [Pbx], "ko", ms=7)
    ax3.plot([Qx], [Psx], "ko", ms=7)
    ax3.plot([Qx, Qx], [Psx, Pbx], color="#e67e22", lw=2.5)
    ax3.annotate("楔子 t=2", xy=(Qx + 3.5, (Pbx + Psx) / 2), fontsize=9.5, color="#e67e22")
    ax3.set_title(tt, fontsize=11)
    ax3.set_xlabel("数量 Q")
    ax3.set_ylabel("价格 P")
    ax3.set_xlim(0, 28)
    ax3.set_ylim(0, 15)
    ax3.legend(loc="lower right", fontsize=8)
fig3.suptitle("同样的税，不同的命运：弹性决定谁掏钱", fontsize=12)
fig3.tight_layout(rect=[0, 0, 1, 0.94])
fig3.savefig(os.path.join(FIGDIR, "lec05_fig3_tax_incidence.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec05_fig3_tax_incidence.png"))

print()
print("[OK] figures/lec05_fig1_price_ceiling、lec05_fig2_min_wage、lec05_fig3_tax_incidence 已生成。")