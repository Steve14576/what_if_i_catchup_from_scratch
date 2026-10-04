# =====================================================================
# lec16-01 三相电路：对称量、一相法、功率、不对称与中线
#          （第 16 讲 §1-§4 数值实验；图 1 波形、图 2 相量图、图 3 端子图）
# 规模纪律：总耗时 < 10 秒（numpy 向量化 + 三张图）。
#
# 主例：对称 Y-Y：相电压 100 V（A 相 0°）、每相负载 Z = 3+4j = 5∠53.13°。
#   相电流 20∠-53.13°（±120° 轮换）；中线电流 0；
#   线电压 = 100√3∠30° = 173.2∠30°；三相 P = 3600 W、Q = 4800 var、S = 6000 VA
#   （3U_pI_pcosφ 与 √3U_lI_lcosφ 双公式互验）；
#   对称三相瞬时总功率恒定 3600 W（三个 2w 波动互差 120° 抵消）。
# 不对称（10/20/20）：带中线各相独立、中线电流 5∠0°；
#   断中线：中性点偏移 25∠0° -> A 相 75 V（欠）、B/C 相 114.56 V（过）。
# 一相断开（B/C 各 10 ohm）：中性点 -50 -> 两相各 86.60 V（=线电压/2）、
#   电流 8.66 A（串联分压）。
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
Up = 100.0
Z = 3 + 4j

# ---------------------------------------------------------------------
print("=== 实验 1：对称三相的量（主例） ===")
ang = np.arctan(4 / 3)
UA = Up * np.exp(1j * 0)
UB = Up * np.exp(-1j * 2 * np.pi / 3)
UC = Up * np.exp(+1j * 2 * np.pi / 3)
IA = UA / Z
IB = UB / Z
IC = UC / Z
IN = IA + IB + IC
UAB = UA - UB
print("  相电压：100∠0° / 100∠-120° / 100∠+120°")
print("  相电流：%.0f∠%.4f° / %.0f∠%.4f° / %.0f∠%.4f°（有效值都是 %.0f A）"
      % (abs(IA), np.degrees(np.angle(IA)), abs(IB), np.degrees(np.angle(IB)),
         abs(IC), np.degrees(np.angle(IC)), abs(IA)))
print("  中线电流 |I_N| = %.2e A（对称 -> 零）" % abs(IN))
print("  线电压 U_AB = %.1f∠%.4f° V（= 100√3∠30°，√3 与 30° 的来历）"
      % (abs(UAB), np.degrees(np.angle(UAB))))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：三相功率与瞬时功率恒定 ===")
Ip = abs(IA)
P3 = 3 * Up * Ip * np.cos(ang)
Q3 = 3 * Up * Ip * np.sin(ang)
S3 = 3 * Up * Ip
Ul = abs(UAB)
print("  3 倍法：P = 3x100x20xcos53.13° = %.0f W；Q = %.0f var；S = %.0f VA" % (P3, Q3, S3))
print("  √3 法：P = √3 x %.1f x %.0f x 0.6 = %.0f W（两法一致）" % (Ul, Ip, np.sqrt(3) * Ul * Ip * np.cos(ang)))
# 瞬时功率恒定：p_A = 1200 + 2000cos(2wt - 53.13°) 等
T2 = 2 * 2 * np.pi / w
t = np.linspace(0, T2, 20001)
pA = 100 * np.sqrt(2) * np.cos(w * t) * 20 * np.sqrt(2) * np.cos(w * t - ang)
pB = 100 * np.sqrt(2) * np.cos(w * t - 2 * np.pi / 3) * 20 * np.sqrt(2) * np.cos(w * t - 2 * np.pi / 3 - ang)
pC = 100 * np.sqrt(2) * np.cos(w * t + 2 * np.pi / 3) * 20 * np.sqrt(2) * np.cos(w * t + 2 * np.pi / 3 - ang)
ptot = pA + pB + pC
print("  对称三相瞬时总功率：均值 %.2f W，最大偏差 %.2e W（恒定不波动！）"
      % (np.mean(ptot), np.max(np.abs(ptot - 3600))))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：不对称负载 10/20/20（有中线 vs 无中线） ===")
# 有中线
IA2 = UA / 10
IB2 = UB / 20
IC2 = UC / 20
IN2 = IA2 + IB2 + IC2
print("  有中线：I_A = %.0f∠0°、I_B = %.0f∠-120°、I_C = %.0f∠+120°；中线电流 = %.0f∠%.0f° A"
      % (abs(IA2), abs(IB2), abs(IC2), abs(IN2), np.degrees(np.angle(IN2))))
# 无中线：结点法
YA, YB, YC = 1 / 10, 1 / 20, 1 / 20
Un = (YA * UA + YB * UB + YC * UC) / (YA + YB + YC)
UA2 = UA - Un
UB2 = UB - Un
UC2 = UC - Un
print("  无中线：中性点偏移 U_n = %.0f∠%.0f° V" % (abs(Un), np.degrees(np.angle(Un))))
print("  A 相负载电压 %.0f V（欠！原 100）；B/C 相 %.2f V（过！）" % (abs(UA2), abs(UB2)))
print("  （114.56 = 25√21 的近似：B/C 相被顶到 %.2f∠%.1f°）" % (abs(UB2), np.degrees(np.angle(UB2))))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：一相断开（B/C 各 10 ohm，A 相开路） ===")
YB2, YC2 = 1 / 10, 1 / 10
Un3 = (YB2 * UB + YC2 * UC) / (YB2 + YC2)
UB3 = UB - Un3
UC3 = UC - Un3
print("  中性点 U_n = %.0f V；两相各分 %.2f V（= 线电压 %.1f / 2 = %.1f）"
      % (abs(Un3), abs(UB3), abs(UAB), abs(UAB) / 2))
print("  电流 |I_B| = |I_C| = %.2f A；两相电压反相（串联回路）" % (abs(UB3) / 10))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：三相波形（相差 120°） ===")
fig, ax = plt.subplots(figsize=(9.8, 4.4))
deg = np.linspace(0, 720, 2000)
r = np.deg2rad(deg)
ax.plot(deg, np.cos(r), color="#c0392b", lw=2.0, label="$u_A$")
ax.plot(deg, np.cos(r - 2 * np.pi / 3), color="#1f5fa8", lw=2.0, label="$u_B$")
ax.plot(deg, np.cos(r + 2 * np.pi / 3), color="#2e7d32", lw=2.0, label="$u_C$")
for d0, cc in [(0, "#c0392b"), (240, "#1f5fa8"), (120, "#2e7d32")]:
    ax.plot([d0], [1], "o", color=cc, ms=5)
ax.annotate("相序 A -> B -> C：B 滞后 A 120°，C 超前 A 120°", xy=(100, 0.5), xytext=(315, 1.35),
            fontsize=10, color="#333333")
ax.axhline(0, color="#444444", lw=0.8)
ax.set_xlabel("相位 $\\omega t$ / 度")
ax.set_ylabel("归一化电压")
ax.set_title("对称三相：同一振幅、互差 120°（图中峰值依次出现在 0° / 240° / 120°）", fontsize=11)
ax.legend(fontsize=10, loc="lower right")
ax.set_xlim(0, 720)
ax.set_ylim(-1.5, 1.6)
ax.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec16_fig1_waveforms"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：三相电压相量图与线电压合成 ===")
fig, ax = plt.subplots(figsize=(7.2, 5.6))
ax.annotate("", xy=(100, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#c0392b", lw=2.4))
ax.annotate("", xy=(-50, -86.6), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#1f5fa8", lw=2.4))
ax.annotate("", xy=(-50, 86.6), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=2.4))
ax.annotate("", xy=(150, 86.6), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#e67e22", lw=2.8))
ax.plot([-50, 150], [-86.6, 86.6], ls="--", color="#999999", lw=1.1)
ax.plot([100, 150], [0, 86.6], ls="--", color="#999999", lw=1.1)
ax.text(101, -9, "$\\dot U_A$ = 100∠0°", fontsize=10, color="#c0392b")
ax.text(-96, -100, "$\\dot U_B$", fontsize=10, color="#1f5fa8")
ax.text(-96, 90, "$\\dot U_C$", fontsize=10, color="#2e7d32")
ax.text(120, 96, "$\\dot U_{AB}$ = 173.2∠30°（= √3 倍，超前 30°）", fontsize=10, color="#e67e22")
ax.annotate("30°", xy=(30, 10), fontsize=11, color="#e67e22")
ax.axhline(0, color="#444444", lw=0.8)
ax.axvline(0, color="#444444", lw=0.8)
ax.set_aspect("equal")
ax.set_xlim(-135, 240)
ax.set_ylim(-135, 135)
ax.set_xlabel("实轴 / V")
ax.set_title("三相电压相量与 $\\dot U_{AB} = \\dot U_A - \\dot U_B$", fontsize=11)
ax.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec16_fig2_phasor"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：三相四线制端子图（220 / 380 在哪） ===")
fig, ax = plt.subplots(figsize=(8.6, 4.6))
A, B, C, N = (1.2, 3.0), (3.6, 3.0), (6.0, 3.0), (3.6, 0.8)
for P, name in [(A, "A"), (B, "B"), (C, "C"), (N, "N")]:
    ax.plot([P[0]], [P[1]], "o", color="#333333", ms=7)
    ax.text(P[0] - 0.12, P[1] + 0.16, name, fontsize=13)
ax.plot([A[0], B[0]], [A[1], B[1]], color="#c0392b", lw=2.0)
ax.plot([B[0], C[0]], [B[1], C[1]], color="#c0392b", lw=2.0)
ax.plot([B[0], N[0]], [B[1], N[1]], ls=":", color="#1f5fa8", lw=1.8)
ax.annotate("", xy=(B[0], 2.45), xytext=(A[0], 2.45), arrowprops=dict(arrowstyle="<->", color="#c0392b", lw=1.4))
ax.text(1.6, 2.0, "线电压 380 V（火-火）", fontsize=11, color="#c0392b")
ax.annotate("", xy=(3.15, B[1]), xytext=(3.15, N[1]), arrowprops=dict(arrowstyle="<->", color="#1f5fa8", lw=1.4))
ax.text(3.8, 1.55, "相电压 220 V（火-零）", fontsize=11, color="#1f5fa8")
ax.text(6.3, 0.62, "中性线 N（零线）", fontsize=11, color="#333333")
ax.text(0.2, 3.35, "三根相线（火线）", fontsize=11, color="#c0392b")
ax.set_title("三相四线制：同一张网，两种读数（220 = 380 / √3）", fontsize=12)
ax.set_xlim(-0.3, 9.2)
ax.set_ylim(0.2, 3.9)
ax.axis("off")
plt.tight_layout()
save_stem = "lec16_fig3_terminals"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec16-01 完成。")