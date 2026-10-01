# =====================================================================
# lec11-01 成本的两本账与成本曲线（第 11 讲 §1-§5）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   实验 1：面包房两本账：收入 50；显性 40 -> 会计利润 10；
#           隐性 13.8（资金 1.8 + 劳动 12）-> 经济利润 -3.8。
#   实验 2：生产函数：L=1..6 -> Q=50/90/120/140/150/155；MP 递减。
#   实验 3：成本表（FC=120）：VC/TC/ATC/AVC/AFC/MC 全表 +
#           验证 ATC = AVC + AFC；验证 MC < ATC 时 ATC 降、MC > ATC 时升。
#   实验 4：长期平均成本 LAC = 2000/Q + 5Q：最低点 Q=20、LAC=200。
#   生成 figures/lec11_fig1_cost_curves.svg/.png、
#        figures/lec11_fig2_marginal_product.svg/.png、
#        figures/lec11_fig3_long_run.svg/.png。
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

# ---------------------------------------------------------------------
print("=== 实验 1：面包房的两本账 ===")
revenue = 50.0
explicit = {"原料": 20.0, "房租": 8.0, "雇工": 12.0}
implicit = {"自有资金的机会成本（理财收益）": 1.8, "老板劳动的机会成本（店长年薪）": 12.0}
acct = revenue - sum(explicit.values())
econ = revenue - sum(explicit.values()) - sum(implicit.values())
print("  收入 %.1f；显性成本合计 %.1f（%s）" % (revenue, sum(explicit.values()), explicit))
print("  会计利润 = %.1f - %.1f = %.1f" % (revenue, sum(explicit.values()), acct))
print("  隐性成本合计 %.1f（%s）" % (sum(implicit.values()), implicit))
print("  经济利润 = %.1f - %.1f - %.1f = %.1f" % (revenue, sum(explicit.values()), sum(implicit.values()), econ))
print("  -> 结论：账本上赚 10 万，经济学账上亏 3.8 万——差距全在'没有发票的成本'。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：生产函数与边际产量（面包房一天的产量） ===")
Ls = [1, 2, 3, 4, 5, 6]
Qs = [50, 90, 120, 140, 150, 155]
print("  工人 L | 产量 Q | 边际产量 MP")
prev = 0
for L, Q in zip(Ls, Qs):
    print("    %d    |  %4d  |   %3d" % (L, Q, Q - prev))
    prev = Q
print("  -> 结论：MP 从 50 一路递减到 5——边际产量递减；总产量仍在涨，只是越涨越慢。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：短期成本表（FC = 120） ===")
FC = 120.0
Qs2 = [1, 2, 3, 4, 5, 6]
VCs = [60.0, 100.0, 150.0, 210.0, 290.0, 390.0]
print("   Q |  VC  |  TC  |  ATC  |  AVC  |  AFC  |  MC")
prev_vc = 0.0
prev_atc = None
for Q, VC in zip(Qs2, VCs):
    TC = FC + VC
    ATC = TC / Q
    AVC = VC / Q
    AFC = FC / Q
    MC = VC - prev_vc
    flag = ""
    if prev_atc is not None:
        flag = "（MC<ATC：ATC 降）" if MC < prev_atc else "（MC>ATC：ATC 升）"
    print("  %2d | %4.0f | %4.0f | %5.1f | %5.1f | %5.1f | %4.0f %s" %
          (Q, VC, TC, ATC, AVC, AFC, MC, flag))
    prev_vc = VC
    prev_atc = ATC
print("  验证：每行 ATC = AVC + AFC（如 Q=5：58 + 24 = 82）")
print("  验证：Q=5 处 MC=80 < ATC=82 -> ATC 继续降；Q=6 处 MC=100 > 82 -> ATC 转升")
print("  -> 结论：MC 在 ATC 的最低点'掉头'处穿过——'新成绩与平均分'的关系。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：长期平均成本与规模经济（LAC = 2000/Q + 5Q） ===")
print("   Q  | LAC")
best_q, best_lac = 0, 1e9
for Q in range(8, 33, 4):
    LAC = 2000 / Q + 5 * Q
    if LAC < best_lac:
        best_q, best_lac = Q, LAC
    print("  %2d | %.0f" % (Q, LAC))
print("  连续最低点：Q = 20（LAC = %.0f）——左侧规模经济、右侧规模不经济" % (2000 / 20 + 5 * 20))
print("  -> 结论：长期成本先降后升，碗形；最低点又称'有效规模'。")

# ---------------------------------------------------------------------
# 图 1：成本曲线双联（上：总量；下：平均与边际）
fig, (axu, axd) = plt.subplots(2, 1, figsize=(7.0, 7.2), dpi=120)
xs = [0] + Qs2
TCs = [FC] + [FC + v for v in VCs]
VCs_plot = [0] + VCs
FCs = [FC] * len(xs)
axu.plot(xs, TCs, "o-", color="#c0392b", lw=2, label="总成本 TC")
axu.plot(xs, VCs_plot, "s-", color="#2471a3", lw=2, label="可变成本 VC")
axu.plot(xs, FCs, "--", color="#7f8c8d", lw=1.8, label="固定成本 FC = 120")
axu.set_xlabel("产量 Q")
axu.set_ylabel("元 / 天")
axu.set_title("上组：总量的三条线（TC 与 VC 平行，差距恰为 FC）", fontsize=11)
axu.set_xlim(0, 6.5)
axu.set_ylim(0, 540)
axu.legend(loc="upper left", fontsize=8.5)
ATCs = [TC / Q for Q, TC in zip(Qs2, TCs[1:])]
AVCs = [v / Q for Q, v in zip(Qs2, VCs)]
AFCs = [FC / Q for Q in Qs2]
MCs = [VCs[0]] + [VCs[i] - VCs[i - 1] for i in range(1, len(VCs))]
axd.plot(Qs2, ATCs, "o-", color="#c0392b", lw=2, label="平均总成本 ATC")
axd.plot(Qs2, AVCs, "s-", color="#2471a3", lw=2, label="平均可变成本 AVC")
axd.plot(Qs2, AFCs, "^--", color="#7f8c8d", lw=1.8, label="平均固定成本 AFC")
axd.plot(Qs2, MCs, "d-", color="#27ae60", lw=2, label="边际成本 MC")
axd.plot([5], [82], "ko", ms=8)
axd.annotate("ATC 最低点 (5, 82)", xy=(5, 82), xytext=(2.6, 60), fontsize=9.5,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
axd.set_xlabel("产量 Q")
axd.set_ylabel("元 / 单位")
axd.set_title("下组：平均与边际的四条线（MC 在 ATC 最低点穿过）", fontsize=11)
axd.set_xlim(0, 6.5)
axd.set_ylim(0, 200)
axd.legend(loc="upper right", fontsize=8.5)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec11_fig1_cost_curves.svg"))
fig.savefig(os.path.join(FIGDIR, "lec11_fig1_cost_curves.png"))

# ---------------------------------------------------------------------
# 图 2：边际产量递减
fig2, ax2 = plt.subplots(figsize=(6.8, 4.2), dpi=120)
ax2.plot(Ls, Qs, "o-", color="#c0392b", lw=2, label="总产量 Q")
MPs = [50, 40, 30, 20, 10, 5]
ax2.plot(Ls, MPs, "s--", color="#2471a3", lw=2, label="边际产量 MP")
for L, mp in zip(Ls, MPs):
    dy = -9 if mp >= 10 else 7
    ax2.annotate("%d" % mp, xy=(L, mp), xytext=(L + 0.08, mp + dy), fontsize=8.5, color="#2471a3")
ax2.set_xlabel("工人数 L")
ax2.set_ylabel("产量（个 / 天）")
ax2.set_title("边际产量递减：每多一个人，增量更小")
ax2.set_xlim(0.5, 6.5)
ax2.set_ylim(0, 170)
ax2.legend(loc="center right", fontsize=9)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec11_fig2_marginal_product.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec11_fig2_marginal_product.png"))

# ---------------------------------------------------------------------
# 图 3：长期平均成本（碗形与三段）
fig3, ax3 = plt.subplots(figsize=(6.8, 4.2), dpi=120)
xs3 = [8 + i / 2 for i in range(0, 65)]      # 8 .. 40
lacs = [2000 / q + 5 * q for q in xs3]
ax3.plot(xs3, lacs, color="#27ae60", lw=2.2)
ax3.plot([20], [200], "ko", ms=8)
ax3.annotate("有效规模 (20, 200)", xy=(20, 200), xytext=(22, 235), fontsize=10)
ax3.axvspan(8, 20, color="#d5f5e3", alpha=0.5)
ax3.axvspan(20, 40, color="#fadbd8", alpha=0.5)
ax3.annotate("规模经济", xy=(12, 250), fontsize=11, color="#1e8449")
ax3.annotate("规模不经济", xy=(30, 250), fontsize=11, color="#922b21")
ax3.set_xlabel("产量 Q")
ax3.set_ylabel("长期平均成本 LAC")
ax3.set_title("长期平均成本：先降后升的'碗'")
ax3.set_xlim(8, 40)
ax3.set_ylim(150, 290)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec11_fig3_long_run.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec11_fig3_long_run.png"))

print()
print("[OK] figures/lec11_fig1_cost_curves、lec11_fig2_marginal_product、lec11_fig3_long_run 已生成。")