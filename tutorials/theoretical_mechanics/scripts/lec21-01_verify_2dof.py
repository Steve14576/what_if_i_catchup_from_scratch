# L21 two-DOF vibration verification
# 规模纪律: 目标 < 2 秒; 纯 numpy
# 验证内容:
#   Exp 1: 频率方程 (eig(M^-1 K) vs 手算两解) + 振型
#   Exp 2: 模态叠加 (RK4 vs 两模态解析叠加)
#   Exp 3: 拍振 (软耦合 + 单侧激发: 包络周期 vs 4*pi/dw, 能量往复)
#   Exp 4: 动力吸振器 (主结构稳态幅值趋零, 小振子接管 F0/k2)
# print 全 ASCII

import numpy as np

print("=" * 64)
print("L21 two-DOF vibration verification")
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


# ---------- Exp 1: frequency equation ----------
m, k = 1.0, 100.0
M = np.eye(2) * m
K = k * np.array([[2.0, -1.0], [-1.0, 2.0]])
w2 = np.sort(np.linalg.eigvals(np.linalg.inv(M) @ K).real)
ok1a = abs(w2[0] - k / m) < 1e-9 and abs(w2[1] - 3 * k / m) < 1e-9
print("[Exp 1] frequency equation (m1=m2=m, k1=k2=k3=k)")
print("  eigenvalues of M^-1 K: w^2 = [%.3f, %.3f] * k/m" % (w2[0] / k, w2[1] / k))
print("  hand formula: w^2 = [1.000, 3.000] * k/m  %s" % ("PASS" if ok1a else "FAIL"))
# mode shapes via eigenvectors
vals, vecs = np.linalg.eigh(np.linalg.inv(M) @ K)
u1 = vecs[:, 0] / vecs[0, 0]
u2 = vecs[:, 1] / vecs[0, 1]
ok1b = abs(u1[1] - 1.0) < 1e-9 and abs(u2[1] + 1.0) < 1e-9
print("  mode shapes: u1 = [1, %+.3f], u2 = [1, %+.3f]  %s (ratio exact)"
      % (u1[1], u2[1], "PASS" if ok1b else "FAIL"))

# ---------- Exp 2: modal superposition ----------
w1, w2v = np.sqrt(w2[0]), np.sqrt(w2[1])


def f_chain(s):
    x1, x2, v1, v2 = s
    return np.array([v1, v2, (-(2 * k) * x1 + k * x2) / m, (k * x1 - (2 * k) * x2) / m])


dt = 1e-4
s = np.array([0.08, -0.03, 0.1, 0.2])
# modal decomposition of initial conditions: x = a1*u1 + a2*u2 (u1=[1,1], u2=[1,-1])
a1 = (s[0] + s[1]) / 2.0
a2 = (s[0] - s[1]) / 2.0
b1 = (s[2] + s[3]) / 2.0    # modal velocities
b2 = (s[2] - s[3]) / 2.0
max_d = 0.0
for i in range(50000):      # 5 s
    s = rk4(f_chain, s, dt, 1)
    t = (i + 1) * dt
    x1_ana = a1 * np.cos(w1 * t) + b1 / w1 * np.sin(w1 * t) + a2 * np.cos(w2v * t) + b2 / w2v * np.sin(w2v * t)
    x2_ana = a1 * np.cos(w1 * t) + b1 / w1 * np.sin(w1 * t) - a2 * np.cos(w2v * t) - b2 / w2v * np.sin(w2v * t)
    max_d = max(max_d, abs(s[0] - x1_ana), abs(s[1] - x2_ana))
ok2 = max_d < 1e-8
print("[Exp 2] modal superposition (generic initial conditions)")
print("  RK4 vs two-mode analytic: max diff = %.1e  %s" % (max_d, "PASS" if ok2 else "FAIL"))

# ---------- Exp 3: beating ----------
k_side, k_mid = 100.0, 5.0


def f_soft(s):
    x1, x2, v1, v2 = s
    return np.array([v1, v2,
                     (-(k_side + k_mid) * x1 + k_mid * x2) / m,
                     (k_mid * x1 - (k_side + k_mid) * x2) / m])


w1s = np.sqrt(k_side / m)                # 10
w2s = np.sqrt((k_side + 2 * k_mid) / m)  # sqrt(110) ~ 10.488
dw = w2s - w1s
T_beat = 4 * np.pi / dw
# track x1 envelope maxima over 100 s; count beat period from successive envelope zeros
dt = 1e-3
s = np.array([0.1, 0.0, 0.0, 0.0])
env_zeros = []
prev = s[0]
n3 = int(100.0 / dt)
for i in range(n3):
    s = rk4(f_soft, s, dt, 1)
    # envelope zero ~ |x1| stays tiny over a window: detect local minimum of |x1| near zero
    if i % 100 == 0:
        pass
    prev = s[0]
# simpler: sample |x1| max in each 1 s window; beat period from distance between minima
amps = []
for j in range(100):
    amax = 0.0
    for i in range(1000):
        s = rk4(f_soft, s, dt, 1)
        amax = max(amax, abs(s[0]))
    amps.append(amax)
amps = np.array(amps)
# find first two minima of the windowed amplitude (envelope zeros)
mins = []
for j in range(1, 99):
    if amps[j] < amps[j - 1] and amps[j] < amps[j + 1] and amps[j] < 0.02:
        if not mins or j - mins[-1] > 5:
            mins.append(j)
# energy sloshing: at quarter beat, x1 ~ 0 and |x2| ~ X
s2 = np.array([0.1, 0.0, 0.0, 0.0])
t_zero = np.pi / dw                       # envelope cos(dw t/2) zero
i_zero = int(round(t_zero / dt))
x2_win = 0.0
half_carrier = int(round((np.pi / ((w1s + w2s) / 2)) / dt))   # half carrier period in steps
for i in range(i_zero + half_carrier):
    s2 = rk4(f_soft, s2, dt, 1)
    if abs(i - i_zero) <= half_carrier:
        x2_win = max(x2_win, abs(s2[1]))
T_zero = 2 * np.pi / dw                  # envelope-zero spacing (half of full beat)
ok3 = len(mins) >= 2 and abs((mins[1] - mins[0]) - T_zero) < 1.5 and x2_win > 0.09
print("[Exp 3] beating (soft coupling k2 = 0.05k, x1(0)=X, x2(0)=0)")
print("  dw = %.4f rad/s; full beat period 4*pi/dw = %.1f s, envelope-zero spacing 2*pi/dw = %.1f s"
      % (dw, T_beat, T_zero))
print("  numeric envelope-zero spacing of x1 = %.1f s  %s"
      % ((mins[1] - mins[0]) if len(mins) >= 2 else -1,
         "PASS" if len(mins) >= 2 and abs((mins[1] - mins[0]) - T_zero) < 1.5 else "FAIL"))
print("  energy sloshing: near t=%.1fs (x1 envelope zero) window max |x2| = %.3f X  %s"
      % (t_zero, x2_win / 0.1, "PASS" if x2_win > 0.09 else "FAIL"))

# ---------- Exp 4: tuned absorber ----------
m1, k1 = 1.0, 100.0
Om = np.sqrt(k1 / m1)                    # 10
F0 = 1.0
m2, k2 = 0.1, 10.0                       # k2/m2 = 100 = Om^2 (tuned)


def f_abs(s):
    x1, x2, v1, v2, t = s
    return np.array([v1, v2,
                     (F0 * np.cos(Om * t) - (k1 + k2) * x1 + k2 * x2) / m1,
                     (k2 * x1 - k2 * x2) / m2,
                     1.0])


dt = 1e-3
s = np.zeros(5)
# integrate to steady state: 40 s (transient decays only by numerical damping? no damping!)
# NOTE: undamped system -> transient never decays. Use modal decomposition instead:
# steady-state particular solution: assume x1 = A1 cos(Om t), x2 = A2 cos(Om t)
# m1*(-Om^2*A1) = F0 - (k1+k2)A1 + k2*A2 ; m2*(-Om^2*A2) = k2*A1 - k2*A2
A = np.array([[k1 + k2 - m1 * Om ** 2, -k2], [-k2, k2 - m2 * Om ** 2]])
rhs = np.array([F0, 0.0])
Amp = np.linalg.solve(A, rhs)
ok4 = abs(Amp[0]) < 1e-9 and abs(abs(Amp[1]) - F0 / k2) < 1e-9
print("[Exp 4] tuned absorber (m1=1, k1=100, F at w=10, absorber m2=0.1, k2=10)")
print("  steady |x1| = %.1e (analytic zero)  %s" % (abs(Amp[0]), "PASS" if abs(Amp[0]) < 1e-9 else "FAIL"))
print("  steady |x2| = %.3f, sign = %+.0f (anti-phase, analytic -F0/k2)  %s"
      % (abs(Amp[1]), np.sign(Amp[1]), "PASS" if abs(abs(Amp[1]) - F0 / k2) < 1e-9 else "FAIL"))

flags = [ok1a, ok1b, ok2, ok3, ok4]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
