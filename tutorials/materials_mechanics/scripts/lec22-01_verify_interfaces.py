# =====================================================================
# lec22-01 第 22 讲《与后续的接口》数字核对与配图（末讲）
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 末讲不再引入新公式，而是量化"本课各条基本假设在哪里开始失效"：
#   EXP1 剪切变形占比（Timoshenko 认识层）：w_s/w_b 随 L/h 变化 -> 细长梁界限
#   EXP2 应力集中（均匀假设失效）：有限宽板中心圆孔的 k_t 与峰值应力
#   EXP3 纵横弯曲放大系数 1/(1-P/P_cr)（小变形/线性叠加失效）
#   EXP4 有限元收敛（连续场离散逼近）：线性单元最大误差随单元数 O(h^2) 下降
# 出图（编号按正文出现顺序）：
#   lec22_fig1_map            基本假设 -> 下游方向的松绑地图
#   lec22_fig2_limits         两条假设的失效边界（细长比、应力集中）
#   lec22_fig3_fem_amplify    有限元收敛与纵横弯曲放大
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
# 注意：mathtext 内不等式写 \leq，不写 \le（matplotlib 不支持）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

RED = "#c0392b"
BLUE = "#2b6cb0"
GREEN = "#2f855a"
GREY = "#718096"
ORANGE = "#c05621"


def savefig(fig, stem):
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, stem + ".svg"))
    fig.savefig(os.path.join(FIGDIR, stem + ".png"), dpi=200)
    plt.close(fig)
    print("[OK] figures/%s.svg 与 .png 已生成。" % stem)


# ---------------------------------------------------------------------
print("=== 数字核对：第 22 讲 ===")

# EXP1 剪切变形占比（矩形截面，mu=0.3，kappa=5/6）
mu = 0.3
EG = 2.0 * (1.0 + mu)
print("  EXP1 剪切变形相对弯曲变形的占比 w_s/w_b = 11.52*(I/(A L^2))*(E/G)（矩形）：")
for ratio in [20.0, 10.0, 5.0, 2.0]:
    hL = 1.0 / ratio
    I_over_A = hL ** 2 / 12.0     # I/A = h^2/12 -> 与 h/L 的平方成正比
    ws_wb = 11.52 * I_over_A * EG
    print("        L/h=%4.0f -> w_s/w_b = %.4f（%.2f%%）%s"
          % (ratio, ws_wb, ws_wb * 100, "  <-- 工程上细长梁界限" if ratio == 10 else ""))

# EXP2 应力集中（有限宽板中心圆孔）
W, d, t, P = 100.0, 30.0, 10.0, 100.0e3
kt = 2.0 + (1.0 - d / W) ** 3
sig_net = P / ((W - d) * t)
sig_max = kt * sig_net
sig_naive = P / (W * t)
print("  EXP2 应力集中（W=%.0f, d=%.0f, t=%.0f, P=%.0f kN）：" % (W, d, t, P / 1e3))
print("        k_t=2+(1-d/W)^3=%.3f；净截面 sigma_net=%.2f MPa -> sigma_max=%.2f MPa" % (kt, sig_net, sig_max))
print("        若按均匀假设估 sigma=P/(Wt)=%.2f MPa，峰值是其 %.2f 倍" % (sig_naive, sig_max / sig_naive))

# EXP3 纵横弯曲放大系数
print("  EXP3 纵横弯曲放大系数 1/(1-P/P_cr)：")
for r in [0.0, 0.25, 0.5, 0.75, 0.9]:
    print("        P/P_cr=%.2f -> 放大系数 = %.3f" % (r, 1.0 / (1.0 - r)))

# EXP4 有限元收敛（线性单元逼近 sin(pi x)）
print("  EXP4 有限元收敛（线性单元插值 sin(pi*x) 的最大误差）：")
prev = None
for n in [4, 8, 16, 32]:
    xs = np.linspace(0, 1, n + 1)
    exact = np.sin(np.pi * xs)
    xf = np.linspace(0, 1, 2001)
    approx = np.interp(xf, xs, exact)
    err = np.max(np.abs(np.sin(np.pi * xf) - approx))
    if prev is None:
        print("        n=%2d -> max_err=%.5f" % (n, err))
    else:
        print("        n=%2d -> max_err=%.5f（误差比 %.2f，应接近 4 = O(h^2)）" % (n, err, prev / err))
    prev = err


# ---------------------------------------------------------------------
print()
print("=== 图 1：基本假设 -> 下游方向的松绑地图 ===")
fig, ax = plt.subplots(figsize=(10.6, 5.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis("off")
left = ["连续、均匀、各向同性", "平面假设（平截面）", "小变形假设", "线弹性（胡克定律）"]
right = ["弹性力学 / 塑性力学", "结构力学 / 有限元", "几何非线性分析", "断裂力学 / 损伤力学"]
y0 = 6.4
ax.text(1.9, 7.4, "本课的基本假设", ha="center", fontsize=11, weight="bold", color=BLUE)
ax.text(8.1, 7.4, "下游方向", ha="center", fontsize=11, weight="bold", color=GREEN)
for i, (L, R) in enumerate(zip(left, right)):
    y = y0 - i * 1.35
    ax.add_patch(Rectangle((0.2, y - 0.42), 3.4, 0.84, fc="#e7f0fb", ec=BLUE, lw=1.4))
    ax.text(1.9, y, L, ha="center", fontsize=10)
    ax.add_patch(Rectangle((6.4, y - 0.42), 3.4, 0.84, fc="#e8f5e9", ec=GREEN, lw=1.4))
    ax.text(8.1, y, R, ha="center", fontsize=10)
    ax.annotate("", xy=(6.35, y), xytext=(3.65, y),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.6))
ax.text(5.0, 0.6, "同一套力学原理，沿维度、尺度、非线性三个方向扩展",
        ha="center", fontsize=9.5, color=GREY)
savefig(fig, "lec22_fig1_map")


# ---------------------------------------------------------------------
print()
print("=== 图 2：两条假设的失效边界 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.2, 4.6))

ratio_arr = np.linspace(2, 25, 200)
ws_arr = 11.52 * (1.0 / ratio_arr) ** 2 / 12.0 * EG
a1.plot(ratio_arr, ws_arr * 100, color=BLUE, lw=2.4)
a1.axhline(5, color=RED, ls="--", lw=1.4)
a1.text(24, 6.0, "5% 参考线", ha="right", fontsize=9, color=RED)
a1.axvline(10, color=GREY, ls=":", lw=1.2)
a1.text(10.4, 18, r"$L/h=10$", fontsize=9.5, color=GREY)
a1.set_xlabel(r"跨高比 $L/h$", fontsize=11)
a1.set_ylabel(r"剪切变形占比 $w_s/w_b$ / %", fontsize=11)
a1.set_title(r"(a) 梁理论：$L/h$ 越小剪切变形越不可忽略", fontsize=10.5)

dd = np.linspace(0.01, 0.8, 200)
kt_arr = 2.0 + (1.0 - dd) ** 3
a2.plot(dd, kt_arr, color=ORANGE, lw=2.4)
a2.set_xlabel(r"孔径比 $d/W$", fontsize=11)
a2.set_ylabel(r"应力集中系数 $k_t$", fontsize=11)
a2.set_ylim(1.9, 3.1)
a2.set_title(r"(b) 应力集中：圆形孔 $k_t=2+(1-d/W)^3$", fontsize=10.5)
savefig(fig, "lec22_fig2_limits")


# ---------------------------------------------------------------------
print()
print("=== 图 3：有限元收敛与纵横弯曲放大 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.2, 4.6))

ns = np.array([4, 8, 16, 32, 64])
errs = []
for n in ns:
    xs = np.linspace(0, 1, n + 1)
    xf = np.linspace(0, 1, 2001)
    approx = np.interp(xf, xs, np.sin(np.pi * xs))
    errs.append(np.max(np.abs(np.sin(np.pi * xf) - approx)))
errs = np.array(errs)
a1.loglog(ns, errs, "o-", color=BLUE, lw=2)
ref = errs[0] * (ns[0] / ns) ** 2
a1.loglog(ns, ref, "--", color=RED, lw=1.4)
a1.text(9, errs[0] * 0.25, r"参考斜率 $-2$（即 $O(h^2)$）", fontsize=9, color=RED)
a1.set_xlabel(r"单元数 $n$", fontsize=11)
a1.set_ylabel(r"最大误差", fontsize=11)
a1.set_title("(a) 有限元：网格加密，误差按 $O(h^2)$ 下降", fontsize=10.5)

rr = np.linspace(0, 0.95, 200)
a2.plot(rr, 1.0 / (1.0 - rr), color=GREEN, lw=2.4)
a2.set_xlabel(r"轴压力比 $P/P_{cr}$", fontsize=11)
a2.set_ylabel(r"挠度放大系数", fontsize=11)
a2.set_ylim(0, 12)
a2.set_title(r"(b) 纵横弯曲：$1/(1-P/P_{cr})$，接近临界时趋于无穷", fontsize=10.5)
savefig(fig, "lec22_fig3_fem_amplify")

print()
print("[DONE] 第 22 讲数字核对与三张图全部完成。")