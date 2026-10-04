# =====================================================================
# lec16-02 作业数字预验证（Q2-Q7）
# 规模纪律：总耗时 < 5 秒（纯计算）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import numpy as np

print("=== Q2：Y 接换算 ===")
print("  相电压 220 -> 线电压 220√3 = %.2f（标称 380）" % (220 * np.sqrt(3)))
print("  线电压 380 -> 相电压 380/√3 = %.2f" % (380 / np.sqrt(3)))

print()
print("=== Q3：Δ 接（Ul = 220、Z = 22∠53.13°） ===")
Ip = 220 / 22
ang = np.arctan(4 / 3)
IAB = 220 / (22 * np.exp(1j * ang))
ICA = (220 * np.exp(1j * 2 * np.pi / 3)) / (22 * np.exp(1j * ang))
IA = IAB - ICA
print("  相电流 Ip = %.0f A（滞后 %.4f°）；线电流 Il = √3 x %.0f = %.2f∠%.4f°（再滞后 30°）"
      % (Ip, np.degrees(ang), Ip, abs(IA), np.degrees(np.angle(IA))))

print()
print("=== Q4：主例复算（对称 Y-Y：100V、3+4j/相） ===")
Up, Z = 100.0, 3 + 4j
IA = Up / Z
print("  I_A = %.0f∠%.4f° A（B/C 各 -/+120°）；I_N = 0" % (abs(IA), np.degrees(np.angle(IA))))
print("  P = 3x100x20x0.6 = %.0f W；Q = %.0f var；S = %.0f VA" % (3600, 4800, 6000))

print()
print("=== Q5：√3 快速公式（Ul = 173.2、Il = 20、cosφ = 0.6） ===")
P = np.sqrt(3) * 173.2 * 20 * 0.6
Q = np.sqrt(3) * 173.2 * 20 * 0.8
S = np.sqrt(3) * 173.2 * 20
print("  P = %.0f W；Q = %.0f var；S = %.0f VA（与 3 倍法一致）" % (P, Q, S))

print()
print("=== Q7：一相断开（B/C 各 10 ohm，A 开） ===")
UB = 100 * np.exp(-1j * 2 * np.pi / 3)
UC = 100 * np.exp(+1j * 2 * np.pi / 3)
Un = (UB / 10 + UC / 10) / (1 / 10 + 1 / 10)
UB2, UC2 = UB - Un, UC - Un
print("  U_n = %.0f V；U_B' = %.2f∠%.1f° V；U_C' = %.2f∠%.1f° V" 
      % (Un.real, abs(UB2), np.degrees(np.angle(UB2)), abs(UC2), np.degrees(np.angle(UC2))))
print("  电流 = %.2f A；校验两电压之和 = 线电压：%.2f ≈ %.1f"
      % (abs(UB2) / 10, abs(UB2) + abs(UC2), 100 * np.sqrt(3)))

print()
print("[DONE] lec16-02 完成。")