# =====================================================================
# lec17-01 第 17 讲《压杆稳定》数字核对与配图
# 规模纪律：总耗时 < 20 秒（三张图 + 数字核对，纯 numpy/matplotlib）。
# 数字核对（圆截面 d=30 mm，L=800 mm，E=200 GPa，Q235）：
#   EXP1 柔度与欧拉临界力：i、lambda、P_cr、sigma_cr
#   EXP2 长度系数 mu 的影响（1 / 2 / 0.5 / 0.7）
#   EXP3 柔度分界：lambda_p=pi*sqrt(E/sigma_p)、lambda_s=(a-sigma_s)/b
#   EXP4 中柔度（直线公式 sigma_cr=a-b*lambda 在 lambda=80）
#   EXP5 稳定校核：n_st = P_cr / P
# 出图（编号按正文出现顺序）：
#   lec17_fig1_equilibrium    稳定/临界/不稳定平衡
#   lec17_fig2_mu_cases       四种约束下的长度系数
#   lec17_fig3_sigma_cr_total 临界应力总图
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 ° 无 →，用 [OK] / -> / deg / ^2）。
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
print("=== 数字核对：第 17 讲 ===")
d, L, E = 30.0, 800.0, 2.0e5
I = np.pi * d ** 4 / 64.0
A = np.pi * d ** 2 / 4.0
i_gyr = np.sqrt(I / A)
lam = L / i_gyr
Pcr = np.pi ** 2 * E * I / (1.0 * L) ** 2
sig_cr = np.pi ** 2 * E / lam ** 2
print("  EXP1 圆截面 d=%.0f, L=%.0f, E=%.0f, 两端铰支（mu=1）：" % (d, L, E))
print("        I=%.1f mm^4, A=%.1f mm^2, i=d/4=%.2f mm -> lambda=%.2f" % (I, A, i_gyr, lam))
print("        P_cr=%.2f kN, sigma_cr=%.1f MPa（=P_cr/A）" % (Pcr / 1e3, sig_cr))

print("  EXP2 长度系数 mu 的影响（P_cr 与 mu^2 成反比）：")
for mu in [1.0, 2.0, 0.5, 0.7]:
    P = np.pi ** 2 * E * I / (mu * L) ** 2
    print("        mu=%.1f -> P_cr=%.2f kN" % (mu, P / 1e3))

sig_p, sig_s, a_l, b_l = 200.0, 235.0, 304.0, 1.12
lam_p = np.pi * np.sqrt(E / sig_p)
lam_s = (a_l - sig_s) / b_l
print("  EXP3 柔度分界：lambda_p=pi*sqrt(E/sigma_p)=%.2f（大/中柔度分界）；"
      "lambda_s=(a-sigma_s)/b=%.2f（中/小柔度分界）" % (lam_p, lam_s))

lam_mid = 80.0
sig_mid = a_l - b_l * lam_mid
print("  EXP4 中柔度（lambda=%.0f，直线公式）：sigma_cr=a-b*lambda=%.1f MPa -> P_cr=%.2f kN"
      % (lam_mid, sig_mid, sig_mid * A / 1e3))

P_work, n_req = 100.0e3, 3.0
n_act = Pcr / P_work
print("  EXP5 稳定校核（P=%.0f kN，要求 n_st=%.1f）：n_st=%.3f -> %s"
      % (P_work / 1e3, n_req, n_act, "安全" if n_act >= n_req else "不安全（需加强约束或加大截面）"))
print("        （若改为一端固定一端铰支 mu=0.7：P_cr=%.2f kN -> n_st=%.2f）"
      % (np.pi ** 2 * E * I / (0.7 * L) ** 2 / 1e3, np.pi ** 2 * E * I / (0.7 * L) ** 2 / P_work))


# ---------------------------------------------------------------------
print()
print("=== 图 1：稳定 / 临界 / 不稳定平衡 ===")
fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.6))
for ax in axes:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")


def draw_column(ax, wobble):
    """wobble=0 直杆；(>0) 侧向挠曲幅值。"""
    yy = np.linspace(0.8, 6.4, 60)
    xx = 5.0 + wobble * np.sin(np.pi * (yy - 0.8) / 5.6)
    ax.plot(xx, yy, color=BLUE, lw=3.2)
    ax.plot([4.3, 5.7], [0.8, 0.8], color=GREY, lw=3)
    ax.annotate("", xy=(5.0, 6.6), xytext=(5.0, 7.6), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
    ax.text(5.3, 7.5, r"$P$（压力）", fontsize=11, color=RED)


draw_column(axes[0], 0.0)
axes[0].text(5.0, 0.2, "(a) $P<P_{cr}$：扰动后回到直线（稳定）", ha="center", fontsize=9.5, color=GREEN)
draw_column(axes[1], 0.6)
axes[1].text(5.0, 0.2, "(b) $P=P_{cr}$：可停留在微弯状态（临界）", ha="center", fontsize=9.5, color=ORANGE)
draw_column(axes[2], 1.3)
axes[2].text(5.0, 0.2, "(c) $P>P_{cr}$：迅速侧弯（失稳）", ha="center", fontsize=9.5, color=RED)
savefig(fig, "lec17_fig1_equilibrium")


# ---------------------------------------------------------------------
print()
print("=== 图 2：四种约束下的长度系数 ===")
fig, axes = plt.subplots(1, 4, figsize=(12.4, 4.2))
cases = [(1.0, "两端铰支", r"$\mu=1$", 0.55),
         (2.0, "一端固定\n一端自由", r"$\mu=2$", 1.1),
         (0.5, "两端固定", r"$\mu=0.5$", 0.9),
         (0.7, "一端固定\n一端铰支", r"$\mu=0.7$", 0.75)]
for ax, (mu, name, mu_txt, amp) in zip(axes, cases):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    if name == "一端固定\n一端自由":
        yy = np.linspace(0.8, 6.6, 60)
        xx = 5.0 - amp * (1 - np.cos(np.pi * (yy - 0.8) / 5.8)) / 2
        ax.plot(xx, yy, color=BLUE, lw=3.0)
        ax.plot([4.2, 5.8], [0.8, 0.8], color=GREY, lw=3)
    elif name == "两端固定":
        yy = np.linspace(0.8, 6.6, 80)
        xx = 5.0 + amp * 0.5 * np.sin(2 * np.pi * (yy - 0.8) / 5.8)
        ax.plot(xx, yy, color=BLUE, lw=3.0)
        ax.plot([4.2, 5.8], [0.8, 0.8], color=GREY, lw=3)
        ax.plot([4.2, 5.8], [6.6, 6.6], color=GREY, lw=3)
    elif name == "一端固定\n一端铰支":
        yy = np.linspace(0.8, 6.6, 80)
        xi = (yy - 0.8) / 5.8
        xx = 5.0 + amp * xi ** 2 * (1 - xi) / 0.1481
        ax.plot(xx, yy, color=BLUE, lw=3.0)
        ax.plot([4.2, 5.8], [0.8, 0.8], color=GREY, lw=3)
        ax.plot([4.5, 5.5], [6.6, 6.6], color=GREY, lw=2)
    else:
        yy = np.linspace(0.8, 6.6, 60)
        xx = 5.0 + amp * np.sin(np.pi * (yy - 0.8) / 5.8)
        ax.plot(xx, yy, color=BLUE, lw=3.0)
        ax.plot([4.4, 5.6], [0.8, 0.8], color=GREY, lw=2)
        ax.plot([4.4, 5.6], [6.6, 6.6], color=GREY, lw=2)
    ax.text(5.0, 7.4, mu_txt, ha="center", fontsize=13, color=RED)
    ax.text(5.0, 0.15, name, ha="center", fontsize=9.5)
savefig(fig, "lec17_fig2_mu_cases")


# ---------------------------------------------------------------------
print()
print("=== 图 3：临界应力总图 ===")
fig, ax = plt.subplots(figsize=(9.0, 5.4))
ax.set_xlim(0, 160)
ax.set_ylim(0, 320)
lam1 = np.linspace(lam_p, 160, 200)
ax.plot(lam1, np.pi ** 2 * E / lam1 ** 2, color=BLUE, lw=2.4)
lam2 = np.linspace(lam_s, lam_p, 100)
ax.plot(lam2, a_l - b_l * lam2, color=ORANGE, lw=2.4)
lam3 = np.linspace(0, lam_s, 50)
ax.plot(lam3, np.full_like(lam3, sig_s), color=GREEN, lw=2.4)
for xv, txt, col in [(lam_p, r"$\lambda_p=%.1f$" % lam_p, BLUE),
                     (lam_s, r"$\lambda_s=%.1f$" % lam_s, ORANGE)]:
    ax.axvline(xv, color=GREY, ls=":", lw=1)
    ax.text(xv + 1.5, 12, txt, fontsize=9.5, color=col)
ax.text(104, 42, r"大柔度" + "\n" + r"$\sigma_{cr}=\dfrac{\pi^2E}{\lambda^2}$", fontsize=10, color=BLUE)
ax.text(78, 250, r"中柔度" + "\n" + r"$\sigma_{cr}=a-b\lambda$", fontsize=10, color=ORANGE)
ax.text(18, 250, r"小柔度" + "\n" + r"$\sigma_{cr}=\sigma_s$", fontsize=10, color=GREEN)
ax.set_xlabel(r"柔度 $\lambda=\mu L/i$", fontsize=11)
ax.set_ylabel(r"临界应力 $\sigma_{cr}$ / MPa", fontsize=11)
ax.set_title("临界应力总图（Q235 示例：a=304, b=1.12, $\\sigma_s$=235）", fontsize=10.5)
savefig(fig, "lec17_fig3_sigma_cr_total")

print()
print("[DONE] 第 17 讲数字核对与三张图全部完成。")