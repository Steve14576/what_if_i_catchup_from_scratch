# =====================================================================
# lec02-01 比较优势与贸易收益（第 02 讲 §3 / §5 / §6）
# 规模纪律：总耗时 < 5 秒（纯算术 + 两张小图）。
# 方法：
#   实验 1：机会成本与比较优势判定。预期：拿铁比较优势在小强、可颂在小明；
#           绝对优势两项都在小强（用来演示"绝对优势 ≠ 比较优势"）。
#   实验 2：专业化与贸易的收益。预期：贸易后双方净赚（小强 2 个可颂、
#           小明 1 杯拿铁）；双方消费包的产能占用 = 112.5% > 100%
#           （即"消费点走出自家 PPF"）。
#   实验 3：贸易价格扫描。预期：双赢区间 1 < p < 2。
#   生成 figures/lec02_fig1_ppf_trade.svg/.png 与
#        figures/lec02_fig2_price_range.svg/.png。
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

# 产能（每人每天，全干一样时的产量）
# 小强：拿铁 32 杯 / 可颂 16 个；小明：拿铁 8 杯 / 可颂 8 个
QL, QC = 32, 16
ML, MC = 8, 8

# ---------------------------------------------------------------------
print("=== 实验 1：机会成本与比较优势判定 ===")
oc_strong_1c = QL / QC          # 小强做 1 个可颂，放弃几杯拿铁
oc_strong_1l = QC / QL          # 小强做 1 杯拿铁，放弃几个可颂
oc_m_1c = ML / MC
oc_m_1l = MC / ML
print("  小强：1 个可颂 = %d/%d = %.3f 杯拿铁；1 杯拿铁 = %d/%d = %.3f 个可颂" %
      (QL, QC, oc_strong_1c, QC, QL, oc_strong_1l))
print("  小明：1 个可颂 = %d/%d = %.3f 杯拿铁；1 杯拿铁 = %d/%d = %.3f 个可颂" %
      (ML, MC, oc_m_1c, MC, ML, oc_m_1l))
who_l = "小强" if oc_strong_1l < oc_m_1l else "小明"
who_c = "小强" if oc_strong_1c < oc_m_1c else "小明"
print("  拿铁机会成本对比：小强 %.3f  vs  小明 %.3f  -> 比较优势在 %s" % (oc_strong_1l, oc_m_1l, who_l))
print("  可颂机会成本对比：小强 %.3f  vs  小明 %.3f  -> 比较优势在 %s" % (oc_strong_1c, oc_m_1c, who_c))
print("  绝对优势对比：拿铁 %d vs %d；可颂 %d vs %d -> 两项绝对优势都在小强" % (QL, ML, QC, MC))
print("  -> 结论：绝对优势全被小强包揽，比较优势却一人一边——贸易的基础是后者。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：专业化与贸易的收益 ===")
print("  自给自足（各花一半时间）：小强 16 杯 + 8 个；小明 4 杯 + 4 个；合计 20 杯 + 12 个")
print("  专业化：小强全做拿铁 32 杯；小明全做可颂 8 个；合计 32 杯 + 8 个")

trade_c = 5.0     # 小明交给小强的可颂个数
trade_l = 6.0     # 小强交给小明的拿铁杯数
p_trade = trade_l / trade_c
final_S_l, final_S_c = QL - trade_l, trade_c            # 小强最终 26 杯 + 5 个
final_M_l, final_M_c = trade_l, MC - trade_c            # 小明最终 6 杯 + 3 个
print("  贸易：小明交给小强 %.0f 个可颂，换回 %.0f 杯拿铁（价格 p = %.0f/%.0f = %.1f 杯/个）" %
      (trade_c, trade_l, trade_l, trade_c, p_trade))
print("  最终消费：小强 %.0f 杯 + %.0f 个；小明 %.0f 杯 + %.0f 个" %
      (final_S_l, final_S_c, final_M_l, final_M_c))

gain_S = trade_c - trade_l * oc_strong_1l      # 小强：收到 5 个，自制代价 6*0.5=3 个 -> 净赚 2 个（以可颂计）
gain_M = trade_l - trade_c * oc_m_1c           # 小明：收到 6 杯，自制代价 5*1=5 杯 -> 净赚 1 杯（以拿铁计）
print("  折算检验 小强：交出 %.0f 杯拿铁 = 自制 %.1f 个可颂的代价；换回 %.0f 个 -> 净赚 %.1f 个可颂" %
      (trade_l, trade_l * oc_strong_1l, trade_c, gain_S))
print("  折算检验 小明：交出 %.0f 个可颂 = 自制 %.1f 杯拿铁的代价；换回 %.0f 杯 -> 净赚 %.1f 杯拿铁" %
      (trade_c, trade_c * oc_m_1c, trade_l, gain_M))

use_S = final_S_l / QL + final_S_c / QC        # 小强消费包的产能占用
use_M = final_M_l / ML + final_M_c / MC        # 小明消费包的产能占用
print("  产能占用检验 小强：%.0f/32 + %.0f/16 = %.1f%% > 100%% -> 自力做不到" %
      (final_S_l, final_S_c, use_S * 100))
print("  产能占用检验 小明：%.0f/8 + %.0f/8 = %.1f%% > 100%% -> 自力做不到" %
      (final_M_l, final_M_c, use_M * 100))
print("  -> 结论：贸易让双方的消费点都走出自家 PPF；且每笔交换对双方都比自制划算。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：贸易价格的双方意愿扫描 ===")
print("  单位：1 个可颂的价格 p（杯拿铁/个）")
print("  小明赚头（拿铁计/个）= p - %.1f；小强赚头（拿铁计/个）= %.1f - p" % (oc_m_1c, oc_strong_1c))
print("    p    | 小明赚头 | 小强赚头 | 成交")
for p in [0.5, 0.75, 1.0, 1.2, 1.5, 1.75, 2.0, 2.5]:
    gM = p - oc_m_1c
    gS = oc_strong_1c - p
    if gM > 0 and gS > 0:
        state = "[OK] 双方都干"
    elif gM < 0 and gS > 0:
        state = "小明不干"
    elif gM > 0 and gS < 0:
        state = "小强不干"
    else:
        state = "打平（勉强）"
    print("   %.2f  |  %+.2f   |  %+.2f   | %s" % (p, gM, gS, state))
print("  -> 结论：双赢区间 %.1f < p < %.1f；区间内 p 越高，好处越偏向小明。" % (oc_m_1c, oc_strong_1c))

# ---------------------------------------------------------------------
# 图 1：两人的 PPF 与"走出 PPF"的消费点
fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.4), dpi=120)

ax = axes[0]
ax.plot([QL, 0], [0, QC], color="#2c3e50", lw=2, label="小强的 PPF")
ax.plot([QL / 2], [QC / 2], "s", color="#7f8c8d", ms=8)
ax.annotate("自给自足（16, 8）", xy=(16, 8), xytext=(17.5, 10.5), fontsize=10, color="#7f8c8d")
ax.plot([final_S_l], [final_S_c], "*", color="#c0392b", ms=16)
ax.annotate("贸易后（26, 5）\n在自家 PPF 之外", xy=(26, 5), xytext=(25.6, 7.0), fontsize=10, color="#c0392b")
ax.set_xlabel("拿铁（杯/天）")
ax.set_ylabel("可颂（个/天）")
ax.set_title("小强：两项绝对优势")
ax.set_xlim(0, 36)
ax.set_ylim(0, 18)
ax.legend(loc="upper right", fontsize=9)

ax = axes[1]
ax.plot([ML, 0], [0, MC], color="#2c3e50", lw=2, label="小明的 PPF")
ax.plot([ML / 2], [MC / 2], "s", color="#7f8c8d", ms=8)
ax.annotate("自给自足（4, 4）", xy=(4, 4), xytext=(2.2, 4.9), fontsize=10, color="#7f8c8d")
ax.plot([final_M_l], [final_M_c], "*", color="#c0392b", ms=16)
ax.annotate("贸易后（6, 3）\n在自家 PPF 之外", xy=(6, 3), xytext=(5.2, 5.1), fontsize=10, color="#c0392b")
ax.set_xlabel("拿铁（杯/天）")
ax.set_ylabel("可颂（个/天）")
ax.set_title("小明：慢，但有可颂的比较优势")
ax.set_xlim(0, 9)
ax.set_ylim(0, 9)
ax.legend(loc="upper right", fontsize=9)

fig.suptitle("贸易收益：消费点走出各自的 PPF", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(os.path.join(FIGDIR, "lec02_fig1_ppf_trade.svg"))
fig.savefig(os.path.join(FIGDIR, "lec02_fig1_ppf_trade.png"))

# ---------------------------------------------------------------------
# 图 2：贸易价格的"双赢区"
fig2, ax2 = plt.subplots(figsize=(8.0, 2.6), dpi=120)
ax2.axvspan(oc_m_1c, oc_strong_1c, color="#27ae60", alpha=0.16)
ax2.axvline(oc_m_1c, color="#7f8c8d", ls="--", lw=1.2)
ax2.axvline(oc_strong_1c, color="#7f8c8d", ls="--", lw=1.2)
ax2.text(0.72, 0.5, "小明不卖\n（低于他的成本）", ha="center", va="center", fontsize=10, color="#7f8c8d")
ax2.text(1.5, 0.5, "双赢区\n1 < p < 2", ha="center", va="center", fontsize=11, color="#1e8449")
ax2.text(2.28, 0.5, "小强不买\n（高于他的成本）", ha="center", va="center", fontsize=10, color="#7f8c8d")
ax2.set_xlim(0.5, 2.5)
ax2.set_ylim(0, 1)
ax2.set_xlabel("价格 p（杯拿铁 / 个可颂）")
ax2.set_yticks([])
ax2.spines["left"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["top"].set_visible(False)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec02_fig2_price_range.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec02_fig2_price_range.png"))

print()
print("[OK] figures/lec02_fig1_ppf_trade.svg/.png 与 lec02_fig2_price_range.svg/.png 已生成。")