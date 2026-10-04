# =====================================================================
# lec17-02 作业数字预验证（Q2-Q8）
# 规模纪律：总耗时 < 5 秒（纯计算）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import numpy as np

mu0 = 4 * np.pi * 1e-7

print("=== Q2：主例复算（N=1000、i=1A、l=40cm、S=4cm2、mur=2500、d=1mm） ===")
Rfe = 0.4 / (2500 * mu0 * 4e-4)
Rgap = 1e-3 / (mu0 * 4e-4)
Phi = 1000 / (Rfe + Rgap)
print("  R铁 = %.4e；R气 = %.4e；R总 = %.4e" % (Rfe, Rgap, Rfe + Rgap))
print("  Phi = %.4e Wb = %.3f mWb；B = %.4f T；L = %.4f H"
      % (Phi, Phi * 1e3, Phi / 4e-4, 1000 ** 2 / (Rfe + Rgap)))

print()
print("=== Q3：去气隙的线性外推 ===")
Phi0 = 1000 / Rfe
print("  Phi' = %.3f mWb；B' = %.2f T（远超 Bs≈1.6——线性模型失效；真实 B 被饱和限制）"
      % (Phi0 * 1e3, Phi0 / 4e-4))

print()
print("=== Q4：气隙对电感的打击 ===")
L0 = 1000 ** 2 / Rfe
print("  有气隙 L = %.4f H；无气隙（线性）L' = %.2f H（气隙按 R 份额直接砍电感）"
      % (1000 ** 2 / (Rfe + Rgap), L0))

print()
print("=== Q5：4.44 与频率危 ===")
NN = 220 / (2 * np.pi / np.sqrt(2) * 50 * 1e-3)
Phim25 = 220 / (2 * np.pi / np.sqrt(2) * 25 * NN)
print("  220V/50Hz/Bm=1T：N = %.1f 匝" % NN)
print("  若频率降到 25 Hz（电压不变、匝数不变）：Phi_m = %.3f mWb -> Bm = %.2f T（饱和危险！）"
      % (Phim25 * 1e3, Phim25 / 1e-3))

print()
print("=== Q7：安匝账复核 ===")
Hfe = Phi / 4e-4 / (2500 * mu0)
Hgap = Phi / 4e-4 / mu0
print("  H铁 l = %.1f A；H气 d = %.1f A；和 = %.1f A（= F）" % (Hfe * 0.4, Hgap * 1e-3, Hfe * 0.4 + Hgap * 1e-3))

print()
print("[DONE] lec17-02 完成。")