# =====================================================================
# lec18-01 三大前沿：信息、政治与行为（第 18 讲 §1-§3）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   实验 1：柠檬市场迭代崩溃：质量 q = 1..10 各一台（卖方保留价 = q），
#           买家支付意愿 WTP = 市场平均质量。市场上剩 q <= WTP 的车；
#           迭代：10 台 -> 5 -> 3 -> 2 -> 1（只剩下最差的 q=1）。
#   实验 2：康多塞悖论：三选民（A>B>C；B>C>A；C>A>B）两两对决：
#           A 胜 B、B 胜 C、C 胜 A——多数循环。
#   实验 3：中位投票人：101 人理想点分布（40@30、11@45、50@70）：
#           中位 = 45；A=30、B=70 时 A 得 51 票；B 移到 50 反夺 61 票；
#           A 挤到 45 后回到 51-50 拉锯——"向中间挤"的演示。
#   实验 4：行为数值：损失厌恶 λ=2.25（丢 100 的痛约需得 506 抵消）；
#           锚定公开数据对照表（轮盘 10/65 -> 估计 25%/45%）。
#   生成 figures/lec18_fig1_lemons.svg/.png、
#        figures/lec18_fig2_median_voter.svg/.png、
#        figures/lec18_fig3_value_function.svg/.png。
# 输出用 GBK 安全字符（无禁区符号，用 [OK] / ^2 / ->）。
# =====================================================================
import os
import math
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
print("=== 实验 1：柠檬市场的迭代崩溃（质量 1..10，WTP = 平均质量） ===")
q = list(range(1, 11))
print("  轮次 | 在市场里的车 | 平均质量 | 买家 WTP | 下一轮剩什么")
rounds_log = []
t = 1
while True:
    avg = sum(q) / len(q)
    keep = [x for x in q if x <= avg]
    print("    %d  | %s |  %5.2f   |  %5.2f  | %s" % (t, q, avg, avg, keep))
    rounds_log.append((t, len(q), avg))
    if len(keep) == len(q):
        break
    q = keep
    t += 1
print("  稳定态：只剩 1 台，质量 = 1——最差的那台。")
print("  -> 结论：买家按'平均质量'出价，高质量车陆续退出——市场被'柠檬'占领。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：康多塞悖论（三选民、三选项） ===")
votes = {
    "X vs Y": ["甲: X>Y", "乙: Y>X", "丙: X>Y"],
    "Y vs Z": ["甲: Y>Z", "乙: Y>Z", "丙: Z>Y"],
    "X vs Z": ["甲: X>Z", "乙: Z>X", "丙: Z>X"],
}
winners = {}
for pair, vs in votes.items():
    x, y = pair.split(" vs ")
    tally = {x: 0, y: 0}
    detail = []
    for v in vs:
        pref = v.split(": ")[1]
        w = pref.split(">")[0]
        tally[w] += 1
        detail.append(v)
    win = max(tally, key=tally.get)
    winners[pair] = win
    print("  %s：%s -> %s 胜（%d:%d）" % (pair, "; ".join(detail), win, tally[win], 3 - tally[win]))
print("  传递性检查：X 胜 Y、Y 胜 Z、而 Z 胜 X——循环！")
print("  -> 结论：多数偏好在三选项下可能循环——'多数人的意志'未必存在。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：中位投票人（101 人：40@30、11@45、50@70） ===")
peaks = [30] * 40 + [45] * 11 + [70] * 50
med = sorted(peaks)[50]  # 第 51 个（0 索引 50）
print("  中位选民位置 = %d" % med)
def tally(a, b):
    a_votes = sum(1 for p in peaks if abs(p - a) < abs(p - b))
    b_votes = sum(1 for p in peaks if abs(p - b) < abs(p - a))
    tie = len(peaks) - a_votes - b_votes
    return a_votes + tie, b_votes  # 平局按惯例记给 A
for a, b, tag in [(30, 70, "R1 原始站位"), (30, 50, "R2 B 向中间移动"), (45, 50, "R3 A 也挤到中间")]:
    av, bv = tally(a, b)
    print("  %s：A@%d 得 %d 票，B@%d 得 %d 票 -> %s" % (tag, a, av, b, bv, "A 胜" if av > bv else "B 胜"))
print("  -> 结论：谁背离中位选民谁丢票——双方都被逼向中间（中位数附近）。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：行为经济学的两个数值 ===")
lam = 2.25
loss_v = lam * math.sqrt(100)
x_needed = loss_v ** 2
print("  损失厌恶（λ=2.25）：丢 100 的心理损失 = 2.25*sqrt(100) = %.1f" % loss_v)
print("  等价快乐：需得 %.0f 元（sqrt(%.0f) = %.1f）——'丢 100 的痛约等于得 506 的乐'" %
      (x_needed, x_needed, math.sqrt(x_needed)))
print("  锚定（公开实验数据，卡尼曼与特沃斯基的轮盘实验）：")
print("    看到转盘停在 10 的人：中位估计 25%；看到停在 65 的人：中位估计 45%")
print("    同一个问题（非洲国家占联合国席位的比例），答案被无关数字拖动")
print("  -> 结论：偏好会被'参照与损失'系统性塑造——偏差可预测，不是噪声。")

# ---------------------------------------------------------------------
# 图 1：柠檬崩溃
fig, ax = plt.subplots(figsize=(7.0, 4.4), dpi=120)
rs = [r[0] for r in rounds_log]
counts = [r[1] for r in rounds_log]
avgs = [r[2] for r in rounds_log]
ax.plot(rs, counts, "o-", color="#c0392b", lw=2.2, ms=7, label="市场上剩多少台车")
ax.plot(rs, avgs, "s--", color="#2471a3", lw=2.2, ms=7, label="平均质量（= 买家出价）")
for r, c, a in zip(rs, counts, avgs):
    ax.annotate("%d 台" % c, xy=(r, c), xytext=(r, c + 0.7), fontsize=9, color="#c0392b")
    if a >= 1.5:
        ax.annotate("%.1f" % a, xy=(r, a), xytext=(r, a - 1.3), fontsize=9, color="#2471a3")
    else:
        ax.annotate("%.1f" % a, xy=(r, a), xytext=(r - 0.28, a + 1.35), fontsize=9, color="#2471a3")
ax.set_xlabel("迭代轮次")
ax.set_ylabel("数量 / 质量")
ax.set_title("柠檬市场：按'平均质量'出价，好车一台台退出")
ax.set_xticks(rs)
ax.set_ylim(0, 12)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec18_fig1_lemons.svg"))
fig.savefig(os.path.join(FIGDIR, "lec18_fig1_lemons.png"))

# ---------------------------------------------------------------------
# 图 2：中位投票人
fig2, ax2 = plt.subplots(figsize=(7.4, 4.4), dpi=120)
for grp, pos, col, dy in [(40, 30, "#c0392b", 4), (11, 45, "#27ae60", 7), (50, 70, "#2471a3", 4)]:
    ax2.plot([pos], [grp], "o", ms=14, color=col)
    ax2.annotate("%d 人 @ %d" % (grp, pos), xy=(pos, grp), xytext=(pos - 1, grp + dy),
                 ha="center", fontsize=10, color=col)
ax2.axvline(45, color="#7f8c8d", lw=1.8, ls="--")
ax2.annotate("中位选民 = 45", xy=(45, 62), xytext=(46.5, 60), fontsize=10, color="#566573")
ax2.annotate("", xy=(44.2, 20), xytext=(31, 20), arrowprops=dict(arrowstyle="->", color="#e67e22", lw=1.8))
ax2.annotate("", xy=(44.2, 14), xytext=(69, 14), arrowprops=dict(arrowstyle="->", color="#e67e22", lw=1.8))
ax2.annotate("两个候选人都被迫挤向中间", xy=(37, 8), fontsize=10.5, color="#b9770e")
ax2.set_xlabel("政策位置（左----右）")
ax2.set_ylabel("选民人数")
ax2.set_title("中位投票人：谁背离中位，谁丢票")
ax2.set_xlim(15, 85)
ax2.set_ylim(0, 66)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec18_fig2_median_voter.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec18_fig2_median_voter.png"))

# ---------------------------------------------------------------------
# 图 3：前景理论价值函数
fig3, ax3 = plt.subplots(figsize=(7.0, 4.6), dpi=120)
xs_pos = [i / 2 for i in range(0, 201)]      # 0 .. 100
xs_neg = [-i / 2 for i in range(1, 201)]     # -0.5 .. -100
ax3.plot(xs_pos, [math.sqrt(x) for x in xs_pos], color="#1e8449", lw=2.4)
ax3.plot(xs_neg, [-lam * math.sqrt(-x) for x in xs_neg], color="#c0392b", lw=2.4)
ax3.axhline(0, color="#7f8c8d", lw=1)
ax3.axvline(0, color="#7f8c8d", lw=1)
ax3.plot([0], [0], "ko", ms=7)
ax3.annotate("参照点", xy=(0, 0), xytext=(3, -4.5), fontsize=10)
ax3.annotate("收益段：越赚越平淡", xy=(40, 9.5), fontsize=10, color="#1e8449")
ax3.annotate("损失段：更陡（λ≈2.25）\n丢 100 的痛 ≈ 得 506 的乐", xy=(-95, -12), xytext=(-88, -4.6),
             fontsize=9.5, color="#922b21")
ax3.set_xlabel("损益（相对参照点）")
ax3.set_ylabel("心理价值")
ax3.set_title("前景理论价值函数：损失和收益天生不对称")
ax3.set_xlim(-105, 105)
ax3.set_ylim(-25, 12)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec18_fig3_value_function.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec18_fig3_value_function.png"))

print()
print("[OK] figures/lec18_fig1_lemons、lec18_fig2_median_voter、lec18_fig3_value_function 已生成。")