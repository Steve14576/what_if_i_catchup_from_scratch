# =====================================================================
# lec03-01 串并联与分压分流：引子带载全解、公式核对、等效化简（第 03 讲 引子 / §1）
# 规模纪律：总耗时 < 10 秒（纯算术 + 两张小图）。
# 方法：
#   实验 1：引子——分压器带载（9 V + 2 kΩ + 1 kΩ，负载 1 kΩ）：
#           化简链 R2∥RL = 0.5 kΩ → 总阻 2.5 kΩ → i = 3.6 mA → 输出 1.8 V；
#           功率账（mW）32.4 = 25.92 + 3.24 + 3.24；并用直接结点方程交叉核对。
#   实验 2：分压公式核对（空载 9 V + 2 kΩ + 1 kΩ → 输出 3 V）。
#   实验 3：分流公式核对（6 mA 注入 2 kΩ ∥ 3 kΩ → 3.6 mA / 2.4 mA，电压同 7.2 V）。
#   实验 4：串并联等效公式核对（ΣR 与 G 求和、两电阻"积除和"）。
#   并生成 figures/lec03_fig1_loaded_divider.svg 与 .png（引子：带载分压器），
#       figures/lec03_fig2_divider_splitter.svg 与 .png（分压/分流对偶）。
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

elm.style(elm.STYLE_IEC)
schemdraw.config(font="Microsoft YaHei", fontsize=14)

# ---------------------------------------------------------------------
print("=== 实验 1：引子——分压器带载（9 V + 2 kΩ + 1 kΩ，负载 1 kΩ） ===")
U, R1, R2, RL = 9.0, 2000.0, 1000.0, 1000.0
R_par = R2 * RL / (R2 + RL)      # 1k 并 1k = 0.5k
R_tot = R1 + R_par               # 2.5k
i = U / R_tot                    # 3.6 mA
u_out = R_par * i                # 1.8 V
print("  化简链：R2 并 RL = %.2f kΩ；总阻 = %.1f kΩ；i = %.2f mA"
      % (R_par / 1e3, R_tot / 1e3, i * 1e3))
print("  输出 = %.2f V（空载时是 3 V——被负载拉低）" % u_out)
p_src = U * i
p1 = R1 * i**2
p2 = u_out**2 / R2
p_l = u_out**2 / RL
print("  功率账（mW）：发出 %.2f = 吸收 %.2f + %.2f + %.2f；残差 = %.2e"
      % (p_src * 1e3, p1 * 1e3, p2 * 1e3, p_l * 1e3, (p_src - p1 - p2 - p_l) * 1e3))
V_node = (U / R1) / (1 / R1 + 1 / R2 + 1 / RL)   # 对输出结点直接列 KCL
print("  直接结点方程交叉核对：V = %.2f V；与化简法差 = %.2e V"
      % (V_node, abs(V_node - u_out)))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：分压公式核对（空载） ===")
u2_div = U * R2 / (R1 + R2)
i_unload = U / (R1 + R2)
print("  分压公式：u2 = 9 x 1/(2+1) = %.1f V；直接解：i = %.1f mA，u2 = %.1f V"
      % (u2_div, i_unload * 1e3, R2 * i_unload))
print("  两者差 = %.2e V（空载 3 V，与 02 讲一致）" % abs(u2_div - R2 * i_unload))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：分流公式核对（6 mA 注入 2 kΩ ∥ 3 kΩ） ===")
I3 = 6e-3
Ra, Rb = 2000.0, 3000.0
i_a = I3 * Rb / (Ra + Rb)        # 分流看"对面"的电阻
i_b = I3 * Ra / (Ra + Rb)
u_a, u_b = i_a * Ra, i_b * Rb
print("  i_2k = 6 x 3/5 = %.1f mA；i_3k = 6 x 2/5 = %.1f mA" % (i_a * 1e3, i_b * 1e3))
print("  各自电阻上的电压：%.2f V 与 %.2f V（并联必须相等）；差 = %.2e V"
      % (u_a, u_b, abs(u_a - u_b)))
print("  用导纳口径核对：G1:G2 = %.2f : %.2f" % (1 / Ra * 1e3, 1 / Rb * 1e3))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：串并联等效公式核对 ===")
R_ser = R1 + R2
R_par2 = R1 * R2 / (R1 + R2)
R_par2_G = 1 / (1 / R1 + 1 / R2)
print("  串联：R1+R2 = %.1f kΩ（直接求和）" % (R_ser / 1e3))
print("  并联：积除和 = %.4f kΩ；导纳口径 = %.4f kΩ；差 = %.2e kΩ"
      % (R_par2 / 1e3, R_par2_G / 1e3, abs(R_par2 - R_par2_G) / 1e3))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：引子——带载的分压器 ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.BatteryCell().at((0, 0)).to((0, 3))
    d += elm.Label().at((-0.7, 1.5)).label("9 V")
    d += elm.Line().at((0, 3)).to((4, 3))
    d += elm.Resistor().at((4, 3)).to((4, 1.5))
    d += elm.Label().at((2.3, 2.35)).label("$R_1$ = 2 kΩ")
    d += elm.Resistor().at((4, 1.5)).to((4, 0))
    d += elm.Label().at((5.45, 0.72)).label("$R_2$ = 1 kΩ")
    d += elm.Line().at((4, 1.5)).to((7, 1.5))
    d += elm.Resistor().at((7, 1.5)).to((7, 0))
    d += elm.Label().at((8.45, 0.72)).label("负载 1 kΩ")
    d += elm.Line().at((0, 0)).to((7, 0))
    d += elm.Dot().at((4, 1.5))
    d += elm.Dot().at((4, 0))
    d += elm.Label().at((6.6, 1.9)).label("输出端：3 V 还作数吗？")
save_stem = "lec03_fig1_loaded_divider"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("=== 生成图 2：分压与分流（对偶） ===")
with schemdraw.Drawing(show=False) as d:
    # (a) 串联：分压
    d += elm.BatteryCell().at((0, 0)).to((0, 3))
    d += elm.Label().at((-0.65, 1.5)).label("$U$")
    d += elm.Line().at((0, 3)).to((1, 3))
    d += elm.Resistor().at((1, 3)).to((3, 3))
    d += elm.Resistor().at((3, 3)).to((5, 3))
    d += elm.Line().at((5, 3)).to((5, 0))
    d += elm.Line().at((5, 0)).to((0, 0))
    d += elm.Label().at((2, 3.5)).label("$R_1$")
    d += elm.Label().at((4, 3.5)).label("$R_2$")
    d += elm.Label().at((2, 2.55)).label("$u_1$")
    d += elm.Label().at((4, 2.55)).label("$u_2$")
    d += elm.Label().at((2.5, 1.2)).label("同一电流 $i$")
    d += elm.Arrow().at((1.2, 1.9)).to((2.2, 1.9))
    d += elm.Label().at((2.5, -0.85)).label("(a) 串联：$u_k = U\\,R_k/R_{eq}$")
    # (b) 并联：分流
    d += elm.BatteryCell().at((9, 0)).to((9, 3))
    d += elm.Label().at((8.35, 1.5)).label("$U$")
    d += elm.Line().at((9, 3)).to((12.5, 3))
    d += elm.Resistor().at((10.5, 3)).to((10.5, 0))
    d += elm.Resistor().at((12.5, 3)).to((12.5, 0))
    d += elm.Line().at((9, 0)).to((12.5, 0))
    d += elm.Dot().at((10.5, 3))
    d += elm.Dot().at((10.5, 0))
    d += elm.Label().at((11.15, 2.3)).label("$i_1$")
    d += elm.Label().at((13.15, 2.3)).label("$i_2$")
    d += elm.Arrow().at((10.5, 2.95)).to((10.5, 2.4))
    d += elm.Arrow().at((12.5, 2.95)).to((12.5, 2.4))
    d += elm.Label().at((9.8, 3.5)).label("$R_1$")
    d += elm.Label().at((11.9, 3.5)).label("$R_2$")
    d += elm.Label().at((11.5, 0.75)).label("同一电压")
    d += elm.Label().at((10.75, -0.85)).label("(b) 并联：$i_k = I\\,G_k/G_{eq}$")
save_stem = "lec03_fig2_divider_splitter"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec03-01 完成。")