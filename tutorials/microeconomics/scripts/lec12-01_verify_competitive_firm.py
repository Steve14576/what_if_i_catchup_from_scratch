# =====================================================================
# lec12-01 竞争企业的产量、停产与长期均衡（第 12 讲 §2-§4）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   实验 1：逐单位决策（MC = 4,5,6,7,8,9,11,13；P = 10）：
#           净得 6,5,4,3,2,1,-1,-3；累计峰值唯一在 Q = 6。
#   实验 2：用 11 讲七件套表（FC=120）验证 P=MC 规则：
#           P=90 -> Q=5，利润 +40；P=80 -> Q=5，-10（继续，AVC=58<80）；
#           P=60 -> Q=4，-90（继续，AVC=52.5<60）；P=40 -> 停产（-120）。
#   实验 3：长期均衡收敛：minATC=30、每家有效规模 q=5；
#           市场 Qd = 600-10P -> 均衡 N=60、P=30；
#           N=50 -> P=35（+25/家，进入）；N=70 -> P=25（-25/家，退出）。
#   生成 figures/lec12_fig1_unit_decision.svg/.png、
#        figures/lec12_fig2_three_cases.svg/.png、
#        figures/lec12_fig3_long_run.svg/.png。
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
print("=== 实验 1：烤到第几个？逐单位决策（P = 10） ===")
P1 = 10.0
MCs = [4, 5, 6, 7, 8, 9, 11, 13]
print("  第 k 个 | MC  | 单件净得 P-MC | 累计净得")
cum = 0
best_q, best_cum = 0, 0
for k, mc in enumerate(MCs, 1):
    net = P1 - mc
    cum += net
    if cum > best_cum:
        best_q, best_cum = k, cum
    print("    %d    | %2d  |    %+5.1f     |   %+5.1f" % (k, mc, net, cum))
print("  累计峰值：Q = %d（%+.0f 元）——最后一个'MC 不超过 10'的单位" % (best_q, best_cum))
print("  -> 结论：不烤第 7 个（MC=11 > 10，单件净亏）；规则：做到 MC <= P 的最后一个单位。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：用七件套表验证 P=MC（接 11 讲：FC=120） ===")
FC = 120.0
Qs = [1, 2, 3, 4, 5, 6]
VCs = [60.0, 100.0, 150.0, 210.0, 290.0, 390.0]
TCs = [FC + v for v in VCs]
ATCs = [TC / q for q, TC in zip(Qs, TCs)]
AVCs = [v / q for q, v in zip(Qs, VCs)]
MCs2 = [VCs[0]] + [VCs[i] - VCs[i - 1] for i in range(1, len(VCs))]
min_avc = min(AVCs)
min_atc = min(ATCs)
print("  MC 表：%s；min AVC = %.1f（Q=%d）；min ATC = %.1f（Q=%d）" %
      (MCs2, min_avc, AVCs.index(min_avc) + 1, min_atc, ATCs.index(min_atc) + 1))
for P in [90.0, 80.0, 60.0, 40.0]:
    # 选 MC <= P 的最大产量（离散规则）
    q_sel = 0
    for q, mc in zip(Qs, MCs2):
        if mc <= P:
            q_sel = q
    if P < min_avc:
        print("  P=%.0f：价格低于 minAVC -> 停产，利润 = -FC = %.0f" % (P, -FC))
    else:
        TR = P * q_sel
        TC = TCs[q_sel - 1]
        profit = TR - TC
        stop = -FC
        tag = "继续生产" if profit > stop else "与停产持平"
        print("  P=%.0f：Q=%d，利润 = %.0f（停产为 %.0f -> %s）" % (P, q_sel, profit, stop, tag))
print("  -> 结论：P>minAVC 就生产（哪怕亏损，亏得比停产少）；P<minAVC 才停产。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：长期均衡的进入-退出收敛（minATC=30，每家 q=5） ===")
print("  市场 Qd = 600 - 10P；N 家时 Q = 5N -> P = 60 - 0.5N")
for N in [50, 60, 70]:
    P = 60 - 0.5 * N
    prof = (P - 30) * 5
    signal = "进入（利润>0）" if prof > 0 else ("均衡（利润=0）" if prof == 0 else "退出（亏损）")
    print("  N=%d 家：P=%.0f，每家利润 = (%.0f-30)*5 = %+.0f -> %s" % (N, P, P, prof, signal))
print("  -> 结论：收敛于 N*=60、P*=30=minATC——长期零经济利润。")

# ---------------------------------------------------------------------
# 图 1：逐单位决策
fig, ax = plt.subplots(figsize=(7.0, 4.2), dpi=120)
ks = list(range(1, 9))
colors = ["#27ae60" if mc <= P1 else "#c0392b" for mc in MCs]
ax.bar(ks, MCs, color=colors, width=0.6, alpha=0.85)
ax.axhline(P1, color="#2c3e50", lw=2, ls="--")
ax.annotate("市场价 P = 10", xy=(0.6, 10.4), fontsize=10.5, color="#2c3e50")
ax.annotate("烤到第 6 个", xy=(6, 9.6), xytext=(6.4, 6.2), fontsize=10.5,
            arrowprops=dict(arrowstyle="->", color="#2c3e50", lw=1.2))
ax.annotate("第 7 个起：MC > P\n（每烤一个亏一点）", xy=(7.5, 12), fontsize=9.5, color="#922b21")
ax.set_xlabel("第几个面包")
ax.set_ylabel("边际成本 MC（元）")
ax.set_title("逐单位决策：MC 不超过 P 的最后一个单位")
ax.set_xticks(ks)
ax.set_ylim(0, 16)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec12_fig1_unit_decision.svg"))
fig.savefig(os.path.join(FIGDIR, "lec12_fig1_unit_decision.png"))

# ---------------------------------------------------------------------
# 图 2：三情景（用七件套表数据）
fig2, ax2 = plt.subplots(figsize=(7.0, 4.6), dpi=120)
ax2.plot(Qs, ATCs, "o-", color="#c0392b", lw=2, label="ATC")
ax2.plot(Qs, AVCs, "s-", color="#2471a3", lw=2, label="AVC")
ax2.plot(Qs, MCs2, "d-", color="#27ae60", lw=2, label="MC")
for P, c, lab in [(90, "#1e8449", "P=90：盈利（P>ATC）"),
                  (60, "#b9770e", "P=60：亏损但生产（AVC<P<ATC）"),
                  (40, "#922b21", "P=40：停产（P<minAVC）")]:
    ax2.axhline(P, color=c, lw=1.6, ls="--")
    ax2.annotate(lab, xy=(0.06, P + 3), fontsize=9, color=c)
ax2.plot([5], [82], "ko", ms=8)
ax2.annotate("minATC=82", xy=(5, 82), xytext=(3.3, 66), fontsize=9,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
ax2.plot([2.5], [50], "o", color="#2471a3", ms=7)
ax2.annotate("minAVC=50", xy=(2.5, 50), xytext=(1.1, 33), fontsize=9, color="#2471a3")
ax2.set_xlabel("产量 Q")
ax2.set_ylabel("元 / 单位")
ax2.set_title("三种价格、三种命运：盈利 / 亏损但生产 / 停产")
ax2.set_xlim(0, 7)
ax2.set_ylim(0, 200)
ax2.legend(loc="upper right", fontsize=9)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec12_fig2_three_cases.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec12_fig2_three_cases.png"))

# ---------------------------------------------------------------------
# 图 3：长期均衡双联
fig3, (axa, axb) = plt.subplots(1, 2, figsize=(10.8, 4.3), dpi=120)
axa.plot(Qs, ATCs, "o-", color="#c0392b", lw=2, label="ATC")
axa.plot(Qs, MCs2, "d-", color="#27ae60", lw=2, label="MC")
axa.axhline(82, color="#2c3e50", lw=1.8, ls="--")
axa.annotate("P = minATC = 82", xy=(0.06, 84), fontsize=9.5, color="#2c3e50")
axa.plot([5], [82], "ko", ms=8)
axa.annotate("均衡点：P=MC=minATC\n（离散表下的近似）", xy=(5, 82), xytext=(2.4, 120), fontsize=9,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
axa.set_xlabel("产量 Q（单家企业）")
axa.set_ylabel("元 / 单位")
axa.set_title("长期均衡：零经济利润的那一点", fontsize=11)
axa.set_xlim(0, 7)
axa.set_ylim(0, 200)
axa.legend(loc="upper right", fontsize=9)
Ns = [i for i in range(30, 81)]
Ps = [60 - 0.5 * n for n in Ns]
axb.plot(Ns, Ps, color="#2471a3", lw=2.2)
axb.axhline(30, color="#2c3e50", lw=1.6, ls="--")
axb.annotate("minATC = 30", xy=(31, 31.4), fontsize=9.5, color="#2c3e50")
for N, tag, xy_t, col in [(50, "P=35，利润+25 -> 进入", (33, 45.5), "#1e8449"),
                          (60, "P=30，利润 0 -> 停", (61.5, 33.5), "#2c3e50"),
                          (70, "P=25，亏 25 -> 退出", (62, 17.5), "#922b21")]:
    P = 60 - 0.5 * N
    axb.plot([N], [P], "o", color=col, ms=8)
    axb.annotate(tag, xy=(N, P), xytext=xy_t, fontsize=8.5, color=col,
                 arrowprops=dict(arrowstyle="-", color=col, lw=0.7))
axb.set_xlabel("行业内企业数 N")
axb.set_ylabel("市场价格 P")
axb.set_title("进入与退出的双向挤压：收敛到零利润", fontsize=11)
axb.set_xlim(30, 80)
axb.set_ylim(15, 52)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec12_fig3_long_run.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec12_fig3_long_run.png"))

print()
print("[OK] figures/lec12_fig1_unit_decision、lec12_fig2_three_cases、lec12_fig3_long_run 已生成。")