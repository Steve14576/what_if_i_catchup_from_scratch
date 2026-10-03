# =====================================================================
# lec01-02 功率平衡：引子两元件账与含导线三元件账（第 01 讲 §4）
# 规模纪律：总耗时 < 5 秒（纯算术 + 一张小图）。
# 方法：
#   实验 1：引子回路两元件账——电池发出 0.45 W，灯泡吸收 0.45 W，
#           按"吸收"口径求和残差应为 0（浮点机器精度）。
#           预期：-0.45 + 0.45 = 0。
#   实验 2：含导线三元件账——电池发出 0.75 W；灯泡吸收 0.725 W；
#           导线吸收 0.025 W；吸收合计 0.75 W 与发出配平。
#           预期：0.725 + 0.025 = 0.75。
#   并生成 figures/lec01_fig2_power_balance.svg 与 .png（两本账配平视图）。
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

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../electric_circuits
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# ---------------------------------------------------------------------
print("=== 实验 1：引子回路的两元件功率账 ===")
u_batt, i_loop = 1.5, 0.3
p_batt = -(u_batt * i_loop)  # 电池：电流从 + 流出 -> 非关联
p_lamp = +(u_batt * i_loop)  # 灯泡：电流从 + 流入 -> 关联（理想导线，灯泡电压 = 电池电压）
print("  电池（非关联）：p = -(1.5 x 0.3) = %+.2f W  -> 发出" % p_batt)
print("  灯泡（关联）  ：p = +(1.5 x 0.3) = %+.2f W  -> 吸收" % p_lamp)
res1 = p_batt + p_lamp
print("  按'吸收'口径求和：%+.2f + %+.2f = %.2e W（机器精度，即 0）" % (p_batt, p_lamp, res1))
print("  -> 结论：两元件账配平：发出 0.45 W = 吸收 0.45 W。")

# ---------------------------------------------------------------------
print()
print("=== 实验 2：含导线的三元件功率账 ===")
u2, i2 = 1.5, 0.5
u_wire, u_lamp = 0.05, 1.45
p_batt2 = -(u2 * i2)     # 非关联
p_lamp2 = +(u_lamp * i2)  # 关联
p_wire2 = +(u_wire * i2)  # 关联
print("  电压分配核对：导线 %.2f V + 灯泡 %.2f V = %.2f V（电池电压）" % (u_wire, u_lamp, u_wire + u_lamp))
print("  电池（非关联）：p = -(1.5 x 0.5)  = %+.3f W -> 发出" % p_batt2)
print("  灯泡（关联）  ：p = +(1.45 x 0.5) = %+.3f W -> 吸收" % p_lamp2)
print("  导线（关联）  ：p = +(0.05 x 0.5) = %+.3f W -> 吸收" % p_wire2)
res2 = p_batt2 + p_lamp2 + p_wire2
print("  按'吸收'口径求和：%+.3f + %+.3f + %+.3f = %.2e W（机器精度，即 0）"
      % (p_batt2, p_lamp2, p_wire2, res2))
print("  -> 结论：账多了新成员照样平：0.725 + 0.025 = 0.75 W。")

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：两本功率账的配平视图 ===")
fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=120)
labels = ["电池", "灯泡", "电池", "灯泡", "导线"]
xs = [0, 1, 3, 4, 5]
vals = [p_batt, p_lamp, p_batt2, p_lamp2, p_wire2]
colors = ["#c0392b" if v < 0 else "#2471a3" for v in vals]
ax.bar(xs, vals, color=colors, width=0.62)
for x, v in zip(xs, vals):
    va = "bottom" if v > 0 else "top"
    off = 0.03 if v > 0 else -0.03
    ax.text(x, v + off, "%+.3g" % v, ha="center", va=va, fontsize=10)
ax.axhline(0, color="#7f8c8d", lw=1)
ax.axvline(2, color="#bdc3c7", lw=1, ls="--")
ax.text(0.5, 0.64, "引子回路（两元件账）", ha="center", fontsize=10)
ax.text(4, 0.92, "含导线回路（三元件账）", ha="center", fontsize=10)
ax.set_xticks(xs)
ax.set_xticklabels(labels)
ax.set_ylabel("功率 / W（正 = 吸收，负 = 发出）")
ax.set_title("功率账配平：每组的向上面积 = 向下面积")
ax.set_ylim(-0.95, 1.04)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "lec01_fig2_power_balance.svg"))
fig.savefig(os.path.join(FIGDIR, "lec01_fig2_power_balance.png"))
print("[OK] figures/lec01_fig2_power_balance.svg 与 .png 已生成。")