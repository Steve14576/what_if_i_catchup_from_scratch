# =====================================================================
# lec14-01 垄断竞争、博弈论与古诺寡头（第 14 讲 §1-§4）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   实验 1：垄断竞争长期均衡相切验证：P = 30-Q、MC = 10、ATC = 10+100/Q：
#           相切点 (10, 20)：P = ATC（零利润）、P > MC（markup，数字例简化）。
#           短期对照：若需求 P = 34-Q（未调整时）：Q=12、P=22、
#           ATC=18.33、利润 = 44（>0 -> 吸引进入）。
#   实验 2：囚徒困境（两家奶茶大店的"降价/维持"矩阵）：
#           占优策略验证（双方"降价"占优）+ 纳什均衡 (降价, 降价) = 60/60。
#   实验 3：古诺反应函数迭代（P = 100-Q、MC = 10、q = (90-q')/2）：
#           从 (10,10) 与 (50,50) 都收敛到 (30, 30)。
#   实验 4：古诺 vs 合谋 vs 竞争三方对照：
#           Q = 60 / 45 / 90；P = 40 / 55 / 10；利润 1800 / 2025 / 0。
#   生成 figures/lec14_fig1_monopolistic.svg/.png、
#        figures/lec14_fig2_prisoner.svg/.png、
#        figures/lec14_fig3_cournot.svg/.png。
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
print("=== 实验 1：垄断竞争长期均衡的相切验证（P = 30-Q；MC = 10；ATC = 10+100/Q） ===")
print("  相切点：MR = 30-2Q = 10 -> Q = 10；P = 30-10 = 20")
print("  ATC(10) = 10 + 100/10 = 20 = P -> 经济利润 0（相切）")
print("  P - MC = 20 - 10 = 10 > 0（加成定价：价格高于边际成本）")
print("  短期对照：若需求暂时是 P = 34-Q：MR = 34-2Q = 10 -> Q = 12；P = 22")
print("            ATC(12) = 10 + 100/12 = %.2f；利润 = (22 - %.2f) * 12 = %.0f > 0" %
      (10 + 100 / 12, 10 + 100 / 12, (22 - (10 + 100 / 12)) * 12))
print("  -> 结论：正利润吸引新店进入 -> 老店需求被挤短 -> 一路挤到'相切、零利润'。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：囚徒困境（两家奶茶大店：降价 / 维持高价） ===")
# 支付矩阵（万元利润）：(A 的利润, B 的利润)
M = {
    ("维持", "维持"): (100, 100),
    ("维持", "降价"): (40, 130),
    ("降价", "维持"): (130, 40),
    ("降价", "降价"): (60, 60),
}
print("  矩阵（万元）：")
print("            B 维持   |  B 降价")
print("  A 维持  | 100 /100 | 40 /130")
print("  A 降价  | 130/ 40  | 60 / 60")
# 占优策略验证
for firm, ix in [("A", 0), ("B", 1)]:
    vals = {}
    for s in ["维持", "降价"]:
        for other in ["维持", "降价"]:
            if ix == 0:
                vals[(s, other)] = M[(s, other)][0]
            else:
                vals[(s, other)] = M[(other, s)][1]
    cheap_when_high = vals[("降价", "维持")] > vals[("维持", "维持")]
    cheap_when_low = vals[("降价", "降价")] > vals[("维持", "降价")]
    print("  %s：对方维持时降价更优（%d>%d）=%s；对方降价时降价更优（%d>%d）=%s -> 降价是占优策略" %
          (firm, vals[("降价", "维持")], vals[("维持", "维持")], cheap_when_high,
           vals[("降价", "降价")], vals[("维持", "降价")], cheap_when_low))
print("  纳什检查 (降价,降价)=(60,60)：单方改'维持'会变成 40 < 60 -> 没人愿意单方面偏离")
print("  -> 结论：双方占优策略都指向降价；但 (维持,维持) = 100/100 对双方更好——囚徒困境。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：古诺反应函数的迭代（P = 100-Q；MC = 10；q1 = (90-q2)/2） ===")
for q1, q2 in [(10.0, 10.0), (50.0, 50.0)]:
    print("  从 (%.0f, %.0f) 出发：" % (q1, q2))
    for t in range(5):
        q1 = (90 - q2) / 2
        q2 = (90 - q1) / 2
        print("    第 %d 轮：q1 = %.2f，q2 = %.2f" % (t + 1, q1, q2))
print("  收敛点：q1 = q2 = 30（验证：(90-30)/2 = 30，稳定）")
print("  -> 结论：各自'对对方产量的最佳反应'反复代入，收敛到古诺均衡 (30, 30)。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：古诺 vs 合谋 vs 竞争（P = 100-Q；MC = 10） ===")
# 古诺：(30, 30) -> Q=60, P=40
q_古, p_古 = 60.0, 40.0
# 合谋：总 MR = 100-2Q = 10 -> Q = 45, P = 55
q_合, p_合 = 45.0, 55.0
# 竞争：P = MC = 10 -> Q = 90
q_竞, p_竞 = 90.0, 10.0
for name, Q, P in [("合谋（像一家垄断）", q_合, p_合), ("古诺双头", q_古, p_古), ("竞争（P=MC）", q_竞, p_竞)]:
    prof = (P - 10) * Q
    print("  %s：Q=%.0f  P=%.0f  行业利润=%.0f（每家 %.0f）" %
          (name, Q, P, prof, prof / 2 if name != "竞争（P=MC）" else prof))
print("  -> 结论：古诺的产量（60）夹在垄断（45）与竞争（90）之间；")
print("     利润（1800）低于合谋（2025）——'自利'把行业推离了合作水平。")

# ---------------------------------------------------------------------
# 图 1：垄断竞争长期均衡（示意）
fig, ax = plt.subplots(figsize=(7.4, 4.8), dpi=120)
qs = [i / 4 for i in range(8, 49)]             # 2 .. 12
atc = [0.5 * (q - 8) ** 2 + 16 for q in qs]
mc = [1.5 * q * q - 16 * q + 48 for q in qs]
dem = [35.5 - 3 * q for q in qs]
ax.plot(qs, atc, color="#8e44ad", lw=2.2, label="ATC（U 形）")
ax.plot(qs, mc, color="#2471a3", lw=2.2, label="MC")
ax.plot(qs, dem, color="#c0392b", lw=2.2, label="每家的需求 D")
ax.plot([5], [20.5], "ko", ms=9)
ax.plot([8], [16], "o", color="#7f8c8d", ms=8)
ax.plot([5, 5], [0, 20.5], color="#7f8c8d", ls=":", lw=1)
ax.plot([8, 8], [0, 16], color="#7f8c8d", ls=":", lw=1)
ax.annotate("长期均衡：相切、零利润\n(5, 20.5)", xy=(5, 20.5), xytext=(1.2, 28), fontsize=9,
            arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
ax.annotate("有效规模 (8, 16)", xy=(8, 16), xytext=(8.6, 10), fontsize=9, color="#7f8c8d")
ax.annotate("", xy=(5, 25.2), xytext=(8, 25.2), arrowprops=dict(arrowstyle="<->", color="#e67e22", lw=1.4))
ax.annotate("过剩产能", xy=(5.6, 26), fontsize=9.5, color="#b9770e")
ax.annotate("P=20.5 > MC=5.5：加成定价", xy=(5, 20.5), xytext=(7.6, 6.0), fontsize=9.5, color="#922b21",
            arrowprops=dict(arrowstyle="-", color="#922b21", lw=0.8))
ax.set_xlabel("产量 Q（单家店）")
ax.set_ylabel("价格 P")
ax.set_title("垄断竞争的长期均衡：在最低点'左边'相切（示意图）")
ax.set_xlim(0, 12)
ax.set_ylim(0, 34)
ax.legend(loc="upper right", fontsize=8.5)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec14_fig1_monopolistic.svg"))
fig.savefig(os.path.join(FIGDIR, "lec14_fig1_monopolistic.png"))

# ---------------------------------------------------------------------
# 图 2：囚徒困境矩阵
fig2, ax2 = plt.subplots(figsize=(7.0, 5.0), dpi=120)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis("off")
labels = [
    (2.5, 7.5, "维持 / 维持\n100 / 100", "#d5f5e3"),
    (7.0, 7.5, "维持 / 降价\n40 / 130", "#fdebd0"),
    (2.5, 3.8, "降价 / 维持\n130 / 40", "#fdebd0"),
    (7.0, 3.8, "降价 / 降价\n60 / 60", "#fadbd8"),
]
for x, y, t, c in labels:
    ax2.add_patch(plt.Rectangle((x - 1.9, y - 1.5), 3.8, 3.0, facecolor=c, edgecolor="#566573", lw=1.6))
    ax2.text(x, y, t, ha="center", va="center", fontsize=12)
ax2.text(0.35, 5.7, "A 维持", rotation=90, va="center", fontsize=11)
ax2.text(0.35, 2.9, "A 降价", rotation=90, va="center", fontsize=11)
ax2.text(2.5, 9.4, "B 维持", ha="center", fontsize=11)
ax2.text(7.0, 9.4, "B 降价", ha="center", fontsize=11)
ax2.text(11.0, 9.4, "", fontsize=1)
ax2.text(4.75, 1.2, "纳什均衡：(降价, 降价) = 60 / 60\n（但 100 / 100 其实对双方更好）", ha="center", fontsize=11, color="#922b21")
ax2.set_title("囚徒困境（奶茶大店版）：个体理性，集体买单", fontsize=12)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec14_fig2_prisoner.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec14_fig2_prisoner.png"))

# ---------------------------------------------------------------------
# 图 3：古诺反应函数与收敛
fig3, ax3 = plt.subplots(figsize=(6.8, 5.0), dpi=120)
q2s = [i / 2 for i in range(0, 181)]           # 0 .. 90
ax3.plot([(90 - x) / 2 for x in q2s], q2s, color="#c0392b", lw=2.2, label="店 1 的反应函数 q1=(90-q2)/2")
ax3.plot(q2s, [(90 - x) / 2 for x in q2s], color="#2471a3", lw=2.2, label="店 2 的反应函数 q2=(90-q1)/2")
ax3.plot([30], [30], "ko", ms=9)
ax3.annotate("古诺均衡 (30, 30)", xy=(30, 30), xytext=(38, 22), fontsize=10,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
# 迭代台阶（从 (50, 50) 出发）
q1, q2 = 50.0, 50.0
pxs, pys = [q1], [q2]
for _ in range(4):
    q1 = (90 - q2) / 2
    pxs.append(q1); pys.append(q2)
    q2 = (90 - q1) / 2
    pxs.append(q1); pys.append(q2)
ax3.plot(pxs, pys, "o--", color="#27ae60", lw=1.4, ms=4, label="迭代路径（从 50,50 出发）")
ax3.set_xlabel("店 1 的产量 q1")
ax3.set_ylabel("店 2 的产量 q2")
ax3.set_title("古诺双头：两条反应函数交于均衡")
ax3.set_xlim(0, 90)
ax3.set_ylim(0, 90)
ax3.legend(loc="upper right", fontsize=8.5)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec14_fig3_cournot.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec14_fig3_cournot.png"))

print()
print("[OK] figures/lec14_fig1_monopolistic、lec14_fig2_prisoner、lec14_fig3_cournot 已生成。")