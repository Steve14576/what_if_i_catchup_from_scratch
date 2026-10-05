# =====================================================================
# lec21-01 拉普拉斯变换与运算法：变换对数值验证、RL/ RLC 运算法全解、部分分式三形态
#          （第 21 讲 §2-§4 数值实验；图 1 s 域模型、图 2 主例响应、图 3 s 平面与响应形态）
# 规模纪律：总耗时 < 20 秒（sympy 符号运算 + 数值对照 + 三张图）。
#
# 主例：RLC 放电（12 讲同电路）：R = 28 欧、L = 50 mH、C = 20 uF、
#   u_C(0) = 10 V、i_L(0) = 0。s 域：I(s) = u_C(0)/(s(R+sL+1/(sC)))
#   = 10/(28s+0.05s^2+50000) = 200/(s^2+560s+10^6) = 200/((s+280)^2+960^2)
#   -> i(t) = (200/960) e^{-280t} sin 960t = 0.2083 e^{-280t} sin 960t A
#   -> u_C(t) = e^{-280t}[10 cos 960t + 2.9167 sin 960t] V（与 12 讲一致）
# 辅助例：RL 阶跃+初值：10 V、R = 2 欧、L = 1 H、i(0) = 2 A
#   -> I(s) = (10/s + 2)/(s+2) = 5/s - 3/(s+2) -> i(t) = 5 - 3 e^{-2t}
# 部分分式三形态：单根 / 复根 / 假分式（先长除）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import os

import numpy as np
import sympy as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import schemdraw
import schemdraw.elements as elm

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

elm.style(elm.STYLE_IEC)
schemdraw.config(font="Microsoft YaHei", fontsize=12)

t, s = sp.symbols("t s", real=True)

# ---------------------------------------------------------------------
print("=== 实验 1：常用变换对的数值验证（数值积分 vs 公式） ===")
def numlaplace(f, sv, T=60.0, n=400000):
    tt = np.linspace(0, T, n)
    return np.trapezoid(f(tt) * np.exp(-sv * tt), tt)

checks = [
    ("e^{-2t} -> 1/(s+2)", lambda x: np.exp(-2 * x), 1.0, 1 / (1 + 2)),
    ("1 (t>0) -> 1/s", lambda x: np.ones_like(x), 2.0, 1 / 2),
    ("cos 3t -> s/(s^2+9)", lambda x: np.cos(3 * x), 1.0, 1 / (1 + 9)),
    ("t e^{-t} -> 1/(s+1)^2", lambda x: x * np.exp(-x), 2.0, 1 / (2 + 1) ** 2),
]
for name, f, sv, expect in checks:
    val = numlaplace(f, sv)
    print("  %-22s s = %.1f：数值 %.6f，公式 %.6f，差 %.1e" % (name, sv, val, expect, abs(val - expect)))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：RL 阶跃+初值（sympy 运算法全解） ===")
R1, L1, E1, i0 = 2.0, 1.0, 10.0, 2.0
Is = (E1 / s + L1 * i0) / (s * L1 + R1)
print("  I(s) = %s" % sp.simplify(Is))
ipart = sp.apart(Is, s)
print("  部分分式：%s" % ipart)
it = sp.inverse_laplace_transform(Is, s, t)
print("  逆变换：i(t) = %s" % sp.simplify(it))
print("  核对：i(0+) = %.4f（expect %.1f）；i(inf) = %.1f（expect %.1f）"
      % (float(it.subs(t, 1e-6)), i0, float(it.subs(t, 100)), E1 / R1))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：RLC 放电运算法全解（与 12 讲对照） ===")
R2, L2, C2, u0 = 28.0, 50e-3, 20e-6, 10.0
Zs = R2 + s * L2 + 1 / (s * C2)
Is2 = sp.simplify(u0 / (s * Zs))
print("  I(s) = %s" % sp.simplify(Is2))
it2 = sp.simplify(sp.inverse_laplace_transform(Is2, s, t))
print("  i(t) = %s  (m = 280, wd = 960)" % it2)
Us2 = sp.simplify(Is2 * (R2 + s * L2))   # 电容电压 = 回路电流乘 (R + sL)（方向一致，避开模型符号坑）
ut2 = sp.simplify(sp.inverse_laplace_transform(Us2, s, t))
print("  u_C(t) = %s" % ut2)
# 与 12 讲解析解对照
def u12(tt):
    return np.exp(-280 * tt) * (10 * np.cos(960 * tt) + 10 * 280 / 960 * np.sin(960 * tt))
def i12(tt):
    return 200 / 960 * np.exp(-280 * tt) * np.sin(960 * tt)
f_i = sp.lambdify(t, it2.subs(sp.Heaviside(t), 1), "numpy")   # t>0 分支（避开 Heaviside 数值映射坑）
f_u = sp.lambdify(t, ut2.subs(sp.Heaviside(t), 1), "numpy")
tt = np.linspace(0, 0.012, 200)
d_i = np.max(np.abs(f_i(tt) - i12(tt)))
d_u = np.max(np.abs(f_u(tt) - u12(tt)))
print("  与 12 讲解析解最大偏差：i %.2e A；u_C %.2e V" % (d_i, d_u))
# RK4 数值对照
dt = 1e-6
Nn = int(0.012 / dt)
uc, il = 10.0, 0.0
mx = 0.0
for k in range(Nn):
    def f(ucv, ilv):
        return (-ilv / C2, (ucv - R2 * ilv) / L2)   # 放电 i 从正端流出：du/dt = -i/C
    k1 = f(uc, il)
    k2 = f(uc + dt / 2 * k1[0], il + dt / 2 * k1[1])
    k3 = f(uc + dt / 2 * k2[0], il + dt / 2 * k2[1])
    k4 = f(uc + dt * k3[0], il + dt * k3[1])
    uc += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
    il += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    tv = (k + 1) * dt
    mx = max(mx, abs(uc - float(f_u(tv))), abs(il - float(f_i(tv))))
print("  RK4 数值 vs 运算法解析：全程最大偏差 %.2e" % mx)

# ---------------------------------------------------------------------
print()
print("=== 实验 4：部分分式三个形态 ===")
F1 = (3 * s + 11) / ((s + 2) * (s + 3))
print("  单根：%s = %s" % (sp.simplify(F1), sp.apart(F1, s)))
F2 = 10 / (s ** 2 + 6 * s + 25)
print("  复根：%s = %s" % (F2, sp.apart(F2, s)))
print("        配方法 -> (10/4) * 4/((s+3)^2+4^2) -> f(t) = 2.5 e^{-3t} sin 4t")
F3 = (s ** 2 + 3 * s + 3) / (s + 1)
q3, r3 = sp.div(sp.expand(s ** 2 + 3 * s + 3), s + 1)
print("  假分式：%s 长除 = %s + %s/(s+1)（先除成真分式，商多项式对应冲激项，认识层）" % (F3, q3, r3))
print("  数值核对：2.5 e^{-3t} sin 4t 的拉氏在 s=1 处 = %.6f；10/(1+6+25) = %.6f"
      % (numlaplace(lambda x: 2.5 * np.exp(-3 * x) * np.sin(4 * x), 1.0), 10 / 32))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：s 域元件模型（串联压源版） ===")
with schemdraw.Drawing(show=False) as d:
    # 格1：电感（sL 串联 Li(0-) 压源）
    d += elm.Inductor().at((0, 2.0)).to((1.6, 2.0))
    d += elm.SourceV().at((1.6, 2.0)).right().length(1.6)
    d += elm.Line().at((0, 0.7)).to((3.2, 0.7))
    d += elm.Line().at((0, 2.0)).to((0, 0.7))
    d += elm.Line().at((3.2, 2.0)).to((3.2, 0.7))
    d += elm.Label().at((1.6, 3.35)).label("电感：$sL$ 串联 $Li(0^-)$", fontsize=11)
    d += elm.Label().at((0.8, 2.45)).label("$sL$", fontsize=10)
    d += elm.Label().at((2.4, 1.2)).label("$Li(0^-)$", fontsize=10)
    # 格2：电容（1/(sC) 串联 u(0-)/s 压源）
    d += elm.Capacitor().at((5.4, 2.0)).to((7.0, 2.0))
    d += elm.SourceV().at((7.0, 2.0)).right().length(1.6)
    d += elm.Line().at((5.4, 0.7)).to((8.6, 0.7))
    d += elm.Line().at((5.4, 2.0)).to((5.4, 0.7))
    d += elm.Line().at((8.6, 2.0)).to((8.6, 0.7))
    d += elm.Label().at((7.0, 3.35)).label("电容：$1/(sC)$ 串联 $u(0^-)/s$", fontsize=11)
    d += elm.Label().at((6.2, 2.45)).label("$1/(sC)$", fontsize=10)
    d += elm.Label().at((7.8, 1.2)).label("$u(0^-)/s$", fontsize=10)

save_stem = "lec21_fig1_smodels"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：主例 RLC 放电的响应（运算法 vs 12 讲解析 vs RK4） ===")
tt2 = np.linspace(0, 12e-3, 800)
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.4, 6.2), sharex=True)
a1.plot(tt2 * 1e3, f_u(tt2), color="#1f5fa8", lw=2.2, label="运算法 u_C(t)")
a1.plot(tt2 * 1e3, u12(tt2), color="#c0392b", lw=1.2, ls="--", label="12 讲解析解")
a1.set_ylabel("$u_C$ / V")
a1.set_title("运算法一次给出完整响应（含初值），与 12 讲逐点一致（最大偏差 1e-15 量级）", fontsize=11)
a1.legend(fontsize=9, loc="upper right")
a1.grid(alpha=0.3)
a2.plot(tt2 * 1e3, f_i(tt2), color="#2e7d32", lw=2.2, label="运算法 i(t)")
a2.plot(tt2 * 1e3, i12(tt2), color="#e67e22", lw=1.2, ls="--", label="12 讲解析解")
a2.set_xlabel("时间 $t$ / ms")
a2.set_ylabel("$i$ / A")
a2.legend(fontsize=9, loc="upper right")
a2.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec21_fig2_rlc_response"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：s 平面根位置与响应形态（认识层，22 讲钩子） ===")
fig, ax = plt.subplots(figsize=(8.8, 4.8))
ax.axvline(0, color="#666666", lw=1.0)
ax.axhline(0, color="#cccccc", lw=0.8)
# 主例复根对
ax.plot([-280, -280], [960, -960], "o", color="#c0392b", ms=7)
ax.annotate("复根对（欠阻尼）：衰减振荡\n主例 $-280 \\pm \\mathrm{j}960$", xy=(-280, 960),
            xytext=(-1180, 1020), fontsize=9, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
# 双实根（过阻尼）
ax.plot([-1000, -100], [0, 0], "o", color="#e67e22", ms=7)
ax.text(-1300, -300, "双实根（过阻尼）：两个实指数叠加", fontsize=9, color="#e67e22")
# 单实根
ax.plot([-500], [0], "s", color="#2e7d32", ms=7)
ax.text(-560, 250, "单实根：纯指数", fontsize=9, color="#2e7d32")
ax.set_xlim(-1370, 500)
ax.set_ylim(-1200, 1300)
ax.set_xlabel("$\\sigma$（实部：决定衰减快慢）")
ax.set_ylabel("$\\mathrm{j}\\omega$（虚部：决定振荡频率）")
ax.set_title("根在 s 平面上的位置决定响应形态（22 讲的主题：极点零点）", fontsize=11)
ax.grid(alpha=0.25)
plt.tight_layout()
save_stem = "lec21_fig3_spole"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec21-01 完成。")