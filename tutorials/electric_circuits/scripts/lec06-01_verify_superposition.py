# =====================================================================
# lec06-01 叠加定理：分解与实测（04 电路部分响应、混合源陷阱、功率反例）
#          （第 06 讲 引子 / §2；图 1 三面板）
# 规模纪律：总耗时 < 10 秒（纯算术 + 一张三面板图）。
# 方法：
#   实验 1：04 电路（12V+2Ω ∥ 2Ω ∥ 10V+1Ω）叠加分解：
#           12V 单独作用 V1 = 3 V；10V 单独作用 V2 = 5 V；V = 3+5 = 8 V（与 04/05 一致）。
#   实验 2：支路电流逐项分解表（左/右/负载 × 两次单独作用 = 总计）。
#   实验 3：功率不能叠加：负载功率 32 W != 部分功率和 17 W；交叉项 15 W 补齐恒等式。
#   实验 4：混合源陷阱（12V+2Ω ∥ 2Ω + 4A 注入）：V = 6+4 = 10 V；
#           若把"置零"错当成"整条支路拿掉"，会得到 6+8 = 14 V 的错账（记录陷阱数值）。
#   实验 5：作业 Q2–Q4 数字预验证（12V+2Ω/6V+2Ω 变体；三源版 9 = 3+5+1；功率 40.5 vs 17.5）。
#   并生成 figures/lec06_fig1_zeroing.svg/.png（原电路 / 两次单独作用）。
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
print("=== 实验 1：04 电路的叠加分解 ===")
# 直接解（05 讲结点法 1 方程）
V_direct = (12 / 2 + 10 / 1) / (1 / 2 + 1 / 1 + 1 / 2)
# 12 V 单独作用（10 V 置零=短路）：(V-12)/2 + V/1 + V/2 = 0 -> 4V = 12
V1 = 12.0 / 4.0
# 10 V 单独作用（12 V 置零=短路）：(V-10)/1 + V/2 + V/2 = 0 -> 4V = 20
V2 = 20.0 / 4.0
print("  直接解 V = %.0f V；部分响应 V1 = %.0f V、V2 = %.0f V；V1+V2 = %.0f V；差 = %.2e"
      % (V_direct, V1, V2, V1 + V2, abs(V1 + V2 - V_direct)))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：支路电流逐项分解 ===")
# 约定方向：左支路 (12V 源->结点) 为正、右支路 (结点->10V 源) 为正、负载 (结点->参考) 为正
iL1, iL2 = (12 - V1) / 2.0, (0 - V2) / 2.0      # 左支路
iR1, iR2 = (V1 - 0) / 1.0, (V2 - 10) / 1.0      # 右支路
id1, id2 = V1 / 2.0, V2 / 2.0                   # 负载
print("  左支路：%.1f + (%.1f) = %.1f A（总解核对 %.1f A）" % (iL1, iL2, iL1 + iL2, (12 - V_direct) / 2))
print("  右支路：%.1f + (%.1f) = %.1f A（总解核对 %.1f A）" % (iR1, iR2, iR1 + iR2, (V_direct - 10) / 1))
print("  负载  ：%.1f +  %.1f  = %.1f A（总解核对 %.1f A）" % (id1, id2, id1 + id2, V_direct / 2))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：功率不能叠加 ===")
P_total = V_direct ** 2 / 2.0
P_sum = V1 ** 2 / 2.0 + V2 ** 2 / 2.0
P_cross = 2 * V1 * V2 / 2.0
print("  负载功率（用总电压）= %.0f W；部分功率和 = %.0f + %.0f = %.0f W -> 不相等"
      % (P_total, V1 ** 2 / 2, V2 ** 2 / 2, P_sum))
print("  恒等式：%.0f（部分）+ %.0f（交叉项）= %.0f W -> 交叉项就是被丢掉的那部分"
      % (P_sum, P_cross, P_sum + P_cross))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：混合源陷阱（短路后串联电阻还在） ===")
# 电路：12V+2Ω 支路到结点、2Ω 到参考、4A 电流源注入结点
V_mix = (12 / 2 + 4) / (1 / 2 + 1 / 2)          # (V-12)/2 + V/2 = 4 -> V = 10
V_mix1 = 12.0 / 2.0                              # 12V 单独：2V = 12 -> V = 6
V_mix2 = 4.0 / 1.0                               # 4A 单独：V/2 + V/2 = 4 -> V = 4
V_mix_wrong = 4.0 / 0.5                          # 错误做法：短路时把整条支路拿掉 -> 只剩 V/2 = 4 -> V = 8
print("  直接解 V = %.0f V；部分响应 %.0f + %.0f = %.0f V；差 = %.2e"
      % (V_mix, V_mix1, V_mix2, V_mix1 + V_mix2, abs(V_mix1 + V_mix2 - V_mix)))
print("  对照错解：若短路时把串联 2Ω 一并拿掉，4A 单独作用得 %.0f V，总和 %.0f V != %.0f V"
      % (V_mix_wrong, V_mix1 + V_mix_wrong, V_mix))

# ---------------------------------------------------------------------
print()
print("=== 实验 5：作业数字预验证 ===")
# Q2：12V+2Ω 与 6V+2Ω 并联供 2Ω 负载
V_q2 = 6.0
print("  Q2：V = %.0f V = %.0f（12V 独）+ %.0f（6V 独）；负载 %.0f A；右支路 %.0f A（部分 2 + (-2) 对消）"
      % (V_q2, 4.0, 2.0, V_q2 / 2, (V_q2 - 6) / 2))
# Q3：04 电路 + 2A 注入
V_q3 = 9.0
print("  Q3：V = %.0f V = %.0f+%.0f+%.0f（三个源）；负载 %.1f A"
      % (V_q3, 3, 5, 1, V_q3 / 2))
# Q4：三源电路负载功率
P_q4_total = (V_q3 / 2) ** 2 * 2
P_q4_sum = (3 / 2) ** 2 * 2 + (5 / 2) ** 2 * 2 + (1 / 2) ** 2 * 2
print("  Q4：负载功率 = %.1f W != 部分和 %.1f W（差 %.1f W 为交叉项）"
      % (P_q4_total, P_q4_sum, P_q4_total - P_q4_sum))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：叠加定理的置零三面板 ===")
with schemdraw.Drawing(show=False) as d:
    def panel(x0, title, left_short=False):
        global d
        # 左支路：正常 = 12V 源 + 2Ω；短路版 = 只有 2Ω
        if left_short:
            d += elm.Line().at((x0, 0)).to((x0, 0.55))
            d += elm.Resistor().at((x0, 0.55)).up().length(0.7)
            d += elm.Label().at((x0 - 0.85, 0.9)).label("2 Ω")
            d += elm.Line().at((x0, 1.25)).to((x0, 2.2))
        else:
            d += elm.SourceV().at((x0, 0)).up().length(1.0)
            d += elm.Label().at((x0 - 0.85, 0.5)).label("12 V")
            d += elm.Resistor().at((x0, 1.0)).up().length(0.7)
            d += elm.Label().at((x0 - 0.9, 1.35)).label("2 Ω")
            d += elm.Line().at((x0, 1.7)).to((x0, 2.2))
        # 顶部横线、负载支路、底部公共线
        d += elm.Line().at((x0, 2.2)).to((x0 + 3.4, 2.2))
        d += elm.Dot().at((x0 + 1.7, 2.2))
        d += elm.Resistor().at((x0 + 1.7, 0.9)).up().length(1.1)
        d += elm.Label().at((x0 + 2.5, 1.35)).label("2 Ω")
        d += elm.Line().at((x0 + 1.7, 2.2)).to((x0 + 1.7, 0.9))
        d += elm.Line().at((x0 + 1.7, 0.9)).to((x0 + 1.7, 0))
        d += elm.Line().at((x0, 0)).to((x0 + 3.4, 0))
        d += elm.Label().at((x0 + 1.7, -0.55)).label(title, fontsize=10)

    def right_full(x0):
        global d
        # 右支路：10V 源 + 1Ω
        d += elm.SourceV().at((x0 + 3.4, 0)).up().length(1.0)
        d += elm.Label().at((x0 + 4.35, 0.5)).label("10 V")
        d += elm.Resistor().at((x0 + 3.4, 1.0)).up().length(0.7)
        d += elm.Label().at((x0 + 4.3, 1.35)).label("1 Ω")
        d += elm.Line().at((x0 + 3.4, 1.7)).to((x0 + 3.4, 2.2))

    def right_short(x0):
        global d
        # 右支路：10V 置零 -> 短路（1Ω 保留）
        d += elm.Line().at((x0 + 3.4, 0)).to((x0 + 3.4, 1.0))
        d += elm.Resistor().at((x0 + 3.4, 1.0)).up().length(0.7)
        d += elm.Label().at((x0 + 4.3, 1.35)).label("1 Ω")
        d += elm.Line().at((x0 + 3.4, 1.7)).to((x0 + 3.4, 2.2))

    # (a) 原电路
    x0 = 0.0
    panel(x0, "（a）原电路")
    right_full(x0)
    d += elm.Label().at((x0 + 1.7, 2.75)).label("$V$")

    # (b) 12V 单独作用
    x1 = 7.0
    panel(x1, "（b）12 V 单独作用：10 V 置零 -> 短路")
    right_short(x1)
    d += elm.Label().at((x1 + 1.7, 2.75)).label("$V_1$ = 3 V")

    # (c) 10V 单独作用
    x2 = 14.0
    panel(x2, "（c）10 V 单独作用：12 V 置零 -> 短路", left_short=True)
    right_full(x2)
    d += elm.Label().at((x2 + 1.7, 2.75)).label("$V_2$ = 5 V")

save_stem = "lec06_fig1_zeroing"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec06-01 完成。")