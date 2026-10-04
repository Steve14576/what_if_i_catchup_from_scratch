# =====================================================================
# lec12-01 二阶电路：RLC 串联放电的三种阻尼（参数、解、形态）
#          （第 12 讲 §1-§4 数值实验；图 1 电路、图 2 三阻尼对比）
# 规模纪律：总耗时 < 10 秒（RK4 dt=1us、三案例 + 两张图）。
#
# 运行例：L = 50 mH、C = 20 uF、u_C(0) = 10 V、i_L(0) = 0；
#   t=0 合上开关，电容经 R、L 放电（串联 RLC 零输入）。
#   特征参数：omega0 = 1/sqrt(LC) = 1000 rad/s；alpha = R/(2L)。
#     欠阻尼 R = 28： alpha = 280，omega_d = 960（7-24-25）；
#     临界   R = 100：alpha = 1000 = omega0；
#     过阻尼 R = 125：alpha = 1250，根 s1 = -500、s2 = -2000。
#   解析解：
#     欠：u = e^(-280t)[10 cos960t + (35/12) sin960t]
#         = (125/12) e^(-280t) cos(960t - 0.2838)
#     临：u = 10(1 + 1000t) e^(-1000t)
#     过：u = (40/3) e^(-500t) - (10/3) e^(-2000t)
# 实验 1：特征根与参数打印。
# 实验 2：解析 vs RK4 数值（三案例的 u 与 i）。
# 实验 3：欠阻尼特征量（T_d、首谷时刻与值，解析 vs 数值）。
# 并生成 figures/lec12_fig1_circuit.svg/.png 与 lec12_fig2_damping.svg/.png。
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

L, C, U0 = 50e-3, 20e-6, 10.0
w0 = 1 / np.sqrt(L * C)
print("=== 实验 1：特征参数与三种 R 的根 ===")
print("  omega0 = 1/sqrt(LC) = %.0f rad/s" % w0)
for R, tag in [(28.0, "欠阻尼"), (100.0, "临界"), (125.0, "过阻尼")]:
    al = R / (2 * L)
    disc = al * al - w0 * w0
    if disc < 0:
        wd = np.sqrt(-disc)
        print("  R = %3.0f（%s）：alpha = %.0f < omega0；根 = -%.0f +/- j%.0f（omega_d = %.0f）"
              % (R, tag, al, al, wd, wd))
    elif abs(disc) < 1e-6:
        print("  R = %3.0f（%s）：alpha = %.0f = omega0；重根 s = -%.0f" % (R, tag, al, al))
    else:
        r1, r2 = -al + np.sqrt(disc), -al - np.sqrt(disc)
        print("  R = %3.0f（%s）：alpha = %.0f > omega0；根 = %.0f 与 %.0f"
              % (R, tag, al, r1, r2))
print("  临界电阻公式核对：2 sqrt(L/C) = %.0f ohm" % (2 * np.sqrt(L / C)))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：解析 vs RK4 数值（u_C 与 i_L） ===")
def u_under(t):
    return np.exp(-280 * t) * (10 * np.cos(960 * t) + (35 / 12) * np.sin(960 * t))
def u_crit(t):
    return 10 * (1 + 1000 * t) * np.exp(-1000 * t)
def u_over(t):
    return (40 / 3) * np.exp(-500 * t) - (10 / 3) * np.exp(-2000 * t)
def i_under(t):
    return (5 / 24) * np.exp(-280 * t) * np.sin(960 * t)
def i_crit(t):
    return 200 * t * np.exp(-1000 * t)
def i_over(t):
    return (2 / 15) * (np.exp(-500 * t) - np.exp(-2000 * t))

def rk4_rlc(R, T=12e-3, dt=1e-6):
    n = int(round(T / dt)) + 1
    t = np.arange(n) * dt
    u = np.zeros(n)
    i = np.zeros(n)
    u[0] = U0
    for k in range(1, n):
        ku1, ki1 = -i[k - 1] / C, (u[k - 1] - R * i[k - 1]) / L
        ku2, ki2 = -(i[k - 1] + ki1 * dt / 2) / C, (u[k - 1] + ku1 * dt / 2 - R * (i[k - 1] + ki1 * dt / 2)) / L
        ku3, ki3 = -(i[k - 1] + ki2 * dt / 2) / C, (u[k - 1] + ku2 * dt / 2 - R * (i[k - 1] + ki2 * dt / 2)) / L
        ku4, ki4 = -(i[k - 1] + ki3 * dt) / C, (u[k - 1] + ku3 * dt - R * (i[k - 1] + ki3 * dt)) / L
        u[k] = u[k - 1] + (ku1 + 2 * ku2 + 2 * ku3 + ku4) * dt / 6
        i[k] = i[k - 1] + (ki1 + 2 * ki2 + 2 * ki3 + ki4) * dt / 6
    return t, u, i

cases = [
    (28.0, u_under, i_under, "欠阻尼"),
    (100.0, u_crit, i_crit, "临界"),
    (125.0, u_over, i_over, "过阻尼"),
]
ts = {}
res = {}
for R, uf, if_, tag in cases:
    t, u, i = rk4_rlc(R)
    err_u = np.max(np.abs(u - uf(t)))
    err_i = np.max(np.abs(i - if_(t)))
    print("  %s（R=%.0f）：max|u 偏差| = %.2e V，max|i 偏差| = %.2e A" % (tag, R, err_u, err_i))
    ts[R] = t
    res[R] = (u, i)

# ---------------------------------------------------------------------
print()
print("=== 实验 3：欠阻尼特征量（解析 vs 数值） ===")
K = 125 / 12
Td = 2 * np.pi / 960
# 峰谷时刻 = 导数零点：本例初值 du/dt(0)=0 使极值恰在 960t = k*pi 处
t_valley = np.pi / 960
u_valley = -10 * np.exp(-280 * np.pi / 960)
t_peak2 = 2 * np.pi / 960
u_peak2 = 10 * np.exp(-280 * 2 * np.pi / 960)
t_valley3 = 3 * np.pi / 960
u_valley3 = -10 * np.exp(-280 * 3 * np.pi / 960)
print("  振荡周期 T_d = 2 pi / omega_d = %.3f ms" % (Td * 1e3))
print("  首谷：解析 t = %.3f ms、u = -10 e^(-7pi/24) = %.3f V" % (t_valley * 1e3, u_valley))
t4 = ts[28.0]
u4, i4 = res[28.0]
win = int(6e-3 / 1e-6)
idx = int(np.argmin(u4[:win]))
print("  首谷：数值 t = %.3f ms、u = %.3f V（一致）" % (t4[idx] * 1e3, u4[idx]))
print("  次峰：t = %.3f ms、u = %.3f V；次谷：t = %.3f ms、u = %.3f V"
      % (t_peak2 * 1e3, u_peak2, t_valley3 * 1e3, u_valley3))
# i_L 峰值
ti = np.arctan(960 / 280) / 960
i_peak = (5 / 24) * np.exp(-280 * ti) * np.sin(960 * ti)
print("  i_L 峰值：t = %.3f ms、i = %.4f A（w_L 峰值 = %.0f uJ）"
      % (ti * 1e3, i_peak, 0.5 * L * i_peak ** 2 * 1e6))
print("  初始能量 W(0) = 1/2 C U0^2 = %.0f uJ" % (0.5 * C * U0 ** 2 * 1e6))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：运行例电路（C 预充放电回路） ===")
with schemdraw.Drawing(show=False) as d:
    # 回路矩形：左 C、上开关、右 R、下 L
    d += elm.Line().at((0, 2.2)).to((0.7, 2.2))
    d += elm.Dot().at((0.7, 2.2))
    d += elm.Dot().at((1.5, 2.2))
    d += elm.Line().at((0.7, 2.2)).to((1.5, 2.2))
    d += elm.Label().at((1.1, 2.55)).label("$t=0$ 合上", fontsize=10)
    d += elm.Line().at((1.5, 2.2)).to((3.0, 2.2))
    # 右侧 R
    d += elm.Line().at((3.0, 2.2)).to((3.0, 1.7))
    d += elm.Resistor().at((3.0, 0.7)).up().length(1.0)
    d += elm.Label().at((2.25, 1.2)).label("$R$")
    d += elm.Line().at((3.0, 0.7)).to((3.0, 0))
    # 底边 L
    d += elm.Line().at((3.0, 0)).to((2.0, 0))
    d += elm.Inductor().at((2.0, 0)).left().length(1.0)
    d += elm.Label().at((1.45, -0.55)).label("$L$")
    d += elm.Line().at((1.0, 0)).to((0, 0))
    # 左侧 C
    d += elm.Line().at((0, 2.2)).to((0, 1.45))
    d += elm.Line().at((-0.25, 1.45)).to((0.25, 1.45))
    d += elm.Line().at((-0.25, 1.25)).to((0.25, 1.25))
    d += elm.Line().at((0, 1.25)).to((0, 0))
    d += elm.Label().at((0.55, 1.35)).label("$C$", fontsize=11)
    d += elm.Label().at((0.42, 1.75)).label("+", fontsize=11)
    d += elm.Label().at((0.42, 0.85)).label("-", fontsize=11)
    d += elm.Label().at((1.55, 0.7)).label("$u_C(0) = 10$ V", fontsize=10)

save_stem = "lec12_fig1_circuit"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：三种阻尼对比 ===")
fig, ax = plt.subplots(figsize=(9.5, 4.8))
tt = np.linspace(0, 12e-3, 2000)
ax.plot(tt * 1e3, u_over(tt), color="#2e7d32", lw=2.2, label="过阻尼：$R$ = 125 $\\Omega$")
ax.plot(tt * 1e3, u_crit(tt), color="#c0392b", lw=2.2, label="临界：$R$ = 100 $\\Omega$")
ax.plot(tt * 1e3, u_under(tt), color="#1f5fa8", lw=2.4, label="欠阻尼：$R$ = 28 $\\Omega$")
ax.plot(tt * 1e3, K * np.exp(-280 * tt), ls="--", color="#999999", lw=1.1,
        label="包络 $\\pm\\frac{125}{12}e^{-280t}$")
ax.plot(tt * 1e3, -K * np.exp(-280 * tt), ls="--", color="#999999", lw=1.1)
ax.axhline(0, color="#444444", lw=0.8)
ax.annotate("首谷 -4.00 V @ 3.27 ms", xy=(3.272, -4.0), xytext=(4.9, -3.9), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#1f5fa8"), color="#1f5fa8")
ax.annotate("临界：不超调、最快收场", xy=(1.0, 3.5), xytext=(2.6, 6.4), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#c0392b"), color="#c0392b")
ax.annotate("过阻尼：尾巴最慢", xy=(8.0, 0.9), xytext=(7.2, 3.0), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#2e7d32"), color="#2e7d32")
ax.set_xlabel("时间 $t$ / ms")
ax.set_ylabel("$u_C$ / V")
ax.set_title("同一回路（$L$=50 mH、$C$=20 $\\mu$F、$u_C(0)$=10 V），$R$ 换三次", fontsize=11)
ax.legend(fontsize=9, loc="upper right")
ax.set_ylim(-6.5, 11)
ax.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec12_fig2_damping"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec12-01 完成。")