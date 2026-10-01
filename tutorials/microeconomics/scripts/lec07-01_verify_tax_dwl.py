# =====================================================================
# lec07-01 税收的无谓损失与拉弗曲线（第 07 讲 §1-§4）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   主场景（05 讲实验 3 的延续）：Qd = 200-10P；Qs = 10P-100。
#   实验 1：四方账本。无税 (50,15)：CS=125、PS=125、TS=250；
#           t=4 -> P_b=17、P_s=13、Q=30：CS=45、PS=45、政府=120、
#           合计 210、DWL=40。
#   实验 2：损失拆解：CS 减少 80 = 转移 60 + 蒸发 20；PS 同。
#   实验 3：税率扫描 t=2,4,6,8,10：DWL = 2.5 t^2（平方量级）；
#           收入 R(t) = t(50-5t) 峰值在 t=5（Laffer）。
#   实验 4：弹性对照：更陡需求（Qd=80-2P，同起点）在 t=4 下
#           DWL 约 13.33（vs 40）——越缺弹性、损失越小。
#   生成 figures/lec07_fig1_four_zones.svg/.png、
#        figures/lec07_fig2_laffer_dwl.svg/.png、
#        figures/lec07_fig3_elasticity_dwl.svg/.png。
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

# 主场景：反需求 P = 20 - Q/10；反供给 P = 10 + Q/10
# 无税均衡 (50, 15)；向卖者征 t：P_b = 15 + t/2；Q(t) = 50 - 5t


def Pb_of(t):
    return 15 + t / 2


def Q_of(t):
    return 50 - 5 * t


def R_of(t):
    return t * Q_of(t)


def DWL_of(t):
    return 0.5 * t * (5 * t)   # ½ * t * ΔQ，ΔQ = 5t


# ---------------------------------------------------------------------
print("=== 实验 1：四方账本（无税 vs t=4） ===")
# 无税：CS = ½*50*(20-15) = 125；PS = ½*50*(15-10) = 125
cs0, ps0 = 125.0, 125.0
print("  无税 (50, 15)：CS=%.0f  PS=%.0f  TS=%.0f" % (cs0, ps0, cs0 + ps0))
t = 4.0
Q1 = Q_of(t)
cs1 = 0.5 * Q1 * (20 - Pb_of(t))          # 需求线与 P_b 之间（Q ≤ 30 时也是三角）
ps1 = 0.5 * Q1 * (Pb_of(t) - t - 10)      # P_s 与供给线之间
tax = t * Q1
print("  t=4 (Q=%.0f)：P_b=%.0f  P_s=%.0f" % (Q1, Pb_of(t), Pb_of(t) - t))
print("  CS=%.0f  PS=%.0f  政府税收=%.0f  合计=%.0f" % (cs1, ps1, tax, cs1 + ps1 + tax))
print("  DWL = %.0f（对比无税 TS=%.0f）" % (cs0 + ps0 - (cs1 + ps1 + tax), cs0 + ps0))
print("  -> 结论：CS 与 PS 各损 80，其中 120 变成税收（转移），40 无人得到（蒸发）。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：损失拆解（每方 80 = 转移 60 + 蒸发 20） ===")
transfer_each = (Pb_of(t) - 15) * Q1     # 买家每单位多付 2 * 30 = 60
vanish_each = 0.5 * (50 - Q1) * (Pb_of(t) - 15)   # 小三角 ½*20*2 = 20
print("  买家：CS 减 %.0f = 转给政府 %.0f + 蒸发 %.0f" % (cs0 - cs1, transfer_each, vanish_each))
print("  卖家：PS 减 %.0f = 转给政府 %.0f + 蒸发 %.0f" % (ps0 - ps1, transfer_each, vanish_each))
print("  -> 结论：DWL = %.0f = 两块小三角之和（%0.f + %.0f）——它不在任何人口袋里。" %
      (2 * vanish_each, vanish_each, vanish_each))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：税率扫描（平方律与拉弗） ===")
print("   t  |   Q  | 政府收入 |  DWL")
for tt in [2.0, 4.0, 6.0, 8.0, 10.0]:
    print("  %2.0f  | %3.0f  |  %5.0f   | %5.0f" % (tt, Q_of(tt), R_of(tt), DWL_of(tt)))
print("  连续峰值：收入在 t=5 处最大（R=%.0f）；DWL(t) = 2.5*t^2 单调加速上升" % R_of(5.0))
print("  平方律验证：t=2->4，DWL %.0f->%.0f（x%.0f）；t=4->8，DWL %.0f->%.0f（x%.0f）" %
      (DWL_of(2), DWL_of(4), DWL_of(4) / DWL_of(2), DWL_of(4), DWL_of(8), DWL_of(8) / DWL_of(4)))
print("  t=10（Q=0）：市场关停，收入 0，DWL=%.0f = 原 TS 全部蒸发" % DWL_of(10))
print("  -> 结论：收入先升后降（拉弗山）；DWL 一路平方式加速。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：弹性对照（更陡的需求） ===")
# 市场 B：Qd = 80 - 2P（反需求 P = 40 - Q/2），同起点 (50, 15)，Qs 同
# P_b = 15 + t*10/12；Q_B(t) = 50 - (5/3)t
tB = 4.0
PbB = 15 + tB * 10 / 12
QB = 50 - (5 / 3) * tB
dQB = 50 - QB
DWLB = 0.5 * tB * dQB
print("  A（需求平/富弹性）：t=4 -> ΔQ=20，DWL=40")
print("  B（需求陡/缺弹性）：t=4 -> P_b=%.2f，ΔQ=%.2f，DWL=%.2f" % (PbB, dQB, DWLB))
print("  -> 结论：同一笔税，需求越缺弹性、被吓退的交易越少，DWL 越小。")

# ---------------------------------------------------------------------
# 图 1：四区图
fig, ax = plt.subplots(figsize=(7.4, 5.0), dpi=120)
qs = [i / 2 for i in range(0, 141)]           # 0 .. 70
dem = [20 - q / 10 for q in qs]
sup = [10 + q / 10 for q in qs]
sup_tax = [14 + q / 10 for q in qs]
q30 = [i / 2 for i in range(0, 61)]           # 0 .. 30
ax.plot(qs, dem, color="#c0392b", lw=2, label="需求")
ax.plot(qs, sup, color="#bdc3c7", lw=1.8, ls="--", label="原供给")
ax.plot(qs, sup_tax, color="#2471a3", lw=2, label="征税后供给（上移 4）")
ax.fill_between(q30, [20 - q / 10 for q in q30], 17, color="#aed6f1", alpha=0.55)
ax.fill_between(q30, 13, [14 + q / 10 for q in q30], color="#f5cba7", alpha=0.7)
ax.fill_between(q30, 13, 17, color="#d5f5e3", alpha=0.9)
tri_x = [30, 50, 30]
tri_top = [17, 15, 13]
ax.fill(tri_x, tri_top, color="#95a5a6", alpha=0.8)
ax.plot([30], [17], "ko", ms=7)
ax.plot([30], [13], "ko", ms=7)
ax.plot([50], [15], "o", color="#7f8c8d", ms=7)
ax.annotate("CS=45", xy=(10, 18.2), fontsize=10, color="#1a5276")
ax.annotate("PS=45", xy=(10, 11.8), fontsize=10, color="#935116")
ax.annotate("税收\n120", xy=(13, 15), fontsize=10, color="#1e8449")
ax.annotate("DWL=40", xy=(36, 14.4), fontsize=11, color="#2c3e50")
ax.annotate("原均衡 (50, 15)", xy=(50, 15), xytext=(52, 16.6), fontsize=9.5, color="#7f8c8d")
ax.annotate("新均衡\n(30, 17/13)", xy=(30, 17), xytext=(25.5, 19.4), fontsize=9.5)
ax.set_xlabel("数量 Q")
ax.set_ylabel("价格 P")
ax.set_title("一笔税的四块账：CS、PS、政府税收、以及蒸发掉的 DWL")
ax.set_xlim(0, 70)
ax.set_ylim(0, 24)
ax.legend(loc="upper right", fontsize=8.5)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec07_fig1_four_zones.svg"))
fig.savefig(os.path.join(FIGDIR, "lec07_fig1_four_zones.png"))

# ---------------------------------------------------------------------
# 图 2：拉弗山 + DWL 抛物线
fig2, (axa, axb) = plt.subplots(1, 2, figsize=(10.6, 4.2), dpi=120)
ts = [i / 20 for i in range(0, 201)]          # 0 .. 10
axa.plot(ts, [R_of(t) for t in ts], color="#27ae60", lw=2.2)
axa.plot([5], [125], "ko", ms=9)
axa.annotate("峰：t=5，收入 125", xy=(5, 125), xytext=(3.4, 60), fontsize=10)
axa.set_xlabel("单位税 t")
axa.set_ylabel("政府收入")
axa.set_title("拉弗山：税收收入先升后降", fontsize=11)
axa.set_xlim(0, 10)
axa.set_ylim(0, 145)
axb.plot(ts, [DWL_of(t) for t in ts], color="#c0392b", lw=2.2)
for tt in [2.0, 4.0, 8.0]:
    axb.plot([tt], [DWL_of(tt)], "o", color="#e67e22", ms=7)
    axb.annotate("t=%d: %.0f" % (tt, DWL_of(tt)), xy=(tt, DWL_of(tt)), xytext=(tt + 0.3, DWL_of(tt) + 8), fontsize=9, color="#e67e22")
axb.set_xlabel("单位税 t")
axb.set_ylabel("无谓损失 DWL")
axb.set_title("DWL 抛物线：t 翻倍，损失约四倍", fontsize=11)
axb.set_xlim(0, 10)
axb.set_ylim(0, 280)
fig2.suptitle("税率的两个后果：收入会回落，损失不会", fontsize=12)
fig2.tight_layout(rect=[0, 0, 1, 0.94])
fig2.savefig(os.path.join(FIGDIR, "lec07_fig2_laffer_dwl.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec07_fig2_laffer_dwl.png"))

# ---------------------------------------------------------------------
# 图 3：弹性对照（A 富弹性 vs B 缺弹性）
fig3, axes = plt.subplots(1, 2, figsize=(10.6, 4.4), dpi=120)
# 左：A
axA = axes[0]
qA = [i / 2 for i in range(0, 111)]
axA.plot(qA, [20 - q / 10 for q in qA], color="#c0392b", lw=2, label="需求 A（平）")
axA.plot(qA, [10 + q / 10 for q in qA], color="#bdc3c7", lw=1.6, ls="--", label="原供给")
axA.plot(qA, [14 + q / 10 for q in qA], color="#2471a3", lw=2, label="征税后供给")
axA.fill([30, 50, 30], [17, 15, 13], color="#95a5a6", alpha=0.75)
axA.annotate("消失 20 单位", xy=(40, 15.0), xytext=(44.5, 12.3), fontsize=9.5, color="#566573", arrowprops=dict(arrowstyle="-", color="#566573", lw=0.8))
axA.annotate("DWL=40", xy=(33, 14.3), fontsize=10.5, color="#2c3e50")
axA.set_xlim(0, 70)
axA.set_ylim(0, 24)
axA.set_xlabel("数量 Q")
axA.set_ylabel("价格 P")
axA.set_title("A：需求平（富弹性）——交易丢得多", fontsize=10.5)
axA.legend(loc="upper right", fontsize=8)
# 右：B
axB = axes[1]
qB = [i / 2 for i in range(0, 111)]
axB.plot(qB, [40 - q / 2 for q in qB], color="#c0392b", lw=2, label="需求 B（陡）")
axB.plot(qB, [10 + q / 10 for q in qB], color="#bdc3c7", lw=1.6, ls="--", label="原供给")
axB.plot(qB, [14 + q / 10 for q in qB], color="#2471a3", lw=2, label="征税后供给")
xq = 43.3333
pbBv = 40 - xq / 2
axB.fill([43.3333, 50, 43.3333], [pbBv, 15, pbBv - 4], color="#95a5a6", alpha=0.75)
axB.annotate("只消失 6.7 单位", xy=(32, 19.6), fontsize=9.5, color="#566573")
axB.annotate("DWL≈13.3", xy=(40, 12.8), fontsize=10.5, color="#2c3e50")
axB.set_xlim(0, 70)
axB.set_ylim(0, 24)
axB.set_xlabel("数量 Q")
axB.set_ylabel("价格 P")
axB.set_title("B：需求陡（缺弹性）——交易丢得少", fontsize=10.5)
axB.legend(loc="upper right", fontsize=8)
fig3.suptitle("同样的税，弹性越小、死损失越小", fontsize=12)
fig3.tight_layout(rect=[0, 0, 1, 0.94])
fig3.savefig(os.path.join(FIGDIR, "lec07_fig3_elasticity_dwl.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec07_fig3_elasticity_dwl.png"))

print()
print("[OK] figures/lec07_fig1_four_zones、lec07_fig2_laffer_dwl、lec07_fig3_elasticity_dwl 已生成。")