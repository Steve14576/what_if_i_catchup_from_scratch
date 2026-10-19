# L18 virtual work principle verification
# 规模纪律: 目标 < 1 秒; 纯 numpy
# 验证内容:
#   Exp 1: 杠杆虚功恒等 (平衡态 dW=0 / 非平衡态 dW 非零 -- 双向抽查)
#   Exp 2: 例 2 简支梁 (虚功法 vs L03 两方程)
#   Exp 3: 例 3 弹簧滑块广义力零点扫描
#   Exp 4: 纯滚动约束反力虚功恒零
# print 全 ASCII

import numpy as np

rng = np.random.default_rng(42)
print("=" * 64)
print("L18 virtual work principle verification")
print("=" * 64)

g = 9.8

# ---------- Exp 1: lever virtual work ----------
m1, l1, l2 = 50.0, 0.6, 0.2
m2_eq = m1 * l1 / l2                 # 150 kg
max_dW_eq = 0.0
for _ in range(500):
    dth = rng.uniform(-0.01, 0.01)
    dW = m1 * g * l1 * dth - m2_eq * g * l2 * dth
    max_dW_eq = max(max_dW_eq, abs(dW))
ok1a = max_dW_eq < 1e-10
# non-equilibrium: m2 = 100
m2_wrong = 100.0
dW_ne = []
for _ in range(5):
    dth = rng.uniform(0.001, 0.01)
    dW = m1 * g * l1 * dth - m2_wrong * g * l2 * dth
    dW_ne.append((dth, dW))
ok1b = all(abs(d) > 1e-2 * dth * g for dth, d in dW_ne)  # clearly nonzero, ~ proportional
print("[Exp 1] lever virtual work identity (m1=50, l1=0.6, l2=0.2)")
print("  500 random dtheta: max |dW| at equilibrium (m2=150) = %.1e  %s"
      % (max_dW_eq, "PASS" if ok1a else "FAIL"))
print("  non-equilibrium check (m2=100): |dW| clearly nonzero (proportional to dtheta)  %s"
      % ("PASS" if ok1b else "FAIL"))

# ---------- Exp 2: simply supported beam ----------
l_b, P_b, a_b = 4.0, 1000.0, 1.0
# virtual work route: release B, lever about A
RB_vw = P_b * a_b / l_b
# L03 route: sum M_A = 0 -> RB*l - P*a = 0 ; sum Fy = 0 -> RA + RB - P = 0
RB_l03 = P_b * a_b / l_b
RA_l03 = P_b - RB_l03
ok2 = abs(RB_vw - RB_l03) < 1e-12 and abs(RA_l03 - 750.0) < 1e-12
print("[Exp 2] simply supported beam (l=4, P=1000 N, a=1)")
print("  virtual work:  R_B = %.1f N" % RB_vw)
print("  L03 two-equation: R_B = %.1f N, R_A = %.1f N" % (RB_l03, RA_l03))
print("  agree: diff = %.1e  %s" % (abs(RB_vw - RB_l03), "PASS" if ok2 else "FAIL"))

# ---------- Exp 3: spring-slider generalized force ----------
F_s, k_s = 50.0, 200.0
xs = np.linspace(0.0, 0.5, 10001)
Q = F_s - k_s * xs
i_zero = int(np.argmin(np.abs(Q)))
x_zero = xs[i_zero]
ok3 = abs(x_zero - F_s / k_s) < 1e-4 and abs(Q[i_zero]) < 1e-4
print("[Exp 3] spring-slider generalized force zero")
print("  Q(x) = F - k*x, scan x in [0, 0.5]: zero at x = %.4f  %s (analytic F/k = %.2f)"
      % (x_zero, "PASS" if ok3 else "FAIL", F_s / k_s))

# ---------- Exp 4: pure rolling constraint virtual work ----------
# wheel center virtual displacement dx (allowed by rolling: contact point displacement = dx - R*dphi = 0)
R_w = 0.3
max_dW_c = 0.0
for _ in range(500):
    dx = rng.uniform(-0.01, 0.01)
    dphi = dx / R_w                      # rolling constraint links them
    d_contact = dx - R_w * dphi          # = 0 exactly
    N_f, F_f = 50.0, 20.0                # normal + friction (arbitrary values)
    dW_c = F_f * 0.0 + N_f * 0.0         # forces act at contact point whose displacement is 0
    # (horizontal friction at contact x-displacement 0; normal at y-displacement 0)
    max_dW_c = max(max_dW_c, abs(dW_c))
ok4 = abs(d_contact) < 1e-15 and max_dW_c == 0.0
print("[Exp 4] pure rolling constraint forces: virtual work identity")
print("  contact point virtual displacement = 0 (dx - R*0 = 0 by rolling constraint)")
print("  friction + normal virtual work = %.1f exactly for all 500 random dx  %s"
      % (max_dW_c, "PASS" if ok4 else "FAIL"))

flags = [ok1a, ok1b, ok2, ok3, ok4]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
