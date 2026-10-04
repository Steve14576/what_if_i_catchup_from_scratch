# =====================================================================
# lec02-03 补充配图组：支路结点回路词汇、KCL、KVL、三个实验电路图
#          （第 02 讲 §3.1 / §3.2 / §3.3 / §4.3 / §4.4 / §4.5）
# 规模纪律：总耗时 < 15 秒（六张小图，纯绘图 + 数字核对）。
# 方法：
#   核对：KCL 结点例（2 = 1 + 0.5 + i4）与 KVL 最小例（-6 + 2 + 4 = 0），
#         以及三个实验电路的数字与 lec02-01 交叉一致
#         （受控源回路 i = 1 A；单结点对 u = 1 V；电池带载 i = 1.5 mA）。
#   出图：
#     lec02_fig3_branch_node_loop  支路/结点/回路在一个并联电路上辨认
#     lec02_fig4_kcl               两联图：(a) 单结点账 (b) 广义结点打包
#     lec02_fig5_kvl               A/B/C 回路：极性、绕行方向与记账
#     lec02_fig6_ccvs              含受控源单回路（菱形 CCVS）
#     lec02_fig7_node_pair         单结点对（结点处 KCL 箭头）
#     lec02_fig8_battery_load      实际电池带载（内阻 + 负载）
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ->）。
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
print("=== 数字核对（与 lec02-01 交叉） ===")
i4 = 2 - 1 - 0.5
print("  KCL 结点例：i4 = 2 - 1 - 0.5 = %.1f mA" % i4)
r_kvl = -6 + 2 + 4
print("  KVL 最小例：-6 + 2 + 4 = %.1f（应为 0）" % r_kvl)

i6 = 3.0 / (1.0 + 2.0)
print("  受控源回路：i = 3 / (1 + 2) = %.1f A；u_R = %.1f V；u_受控 = %.1f V"
      % (i6, 1.0 * i6, 2.0 * i6))

u7 = 2e-3 * 500.0
print("  单结点对：u = 2 mA x 500 ohm = %.1f V；i1 = i2 = %.1f mA"
      % (u7, (u7 / 1000.0) * 1e3))

i8 = 6.0 / 4000.0
u_term = 6.0 - 1000.0 * i8
print("  电池带载：i = %.1f mA；端电压 = %.1f V（从 6 V 下垂 %.1f V）"
      % (i8 * 1e3, u_term, 6.0 - u_term))


def save(d, stem):
    d.save(os.path.join(FIGDIR, stem + ".svg"), transparent=False)
    d.save(os.path.join(FIGDIR, stem + ".png"), transparent=False, dpi=200)
    print("[OK] figures/%s.svg 与 .png 已生成。" % stem)


# ---------------------------------------------------------------------
print()
print("=== 图 3：支路 / 结点 / 回路词汇图 ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.SourceV().at((0, 0)).to((0, 3))
    d += elm.Label().at((-1.05, 1.5)).label("支路①")
    d += elm.Line().at((0, 3)).to((6, 3))
    d += elm.Resistor().at((3, 3)).to((3, 0))
    d += elm.Label().at((3.9, 1.5)).label("支路②")
    d += elm.Resistor().at((6, 3)).to((6, 0))
    d += elm.Label().at((6.9, 1.5)).label("支路③")
    d += elm.Line().at((0, 0)).to((6, 0))
    d += elm.Dot().at((3, 3))
    d += elm.Dot().at((3, 0))
    d += elm.Label().at((3.5, 3.45)).label("结点")
    d += elm.Label().at((3.45, -0.5)).label("结点")
    # 左侧网孔内的回路指示箭头（逆时针一圈）
    d += elm.Arrow().at((0.8, 0.7)).to((0.8, 2.3))
    d += elm.Arrow().at((0.8, 2.3)).to((2.2, 2.3))
    d += elm.Arrow().at((2.2, 2.3)).to((2.2, 0.7))
    d += elm.Arrow().at((2.2, 0.7)).to((0.8, 0.7))
    d += elm.Label().at((1.5, 1.5)).label("回路")
    d += elm.Label().at((1.4, -0.8)).label("四角是 2 支路相接：并掉，不算结点")
save(d, "lec02_fig3_branch_node_loop")

# ---------------------------------------------------------------------
print()
print("=== 图 4：KCL 两联图 ===")
with schemdraw.Drawing(show=False) as d:
    # (a) 单结点：4 条支路的进出账（文字全部自由摆放，避开箭头与结点）
    d += elm.Arrow().at((0.25, 2)).to((2.9, 2))
    d += elm.Arrow().at((3.1, 2)).to((5.75, 2))
    d += elm.Arrow().at((3, 2.1)).to((3, 3.9))
    d += elm.Arrow().at((3, 1.9)).to((3, 0.1))
    d += elm.Dot().at((3, 2))
    d += elm.Label().at((1.4, 2.5)).label("$i_1$ = 2 mA（入）")
    d += elm.Label().at((4.6, 2.5)).label("$i_2$ = 1 mA（出）")
    d += elm.Label().at((4.45, 3.3)).label("$i_3$ = 0.5 mA（出）")
    d += elm.Label().at((4.45, 1.0)).label("$i_4$ = ?（出）")
    d += elm.Label().at((2.9, 4.5)).label("(a) 单结点：流入 = 流出")
    d += elm.Label().at((1.7, -0.85)).label("KCL：2 = 1 + 0.5 + $i_4$")
    # (b) 广义结点：虚线框打包记账
    d += elm.Arrow().at((9.5, 3)).to((11.5, 3))
    d += elm.Line().at((11.5, 3)).to((11.5, 1.5))
    d += elm.Resistor().at((11.5, 1.5)).to((14, 1.5))
    d += elm.Arrow().at((14, 1.5)).to((16.3, 1.5))
    d += elm.Arrow().at((11.5, 1.5)).to((11.5, -0.6))
    d += elm.Dot().at((11.5, 1.5))
    d += elm.Dot().at((14, 1.5))
    # 虚线打包框（四条虚线围成矩形）
    d += elm.Line(ls="--").at((10.2, 0.3)).to((15.2, 0.3))
    d += elm.Line(ls="--").at((15.2, 0.3)).to((15.2, 2.4))
    d += elm.Line(ls="--").at((15.2, 2.4)).to((10.2, 2.4))
    d += elm.Line(ls="--").at((10.2, 2.4)).to((10.2, 0.3))
    d += elm.Label().at((10.4, 3.35)).label("$i_a$ = 2 mA（进）")
    d += elm.Label().at((12.75, 2.0)).label("内部支路")
    d += elm.Label().at((16.5, 1.95)).label("$i_b$ = 1.5 mA")
    d += elm.Label().at((9.9, -0.35)).label("$i_c$ = ?（出）")
    d += elm.Label().at((12.8, 4.0)).label("(b) 广义结点：整块打包")
    d += elm.Label().at((12.8, -1.2)).label("KCL（对框）：2 = 1.5 + $i_c$")
save(d, "lec02_fig4_kcl")

# ---------------------------------------------------------------------
print()
print("=== 图 5：KVL 绕行示意（A / B / C 回路） ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.RBox().at((0, 0)).to((0, 3.5))
    d += elm.RBox().at((0, 3.5)).to((6, 3.5))
    d += elm.RBox().at((6, 3.5)).to((6, 0))
    d += elm.Label().at((-0.7, 1.75)).label("A")
    d += elm.Label().at((3.0, 3.95)).label("B")
    d += elm.Label().at((6.65, 1.75)).label("C")
    d += elm.Line().at((0, 0)).to((6, 0))
    # 绕行方向（顺时针一圈）
    d += elm.Arrow().at((1.0, 0.7)).to((1.0, 2.8))
    d += elm.Arrow().at((1.0, 2.8)).to((5.0, 2.8))
    d += elm.Arrow().at((5.0, 2.8)).to((5.0, 0.7))
    d += elm.Arrow().at((5.0, 0.7)).to((1.0, 0.7))
    d += elm.Label().at((3.0, 1.75)).label("绕行方向")
    # 各元件端点极性标记
    d += elm.Label().at((-0.35, 3.05)).label("+")
    d += elm.Label().at((-0.35, 0.45)).label("−")
    d += elm.Label().at((0.6, 3.9)).label("+")
    d += elm.Label().at((5.4, 3.9)).label("−")
    d += elm.Label().at((6.35, 3.05)).label("+")
    d += elm.Label().at((6.35, 0.45)).label("−")
    # 底部记账说明
    d += elm.Label().at((3.0, -0.75)).label("按绕行方向记账：A −6（升 6 V）、B +2（降 2 V）、C +4（降 4 V）")
    d += elm.Label().at((3.0, -1.3)).label("KVL：−6 + 2 + 4 = 0")
save(d, "lec02_fig5_kvl")

# ---------------------------------------------------------------------
print()
print("=== 图 6：含受控源单回路（3 V + 1 Ω + CCVS[2 Ω]） ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.SourceV().at((0, 0)).to((0, 3))
    d += elm.Label().at((-0.9, 1.5)).label("3 V")
    d += elm.Line().at((0, 3)).to((1.2, 3))
    d += elm.Arrow().at((0.2, 3)).to((1.2, 3)).label("$i$（回路电流）", loc="top")
    d += elm.Resistor().at((1.2, 3)).to((3.8, 3)).label("1 Ω", loc="top")
    d += elm.Line().at((3.8, 3)).to((5, 3))
    d += elm.SourceControlledV().at((5, 3)).down().length(3)
    d += elm.Label().at((6.0, 1.5)).label("CCVS")
    d += elm.Label().at((6.1, 2.5)).label("(系数 2 Ω)")
    d += elm.Line().at((5, 0)).to((0, 0))
    d += elm.Label().at((2.6, -0.8)).label("解得：$i$ = 1 A，$u_R$ = 1 V，受控源电压 2 V")
    d += elm.Label().at((2.6, -1.35)).label("功率账：3 = 1 + 2 W（受控源在吸收）")
save(d, "lec02_fig6_ccvs")

# ---------------------------------------------------------------------
print()
print("=== 图 7：单结点对（2 mA 源并联两只 1 kΩ） ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.SourceI().at((0, 0)).to((0, 3))
    d += elm.Line().at((0, 3)).to((5, 3))
    d += elm.Arrow().at((0.2, 3)).to((1.4, 3)).label("2 mA（入）", loc="top")
    d += elm.Resistor().at((2.5, 3)).to((2.5, 0))
    d += elm.Resistor().at((5, 3)).to((5, 0))
    d += elm.Line().at((0, 0)).to((5, 0))
    d += elm.Dot().at((2.5, 3))
    d += elm.Dot().at((2.5, 0))
    d += elm.Arrow().at((2.5, 2.95)).to((2.5, 2.35))
    d += elm.Arrow().at((5, 2.95)).to((5, 2.35))
    d += elm.Label().at((3.15, 1.4)).label("1 kΩ")
    d += elm.Label().at((5.65, 1.4)).label("1 kΩ")
    d += elm.Label().at((2.95, 2.65)).label("$i_1$")
    d += elm.Label().at((5.45, 2.65)).label("$i_2$")
    d += elm.Label().at((2.5, -0.75)).label("KCL（上结点）：2 mA = $i_1$ + $i_2$")
    d += elm.Label().at((2.5, -1.3)).label("解得：$u$ = 1 V，$i_1$ = $i_2$ = 1 mA")
save(d, "lec02_fig7_node_pair")

# ---------------------------------------------------------------------
print()
print("=== 图 8：实际电池带载（6 V + 内阻 1 kΩ + 负载 2 kΩ + 1 kΩ） ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.BatteryCell().at((0, 0)).to((0, 3))
    d += elm.Label().at((-0.75, 1.5)).label("6 V")
    d += elm.Line().at((0, 3)).to((5, 3))
    d += elm.Label().at((2.8, 3.55)).label("端电压 4.5 V（不是 6 V）")
    d += elm.Resistor().at((5, 3)).to((5, 1.6))
    d += elm.Label().at((6.2, 2.3)).label("内阻 1 kΩ")
    d += elm.Line().at((5, 1.6)).to((5, 0))
    d += elm.Resistor().at((5, 0)).to((2.5, 0)).label("2 kΩ", loc="bottom")
    d += elm.Resistor().at((2.5, 0)).to((0, 0)).label("1 kΩ", loc="bottom")
    d += elm.Label().at((2.5, -1.0)).label("回路电流 1.5 mA：内阻把端电压拉低 1.5 V")
    d += elm.Label().at((2.5, -1.55)).label("功率账：9 = 2.25 + 4.5 + 2.25 mW（源 = 内阻 + 2k + 1k）")
save(d, "lec02_fig8_battery_load")

print()
print("[DONE] 六张补充图全部生成完成。")