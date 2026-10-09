# =====================================================================
# lec15-01 第 15 讲《强度理论》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对：
#   EXP1 一般三向状态（s1=100,s2=50,s3=-20; mu=0.3）的四个相当应力
#   EXP2 薄壁圆筒（D=1000,t=10,p=1 MPa）：sigma_theta、sigma_z 与相当应力
#   EXP3 纯剪切：sigma_r3=2*tau、sigma_r4=sqrt(3)*tau（经典结果核对）
#   EXP4 弯扭组合：sigma_r3=sqrt(sigma^2+4tau^2)、sigma_r4=sqrt(sigma^2+3tau^2)
# 出图（编号按正文出现顺序）：
#   lec15_fig1_four_theories   四个强度理论的控制因素
#   lec15_fig2_sigma_r_compare  同一状态下四个相当应力对比
#   lec15_fig3_thin_cylinder    薄壁圆筒（内压容器）的应力
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


def sr1(s1, s2, s3):
    return s1


def sr2(s1, s2, s3, mu=0.3):
    return s1 - mu * (s2 + s3)


def sr3(s1, s2, s3):
    return s1 - s3


def sr4(s1, s2, s3):
    return np.sqrt(0.5 * ((s1 - s2) ** 2 + (s2 - s3) ** 2 + (s3 - s1) ** 2))


# ---------------------------------------------------------------------
print("=== 数字核对：第 15 讲 ===")
s1, s2, s3 = 100.0, 50.0, -20.0
print("  EXP1 一般三向（s1=%.0f,s2=%.0f,s3=%.0f, mu=0.3）：" % (s1, s2, s3))
print("        sigma_r1=%.1f, sigma_r2=%.1f, sigma_r3=%.1f, sigma_r4=%.1f MPa"
      % (sr1(s1, s2, s3), sr2(s1, s2, s3), sr3(s1, s2, s3), sr4(s1, s2, s3)))

D, t, p = 1000.0, 10.0, 1.0
sth = p * D / (2 * t)
sz = p * D / (4 * t)
print("  EXP2 薄壁圆筒（D=%.0f, t=%.0f, p=%.1f MPa）：sigma_theta=%.1f, sigma_z=%.1f MPa" % (D, t, p, sth, sz))
print("        主应力 (%.1f, %.1f, 0) -> sigma_r3=%.1f, sigma_r4=%.1f MPa"
      % (sth, sz, sr3(sth, sz, 0), sr4(sth, sz, 0)))

tau = 100.0
print("  EXP3 纯剪切（tau=%.0f）：sigma_r3=2tau=%.1f；sigma_r4=sqrt(3)tau=%.2f"
      % (tau, 2 * tau, np.sqrt(3) * tau))
print("        （互证：sqrt(3)*tau = %.4f）" % (np.sqrt(3) * tau,))

sig, txy = 100.0, 40.0
R = np.sqrt((sig / 2) ** 2 + txy ** 2)
sp1, sp2, sp3 = sig / 2 + R, 0.0, sig / 2 - R
sr3_bt = np.sqrt(sig ** 2 + 4 * txy ** 2)
sr4_bt = np.sqrt(sig ** 2 + 3 * txy ** 2)
print("  EXP4 弯扭组合（sigma=%.0f, tau=%.0f）：主应力 (%.2f, %.2f, %.2f)" % (sig, txy, sp1, sp2, sp3))
print("        sigma_r3=sqrt(s^2+4t^2)=%.2f（主应力法 %0.2f）；sigma_r4=sqrt(s^2+3t^2)=%.2f（主应力法 %.2f）"
      % (sr3_bt, sr3(sp1, sp2, sp3), sr4_bt, sr4(sp1, sp2, sp3)))


# ---------------------------------------------------------------------
print()
print("=== 图 1：四个强度理论的控制因素 ===")
fig, axes = plt.subplots(2, 2, figsize=(9.6, 7.2))
for ax in axes.ravel():
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

# (1) 最大拉应力
ax = axes[0, 0]
ax.add_patch(Rectangle((3.5, 4), 3, 2, fc="#e7f0fb", ec=BLUE))
ax.annotate("", xy=(2.6, 5.0), xytext=(3.5, 5.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.annotate("", xy=(7.4, 5.0), xytext=(6.5, 5.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(5, 6.6, "拉断由最大拉应力控制", ha="center", fontsize=9.5, color=RED)
ax.text(5, 2.6, r"$\sigma_{r1}=\sigma_1$", ha="center", fontsize=12, color=BLUE)
ax.text(5, 8.6, "第一强度理论（最大拉应力）", ha="center", fontsize=10, weight="bold")

# (2) 最大伸长线应变
ax = axes[0, 1]
ax.add_patch(Rectangle((3.2, 4.4), 3.6, 1.2, fc="#e7f0fb", ec=BLUE))
ax.annotate("", xy=(2.4, 5.0), xytext=(3.2, 5.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.annotate("", xy=(7.6, 5.0), xytext=(6.8, 5.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.annotate("", xy=(5, 3.6), xytext=(5, 4.3), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.5))
ax.annotate("", xy=(5, 6.4), xytext=(5, 5.7), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.5))
ax.text(5, 6.9, r"纵向伸长（应变 $\varepsilon_1$）控制", ha="center", fontsize=9.5, color=RED)
ax.text(5, 2.6, r"$\sigma_{r2}=\sigma_1-\mu(\sigma_2+\sigma_3)$", ha="center", fontsize=11, color=BLUE)
ax.text(5, 8.6, "第二强度理论（最大伸长线应变）", ha="center", fontsize=10, weight="bold")

# (3) 最大切应力
ax = axes[1, 0]
ax.add_patch(Rectangle((3.5, 4), 3, 2, fc="#fde9d9", ec=ORANGE))
ax.annotate("", xy=(6.5, 6.0), xytext=(3.5, 6.0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2))
ax.annotate("", xy=(3.5, 4.0), xytext=(6.5, 4.0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2))
ax.text(5, 6.9, "屈服由最大切应力控制", ha="center", fontsize=9.5, color=GREEN)
ax.text(5, 2.6, r"$\sigma_{r3}=\sigma_1-\sigma_3$", ha="center", fontsize=12, color=BLUE)
ax.text(5, 8.6, "第三强度理论（最大切应力）", ha="center", fontsize=10, weight="bold")

# (4) 畸变能密度
ax = axes[1, 1]
ax.add_patch(Polygon([[3.5, 4.4], [6.5, 4.0], [6.9, 5.8], [3.9, 6.2]], closed=True, fc="#e8f5e9", ec=GREEN))
ax.annotate("", xy=(7.6, 5.1), xytext=(6.6, 5.1), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
ax.text(5, 6.9, "屈服由形状改变（畸变）能量控制", ha="center", fontsize=9.5, color=GREEN)
ax.text(5, 2.6, r"$\sigma_{r4}=\sqrt{\frac{1}{2}[(\sigma_1-\sigma_2)^2+(\sigma_2-\sigma_3)^2+(\sigma_3-\sigma_1)^2]}$",
        ha="center", fontsize=9.5, color=BLUE)
ax.text(5, 8.6, "第四强度理论（畸变能密度）", ha="center", fontsize=10, weight="bold")
savefig(fig, "lec15_fig1_four_theories")


# ---------------------------------------------------------------------
print()
print("=== 图 2：四个相当应力对比 ===")
fig, ax = plt.subplots(figsize=(8.0, 4.6))
vals = [sr1(s1, s2, s3), sr2(s1, s2, s3), sr3(s1, s2, s3), sr4(s1, s2, s3)]
labels = [r"$\sigma_{r1}$", r"$\sigma_{r2}$", r"$\sigma_{r3}$", r"$\sigma_{r4}$"]
colors = [BLUE, GREEN, RED, ORANGE]
bars = ax.bar(labels, vals, color=colors, width=0.55)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 2, "%.1f" % v, ha="center", fontsize=10)
ax.set_ylim(0, 140)
ax.set_ylabel("相当应力 / MPa", fontsize=10)
ax.set_title(r"同一状态 $(\sigma_1,\sigma_2,\sigma_3)=(100,50,-20)$ 的四个相当应力", fontsize=10.5)
ax.axhline(max(vals), color=GREY, ls=":", lw=1)
ax.text(3.35, max(vals) + 4, "上限（第三理论最保守）", ha="right", fontsize=8.5, color=GREY)
savefig(fig, "lec15_fig2_sigma_r_compare")


# ---------------------------------------------------------------------
print()
print("=== 图 3：薄壁圆筒的应力 ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 4.4))
for ax in (a1, a2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect("equal")
    ax.axis("off")

# (a) 圆筒
a1.add_patch(Rectangle((2.0, 1.8), 6.0, 2.4, fc="#eef2f7", ec=GREY))
a1.add_patch(Rectangle((2.0, 2.5), 6.0, 1.0, fc="#e7f0fb", ec=BLUE))
# 内压箭头
for xx in np.linspace(2.6, 7.4, 6):
    a1.annotate("", xy=(xx, 2.5), xytext=(xx, 2.1), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
    a1.annotate("", xy=(xx, 3.5), xytext=(xx, 3.9), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
a1.text(5.0, 1.3, r"内压 $p$（向外胀）", ha="center", fontsize=9, color=RED)
# 环向/轴向应力标注
a1.text(5.0, 3.0, r"$\sigma_\theta$", ha="center", fontsize=13, color=GREEN)
a1.text(5.0, 5.3, r"环向 $\sigma_\theta=\dfrac{pD}{2t}$；轴向 $\sigma_z=\dfrac{pD}{4t}$", ha="center", fontsize=9.5, color=BLUE)
a1.text(5.0, 0.6, "(a) 薄壁圆筒受内压", ha="center", fontsize=11, weight="bold")

# (b) 单元体
a2.add_patch(Rectangle((3.5, 2.0), 3.0, 2.0, fc="#fde9d9", ec=ORANGE))
a2.annotate("", xy=(8.0, 3.0), xytext=(6.6, 3.0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2))
a2.annotate("", xy=(2.0, 3.0), xytext=(3.4, 3.0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2))
a2.annotate("", xy=(5.0, 5.2), xytext=(5.0, 4.1), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2))
a2.annotate("", xy=(5.0, 0.8), xytext=(5.0, 1.9), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2))
a2.text(8.2, 3.2, r"$\sigma_\theta$", fontsize=12, color=GREEN)
a2.text(5.2, 5.4, r"$\sigma_z$", fontsize=12, color=BLUE)
a2.text(5.0, 3.55, r"$\sigma_\theta>\sigma_z$", fontsize=9.5, color=ORANGE)
a2.text(5.0, 0.2, "(b) 二向应力状态（危险点单元体）", ha="center", fontsize=11, weight="bold")
savefig(fig, "lec15_fig3_thin_cylinder")

print()
print("[DONE] 第 15 讲数字核对与三张图全部完成。")