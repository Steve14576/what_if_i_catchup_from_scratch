# =====================================================================
# lec22-01 网络函数、极点零点与稳定性：H(s) 极零点、s=jω 切片互证、稳定性三态
#          （第 22 讲 §1-§3 数值实验；图 1 极零点图、图 2 稳定性三态、图 3 切片互证）
# 规模纪律：总耗时 < 15 秒（sympy 符号 + 扫频 + 时域积分 + 三张图）。
#
# 主例（沿用 19 讲 RLC）：R = 10 欧、L = 100 mH、C = 10 uF。
#   w0 = 1000 rad/s；Q = 10；alpha = R/2L = 50；wd = 998.75。
#   电容口：H_C(s) = 1e6/(s^2+100s+1e6) -> 极点 -50 ± j998.75，无零点。
#   电阻口：H_R(s) = 100s/(s^2+100s+1e6) -> 零点 0，极点同上。
#   s=jw 切片 = 19 讲的 |H_C(jw)|、|H_R(jw)|（峰值 10.0125 @ 997.5；带通峰 1）。
# 稳定性三态：RC 低通（极点 -1e4，稳定）；理想 LC（±j1000，临界）；
#   负阻尼 RLC（+50 ± j998.75，不稳定，冲激响应发散）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import os

import numpy as np
import sympy as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

s = sp.symbols("s")
R, L, C = 10.0, 0.1, 10e-6
w0 = 1 / np.sqrt(L * C)
Q = w0 * L / R
alpha = R / (2 * L)
wd = np.sqrt(w0 ** 2 - alpha ** 2)

print("=== 实验 1：主例 H(s) 的极零点（sympy 求根） ===")
HC = 1e6 / (s ** 2 + 100 * s + 1e6)
HR = 100 * s / (s ** 2 + 100 * s + 1e6)
print("  H_C(s) = %s：极点 %s（无零点）" % (HC, sp.solve(sp.denom(sp.together(HC)), s)))
print("  H_R(s) = %s：零点 %s；极点 %s"
      % (HR, sp.solve(sp.numer(sp.together(HR)), s), sp.solve(sp.denom(sp.together(HR)), s)))
print("  核对：|极点| = %.4f（= w0 = %.1f）；实部 = %.1f（= -alpha）"
      % (abs(complex(-50, wd)), w0, -50))

print()
print("=== 实验 2：s = jw 切片 = 19 讲频响 ===")
w = np.logspace(2, 4.2, 40000)
fHC = sp.lambdify(s, HC, "numpy")
fHR = sp.lambdify(s, HR, "numpy")
HCjw = np.abs(fHC(1j * w))
HRjw = np.abs(fHR(1j * w))
iw = np.argmax(HCjw)
print("  |H_C(jw)| 峰 = %.4f @ %.1f rad/s（19 讲实测 10.0125 @ 997.5）" % (HCjw[iw], w[iw]))
print("  |H_R(jw0)| = %.4f（expect 1）；|H_C(jw0)| = %.4f（expect Q = 10）"
      % (abs(HR.subs(s, 1j * w0)), abs(HC.subs(s, 1j * w0))))
# 与 19 讲公式直接对照
H19 = np.abs(1 / (1 - w ** 2 * L * C + 1j * w * R * C))
print("  与 19 讲公式 max 偏差 = %.2e" % np.max(np.abs(HCjw - H19)))

print()
print("=== 实验 3：稳定性三态（极点位置 -> 冲激响应） ===")
cases = [
    ("RC 低通（极点 -1e4）", [-1e4], "稳定：衰减"),
    ("理想 LC（极点 ±j1000）", [1j * 1000, -1j * 1000], "临界：等幅振荡"),
    ("负阻尼 RLC（极点 +50±j998.75）", [complex(50, wd), complex(50, -wd)], "不稳定：发散"),
]
for name, poles, tag in cases:
    pole = poles[0]
    sig = pole.real
    verdict = "左半平面" if sig < 0 else ("虚轴" if sig == 0 else "右半平面")
    print("  %-30s 首极点实部 %+8.1f -> %s（%s）" % (name, sig, verdict, tag))

print()
print("=== 实验 4：冲激响应验证三态（RK4 二阶系统） ===")
def sim_impulse(a1, a0, T=0.03, dt=1e-6, tag=""):
    # y'' + a1 y' + a0 y = 冲激 -> 等价初值 y(0)=0, y'(0)=1（对二阶真分式）
    y, dy = 0.0, 1.0
    n = int(T / dt)
    tr, yr = [], []
    for k in range(n):
        def f(yv, dyv):
            return (dyv, -a1 * dyv - a0 * yv)
        k1 = f(y, dy); k2 = f(y + dt/2*k1[0], dy + dt/2*k1[1])
        k3 = f(y + dt/2*k2[0], dy + dt/2*k2[1]); k4 = f(y + dt*k3[0], dy + dt*k3[1])
        y += dt/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        dy += dt/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        tr.append((k+1)*dt); yr.append(y)
    return np.array(tr), np.array(yr)
def sim_first(a1, T=6e-4, dt=1e-7):
    # 一阶：y' = -a1 y，y(0)=1（即 H(s)=1/(s+a1) 的冲激响应 e^{-a1 t}）
    y = 1.0
    n = int(T / dt)
    tr, yr = [], []
    for k in range(n):
        k1 = -a1 * y
        k2 = -a1 * (y + dt / 2 * k1)
        k3 = -a1 * (y + dt / 2 * k2)
        k4 = -a1 * (y + dt * k3)
        y += dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        tr.append((k + 1) * dt)
        yr.append(y)
    return np.array(tr), np.array(yr)

t1, y1 = sim_first(1e4)                                  # 极点 -1e4（一阶）
t2, y2 = sim_impulse(0, 1e6, T=0.03, tag="LC")           # 极点 ±j1000
t3, y3 = sim_impulse(-100, 1e6, T=0.03, tag="RLC")       # 极点 +50±j998.75
print("  RC：末值 = %.2e（趋零 -> 稳定）" % y1[-1])
print("  LC：末段峰值 %.4f（不衰减 -> 临界）" % np.max(np.abs(y2[len(y2)//2:])))
print("  RLC：末值/峰值 = %.2f（增长 -> 不稳定）" % (np.max(np.abs(y3[-2000:])) / np.max(np.abs(y3[:2000]))))

print()
print("=== 实验 5：冲激响应与 H(s) 的对应（主例 h(t)） ===")
t = sp.symbols("t", positive=True)
ht = sp.simplify(sp.inverse_laplace_transform(HC, s, t))
print("  h(t) = %s（= (2Q/wd?) e^{-50t} sin 998.75t 形式）" % ht)
print("  数值核对：h(1e-9) = %.4f（≈0，极限 0）；h'(0+) = %.0f" % (float(ht.subs(t, 1e-9)), float(sp.diff(ht, t).subs(t, 1e-9))))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：极零点图（主例两个端口） ===")
fig, ax = plt.subplots(figsize=(8.6, 4.8))
ax.axhline(0, color="#cccccc", lw=0.8)
ax.axvline(0, color="#666666", lw=1.0)
ax.plot([-50, -50], [wd, -wd], "x", color="#c0392b", ms=9, mew=2.2, label="极点 $-50\\pm\\mathrm{j}998.75$（两个 H 共有）")
ax.plot([0], [0], "o", color="#1f5fa8", ms=8, label="零点 $0$（仅 $H_R$）")
ax.annotate("$\\omega_0$ = |极点| = 1000", xy=(-50, wd), xytext=(-950, 1120), fontsize=9, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.set_xlim(-1200, 400)
ax.set_ylim(-1200, 1300)
ax.set_xlabel("$\\sigma$")
ax.set_ylabel("$\\mathrm{j}\\omega$")
ax.set_title("主例极零点图：$H_C$ 无零点、$H_R$ 多一个原点零点（同一组极点）", fontsize=11)
ax.legend(fontsize=9, loc="lower right")
ax.grid(alpha=0.25)
plt.tight_layout()
save_stem = "lec22_fig1_polezero"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：稳定性三态（s 平面 + 冲激响应） ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.4))
a1.axhline(0, color="#cccccc", lw=0.8)
a1.axvline(0, color="#666666", lw=1.0)
a1.plot([-100], [0], "o", color="#2e7d32", ms=9, label="RC：左半平面（稳定）")
a1.plot([0, 0], [1000, -1000], "s", color="#e67e22", ms=8, label="LC：虚轴（临界）")
a1.plot([50, 50], [wd, -wd], "^", color="#c0392b", ms=9, label="负阻尼：右半平面（不稳定）")
a1.set_xlim(-140, 90)
a1.set_ylim(-1300, 1300)
a1.set_xlabel("$\\sigma$")
a1.set_ylabel("$\\mathrm{j}\\omega$")
a1.set_title("极点位置", fontsize=11)
a1.legend(fontsize=8, loc="lower right")
a1.grid(alpha=0.25)
# 三种情形量级差约 1000 倍，各自归一化显示（比形态）
n1 = np.max(np.abs(y1[: max(1, len(y1) // 50)]))
n2 = np.max(np.abs(y2[: max(1, len(y2) // 50)]))
n3 = np.max(np.abs(y3[: max(1, len(y3) // 50)]))
a2.plot(t1 * 1e3, y1 / n1, color="#2e7d32", lw=1.8, label="RC：衰减（稳定）")
a2.plot(t2 * 1e3, y2 / n2, color="#e67e22", lw=1.6, label="LC：等幅（临界）")
a2.plot(t3 * 1e3, np.clip(y3 / n3, -30, 30), color="#c0392b", lw=1.6, label="负阻尼：发散（不稳定）")
a2.set_xlabel("时间 $t$ / ms")
a2.set_ylabel("归一化冲激响应")
a2.set_title("对应的冲激响应（各自首段峰值归一）", fontsize=11)
a2.legend(fontsize=8, loc="upper right")
a2.set_ylim(-3, 3)
a2.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec22_fig2_stability"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：s=jw 切片与频响互证 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.4))
a1.axvline(0, color="#666666", lw=1.0)
a1.axhline(0, color="#cccccc", lw=0.8)
a1.plot([-50, -50], [wd, -wd], "x", color="#c0392b", ms=9, mew=2.2)
a1.plot([0, 0], [-1100, 1100], color="#1f5fa8", lw=2.0)
a1.annotate("$s = \\mathrm{j}\\omega$（虚轴切片）", xy=(0, 900), xytext=(-1050, 1150),
            fontsize=9, color="#1f5fa8", arrowprops=dict(arrowstyle="->", color="#1f5fa8"))
a1.plot([0], [1000], "o", color="#1f5fa8", ms=6)
a1.text(-980, 620, "沿虚轴移动取样\n每个 $\\omega$ 取一个 $H$ 值", fontsize=9, color="#666666")
a1.set_xlim(-1200, 400)
a1.set_ylim(-1200, 1300)
a1.set_xlabel("$\\sigma$")
a1.set_ylabel("$\\mathrm{j}\\omega$")
a1.set_title("在 s 平面上：沿虚轴取样", fontsize=11)
a1.grid(alpha=0.25)
a2.semilogx(w, HCjw, color="#c0392b", lw=2.0, label="$|H_C|$（峰 $Q$）")
a2.semilogx(w, HRjw, color="#1f5fa8", lw=2.0, label="$|H_R|$（带通）")
a2.axvline(1000, color="#cccccc", lw=1.0, ls="--")
a2.axhline(1 / np.sqrt(2), color="#999999", lw=1.0, ls=":")
a2.set_xlabel("$\\omega$ / (rad/s)")
a2.set_ylabel("$|H|$")
a2.set_title("得到的是 19 讲的频率响应曲线", fontsize=11)
a2.legend(fontsize=9, loc="upper right")
a2.grid(alpha=0.3, which="both")
plt.tight_layout()
save_stem = "lec22_fig3_slice"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec22-01 完成。")