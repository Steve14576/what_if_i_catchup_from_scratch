# =====================================================================
# lec14-02 作业数字预验证（Q2-Q8）
# 规模纪律：总耗时 < 5 秒（纯计算）。
#
# 主例数据：U = 50∠0°、Z1 = 3+4j、Z2 = 3-4j（w = 1000）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import numpy as np

w = 1000.0

print("=== Q2：三元件阻抗与导纳（w = 1000） ===")
ZR = 10.0
ZL = 1j * w * 10e-3          # 10 mH
ZC = -1j / (w * 100e-6)      # 100 uF
for name, Z in [("R = 10 ohm", ZR), ("L = 10 mH", ZL), ("C = 100 uF", ZC)]:
    zr = 0.0 if abs(Z.real) < 1e-9 else Z.real
    zi = 0.0 if abs(Z.imag) < 1e-9 else Z.imag
    print("  %-11s Z = %.0f%+.0fj = %.0f∠%.0f°；Y = %.4f∠%.0f°"
          % (name, zr, zi, abs(Z), np.degrees(np.angle(Z)),
             abs(1 / Z), np.degrees(np.angle(1 / Z))))

print()
print("=== Q3：串并联合成 ===")
Z1 = 3 + 4j
Z2 = 3 - 4j
print("  Z串 = %s = %.0f∠%.0f°；Z并 = %s = %.4f∠%.0f°"
      % (("%.0f%+.0fj" % (Z1.real + Z2.real, Z1.imag + Z2.imag)), abs(Z1 + Z2),
         np.degrees(np.angle(Z1 + Z2)),
         ("%.4f%+.4fj" % ((Z1 * Z2 / (Z1 + Z2)).real, (Z1 * Z2 / (Z1 + Z2)).imag)),
         abs(Z1 * Z2 / (Z1 + Z2)), np.degrees(np.angle(Z1 * Z2 / (Z1 + Z2)))))

print()
print("=== Q4：分流公式复现 ===")
It = 12.0
I1 = It * Z2 / (Z1 + Z2)
print("  I1 = 12∠0° x (5∠-53.13° / 6) = %.0f∠%.4f° A" % (abs(I1), np.degrees(np.angle(I1))))

print()
print("=== Q5：几何合成 ===")
geo = 2 * 10 * np.cos(np.arctan(4 / 3))
cos_theo = np.sqrt(100 + 100 + 2 * 100 * np.cos(2 * np.arctan(4 / 3)))
print("  水平分量法：2 x 10 x cos53.13° = %.4f A" % geo)
print("  余弦定理：sqrt(100+100+200cos106.26°) = %.4f A" % cos_theo)

print()
print("=== Q7：结点法（三支路并联，L 与 C 电流相消） ===")
Is = 10.0                    # 电流源有效值 10A，取 10∠0°
YR = 1 / 5.0
YL = 1 / (1j * 10.0)
YC = 1 / (-1j * 10.0)
YA = YR + YL + YC
UA = Is / YA
IR = UA / 5.0
IL = UA / (1j * 10.0)
IC = UA / (-1j * 10.0)
print("  Y总 = %.2f（虚部 ±0.1j 相消）-> U_A = %.0f∠%.0f° V" % (YA.real, abs(UA), np.degrees(np.angle(UA))))
print("  I_R = %.0f∠%.0f°；I_L = %.0f∠%.0f°；I_C = %.0f∠%.0f°"
      % (abs(IR), np.degrees(np.angle(IR)), abs(IL), np.degrees(np.angle(IL)),
         abs(IC), np.degrees(np.angle(IC))))
print("  KCL 核账：|I_R + I_L + I_C - I_S| = %.2e A" % abs(IR + IL + IC - Is))

print()
print("=== Q8：导纳法 + 无功对消 ===")
Y1, Y2 = 1 / Z1, 1 / Z2
print("  Y1 + Y2 = %.4f%+.4fj；虚部相消 -> Y总 = %.2f -> Z总 = 1/%.2f = %.4f"
      % ((Y1 + Y2).real, (Y1 + Y2).imag, (Y1 + Y2).real, (Y1 + Y2).real, 1 / (Y1 + Y2).real))

print()
print("[DONE] lec14-02 完成。")