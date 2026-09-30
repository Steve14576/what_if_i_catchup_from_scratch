# =====================================================================
# lec03-01 供需均衡与冲击分析（第 03 讲 §2-§5）
# 规模纪律：总耗时 < 5 秒（纯算术 + 三张小图）。
# 方法：
#   实验 1：番茄市场的供需表与均衡求解。
#           Qd = 160 - 20P；Qs = 20P - 40。预期均衡 (5, 60)。
#   实验 2：三个冲击的比较静态。预期：
#           a 需求右移(+20) -> (5.5, 70)；b 供给左移(-20) -> (5.5, 50)；
#           c 双移动(需求+20 且供给-20) -> (6, 60)。
#   实验 3：价格的自我修正动态（过剩降价/短缺涨价，迭代收敛到 5）。
#   生成 figures/lec03_fig1_supply_demand.svg/.png、
#        figures/lec03_fig2_shifts.svg/.png、
#        figures/lec03_fig3_price_dynamics.svg/.png。
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

# 线性供需：Qd = A_d - B_d*P；Qs = A_s + B_s*P（数量单位：斤/天；价格单位：元/斤）
A_d, B_d = 160.0, 20.0
A_s, B_s = -40.0, 20.0


def Qd(P, A=A_d, B=B_d):
    return A - B * P


def Qs(P, A=A_s, B=B_s):
    return A + B * P


def equilibrium(A_d_, B_d_, A_s_, B_s_):
    # 联立 Qd = Qs 解线性方程
    P = (A_d_ - A_s_) / (B_d_ + B_s_)
    Q = A_d_ - B_d_ * P
    return P, Q


# ---------------------------------------------------------------------
print("=== 实验 1：番茄市场的供需表（Qd = 160 - 20P；Qs = 20P - 40） ===")
print("  价格 | 需求量 | 供给量 | 差额(供给-需求) | 状态")
for P in [3.0, 4.0, 5.0, 6.0, 7.0]:
    qd, qs = Qd(P), Qs(P)
    gap = qs - qd
    if gap > 0:
        state = "过剩（卖家想降价）"
    elif gap < 0:
        state = "短缺（买家愿加价）"
    else:
        state = "均衡"
    print("  %.1f  |  %5.0f |  %5.0f |     %+5.0f     | %s" % (P, qd, qs, gap, state))
P_eq, Q_eq = equilibrium(A_d, B_d, A_s, B_s)
print("  解方程 160 - 20P = 20P - 40 -> 40P = 200 -> P* = %.0f，Q* = %.0f" % (P_eq, Q_eq))
print("  -> 结论：只有 P=5 时买卖量恰好对上；其他价格都会产生调整压力。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：三个冲击的比较静态 ===")
print("  基准均衡：P* = %.1f，Q* = %.0f" % equilibrium(A_d, B_d, A_s, B_s))
cases = [
    ("a 需求右移（每个价格上需求量 +20，如新地铁开通）", A_d + 20, B_d, A_s, B_s),
    ("b 供给左移（每个价格上供给量 -20，如肥料涨价）", A_d, B_d, A_s - 20, B_s),
    ("c 双移动（需求 +20 且供给 -20）", A_d + 20, B_d, A_s - 20, B_s),
]
for name, Ad, Bd, As, Bs in cases:
    P, Q = equilibrium(Ad, Bd, As, Bs)
    dP, dQ = P - P_eq, Q - Q_eq
    print("  %s" % name)
    print("     新均衡：P* = %.1f（%+.1f），Q* = %.0f（%+.0f）" % (P, dP, Q, dQ))
print("  -> 结论：需求右移 (P↑,Q↑)；供给左移 (P↑,Q↓)；双移动 (P↑↑，Q 恰好不变——")
print("     本例两股力量数量效果正好抵消；一般情形下双移动对某一变量的方向要看相对幅度)。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：价格自我修正的动态（过剩降价 / 短缺涨价） ===")
print("  调整规则：P <- P + 0.02 * (Qd - Qs)，即缺口越大调得越快")
for P0 in [3.0, 7.0]:
    print("  从 P = %.1f 出发：" % P0)
    P = P0
    for t in range(6):
        gap = Qd(P) - Qs(P)
        print("    第 %d 步：P = %.4f，缺口(需求-供给) = %+7.2f" % (t, P, gap))
        P = P + 0.02 * gap
    print("    第 6 步后：P = %.4f  -> 已贴着 5.0" % P)
print("  -> 结论：没人指挥，过剩压价、短缺抬价，价格自己爬向均衡 5.0。")

# ---------------------------------------------------------------------
# 图 1：基础供需图
fig, ax = plt.subplots(figsize=(6.6, 4.6), dpi=120)
Ps = [x / 10 for x in range(10, 81)]  # 1.0 .. 8.0
ax.plot([Qd(p) for p in Ps], Ps, color="#c0392b", lw=2, label="需求 D")
ax.plot([Qs(p) for p in Ps], Ps, color="#2471a3", lw=2, label="供给 S")
ax.plot([Q_eq], [P_eq], "ko", ms=9)
ax.annotate("均衡 E（60, 5）", xy=(Q_eq, P_eq), xytext=(70, 6.4), fontsize=10)
ax.plot([Q_eq, Q_eq], [0, P_eq], color="#7f8c8d", ls="--", lw=1)
ax.plot([0, Q_eq], [P_eq, P_eq], color="#7f8c8d", ls="--", lw=1)
ax.set_xlabel("数量 Q（斤/天）")
ax.set_ylabel("价格 P（元/斤）")
ax.set_title("番茄市场：供需相遇于均衡")
ax.set_xlim(0, 130)
ax.set_ylim(0, 8)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec03_fig1_supply_demand.svg"))
fig.savefig(os.path.join(FIGDIR, "lec03_fig1_supply_demand.png"))

# ---------------------------------------------------------------------
# 图 2：三联比较静态
fig2, axes = plt.subplots(1, 3, figsize=(12.6, 4.0), dpi=120)
titles = ["a 需求右移：P↑ Q↑", "b 供给左移：P↑ Q↓", "c 双移动：P↑↑，Q 恰好不变"]
for ax2, (name, Ad, Bd, As, Bs), tt in zip(axes, cases, titles):
    ax2.plot([Qd(p) for p in Ps], Ps, color="#bdc3c7", lw=1.6, ls="--", label="原需求")
    ax2.plot([Qs(p) for p in Ps], Ps, color="#bdc3c7", lw=1.6, ls=":", label="原供给")
    # 新需求 / 新供给（按案例选择画哪条动）
    if Ad != A_d:
        ax2.plot([Qd(p, Ad, Bd) for p in Ps], Ps, color="#c0392b", lw=2, label="新需求")
    else:
        ax2.plot([Qd(p) for p in Ps], Ps, color="#c0392b", lw=2, label="需求")
    if As != A_s:
        ax2.plot([Qs(p, As, Bs) for p in Ps], Ps, color="#2471a3", lw=2, label="新供给")
    else:
        ax2.plot([Qs(p) for p in Ps], Ps, color="#2471a3", lw=2, label="供给")
    P1, Q1 = equilibrium(Ad, Bd, As, Bs)
    ax2.plot([Q_eq], [P_eq], "o", color="#7f8c8d", ms=7)
    ax2.plot([Q1], [P1], "ko", ms=8)
    ax2.annotate("新均衡", xy=(Q1, P1), xytext=(Q1 + 6, P1 + 0.7), fontsize=9)
    ax2.set_title(tt, fontsize=11)
    ax2.set_xlabel("数量 Q（斤/天）")
    ax2.set_ylabel("价格 P（元/斤）")
    ax2.set_xlim(0, 130)
    ax2.set_ylim(0, 8)
    ax2.legend(loc="upper right", fontsize=7.5)
fig2.tight_layout()
fig2.savefig(os.path.join(FIGDIR, "lec03_fig2_shifts.svg"))
fig2.savefig(os.path.join(FIGDIR, "lec03_fig2_shifts.png"))

# ---------------------------------------------------------------------
# 图 3：价格自我修正的动态轨迹
fig3, ax3 = plt.subplots(figsize=(6.6, 4.0), dpi=120)
for P0, color in [(3.0, "#c0392b"), (7.0, "#2471a3")]:
    traj = [P0]
    P = P0
    for _ in range(7):
        P = P + 0.02 * (Qd(P) - Qs(P))
        traj.append(P)
    ax3.plot(range(len(traj)), traj, "o-", color=color, lw=2, label="从 P=%.0f 出发" % P0)
ax3.axhline(P_eq, color="#7f8c8d", ls="--", lw=1.2)
ax3.annotate("均衡 5.0", xy=(6.4, P_eq), xytext=(6.2, 5.5), fontsize=10, color="#7f8c8d")
ax3.set_xlabel("调整步数")
ax3.set_ylabel("市场价格 P（元/斤）")
ax3.set_title("过剩压价、短缺抬价：价格自己爬向均衡")
ax3.set_ylim(2.6, 7.4)
ax3.legend(loc="upper right", fontsize=9)
fig3.tight_layout()
fig3.savefig(os.path.join(FIGDIR, "lec03_fig3_price_dynamics.svg"))
fig3.savefig(os.path.join(FIGDIR, "lec03_fig3_price_dynamics.png"))

print()
print("[OK] figures/lec03_fig1_supply_demand、lec03_fig2_shifts、lec03_fig3_price_dynamics 已生成。")