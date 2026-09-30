# =====================================================================
# lec01-01 平均账 vs 边际账，与"最优在哪停"（第 01 讲 引子收尾 / §3）
# 规模纪律：总耗时 < 5 秒（纯算术 + 一张小图）。
# 方法：
#   实验 1：民宿"深夜特价接不接"——两个方案的利润对照。
#           预期：接单比不接多赚 300 - 110 = 190 元。
#   实验 2：营业时长延长的逐小时 MB/MC 表——扫描累计净收益。
#           预期：累计净收益最大在 q=5（MB=70 >= MC=60；第 6 小时 60 < 65 停）；
#           全延 10 小时总账为负（-45），但"一小时都不延"同样不是最优。
#   并生成 figures/lec01_fig1_marginal_decision.svg 与 .png。
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
print("=== 实验 1：民宿深夜特价，接不接？两个方案对照 ===")
fixed = 4000.0           # 每天雷打不动的开支：房租、工资等
var = 110.0              # 每多住一间才发生的开支：清洁、水电、早餐
sold, price = 2, 800.0   # 今晚已确定 2 间，每间 800 元
offer = 300.0            # 深夜来电：第 3 间只肯出 300 元

profit_no = sold * price - fixed - sold * var
profit_yes = sold * price + offer - fixed - (sold + 1) * var
print("  不接：利润 = 2*800 - 4000 - 2*110 = %.0f 元" % profit_no)
print("  接  ：利润 = (2*800 + 300) - 4000 - 3*110 = %.0f 元" % profit_yes)
print("  两方案差 = %.0f 元（= 报价 300 - 边际成本 110）" % (profit_yes - profit_no))
avg_all = fixed / 3 + var
print("  平均账陷阱：把当天全部开支摊到 3 间上，平均每间 %.0f 元，" % avg_all)
print("  看起来'卖 300 亏 %.0f'——但摊掉的固定开支，不接单也一样发生。" % (avg_all - offer))
print("  -> 结论：决策只比较'变动的部分'：多收 300，多花 110，净改善 190，应当接。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：营业时长每小时延长，延长到哪一小时停？ ===")
MB = [110, 100, 90, 80, 70, 60, 50, 40, 30, 20]   # 第 k 小时带来的额外收入（递减）
MC = [40, 45, 50, 55, 60, 65, 75, 85, 100, 120]  # 第 k 小时的额外成本（递增，后段加速）
print("  小时 | 边际收益 | 边际成本 | 该小时净得 | 累计净得")
cum = 0
best_q, best_cum = 0, 0
for q in range(1, 11):
    net = MB[q - 1] - MC[q - 1]
    cum += net
    if cum > best_cum:
        best_q, best_cum = q, cum
    print("   %2d  |   %3d    |   %3d    |   %+4d     |   %+4d" % (q, MB[q - 1], MC[q - 1], net, cum))
print("  累计净得最大在 q = %d（最多 %+d 元）" % (best_q, best_cum))
print("  检查规则：第 %d 小时 MB=%d >= MC=%d，该做；第 %d 小时 MB=%d < MC=%d，该停。" %
      (best_q, MB[best_q - 1], MC[best_q - 1], best_q + 1, MB[best_q], MC[best_q]))
print("  全有全无对照：全延 10 小时总收益 %+d，总成本 %d，总账 %+d，" %
      (sum(MB), sum(MC), sum(MB) - sum(MC)))
print("  但'干脆一小时也别延'同样是错的——前 5 小时净赚 %+d。" % best_cum)
print("  -> 结论：最优不在'做'与'不做'两端，而在 MB 与 MC 的交点处。")

# ---------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=120)
qs = list(range(1, 11))
ax.plot(qs, MB, "o-", color="#c0392b", lw=2, label="边际收益 MB")
ax.plot(qs, MC, "s-", color="#2471a3", lw=2, label="边际成本 MC")
ax.axvline(5.5, color="#7f8c8d", ls="--", lw=1)
ax.annotate("交点：做满 5 小时", xy=(5.5, 72), xytext=(5.8, 100), fontsize=10)
ax.annotate("MB > MC：继续做", xy=(2.2, 58), fontsize=10, color="#c0392b")
ax.annotate("MB < MC：停", xy=(7.4, 42), fontsize=10, color="#2471a3")
ax.set_xlabel("延长的第几小时")
ax.set_ylabel("元 / 小时")
ax.set_title("边际决策：做到 MB 与 MC 的交点")
ax.legend(loc="upper right", fontsize=9)
ax.set_xlim(0.5, 10.5)
ax.set_ylim(0, 130)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec01_fig1_marginal_decision.svg"))
fig.savefig(os.path.join(FIGDIR, "lec01_fig1_marginal_decision.png"))
print()
print("[OK] figures/lec01_fig1_marginal_decision.svg 与 .png 已生成。")