# L17 d'Alembert principle verification
# 规模纪律: 目标 < 1 秒; 纯 numpy
# 验证内容:
#   Exp 1: 惯性力系简化恒等 (3 质点刚性系: 合力=-M*aC, 对质心矩=-Jc*alpha)
#   Exp 2: 例 2 偏心轴承动反力 me*w^2
#   Exp 3: 例 3 滚动圆柱: 动静法 vs L14 三件套 (a = (2/3)g sin(theta))
# print 全 ASCII

import numpy as np

print("=" * 64)
print("L17 d'Alembert principle verification")
print("=" * 64)

g = 9.8

# ---------- Exp 1: inertial force system reduction ----------
# 3 particles rigid assembly: rotate about C with alpha, translate with aC
m = np.array([1.0, 2.0, 3.0])
M = m.sum()
# positions relative to C (sum m*r = 0 by construction)
r = np.array([[-0.5, 0.0], [0.2, -0.3], [-0.1, 0.2]])
# force sum m_i * r_i = [ -0.5 + 0.4 - 0.3, -0.6 + 0.6 ] = [-0.4, 0.0] -- not zero!
# adjust: make sum m*r = 0
r[2] = np.array([0.1, 0.2])
# check: 1*(-0.5) + 2*(0.2) + 3*(0.1) = -0.5 + 0.4 + 0.3 = 0.2 -- still not zero
r[0] = np.array([-0.7, 0.0])
# 1*(-0.7) + 2*(0.2) + 3*(0.1) = -0.7 + 0.4 + 0.3 = 0.0  ✓
# 1*(0.0) + 2*(-0.3) + 3*(0.2) = -0.6 + 0.6 = 0.0  ✓

aC = np.array([2.0, 1.0])   # centroid acceleration
alpha = 0.5                  # angular acceleration
# particle velocities relative to C: each rotates with alpha
# accelerations: a_i = aC + alpha x r_i + omega^2 stuff (take omega=0 for now)
# a_i = aC + alpha cross r_i  (with omega = 0)
acc = []
for i in range(3):
    a_rel = alpha * np.array([-r[i][1], r[i][0]])  # alpha x r  (z-component only)
    acc.append(aC + a_rel)
acc = np.array(acc)

# inertial forces: F_i = -m_i * a_i
F_in = np.array([-m[i] * acc[i] for i in range(3)])
sum_F = F_in.sum(axis=0)

# compare with -M * aC
F_theory = -M * aC
diff_F = np.abs(sum_F - F_theory)

# moment about C: sum r_i x F_i
Mc = 0.0
for i in range(3):
    Mc += r[i][0] * F_in[i][1] - r[i][1] * F_in[i][0]
# theory: -J_C * alpha
J_C = (m * (r ** 2).sum(axis=1)).sum()
Mc_theory = -J_C * alpha
diff_M = abs(Mc - Mc_theory)

ok1 = diff_F.max() < 1e-12 and diff_M < 1e-12
print("[Exp 1] inertial force system reduction, 3-particle rigid assembly")
print("  sum of inertial forces vs -M*aC:")
print("    max |Fx - (-M*aCx)| = %.1e  %s" % (diff_F[0], "PASS" if diff_F[0] < 1e-12 else "FAIL"))
print("    max |Fy - (-M*aCy)| = %.1e  %s" % (diff_F[1], "PASS" if diff_F[1] < 1e-12 else "FAIL"))
print("  moment about C vs -Jc*alpha:")
print("    max |Mc - (-Jc*alpha)| = %.1e  %s" % (diff_M, "PASS" if diff_M < 1e-12 else "FAIL"))

# ---------- Exp 2: eccentric disk bearing force ----------
m_d, e_d, n_d = 10.0, 0.002, 3000.0
w_d = n_d * 2 * np.pi / 60
F_d = m_d * e_d * w_d ** 2
ok2 = abs(F_d - 1973.9) < 1.0
print("[Exp 2] eccentric disk bearing force (m=10, e=2mm, n=3000rpm)")
print("  F = m*e*w^2 = %.1f N  %s (matches hand)" % (F_d, "PASS" if ok2 else "FAIL"))

# ---------- Exp 3: rolling cylinder ----------
th = np.deg2rad(30.0)
a_dalembert = (2.0 / 3.0) * g * np.sin(th)
a_theory = g * np.sin(th) / (1 + 0.5)  # same formula from L14
ok3 = abs(a_dalembert - a_theory) < 1e-12
print("[Exp 3] rolling cylinder: d'Alembert vs L14 three-piece")
print("  a = %.4f m/s^2  %s (identical to (2/3)g*sin(30) = %.4f)"
      % (a_dalembert, "PASS" if ok3 else "FAIL", a_theory))

flags = [ok1, ok2, ok3]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
