# =====================================================================
# lec21-01 第 21 讲《交变应力与疲劳强度》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 循环特征 r=sigma_min/sigma_max（对称 -1、脉动 0、静载 1）
#   EXP2 平均应力 sigma_m 与应力幅 sigma_a（一般循环的分解与回代互证）
#   EXP3 S-N 幂律 N*sigma^m=C：由 (300 MPa, 1e4) 推 1e6 次时的应力
#   EXP4 构件持久极限 = 材料持久极限 * 尺寸系数 * 表面质量系数 / 有效应力集中系数
#   EXP5 对称循环疲劳校核 n=(sigma_-1)_构/sigma_a
# 出图（编号按正文出现顺序）：
#   lec21_fig1_cycles        三种典型应力循环
#   lec21_fig2_sn_curve      S-N 曲线与持久极限
#   lec21_fig3_factors       影响持久极限的三个系数
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

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
print("=== 数字核对：第 21 讲 ===")
for smax, smin, name in [(100.0, -100.0, "对称循环"), (100.0, 0.0, "脉动循环"),
                         (100.0, 50.0, "一般循环"), (100.0, 100.0, "静载荷")]:
    print("  EXP1 %s：sigma_max=%.0f, sigma_min=%.0f -> r=sigma_min/sigma_max=%.2f"
          % (name, smax, smin, smin / smax))

smax, smin = 120.0, -40.0
sm, sa = (smax + smin) / 2.0, (smax - smin) / 2.0
print("  EXP2 一般循环分解：sigma_max=%.0f, sigma_min=%.0f -> sigma_m=%.1f, sigma_a=%.1f" % (smax, smin, sm, sa))
print("        回代互证：sigma_m+sigma_a=%.1f（=sigma_max）；sigma_m-sigma_a=%.1f（=sigma_min）" % (sm + sa, sm - sa))

sig1, N1, N2, m = 300.0, 1.0e4, 1.0e6, 9.0
sig2 = sig1 * (N1 / N2) ** (1.0 / m)
C = sig1 ** m * N1
print("  EXP3 S-N 幂律 N*sigma^m=C（m=%.0f）：(sigma=%.0f MPa, N=%.0e) -> N=%.0e 时 sigma=%.2f MPa"
      % (m, sig1, N1, N2, sig2))
print("        互证：C=sigma1^m*N1=%.4e；用 C 反算 sigma2=%.2f MPa" % (C, (C / N2) ** (1.0 / m)))

s_1, k_sig, eps, beta = 250.0, 2.0, 0.8, 0.85
s_1_comp = s_1 * eps * beta / k_sig
print("  EXP4 构件持久极限：sigma_-1=%.0f, k_sigma=%.1f, eps=%.2f, beta=%.2f" % (s_1, k_sig, eps, beta))
print("        (sigma_-1)_构件 = %.0f*%.2f*%.2f/%.1f = %.2f MPa" % (s_1, eps, beta, k_sig, s_1_comp))

n_req = 1.5
for sa_work in [50.0, 70.0]:
    n_act = s_1_comp / sa_work
    print("  EXP5 疲劳校核（sigma_a=%.0f MPa, [n]=%.1f）：n=%.3f -> %s"
          % (sa_work, n_req, n_act, "安全" if n_act >= n_req else "不合格"))


# ---------------------------------------------------------------------
print()
print("=== 图 1：三种典型应力循环 ===")
fig, axes = plt.subplots(1, 3, figsize=(11.8, 4.0))
tt = np.linspace(0, 2, 400)


def draw_cycle(ax, curve, title, note):
    ax.set_xlim(0, 2)
    ax.set_ylim(-1.5, 1.5)
    ax.axhline(0, color=GREY, lw=1)
    ax.plot(tt, curve, color=BLUE, lw=2.2)
    ax.set_xlabel("t", fontsize=10)
    ax.set_ylabel(r"$\sigma$", fontsize=10)
    ax.set_title(title, fontsize=10.5)
    ax.text(1.0, -1.42, note, ha="center", fontsize=9, color=RED)


draw_cycle(axes[0], np.sin(2 * np.pi * tt), r"对称循环 $r=-1$", r"$\sigma_{\max}=-\sigma_{\min}$")
draw_cycle(axes[1], 0.5 * (1 - np.cos(2 * np.pi * tt)), r"脉动循环 $r=0$", r"$\sigma_{\min}=0$")
draw_cycle(axes[2], np.full_like(tt, 1.0), r"静载荷 $r=+1$", r"$\sigma_{\max}=\sigma_{\min}$")
savefig(fig, "lec21_fig1_cycles")


# ---------------------------------------------------------------------
print()
print("=== 图 2：S-N 曲线与持久极限 ===")
fig, ax = plt.subplots(figsize=(8.8, 5.0))
NN = np.logspace(3, 8, 300)
mm = 9.0
sig_curve = sig1 * (N1 / NN) ** (1.0 / mm)
sig_curve = np.maximum(sig_curve, 180.0)
ax.semilogx(NN, sig_curve, color=BLUE, lw=2.4)
ax.axhline(180.0, color=RED, ls="--", lw=1.6)
ax.text(3e3, 186, r"持久极限 $\sigma_{-1}$（曲线变水平）", fontsize=9.5, color=RED)
ax.plot([N1], [sig1], "o", color=GREEN, ms=6)
ax.text(N1 * 1.3, sig1 + 4, r"$(N_1,\sigma_1)$：高应力、寿命短", fontsize=9, color=GREEN)
ax.set_xlabel(r"循环次数 $N$（对数坐标）", fontsize=11)
ax.set_ylabel(r"最大应力 $\sigma_{\max}$ / MPa", fontsize=11)
ax.set_ylim(150, 330)
ax.set_title(r"S-N 曲线：$N\sigma^m=C$，超过约 $10^6$ 次后曲线水平", fontsize=10.5)
savefig(fig, "lec21_fig2_sn_curve")


# ---------------------------------------------------------------------
print()
print("=== 图 3：影响持久极限的三个系数 ===")
fig, axes = plt.subplots(1, 3, figsize=(11.8, 4.2))
for ax in axes:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

# (a) 有效应力集中系数
axes[0].plot([1.0, 4.6, 4.6, 9.0], [3.0, 3.0, 4.6, 4.6], color=GREY, lw=8, solid_capstyle="butt")
axes[0].annotate("", xy=(4.6, 5.6), xytext=(7.0, 5.6), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))
axes[0].text(5.0, 5.8, "缺口/圆角", fontsize=9.5, color=RED)
axes[0].text(5.0, 1.8, r"$k_\sigma>1$（应力集中，最不利）", ha="center", fontsize=10, color=BLUE)
axes[0].text(5.0, 1.0, "(a) 构件外形", ha="center", fontsize=10.5, weight="bold")

# (b) 尺寸系数
axes[1].add_patch(Rectangle((2.0, 3.4), 2.0, 1.6, fc="#e7f0fb", ec=BLUE))
axes[1].add_patch(Rectangle((5.6, 2.9), 3.0, 2.6, fc="#cfe3f7", ec=BLUE))
axes[1].text(3.0, 4.2, "小", ha="center", fontsize=11)
axes[1].text(7.1, 4.2, "大", ha="center", fontsize=11)
axes[1].text(5.0, 1.8, r"$\varepsilon\leq 1$（尺寸越大越不利）", ha="center", fontsize=10, color=BLUE)
axes[1].text(5.0, 1.0, "(b) 构件尺寸", ha="center", fontsize=10.5, weight="bold")

# (c) 表面质量系数
axes[2].add_patch(Rectangle((3.0, 2.8), 4.0, 2.2, fc="#e8f5e9", ec=GREEN))
xx = np.linspace(3.0, 7.0, 60)
axes[2].plot(xx, 5.0 + 0.12 * np.sin(12 * xx), color=GREEN, lw=1.4)
axes[2].text(5.0, 3.9, "表面粗糙", ha="center", fontsize=10)
axes[2].text(5.0, 1.8, r"$\beta\leq 1$（越粗糙越不利）", ha="center", fontsize=10, color=BLUE)
axes[2].text(5.0, 1.0, "(c) 表面加工质量", ha="center", fontsize=10.5, weight="bold")
savefig(fig, "lec21_fig3_factors")

print()
print("[DONE] 第 21 讲数字核对与三张图全部完成。")