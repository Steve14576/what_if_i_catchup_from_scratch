# =====================================================================
# lec15-01 生产要素市场：VMPL、劳动均衡与现值（第 15 讲 §1-§4）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   果园场景：苹果价 P = 2 元/斤；工日采果量 MP = 50,45,40,35,30,25,20；
#   VMPL = MP*P = 100,90,80,70,60,50,40。
#   实验 1：雇工决策：W=100 -> 雇 1；W=80 -> 雇 3；W=60 -> 雇 5
#           （规则：VMPL >= W 的最后一个）。
#   实验 2：市场均衡：供给表 W=40..100 对应 3..9 人；逐工资对照找均衡
#           预期 (W*=60, L*=5)。
#   实验 3：产品涨价（P=2 -> 3）：VMPL 变 150,135,120,105,90,75,60；
#           同工资 60 下雇工 5 -> 7；新均衡约 (70, 6)。
#   实验 4：现值：年租 1000、利率 10%：前 3 期 909.09/826.45/751.31；
#           前 10 期累计；永续极限 10000；利率 20% 时极限 5000。
#   生成 figures/lec15_fig1_vmpl.svg/.png、
#        figures/lec15_fig2_labor_eq.svg/.png、
#        figures/lec15_fig3_pv.svg/.png。
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

P_apple = 2.0
MPs = [50, 45, 40, 35, 30, 25, 20]
VMPL = [p * P_apple for p in MPs]
# 劳动供给：工资 -> 愿干人数
supply = {40: 3, 50: 4, 60: 5, 70: 6, 80: 7, 90: 8, 100: 9}

# ---------------------------------------------------------------------
print("=== 实验 1：果园的雇工决策（P=%.0f，VMPL = %s） ===" % (P_apple, VMPL))
for W in [100.0, 80.0, 60.0]:
    hire = sum(1 for v in VMPL if v >= W)
    print("  日工资 %.0f：VMPL >= %.0f 的工人共 %d 个 -> 雇 %d 个" % (W, W, hire, hire))
print("  -> 结论：劳动需求（雇工数）跟着 VMPL 走——工资越低、雇得越多（阶梯向下）。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：劳动市场的均衡（供给表：40->3 ... 100->9） ===")
print("  工资 | 需求(VMPL>=W 的人数) | 供给 | 差")
eq = None
for W in [40, 50, 60, 70, 80, 90, 100]:
    dem = sum(1 for v in VMPL if v >= W)
    sup = supply[W]
    gap = dem - sup
    tag = ""
    if gap == 0:
        tag = " <- 均衡"
        eq = (W, dem)
    print("  %3d  |        %d             |  %d   | %+d%s" % (W, dem, sup, gap, tag))
print("  均衡：W* = %d，L* = %d（60 元/天、5 个工人）" % eq)
print("  -> 结论：工资是供需碰出来的——也是 VMPL 与劳动供给的交点。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：苹果涨价（2 -> 3 元）的对照 ===")
VMPL2 = [p * 3.0 for p in MPs]
print("  新 VMPL = %s" % VMPL2)
d60 = sum(1 for v in VMPL if v >= 60)
d60b = sum(1 for v in VMPL2 if v >= 60)
print("  同工资 60 元：雇工 %d -> %d 个（劳动需求右移）" % (d60, d60b))
for W in [60, 70, 80]:
    dem = sum(1 for v in VMPL2 if v >= W)
    sup = supply[W] if W in supply else round((W - 10) / 10)
    print("    W=%d：需求 %d、供给 %d" % (W, dem, sup))
print("  新均衡约在 (70, 6)：工资 60->70、就业 5->6")
print("  -> 结论：产品涨价抬升 VMPL -> 劳动需求右移 -> 工资与就业同升。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：现值（年租 1000 元，利率 10%） ===")
rent, r = 1000.0, 0.10
cum = 0.0
for t in range(1, 11):
    pv_t = rent / (1 + r) ** t
    cum += pv_t
    if t <= 3 or t == 10:
        print("  第 %2d 期现值 = %.2f；累计 = %.2f" % (t, pv_t, cum))
print("  永续极限 = 租金 / 利率 = 1000 / 0.10 = %.0f" % (rent / r))
print("  利率升到 20%%：极限 = 1000 / 0.20 = %.0f（利率越高、资产越便宜）" % (rent / 0.20))
print("  地租例：土地供给固定 100 亩、需求 W = 2000-10A -> 地租 = %.0f 元/亩" % (2000 - 10 * 100))
print("  -> 结论：资产价格 = 未来租金的现值；地租在供给固定时由需求单方面决定。")

# ---------------------------------------------------------------------
# 图 1：VMPL 与雇工决策
fig, ax = plt.subplots(figsize=(7.0, 4.4), dpi=120)
ks = list(range(1, 8))
ax.bar(ks, VMPL, color="#d6eaf8", edgecolor="#2471a3", width=0.6, label="VMPL（边际产值）")
for W, c in [(100, "#922b21"), (80, "#b9770e"), (60, "#1e8449")]:
    ax.axhline(W, color=c, lw=1.6, ls="--")
    ax.annotate("工资 %d" % W, xy=(0.55, W + 3), fontsize=9, color=c)
ax.annotate("雇 1 个", xy=(1, 112), fontsize=10, color="#922b21")
ax.annotate("雇 3 个", xy=(3, 92), fontsize=10, color="#b9770e")
ax.annotate("雇 5 个", xy=(5, 72), fontsize=10, color="#1e8449")
ax.set_xlabel("第几个工人")
ax.set_ylabel("VMPL（元 / 天）")
ax.set_title("劳动需求：VMPL 阶梯——工资线切到哪里，就雇到哪里")
ax.set_xticks(ks)
ax.set_ylim(0, 120)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec15_fig1_vmpl.svg"))
fig.savefig(os.path.join(FIGDIR, "lec15_fig1_vmpl.png"))

# ---------------------------------------------------------------------
# 图 2：劳动市场均衡
fig2, ax2 = plt.subplots(figsize=(7.0, 4.6), dpi=120)
ax2.plot(ks, VMPL, "o-", color="#c0392b", lw=2, label="劳动需求（VMPL）")
sup_x = sorted(supply.values())
sup_y = sorted(supply.keys())
ax2.plot(sup_x, sup_y, "s-", color="#2471a3", lw=2, label="劳动供给")
ax2.plot([5], [60], "ko", ms=9)
ax2.annotate("均衡 (5, 60)", xy=(5, 60), xytext=(5.6, 72), fontsize=10,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
ax2.plot(ks, VMPL2[:7], "o--", color="#e59866", lw=1.6, label="涨价后的劳动需求")
ax2.set_xlabel("工人数 L")
ax2.set_ylabel("工资 W（元/天）")
ax2.set_title("劳动市场：工资与就业在供需交叉处被'碰'出来")
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 160)
ax2.legend(loc="upper right", fontsize=8.5)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec15_fig2_labor_eq.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec15_fig2_labor_eq.png"))

# ---------------------------------------------------------------------
# 图 3：现值累计收敛
fig3, ax3 = plt.subplots(figsize=(7.0, 4.4), dpi=120)
ts = list(range(1, 31))
cums = []
c = 0.0
for t in ts:
    c += rent / (1 + r) ** t
    cums.append(c)
ax3.plot(ts, cums, "o-", color="#27ae60", lw=2, ms=4)
ax3.axhline(10000, color="#7f8c8d", lw=1.6, ls="--")
ax3.annotate("永续极限 10000 元", xy=(16, 10250), fontsize=10, color="#566573")
ax3.plot([10], [cums[9]], "o", color="#c0392b", ms=8)
ax3.annotate("前 10 期 ≈ %.0f" % cums[9], xy=(10, cums[9]), xytext=(11, 7300), fontsize=9.5,
             arrowprops=dict(arrowstyle="-", color="#922b21", lw=0.8))
ax3.set_xlabel("期数（年）")
ax3.set_ylabel("累计现值（元）")
ax3.set_title("资产的价格：未来租金的现值累计逼近一个极限")
ax3.set_xlim(0, 31)
ax3.set_ylim(0, 11500)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec15_fig3_pv.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec15_fig3_pv.png"))

print()
print("[OK] figures/lec15_fig1_vmpl、lec15_fig2_labor_eq、lec15_fig3_pv 已生成。")