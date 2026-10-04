# =====================================================================
# lec19-02 作业数字预验证（Q2-Q7）
# 规模纪律：总耗时 < 5 秒（纯计算）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import numpy as np

print("=== Q2/Q3：串联谐振（L = 40 mH、C = 25 uF、R = 20 欧） ===")
L, C, R = 0.04, 25e-6, 20.0
w0 = 1 / np.sqrt(L * C)
Q = w0 * L / R
print("  w0 = %.0f rad/s；Q = %.1f；BW = %.1f rad/s" % (w0, Q, w0 / Q))
w1 = w0 * (np.sqrt(1 + 1 / (4 * Q ** 2)) - 1 / (2 * Q))
w2 = w0 * (np.sqrt(1 + 1 / (4 * Q ** 2)) + 1 / (2 * Q))
print("  半功率点：%.1f / %.1f（BW 核对 %.1f）" % (w1, w2, w2 - w1))
print("  Vs = 10 V 时：I0 = %.1f A；U_C = U_L = Q Vs = %.0f V" % (10 / R, Q * 10))

print()
print("=== Q4：并联谐振（R = 500 欧、L = 100 mH、C = 10 uF、Vs = 10 V） ===")
Rp, Lp, Cp = 500.0, 0.1, 10e-6
wp = 1 / np.sqrt(Lp * Cp)
Qp = Rp / (wp * Lp)
print("  w0 = %.0f rad/s；Q_p = R/(w0 L) = %.1f；BW = %.0f rad/s" % (wp, Qp, wp / Qp))
print("  |Z| 峰 = %.0f 欧；总电流最小 = %.0f mA；支路电流 = U/(w0 L) = %.0f mA（= Q x I 总）"
      % (Rp, 10 / Rp * 1e3, 10 / (wp * Lp) * 1e3))

print()
print("=== Q5：网络函数（主例 Q = 10 口径） ===")
R, L, C = 10.0, 0.1, 1e-5
w0 = 1 / np.sqrt(L * C)
Q = w0 * L / R
H_R = np.abs(1j * w0 * R * C / (1 - w0 ** 2 * L * C + 1j * w0 * R * C))
H_C = np.abs(1 / (1 - w0 ** 2 * L * C + 1j * w0 * R * C))
print("  |H_R(w0)| = %.4f（峰 1）；|H_C(w0)| = %.4f（= Q）" % (H_R, H_C))

print()
print("=== Q6：RC 低通（R = 1 k、C = 100 nF） ===")
Rc, Cc = 1000.0, 1e-7
wc = 1 / (Rc * Cc)
Hw = lambda ww: 1 / np.sqrt(1 + (ww * Rc * Cc) ** 2)
print("  wc = %.0f rad/s；|H(wc)| = %.4f（-3 dB）；|H(10 wc)| = %.4f（= 1/sqrt(101)）"
      % (wc, Hw(wc), Hw(10 * wc)))
print("  dB 核对：20log|H(wc)| = %.2f dB；斜率 %.1f dB/dec"
      % (20 * np.log10(Hw(wc)), 20 * np.log10(Hw(100 * wc) / Hw(10 * wc))))

print()
print("=== Q7：接收机前端设计（w0 = 1e6、BW = 1e4、L = 1 mH） ===")
w0r, BWr, Lr = 1e6, 1e4, 1e-3
Qr = w0r / BWr
Cr = 1 / (w0r ** 2 * Lr)
Rr = w0r * Lr / Qr
print("  Q = w0/BW = %.0f；C = 1/(w0^2 L) = %.0f nF；R = w0 L/Q = %.0f 欧"
      % (Qr, Cr * 1e9, Rr))
print("  核对：w0 L = %.0f 欧（谐振时与容抗相消，Z = R = %.0f 欧）" % (w0r * Lr, Rr))

print()
print("[DONE] lec19-02 完成。")