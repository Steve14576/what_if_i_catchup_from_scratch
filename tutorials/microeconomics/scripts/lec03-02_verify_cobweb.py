# =====================================================================
# lec03-02 蛛网模型：供给"看上一期价格"时的动态（第 03 讲 §4.4 补节）
# 规模纪律：总耗时 < 5 秒（纯算术 + 一张双联小图）。
# 方法：
#   需求 Q_d = 140 - 2P（固定）；时滞供给 Q_s,t = d * P_(t-1) + 20；
#   迭代 P_t = (140 - Q_s,t) / 2。三形态只换 d：
#     d=1（供:需弹性 = 0.5）：均衡 P*=40；从 60 出发 -> 振荡收敛；
#     d=2（弹性比 = 1.0）：均衡 P*=30；从 50 出发 -> 等幅循环（50 <-> 10）；
#     d=3（弹性比 = 1.5）：均衡 P*=24；从 30 出发 -> 发散（第 5 期为负）。
#   另打印 d=1 的蛛网相位转折点（Q, P），供图 4 左图核对。
#   生成 figures/lec03_fig4_cobweb.svg/.png（左：蛛网相位；右：三形态轨迹）。
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


def iterate(d, p0, n):
    """时滞迭代：Q_t = d*P_(t-1)+20；P_t = (140-Q_t)/2；返回价格序列（长度 n+1）"""
    ps = [p0]
    p = p0
    for _ in range(n):
        q = d * p + 20
        p = (140 - q) / 2
        ps.append(p)
    return ps


def long_run(d):
    """去掉时滞的长期均衡：140-2P = dP+20"""
    p_star = 120 / (2 + d)
    return p_star, d * p_star + 20


# ---------------------------------------------------------------------
print("=== 实验 4（补节）：蛛网模型三形态（需求 Q=140-2P；时滞供给 Q_t = d*P_(t-1)+20） ===")
cases = [
    (1, 60.0, "收敛"),
    (2, 50.0, "循环"),
    (3, 30.0, "发散"),
]
for d, p0, tag in cases:
    p_star, q_star = long_run(d)
    ps = iterate(d, p0, 5)
    ratio = d / 2.0
    print("  d=%d（供:需弹性比 %.1f）：长期均衡 P*=%.0f、Q*=%.0f" % (d, ratio, p_star, q_star))
    print("    价格轨迹（P0 起 6 期）：%s" % ["%.2f" % x for x in ps])
    print("    形态判定：%s（从错误价格出发的方向：%s）" %
          (tag, "越荡越近" if tag == "收敛" else ("永远来回" if tag == "循环" else "越荡越远")))
print("  -> 结论：供给弹性 < 需求弹性 -> 收敛；= -> 循环；> -> 发散。")

# ---------------------------------------------------------------------
print()
print("=== 蛛网相位转折点（d=1，从 P0=60 出发，供图 4 左图核对） ===")
p = 60.0
pts = [(None, p)]
for k in range(1, 6):
    q = 1 * p + 20
    pts.append((q, p))          # 横到供给线
    p = (140 - q) / 2
    pts.append((q, p))          # 竖到需求线
    print("  第 %d 环：产量 Q=%6.2f -> 新价 P=%6.2f" % (k, q, p))
print("  -> 阶梯一圈圈内收，终点趋近 (60, 40)。")

# ---------------------------------------------------------------------
# 图 4：双联（左：蛛网相位；右：三形态轨迹）
fig, (axa, axb) = plt.subplots(1, 2, figsize=(11.2, 4.6), dpi=120)

# 左：d=1 的蛛网相位
qs = [i / 2 for i in range(30, 201)]           # 15 .. 100
axa.plot(qs, [70 - q / 2 for q in qs], color="#c0392b", lw=2.2, label="需求 P = 70 - Q/2")
qs2 = [i / 2 for i in range(40, 161)]          # 20 .. 80
axa.plot(qs2, [q - 20 for q in qs2], color="#2471a3", lw=2.2, label="供给 P = Q - 20")
axa.plot([60], [40], "ko", ms=9)
axa.annotate("均衡 (60, 40)", xy=(60, 40), xytext=(50, 52), fontsize=10,
             arrowprops=dict(arrowstyle="-", color="#2c3e50", lw=0.8))
# 蛛网阶梯（d=1，从 P0=60 出发）
p = 60.0
xx, yy = [80], [60]
for _ in range(5):
    q = p + 20
    xx.append(q); yy.append(p)
    p = (140 - q) / 2
    xx.append(q); yy.append(p)
axa.plot(xx, yy, color="#27ae60", lw=1.6)
axa.annotate("蛛网一圈圈收拢", xy=(62, 36), xytext=(38, 56), fontsize=10, color="#1e8449",
             arrowprops=dict(arrowstyle="->", color="#1e8449", lw=1))
axa.set_xlabel("数量 Q")
axa.set_ylabel("价格 P")
axa.set_title("收拢的真蛛网（d=1）", fontsize=11)
axa.set_xlim(15, 100)
axa.set_ylim(0, 70)
axa.legend(loc="upper right", fontsize=8.5)

# 右：三形态价格轨迹
ts = list(range(0, 6))
ps1 = iterate(1, 60.0, 5)
ps2 = iterate(2, 50.0, 5)
ps3 = iterate(3, 30.0, 5)
axb.plot(ts, ps1, "o-", color="#1e8449", lw=2, label="d=1：收敛（P*=40）")
axb.plot(ts, ps2, "s-", color="#b9770e", lw=2, label="d=2：循环（P*=30）")
axb.plot(ts, ps3, "d-", color="#c0392b", lw=2, label="d=3：发散（P*=24）")
for p_star, c in [(40, "#1e8449"), (30, "#b9770e"), (24, "#c0392b")]:
    axb.axhline(p_star, color=c, lw=1, ls="--", alpha=0.55)
axb.annotate("第 5 期：价格已为负\n（模型宣布失控）", xy=(5, -21.56), xytext=(2.2, -19), fontsize=9.5, color="#922b21",
             arrowprops=dict(arrowstyle="->", color="#922b21", lw=1))
axb.set_xlabel("期数（年）")
axb.set_ylabel("价格 P")
axb.set_title("三种命运：只看一个数字（d）", fontsize=11)
axb.set_xticks(ts)
axb.set_xlim(0, 5.4)
axb.set_ylim(-30, 66)
axb.legend(loc="upper center", fontsize=8.5)
fig.suptitle("蛛网模型：供给看'上一期的价'时的价与量", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(os.path.join(FIGDIR, "lec03_fig4_cobweb.svg"))
fig.savefig(os.path.join(FIGDIR, "lec03_fig4_cobweb.png"))

print()
print("[OK] figures/lec03_fig4_cobweb 已生成。")