# =====================================================================
# lec08-01 国际贸易的赢家输家与关税（第 08 讲 §1-§3）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   国内市场：Qd = 100-2P；Qs = 2P-20（封闭均衡 (40, 30)）。
#   实验 1：进口国三级账（世界价 20）。
#     封闭：(40,30) CS=400 PS=400 TS=800；
#     自贸（价20）：Qd=60 Qs=20 进口=40；CS=900 PS=100 TS=1000；
#     关税 t=5（价25）：Qd=50 Qs=30 进口=20；CS=625 PS=225 收入=100
#       合计950；DWL=50（两块三角各 25）。
#   实验 2：出口国两级账（世界价 40）：出口=40；CS=100 PS=900 TS=1000。
#   实验 3：关税扫描 t=0..10：进口 = 40-4t；收入 R=t(40-4t) 峰 t=5（100）；
#     DWL = 2t^2（两块三角各 t^2）：t=2.5 -> 12.5；t=5 -> 50；t=10 -> 200。
#   生成 figures/lec08_fig1_importer.svg/.png、
#        figures/lec08_fig2_exporter.svg/.png、
#        figures/lec08_fig3_tariff_zones.svg/.png。
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

# 反需求 P = 50 - Q/2；反供给 P = 10 + Q/2
# 世界价 20：Qd(20)=60、Qs(20)=20；世界价 40：Qd(40)=20、Qs(40)=60


def Qd(P):
    return 100 - 2 * P


def Qs(P):
    return 2 * P - 20


def cs_of(Q_at_p, p):
    # CS = ½*Q*(50-50+…) 直接用三角：需求截距 50
    return 0.5 * Q_at_p * (50 - p)


def ps_of(Q_at_p, p):
    # PS = ½*Q*(p-10)
    return 0.5 * Q_at_p * (p - 10)


# ---------------------------------------------------------------------
print("=== 实验 1：进口国（世界价 20 < 封闭价 30）的三级账 ===")
print("  封闭（无贸易）：P*=30，Q*=40 -> CS=%.0f  PS=%.0f  TS=%.0f" %
      (cs_of(40, 30), ps_of(40, 30), cs_of(40, 30) + ps_of(40, 30)))
pw = 20.0
print("  自由贸易（世界价 %.0f）：Qd=%.0f Qs=%.0f -> 进口=%.0f" % (pw, Qd(pw), Qs(pw), Qd(pw) - Qs(pw)))
print("     CS=%.0f  PS=%.0f  TS=%.0f（比封闭 %+.0f）" %
      (cs_of(Qd(pw), pw), ps_of(Qs(pw), pw), cs_of(Qd(pw), pw) + ps_of(Qs(pw), pw),
       cs_of(Qd(pw), pw) + ps_of(Qs(pw), pw) - 800))
t = 5.0
pt = pw + t
print("  关税 t=%.0f（国内价 %.0f）：Qd=%.0f Qs=%.0f -> 进口=%.0f" % (t, pt, Qd(pt), Qs(pt), Qd(pt) - Qs(pt)))
rev = t * (Qd(pt) - Qs(pt))
print("     CS=%.0f  PS=%.0f  关税收入=%.0f  合计=%.0f" %
      (cs_of(Qd(pt), pt), ps_of(Qs(pt), pt), rev, cs_of(Qd(pt), pt) + ps_of(Qs(pt), pt) + rev))
print("     DWL = %.0f（= 自贸 TS %.0f - 关税 TS %.0f）" %
      (1000 - (cs_of(Qd(pt), pt) + ps_of(Qs(pt), pt) + rev),
       cs_of(Qd(pw), pw) + ps_of(Qs(pw), pw),
       cs_of(Qd(pt), pt) + ps_of(Qs(pt), pt) + rev))
prod_tri = 0.5 * (Qs(pt) - Qs(pw)) * t
cons_tri = 0.5 * (Qd(pw) - Qd(pt)) * t
print("     两块拆解：生产扭曲 %.0f + 消费扭曲 %.0f = %.0f" % (prod_tri, cons_tri, prod_tri + cons_tri))
print("  -> 结论：自贸总账 +200；关税把总账拉回 950（少 50），赢家是生产者+政府、输家是消费者。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：出口国（世界价 40 > 封闭价 30）的两级账 ===")
px = 40.0
print("  封闭：CS=400  PS=400  TS=800")
print("  自由贸易（世界价 %.0f）：Qd=%.0f Qs=%.0f -> 出口=%.0f" % (px, Qd(px), Qs(px), Qs(px) - Qd(px)))
print("     CS=%.0f  PS=%.0f  TS=%.0f（比封闭 %+.0f）" %
      (cs_of(Qd(px), px), ps_of(Qs(px), px), cs_of(Qd(px), px) + ps_of(Qs(px), px),
       cs_of(Qd(px), px) + ps_of(Qs(px), px) - 800))
print("  -> 结论：出口国的赢家输家恰好对调（生产者大赢、消费者小输），总账同样 +200。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：关税扫描（t = 0 到 10） ===")
print("   t  | 国内价 | 进口量 | 关税收入 |  DWL")
for tt in [0.0, 2.5, 5.0, 7.5, 10.0]:
    p = pw + tt
    imp = Qd(p) - Qs(p)
    rev = tt * imp
    dwtot = 1000 - (cs_of(Qd(p), p) + ps_of(Qs(p), p) + rev)
    print("  %4.1f|  %5.1f |  %4.0f  |   %4.0f   |  %5.1f" % (tt, p, imp, rev, dwtot))
print("  关税收入峰在 t=5（100）；DWL 序列 0 / 12.5 / 50 / 112.5 / 200 = 2t^2")
print("  平方律再验证：t=2.5->5，DWL x4；t=5->10，DWL x4")
print("  -> 结论：关税就是'从量税'——拉弗山与平方律原样复现。")

# ---------------------------------------------------------------------
# 图 1：进口国全景
fig, ax = plt.subplots(figsize=(7.2, 4.8), dpi=120)
qq = [i / 2 for i in range(0, 141)]           # 0 .. 70
dem = [50 - q / 2 for q in qq]
sup = [10 + q / 2 for q in qq]
ax.plot(qq, dem, color="#c0392b", lw=2, label="国内需求")
ax.plot(qq, sup, color="#2471a3", lw=2, label="国内供给")
ax.plot([0, 70], [20, 20], color="#7f8c8d", lw=1.8, ls="--")
ax.annotate("世界价格 20", xy=(6, 20), xytext=(6, 17.6), fontsize=10, color="#7f8c8d")
ax.plot([0, 70], [25, 25], color="#e67e22", lw=1.8, ls=":")
ax.annotate("关税后价格 25", xy=(6, 25), xytext=(6, 26.2), fontsize=10, color="#e67e22")
ax.plot([40], [30], "o", color="#7f8c8d", ms=8)
ax.annotate("封闭均衡 (40, 30)", xy=(40, 30), xytext=(30, 40), fontsize=9.5, color="#7f8c8d", arrowprops=dict(arrowstyle="-", color="#7f8c8d", lw=0.8))
ax.annotate("", xy=(60, 20), xytext=(20, 20), arrowprops=dict(arrowstyle="<->", color="#2c3e50", lw=1.6))
ax.annotate("进口 40", xy=(36, 21.2), fontsize=10.5, color="#2c3e50")
ax.annotate("", xy=(50, 25), xytext=(30, 25), arrowprops=dict(arrowstyle="<->", color="#e67e22", lw=1.6))
ax.annotate("关税后进口 20", xy=(31, 26.2), fontsize=10, color="#e67e22")
ax.set_xlabel("数量 Q")
ax.set_ylabel("价格 P")
ax.set_title("进口国：世界价格低于国内价，敞开买")
ax.set_xlim(0, 70)
ax.set_ylim(0, 55)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec08_fig1_importer.svg"))
fig.savefig(os.path.join(FIGDIR, "lec08_fig1_importer.png"))

# ---------------------------------------------------------------------
# 图 2：出口国全景
fig2, ax2 = plt.subplots(figsize=(7.2, 4.8), dpi=120)
ax2.plot(qq, dem, color="#c0392b", lw=2, label="国内需求")
ax2.plot(qq, sup, color="#2471a3", lw=2, label="国内供给")
ax2.plot([0, 70], [40, 40], color="#7f8c8d", lw=1.8, ls="--")
ax2.annotate("世界价格 40", xy=(6, 40), xytext=(6, 37.6), fontsize=10, color="#7f8c8d")
ax2.plot([40], [30], "o", color="#7f8c8d", ms=8)
ax2.annotate("封闭均衡 (40, 30)", xy=(40, 30), xytext=(10, 34), fontsize=9.5, color="#7f8c8d", arrowprops=dict(arrowstyle="-", color="#7f8c8d", lw=0.8))
ax2.annotate("", xy=(60, 40), xytext=(20, 40), arrowprops=dict(arrowstyle="<->", color="#2c3e50", lw=1.6))
ax2.annotate("出口 40", xy=(36, 41.2), fontsize=10.5, color="#2c3e50")
ax2.set_xlabel("数量 Q")
ax2.set_ylabel("价格 P")
ax2.set_title("出口国：世界价格高于国内价，卖到外面")
ax2.set_xlim(0, 70)
ax2.set_ylim(0, 55)
ax2.legend(loc="upper right", fontsize=9)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec08_fig2_exporter.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec08_fig2_exporter.png"))

# ---------------------------------------------------------------------
# 图 3：关税的四区账
fig3, ax3 = plt.subplots(figsize=(7.6, 5.0), dpi=120)
ax3.plot(qq, dem, color="#c0392b", lw=2, label="国内需求")
ax3.plot(qq, sup, color="#2471a3", lw=2, label="国内供给")
ax3.plot([0, 70], [20, 20], color="#7f8c8d", lw=1.8, ls="--", label="世界价格 20")
ax3.plot([0, 70], [25, 25], color="#e67e22", lw=1.8, ls=":", label="关税后价格 25")
# CS：需求下 25 上，Q 0..50
q50 = [i / 2 for i in range(0, 101)]
ax3.fill_between(q50, [50 - q / 2 for q in q50], 25, color="#aed6f1", alpha=0.5)
# PS：25 下、供给上，Q 0..30
q30 = [i / 2 for i in range(0, 61)]
ax3.fill_between(q30, 25, [10 + q / 2 for q in q30], color="#f5cba7", alpha=0.65)
# 收入矩形 30..50, 20..25
ax3.fill([30, 50, 50, 30], [20, 20, 25, 25], color="#d5f5e3", alpha=0.95)
# 生产扭曲三角 (20,20)-(30,20)-(30,25)
ax3.fill([20, 30, 30], [20, 20, 25], color="#95a5a6", alpha=0.85)
# 消费扭曲三角 (50,25)-(50,20)-(60,20)
ax3.fill([50, 50, 60], [25, 20, 20], color="#95a5a6", alpha=0.85)
ax3.plot([40], [30], "o", color="#7f8c8d", ms=7)
ax3.annotate("CS=625", xy=(12, 33), fontsize=10, color="#1a5276")
ax3.annotate("PS=225", xy=(8, 15), fontsize=10, color="#935116")
ax3.annotate("关税收入\n100", xy=(33.5, 22.2), fontsize=9.5, color="#1e8449")
ax3.annotate("生产扭曲\n25", xy=(20.5, 22.4), fontsize=9, color="#2c3e50")
ax3.annotate("消费扭曲\n25", xy=(51, 22.4), fontsize=9, color="#2c3e50")
ax3.annotate("进口 20", xy=(37, 27.6), fontsize=10)
ax3.set_xlabel("数量 Q")
ax3.set_ylabel("价格 P")
ax3.set_title("关税的四区账：消费者出血、生产者与政府进账、两块蒸发")
ax3.set_xlim(0, 70)
ax3.set_ylim(0, 55)
ax3.legend(loc="upper right", fontsize=8.5)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec08_fig3_tariff_zones.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec08_fig3_tariff_zones.png"))

print()
print("[OK] figures/lec08_fig1_importer、lec08_fig2_exporter、lec08_fig3_tariff_zones 已生成。")