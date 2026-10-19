# L11 non-inertial dynamics verification
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 加速车厢单摆双路线恒等 (惯性系方程 vs 有效重力摆方程, 两段独立代码)
#          + 加阻尼收敛到稳态偏角 14.04 deg + 张力 2.02 N
#   Exp 2: 弹簧槽系统: r_eq = k*r0/(k - m*w^2) = 0.20833 (离心外移)
#   Exp 3: 落体偏东: 三维 RK4 完整科氏项 vs 近似公式 (h=100 m, lat 45 deg)
#   Exp 4: 转盘静摩擦二分: f_min=0.4898, mu=0.49 sticks; mu=0.45 滑动模型外漂
#   Exp 5: 例1/例2 手算卡复算
# print 全 ASCII (GBK 控制台安全)

import numpy as np

print("=" * 64)
print("L11 non-inertial dynamics verification")
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


# ---------- Exp 1: pendulum in accelerating car, two routes ----------
a_car, m_p, l_p, c_p = 2.45, 0.2, 0.5, 1.5
theta0_eq = -np.arctan(a_car / g)          # theta measured from vertical, +x fwd


def f_inertial(s):                          # l*theta'' = -(g sin + a cos) - c*theta'
    return np.array([s[1], -(g * np.sin(s[0]) + a_car * np.cos(s[0])) / l_p
                     - c_p * s[1]])


g_eff = np.hypot(g, a_car)


def f_moving(s):                            # theta'' = -(g_eff/l) sin(theta - theta_eq) - c theta'
    return np.array([s[1], -g_eff / l_p * np.sin(s[0] - theta0_eq) - c_p * s[1]])


dt = 1e-3
n = 10000                                   # 10 s
s1 = rk4_scalar(f_inertial, [0.0, 0.0], dt, n)
s2 = rk4_scalar(f_moving, [0.0, 0.0], dt, n)
# track both trajectories step-by-step, record max angle difference
sA = np.array([0.0, 0.0])
sB = np.array([0.0, 0.0])
max_diff = 0.0
for step in range(n):
    k1 = f_inertial(sA)
    k2 = f_inertial(sA + dt / 2 * k1)
    k3 = f_inertial(sA + dt / 2 * k2)
    k4 = f_inertial(sA + dt * k3)
    sA = sA + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    k1 = f_moving(sB)
    k2 = f_moving(sB + dt / 2 * k1)
    k3 = f_moving(sB + dt / 2 * k2)
    k4 = f_moving(sB + dt * k3)
    sB = sB + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    if step % 100 == 0:
        max_diff = max(max_diff, abs(sA[0] - sB[0]))
theta_steady = abs(sA[0])
T_tension = m_p * g_eff
ok1 = (max_diff < 1e-12 and abs(np.rad2deg(theta_steady) - 14.04) < 0.05
       and abs(T_tension - 2.02) < 0.005)
print("[Exp 1] pendulum in accelerating car (a=2.45, l=0.5, damping %.1f)" % c_p)
print("  two-route trajectories: max |theta1 - theta2| = %.1e  %s"
      % (max_diff, "PASS" if max_diff < 1e-12 else "FAIL"))
print("  steady-state |theta| = %.2f deg (analytic arctan(a/g)=%.2f)  %s"
      % (np.rad2deg(theta_steady), np.rad2deg(np.arctan(a_car / g)),
         "PASS" if abs(np.rad2deg(theta_steady) - 14.04) < 0.05 else "FAIL"))
print("  T = m*g_eff = %.2f N (g_eff = %.3f)  %s"
      % (T_tension, g_eff, "PASS" if abs(T_tension - 2.02) < 0.005 else "FAIL"))

# ---------- Exp 2: spring-in-slot equilibrium ----------
m_s, k_s, w_s, r0_s, c_s = 0.5, 200.0, 4.0, 0.2, 4.0


def f_slot(s):
    return np.array([s[1], w_s ** 2 * s[0] - (k_s / m_s) * (s[0] - r0_s) - c_s * s[1]])


s_eq = rk4_scalar(f_slot, [r0_s, 0.0], 1e-3, 2000)
r_eq_ana = k_s * r0_s / (k_s - m_s * w_s ** 2)
ok2 = abs(s_eq[0] - r_eq_ana) < 1e-4
print("[Exp 2] spring-in-slot on turntable (m=0.5, k=200, w=4, r0=0.2)")
print("  equilibrium r_eq = %.5f m (analytic k*r0/(k-m*w^2)=%.5f)  %s"
      % (s_eq[0], r_eq_ana, "PASS" if ok2 else "FAIL"))
print("  note: inertial-frame derivation and 'centrifugal' bookkeeping give")
print("        the SAME equation: r'' - w^2 r = -(k/m)(r-r0)")

# ---------- Exp 3: eastward deflection, full Coriolis, 3D RK4 ----------
w_e = 7.292e-5
lam = np.deg2rad(45.0)
wy, wz = w_e * np.cos(lam), w_e * np.sin(lam)


def f_fall(t, s):
    vx, vy, vz = s[3], s[4], s[5]
    return np.array([vx, vy, vz,
                     -2 * (wy * vz - wz * vy),
                     -2 * (wz * vx - 0.0 * vz),
                     -g + 2 * wy * vx])


dt3 = 1e-3
s = np.zeros(6)
t = 0.0
h_tower = 100.0
landed = False
for _ in range(10000):
    k1 = f_fall(t, s)
    k2 = f_fall(t + dt3 / 2, s + dt3 / 2 * k1)
    k3 = f_fall(t + dt3 / 2, s + dt3 / 2 * k2)
    k4 = f_fall(t + dt3, s + dt3 * k3)
    s_new = s + dt3 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    if s_new[2] <= -h_tower:
        frac = (s[2] + h_tower) / (s[2] - s_new[2])
        x_land = s[0] + frac * (s_new[0] - s[0])
        y_land = s[4] + frac * (s_new[4] - s[4])
        t_land = t + frac * dt3
        landed = True
        break
    s = s_new
    t += dt3
t_fall = np.sqrt(2 * h_tower / g)
delta_formula = w_e * g * np.cos(lam) * t_fall ** 3 / 3.0
diff_pct = 100 * abs(x_land - delta_formula) / delta_formula
ok3 = landed and diff_pct < 1.0
print("[Exp 3] eastward deflection of falling body (h=100 m, lat 45 deg)")
print("  numeric:  delta_E = %.3e m, delta_S = %.2e m (t_land = %.3f s)"
      % (x_land, y_land, t_land))
print("  formula:  delta_E = (1/3)*w*g*cos(lat)*t^3 = %.3e m" % delta_formula)
print("  diff = %.1e m (%.2f%%)  %s; south drift is 2nd-order (w^2), as stated"
      % (abs(x_land - delta_formula), diff_pct, "PASS" if ok3 else "FAIL"))

# ---------- Exp 4: turntable static friction, stick-or-slip ----------
m_b, w_b, r_b = 0.5, 4.0, 0.3
f_min = w_b ** 2 * r_b / g
need = m_b * w_b ** 2 * r_b
cap_49 = 0.49 * m_b * g
stick_ok = need <= cap_49
# sliding model with mu=0.45, tiny initial outward slip to avoid stick-slip switch
mu_sl = 0.45


def f_slide(t, s):
    x, y, vx, vy = s
    wv = np.array([-w_b * y, w_b * x])       # table velocity at this point
    u = np.array([vx, vy]) - wv
    un = np.linalg.norm(u)
    if un < 1e-12:
        fric = np.zeros(2)
    else:
        fric = -mu_sl * m_b * g * u / un
    return np.array([vx, vy, fric[0] / m_b, fric[1] / m_b])


s4 = np.array([r_b, 0.0, 0.01, w_b * r_b])  # tiny outward slip + table speed
t4 = 0.0
for _ in range(2000):
    k1 = f_slide(t4, s4)
    k2 = f_slide(t4 + dt / 2, s4 + dt / 2 * k1)
    k3 = f_slide(t4 + dt / 2, s4 + dt / 2 * k2)
    k4 = f_slide(t4 + dt, s4 + dt * k3)
    s4 = s4 + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    t4 += dt
r_end = np.hypot(s4[0], s4[1])
ok4 = stick_ok and (r_end - r_b) > 0.01
print("[Exp 4] turntable static friction (m=0.5, w=4, r=0.3)")
print("  f_min = w^2*r/g = %.4f; mu=0.49 -> %s (%.3f <= %.3f N)  %s"
      % (f_min, "sticks" if stick_ok else "slips", need, cap_49,
         "PASS" if stick_ok else "FAIL"))
print("  mu=0.45 sliding model from tiny initial slip: r(2s) drift")
print("    r: %.4f -> %.4f m (outward drift +%.1f cm)  %s"
      % (r_b, r_end, 100 * (r_end - r_b), "PASS" if (r_end - r_b) > 0.01 else "FAIL"))

# ---------- Exp 5: hand-card replay ----------
th_hd = np.rad2deg(np.arctan(2.45 / 9.8))
T_hd = 0.2 * np.hypot(9.8, 2.45)
F_hd = 0.5 * 16 * 0.3
ok5 = (abs(th_hd - 14.04) < 0.01 and abs(T_hd - 2.02) < 0.005
       and abs(F_hd - 2.4) < 1e-9 and abs(f_min - 0.4898) < 1e-4)
print("[Exp 5] hand-card replay: theta=%.2f deg, T=%.2f N, F_je=%.1f N, f_min=%.4f  %s"
      % (th_hd, T_hd, F_hd, f_min, "PASS" if ok5 else "FAIL"))

flags = [ok1, ok2, ok3, ok4, ok5]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
