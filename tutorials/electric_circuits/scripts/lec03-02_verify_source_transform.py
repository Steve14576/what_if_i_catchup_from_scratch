# =====================================================================
# lec03-02 电源的两种模型互换：等效性扫描、电池账重算、内部功率对比（第 03 讲 §2）
# 规模纪律：总耗时 < 10 秒（纯算术 + 一张小图）。
# 方法：
#   实验 1：等效性扫描——V 模型（6 V 串 1 kΩ）与 I 模型（6 mA 并 1 kΩ）
#           对外端口电流 i(u) = (6-u)/1000 与 6 mA - u/1000 逐点一致（残差 0）。
#   实验 2：结 02 的账——电池带载（6 V + 1 kΩ 内阻 + 3 kΩ 负载）用 I 模型
#           重算：u = 6 mA x (1k∥3k) = 4.5 V，与 02 讲同答案。
#   实验 3：内部账对比——V 模型内阻损耗 2.25 mW、源出力 9 mW；
#           I 模型内阻损耗 20.25 mW、源出力 27 mW；负载两侧都是 6.75 mW。
#   并生成 figures/lec03_fig3_source_transform.svg 与 .png（两种模型互换）。
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
print("=== 实验 1：等效性扫描（V 模型 vs I 模型） ===")
US, Rs = 6.0, 1000.0
IS = US / Rs
print("  互换参数：I_S = U_S / R_s = %.1f mA，R_s 不动。" % (IS * 1e3))
worst = 0.0
for u in [-3.0, 0.0, 3.0, 4.5, 6.0, 9.0]:
    i_v = (US - u) / Rs        # V 模型对外给出（流入外电路）的电流
    i_i = IS - u / Rs          # I 模型对外给出的电流
    worst = max(worst, abs(i_v - i_i))
    print("  端口 u = %5.1f V：V 模型 i = %+7.3f mA；I 模型 i = %+7.3f mA"
          % (u, i_v * 1e3, i_i * 1e3))
print("  全扫描最大差 = %.2e mA -> 对外伏安关系完全相同" % (worst * 1e3))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：结 02 的账——电池带载用 I 模型重算 ===")
RL = 3000.0
R_par = Rs * RL / (Rs + RL)          # 1k 并 3k = 0.75k
u_load = IS * R_par                  # 6m x 0.75k = 4.5 V
i_load = u_load / RL                 # 1.5 mA
print("  6 mA 灌进 1k∥3k = %.2f kΩ：u = %.1f V；负载电流 = %.1f mA"
      % (R_par / 1e3, u_load, i_load * 1e3))
u_check = US - Rs * i_load           # 02 讲的老路
print("  02 讲老路复算：u = 6 - 1k x %.1f mA = %.1f V；两条路差 = %.2e V"
      % (i_load * 1e3, u_check, abs(u_load - u_check)))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：内部账对比（等效不等于相同） ===")
p_load = u_load * i_load * 1e3                       # 6.75 mW
p_rs_v = Rs * i_load**2 * 1e3                        # V 模型内阻
p_src_v = US * i_load * 1e3                          # V 模型源出力
i_rs_i = u_load / Rs                                 # I 模型内阻电流 4.5 mA
p_rs_i = u_load * i_rs_i * 1e3                       # I 模型内阻损耗
p_src_i = u_load * IS * 1e3                          # I 模型源出力
print("  V 模型：源出力 %.2f mW = 内阻 %.2f + 负载 %.2f（残差 %.2e）"
      % (p_src_v, p_rs_v, p_load, p_src_v - p_rs_v - p_load))
print("  I 模型：源出力 %.2f mW = 内阻 %.2f + 负载 %.2f（残差 %.2e）"
      % (p_src_i, p_rs_i, p_load, p_src_i - p_rs_i - p_load))
print("  -> 负载拿到的完全一样（%.2f mW）；内部损耗与源出力完全不同。" % p_load)

# ---------------------------------------------------------------------
print()
print("=== 实验 4：两支路并联的合并（含源支路的组合用法） ===")
# 支路 1：6 V 串 1 kΩ；支路 2：3 mA 并 1 kΩ；两支路并联
I2 = 3e-3
i_oc = US / Rs + I2                  # 短路电流：0.009 A
R_par2 = 1 / (1 / Rs + 1 / Rs)       # 0.5 kΩ
u_oc = i_oc * R_par2                # 开路电压：4.5 V
print("  合并：短路电流 6 + 3 = %.1f mA；内阻 1k∥1k = %.2f kΩ -> 等效 %.1f V 串 %.2f kΩ"
      % (i_oc * 1e3, R_par2 / 1e3, u_oc, R_par2 / 1e3))
worst = 0.0
for u in [0.0, 1.0, 4.5, 9.0]:
    i_b1 = (US - u) / Rs             # 支路 1 对外提供
    i_b2 = I2 - u / Rs               # 支路 2 对外提供
    i_comb = i_oc - u / R_par2       # 合并模型对外提供
    worst = max(worst, abs((i_b1 + i_b2) - i_comb))
    print("  u = %4.1f V：逐支路求和 i = %.3f mA；合并模型 i = %.3f mA"
          % (u, (i_b1 + i_b2) * 1e3, i_comb * 1e3))
print("  全扫描最大差 = %.2e mA -> 合并正确" % (worst * 1e3))

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：电源的两种模型互换 ===")
with schemdraw.Drawing(show=False) as d:
    # (a) V 模型：a 端 -> 6 V 源 -> 1 kΩ -> b 端
    d += elm.Dot().at((0, 3.4))
    d += elm.Label().at((0.35, 3.55)).label("a")
    d += elm.SourceV().at((0, 1.4)).up().length(2.0)
    d += elm.Label().at((-0.85, 2.4)).label("6 V")
    d += elm.Resistor().at((0, 1.4)).to((0, -0.4))
    d += elm.Label().at((1.5, 0.5)).label("$R_s$ = 1 kΩ")
    d += elm.Dot().at((0, -0.4))
    d += elm.Label().at((0.35, -0.55)).label("b")
    d += elm.Label().at((0.1, -1.15)).label("(a) 电压源 + 串电阻")
    # 中部互换标注
    d += elm.Label().at((3.0, 2.3)).label("互换：$U_S = I_S\\,R_s$")
    d += elm.Label().at((3.0, 1.75)).label("（箭头指向 a 端）")
    d += elm.Label().at((3.0, 0.6)).label("$\\Longleftrightarrow$")
    # (b) I 模型：a 端 -> 6 mA 源 ∥ 1 kΩ -> b 端
    d += elm.Dot().at((6.6, 3.0))
    d += elm.Label().at((6.95, 3.15)).label("a")
    d += elm.Line().at((6.6, 3.0)).to((6.6, 2.6))
    d += elm.Line().at((6.0, 2.6)).to((7.2, 2.6))
    d += elm.Dot().at((6.6, 2.6))
    d += elm.SourceI().at((6.0, 0.4)).up().length(2.2)
    d += elm.Label().at((5.15, 1.5)).label("6 mA")
    d += elm.Resistor().at((7.2, 2.6)).to((7.2, 0.4))
    d += elm.Label().at((8.15, 1.5)).label("$R_s$ = 1 kΩ")
    d += elm.Line().at((6.0, 0.4)).to((7.2, 0.4))
    d += elm.Dot().at((6.6, 0.4))
    d += elm.Line().at((6.6, 0.4)).to((6.6, 0.0))
    d += elm.Dot().at((6.6, 0.0))
    d += elm.Label().at((6.95, -0.15)).label("b")
    d += elm.Label().at((6.6, -0.85)).label("(b) 电流源 + 并电阻")
save_stem = "lec03_fig3_source_transform"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec03-02 完成。")