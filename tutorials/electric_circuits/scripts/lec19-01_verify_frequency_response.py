# =====================================================================
# lec19-01 电路的频率响应：串联谐振扫频、三 Q 对照、并联谐振、网络函数两副面孔、RC 低通
#          （第 19 讲 §1-§5 数值实验；图 1 串联 RLC、图 2 三 Q 幅频、图 3 两副面孔）
# 规模纪律：总耗时 < 10 秒（一维扫频 + 解析计算 + 三张图）。
#
# 主例：串联 RLC：R = 10 欧、L = 100 mH、C = 10 uF、Vs = 10 V。
#   w0 = 1/sqrt(LC) = 1000 rad/s；Q = w0 L/R = 10；BW = w0/Q = 100 rad/s。
#   谐振：Z = R = 10；I = 1 A；U_C = U_L = Q Vs = 100 V。
#   半功率点：w1 = 951.25、w2 = 1051.25（BW = 100）。
# 三 Q 对照：R = 5/10/20 -> Q = 20/10/5（|H_R| 峰都是 1，宽窄不同）。
# 并联：R = 1 k、同 L/C、Vs = 10 V：Z 峰 = 1 k（@w0）；I 总最小 = 10 mA；
#   支路 I_L = I_C = 100 mA（= Q x I 总）；Q_p = R/(w0 L) = 10。
# 网络函数：H_R = jwRC/(1 - w^2 LC + jwRC)（带通，峰 1）；H_C = 1/(...)（低通带峰，峰 Q = 10）。
# RC 低通：R = 1 k、C = 100 nF -> wc = 1e4；10 倍频程 -20 dB 斜率。
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

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

elm.style(elm.STYLE_IEC)
schemdraw.config(font="Microsoft YaHei", fontsize=13)

R, L, C, Vs = 10.0, 0.1, 1e-5, 10.0
w0 = 1 / np.sqrt(L * C)
Q = w0 * L / R
BW = w0 / Q

def H_R(w):
    x = 1j * w * R * C
    return x / (1 - w ** 2 * L * C + x)

def H_C(w):
    return 1.0 / (1 - w ** 2 * L * C + 1j * w * R * C)

# ---------------------------------------------------------------------
print("=== 实验 1：串联谐振扫频 ===")
w = np.logspace(2, 4.2, 40000)
HR = np.abs(H_R(w))
HC = np.abs(H_C(w))
iw = np.argmax(HR)
print("  w0(解析) = %.2f rad/s；扫频峰位置 = %.2f rad/s" % (w0, w[iw]))
print("  |H_R| 峰值 = %.4f（expect 1）；|H_C| 峰值 = %.4f（expect Q = 10）@ %.1f rad/s"
      % (HR[iw], HC[np.argmax(HC)], w[np.argmax(HC)]))
# 半功率点（数值插值）
half = 1 / np.sqrt(2)
idx = np.where(HR >= half)[0]
w1n, w2n = w[idx[0]], w[idx[-1]]
w1a = w0 * (np.sqrt(1 + 1 / (4 * Q ** 2)) - 1 / (2 * Q))
w2a = w0 * (np.sqrt(1 + 1 / (4 * Q ** 2)) + 1 / (2 * Q))
print("  半功率点：数值 %.2f / %.2f；解析 %.2f / %.2f；BW 数值 %.2f（expect 100）"
      % (w1n, w2n, w1a, w2a, w2n - w1n))
print("  谐振时：U_C = U_L = %.1f V（= Q Vs，10 V 电源上挂 100 V）" % (Q * Vs))

# ---------------------------------------------------------------------
print()
print("=== 实验 2：三 Q 对照（R = 5 / 10 / 20） ===")
for Ri in [5.0, 10.0, 20.0]:
    Qi = w0 * L / Ri
    HRi = np.abs(1j * w * Ri * C / (1 - w ** 2 * L * C + 1j * w * Ri * C))
    iXi = np.where(HRi >= half)[0]
    bwi = w[iXi[-1]] - w[iXi[0]]
    print("  R = %4.0f：Q = %4.1f，数值 BW = %6.1f（解析 w0/Q = %6.1f）"
          % (Ri, Qi, bwi, w0 / Qi))

# ---------------------------------------------------------------------
print()
print("=== 实验 3：并联谐振（R = 1 k、同 L/C、Vs = 10 V） ===")
Rp = 1000.0
Yp = 1 / Rp + 1j * (w * C - 1 / (w * L))
Zp = 1 / np.abs(Yp)
iz = np.argmax(Zp)
Qp = Rp / (w0 * L)
print("  |Z| 峰 = %.1f 欧 @ %.1f rad/s（expect 1000 @ 1000）" % (Zp[iz], w[iz]))
print("  总电流最小 = %.1f mA（expect 10）" % (Vs / Zp[iz] * 1e3))
print("  谐振支路电流 I_L = U/(w0 L) = %.1f mA（= Q_p x I 总 = %.0f x %.0f mA）"
      % (Vs / (w0 * L) * 1e3, Qp, Vs / Zp[iz] * 1e3))
print("  Q_p = R/(w0 L) = %.1f；BW = w0/Q_p = %.1f rad/s（同串联公式）" % (Qp, w0 / Qp))

# ---------------------------------------------------------------------
print()
print("=== 实验 4：网络函数两副面孔（同一电路，不同输出端口） ===")
print("  |H_R(w0)| = %.4f（带通，峰 1）；|H_C(w0)| = %.4f（低通带峰，峰 Q）" % (abs(H_R(w0)), abs(H_C(w0))))
print("  |H_C(0+)| = %.4f（直流全通）；|H_R(10 w0)| = %.4f（约 1/100）" % (abs(H_C(1.0)), abs(H_R(10 * w0))))
print("  H_R 相频：0.1w0 处 %.1f 度；w0 处 %.1f 度；10w0 处 %.1f 度（+90 -> 0 -> -90）"
      % (np.degrees(np.angle(H_R(0.1 * w0))), np.degrees(np.angle(H_R(w0))), np.degrees(np.angle(H_R(10 * w0)))))

# ---------------------------------------------------------------------
print()
print("=== 实验 5：RC 低通（R = 1 k、C = 100 nF） ===")
Rc, Cc = 1000.0, 1e-7
wc = 1 / (Rc * Cc)
Hl = lambda ww: 1 / (1 + 1j * ww * Rc * Cc)
print("  wc = 1/(RC) = %.0f rad/s；|H(wc)| = %.4f（= 1/sqrt(2) = %.4f）"
      % (wc, abs(Hl(wc)), 1 / np.sqrt(2)))
h10, h100 = abs(Hl(10 * wc)), abs(Hl(100 * wc))
print("  |H(10 wc)| = %.4f；|H(100 wc)| = %.4f" % (h10, h100))
print("  十倍频程衰减 = %.2f dB（expect ~-20 dB/dec）" % (20 * np.log10(h100 / h10)))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：串联 RLC 电路 ===")
with schemdraw.Drawing(show=False) as d:
    d += elm.SourceSin().at((0, 0)).up().length(2.0).label("$U_S$", loc="left")
    d += elm.Line().at((0, 2)).to((0.7, 2))
    d += elm.Resistor().at((0.7, 2)).to((1.9, 2)).label("$R$")
    d += elm.Line().at((1.9, 2)).to((2.4, 2))
    d += elm.Inductor().at((2.4, 2)).to((3.4, 2)).label("$L$")
    d += elm.Line().at((3.4, 2)).to((4.0, 2))
    d += elm.Capacitor().at((4.0, 2)).down().length(1.0).label("$C$", loc="right")
    d += elm.Line().at((4.0, 1.0)).to((4.0, 0))
    d += elm.Line().at((4.0, 0)).to((0, 0))
    d += elm.Arrow().at((4.45, 1.75)).to((4.45, 1.25))
    d += elm.Label().at((4.75, 1.5)).label("$u_C$", fontsize=10)

save_stem = "lec19_fig1_series_rlc"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：三 Q 的幅频曲线 ===")
fig, ax = plt.subplots(figsize=(9.2, 4.8))
colors = ["#c0392b", "#2e7d32", "#1f5fa8"]
for Ri, cc, tg in zip([5.0, 10.0, 20.0], colors, ["Q = 20", "Q = 10", "Q = 5"]):
    HRi = np.abs(1j * w * Ri * C / (1 - w ** 2 * L * C + 1j * w * Ri * C))
    ax.semilogx(w, HRi, color=cc, lw=2.0, label="%s（R = %.0f Ω）" % (tg, Ri))
ax.axhline(1 / np.sqrt(2), color="#999999", lw=1.2, ls=":")
ax.text(2200, 1 / np.sqrt(2) + 0.03, "半功率线 $1/\\sqrt{2}$", fontsize=10, color="#666666")
ax.axvline(1000, color="#cccccc", lw=1.0, ls="--")
ax.text(1030, 1.02, "$\\omega_0$ = 1000", fontsize=10, color="#666666")
ax.set_xlabel("角频率 $\\omega$ / (rad/s)")
ax.set_ylabel("$|H_R| = |U_R|/U_S$")
ax.set_title("同一电路不同 R：Q 越大，峰越尖、带越窄（峰高都是 1）", fontsize=11)
ax.legend(fontsize=9, loc="upper right")
ax.set_ylim(0, 1.15)
ax.grid(alpha=0.3, which="both")
plt.tight_layout()
save_stem = "lec19_fig2_q_compare"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：两副面孔（H_C 低通带峰 vs H_R 带通；H_R 相频） ===")
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.2, 6.4), sharex=True)
a1.semilogx(w, HC, color="#c0392b", lw=2.2, label="$|H_C| = |U_C|/U_S$（峰 Q = 10）")
a1.semilogx(w, HR, color="#1f5fa8", lw=2.2, label="$|H_R| = |U_R|/U_S$（峰 1）")
a1.axhline(Q, color="#c0392b", lw=0.8, ls=":")
a1.set_ylabel("幅频")
a1.set_title("同一电路的两种取法：电容口 = 低通带峰，电阻口 = 带通（Q = 10）", fontsize=11)
a1.legend(fontsize=9, loc="upper right")
a1.set_ylim(0, 11)
a1.grid(alpha=0.3, which="both")
a2.semilogx(w, np.degrees(np.angle(H_R(w))), color="#1f5fa8", lw=2.0)
a2.axhline(0, color="#999999", lw=0.8, ls=":")
a2.axvline(w0, color="#cccccc", lw=1.0, ls="--")
a2.set_ylabel("相位 / 度")
a2.set_xlabel("角频率 $\\omega$ / (rad/s)")
a2.set_title("$H_R$ 的相频：低频 +90°、谐振 0°、高频 -90°（过谐振相位翻转）", fontsize=11)
a2.set_ylim(-100, 100)
a2.grid(alpha=0.3, which="both")
plt.tight_layout()
save_stem = "lec19_fig3_two_faces"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec19-01 完成。")