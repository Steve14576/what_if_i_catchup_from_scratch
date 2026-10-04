# =====================================================================
# lec17-01 磁路与铁心线圈：主例全账、气隙杠杆、4.44、饱和演示
#          （第 17 讲 §1-§4 数值实验；图 1 铁心线圈、图 2 B-H、图 3 4.44）
# 规模纪律：总耗时 < 10 秒（解析计算 + 一维求根 + 三张图）。
#
# 主例：铁心线圈 N = 1000 匝、i = 1 A（F = 1000 A）；铁心 l = 40 cm、
#   S = 4 cm^2、mu_r = 2500（mu = pi x 1e-3）；气隙 delta = 1 mm。
#   R铁 = 1e6/pi、R气 = 6.25 x R铁、R总 = 7.25e6/pi；
#   Phi = pi/7250 = 0.4333 mWb；B = 1.0832 T；
#   安匝账：H铁 x l = 137.9、H气 x delta = 862.1（和 = 1000）；
#   L = N^2/R总 = 0.4333 H。
#   无气隙线性外推：B = 7.85 T（远超饱和——线性模型失效的现场）。
# 4.44 例：S = 10 cm^2、Bm = 1 T、f = 50 Hz -> Phi_m = 1 mWb；
#   U = 220 V 需要 N = 220/(4.44 x 50 x 1e-3) = 990 匝。
# 饱和演示（tanh 平滑模型，当场选取的示意模型）：F 1000->2000，
#   曲线口径 B 1.052 -> 1.596 T（线性外推会得 2.17——不存在）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

mu0 = 4 * np.pi * 1e-7

# ---------------------------------------------------------------------
print("=== 实验 1：主例磁路全账 ===")
N, I0 = 1000, 1.0
F = N * I0
l, S, mur, delta = 0.4, 4e-4, 2500.0, 1e-3
mu = mur * mu0
Rfe = l / (mu * S)
Rgap = delta / (mu0 * S)
Rt = Rfe + Rgap
Phi = F / Rt
B = Phi / S
Hfe = B / mu
Hgap = B / mu0
L = N ** 2 / Rt
print("  F = Ni = %.0f A；mu = mu_r mu0 = pi x 1e-3（2500 与 4pi 的巧遇）" % F)
print("  R铁 = %.4e 1/H；R气 = %.4e（= %.2f x R铁）；R总 = %.4e" % (Rfe, Rgap, Rgap / Rfe, Rt))
print("  Phi = %.4e Wb = %.2f mWb；B = %.4f T" % (Phi, Phi * 1e3, B))
print("  安匝账：H铁 x l = %.1f A，H气 x delta = %.1f A（和 = %.0f）"
      % (Hfe * l, Hgap * delta, Hfe * l + Hgap * delta))
print("  L = N^2/R总 = %.4f H" % L)
Phi0 = F / Rfe
print("  无气隙线性外推：Phi = %.2f mWb -> B = %.2f T（远超饱和——线性模型失效）"
      % (Phi0 * 1e3, Phi0 / S))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：气隙杠杆——磁阻份额随 delta 线性上升 ===")
for d in [0.5e-3, 1e-3, 2e-3, 4e-3]:
    Rg = d / (mu0 * S)
    print("  delta = %.1f mm：R气/R铁 = %.3f（= mu_r x delta/l）；Phi = %.3f mWb"
          % (d * 1e3, Rg / Rfe, F / (Rfe + Rg) * 1e3))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：4.44 公式的正弦积分验证 ===")
f = 50.0
Phim = 1e-3
NN = 1000
w = 2 * np.pi * f
t = np.linspace(0, 1 / f, 20001)
phi_t = Phim * np.sin(w * t)
u_num = NN * np.gradient(phi_t, t, edge_order=2)
u_exact = NN * w * Phim * np.cos(w * t)
U_eff = np.max(u_num) / np.sqrt(2)
print("  数值微分 vs 解析（N dPhi/dt）：max 偏差 = %.2e V" % np.max(np.abs(u_num - u_exact)))
print("  峰值 Um = 2 pi f N Phi_m = %.2f V；有效值 U = %.2f V（= 4.4429 f N Phi_m）"
      % (NN * w * Phim, U_eff))
print("  反解：220 V / 50 Hz / Bm = 1 T（S = 10 cm^2）需要 N = %.1f 匝（工程约取 990~1000）"
      % (220 / (2 * np.pi / np.sqrt(2) * f * 1e-3)))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：饱和演示（tanh 平滑模型，当场选取） ===")
Bs, mur0 = 1.6, 2500.0
def H_of_B(Bv):
    return (Bs / (mu0 * mur0)) * np.arctanh(np.clip(Bv / Bs, 0, 0.999999))
def F_of_B(Bv):
    return H_of_B(Bv) * l + (Bv / mu0) * delta
def solve_B(Fv):
    lo, hi = 1e-6, Bs * 0.9999
    for _ in range(120):
        mid = (lo + hi) / 2
        if F_of_B(mid) < Fv:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
B1000 = solve_B(1000)
B2000 = solve_B(2000)
print("  F = 1000：曲线口径 B = %.3f T（线性口径曾给 1.083）" % B1000)
print("  F = 2000：曲线口径 B = %.3f T（电流翻倍、磁通不再翻倍；线性外推 2.17 T 不存在）" % B2000)

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：铁心线圈示意（含气隙与绕组） ===")
with schemdraw.Drawing(show=False) as d:
    # 矩形磁路中心线：左臂含绕组、右臂含气隙
    d += elm.Line().at((0, 0)).to((3, 0))
    d += elm.Line().at((3, 0)).to((3, 0.9))
    d += elm.Line().at((3, 1.1)).to((3, 2.0))
    d += elm.Line().at((3, 2.0)).to((0, 2.0))
    d += elm.Line().at((0, 2.0)).to((0, 1.35))
    d += elm.Inductor().at((0, 1.35)).down().length(0.7)
    d += elm.Line().at((0, 0.65)).to((0, 0))
    # 绕组与电流
    d += elm.Arrow().at((-0.75, 0.8)).to((-0.75, 1.2))
    d += elm.Label().at((-1.05, 1.0)).label("$i$")
    d += elm.Label().at((-0.95, 1.75)).label("$N$ 匝", fontsize=11)
    # 气隙标注
    d += elm.Label().at((3.35, 1.0)).label("$\\delta$", fontsize=12)
    d += elm.Label().at((3.7, 0.55)).label("气隙", fontsize=10)
    # 磁通标注（上臂箭头）
    d += elm.Arrow().at((1.1, 2.0)).to((1.8, 2.0))
    d += elm.Label().at((1.35, 2.3)).label("$\\Phi$", fontsize=12)
    d += elm.Label().at((1.5, 1.05)).label("铁心", fontsize=11)
    d += elm.Label().at((0.85, -0.55)).label("铁心：平均路径长 $l$、截面 $S$", fontsize=10)

save_stem = "lec17_fig1_circuit"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：B-H 曲线与饱和 ===")
fig, ax = plt.subplots(figsize=(8.6, 4.8))
Hv = np.linspace(0, 5000, 800)
Bv = Bs * np.tanh(mu0 * mur0 * Hv / Bs)
ax.plot(Hv, Bv, color="#1f5fa8", lw=2.4, label="真实 B-H（示意：tanh 平滑饱和）")
ax.plot(Hv, np.minimum(mu0 * mur0 * Hv, 6), color="#c0392b", lw=1.6, ls="--", label="线性模型（mu_r = 2500）")
ax.axhline(Bs, color="#999999", lw=1.0, ls=":")
ax.text(4200, Bs + 0.06, "饱和 $B_s$ = 1.6 T", fontsize=10, color="#666666")
for Hpt, Bpt, cc, tag in [(H_of_B(B1000), B1000, "#2e7d32", "F = 1000"), (H_of_B(B2000), B2000, "#e67e22", "F = 2000")]:
    ax.plot([Hpt], [Bpt], "o", color=cc, ms=6)
    ax.annotate(tag, xy=(Hpt, Bpt), xytext=(Hpt + 260, Bpt - 0.28), fontsize=10, color=cc,
                arrowprops=dict(arrowstyle="->", color=cc))
ax.set_xlabel("磁场强度 $H$ / (A/m)")
ax.set_ylabel("磁感应强度 $B$ / T")
ax.set_title("铁磁材料的 B-H 曲线：线性段 -> 膝点 -> 饱和（示意图）", fontsize=11)
ax.legend(fontsize=9, loc="lower right")
ax.set_ylim(0, 3.2)
ax.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec17_fig2_bh"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：4.44 的来历（Phi 正弦 -> u 余弦） ===")
fig, ax1 = plt.subplots(figsize=(9.6, 4.4))
ax1.plot(t * 1e3, phi_t * 1e3, color="#1f5fa8", lw=2.2, label="$\\Phi(t)$ / mWb（左轴）")
ax1.set_xlabel("时间 $t$ / ms")
ax1.set_ylabel("磁通 $\\Phi$ / mWb", color="#1f5fa8")
ax1.set_ylim(-1.4, 1.4)
ax1.grid(alpha=0.3)
ax2 = ax1.twinx()
ax2.plot(t * 1e3, u_exact, color="#c0392b", lw=2.2, label="$u = N\\,d\\Phi/dt$ / V（右轴）")
ax2.set_ylabel("电压 $u$ / V", color="#c0392b")
ax2.set_ylim(-420, 420)
ax2.axhline(314.16, color="#999999", lw=1.0, ls=":")
ax2.text(8.5, 330, "峰值 314 V -> 有效值 222 V = 4.44 f N $\\Phi_m$", fontsize=10, color="#666666")
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, fontsize=9, loc="lower left")
ax1.set_title("电压是磁通的变化率：$\\Phi$ 正弦 -> $u$ 余弦、峰值 $2\\pi f N\\Phi_m$", fontsize=11)
plt.tight_layout()
save_stem = "lec17_fig3_flux44"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec17-01 完成。")