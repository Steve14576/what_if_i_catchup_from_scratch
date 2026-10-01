# =====================================================================
# lec06-01 消费者剩余、生产者剩余与总剩余（第 06 讲 §1-§4）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   实验 1：引子台阶核对（离散）：边际价值 [10,8,6,4]、边际成本 [2,4,6,8]，
#           价格 6 -> CS=6、PS=6、TS=12。
#   实验 2：连续市场几何（反需求 50-Q、反供给 10+Q；均衡 (20,30)）：
#           CS=200、PS=200、TS=400。
#   实验 3：总剩余扫描 TS(Q)=40Q-Q^2：峰值 Q=20（400）；两侧同损失。
#   实验 4：05 讲租金上限的账本重算：均衡 TS=1500 -> 管制后 1125（少 375）。
#   生成 figures/lec06_fig1_surplus_areas.svg/.png、
#        figures/lec06_fig2_ts_curve.svg/.png、
#        figures/lec06_fig3_ceiling_ledger.svg/.png。
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
print("=== 实验 1：引子台阶核对（一个买家 + 一个摊主，价格 6） ===")
values = [10, 8, 6, 4]   # 这个买家对第 1、2、3、4 杯的边际价值
costs = [2, 4, 6, 8]     # 摊主做第 1、2、3、4 杯的边际成本
P = 6.0
CS = sum(v - P for v in values if v >= P)
PS = sum(P - c for c in costs if c <= P)
print("  买家愿付不低于 6 元的单位：%s -> CS = %.0f" % ([v for v in values if v >= P], CS))
print("  摊主成本不高于 6 元的单位：%s -> PS = %.0f" % ([c for c in costs if c <= P], PS))
print("  总剩余 = %.0f + %.0f = %.0f" % (CS, PS, CS + PS))
print("  -> 结论：价款 18 元（6*3）只是'转移'；12 元是交易创造出来的。")

# ---------------------------------------------------------------------
print("=== 实验 2：连续市场几何（反需求 P = 50 - Q；反供给 P = 10 + Q） ===")
# 均衡：50 - Q = 10 + Q -> Q = 20, P = 30
Q_eq, P_eq = 20.0, 30.0
# CS = ∫0^20 [(50-q) - 30] dq = ∫(20 - q) dq = 400 - 200 = 200
cs = 20 * Q_eq - Q_eq ** 2 / 2
# PS = ∫0^20 [30 - (10+q)] dq = ∫(20 - q) dq = 200
ps = 20 * Q_eq - Q_eq ** 2 / 2
print("  均衡：Q* = %.0f，P* = %.0f" % (Q_eq, P_eq))
print("  CS = 梯形/积分 = %.0f；PS = %.0f；TS = %.0f" % (cs, ps, cs + ps))
print("  -> 结论：CS、PS 各 200，总剩余 400——两条线'夹出'的两个三角形。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：总剩余扫描 TS(Q) = 40Q - Q^2（Q 为市场成交量） ===")
print("   Q  |   TS")
best_Q, best_TS = 0, -1
for Q in range(0, 31, 5):
    TS = 40 * Q - Q * Q
    if TS > best_TS:
        best_Q, best_TS = Q, TS
    print("  %2d  |  %4d" % (Q, TS))
print("  峰值在 Q = %d（TS = %d）——恰是均衡量 20 与均衡价 30 的交点" % (best_Q, best_TS))
print("  两侧对照：Q=15 与 Q=25 的 TS 都 = %d，各比峰值少 %d" % (40 * 15 - 225, best_TS - (40 * 15 - 225)))
print("  -> 结论：少交易与多交易都在丢剩余；均衡量 = 总剩余最大量。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：05 讲租金上限的账本重算（Qd = 300-5P；Qs = 10P-300） ===")
# 反需求 P = 60 - Q/5；反供给 P = 30 + Q/10；均衡 (100, 40)
cs_eq = 20 * 100 - 100 ** 2 / 10     # ∫0^100 [(60-q/5)-40] = ∫(20 - q/5)
ps_eq = 10 * 100 - 100 ** 2 / 20     # ∫0^100 [40-(30+q/10)] = ∫(10 - q/10)
print("  均衡 (100, 40)：CS = %.0f；PS = %.0f；TS = %.0f" % (cs_eq, ps_eq, cs_eq + ps_eq))
# 上限 35：成交 50（供给缩到 50），价格 35
cs_cap = 25 * 50 - 50 ** 2 / 10      # ∫0^50 [(60-q/5)-35] = ∫(25 - q/5)
ps_cap = 5 * 50 - 50 ** 2 / 20       # ∫0^50 [35-(30+q/10)] = ∫(5 - q/10)
print("  上限 35（成交 50）：CS = %.0f；PS = %.0f；TS = %.0f" % (cs_cap, ps_cap, cs_cap + ps_cap))
print("  TS 变化：%.0f -> %.0f，少了 %.0f" % (cs_eq + ps_eq, cs_cap + ps_cap, (cs_eq + ps_eq) - (cs_cap + ps_cap)))
print("  -> 结论：账本能给'政策代价'算出一个准确数字（这个'少掉的部分'下一讲正式命名）。")

# ---------------------------------------------------------------------
# 图 1：CS / PS 面积图
fig, ax = plt.subplots(figsize=(6.8, 4.8), dpi=120)
xs = [i / 2 for i in range(0, 41)]          # 0 .. 20
Pd = [50 - x for x in xs]
Ps = [10 + x for x in xs]
ax.plot(xs, Pd, color="#c0392b", lw=2, label="需求（WTP 登记表）")
ax.plot(xs, Ps, color="#2471a3", lw=2, label="供给（成本登记表）")
ax.fill_between(xs, Pd, 30, color="#aed6f1", alpha=0.55)
ax.fill_between(xs, 30, Ps, color="#f5cba7", alpha=0.7)
ax.plot([20], [30], "ko", ms=8)
ax.annotate("均衡 (20, 30)", xy=(20, 30), xytext=(24, 32.5), fontsize=10)
ax.annotate("消费者剩余\n= 200", xy=(8, 40), fontsize=11, color="#1a5276")
ax.annotate("生产者剩余\n= 200", xy=(8, 18), fontsize=11, color="#935116")
ax.set_xlabel("数量 Q")
ax.set_ylabel("价格 P")
ax.set_title("市场这枚硬币的两面：CS 与 PS 的面积")
ax.set_xlim(0, 32)
ax.set_ylim(0, 55)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec06_fig1_surplus_areas.svg"))
fig.savefig(os.path.join(FIGDIR, "lec06_fig1_surplus_areas.png"))

# ---------------------------------------------------------------------
# 图 2：TS(Q) 抛物线
fig2, ax2 = plt.subplots(figsize=(6.8, 4.4), dpi=120)
qs = [i / 2 for i in range(0, 81)]          # 0 .. 40
ts = [40 * q - q * q for q in qs]
ax2.plot(qs, ts, color="#27ae60", lw=2.2)
ax2.plot([20], [400], "ko", ms=9)
ax2.annotate("峰值 (20, 400)\n= 均衡量", xy=(20, 400), xytext=(30.5, 345), fontsize=10)
ax2.plot([20, 20], [0, 400], color="#7f8c8d", ls="--", lw=1)
ax2.plot([15], [375], "o", color="#e67e22", ms=7)
ax2.plot([25], [375], "o", color="#e67e22", ms=7)
ax2.annotate("Q=15：375", xy=(15, 375), xytext=(4, 300), fontsize=9.5, color="#e67e22")
ax2.annotate("Q=25：375", xy=(25, 375), xytext=(26.5, 300), fontsize=9.5, color="#e67e22")
ax2.set_xlabel("成交量 Q")
ax2.set_ylabel("总剩余 TS")
ax2.set_title("总剩余的山坡：均衡量恰在峰顶")
ax2.set_xlim(0, 40)
ax2.set_ylim(0, 460)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec06_fig2_ts_curve.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec06_fig2_ts_curve.png"))

# ---------------------------------------------------------------------
# 图 3：租金上限的账本（05 讲数据）
fig3, ax3 = plt.subplots(figsize=(7.2, 4.8), dpi=120)
xall = [i for i in range(0, 101)]
Pd3 = [60 - x / 5 for x in xall]
Ps3 = [30 + x / 10 for x in xall]
x50 = [i for i in range(0, 51)]
x50to100 = [i for i in range(50, 101)]
ax3.plot(xall, Pd3, color="#c0392b", lw=2, label="需求")
ax3.plot(xall, Ps3, color="#2471a3", lw=2, label="供给")
ax3.fill_between(x50, [60 - x / 5 for x in x50], 35, color="#aed6f1", alpha=0.55)
ax3.fill_between(x50, 35, [30 + x / 10 for x in x50], color="#f5cba7", alpha=0.7)
ax3.fill_between(x50to100, [60 - x / 5 for x in x50to100], [30 + x / 10 for x in x50to100], color="#bdc3c7", alpha=0.7)
ax3.plot([0, 110], [35, 35], color="#e67e22", lw=2, ls="--")
ax3.annotate("上限 35", xy=(4, 35), xytext=(4, 32.5), fontsize=10, color="#e67e22")
ax3.plot([100], [40], "o", color="#7f8c8d", ms=8)
ax3.plot([50], [35], "ko", ms=8)
ax3.annotate("均衡 (100, 40)", xy=(100, 40), xytext=(102, 44), fontsize=9.5, color="#7f8c8d")
ax3.annotate("实际成交 50", xy=(50, 35), xytext=(52, 31), fontsize=9.5)
ax3.annotate("CS=1000", xy=(18, 50), fontsize=10, color="#1a5276")
ax3.annotate("PS=125", xy=(10, 31.2), fontsize=10, color="#935116")
ax3.annotate("缺口 375", xy=(72, 40.5), fontsize=11, color="#566573")
ax3.set_xlabel("住房数量 Q（百套）")
ax3.set_ylabel("租金 P（百元/月）")
ax3.set_title("用账本审政策：租金上限下的剩余地图")
ax3.set_xlim(0, 115)
ax3.set_ylim(24, 64)
ax3.legend(loc="upper right", fontsize=9)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec06_fig3_ceiling_ledger.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec06_fig3_ceiling_ledger.png"))

print()
print("[OK] figures/lec06_fig1_surplus_areas、lec06_fig2_ts_curve、lec06_fig3_ceiling_ledger 已生成。")