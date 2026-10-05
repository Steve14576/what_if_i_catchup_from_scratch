# =====================================================================
# lec20-01 非正弦周期电流电路：方波傅里叶逼近、谐波法（RL）、有效值与功率对照
#          （第 20 讲 §1-§3 数值实验；图 1 逼近、图 2 谐波成分、图 3 合成对照与收敛）
# 规模纪律：总耗时 < 10 秒（级数求和 + RK4 积分 + 三张图）。
#
# 主例：方波源 A = 10 V、基波角频率 w1 = 1000 rad/s，加到 R = 10 欧、L = 10 mH。
#   方波展开：v = (4A/pi)[sin w1 t + (1/3) sin 3w1 t + (1/5) sin 5w1 t + ...]
#   有效值相量（基波）：V1 = 9.003 V -> I1 = 9.003/(10+j10) = 0.6366 角 -45 度
#   n=3: |Z| = sqrt(100+900) = 31.623 -> I3 = 3.001/31.623 = 0.0949 角 -71.565 度
#   n=5: |Z| = sqrt(100+2500) = 50.990 -> I5 = 1.8006/50.990 = 0.0353 角 -78.690 度
#   方波 RMS = A = 10 V（解析，靠 sum(1/n^2, odd) = pi^2/8）；前几项部分和收敛慢（Gibbs）。
#   电流 RMS = sqrt(sum In^2) ~ 0.645 A；功率 P = I^2 R ~ 4.16 W（与时域积分对照）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import os

import numpy as np
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

A = 10.0
w1 = 1000.0
R = 10.0
L = 10e-3
T = 2 * np.pi / w1

# 方波（奇函数、半波对称）：奇次正弦项，系数 4A/(n pi)
def square_partial(t, n_max):
    v = np.zeros_like(t)
    for n in range(1, n_max + 1, 2):
        v += (4 * A / (n * np.pi)) * np.sin(n * w1 * t)
    return v

print("=== 实验 1：方波傅里叶逼近与有效值收敛 ===")
print("  基波峰值 4A/pi = %.3f V；三次 %.3f；五次 %.3f" % (4 * A / np.pi, 4 * A / (3 * np.pi), 4 * A / (5 * np.pi)))
print("  方波有效值（解析）= A = %.1f V（用 sum_{odd} 1/n^2 = pi^2/8）" % A)
for n_max in [1, 3, 5, 9, 49, 199]:
    rms = np.sqrt(sum((4 * A / (n * np.pi)) ** 2 / 2 for n in range(1, n_max + 1, 2)))
    print("  保留到 %2d 次：RMS 部分和 = %.4f V" % (n_max, rms))

print()
print("=== 实验 2：谐波法解 RL 电路（各次谐波独立相量求解） ===")
I_eff = {}
for n in range(1, 40, 2):
    Vn = (4 * A / (n * np.pi)) / np.sqrt(2)          # 有效值
    Zn = R + 1j * n * w1 * L
    In = Vn / Zn
    I_eff[n] = abs(In)
    if n <= 9:
        print("  n = %d：|Z| = %7.3f 欧，相移 %7.3f 度，I 有效值 = %.4f A"
              % (n, abs(Zn), np.degrees(np.angle(Zn)), abs(In)))
I_rms = np.sqrt(sum(v ** 2 for v in I_eff.values()))
P_harm = sum(v ** 2 for v in I_eff.values()) * R
print("  电流有效值（谐波平方和，n<=39）= %.4f A" % I_rms)
print("  功率 P = sum(In^2) R = %.4f W" % P_harm)

print()
print("=== 实验 3：时域数值解对照 ===")
# 解析方波源驱动 RL 的 ODE：L di/dt = v(t) - R i（RK4，dt = T/20000）
def v_src(tt):
    return A if (tt % T) < T / 2 else -A
dt = T / 20000
t = np.arange(0, 6 * T, dt)
i = np.zeros_like(t)
for k in range(len(t) - 1):
    # RK4
    tk, ik = t[k], i[k]
    f = lambda tt, ii: (v_src(tt) - R * ii) / L
    k1 = f(tk, ik)
    k2 = f(tk + dt / 2, ik + dt / 2 * k1)
    k3 = f(tk + dt / 2, ik + dt / 2 * k2)
    k4 = f(tk + dt, ik + dt * k3)
    i[k + 1] = ik + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
# 稳态后两个周期上算 RMS 与功率
mask = t > 4 * T
i_rms_num = np.sqrt(np.mean(i[mask] ** 2))
p_num = np.mean(np.array([v_src(tt) for tt in t[mask]]) * i[mask])
print("  时域数值：I_rms = %.4f A；P = %.4f W（谐波法：%.4f A / %.4f W）"
      % (i_rms_num, p_num, I_rms, P_harm))

print()
print("=== 实验 4：方波的总谐波畸变率（THD，认识层） ===")
U1 = (4 * A / np.pi) / np.sqrt(2)
U_rms_sq = A ** 2
thd = np.sqrt(U_rms_sq - U1 ** 2) / U1
print("  U1 = %.4f V；方波 THD = sqrt(U^2-U1^2)/U1 = %.1f%%（经典值约 48.3%%）" % (U1, thd * 100))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：方波傅里叶逼近 ===")
t1 = np.linspace(0, 2 * T, 2000)
fig, ax = plt.subplots(figsize=(9.6, 4.6))
ax.plot(t1 * 1e3, np.where(np.mod(t1, T) < T / 2, A, -A), color="#888888", lw=3.2, alpha=0.55, label="理想方波")
for nm, cc in zip([1, 3, 9, 49], ["#c0392b", "#e67e22", "#2e7d32", "#1f5fa8"]):
    ax.plot(t1 * 1e3, square_partial(t1, nm), color=cc, lw=1.8, label="保留到 %d 次" % nm)
ax.set_xlabel("时间 $t$ / ms")
ax.set_ylabel("电压 $v$ / V")
ax.set_title("方波 = 奇次谐波叠加：项数增加，逼近变好（过冲不消 = Gibbs 现象，认识层）", fontsize=11)
ax.legend(fontsize=9, loc="upper right", ncol=2)
ax.grid(alpha=0.3)
ax.set_ylim(-13.5, 13.5)
plt.tight_layout()
save_stem = "lec20_fig1_fourier"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：电压谐波与电流谐波的成分对照 ===")
ns = np.arange(1, 12, 2)
Vpk = [4 * A / (n * np.pi) for n in ns]
Ipk = [np.sqrt(2) * I_eff[n] for n in ns]
x = np.arange(len(ns))
fig, ax = plt.subplots(figsize=(9.2, 4.4))
ax.bar(x - 0.19, Vpk, width=0.36, color="#1f5fa8", label="电压谐波峰值 $V_n$（$4A/n\\pi$）")
ax.bar(x + 0.19, Ipk, width=0.36, color="#c0392b", label="电流谐波峰值 $I_n = V_n/|Z_n|$")
ax.set_xticks(x)
ax.set_xticklabels(["%d 次" % n for n in ns])
ax.set_ylabel("幅值 / V 或 A")
ax.set_title("同一方波下：电压谐波按 $1/n$ 缓降，电流谐波被 $|Z_n|$ 加速压低（电感低通效应）", fontsize=11)
ax.legend(fontsize=9)
ax.grid(alpha=0.3, axis="y")
plt.tight_layout()
save_stem = "lec20_fig2_spectrum"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：谐波合成电流 vs 时域数值解 ===")
i_h = np.zeros_like(t)
for n, val in I_eff.items():
    Zn = R + 1j * n * w1 * L
    i_h += np.sqrt(2) * val * np.sin(n * w1 * t + np.angle(1.0 / Zn))
diff = np.max(np.abs(i_h[mask] - i[mask]))
print("  谐波合成（n<=39）vs 时域数值解：稳态段最大偏差 = %.4f A" % diff)
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.6, 6.4), sharex=True)
a1.plot(t * 1e3, i_h, color="#1f5fa8", lw=2.0, label="谐波法合成（n 到 39）")
a1.plot(t * 1e3, i, color="#c0392b", lw=1.4, ls="--", label="时域数值积分（RK4）")
a1.set_ylabel("电流 $i$ / A")
a1.set_title("谐波法合成与时域数值解一致（RL 对方波的稳态电流）", fontsize=11)
a1.legend(fontsize=9, loc="upper right")
a1.grid(alpha=0.3)
rms_part = [np.sqrt(sum((4 * A / (n * np.pi)) ** 2 / 2 for n in range(1, nm + 1, 2))) for nm in range(1, 60, 2)]
a2.plot(range(1, 60, 2), rms_part, "o-", color="#2e7d32", ms=4)
a2.axhline(10, color="#999999", lw=1.2, ls=":")
a2.text(28, 10.02, "解析值 $A$ = 10 V", fontsize=10, color="#666666")
a2.set_ylim(8.85, 10.12)
a2.set_xlabel("保留的最高谐波次数")
a2.set_ylabel("RMS 部分和 / V")
a2.set_title("方波有效值的部分和：随项数缓慢趋向 10 V（含直流与全部奇次谐波）", fontsize=11)
a2.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec20_fig3_compose"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec20-01 完成。")