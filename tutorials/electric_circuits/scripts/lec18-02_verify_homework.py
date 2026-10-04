# =====================================================================
# lec18-02 作业数字预验证（Q2-Q8）
# 规模纪律：总耗时 < 5 秒（纯计算）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import numpy as np

def ph(z):
    return "%.4g 角 %.4g 度" % (abs(z), np.degrees(np.angle(z)))

print("=== Q2：耦合系数 ===")
L1, L2, M = 8.0, 5.0, 2.0
print("  k = M/sqrt(L1 L2) = 2/sqrt(40) = %.4f" % (M / np.sqrt(L1 * L2)))

print()
print("=== Q3：串联去耦 ===")
print("  顺串 = 8+5+4 = %.0f H；反串 = 13-4 = %.0f H" % (L1 + L2 + 2 * M, L1 + L2 - 2 * M))

print()
print("=== Q5：相量互感电路（Us=100 角 0 度；Z1 = 2+j6；jwM = j10；Z2 = 8+j6） ===")
Z1 = complex(2, 6)
Z2 = complex(8, 6)
ZwM = complex(0, 10)
Us = 100.0
A = np.array([[Z1, ZwM], [ZwM, Z2]], dtype=complex)
b = np.array([Us, 0.0], dtype=complex)
sol = np.linalg.solve(A, b)
I1, I2 = sol[0], sol[1]
print("  I1 = %s；I2 = %s" % (ph(I1), ph(I2)))
r1 = Z1 * I1 + ZwM * I2 - Us
r2 = ZwM * I1 + Z2 * I2
print("  KVL 残差：|r1| = %.2e，|r2| = %.2e（expect ~0）" % (abs(r1), abs(r2)))
Zref = (abs(ZwM) ** 2) / Z2
print("  Z_ref = (wM)^2/Z2 = %s；Z_in = Z1+Z_ref = %s -> I1 = Us/Z_in = %s"
      % (ph(Zref), ph(Z1 + Zref), ph(Us / (Z1 + Zref))))

print()
print("=== Q6：理想变压器（N1 = 500、N2 = 50、U1 = 220、RL = 2） ===")
n = 500 / 50
print("  n = N1/N2 = %.0f；U2 = %.0f V；I2 = %.1f A；I1 = I2/n = %.1f A；Z_in = n^2 RL = %.0f 欧"
      % (n, 220 / n, 220 / n / 2, 220 / n / 2 / n, n ** 2 * 2))

print()
print("=== Q7：阻抗匹配（源 10 V、内阻 800 欧；负载 8 欧） ===")
print("  n = sqrt(800/8) = %.0f（变压器把 8 欧变成 800 欧，源看到匹配负载）" % np.sqrt(800 / 8))
print("  核对：匹配时负载获得 P = U^2/(4 Rs) = %.4f W" % (10 ** 2 / (4 * 800)))

print()
print("=== Q8：T 型去耦支路值（L1=8、L2=5、M=2） ===")
print("  同名端共端：LA=%.0f、LB=%.0f、LC=%.0f" % (L1 - M, L2 - M, M))
print("  异名端共端：LA=%.0f、LB=%.0f、LC=%.0f（负电感只是等效参数）" % (L1 + M, L2 + M, -M))

print()
print("[DONE] lec18-02 完成。")