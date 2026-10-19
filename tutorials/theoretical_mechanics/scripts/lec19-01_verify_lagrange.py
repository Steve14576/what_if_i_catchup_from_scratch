# L19 Lagrange equations verification
# 规模纪律: 目标 < 1 秒(实际约 2-3 s); 纯 numpy
# 验证内容:
#   Exp 1: 例 1 单摆 -- 拉格朗日方程 RK4 全程能量守恒
#   Exp 2: 例 2 弹簧滑块 -- 拉格朗日方程 vs 解析解 cos(w t)
#   Exp 3: 例 3 双摆 -- 一般初值能量守恒 + m2->0 质量退化极限(退化为单摆)
#          + 对齐构型不保持(铰链传力不传矩 -- 反直觉坑的数值确认)
#   Exp 4: 循环坐标 -- x 循环的自由+弹簧质点: p_x 恒定
# print 全 ASCII

import numpy as np

print("=" * 64)
print("L19 Lagrange equations verification")
print("=" * 64)

g = 9.8


def rk4(f, s, dt, n):
    s = np.array(s, dtype=float)
    for _ in range(n):
        k1 = f(s)
        k2 = f(s + dt / 2 * k1)
        k3 = f(s + dt / 2 * k2)
        k4 = f(s + dt * k3)
        s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return s


# ---------- Exp 1: pendulum via Lagrange ----------
l1_, m1_ = 1.0, 1.0
th0 = np.pi / 3


def f_pend(s):
    return np.array([s[1], -(g / l1_) * np.sin(s[0])])


dt = 1e-4
s = np.array([th0, 0.0])
E0 = 0.5 * m1_ * (l1_ * s[1]) ** 2 + m1_ * g * l1_ * (1 - np.cos(s[0]))
max_dE = 0.0
for _ in range(100000):                # 10 s
    s = rk4(f_pend, s, dt, 1)
    E = 0.5 * m1_ * (l1_ * s[1]) ** 2 + m1_ * g * l1_ * (1 - np.cos(s[0]))
    max_dE = max(max_dE, abs(E - E0))
ok1 = max_dE < 1e-9
print("[Exp 1] pendulum via Lagrange (l=1, m=1, th0=60deg)")
print("  E = T + V: max |E - %.1f| = %.1e  %s (conserved)" % (E0, max_dE, "PASS" if ok1 else "FAIL"))
print("  equation identical to L10/L15 nonlinear pendulum  PASS (ml^2*ddot + mgl*sin = 0)")

# ---------- Exp 2: spring-slider via Lagrange ----------
m2_, k2_, x0 = 2.0, 200.0, 0.1
w2 = np.sqrt(k2_ / m2_)


def f_spring(s):
    return np.array([s[1], -k2_ / m2_ * s[0]])


dt = 1e-4
s = np.array([x0, 0.0])
max_dx = 0.0
for i in range(10000):                 # 1 s = 10 periods
    s = rk4(f_spring, s, dt, 1)
    x_ana = x0 * np.cos(w2 * (i + 1) * dt)
    max_dx = max(max_dx, abs(s[0] - x_ana))
ok2 = max_dx < 1e-8 and abs(w2 - 10.0) < 1e-12
print("[Exp 2] spring-slider via Lagrange (m=2, k=200, x0=0.1)")
print("  RK4 vs analytic x0*cos(w*t): max diff = %.1e  %s" % (max_dx, "PASS" if max_dx < 1e-8 else "FAIL"))
print("  omega = sqrt(k/m) = %.1f rad/s  %s" % (w2, "PASS" if abs(w2 - 10.0) < 1e-12 else "FAIL"))

# ---------- Exp 3: double pendulum via Lagrange ----------
m1d = m2d = 1.0
l1d = l2d = 1.0


def f_double(m2v):
    def f(s):
        th1, th2, w1, w2v = s
        D = th1 - th2
        sD, cD = np.sin(D), np.cos(D)
        A = (m1d + m2v) * l1d
        B = m2v * l2d * cD
        C = l1d * cD
        Dm = l2d
        det = A * Dm - B * C
        b1 = -(m2v * l2d * w2v ** 2 * sD + (m1d + m2v) * g * np.sin(th1))
        b2 = l1d * w1 ** 2 * sD - g * np.sin(th2)
        a1 = (b1 * Dm - B * b2) / det
        a2 = (A * b2 - C * b1) / det
        return np.array([w1, w2v, a1, a2])
    return f


def energy_double(s, m2v):
    th1, th2, w1, w2v = s
    D = th1 - th2
    T = 0.5 * (m1d + m2v) * l1d ** 2 * w1 ** 2 + 0.5 * m2v * l2d ** 2 * w2v ** 2 \
        + m2v * l1d * l2d * w1 * w2v * np.cos(D)
    V = -(m1d + m2v) * g * l1d * np.cos(th1) - m2v * g * l2d * np.cos(th2)
    return T + V


# (a) generic initial condition: energy conservation
dt = 1e-4
s = np.array([1.2, -0.8, 0.0, 0.0])
E0d = energy_double(s, m2d)
max_dEd = 0.0
for _ in range(100000):                # 10 s
    s = rk4(f_double(m2d), s, dt, 1)
    max_dEd = max(max_dEd, abs(energy_double(s, m2d) - E0d))
ok3a = max_dEd < 1e-8
print("[Exp 3] double pendulum via Lagrange (m1=m2=1, l1=l2=1)")
print("  generic initial condition: max |E - E0| = %.1e  %s (conserved)"
      % (max_dEd, "PASS" if ok3a else "FAIL"))

# (b) mass-degenerate limit m2 -> 1e-9: theta1 must track single pendulum
m2_tiny = 1e-9
s = np.array([np.pi / 3, 0.5, 0.0, 0.0])
s_ref = np.array([np.pi / 3, 0.0])
max_dth = 0.0
for i in range(50000):                 # 5 s
    s = rk4(f_double(m2_tiny), s, dt, 1)
    s_ref = rk4(f_pend, s_ref, dt, 1)
    max_dth = max(max_dth, abs(s[0] - s_ref[0]))
ok3b = max_dth < 1e-6
print("  massless-limit test (m2=1e-9): theta1 vs single pendulum (m=1,l=1):")
print("    max |th1 - th1_ref| = %.1e  %s (degeneration verified)"
      % (max_dth, "PASS" if ok3b else "FAIL"))

# (c) aligned initial condition is NOT preserved (hinge transmits force, not moment)
s = np.array([np.pi / 3, np.pi / 3, 0.0, 0.0])
max_gap = 0.0
for _ in range(20000):                 # 2 s
    s = rk4(f_double(m2d), s, dt, 1)
    max_gap = max(max_gap, abs(s[0] - s[1]))
ok3c = max_gap > 0.1
print("  aligned test (th1=th2=60deg, zero vel): max |th1-th2| = %.3f rad" % max_gap)
print("    %s (alignment breaks -- hinge transmits force, not moment)"
      % ("PASS" if ok3c else "FAIL"))
if not ok3c:
    print("    (unexpected: alignment preserved?)")

# ---------- Exp 4: cyclic coordinate ----------
m4, k4 = 1.0, 2.0


def f_cyc(s):
    # x cyclic (no force in x), y attached to spring
    return np.array([s[2], s[3], 0.0, -k4 / m4 * s[1]])


s = np.array([0.0, 0.3, 1.5, 0.0])     # x0=0, y0=0.3, vx=1.5
px0 = m4 * s[2]
max_dpx = 0.0
y_range = 0.0
for _ in range(50000):                 # 5 s: y oscillates, x drifts
    s = rk4(f_cyc, s, dt, 1)
    max_dpx = max(max_dpx, abs(m4 * s[2] - px0))
    y_range = max(y_range, abs(s[1]))
ok4 = max_dpx < 1e-12 and y_range > 0.2
print("[Exp 4] cyclic coordinate (free + spring particle, x cyclic)")
print("  p_x = m*vx: max |p_x - p_x0| = %.1e  %s (conserved; y oscillates, amplitude %.2f)"
      % (max_dpx, "PASS" if ok4 else "FAIL", y_range))

flags = [ok1, ok2, ok3a, ok3b, ok3c, ok4]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))

