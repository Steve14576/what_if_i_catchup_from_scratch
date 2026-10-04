# =====================================================================
# lec13-01 相量法基础：旋转投影、相量运算、有效值、微分性质
#          （第 13 讲 §1-§2 数值实验；图 1 旋转投影、图 2 RMS 家族）
# 规模纪律：总耗时 < 10 秒（numpy 向量化 + 两张图）。
#
# 内容：
#   实验 1：旋转与投影——Re(e^(jwt)) = cos(wt)；三个时刻的演示。
#   实验 2：同频相加——6cos(wt-53.13)+8cos(wt+36.87) = 10cos(wt)；
#           异频反例——10cos(1000t)+10cos(1200t) 是拍频（非单频）。
#   实验 3：有效值——5 种波形数值 RMS vs 理论（Um=1）。
#   实验 4：微分性质——sqrt(2)*5cos(1000t+20) 的数值微分 vs 相量预测。
#   并生成 figures/lec13_fig1_rotation.svg/.png 与 lec13_fig2_rms.svg/.png。
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

# ---------------------------------------------------------------------
print("=== 实验 1：旋转与投影（Re(e^(jwt)) = cos(wt)） ===")
w = 1000.0
t = np.linspace(0, 2 * np.pi / w, 4000)
err = np.max(np.abs(np.real(np.exp(1j * w * t)) - np.cos(w * t)))
print("  max|Re(e^(jwt)) - cos(wt)| = %.2e（同一个数的两种写法）" % err)
for deg in [40, 140, 250]:
    print("  wt = %d°：矢量位置 (%.4f, %.4f)，实轴投影 = cos = %.4f"
          % (deg, np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg)), np.cos(np.deg2rad(deg))))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：同频相加与异频反例 ===")
ang1 = np.arctan(4 / 3)          # 53.1301...°（精确值）
ang2 = np.arctan(3 / 4)          # 36.8699...°
t2 = np.linspace(0, 4 * np.pi / w, 8000)
x1 = 6 * np.cos(w * t2 - ang1)
x2 = 8 * np.cos(w * t2 + ang2)
x_sum = 10 * np.cos(w * t2)
print("  同频：max|(x1+x2) - 10cos(wt)| = %.2e（相量 6∠-53.13° + 8∠36.87° = 10∠0°）"
      % np.max(np.abs(x1 + x2 - x_sum)))
x3 = 10 * np.cos(1000 * t2)
x4 = 10 * np.cos(1200 * t2)
env = 2 * 10 * np.abs(np.cos(100 * t2))
print("  异频：x3 + x4 的包络 = |20cos(100t)|（拍频），不是单频正弦——相量无从相加")
print("  （拍频周期：T_beat = 2pi/100 = %.1f ms）" % (2 * np.pi / 100 * 1e3))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：有效值——5 种波形（Um = 1，周期 1） ===")
tb = np.linspace(0, 1, 20001)
um = 1.0
waves = [
    ("正弦", um * np.sin(2 * np.pi * tb), 1 / np.sqrt(2)),
    ("对称方波", um * np.where(np.sin(2 * np.pi * tb) >= 0, 1.0, -1.0), 1.0),
    ("三角波", um * (2 * np.abs(2 * (tb % 1) - 1) - 1), 1 / np.sqrt(3)),
    ("半波整流正弦", um * np.maximum(np.sin(2 * np.pi * tb), 0), 0.5),
    ("全波整流正弦", um * np.abs(np.sin(2 * np.pi * tb)), 1 / np.sqrt(2)),
]
print("  波形            数值 RMS    理论值")
for name, xw, thv in waves:
    rms = np.sqrt(np.trapezoid(xw ** 2, tb))
    print("  %-12s    %.4f      %.4f" % (name, rms, thv))
print("  工程例：220 V（有效值）对应的峰值 = 220*sqrt(2) = %.0f V" % (220 * np.sqrt(2)))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：微分性质——数值微分 vs 相量预测 ===")
dt = 1e-7
t4 = np.arange(0, 1.5 * 2 * np.pi / w, dt)
x4t = np.sqrt(2) * 5 * np.cos(w * t4 + np.deg2rad(20))
dx_num = np.gradient(x4t, dt, edge_order=2)
dx_th = np.sqrt(2) * 5000 * np.cos(w * t4 + np.deg2rad(110))
print("  x(t) = sqrt(2)*5cos(1000t+20°)；相量 5∠20° -> jw 乘后 5000∠110°")
print("  数值微分 vs 相量预测 max 偏差 = %.2e" % np.max(np.abs(dx_num - dx_th)))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：旋转矢量与投影 ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
th = np.linspace(0, 2 * np.pi, 400)
ax1.plot(np.cos(th), np.sin(th), color="#999999", lw=1.0, ls="--")
colors = [(40, "#1f5fa8"), (140, "#c0392b"), (250, "#2e7d32")]
for deg, cc in colors:
    r = np.deg2rad(deg)
    ax1.annotate("", xy=(np.cos(r), np.sin(r)), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=cc, lw=2.2))
    ax1.plot([np.cos(r), np.cos(r)], [0, np.sin(r)], ls=":", color=cc, lw=1.1)
    ax1.plot([np.cos(r)], [0], "o", color=cc, ms=6)
ax1.axhline(0, color="#444444", lw=0.8)
ax1.axvline(0, color="#444444", lw=0.8)
ax1.set_aspect("equal")
ax1.set_xlim(-1.35, 1.35)
ax1.set_ylim(-1.35, 1.35)
ax1.set_xlabel("实轴（投影轴）")
ax1.set_title("旋转矢量 $e^{j\\omega t}$：模 1、角 $\\omega t$", fontsize=11)
ax1.annotate("实心点 = 实轴投影 = $\\cos\\omega t$", xy=(0.77, 0), xytext=(-1.3, -1.2),
             fontsize=10, color="#333333")

degs = np.linspace(0, 360, 800)
ax2.plot(degs, np.cos(np.deg2rad(degs)), color="#1f5fa8", lw=2.0)
for deg, cc in colors:
    ax2.plot([deg], [np.cos(np.deg2rad(deg))], "o", color=cc, ms=6)
    ax2.annotate("$\\omega t$ = %d°" % deg, xy=(deg, np.cos(np.deg2rad(deg))),
                 xytext=(deg + 14, np.cos(np.deg2rad(deg)) + (0.28 if deg != 250 else -0.34)),
                 fontsize=9, color=cc)
ax2.axhline(0, color="#444444", lw=0.8)
ax2.set_xlabel("相位 $\\omega t$ / 度")
ax2.set_ylabel("$\\cos\\omega t$")
ax2.set_title("展开到时域：投影点走过的波形", fontsize=11)
ax2.set_xlim(0, 360)
ax2.set_ylim(-1.35, 1.35)
ax2.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec13_fig1_rotation"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：RMS 家族（三种波形） ===")
fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.8))
tfig = np.linspace(0, 2, 1200)
um2 = 10.0
panels = [
    ("正弦：RMS = $U_m/\\sqrt{2}$", um2 * np.sin(2 * np.pi * tfig), um2 / np.sqrt(2), "#1f5fa8"),
    ("对称方波：RMS = $U_m$", um2 * np.where(np.sin(2 * np.pi * tfig) >= 0, 1.0, -1.0), um2, "#c0392b"),
    ("三角波：RMS = $U_m/\\sqrt{3}$", um2 * (2 * np.abs(2 * (tfig % 1) - 1) - 1), um2 / np.sqrt(3), "#2e7d32"),
]
for ax, (title, wave, rmsv, cc) in zip(axes, panels):
    ax.plot(tfig, wave, color=cc, lw=1.8)
    ax.axhline(rmsv, color="#666666", ls="--", lw=1.0)
    ax.axhline(-rmsv, color="#666666", ls="--", lw=1.0)
    ax.axhline(um2, color="#bbbbbb", ls=":", lw=0.9)
    ax.axhline(-um2, color="#bbbbbb", ls=":", lw=0.9)
    ax.set_title(title + "\n（虚线 = RMS %.2f V，点线 = 峰值 %.0f V）" % (rmsv, um2), fontsize=10)
    ax.set_xlabel("时间 / 周期")
    ax.set_ylim(-12, 12)
    ax.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec13_fig2_rms"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec13-01 完成。")