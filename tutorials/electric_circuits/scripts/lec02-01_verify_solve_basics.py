# =====================================================================
# lec02-01 解电路初体验：四个求解实验与回代验算（第 02 讲 §4）
# 规模纪律：总耗时 < 5 秒（纯算术 + 一张小图）。
# 方法：
#   实验 1：分压器全解（9 V 源 + 2 kΩ + 1 kΩ）——i = 3 mA、u1 = 6 V、
#           u2 = 3 V；KVL 残差与功率平衡（27 = 18 + 9 mW）。
#   实验 2：含受控源单回路（3 V + 1 Ω + CCVS[2 Ω]）——i = 1 A；
#           功率账 3 = 1 + 2 W（受控源吸收 2 W）。
#   实验 3：单结点对（2 mA 源并联 1 kΩ × 2）——u = 1 V；
#           功率账 2 = 1 + 1 mW。
#   实验 4：实际电池带载（6 V + 1 kΩ 内阻 + 3 kΩ 负载）——i = 1.5 mA、
#           端电压 4.5 V；功率账 9 = 2.25 + 4.5 + 2.25 mW。
#   并生成 figures/lec02_fig1_divider.svg 与 .png（分压器电路图）。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
# =====================================================================
import os

import matplotlib
matplotlib.use("Agg")

import schemdraw
import schemdraw.elements as elm

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../electric_circuits
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# ---------------------------------------------------------------------
print("=== 实验 1：分压器全解（9 V 源 + 2 kΩ + 1 kΩ） ===")
U, R1, R2 = 9.0, 2000.0, 1000.0
i = U / (R1 + R2)
u1, u2 = R1 * i, R2 * i
print("  KVL 联立：9 = (2000 + 1000)i  ->  i = %.1f mA" % (i * 1e3))
print("  回代：u_R1 = %.0f V, u_R2 = %.0f V;  KVL 残差 = %.2e V" % (u1, u2, U - u1 - u2))
p_src, p1, p2 = U * i, u1 * i, u2 * i
print("  功率账（mW）：发出 %.1f = 吸收 %.1f + %.1f;  残差 = %.2e mW"
      % (p_src * 1e3, p1 * 1e3, p2 * 1e3, (p_src - p1 - p2) * 1e3))
print("  -> 输出端（R2 上端）相对负极：%.0f V（空载）" % u2)

# ---------------------------------------------------------------------
print()
print("=== 实验 2：含受控源单回路（3 V + 1 Ω + CCVS[2 Ω]） ===")
U2, Rr, k = 3.0, 1.0, 2.0
i2 = U2 / (Rr + k)
u_r, u_cs = Rr * i2, k * i2
print("  KVL：3 - i - 2i = 0  ->  i = %.1f A" % i2)
print("  回代：u_R = %.0f V, u_受控 = %.0f V;  KVL 残差 = %.2e V" % (u_r, u_cs, U2 - u_r - u_cs))
print("  功率（W）：源发出 %.1f = R 吸收 %.1f + 受控源吸收 %.1f（受控源在吃功率）"
      % (U2 * i2, u_r * i2, u_cs * i2))
print("  -> 控制量以一条普通档案方程进入联立，无特殊处理。")

# ---------------------------------------------------------------------
print()
print("=== 实验 3：单结点对（2 mA 源并联 1 kΩ × 2） ===")
I3 = 2e-3
Rp = 500.0  # 1k 并联 1k
u3 = I3 * Rp
i3_1 = i3_2 = u3 / 1000.0
print("  KCL：2 mA = i1 + i2；档案 i1 = i2 = u/1000  ->  u = %.1f V" % u3)
print("  i1 = i2 = %.1f mA;  KCL 残差 = %.2e A" % (i3_1 * 1e3, I3 - i3_1 - i3_2))
print("  功率（mW）：源发出 %.1f = 吸收 %.1f + %.1f;  残差 = %.2e mW"
      % (I3 * u3 * 1e3, u3 * i3_1 * 1e3, u3 * i3_2 * 1e3, (I3 - i3_1 - i3_2) * u3 * 1e3))
print("  -> 单结点对 + KCL 的最小解法（第 05 讲结点法的幼体）。")

# ---------------------------------------------------------------------
print()
print("=== 实验 4：实际电池带载（6 V + 1 kΩ 内阻 + 3 kΩ 负载） ===")
U4, Ri, RL = 6.0, 1000.0, 3000.0
i4 = U4 / (Ri + RL)
u_term = U4 - Ri * i4
u_2k, u_1k = u_term * (2000.0 / 3000.0), u_term * (1000.0 / 3000.0)
print("  总阻 4 kΩ：i = 6/4000 = %.1f mA" % (i4 * 1e3))
print("  端电压 = 6 - 1000 x 1.5 mA = %.1f V（比 6 V 下垂 1.5 V）" % u_term)
print("  负载分配：u_2k = %.1f V, u_1k = %.1f V（和 = %.1f V = 端电压）" % (u_2k, u_1k, u_2k + u_1k))
p4 = (U4 * i4, Ri * i4**2, u_2k * i4, u_1k * i4)
print("  功率账（mW）：源发出 %.2f = 内阻 %.2f + 2k %.2f + 1k %.2f;  残差 = %.2e mW"
      % (p4[0] * 1e3, p4[1] * 1e3, p4[2] * 1e3, p4[3] * 1e3, (p4[0] - p4[1] - p4[2] - p4[3]) * 1e3))
print("  -> 元件升级后一切照算：端电压随负载下垂是可算的正常现象。")

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：分压器电路图 ===")
elm.style(elm.STYLE_IEC)
schemdraw.config(font="Microsoft YaHei", fontsize=14)

with schemdraw.Drawing(show=False) as d:
    d += elm.BatteryCell().up().length(3).label("9 V", loc="left")
    d += elm.Line().up().length(3)
    d += elm.Line().right().length(4)
    d += elm.Resistor().down().length(3).label("$R_1$ = 2 kΩ", loc="right")
    d += elm.Dot()
    d += elm.Resistor().down().length(3).label("$R_2$ = 1 kΩ", loc="right", ofst=(0, -1.5))
    d += elm.Line().left().length(4)
    d += elm.Line().at((4, 3)).right().length(2.2).label("输出端（空载 3 V）", loc="bottom")

d.save(os.path.join(FIGDIR, "lec02_fig1_divider.svg"), transparent=False)
d.save(os.path.join(FIGDIR, "lec02_fig1_divider.png"), transparent=False, dpi=200)
print("[OK] figures/lec02_fig1_divider.svg 与 .png 已生成。")