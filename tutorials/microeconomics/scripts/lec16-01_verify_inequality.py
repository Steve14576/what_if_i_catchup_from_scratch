# =====================================================================
# lec16-01 收入不平等、工资差别与政策（第 16 讲 §1-§4）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   实验 1：洛伦兹曲线与基尼系数（五等分份额，梯形法面积）：
#           甲 7/12/17/24/40 -> 基尼约 0.312；乙 3/8/14/25/50 -> 约 0.444。
#   实验 2：超级明星算术：可复制服务（明星）vs 不可复制服务（理发师）：
#           市场总量同为 1 亿：明星第 1 名 8000 万/第 2 名 1000 万/尾部 5 万；
#           理发师 1000 人几乎均分（人均 10 万）。
#   实验 3：歧视的竞争演化：不歧视企业份额 s 按相对竞争力 r 迭代：
#           r=1.02（顾客不歧视）-> 份额上升；r=0.98（顾客也歧视）-> 份额下滑。
#   实验 4：负所得税：补 1000、退坡 50% 与 30%：各收入点的净收入与
#           隐含边际税率（0.5 与 0.3 的"退坡税"）。
#   生成 figures/lec16_fig1_lorenz.svg/.png、
#        figures/lec16_fig2_superstar.svg/.png、
#        figures/lec16_fig3_negative_tax.svg/.png。
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


def lorenz_area(shares):
    """五等分收入份额 -> 洛伦兹曲线下面积（梯形法，从 (0,0) 起）"""
    cum = 0.0
    prev = 0.0
    area = 0.0
    for s in shares:
        cum += s
        area += 0.2 * (prev + cum) / 2
        prev = cum
    return area


# ---------------------------------------------------------------------
print("=== 实验 1：洛伦兹曲线与基尼系数（五等分份额） ===")
A = [0.07, 0.12, 0.17, 0.24, 0.40]
B = [0.03, 0.08, 0.14, 0.25, 0.50]
for name, sh in [("甲国", A), ("乙国", B)]:
    area = lorenz_area(sh)
    gini = (0.5 - area) / 0.5
    cum = []
    c = 0.0
    for s in sh:
        c += s
        cum.append(round(c, 2))
    print("  %s：累计份额 %s；曲线下面积 %.3f -> 基尼 = (0.5-%.3f)/0.5 = %.3f" %
          (name, cum, area, area, gini))
print("  -> 结论：乙国曲线更弯、基尼更大（0.444 > 0.312）——份额越低层越薄，越不平等。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：超级明星算术（可复制 vs 不可复制） ===")
print("  可复制服务市场（总消费 1 亿）：")
print("    第 1 名：8000 万；第 2 名：1000 万；其余 200 名：合计 1000 万（每人 5 万）")
print("    第 1 名 / 第 2 名 = 8 倍；第 1 名 / 尾部同行 = 1600 倍")
print("  不可复制服务市场（总消费同为 1 亿）：")
print("    1000 名理发师，每人固定服务能力 -> 人均 10 万（几乎均等）")
print("  -> 结论：手艺差 10% 不打紧——'能不能被无限复制'决定差距的量级。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：歧视的竞争演化（不歧视企业份额 s 的迭代） ===")
for r, tag in [(1.02, "顾客不歧视（不歧视企业有成本优势）"),
               (0.98, "顾客也歧视（迎合歧视的反而占优）")]:
    s = 0.40
    print("  %s：" % tag)
    for t in range(1, 31):
        s = s * r / (s * r + (1 - s))
        if t % 10 == 0:
            print("    第 %2d 期：不歧视企业份额 = %.1f%%" % (t, s * 100))
print("  -> 结论：具备'顾客不歧视'的条件时，竞争才朝清洗歧视的方向走——")
print("     但这是'慢变量'；顾客本身歧视时，市场反而奖励歧视。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：负所得税的净收入与隐含税率 ===")
def net_a(x):  # 补 1000、退坡 50%
    return x + max(0.0, 1000 - 0.5 * x)
def net_b(x):  # 补 1000、退坡 30%
    return x + max(0.0, 1000 - 0.3 * x)
print("  收入 x | 无政策净收入 | 方案A(50%退坡) | 方案B(30%退坡)")
for x in [0, 500, 1000, 2000, 3000, 4000]:
    print("   %4d  |    %4d      |     %4.0f      |     %4.0f" % (x, x, net_a(x), net_b(x)))
print("  隐含边际税率（0->1000 段）：方案A 1-0.5 = 50%；方案B 1-0.7 = 30%")
print("  方案A 在收入 2000 处补贴退完；方案B 在约 3333 处退完")
print("  -> 结论：'补穷人'与'保留干活激励'之间，靠退坡速度这根旋钮取舍。")

# ---------------------------------------------------------------------
# 图 1：洛伦兹曲线
fig, ax = plt.subplots(figsize=(6.8, 5.0), dpi=120)
xs = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
cumA = [0, 0.07, 0.19, 0.36, 0.60, 1.0]
cumB = [0, 0.03, 0.11, 0.25, 0.50, 1.0]
ax.plot([0, 1], [0, 1], color="#7f8c8d", lw=1.6, ls="--", label="完全平等线（45 度）")
ax.plot(xs, cumA, "o-", color="#2471a3", lw=2.2, label="甲国（基尼 0.312）")
ax.plot(xs, cumB, "s-", color="#c0392b", lw=2.2, label="乙国（基尼 0.444）")
ax.fill_between(xs, cumA, xs, color="#d6eaf8", alpha=0.5)
ax.annotate("两条曲线与 45 度线\n之间的面积越大，\n基尼越大", xy=(0.55, 0.62), fontsize=10, color="#2c3e50")
ax.set_xlabel("人口累计百分比（从最穷到最富）")
ax.set_ylabel("收入累计百分比")
ax.set_title("洛伦兹曲线：谁更不平等，一眼看出")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend(loc="upper left", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec16_fig1_lorenz.svg"))
fig.savefig(os.path.join(FIGDIR, "lec16_fig1_lorenz.png"))

# ---------------------------------------------------------------------
# 图 2：超级明星 vs 理发师（对数刻度）
fig2, ax2 = plt.subplots(figsize=(7.0, 4.4), dpi=120)
labels = ["明星第1名", "明星第2名", "明星尾部\n（人均）", "理发师\n（人均）"]
vals = [8000, 1000, 5, 10]
colors = ["#c0392b", "#e67e22", "#f5b041", "#2471a3"]
bars = ax2.bar(labels, vals, color=colors, width=0.6)
ax2.set_yscale("log")
for b, v in zip(bars, vals):
    ax2.annotate("%g 万" % v, xy=(b.get_x() + b.get_width() / 2, v * 1.25), ha="center", fontsize=10)
ax2.set_ylabel("收入（万元，对数刻度）")
ax2.set_title("同样的手艺差距：可复制服务的差距被放大到 1600 倍")
ax2.set_ylim(1, 30000)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec16_fig2_superstar.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec16_fig2_superstar.png"))

# ---------------------------------------------------------------------
# 图 3：负所得税
fig3, ax3 = plt.subplots(figsize=(7.0, 4.6), dpi=120)
xr = list(range(0, 4001))
ax3.plot(xr, xr, color="#7f8c8d", lw=1.6, ls="--", label="无政策（净收入=收入）")
ax3.plot(xr, [net_a(x) for x in xr], color="#c0392b", lw=2.2, label="负所得税：补 1000、退坡 50%")
ax3.plot(xr, [net_b(x) for x in xr], color="#27ae60", lw=2.2, label="负所得税：补 1000、退坡 30%")
ax3.annotate("起点抬高到 1000", xy=(0, 1000), xytext=(350, 1400), fontsize=9.5,
             arrowprops=dict(arrowstyle="->", color="#2c3e50", lw=1))
ax3.annotate("退坡段：斜率更平（隐含税）", xy=(1000, 1500), xytext=(300, 2550), fontsize=9.5, color="#922b21",
             arrowprops=dict(arrowstyle="->", color="#922b21", lw=1))
ax3.set_xlabel("自己挣的收入（元）")
ax3.set_ylabel("净收入（元）")
ax3.set_title("负所得税：把'安全网'和'干活激励'放进同一条线")
ax3.set_xlim(0, 4000)
ax3.set_ylim(0, 4200)
ax3.legend(loc="upper left", fontsize=9)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec16_fig3_negative_tax.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec16_fig3_negative_tax.png"))

print()
print("[OK] figures/lec16_fig1_lorenz、lec16_fig2_superstar、lec16_fig3_negative_tax 已生成。")