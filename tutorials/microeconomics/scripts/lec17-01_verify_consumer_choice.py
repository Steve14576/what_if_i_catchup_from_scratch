# =====================================================================
# lec17-01 消费者选择：预算、偏好与两效应分解（第 17 讲 §1-§5）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   主场景：奶茶 x（15 元/杯）、电影 y（60 元/张）、预算 M = 360；
#   效用 U = sqrt(x*y)（Cobb-Douglas 对称版）。
#   实验 1：预算线组合表（全奶茶 24 / 全电影 6；斜率 -1/4）。
#   实验 2：最优验证：解析 x* = M/(2*Px) = 12、y* = M/(2*Py) = 3；
#           预算线扫描 U^2 = 6x - 0.25x^2 在 x = 12 取峰（36 -> U = 6）；
#           MRS = y/x = 1/4 = 15/60 相切成立。
#   实验 3：价格分解（奶茶 15 -> 10）：新最优 (18, 3)；
#           补偿点（保持 U = 6、新价格）：x = sqrt(216) ~ 14.70, y ~ 2.45；
#           替代效应 ~ +2.70、收入效应 ~ +3.30（合计 +6）。
#   实验 4：劳动供给（U = sqrt(c*l)、16 小时）：最优工作时长恒为 8 小时
#           （Cobb-Douglas 下两效应精确抵消——"工资涨了也没多干"）。
#   生成 figures/lec17_fig1_budget_ic.svg/.png、
#        figures/lec17_fig2_decomposition.svg/.png、
#        figures/lec17_fig3_labor_backward.svg/.png。
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

Px0, Py, M = 15.0, 60.0, 360.0

# ---------------------------------------------------------------------
print("=== 实验 1：预算线（奶茶 15 元、电影 60 元、预算 360 元） ===")
print("  全买奶茶：360/15 = %d 杯；全买电影：360/60 = %d 张" % (M / Px0, M / Py))
print("  斜率 = -Px/Py = -15/60 = -0.25（多要 1 杯奶茶，须放弃 1/4 张电影）")
print("  几个组合：")
for x in [0, 6, 12, 18, 24]:
    y = (M - Px0 * x) / Py
    print("    奶茶 %2d 杯 -> 电影 %.1f 张" % (x, y))
print("  -> 结论：预算线 = 所有花光 360 元的组合；斜率是价格比。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：最优选择验证（U = sqrt(x*y)） ===")
x_star = M / (2 * Px0)
y_star = M / (2 * Py)
print("  解析最优：x* = M/(2Px) = 360/30 = %.0f；y* = M/(2Py) = 360/120 = %.0f" % (x_star, y_star))
print("  MRS = y/x = %.2f；价格比 Px/Py = %.2f -> 相切成立" % (y_star / x_star, Px0 / Py))
print("  预算线扫描 U^2 = 6x - 0.25x^2：")
for x in [8, 10, 11, 12, 13, 14, 16]:
    y = (M - Px0 * x) / Py
    u2 = x * y
    print("    x=%2d（奶茶）：y=%5.2f，U^2=%6.2f，U=%.3f" % (x, y, u2, math.sqrt(u2)))
print("  -> 结论：U 在 x=12 处取峰（U=6）——相切点就是最高可达到的效用。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：价格分解（奶茶 15 -> 10 元） ===")
Px1 = 10.0
x1 = M / (2 * Px1)
y1 = M / (2 * Py)
print("  新最优：x** = %.0f，y** = %.0f（奶茶 12 -> 18，+6）" % (x1, y1))
U0 = math.sqrt(x_star * y_star)
x_c = math.sqrt(216.0)
y_c = 36.0 / x_c
print("  补偿点（保持 U=%.0f、按新价格）：x = %.2f，y = %.2f" % (U0, x_c, y_c))
sub = x_c - x_star
inc = x1 - x_c
print("  替代效应 = %.2f - 12 = %+.2f；收入效应 = 18 - %.2f = %+.2f" % (x_c, sub, x_c, inc))
print("  合计 = %+.2f + %+.2f = %+.2f（核对：18 - 12 = 6）" % (sub, inc, sub + inc))
print("  -> 结论：降价带来的 +6 杯里，约 +2.7 是'相对变便宜'的替代，+3.3 是'变相变富'的收入。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：劳动供给的两效应（U = sqrt(c*l)，可支配 16 小时） ===")
print("  设定：消费 c = w(16-l)；U = sqrt(c*l)；最优条件 c/l = w")
for w in [10.0, 20.0, 30.0]:
    l = 8.0
    c = w * (16 - l)
    print("  工资 %2.0f/时：最优闲暇 = 工作 %.0f 小时，消费 = %.0f（两效应恰好抵消）" % (w, l, c))
print("  -> 结论：Cobb-Douglas 偏好下工资怎么涨，工作时长都停在 8 小时——")
print("     替代（闲暇变贵）与收入（变富想歇）各拉一半，完全打平。")

# ---------------------------------------------------------------------
# 图 1：预算线与无差异曲线
fig, ax = plt.subplots(figsize=(7.4, 4.8), dpi=120)
xs = [i / 10 for i in range(1, 241)]           # 0.1 .. 24
budget = [6 - 0.25 * x for x in xs]
ax.plot(xs, budget, color="#2c3e50", lw=2.2, label="预算线：15x + 60y = 360")
for c, col in [(16, "#aed6f1"), (36, "#5dade2"), (64, "#2874a6")]:
    ys = [c / x for x in xs if c / x <= 8]
    ax.plot([x for x in xs if c / x <= 8], ys, color=col, lw=2)
ax.plot([12], [3], "ko", ms=9)
ax.annotate("最优 (12, 3)：相切\nMRS = 1/4 = 价格比", xy=(12, 3), xytext=(13.2, 1.2), fontsize=10,
            arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.9))
ax.annotate("同一条线上：\n一样满足", xy=(8, 2), xytext=(3.2, 4.4), fontsize=9.5,
            arrowprops=dict(arrowstyle="-", color="#7f8c8d", lw=0.8))
ax.annotate("够不着", xy=(16, 4), xytext=(17.5, 5.2), fontsize=9.5, color="#922b21")
ax.set_xlabel("奶茶（杯）")
ax.set_ylabel("电影票（张）")
ax.set_title("预算线与无差异曲线：最优在相切处")
ax.set_xlim(0, 24)
ax.set_ylim(0, 6.5)
ax.legend(loc="upper right", fontsize=8.5)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec17_fig1_budget_ic.svg"))
fig.savefig(os.path.join(FIGDIR, "lec17_fig1_budget_ic.png"))

# ---------------------------------------------------------------------
# 图 2：价格分解
fig2, ax2 = plt.subplots(figsize=(7.6, 5.0), dpi=120)
xs2 = [i / 10 for i in range(1, 241)]
ax2.plot(xs2, [6 - 0.25 * x for x in xs2], color="#2c3e50", lw=2, label="原预算线（15 元）")
ax2.plot(xs2, [6 - x / 6 for x in xs2], color="#27ae60", lw=2, label="新预算线（10 元）")
ax2.plot(xs2, [4.9 - x / 6 for x in xs2], color="#b9770e", lw=1.6, ls="--",
         label="补偿预算线（保持原满足）")
for c, col, lw in [(36, "#5dade2", 2), (54, "#e59866", 2)]:
    ys = [c / x for x in xs2 if c / x <= 7]
    ax2.plot([x for x in xs2 if c / x <= 7], ys, color=col, lw=lw)
ax2.plot([12], [3], "ko", ms=9)
ax2.plot([14.70], [2.45], "o", color="#b9770e", ms=9)
ax2.plot([18], [3], "o", color="#1e8449", ms=9)
ax2.annotate("原最优 (12, 3)", xy=(12, 3), xytext=(8.2, 1.0), fontsize=9.5,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
ax2.annotate("补偿点 (14.7, 2.45)", xy=(14.70, 2.45), xytext=(2.6, 1.9), fontsize=9.5, color="#b9770e",
             arrowprops=dict(arrowstyle="-", color="#b9770e", lw=0.8))
ax2.annotate("新最优 (18, 3)", xy=(18, 3), xytext=(17.0, 4.6), fontsize=9.5, color="#1e8449",
             arrowprops=dict(arrowstyle="-", color="#1e8449", lw=0.8))
ax2.annotate("", xy=(14.70, 0.6), xytext=(12, 0.6), arrowprops=dict(arrowstyle="<->", color="#2471a3", lw=1.6))
ax2.annotate("替代 +2.7", xy=(12.9, 0.75), fontsize=9.5, color="#2471a3")
ax2.annotate("", xy=(18, 0.6), xytext=(14.70, 0.6), arrowprops=dict(arrowstyle="<->", color="#c0392b", lw=1.6))
ax2.annotate("收入 +3.3", xy=(15.4, 0.75), fontsize=9.5, color="#c0392b")
ax2.set_xlabel("奶茶（杯）")
ax2.set_ylabel("电影票（张）")
ax2.set_title("奶茶降价 15 -> 10：+6 杯的分解账")
ax2.set_xlim(0, 24)
ax2.set_ylim(0, 6.5)
ax2.legend(loc="upper right", fontsize=8.5)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec17_fig2_decomposition.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec17_fig2_decomposition.png"))

# ---------------------------------------------------------------------
# 图 3：后弯的劳动供给（示意）
fig3, ax3 = plt.subplots(figsize=(7.0, 4.6), dpi=120)
w_pts = [4, 6, 8, 10, 12, 14, 16, 18, 20]
L_pts = [4.0, 5.5, 6.8, 7.6, 8.0, 7.9, 7.5, 7.0, 6.4]
ax3.plot(L_pts, w_pts, "o-", color="#2471a3", lw=2.4, ms=5)
ax3.annotate("替代主导：涨薪 -> 多干", xy=(7.2, 9), xytext=(3.0, 13.5), fontsize=10, color="#1e8449",
             arrowprops=dict(arrowstyle="->", color="#1e8449", lw=1))
ax3.annotate("收入主导：涨薪 -> 反而少干（后弯）", xy=(7.6, 16.5), xytext=(3.2, 18.5), fontsize=10, color="#922b21",
             arrowprops=dict(arrowstyle="->", color="#922b21", lw=1))
ax3.set_xlabel("劳动供给（小时/天）")
ax3.set_ylabel("工资（元/时）")
ax3.set_title("个人劳动供给曲线可以'后弯'（示意）")
ax3.set_xlim(2, 10)
ax3.set_ylim(0, 23)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec17_fig3_labor_backward.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec17_fig3_labor_backward.png"))

print()
print("[OK] figures/lec17_fig1_budget_ic、lec17_fig2_decomposition、lec17_fig3_labor_backward 已生成。")