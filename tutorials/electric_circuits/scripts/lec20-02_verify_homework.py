# =====================================================================
# lec20-02 作业数字预验证（Q2-Q7）
# 规模纪律：总耗时 < 5 秒（纯计算）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import numpy as np

print("=== Q2：含直流与谐波的电压有效值 ===")
u = [20.0, 30.0, 40.0]  # 直流、基波峰值、三次峰值
U = np.sqrt(u[0] ** 2 + u[1] ** 2 / 2 + u[2] ** 2 / 2)
print("  U = sqrt(20^2 + 30^2/2 + 40^2/2) = sqrt(%.0f) = %.2f V" % (u[0] ** 2 + u[1] ** 2 / 2 + u[2] ** 2 / 2, U))

print()
print("=== Q3：方波 A = 5 V 的展开与前两项 RMS ===")
A5 = 5.0
v1, v3, v5 = 4 * A5 / np.pi, 4 * A5 / (3 * np.pi), 4 * A5 / (5 * np.pi)
print("  前三项峰值：%.3f, %.3f, %.3f" % (v1, v3, v5))
rms2 = np.sqrt((v1 ** 2 + v3 ** 2) / 2)
print("  前两项 RMS = %.3f V（解析值 A = %.1f）" % (rms2, A5))

print()
print("=== Q4/Q5：变体 RL（R = 10 欧、L = 20 mH、方波 A = 10、w1 = 1000） ===")
A, w1, R, L = 10.0, 1000.0, 10.0, 20e-3
Ieff = {}
for n in range(1, 40, 2):
    Vn = (4 * A / (n * np.pi)) / np.sqrt(2)
    Zn = R + 1j * n * w1 * L
    In = Vn / Zn
    Ieff[n] = abs(In)
    if n <= 5:
        print("  n = %d：|Z| = %7.3f 欧，相移 %7.3f 度，I 有效值 = %.4f A"
              % (n, abs(Zn), np.degrees(np.angle(Zn)), abs(In)))
Irms = np.sqrt(sum(v ** 2 for v in Ieff.values()))
P = sum(v ** 2 for v in Ieff.values()) * R
print("  I_rms = %.4f A；P = sum(In^2) R = %.4f W" % (Irms, P))
print("  错误对照：U_rms * I_rms = %.4f W（≠ P，二者错相且含谐波）" % (10 * Irms))

print()
print("=== Q7：THD 计算（U1 = 100、U3 = 30、U5 = 20） ===")
thd = np.sqrt(30 ** 2 + 20 ** 2) / 100
print("  THD = sqrt(30^2+20^2)/100 = %.2f%%" % (thd * 100))

print()
print("[DONE] lec20-02 完成。")