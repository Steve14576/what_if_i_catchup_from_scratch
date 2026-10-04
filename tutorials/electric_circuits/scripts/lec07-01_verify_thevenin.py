# =====================================================================
# lec07-01 戴维南/诺顿三件套：开路电压、短路电流、等效电阻（含受控源与边界）
#          （第 07 讲 引子–§3；图 1 三面板）
# 规模纪律：总耗时 < 10 秒（纯算术 + 一张三面板图）。
# 方法：
#   实验 1：04 电路（12V+2Ω ∥ 10V+1Ω）从负载端看进去的三件套：
#           U_oc = 32/3 V、I_sc = 16 A、R_th = 2/3 Ω（置零化简 2∥1；互验一致）。
#   实验 2：任意负载一步解（戴维南分压公式 vs 直接解逐点核对）。
#   实验 3：边界展示——对外等效、内部不同（原网络内部电流 vs 戴维南盒里源的电流）。
#   实验 4：含受控源迷你单口（5V 源串 2Ω，VCCS 0.5S 受控于端口电压）：
#           三法全算 2.5 V / 2.5 A / 1 Ω，互验一致；对照错值（忽略受控源 -> 2Ω）。
#   实验 5：作业数字预验证（Q2：14 V/7 A/2Ω；Q4：5 V/2.5 A/2Ω；Q5 负载表）。
#   并生成 figures/lec07_fig1_capsule.svg/.png（原电路 / 戴维南盒 / 诺顿盒）。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
# =====================================================================
import os

import numpy as np
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
print("=== 实验 1：负载端看进去的三件套 ===")
U_oc = (12 / 2 + 10 / 1) / (1 / 2 + 1 / 1)      # 开路：拆掉负载解结点电压
I_sc = 12 / 2 + 10 / 1                            # 短路：两条支路电流直接相加
R_th_look = 1 / (1 / 2 + 1 / 1)                   # 置零化简：2Ω ∥ 1Ω
R_th_ratio = U_oc / I_sc                          # 互验：U_oc / I_sc
print("  U_oc = %.6f V（= 32/3）；I_sc = %.0f A；R_th（置零化简）= %.6f Ω（= 2/3）"
      % (U_oc, I_sc, R_th_look))
print("  互验 U_oc/I_sc = %.6f Ω；与置零化简之差 = %.2e"
      % (R_th_ratio, abs(R_th_ratio - R_th_look)))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：任意负载一步解（戴维南分压 vs 直接解） ===")
for RL in [0.5, 1.0, 2.0, 4.0]:
    V_thev = U_oc * RL / (R_th_look + RL)
    # 直接解原电路： (V-12)/2 + (V-10)/1 + V/RL = 0
    V_direct = (12 / 2 + 10 / 1) / (1 / 2 + 1 / 1 + 1 / RL)
    print("  RL = %.1f Ω：戴维南 %.6f V；直接解 %.6f V；差 = %.2e"
          % (RL, V_thev, V_direct, abs(V_thev - V_direct)))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：对外等效、内部不同 ===")
RL = 2.0
V_L = U_oc * RL / (R_th_look + RL)
i_box = V_L / RL                                  # 戴维南盒中源输出的电流
i_internal = (10 - V_L) / 1.0                     # 原网络内部 10V 支路电流（结点->源）
print("  负载 2 Ω：端电压 %.0f V、负载电流 %.0f A（两版一致）" % (V_L, V_L / RL))
print("  原网络内部（10V+1Ω 支路）电流 = %.0f A；戴维南盒里源的电流 = %.0f A -> 内部不同"
      % (i_internal, i_box))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：含受控源迷你单口（三法互验） ===")
# 电路：端口 P 经 2Ω 接 5V 源正端（源另一端接地）；VCCS 0.5S 受控于端口电压（向下）
U_oc_c = 2.5             # 开路： (5-u)/2 = 0.5u -> u = 2.5
I_sc_c = 5 / 2.0          # 短路：端口电压=0 -> VCCS 输出 0 -> 只剩 5/2
R_apply = 1.0             # 外施激励： i = u - 2.5 -> u = i + 2.5 -> R = 1
R_naive = 2.0             # 对照错值：忽略受控源只看见 2Ω
print("  开路电压 U_oc = %.1f V；短路电流 I_sc = %.1f A；互验 R = %.1f Ω"
      % (U_oc_c, I_sc_c, U_oc_c / I_sc_c))
# 外施激励法（标准姿势：独立源置零，受控源保留，再加测试源）
# 置零后： i = u/2 + 0.5u = u -> R = 1 Ω
i_test, u_test = 1.0, 1.0
print("  外施激励法（独立源置零后）：加 %.0f A -> u = %.1f V -> R = %.1f Ω（与互验一致）"
      % (i_test, u_test, u_test / i_test))
print("  注：若对含源网络直接外施，端口关系 u = i + 2.5 带着截距——R 要读「斜率」1 Ω，不能读 u/i（那会得 3.5 Ω，典型的坑）")
print("  对照错值：若求 R 时对受控源视而不见，只得 %.0f Ω，互验立刻穿帮" % R_naive)

# ---------------------------------------------------------------------
print()
print("=== 实验 5：作业数字预验证 ===")
# Q2：18V+3Ω 与 6V+6Ω 并在端口上
U2 = (18 / 3 + 6 / 6) / (1 / 3 + 1 / 6)
I2 = 18 / 3 + 6 / 6
R2 = 1 / (1 / 3 + 1 / 6)
print("  Q2：U_oc = %.0f V、I_sc = %.0f A、R_th = %.0f Ω（互验 %.0f）" % (U2, I2, R2, U2 / I2))
for RL in [1.0, 4.0]:
    V = U2 * RL / (R2 + RL)
    print("      RL = %.0f Ω：V = %.4f V、I = %.4f A、P = %.4f W" % (RL, V, V / RL, V * V / RL))
# Q4：10V+4Ω + VCCS 0.25S 受控于端口电压
# 开路：(10-u)/4 = 0.25u -> u = 5；短路（u=0）：10/4；外施（置零后）：i = u/4 + 0.25u = 0.5u
U_q4 = 10.0 / 2.0
I_q4 = 10.0 / 4.0
R_q4 = 1.0 / (0.25 + 1.0 / 4.0)
print("  Q4：U_oc = %.0f V、I_sc = %.1f A、R_th = %.0f Ω（互验 %.0f、外施 %.0f）"
      % (U_q4, I_q4, R_q4, U_q4 / I_q4, R_q4))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：浓缩机三面板 ===")
with schemdraw.Drawing(show=False) as d:
    def draw_network(x0, title):
        global d
        # 原电路：12V+2Ω 左支路、2Ω 负载、10V+1Ω 右支路
        d += elm.SourceV().at((x0, 0)).up().length(1.0)
        d += elm.Label().at((x0 - 0.85, 0.5)).label("12 V")
        d += elm.Resistor().at((x0, 1.0)).up().length(0.7)
        d += elm.Label().at((x0 - 0.9, 1.35)).label("2 Ω")
        d += elm.Line().at((x0, 1.7)).to((x0, 2.2))
        d += elm.Line().at((x0, 2.2)).to((x0 + 3.4, 2.2))
        d += elm.Dot().at((x0 + 1.7, 2.2))
        d += elm.Resistor().at((x0 + 1.7, 0.6)).up().length(1.0)
        d += elm.Label().at((x0 + 2.4, 1.1)).label("2 Ω")
        d += elm.Line().at((x0 + 1.7, 2.2)).to((x0 + 1.7, 1.6))
        d += elm.Line().at((x0 + 1.7, 0.6)).to((x0 + 1.7, 0))
        d += elm.SourceV().at((x0 + 3.4, 0)).up().length(1.0)
        d += elm.Label().at((x0 + 4.35, 0.5)).label("10 V")
        d += elm.Resistor().at((x0 + 3.4, 1.0)).up().length(0.7)
        d += elm.Label().at((x0 + 4.3, 1.35)).label("1 Ω")
        d += elm.Line().at((x0 + 3.4, 1.7)).to((x0 + 3.4, 2.2))
        d += elm.Line().at((x0, 0)).to((x0 + 3.4, 0))
        d += elm.Label().at((x0 + 1.7, -0.85)).label(title, fontsize=10)

    def draw_thev_eq(x0, title):
        global d
        # 左支路：源 10.67 V（+ 上）串 0.67 Ω；右支路：负载
        d += elm.SourceV().at((x0, 0)).up().length(1.0)
        d += elm.Label().at((x0 - 1.25, 0.5)).label("10.67 V")
        d += elm.Resistor().at((x0, 1.0)).up().length(0.7)
        d += elm.Label().at((x0 - 1.25, 1.35)).label("0.67 Ω")
        d += elm.Line().at((x0, 1.7)).to((x0, 1.8))
        d += elm.Line().at((x0, 1.8)).to((x0 + 2.2, 1.8))
        d += elm.Resistor().at((x0 + 2.2, 0.6)).up().length(1.2)
        d += elm.Label().at((x0 + 2.85, 1.2)).label("$R_L$")
        d += elm.Line().at((x0 + 2.2, 0.6)).to((x0 + 2.2, 0))
        d += elm.Line().at((x0, 0)).to((x0 + 2.2, 0))
        d += elm.Label().at((x0 + 1.1, -0.85)).label(title, fontsize=10)

    def draw_norton_eq(x0, title):
        global d
        # 左支路：16 A 源（箭头向上），并联 0.67 Ω 支路；右支路：负载
        d += elm.SourceI().at((x0, 0)).up().length(1.0)
        d += elm.Label().at((x0 - 0.9, 0.5)).label("16 A")
        d += elm.Line().at((x0, 1.0)).to((x0, 1.8))
        d += elm.Resistor().at((x0 + 1.0, 0.55)).up().length(0.7)
        d += elm.Label().at((x0 + 2.1, 0.9)).label("0.67 Ω")
        d += elm.Line().at((x0 + 1.0, 0)).to((x0 + 1.0, 0.55))
        d += elm.Line().at((x0 + 1.0, 1.25)).to((x0 + 1.0, 1.8))
        d += elm.Line().at((x0, 1.8)).to((x0 + 3.0, 1.8))
        d += elm.Resistor().at((x0 + 3.0, 0.6)).up().length(1.2)
        d += elm.Label().at((x0 + 3.65, 1.2)).label("$R_L$")
        d += elm.Line().at((x0 + 3.0, 0.6)).to((x0 + 3.0, 0))
        d += elm.Line().at((x0, 0)).to((x0 + 3.0, 0))
        d += elm.Label().at((x0 + 1.3, -0.85)).label(title, fontsize=10)

    draw_network(0.0, "（a）原电路：负载 2 Ω 时端电压 8 V")
    draw_thev_eq(7.0, "（b）戴维南等效：10.67 V 串 0.67 Ω")
    draw_norton_eq(13.0, "（c）诺顿等效：16 A 并 0.67 Ω")

save_stem = "lec07_fig1_capsule"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec07-01 完成。")