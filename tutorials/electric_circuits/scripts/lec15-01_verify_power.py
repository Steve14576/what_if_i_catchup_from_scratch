# =====================================================================
# lec15-01 正弦稳态功率：账本、瞬时功率、补偿、共轭匹配
#          （第 15 讲 §1-§4 数值实验；图 1 瞬时功率、图 2 三角相似、图 3 补偿）
# 规模纪律：总耗时 < 10 秒（numpy 向量化 + 三张图）。
#
# 主例（延续 14 讲）：U = 50∠0° V；Z1 = 3+4j（İ1 = 10∠-53.13°）、
#   Z2 = 3-4j（İ2 = 10∠+53.13°）；İ总 = 12∠0°。
#   账本：P1 = 300 W、Q1 = +400 var（感性）；P2 = 300、Q2 = -400（容性）；
#   总：P = 600 W、Q = 0、S = 600 VA（而 |Ṡ1|+|Ṡ2| = 1000——S 不守恒）。
#   补偿：并联 C = 160 uF 把 cosφ 提到 1（İ' = 6∠0°、S 降到 300 VA）；
#   C = 70 uF 补到 0.8（I' = 7.5 A、S = 375 VA）。
#   匹配：U_oc = 8∠0°、Z_eq = 4+4j -> Z_L = 4-4j 时 P_max = 4 W；
#   错配 Z_L = Z_eq 时只有 2 W。
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

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../electric_circuits
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

w = 1000.0
U = 50.0
Z1 = 3 + 4j
Z2 = 3 - 4j
I1 = U / Z1
I2 = U / Z2
It = U * (1 / Z1 + 1 / Z2)

# ---------------------------------------------------------------------
print("=== 实验 1：主例功率全账本 ===")
S1 = U * np.conj(I1)
S2 = U * np.conj(I2)
St = U * np.conj(It)
print("  S1 = U I1* = %.0f%+.0fj VA（P1 = %.0f W，Q1 = %+.0f var，|S1| = %.0f VA，感性）"
      % (S1.real, S1.imag, S1.real, S1.imag, abs(S1)))
print("  S2 = U I2* = %.0f%+.0fj VA（P2 = %.0f W，Q2 = %+.0f var，|S2| = %.0f VA，容性）"
      % (S2.real, S2.imag, S2.real, S2.imag, abs(S2)))
print("  S总 = %.0f%+.0fj VA（P = %.0f W，Q = %.0f var，|S| = %.0f VA，cosφ = 1）"
      % (St.real, St.imag, St.real, St.imag, abs(St)))
print("  复功率守恒：|S1 + S2 - S总| = %.2e；而 |S1| + |S2| = %.0f ≠ %.0f（S 不守恒！）"
      % (abs(S1 + S2 - St), abs(S1) + abs(S2), abs(St)))
print("  元件视角：P = I^2 R：支路1 P = 100 x 3 = %.0f W；Q_L = I^2 wL = 100 x 4 = %.0f var"
      % (abs(I1) ** 2 * 3, abs(I1) ** 2 * 4))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：瞬时功率与周期平均 ===")
ang = np.arctan(4 / 3)
T2 = 2 * 2 * np.pi / w
t = np.linspace(0, T2, 200001)
us = U * np.sqrt(2) * np.cos(w * t)
i1t = 10 * np.sqrt(2) * np.cos(w * t - ang)
i2t = 10 * np.sqrt(2) * np.cos(w * t + ang)
p1 = us * i1t
p2 = us * i2t
pt = us * (i1t + i2t)
# 解析形式：p = P + S cos(2wt + psi_u + psi_i)
p1_an = 300 + 500 * np.cos(2 * w * t - ang)
p2_an = 300 + 500 * np.cos(2 * w * t + ang)
pt_an = 600 + 600 * np.cos(2 * w * t)
print("  解析形式核对：max|p1 - (300+500cos(2wt-φ))| = %.2e" % np.max(np.abs(p1 - p1_an)))
print("  max|p2-解析| = %.2e；max|p总-解析| = %.2e"
      % (np.max(np.abs(p2 - p2_an)), np.max(np.abs(pt - pt_an))))
P1_num = np.trapezoid(p1, t) / T2
P2_num = np.trapezoid(p2, t) / T2
Pt_num = np.trapezoid(pt, t) / T2
print("  数值周期平均：p1 -> %.2f W（解析 300）；p2 -> %.2f；p总 -> %.2f（解析 600）"
      % (P1_num, P2_num, Pt_num))
print("  p1 极值：%.0f W / %.0f W（负功率=能量回流）；p总 极值：%.0f / %.0f（永不为负）"
      % (p1.min(), p1.max(), pt.min(), pt.max()))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：功率因数补偿 ===")
# 只留支路 1（感性负载）：P=300、Q=400、S=500、I=10、cosφ=0.6 滞后
C1 = 400 / (w * U ** 2)
Yload = 1 / Z1
Itot_c = U * (Yload + 1j * w * C1)
QC = -U ** 2 * w * C1
print("  补到 cosφ=1：C = Q/(wU^2) = 400/(1000x2500) = %.0f uF" % (C1 * 1e6))
print("    电容电流 I_C = U x wC = %.0f∠90° A；总电流 = %.0f∠%.4f° A；S' = %.0f VA，Q' = 0"
      % (U * w * C1, abs(Itot_c), np.degrees(np.angle(Itot_c)), U * abs(Itot_c)))
# 补到 cosφ=0.8：Q_c = P(tanφ1 - tanφ2) = 300*(4/3-3/4)
tan1 = 4 / 3
tan2 = 3 / 4
Qc2 = 300 * (tan1 - tan2)
C2 = Qc2 / (w * U ** 2)
Itot_c2 = U * (Yload + 1j * w * C2)
print("  补到 cosφ=0.8：Q_c = P(tanφ1-tanφ2) = 300(4/3-3/4) = %.0f var；C = %.0f uF" % (Qc2, C2 * 1e6))
print("    总电流 = %.1f A；S' = %.0f VA；cosφ' = P/S' = %.1f" 
      % (abs(Itot_c2), U * abs(Itot_c2), 300 / (U * abs(Itot_c2))))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：共轭匹配 ===")
Uoc = 8.0
Zeq = 4 + 4j
ZL = 4 - 4j
I_match = Uoc / (Zeq + ZL)
P_match = abs(I_match) ** 2 * ZL.real
print("  Z_L = Z_eq* = 4-4j：I = %.0f∠0° A；P = %.0f W（公式 U_oc^2/4R_eq = %.0f）"
      % (abs(I_match), P_match, Uoc ** 2 / (4 * Zeq.real)))
I_bad = Uoc / (Zeq + Zeq)
P_bad = abs(I_bad) ** 2 * Zeq.real
print("  错配 Z_L = Z_eq = 4+4j：I = %.4f A；P = %.0f W（只有匹配时的一半）"
      % (abs(I_bad), P_bad))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：瞬时功率三曲线 ===")
fig, ax = plt.subplots(figsize=(9.8, 4.6))
ax.plot(t * 1e3, p1, color="#1f5fa8", lw=1.8, label="$p_1$（感性支路）")
ax.plot(t * 1e3, p2, color="#2e7d32", lw=1.8, label="$p_2$（容性支路）")
ax.plot(t * 1e3, pt, color="#c0392b", lw=2.2, label="总瞬时功率 $p$")
ax.axhline(300, color="#1f5fa8", ls="--", lw=1.0)
ax.axhline(600, color="#c0392b", ls="--", lw=1.0)
ax.axhline(0, color="#444444", lw=0.8)
ax.annotate("负功率区：能量回流", xy=(1.85, -150), xytext=(2.6, -550), fontsize=10,
            color="#1f5fa8", arrowprops=dict(arrowstyle="->", color="#1f5fa8"))
ax.annotate("平均 600 W", xy=(10.8, 600), xytext=(9.6, 850), fontsize=10, color="#c0392b")
ax.annotate("平均 300 W", xy=(10.8, 300), xytext=(9.8, 80), fontsize=10, color="#1f5fa8")
ax.set_xlabel("时间 $t$ / ms")
ax.set_ylabel("功率 / W")
ax.set_title("瞬时功率：以 $2\\omega$ 波动，平均值就是有功功率", fontsize=11)
ax.legend(fontsize=9, loc="upper center", ncol=3)
ax.set_ylim(-900, 1350)
ax.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec15_fig1_instant"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：阻抗三角形与功率三角形相似 ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.4))
ax1.annotate("", xy=(3, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=2.2))
ax1.annotate("", xy=(3, 4), xytext=(3, 0), arrowprops=dict(arrowstyle="->", color="#999999", lw=1.6))
ax1.annotate("", xy=(3, 4), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#c0392b", lw=2.4))
ax1.text(1.05, -0.75, "$R$ = 3 $\\Omega$", fontsize=11, color="#2e7d32")
ax1.text(3.2, 1.7, "$X$ = 4 $\\Omega$", fontsize=11, color="#666666")
ax1.text(0.6, 2.5, "$|Z|$ = 5 $\\Omega$", fontsize=11, color="#c0392b")
ax1.text(1.9, 0.6, "53.13°", fontsize=10, color="#c0392b")
ax1.set_title("阻抗三角形（支路 1）", fontsize=11)
ax1.axhline(0, color="#444444", lw=0.8)
ax1.axvline(0, color="#444444", lw=0.8)
ax1.set_aspect("equal")
ax1.set_xlim(-1.2, 5.6)
ax1.set_ylim(-3.0, 5.6)
ax1.grid(alpha=0.3)
ax2.annotate("", xy=(3, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=2.2))
ax2.annotate("", xy=(3, 4), xytext=(3, 0), arrowprops=dict(arrowstyle="->", color="#999999", lw=1.6))
ax2.annotate("", xy=(3, 4), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#c0392b", lw=2.4))
ax2.text(0.75, -0.75, "$P$ = 300 W", fontsize=11, color="#2e7d32")
ax2.text(3.2, 1.7, "$Q$ = 400 var", fontsize=11, color="#666666")
ax2.text(0.5, 2.65, "$S$ = 500 VA", fontsize=11, color="#c0392b")
ax2.text(1.9, 0.6, "53.13°", fontsize=10, color="#c0392b")
ax2.set_title("功率三角形（同形状！乘尺度 $I^2$）", fontsize=11)
ax2.axhline(0, color="#444444", lw=0.8)
ax2.axvline(0, color="#444444", lw=0.8)
ax2.set_aspect("equal")
ax2.set_xlim(-1.2, 5.6)
ax2.set_ylim(-3.0, 5.6)
ax2.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec15_fig2_triangle"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：补偿前后 ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 4.5))
ax1.annotate("", xy=(6, -8), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#1f5fa8", lw=2.2))
ax1.annotate("", xy=(0, 8), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#c0392b", lw=2.2))
ax1.annotate("", xy=(6, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=2.4))
ax1.plot([6, 6], [-8, 0], ls=":", color="#999999", lw=1.0)
ax1.plot([0, 6], [8, 0], ls="--", color="#c0392b", lw=1.0)
ax1.text(6.4, -8.4, "$\\dot I_1$ = 10∠-53.13°", fontsize=10, color="#1f5fa8")
ax1.text(0.5, 8.6, "$\\dot I_C$ = 8∠90°", fontsize=10, color="#c0392b")
ax1.text(6.4, -0.9, "$\\dot I'$ = 6∠0°（补偿后）", fontsize=10, color="#2e7d32")
ax1.set_title("补偿的电流视角：$\\dot I_1 + \\dot I_C = \\dot I'$", fontsize=11)
ax1.axhline(0, color="#444444", lw=0.8)
ax1.axvline(0, color="#444444", lw=0.8)
ax1.set_aspect("equal")
ax1.set_xlim(-1.4, 12.5)
ax1.set_ylim(-10.5, 10.5)
ax1.grid(alpha=0.3)
ax2.annotate("", xy=(3, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=2.2))
ax2.annotate("", xy=(3, 4), xytext=(3, 0), arrowprops=dict(arrowstyle="->", color="#bbbbbb", lw=1.6, ls="--"))
ax2.annotate("", xy=(3, 4), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#bbbbbb", lw=1.8, ls="--"))
ax2.annotate("", xy=(3, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#c0392b", lw=2.6))
ax2.text(0.9, -0.8, "补偿后：$P$ = 300, $Q$ = 0", fontsize=10, color="#c0392b")
ax2.text(3.15, 2.0, "补偿前 $Q$ = 400 var", fontsize=10, color="#888888")
ax2.text(0.4, 2.7, "补偿前 $S$ = 500 VA", fontsize=10, color="#888888")
ax2.set_title("补偿的功率视角：斜边压平成 $S'$ = 300 VA", fontsize=11)
ax2.axhline(0, color="#444444", lw=0.8)
ax2.axvline(0, color="#444444", lw=0.8)
ax2.set_aspect("equal")
ax2.set_xlim(-1.2, 5.6)
ax2.set_ylim(-3.0, 5.6)
ax2.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec15_fig3_compensation"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec15-01 完成。")