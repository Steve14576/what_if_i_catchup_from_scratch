# =====================================================================
# lec03-03 Y-Δ 变换、桥式化简与含受控源单口（第 03 讲 §3 / §4）
# 规模纪律：总耗时 < 10 秒（纯算术 + 三张小图）。
# 方法：
#   实验 1：Y-Δ 公式双向核对——对称情形 Δ(3k,3k,3k) 换 Y(1k,1k,1k)；
#           非对称情形用"端口电阻测试"（1-2、2-3、3-1 三对端口）双向验证。
#   实验 2：桥式化简——R1=1k(左上) R2=2k(左下) R3=3k(右上) R4=3k(右下)
#           R5=3k(中) 求 A-B 端口等效电阻：Y-Δ 路线 2.2 kΩ；
#           直接结点方程核对；扫 u 验证端口伏安一致（i = u/2.2k）。
#   实验 3：含受控源单口——R = 2 kΩ 并 VCCS（g = 0.5 mS）：R_in = 1 kΩ；
#           扫 u 验证 u-i 是一条过原点直线（斜率 1 mS）。
#   并生成 figures/lec03_fig4_wye_delta.svg/.png、lec03_fig5_bridge.svg/.png、
#       lec03_fig6_controlled_port.svg/.png。
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
print("=== 实验 1：Y-Δ 公式双向核对 ===")
# 对称情形：Δ(3k) -> Y(1k)
R_d = 3000.0
R_y = R_d / 3.0
print("  对称：R_Y = R_D/3 = %.1f kΩ" % (R_y / 1e3))


def y_to_delta(R1, R2, R3):
    s = R1 * R2 + R2 * R3 + R3 * R1
    return s / R3, s / R1, s / R2   # 返回 (R12, R23, R31)


def port_res_y(R1, R2, R3, a, b):
    # Y 网络端口 a-b 电阻：两条臂直串（第三臂悬空）
    arms = {1: R1, 2: R2, 3: R3}
    return arms[a] + arms[b]


def port_res_delta(R12, R23, R31, a, b):
    edges = {(1, 2): R12, (2, 3): R23, (1, 3): R31}
    direct = edges[(min(a, b), max(a, b))]
    other = 6 - a - b                    # 第三个结点
    path = edges[(min(a, other), max(a, other))] + edges[(min(b, other), max(b, other))]
    return direct * path / (direct + path)


pairs = [(1, 2), (2, 3), (1, 3)]
for (R1, R2, R3, tag) in [(1000.0, 2000.0, 3000.0, "非对称 (1k,2k,3k)"),
                          (1000.0, 1000.0, 1000.0, "对称 (1k,1k,1k)")]:
    R12, R23, R31 = y_to_delta(R1, R2, R3)
    print("  %s：Y -> Δ 得 (%.4f, %.4f, %.4f) kΩ" % (tag, R12 / 1e3, R23 / 1e3, R31 / 1e3))
    worst = 0.0
    for (a, b) in pairs:
        py = port_res_y(R1, R2, R3, a, b)
        pd = port_res_delta(R12, R23, R31, a, b)
        worst = max(worst, abs(py - pd))
    print("     三对端口电阻最大差 = %.2e kΩ -> 双向公式自洽" % (worst / 1e3))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：桥式化简（A-B 端口等效电阻） ===")
# 结点：A 左、B 右、C 上、D 下；R1=A-C  R2=A-D  R3=C-B  R4=D-B  R5=C-D
R1, R2, R3, R4, R5 = 1000.0, 2000.0, 3000.0, 3000.0, 3000.0
# 路线 1：Δ(C,D,B) = (R5, R4, R3) -> Y
sum3 = R5 + R4 + R3
y_c = R5 * R3 / sum3      # 在 C 的臂：触及 C 的两条边 R5(C-D) 与 R3(C-B)
y_d = R5 * R4 / sum3      # 在 D 的臂
y_b = R3 * R4 / sum3      # 在 B 的臂
R_an = (R1 + y_c) * (R2 + y_d) / (R1 + y_c + R2 + y_d)
R_ab_y = R_an + y_b
print("  Y-Δ 路线：Y 臂 = (%.1f, %.1f, %.1f) kΩ；R_AB = %.2f kΩ"
      % (y_c / 1e3, y_d / 1e3, y_b / 1e3, R_ab_y / 1e3))
# 路线 2：直接结点方程（VB = 0，VA = u）：对 C、D 列 KCL
Amat = np.array([[1 / R1 + 1 / R3 + 1 / R5, -1 / R5],
                 [-1 / R5, 1 / R2 + 1 / R4 + 1 / R5]])
worst = 0.0
for u in [1.0, 2.0, 5.0, 11.0, 20.0]:
    rhs = np.array([u / R1, u / R2])
    Vc, Vd = np.linalg.solve(Amat, rhs)
    i_total = (u - Vc) / R1 + (u - Vd) / R2
    i_eq = u / R_ab_y
    worst = max(worst, abs(i_total - i_eq) / u)
    print("  u = %5.1f V：原桥电流 i = %.6f mA；等效 2.2 kΩ 电流 = %.6f mA"
          % (u, i_total * 1e3, i_eq * 1e3))
print("  端口伏安一致（复阻抗口径最大相对差 = %.2e）" % worst)
Vc11, Vd11 = np.linalg.solve(Amat, np.array([11 / R1, 11 / R2]))
print("  验算样例：u = 11 V 时 V_C = %.0f V、V_D = %.0f V；i = %.0f mA"
      % (Vc11, Vd11, ((11 - Vc11) / R1 + (11 - Vd11) / R2) * 1e3))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：含受控源单口（R = 2 kΩ 并 VCCS g = 0.5 mS） ===")
Rr, g = 2000.0, 0.5e-3
worst = 0.0
for u in [1.0, 2.0, 4.0, 8.0]:
    i = u / Rr + g * u
    worst = max(worst, abs(i - u / 1000.0))
    print("  u = %4.1f V：i = u/2k + g x u = %.3f mA" % (u, i * 1e3))
print("  R_in = u/i = 1 kΩ（最大偏差 %.2e mA）" % (worst * 1e3))
print("  对照：若只把 2 kΩ 当输入电阻（无视受控源），误差 100%%。".replace("%%", "%"))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：平衡电桥（中支路可拿掉） ===")
# R1=A-C 1k；R3=C-B 2k；R2=A-D 2k；R4=D-B 4k；R5=C-D 1k（比例 R1/R3 = R2/R4 -> 平衡）
rb1, rb3, rb2, rb4, rb5 = 1000.0, 2000.0, 2000.0, 4000.0, 1000.0
Amat_b = np.array([[1 / rb1 + 1 / rb3 + 1 / rb5, -1 / rb5],
                   [-1 / rb5, 1 / rb2 + 1 / rb4 + 1 / rb5]])
Vcb, Vdb = np.linalg.solve(Amat_b, np.array([1.0 / rb1, 1.0 / rb2]))
print("  u = 1 V 时：V_C = %.4f V，V_D = %.4f V；差 = %.2e V" % (Vcb, Vdb, abs(Vcb - Vdb)))
R_ab_bal = (rb1 + rb3) * (rb2 + rb4) / (rb1 + rb3 + rb2 + rb4)
print("  拿掉中支路：(R1+R3)∥(R2+R4) = %.1f kΩ" % (R_ab_bal / 1e3))
worst = 0.0
for u in [1.0, 5.0, 10.0]:
    Vc_u, Vd_u = np.linalg.solve(Amat_b, np.array([u / rb1, u / rb2]))
    i_orig = (u - Vc_u) / rb1 + (u - Vd_u) / rb2
    i_simp = u / R_ab_bal
    worst = max(worst, abs(i_orig - i_simp))
print("  三点扫描原桥与化简结果最大差 = %.2e mA -> 中支路确实可拿掉" % (worst * 1e3))

# ---------------------------------------------------------------------
print()
print("=== 生成图 4：Y-Δ 变换 ===")
with schemdraw.Drawing(show=False) as d:
    # (a) Y
    d += elm.Resistor().at((0, 3)).to((2, 1.5))
    d += elm.Resistor().at((0, 0)).to((2, 1.5))
    d += elm.Resistor().at((4, 1.5)).to((2, 1.5))
    d += elm.Dot().at((0, 3))
    d += elm.Dot().at((0, 0))
    d += elm.Dot().at((4, 1.5))
    d += elm.Dot().at((2, 1.5))
    d += elm.Label().at((-0.45, 3.2)).label("1")
    d += elm.Label().at((-0.45, -0.2)).label("2")
    d += elm.Label().at((4.35, 1.6)).label("3")
    d += elm.Label().at((1.35, 2.7)).label("$R_1$")
    d += elm.Label().at((1.35, 0.3)).label("$R_2$")
    d += elm.Label().at((3.15, 2.0)).label("$R_3$")
    d += elm.Label().at((1.3, -0.75)).label("(a) Y（星形）")
    # (b) Δ
    d += elm.Resistor().at((8, 3)).to((8, 0))
    d += elm.Resistor().at((8, 0)).to((12, 1.5))
    d += elm.Resistor().at((12, 1.5)).to((8, 3))
    d += elm.Dot().at((8, 3))
    d += elm.Dot().at((8, 0))
    d += elm.Dot().at((12, 1.5))
    d += elm.Label().at((7.55, 3.2)).label("1")
    d += elm.Label().at((7.55, -0.2)).label("2")
    d += elm.Label().at((12.35, 1.6)).label("3")
    d += elm.Label().at((7.35, 1.5)).label("$R_{12}$")
    d += elm.Label().at((10.2, 0.24)).label("$R_{23}$")
    d += elm.Label().at((10.2, 2.78)).label("$R_{31}$")
    d += elm.Label().at((9.4, -0.75)).label("(b) Δ（三角形）")
    d += elm.Label().at((6.0, 1.5)).label("对外\n等效")
save_stem = "lec03_fig4_wye_delta"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("=== 生成图 5：桥式电路 ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.Resistor().at((0, 1.5)).to((3, 3))
    d += elm.Resistor().at((3, 3)).to((6, 1.5))
    d += elm.Resistor().at((0, 1.5)).to((3, 0))
    d += elm.Resistor().at((3, 0)).to((6, 1.5))
    d += elm.Resistor().at((3, 3)).to((3, 0))
    d += elm.Dot().at((0, 1.5))
    d += elm.Dot().at((6, 1.5))
    d += elm.Label().at((-0.45, 1.65)).label("A")
    d += elm.Label().at((6.45, 1.65)).label("B")
    d += elm.Label().at((1.2, 2.79)).label("$R_1$")
    d += elm.Label().at((4.8, 2.79)).label("$R_3$")
    d += elm.Label().at((1.2, 0.21)).label("$R_2$")
    d += elm.Label().at((4.8, 0.21)).label("$R_4$")
    d += elm.Label().at((3.75, 1.5)).label("$R_5$")
    d += elm.Dot().at((3, 3))
    d += elm.Dot().at((3, 0))
    d += elm.Label().at((3.0, -0.7)).label("中间这条叫\u201c桥\u201d——求 A-B 端口的等效电阻")
save_stem = "lec03_fig5_bridge"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("=== 生成图 6：含受控源的单口 ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.Dot().at((0, 3.0))
    d += elm.Label().at((0.35, 3.15)).label("a")
    d += elm.Line().at((-0.9, 3.0)).to((0.9, 3.0))
    d += elm.Dot().at((0, 3.0))
    d += elm.Resistor().at((-0.9, 3.0)).to((-0.9, 0.4))
    d += elm.Label().at((-2.3, 1.7)).label("$R$ = 2 kΩ")
    d += elm.SourceControlledI().at((0.9, 3.0)).down().length(2.6)
    d += elm.Label().at((2.15, 2.15)).label("受控电流源")
    d += elm.Label().at((2.15, 1.7)).label("$i = g\\,u$")
    d += elm.Label().at((2.4, 1.25)).label("（$g$ = 0.5 mS）")
    d += elm.Line().at((-0.9, 0.4)).to((0.9, 0.4))
    d += elm.Dot().at((0, 0.4))
    d += elm.Label().at((0.35, 0.2)).label("b")
    d += elm.Label().at((0, -0.45)).label("$u$ = 端口电压，它控制右边的源")
save_stem = "lec03_fig6_controlled_port"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec03-03 完成。")