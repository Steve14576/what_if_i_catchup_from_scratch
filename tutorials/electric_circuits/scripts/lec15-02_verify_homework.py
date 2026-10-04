# =====================================================================
# lec15-02 作业数字预验证（Q2-Q8）
# 规模纪律：总耗时 < 5 秒（纯计算）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import numpy as np

print("=== Q2：单口功率账（U=100∠0°、I=5∠-53.13°） ===")
U, I = 100.0, 5.0
psi_i = -np.arctan(4 / 3)
phi = 0.0 - psi_i              # 相位差 phi = psi_u - psi_i
P = U * I * np.cos(phi)
Q = U * I * np.sin(phi)
S = U * I
print("  P = %.0f W；Q = %+.0f var；S = %.0f VA；cosφ = %.1f（滞后）" % (P, Q, S, P / S))
print("  复功率 S = P + jQ = %.0f%+.0fj VA" % (P, Q))

print()
print("=== Q3：RC 单口（U=30V、Z=8-6j） ===")
Z = 8 - 6j
I3 = 30 / abs(Z)
P3 = I3 ** 2 * Z.real
Q3 = I3 ** 2 * Z.imag
S3 = 30 * I3
print("  I = 30/10 = %.0f A；P = I^2 R = %.0f W；Q = I^2 X = %+.0f var；S = %.0f VA；cosφ = %.1f 超前"
      % (I3, P3, Q3, S3, P3 / S3))

print()
print("=== Q4：瞬时功率（u=10√2cos、i=5√2cos(wt-53.13°）） ===")
ang = np.arctan(4 / 3)
print("  P = 10x5xcos53.13° = %.0f W；S = 10x5 = %.0f VA" % (10 * 5 * np.cos(ang), 10 * 5))
print("  p(t) = 30 + 50cos(2wt - 53.13°)；p 极值 = %.0f W / %.0f W（出现负功率=回流）"
      % (30 - 50, 30 + 50))

print()
print("=== Q6：功率因数补偿（P=300、cosφ=0.6 滞后、U=50） ===")
print("  S = P/0.6 = %.0f VA；Q = S sinφ = %.0f var；I = S/U = %.0f A" % (300 / 0.6, 400, 500 / 50))
C1 = 400 / (1000 * 50 ** 2)
print("  (2) 补到 1：C = Q/(wU^2) = %.0f uF；I' = P/U = %.0f A；S' = %.0f VA" % (C1 * 1e6, 6, 300))
C2 = 300 * (4 / 3 - 3 / 4) / (1000 * 50 ** 2)
print("  (3) 补到 0.8：Q_c = P(tanφ1-tanφ2) = %.0f var；C = %.0f uF；I' = %.1f A；S' = %.0f VA"
      % (300 * (4 / 3 - 3 / 4), C2 * 1e6, 7.5, 375))

print()
print("=== Q7：复功率守恒（S1 = 300+400j、S2 = 300-400j） ===")
S1 = 300 + 400j
S2 = 300 - 400j
St = S1 + S2
print("  S总 = %.0f%+.0fj VA；P = %.0f；Q = %.0f；|S总| = %.0f；cosφ = 1" 
      % (St.real, St.imag, St.real, St.imag, abs(St)))
print("  |S1| + |S2| = %.0f ≠ %.0f（视在功率不守恒的活证据）" % (abs(S1) + abs(S2), abs(St)))

print()
print("=== Q8：共轭匹配设计（U_oc = 8、Z_eq = 4+4j） ===")
Uoc, Zeq = 8.0, 4 + 4j
ZL = 4 - 4j
Im = Uoc / (Zeq + ZL)
print("  (1) Z_L = Z_eq* = %.0f%+.0fj" % (ZL.real, ZL.imag))
print("  (2) I = %.0f A；P_max = I^2 R_L = %.0f W（公式 %.0f）"
      % (abs(Im), abs(Im) ** 2 * ZL.real, Uoc ** 2 / (4 * Zeq.real)))
Ib = Uoc / (Zeq + Zeq)
print("  (3) 错配 Z_L = Z_eq：I = %.4f A；P = %.0f W（恰为一半）" % (abs(Ib), abs(Ib) ** 2 * 4))

print()
print("[DONE] lec15-02 完成。")