# =====================================================================
# lec13-01 垄断的定价、福利代价与价格歧视（第 13 讲 §2-§6）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   主场景：反需求 P = 50-Q/2（MR = 50-Q）；MC = 10（常数，无固定成本简化）。
#   实验 1：收入-MR 表（Q 0..80）：垄断点 Q=40/P=30、竞争点 Q=80/P=10。
#   实验 2：价格效应拆账：Q 40->41 多卖一个：29.5 - 40*0.5 = 9.5 ~ MR(40)。
#   实验 3：福利对比：垄断 CS400/利润800/TS1200；竞争 CS1600/TS1600；
#           DWL = 400；一级歧视：利润 1600、CS 0、TS 1600（DWL 0）。
#   实验 4：自然垄断管制（ATC = 10+600/Q）：未管制 (40,30) 利润 200；
#           P=MC 定价 (80,10) 亏 600；P=ATC 定价 (60,20) 保本。
#   生成 figures/lec13_fig1_monopoly.svg/.png、
#        figures/lec13_fig2_price_discrimination.svg/.png、
#        figures/lec13_fig3_regulation.svg/.png。
# 输出用 GBK 安全字符（无禁区符号，用 [OK] / ^2 / ->）。
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

# 反需求 P = 50 - Q/2；MR = 50 - Q；MC = 10
def P(Q):
    return 50 - Q / 2


def MR(Q):
    return 50 - Q


# ---------------------------------------------------------------------
print("=== 实验 1：收入与边际收益表（P = 50-Q/2，MR = 50-Q，MC = 10） ===")
print("   Q  |  P  |  TR   |  MR  | MC")
prev_tr = 0.0
for Q in range(0, 81, 10):
    p = P(Q)
    tr = p * Q
    mr = (tr - prev_tr) / 10 if Q > 0 else None
    print("  %3d | %3.0f | %4.0f | %s | 10" %
          (Q, p, tr, ("%4.0f" % mr) if mr is not None else " -- "))
    prev_tr = tr
print("  垄断产量：MR=MC -> 50-Q=10 -> Q=40，价格上需求线 -> P=30")
print("  竞争产量：P=MC -> 50-Q/2=10 -> Q=80，P=10")
print("  -> 结论：垄断把产量从 80 压到 40，价格从 10 抬到 30。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：多卖一个的拆账（价格效应） ===")
q0 = 40.0
new_p = P(q0 + 1)
gain_new = new_p
loss_old = q0 * 0.5        # 原 40 个单位每个降价 0.5
net = gain_new - loss_old
print("  从 Q=40 到 41：新价格 %.1f；多卖的 1 个收 %.1f；" % (new_p, new_p))
print("  原 40 个单位每单位降 0.5 -> 损失 %.1f；净增 = %.1f - %.1f = %.1f" %
      (loss_old, gain_new, loss_old, net))
print("  对照 MR(40) = 50-40 = 10（离散近似 %.1f）" % net)
print("  -> 结论：MR < P 的根源 = 价格效应；竞争企业没有它（价格不变）。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：福利对比（垄断 / 竞争 / 一级价格歧视） ===")
qm, pm = 40.0, 30.0
cs_m = 0.5 * qm * (50 - pm)
prof_m = (pm - 10) * qm
ts_m = cs_m + prof_m
qc, pc = 80.0, 10.0
cs_c = 0.5 * qc * (50 - pc)
prof_c = (pc - 10) * qc
ts_c = cs_c + prof_c
dwl = ts_c - ts_m
print("  垄断 (%.0f, %.0f)：CS=%.0f  利润=%.0f  TS=%.0f" % (qm, pm, cs_m, prof_m, ts_m))
print("  竞争 (%.0f, %.0f)：CS=%.0f  利润=%.0f  TS=%.0f" % (qc, pc, cs_c, prof_c, ts_c))
print("  DWL = %.0f = (1/2)×40×20 = %.0f" % (dwl, 0.5 * 40 * 20))
tr_pd = 50 * 80 - 80 * 80 / 4      # 一级歧视：TR = 需求曲线下梯形面积
prof_pd = tr_pd - 10 * 80
print("  一级歧视 (Q=80)：TR=%.0f  利润=%.0f  CS=0  TS=%.0f（DWL=0）" % (tr_pd, prof_pd, prof_pd))
print("  -> 结论：垄断的问题不在赚钱，在把交易做到 40 就停了——DWL 400；")
print("     完美的价格歧视把交易做回 80（效率恢复），但 CS 全被搬走。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：自然垄断的管制三选（ATC = 10 + 600/Q） ===")
FC = 600.0
def ATC(Q):
    return 10 + FC / Q
q_u, p_u = 40.0, 30.0
print("  不管制（MR=MC）：Q=%.0f  P=%.0f  ATC=%.0f  利润=%.0f" %
      (q_u, p_u, ATC(q_u), (p_u - ATC(q_u)) * q_u))
q_mc, p_mc = 80.0, 10.0
print("  P=MC 定价：Q=%.0f  P=%.0f  ATC=%.1f  亏损=%.0f（固定成本收不回）" %
      (q_mc, p_mc, ATC(q_mc), (ATC(q_mc) - p_mc) * q_mc))
q_atc, p_atc = 60.0, 20.0
print("  P=ATC 定价：Q=%.0f  P=%.0f  ATC=%.0f  利润=0（保本）" %
      (q_atc, p_atc, ATC(q_atc)))
print("  -> 结论：MC 定价会亏（需补贴）、ATC 定价保本但无降本激励——管制不是一句话的事。")

# ---------------------------------------------------------------------
# 图 1：垄断全图
fig, ax = plt.subplots(figsize=(7.4, 5.0), dpi=120)
qs = [i / 2 for i in range(0, 161)]            # 0 .. 80
dem = [50 - q / 2 for q in qs]
mrs = [50 - q for q in qs]
ax.plot(qs, dem, color="#c0392b", lw=2, label="需求 D")
ax.plot(qs, mrs, color="#8e44ad", lw=2, ls="--", label="边际收益 MR")
ax.plot([0, 100], [10, 10], color="#2471a3", lw=2, label="边际成本 MC = 10")
ax.fill([0, 40, 0], [50, 30, 30], color="#aed6f1", alpha=0.55)
ax.fill([0, 40, 40, 0], [30, 30, 10, 10], color="#f5cba7", alpha=0.8)
ax.fill([40, 80, 40], [30, 10, 10], color="#95a5a6", alpha=0.85)
ax.plot([40], [30], "ko", ms=9)
ax.plot([80], [10], "o", color="#7f8c8d", ms=9)
ax.plot([40, 40], [10, 30], color="#2c3e50", lw=1.2, ls=":")
ax.annotate("垄断点 (40, 30)", xy=(40, 30), xytext=(20, 40), fontsize=10,
            arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
ax.annotate("竞争/理想点 (80, 10)", xy=(80, 10), xytext=(54, 4.5), fontsize=10, color="#7f8c8d",
            arrowprops=dict(arrowstyle="-", color="#7f8c8d", lw=0.8))
ax.annotate("CS=400", xy=(9, 37), fontsize=10, color="#1a5276")
ax.annotate("垄断利润\n800", xy=(13, 17), fontsize=10, color="#935116")
ax.annotate("DWL\n400", xy=(49, 16.5), fontsize=10.5, color="#2c3e50")
ax.set_xlabel("数量 Q")
ax.set_ylabel("价格 P")
ax.set_title("垄断的全景：MR=MC 定产量、需求线定价格")
ax.set_xlim(0, 90)
ax.set_ylim(-5, 55)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec13_fig1_monopoly.svg"))
fig.savefig(os.path.join(FIGDIR, "lec13_fig1_monopoly.png"))

# ---------------------------------------------------------------------
# 图 2：价格歧视双联
fig2, (axa, axb) = plt.subplots(1, 2, figsize=(11.0, 4.4), dpi=120)
# 左：单一定价
axa.plot(qs, dem, color="#c0392b", lw=2, label="需求 D")
axa.plot(qs, mrs, color="#8e44ad", lw=2, ls="--", label="MR")
axa.plot([0, 100], [10, 10], color="#2471a3", lw=2, label="MC")
axa.fill([0, 40, 0], [50, 30, 30], color="#aed6f1", alpha=0.55)
axa.fill([0, 40, 40, 0], [30, 30, 10, 10], color="#f5cba7", alpha=0.8)
axa.fill([40, 80, 40], [30, 10, 10], color="#95a5a6", alpha=0.85)
axa.annotate("CS", xy=(12, 38), fontsize=10, color="#1a5276")
axa.annotate("利润", xy=(14, 19), fontsize=10, color="#935116")
axa.annotate("DWL", xy=(50, 17), fontsize=10, color="#2c3e50")
axa.set_xlim(0, 90)
axa.set_ylim(-5, 55)
axa.set_xlabel("数量 Q")
axa.set_ylabel("价格 P")
axa.set_title("单一定价：交易停在 40", fontsize=11)
axa.legend(loc="upper right", fontsize=8)
# 右：一级歧视
axb.plot(qs, dem, color="#c0392b", lw=2, label="需求 D")
axb.plot([0, 100], [10, 10], color="#2471a3", lw=2, label="MC")
q80 = [i / 2 for i in range(0, 161)]
axb.fill_between(q80, [50 - q / 2 for q in q80], 10, color="#f5cba7", alpha=0.85)
axb.plot([80], [10], "o", color="#7f8c8d", ms=8)
axb.annotate("每一块都按'他的最高愿付'收：\n全部梯形变成利润（1600）", xy=(26, 30), fontsize=9.5, color="#935116")
axb.annotate("交易做到 80：CS=0，无 DWL", xy=(30, 6), fontsize=9.5, color="#2c3e50")
axb.set_xlim(0, 90)
axb.set_ylim(-5, 55)
axb.set_xlabel("数量 Q")
axb.set_ylabel("价格 P")
axb.set_title("一级价格歧视：交易做到 80", fontsize=11)
axb.legend(loc="upper right", fontsize=8)
fig2.suptitle("同样的垄断者，两种定价术：蛋糕怎么切、切多大", fontsize=12)
fig2.tight_layout(rect=[0, 0, 1, 0.94])
fig2.savefig(os.path.join(FIGDIR, "lec13_fig2_price_discrimination.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec13_fig2_price_discrimination.png"))

# ---------------------------------------------------------------------
# 图 3：自然垄断的管制三选
fig3, ax3 = plt.subplots(figsize=(7.4, 4.8), dpi=120)
q3 = [i / 2 for i in range(30, 201)]           # 15 .. 100
ax3.plot(q3, [50 - q / 2 for q in q3], color="#c0392b", lw=2, label="需求 D")
ax3.plot(q3, [10 + 600 / q for q in q3], color="#8e44ad", lw=2, label="ATC = 10 + 600/Q")
ax3.plot([0, 100], [10, 10], color="#2471a3", lw=2, label="MC = 10")
ax3.plot([40], [30], "ko", ms=8)
ax3.annotate("不管制 (40, 30)\n利润 200", xy=(40, 30), xytext=(14, 27), fontsize=9,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
ax3.plot([60], [20], "o", color="#27ae60", ms=8)
ax3.annotate("P=ATC 定价 (60, 20)\n保本", xy=(60, 20), xytext=(62, 30), fontsize=9, color="#1e8449",
             arrowprops=dict(arrowstyle="-", color="#1e8449", lw=0.8))
ax3.plot([80], [10], "o", color="#c0392b", ms=8)
ax3.annotate("P=MC 定价 (80, 10)\n亏 600（需补贴）", xy=(80, 10), xytext=(56, 3), fontsize=9, color="#922b21",
             arrowprops=dict(arrowstyle="-", color="#922b21", lw=0.8))
ax3.set_xlabel("数量 Q")
ax3.set_ylabel("价格 P")
ax3.set_title("自然垄断的管制困境：三种定价，三种账")
ax3.set_xlim(15, 100)
ax3.set_ylim(0, 55)
ax3.legend(loc="upper right", fontsize=8.5)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec13_fig3_regulation.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec13_fig3_regulation.png"))

print()
print("[OK] figures/lec13_fig1_monopoly、lec13_fig2_price_discrimination、lec13_fig3_regulation 已生成。")