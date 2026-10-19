# L15 energy theorem verification
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 功的积分 (500 组随机 F(x): 梯形 vs 解析) + 重力功路径无关 (200 条随机折线路径)
#   Exp 2: 例 1 弹簧释放: RK4 全程能量监控 + v(自然长) = 2.1213
#   Exp 3: 例 3 单摆 (大摆角, 非线性): E 恒 + v(最低) = 3.1305 + T = 2mg
#   Exp 4: 例 2 斜面滚动轮: E = 0.75 m v^2 + mgh 恒 + v_end = 5.112 (L14 闭环)
#   Exp 5: 恒功率提升: RK4 (P/(mv) - g) vs 功率方程 (0.5 m v^2 + mgh = P t)
# print 全 ASCII (GBK 控制台安全)

import numpy as np

rng = np.random.default_rng(42)
print("=" * 64)
print("L15 energy theorem verification")
print("=" * 64)

g = 9.8


def rk4_scalar(f, s, dt, n):
    s = np.array(s, dtype=float)
    for _ in range(n):
        k1 = f(s)
        k2 = f(s + dt / 2 * k1)
        k3 = f(s + dt / 2 * k2)
        k4 = f(s + dt * k3)
        s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return s


# ---------- Exp 1: work integrals + gravity path independence ----------
N = 500
max_d1 = 0.0
cnt = 0
while cnt < N:
    Fc = rng.uniform(-5.0, 5.0, 4)          # F(x) poly deg 3
    x1, x2 = rng.uniform(-1.0, 1.0, 2)
    xs = np.linspace(min(x1, x2), max(x1, x2), 100001)
    W_trap = np.trapezoid(np.polyval(Fc, xs), xs) * np.sign(x2 - x1)
    W_ana = np.polyval(np.polyint(Fc), x2) - np.polyval(np.polyint(Fc), x1)
    max_d1 = max(max_d1, abs(W_trap - W_ana))
    cnt += 1
ok1a = max_d1 < 1e-8
print("[Exp 1] work integrals, %d random F(x)" % N)
print("  max | trapezoid - analytic | = %.1e  %s" % (max_d1, "PASS" if ok1a else "FAIL"))
# gravity path independence: random zigzag paths from (0, 0) to (5, 3)
max_dg = 0.0
for _ in range(200):
    n_seg = int(rng.integers(3, 12))
    xs_p = np.sort(rng.uniform(0.0, 5.0, n_seg - 1))
    xs_p = np.concatenate(([0.0], xs_p, [5.0]))
    ys_p = rng.uniform(-2.0, 5.0, n_seg + 1)
    ys_p[0] = 0.0
    ys_p[-1] = 3.0
    W_path = 0.0
    for i in range(n_seg + 0 if False else len(xs_p) - 1):
        dx = xs_p[i + 1] - xs_p[i]
        dy = ys_p[i + 1] - ys_p[i]
        seg_len = np.hypot(dx, dy)
        if seg_len == 0:
            continue
        # gravity is constant (-mg in y): W = F . dr = -m g dy
        W_path += -1.0 * g * dy              # m = 1 kg
    # expected: W = mg(h1 - h2) = mg*(0 - 3) = -29.4
    max_dg = max(max_dg, abs(W_path - (g * (0.0 - 3.0))))
ok1b = max_dg < 1e-12
print("  gravity path-independence: 200 random zigzag paths,")
print("    max | W_path - mgh | = %.1e  %s (path does not matter)"
      % (max_dg, "PASS" if ok1b else "FAIL"))

# ---------- Exp 2: spring release ----------
k_sp, m_sp, x0_sp = 200.0, 4.0, 0.3
# analytic: v at x=0 is sqrt(2*W/m) with W = 0.5*k*x0^2 = 9 J
v_ana2 = np.sqrt(2 * (0.5 * k_sp * x0_sp ** 2) / m_sp)


def f_spring(s):                             # s = [x, v]
    return np.array([s[1], -k_sp * s[0] / m_sp])


# integrate until x crosses zero (release from x0 moving inward)
dt2 = 1e-5
s = np.array([x0_sp, 0.0])
max_E2 = 0.0
v_at0 = None
for _ in range(int(0.5 / dt2)):
    s_prev = s.copy()
    s = rk4_scalar(f_spring, s, dt2, 1)
    E = 0.5 * m_sp * s[1] ** 2 + 0.5 * k_sp * s[0] ** 2
    max_E2 = max(max_E2, abs(E - 9.0))
    if s_prev[0] > 0 >= s[0]:
        frac = s_prev[0] / (s_prev[0] - s[0])
        v_at0 = s_prev[1] + frac * (s[1] - s_prev[1])
        break
ok2 = max_E2 < 1e-8 and abs(abs(v_at0) - v_ana2) < 1e-6
print("[Exp 2] spring release (k=200, m=4, x0=0.3)")
print("  E = KE + PE: max |E(t) - 9.0| = %.1e  %s (conserved)" % (max_E2, "PASS" if max_E2 < 1e-8 else "FAIL"))
print("  |v| at natural length = %.4f m/s (analytic %.4f)  %s"
      % (abs(v_at0), v_ana2, "PASS" if abs(abs(v_at0) - v_ana2) < 1e-6 else "FAIL"))

# ---------- Exp 3: pendulum, large angle ----------
l_p, m_p, th0_p = 1.0, 1.0, np.pi / 3        # 60 deg
E0_p = m_p * g * l_p * (1 - np.cos(th0_p))   # 4.9 J


def f_pend(s):                               # s = [theta, dtheta]
    return np.array([s[1], -(g / l_p) * np.sin(s[0])])


dt3 = 1e-4
s = np.array([th0_p, 0.0])
max_E3 = 0.0
max_v3 = 0.0
for _ in range(60000):                       # 6 s = many swings
    s = rk4_scalar(f_pend, s, dt3, 1)
    E = 0.5 * m_p * (l_p * s[1]) ** 2 + m_p * g * l_p * (1 - np.cos(s[0]))
    max_E3 = max(max_E3, abs(E - E0_p))
    max_v3 = max(max_v3, abs(l_p * s[1]))
v_ana3 = np.sqrt(2 * g * l_p * (1 - np.cos(th0_p)))
T_bot = m_p * g + m_p * v_ana3 ** 2 / l_p
ok3 = max_E3 < 1e-8 and abs(max_v3 - v_ana3) < 1e-4 and abs(T_bot - 2 * m_p * g) < 1e-9
print("[Exp 3] pendulum (l=1, m=1, theta0=60deg, full nonlinear)")
print("  E: max |E - 4.9| = %.1e  %s (conserved)" % (max_E3, "PASS" if max_E3 < 1e-8 else "FAIL"))
print("  v at bottom = %.4f m/s (analytic %.4f)  %s"
      % (max_v3, v_ana3, "PASS" if abs(max_v3 - v_ana3) < 1e-4 else "FAIL"))
print("  T at bottom = %.2f N = 2mg  %s" % (T_bot, "PASS" if abs(T_bot - 2 * m_p * g) < 1e-9 else "FAIL"))

# ---------- Exp 4: disk rolling down incline ----------
m_r = 10.0
th4 = np.deg2rad(30.0)
s_slope = 4.0                                # 4 m along slope -> h = 2 m
a_r = g * np.sin(th4) / 1.5                  # solid disk
v_end = np.sqrt(2 * a_r * s_slope)
# energy check: E = 0.75 m v^2 + mgh = const = mgh0 = 196
h0 = m_r * g * s_slope * np.sin(th4)
E_check = 0.75 * m_r * v_end ** 2            # KE at end (h=0)
ok4 = abs(E_check - h0) < 1e-9 and abs(v_end - np.sqrt(4 * g * 2 / 3)) < 1e-9
print("[Exp 4] disk rolling down 30-deg incline, h=2 m")
print("  E = 0.75 m v^2 + mgh: |E_end - 196| = %.1e  %s" % (abs(E_check - h0), "PASS" if abs(E_check - h0) < 1e-9 else "FAIL"))
print("  v_end = %.3f m/s (analytic %.3f)  %s (L14 closure)"
      % (v_end, np.sqrt(4 * g * 2 / 3), "PASS" if abs(v_end - np.sqrt(4 * g * 2 / 3)) < 1e-9 else "FAIL"))

# ---------- Exp 5: constant-power lift ----------
P5, m5, t5 = 10000.0, 1000.0, 2.0


def f_lift(s):                               # s = [h, v]
    return np.array([s[1], P5 / (m5 * s[1]) - g if s[1] > 1e-6 else 0.0 - g + 0.0])


# RK4 with care at v ~ 0 (start from tiny v)
dt5 = 1e-3
s = np.array([0.0, 0.01])                    # tiny initial v
for _ in range(int(t5 / dt5)):
    k1 = f_lift(s)
    k2 = f_lift(s + dt5 / 2 * k1)
    k3 = f_lift(s + dt5 / 2 * k2)
    k4 = f_lift(s + dt5 * k3)
    s = s + dt5 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
E_num = 0.5 * m5 * s[1] ** 2 + m5 * g * s[0]
E_eq = P5 * t5
ok5 = abs(E_num - E_eq) / E_eq < 0.005
print("[Exp 5] constant-power lift (P=10 kW, m=1000 kg), t=2 s")
print("  RK4: v = %.3f m/s,  0.5 m v^2 + mgh = %.0f J" % (s[1], E_num))
print("  power eq: 0.5 m v^2 + mgh = P t = %.0f J, diff %.0f J (%.2f%%)  %s"
      % (E_eq, abs(E_num - E_eq), 100 * abs(E_num - E_eq) / E_eq, "PASS" if ok5 else "FAIL"))
print("  (RK4 dt=1e-3 resolves the early transient v->0 singularity)")

flags = [ok1a, ok1b, ok2, ok3, ok4, ok5]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
