# =====================================================================
# lec01-02 PPF 与机会成本递增（第 01 讲 §6.3）
# 规模纪律：总耗时 < 5 秒（纯算术 + 一张小图）。
# 方法：拿铁/可颂日产能组合表 -> 逐段机会成本。
#       预期：机会成本单调递增（0.667 -> 0.909 -> 1.25 -> 1.667）；
#       与"线性近似"（恒定机会成本 1.0）对照。
#       并生成 figures/lec01_fig2_ppf.svg 与 .png。
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

# (拿铁杯/天, 可颂个/天)，从 A 到 E
pairs = [(200, 0), (150, 75), (100, 130), (50, 170), (0, 200)]
labels = ["A", "B", "C", "D", "E"]

print("=== 实验 3：PPF 上的机会成本递增 ===")
print("  日产能组合（拿铁, 可颂）：", pairs)
print("  从 A 到 E 逐段看：每次放弃 50 杯拿铁，换来的可颂越来越少：")
prev_oc = None
for i in range(len(pairs) - 1):
    dl = pairs[i][0] - pairs[i + 1][0]
    dc = pairs[i + 1][1] - pairs[i][1]
    oc = dl / dc
    trend = "" if prev_oc is None else ("（比上一段更贵）" if oc > prev_oc else "（比上一段更便宜）")
    print("   段 %s->%s：放弃 %d 杯，换来 %d 个；可颂的机会成本 = %d/%d = %.3f 杯/个%s" %
          (labels[i], labels[i + 1], dl, dc, dl, dc, oc, trend))
    prev_oc = oc
print("  -> 机会成本从 0.667 递增到 1.667：这就是 PPF 向原点凸出（凹）的原因。")
print("  线性近似对照：若只盯住两端 A(200,0) 与 E(0,200)，直线斜率的绝对值恒为 1.0，")
print("  每一段都被当成 1.0 杯/个——看不出'越往后越贵'这一结构。")

# ---------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 4.6), dpi=120)
xs = [p[0] for p in pairs]
ys = [p[1] for p in pairs]
ax.plot(xs, ys, "o-", color="#2c3e50", lw=2, label="有效点连成的 PPF")

ax.plot([60], [60], "x", color="#c0392b", ms=9, mew=2)
ax.annotate("无效率：资源没用满", xy=(60, 60), xytext=(72, 36), fontsize=10)
ax.plot([130], [130], "x", color="#2471a3", ms=9, mew=2)
ax.annotate("不可行：做不到", xy=(130, 130), xytext=(140, 148), fontsize=10)

offsets = [(-26, 10), (-14, 9), (-14, 9), (-14, 9), (6, 7)]
for (x, y), lb, (dx, dy) in zip(pairs, labels, offsets):
    ax.annotate(lb, xy=(x, y), xytext=(x + dx, y + dy), fontsize=10)

ax.set_xlabel("拿铁（杯/天）")
ax.set_ylabel("可颂（个/天）")
ax.set_title("生产可能性边界（PPF）：一条'取舍菜单'")
ax.set_xlim(0, 230)
ax.set_ylim(0, 230)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec01_fig2_ppf.svg"))
fig.savefig(os.path.join(FIGDIR, "lec01_fig2_ppf.png"))
print()
print("[OK] figures/lec01_fig2_ppf.svg 与 .png 已生成。")