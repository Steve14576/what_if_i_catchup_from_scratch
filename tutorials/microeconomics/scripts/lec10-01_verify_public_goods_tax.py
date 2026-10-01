# =====================================================================
# lec10-01 公共物品、公地与税制设计（第 10 讲 §2-§4）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   实验 1：三人路灯（公共物品）：成本 300；WTP 150/120/80（合计 350）。
#           社会净益 50 > 0；各自独担全 < 300 -> 无人装（搭便车）；
#           平摊 100：甲 +50、乙 +20、丙 -20（总 +50）。
#   实验 2：渔场公地：每船收入 120-n；每船成本 60。
#           自由进入 n=60（净 0）；社会最优 n=30（净 900）；
#           每船收费 30 矫正到 n=30。
#   实验 3：税制三方案（甲 10000 / 乙 20000 / 丙 50000）：
#           人头税 1500（avg 15%/7.5%/3%、marg 0）；
#           比例 10%；累进（免 8000、12%、24%）。
#           加班演示：边际税率 0/25/40% -> 加班/无差异/不加。
#   生成 figures/lec10_fig1_four_quadrants.svg/.png、
#        figures/lec10_fig2_commons.svg/.png、
#        figures/lec10_fig3_tax_rates.svg/.png。
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
print("=== 实验 1：三人路灯（公共物品与搭便车） ===")
cost = 300.0
wtp = [150.0, 120.0, 80.0]
names = ["甲", "乙", "丙"]
total = sum(wtp)
print("  单盏路灯成本 %.0f；三人愿付：%s（合计 %.0f）" % (cost, wtp, total))
print("  社会判断：合计收益 %.0f > 成本 %.0f，净益 %+.0f -> 应该装" % (total, cost, total - cost))
print("  自愿独担：%s" % "；".join("%s愿付%.0f<300不装" % (n, w) for n, w in zip(names, wtp)))
print("  平摊 100：净益 = %s -> 合计 %+.0f（但丙为负）" %
      ("/".join("%+.0f" % (w - 100) for w in wtp), total - cost))
print("  -> 结论：私人自愿供给不足（无人装）；强制平摊有总盈余，但少数反对者问题真实存在。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：渔场公地（每船收入 120-n，每船成本 60） ===")
print("  自由进入：120-n = 60 -> n = 60（每船净收益 0，总净利 0）")
print("  社会最优：max 60n - n^2 在 n = 30（总净利 900）")
print("  对照表：")
for n in [30, 40, 50, 60]:
    print("    n=%2d 头：总净利 = 60*%d - %d^2 = %4.0f" % (n, n, n, 60 * n - n * n))
print("  矫正：每船收费 30 -> 进入条件 120-n = 90 -> n = 30（矫正成功；或配额 30 张证）")
print("  -> 结论：没有'归属'的资源被用到'利润全吃光'为止；社会净利差 900 - 0。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：税制三方案（甲 10000 / 乙 20000 / 丙 50000） ===")
incomes = [10000.0, 20000.0, 50000.0]


def tax_flat(x):
    return 1500.0


def tax_prop(x):
    return 0.10 * x


def tax_prog(x):
    if x <= 8000:
        return 0.0
    if x <= 30000:
        return (x - 8000) * 0.12
    return (30000 - 8000) * 0.12 + (x - 30000) * 0.24


for label, fn, marg in [("人头税 1500/人", tax_flat, "0%"),
                        ("比例税 10%", tax_prop, "10%"),
                        ("累进税（免 8000；12%；24%）", tax_prog, "12%/12%/24%")]:
    taxes = [fn(x) for x in incomes]
    avgs = [t / x * 100 for t, x in zip(taxes, incomes)]
    print("  %s：" % label)
    print("    税额 = %s；平均税率 = %s；边际税率 = %s" %
          ("/".join("%.0f" % t for t in taxes), "/".join("%.1f%%" % a for a in avgs), marg))
print("  -> 结论：人头税平均税率随收入下降（累退）、边际为 0；比例税平均=边际；累进税平均率递增。")

print()
print("  加班决策演示（工资 100/小时，休闲的边际价值 75）：")
for mt in [0.0, 0.25, 0.40]:
    net = 100 * (1 - mt)
    choice = "加班" if net > 75 else ("无所谓" if net == 75 else "不加班（回家）")
    print("    边际税率 %.0f%%：到手 %.0f 元 vs 休闲价值 75 -> %s" % (mt * 100, net, choice))
print("  -> 结论：决定'下一个小时干不干'的是边际税率——它是行为的朋友或敌人。")

# ---------------------------------------------------------------------
# 图 1：四格棋盘
fig, ax = plt.subplots(figsize=(6.8, 5.2), dpi=120)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")


def cell(x, y, title, examples, fc):
    ax.add_patch(plt.Rectangle((x, y), 4.6, 4.2, facecolor=fc, edgecolor="#566573", lw=1.6))
    ax.text(x + 2.3, y + 3.3, title, ha="center", fontsize=13, weight="bold")
    ax.text(x + 2.3, y + 1.5, examples, ha="center", fontsize=9.5, linespacing=1.6)


cell(0.2, 5.4, "私人物品", "排他 √ 竞用 √\n苹果、理发、手机", "#d5f5e3")
cell(5.2, 5.4, "俱乐部物品", "排他 √ 竞用 ×\n收费桥、有线电视", "#d6eaf8")
cell(0.2, 0.6, "公共资源", "排他 × 竞用 √\n渔场、拥堵道路、地下水", "#fdebd0")
cell(5.2, 0.6, "公共物品", "排他 × 竞用 ×\n国防、路灯、基础研究", "#fadbd8")
ax.text(2.5, 9.9, "竞用", ha="center", fontsize=11, color="#566573")
ax.text(7.5, 9.9, "非竞用", ha="center", fontsize=11, color="#566573")
ax.text(0.02, 7.5, "排他", rotation=90, fontsize=11, va="center", color="#566573")
ax.text(0.02, 2.7, "非排他", rotation=90, fontsize=11, va="center", color="#566573")
ax.text(5, 0.05, "横轴：竞用性（多用一份，别人就少一份）　纵轴：排他性（收费拦得住）", ha="center", fontsize=9.5, color="#566573")
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec10_fig1_four_quadrants.svg"))
fig.savefig(os.path.join(FIGDIR, "lec10_fig1_four_quadrants.png"))

# ---------------------------------------------------------------------
# 图 2：公地悲剧（双联）
fig2, (axa, axb) = plt.subplots(1, 2, figsize=(10.8, 4.3), dpi=120)
ns = [i / 4 for i in range(0, 361)]           # 0 .. 90
axa.plot(ns, [120 - n for n in ns], color="#c0392b", lw=2, label="每船收入 120 - n")
axa.plot(ns, [60] * len(ns), color="#2471a3", lw=2, label="每船成本 60")
axa.plot(ns, [90] * len(ns), color="#e67e22", lw=1.6, ls="--", label="收费 30 后门槛 90")
axa.plot([60], [60], "ko", ms=8)
axa.annotate("自由进入停在这：n = 60", xy=(60, 60), xytext=(18, 66), fontsize=9.5,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
axa.plot([30], [90], "o", color="#27ae60", ms=8)
axa.annotate("社会最优 n = 30", xy=(30, 90), xytext=(33, 104), fontsize=9.5, color="#1e8449")
axa.set_xlabel("渔船数 n")
axa.set_ylabel("元 / 船")
axa.set_title("自由进入把船数推到 60", fontsize=11)
axa.set_xlim(0, 90)
axa.set_ylim(0, 130)
axa.legend(loc="upper right", fontsize=8)
axb.plot(ns, [60 * n - n * n for n in ns], color="#27ae60", lw=2.2)
axb.plot([30], [900], "ko", ms=9)
axb.plot([60], [0], "ko", ms=9)
axb.annotate("社会最优 (30, 900)", xy=(30, 900), xytext=(34, 940), fontsize=9.5)
axb.annotate("自由进入 (60, 0)：利润全部被吃光", xy=(60, 0), xytext=(24, 260), fontsize=9.5,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
axb.set_xlabel("渔船数 n")
axb.set_ylabel("总净利（元）")
axb.set_title("公地的结局：超额利润耗散为零", fontsize=11)
axb.set_xlim(0, 90)
axb.set_ylim(-100, 1000)
fig2.suptitle("公地悲剧：不属于任何人的东西，最先被掏空", fontsize=12)
fig2.tight_layout(rect=[0, 0, 1, 0.94])
fig2.savefig(os.path.join(FIGDIR, "lec10_fig2_commons.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec10_fig2_commons.png"))

# ---------------------------------------------------------------------
# 图 3：三种税制的平均税率曲线
fig3, ax3 = plt.subplots(figsize=(7.2, 4.6), dpi=120)
xs = [i * 100 for i in range(50, 601)]        # 5000 .. 60000
ax3.plot(xs, [1500 / x * 100 for x in xs], color="#c0392b", lw=2.2, label="人头税 1500（累退）")
ax3.plot(xs, [10] * len(xs), color="#2471a3", lw=2.2, label="比例税 10%")
ax3.plot(xs, [tax_prog(x) / x * 100 for x in xs], color="#27ae60", lw=2.2, label="累进税（免 8000；12%；24%）")
ax3.set_xlabel("年收入（元）")
ax3.set_ylabel("平均税率（%）")
ax3.set_title("三种税制的'平均税率画像'")
ax3.set_xlim(5000, 60000)
ax3.set_ylim(0, 33)
ax3.legend(loc="upper right", fontsize=9)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec10_fig3_tax_rates.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec10_fig3_tax_rates.png"))

print()
print("[OK] figures/lec10_fig1_four_quadrants、lec10_fig2_commons、lec10_fig3_tax_rates 已生成。")