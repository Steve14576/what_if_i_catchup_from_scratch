# =====================================================================
# lec09-01 外部性、庇古税与许可证（第 09 讲 §1-§5）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   主场景（负外部性：钢厂烟尘，外部成本 10/单位）：
#     需求 P = 50-Q/2；私人供给 P = 10+Q/2；社会供给 P = 20+Q/2。
#   实验 1：私人均衡 (40,30) 社会净 400 vs 社会最优 (30,35) 净 450；
#           DWL = 50 = (1/2)*10*10。
#   实验 2：庇古税 t=10 -> 市场自发落到 (30,35)；税后账：
#           CS=225 PS=225 税=300 外部=300 净=450。
#   实验 3：正外部性对照（外部收益 10/单位）：私人 (40,30) vs 最优 (50,35)；
#           补贴 10；社会净 1200 -> 1250。
#   实验 4：许可证交易（A 减排成本 2、B 成本 8；目标 20 吨）：
#           统一管制 100 vs 交易后 70，省 30。
#   生成 figures/lec09_fig1_negative.svg/.png、
#        figures/lec09_fig2_positive.svg/.png、
#        figures/lec09_fig3_permit.svg/.png。
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

EXT = 10.0   # 边际外部成本（钢厂场景）


def cs_at(Q, p):
    # 反需求 P_d = 50 - Q/2
    return Q * (50 - p) - Q * Q / 4


def ps_at(Q, p):
    # 反私人供给 P_s = 10 + Q/2
    return Q * (p - 10) - Q * Q / 4


# ---------------------------------------------------------------------
print("=== 实验 1：钢厂的私人账 vs 社会的真账（外部成本 10/单位） ===")
# 私人均衡：50-Q/2 = 10+Q/2 -> Q=40, P=30
Qm, Pm = 40.0, 30.0
cs_m, ps_m = cs_at(Qm, Pm), ps_at(Qm, Pm)
ext_m = EXT * Qm
print("  私人均衡 (%.0f, %.0f)：CS=%.0f  PS=%.0f  外部损害=%.0f  社会净=%.0f" %
      (Qm, Pm, cs_m, ps_m, ext_m, cs_m + ps_m - ext_m))
# 社会最优：50-Q/2 = 20+Q/2 -> Q=30, P=35
Qo, Po = 30.0, 35.0
cs_o = cs_at(Qo, Po)
ps_o_social = Qo * (Po - 10) - Qo * Qo / 4     # 以"社会供给"（含外部成本）为成本口径
ext_o = EXT * Qo
print("  社会最优 (%.0f, %.0f)：CS=%.0f  生产者净得（含外部成本口径）=%.0f  外部损害=%.0f  社会净=%.0f" %
      (Qo, Po, cs_o, ps_o_social, ext_o, cs_o + ps_o_social - ext_o))
print("  DWL = %.0f = (1/2)×10×10（超额产量 10 单位 × 外部成本 10）" % (450 - 400))
print("  -> 结论：市场自发多产 10 单位；把外部账补上，社会净从 450 掉到 400 的差额正是 DWL。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：庇古税 t=10：内部化 ===")
# 征税后私人市场：需求 50-Q/2 与 税后供给 20+Q/2 -> (30, 35)
qt, pbt = 30.0, 35.0
pst = pbt - EXT
cs_t = cs_at(qt, pbt)
ps_t = ps_at(qt, pst)
tax_rev = EXT * qt
print("  税后落点 (%.0f, %.0f)：买者付 %.0f、卖者得 %.0f（税 10）" % (qt, pbt, pbt, pst))
print("  税后账：CS=%.0f  PS=%.0f  税=%.0f  外部损害=%.0f  社会净=%.0f" %
      (cs_t, ps_t, tax_rev, ext_o, cs_t + ps_t + tax_rev - ext_o))
print("  -> 结论：庇古税 = 边际外部成本时，私人市场自发落到社会最优点；社会净回到 450。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：正外部性对照（外部收益 10/单位，如疫苗） ===")
# 私人均衡不变 (40,30)；社会需求 60-Q/2 与供给 10+Q/2 -> (50,35)
Qp, Pp = 50.0, 35.0
# 私人均衡社会净 = CS + PS + 外部收益
print("  私人均衡 (40, 30)：CS=%.0f  PS=%.0f  外部收益=%.0f  社会净=%.0f" %
      (cs_m, ps_m, EXT * 40, cs_m + ps_m + EXT * 40))
# 社会最优：买家实付 25（补贴 10），卖者得 35
cs_p = cs_at(Qp, 25.0)
ps_p = ps_at(Qp, 35.0)
print("  补贴 10 后落点 (%.0f)：买者实付 25、卖者得 35" % Qp)
print("  最优账：CS=%.0f  PS=%.0f  外部收益=%.0f  补贴支出=%.0f  社会净=%.0f" %
      (cs_p, ps_p, EXT * Qp, EXT * Qp, cs_p + ps_p + EXT * Qp - EXT * Qp))
print("  -> 结论：正外部性下市场产太少（40 < 50）；补贴把量推回最优，社会净 1200 -> 1250。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：许可证交易（A 成本 2 元/吨，B 成本 8 元/吨；目标减排 20 吨） ===")
cA, cB, target = 2.0, 8.0, 20.0
uniform = cA * 10 + cB * 10
trade = cA * 15 + cB * 5
print("  统一管制（各减 10 吨）：%.0f×10 + %.0f×10 = %.0f" % (cA, cB, uniform))
print("  可交易（A 减 15、B 减 5）：%.0f×15 + %.0f×5 = %.0f" % (cA, cB, trade))
print("  证价 5 落在两家成本之间（2 < 5 < 8）：A 卖证多减、B 买证少减，双方都赚。")
print("  -> 结论：同样完成 20 吨减排，交易比统一管制省 %.0f 元（%.0f%%）。" % (uniform - trade, (uniform - trade) / uniform * 100))

# ---------------------------------------------------------------------
# 图 1：负外部性主图
fig, ax = plt.subplots(figsize=(7.2, 4.8), dpi=120)
qq = [i / 2 for i in range(0, 141)]
dem = [50 - q / 2 for q in qq]
sup = [10 + q / 2 for q in qq]
soc = [20 + q / 2 for q in qq]
ax.plot(qq, dem, color="#c0392b", lw=2, label="需求")
ax.plot(qq, sup, color="#2471a3", lw=2, label="私人供给（钢厂的成本）")
ax.plot(qq, soc, color="#8e44ad", lw=2, ls="--", label="社会供给（成本 + 外部损害 10）")
ax.fill([30, 40, 30], [35, 30, 25], color="#95a5a6", alpha=0.8)
ax.plot([40], [30], "ko", ms=8)
ax.annotate("私人均衡 (40, 30)\n市场自发：产太多", xy=(40, 30), xytext=(42, 19), fontsize=9.5,
            arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
ax.plot([30], [35], "ko", ms=8)
ax.annotate("社会最优 (30, 35)", xy=(30, 35), xytext=(14, 40), fontsize=9.5,
            arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
ax.annotate("DWL=50", xy=(31, 29.2), fontsize=10.5, color="#2c3e50")
ax.annotate("外部损害 10/单位", xy=(2, 16), fontsize=9.5, color="#8e44ad")
ax.set_xlabel("钢产量 Q")
ax.set_ylabel("价格 P")
ax.set_title("负外部性：私人账本里没有的那 10 元")
ax.set_xlim(0, 70)
ax.set_ylim(0, 55)
ax.legend(loc="upper right", fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec09_fig1_negative.svg"))
fig.savefig(os.path.join(FIGDIR, "lec09_fig1_negative.png"))

# ---------------------------------------------------------------------
# 图 2：正外部性
fig2, ax2 = plt.subplots(figsize=(7.2, 4.8), dpi=120)
soc_dem = [60 - q / 2 for q in qq]
ax2.plot(qq, dem, color="#c0392b", lw=2, label="私人需求")
ax2.plot(qq, soc_dem, color="#8e44ad", lw=2, ls="--", label="社会需求（私人 + 外部收益 10）")
ax2.plot(qq, sup, color="#2471a3", lw=2, label="供给")
ax2.fill([40, 40, 50], [30, 40, 35], color="#95a5a6", alpha=0.8)
ax2.plot([40], [30], "ko", ms=8)
ax2.annotate("私人均衡 (40, 30)\n市场自发：产太少", xy=(40, 30), xytext=(20, 20), fontsize=9.5,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
ax2.plot([50], [35], "ko", ms=8)
ax2.annotate("社会最优 (50, 35)", xy=(50, 35), xytext=(52, 40), fontsize=9.5,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
ax2.annotate("DWL=50", xy=(44, 33), fontsize=10.5, color="#2c3e50")
ax2.set_xlabel("疫苗数量 Q")
ax2.set_ylabel("价格 P")
ax2.set_title("正外部性：没被私人算进的 10 元好处")
ax2.set_xlim(0, 70)
ax2.set_ylim(0, 65)
ax2.legend(loc="upper right", fontsize=8)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec09_fig2_positive.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec09_fig2_positive.png"))

# ---------------------------------------------------------------------
# 图 3：许可证示意（双联）
fig3, (axa, axb) = plt.subplots(1, 2, figsize=(10.6, 4.2), dpi=120)
axa.plot([0, 20], [2, 2], color="#27ae60", lw=2.4, label="A 企业减排成本 2")
axa.plot([0, 20], [8, 8], color="#c0392b", lw=2.4, label="B 企业减排成本 8")
axa.plot([0, 20], [5, 5], color="#e67e22", lw=1.8, ls="--", label="许可证市价 5")
axa.annotate("A 低于市价：多减、卖证赚差价", xy=(1, 2.4), fontsize=9.5, color="#1e8449")
axa.annotate("B 高于市价：少减、买证更划算", xy=(1, 8.4), fontsize=9.5, color="#922b21")
axa.set_xlabel("减排量（吨）")
axa.set_ylabel("成本（元/吨）")
axa.set_title("可交易许可证：谁的成本低谁多减", fontsize=11)
axa.set_xlim(0, 20)
axa.set_ylim(0, 11)
axa.legend(loc="center right", fontsize=8)
axb.bar([0, 1], [uniform, trade], color=["#bdc3c7", "#27ae60"], width=0.5)
axb.annotate("统一管制\n100 元", xy=(0, uniform), xytext=(-0.12, uniform + 5), fontsize=10)
axb.annotate("可交易\n70 元", xy=(1, trade), xytext=(0.88, trade + 5), fontsize=10)
axb.annotate("省 30 元", xy=(1, 35), fontsize=11, color="#ffffff")
axb.set_xticks([0, 1])
axb.set_xticklabels(["强制一刀切", "交易后"])
axb.set_ylim(0, 120)
axb.set_ylabel("完成 20 吨减排的总成本")
axb.set_title("同样的减排目标，成本差三成", fontsize=11)
fig3.suptitle("许可证与交易：把减排任务交给'最省钱的人'", fontsize=12)
fig3.tight_layout(rect=[0, 0, 1, 0.94])
fig3.savefig(os.path.join(FIGDIR, "lec09_fig3_permit.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec09_fig3_permit.png"))

print()
print("[OK] figures/lec09_fig1_negative、lec09_fig2_positive、lec09_fig3_permit 已生成。")