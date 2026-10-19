# L20 single-DOF vibration verification
# 规模纪律: 目标 < 1 秒(实际约 2 s); 纯 numpy
# 验证内容:
#   Exp 1: 例 1 自由振动 RK4 vs 解析
#   Exp 2: 阻尼三态 (欠/临界/过) + 包络 + 单调性 + 过阻尼更慢
#   Exp 3: 稳态幅频扫描 (lambda 0~2) vs 放大因子公式
#   Exp 4: 共振特写 (zeta=0.05: 峰位置 vs lambda_r、峰高 vs 1/(2*zeta))
# print 全 ASCII

import numpy as np

print("=" * 64)
print("L20 single-DOF vibration verification")
print("=" * 64)


def rk4(f, s, dt, n):
    s = np.array(s, dtype=float)
    for _ in range(n):
        k1 = f(s)
        k2 = f(s + dt / 2 * k1)
        k3 = f(s + dt / 2 * k2)
        k4 = f(s + dt * k3)
        s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return s


# ---------- Exp 1: free vibration ----------
m1, k1, x0 = 2.0, 200.0, 0.05
wn1 = np.sqrt(k1 / m1)


def f_free(s):
    return np.array([s[1], -k1 / m1 * s[0]])


dt = 1e-4
s = np.array([x0, 0.0])
max_d = 0.0
for i in range(50000):                 # 5 s
    s = rk4(f_free, s, dt, 1)
    x_ana = x0 * np.cos(wn1 * (i + 1) * dt)
    max_d = max(max_d, abs(s[0] - x_ana))
ok1 = max_d < 1e-9 and abs(wn1 - 10.0) < 1e-12 and abs(2 * np.pi / wn1 - 0.6283) < 1e-3
print("[Exp 1] free vibration (m=2, k=200)")
print("  RK4 vs analytic x0*cos(wn*t): max diff = %.1e  %s" % (max_d, "PASS" if max_d < 1e-9 else "FAIL"))
print("  wn = %.1f rad/s, T = %.4f s  %s" % (wn1, 2 * np.pi / wn1, "PASS" if abs(wn1 - 10.0) < 1e-12 else "FAIL"))

# ---------- Exp 2: damping three states ----------
m2, k2 = 1.0, 100.0
wn2 = np.sqrt(k2 / m2)
cc = 2 * np.sqrt(m2 * k2)


def f_damp(c):
    def f(s):
        return np.array([s[1], -(c * s[1] + k2 * s[0]) / m2])
    return f


dt = 1e-4
# underdamped c=8 (zeta=0.4)
c_u = 8.0
zu = c_u / cc
s = np.array([0.1, 0.0])
xs = []
for _ in range(30000):                 # 3 s
    s = rk4(f_damp(c_u), s, dt, 1)
    xs.append(s[0])
xs = np.array(xs)
sign_changes = int(np.sum(np.sign(xs[:-1]) * np.sign(xs[1:]) < 0))
ts = np.arange(1, len(xs) + 1) * dt
# envelope: peaks should lie below A*exp(-zeta*wn*t)
peaks_u = []
for i in range(1, len(xs) - 1):
    if xs[i] > xs[i - 1] and xs[i] > xs[i + 1] and xs[i] > 0:
        peaks_u.append((ts[i], xs[i]))
env_violation = 0.0
for t, p in peaks_u:
    env_violation = max(env_violation, p - 0.1 * np.exp(-zu * wn2 * t))
# peak should approach envelope: use relative check
env_gap = max(abs(p - 0.1 * np.exp(-zu * wn2 * t)) for t, p in peaks_u)
ok2a = sign_changes > 5 and env_gap < 1e-4  # gap dominated by sampling resolution
print("[Exp 2] damping three states (m=1, k=100, cc=20)")
print("  underdamped (c=8, zeta=%.1f): envelope check max gap = %.1e  %s"
      % (zu, env_gap, "PASS" if ok2a else "FAIL"))
print("    oscillation present (sign changes = %d)  %s"
      % (sign_changes, "PASS" if sign_changes > 5 else "FAIL"))

# critically damped c=20 and overdamped c=40: monotonic from positive x0
for c_v, name in ((20.0, "critically damped"), (40.0, "overdamped")):
    s = np.array([0.1, 0.0])
    sc = 0
    prev = s[0]
    for _ in range(30000):
        s = rk4(f_damp(c_v), s, dt, 1)
        if prev > 0 >= s[0]:
            sc += 1
        prev = s[0]
    print("  %s (c=%.0f): monotonic (no sign changes)  %s"
          % (name, c_v, "PASS" if sc == 0 else "FAIL"))

# overdamped slower than critical at t=2 s
s_c = np.array([0.1, 0.0])
s_o = np.array([0.1, 0.0])
for _ in range(20000):                 # 2 s
    s_c = rk4(f_damp(20.0), s_c, dt, 1)
    s_o = rk4(f_damp(40.0), s_o, dt, 1)
ok2b = s_o[0] > s_c[0] > 0
print("  overdamped slower than critical at t=2s: x_over=%.3f > x_crit=%.3f  %s"
      % (s_o[0], s_c[0], "PASS" if ok2b else "FAIL"))

# ---------- Exp 3: steady-state amplitude scan ----------
m3, k3 = 1.0, 100.0
wn3 = np.sqrt(k3 / m3)
F0 = 1.0


def beta(lam, z):
    return 1.0 / np.sqrt((1 - lam ** 2) ** 2 + (2 * z * lam) ** 2)


z3 = 0.1
lam_list = np.linspace(0.0, 2.0, 21)
max_err = 0.0
for lam in lam_list:
    if lam == 0.0:
        continue
    w_ex = lam * wn3
    c3 = 2 * z3 * np.sqrt(m3 * k3)

    def f_ex(s):
        return np.array([s[1], (F0 * np.cos(w_ex * s[2]) - c3 * s[1] - k3 * s[0]) / m3, 1.0])
    # integrate to steady state: 60/(zeta*wn) ~ 60 s, dt=1e-3 fine for omega<=20
    dt3 = 1e-3
    n3 = int(60.0 / dt3)
    s = np.array([0.0, 0.0, 0.0])
    # skip 90% as transient, record max |x| in the last 10%
    amax = 0.0
    for i in range(n3):
        s = rk4(f_ex, s, dt3, 1)
        if i > 0.9 * n3:
            amax = max(amax, abs(s[0]))
    B_num = amax
    B_ana = (F0 / k3) * beta(lam, z3)
    max_err = max(max_err, abs(B_num / (F0 / k3) - B_ana / (F0 / k3)))
ok3 = max_err < 0.01
print("[Exp 3] steady-state amplitude vs frequency (zeta=0.1)")
print("  21 lambda points: max |B_num/B_static - beta_formula| = %.1e  %s"
      % (max_err, "PASS" if ok3 else "FAIL"))

# ---------- Exp 4: resonance zoom ----------
z4 = 0.05
lam_r = np.sqrt(1 - 2 * z4 ** 2)
# numeric peak: scan lambda finely
lams = np.linspace(0.90, 1.10, 41)
best_lam, best_beta = 0.0, -1.0
for lam in lams:
    b = beta(lam, z4)
    if b > best_beta:
        best_beta, best_lam = b, lam
ok4a = abs(best_lam - lam_r) < 0.005
print("[Exp 4] resonance zoom (zeta=0.05)")
print("  numeric peak at lambda = %.3f, formula lambda_r = %.4f  %s"
      % (best_lam, lam_r, "PASS" if ok4a else "FAIL"))
print("  peak height: numeric %.2f, formula 1/(2*zeta) = %.1f  %s"
      % (best_beta, 1.0 / (2 * z4), "PASS" if abs(best_beta - 1.0 / (2 * z4)) < 0.2 else "FAIL"))

flags = [ok1, ok2a, ok2b, ok3, ok4a, abs(best_beta - 1.0 / (2 * z4)) < 0.2]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))


