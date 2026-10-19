# L12 momentum theorem verification
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 质点动量定理: 500 组随机变力 F(t), 数值冲量 vs delta p 两路独立
#   Exp 2: 两球接触弹簧碰撞 (k 扫 100/1000/10000 + 耗散版):
#          碰撞前后总动量不变 (能量账才依赖 k) -- "内力细节无关"实证
#   Exp 3: 人-船互推 (任意内力波形): 总动量恒零 + 质心不动
#   Exp 4: 空中爆炸成三片 (随机内冲量对): 碎片质心轨迹 vs 原抛物线逐点重合
#   Exp 5: 火箭变质量: 数值逐时刻记账 vs 齐奥尔科夫斯基公式
# print 全 ASCII (GBK 控制台安全)

import numpy as np

rng = np.random.default_rng(42)
print("=" * 64)
print("L12 momentum theorem verification")
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


# ---------- Exp 1: impulse = delta p, 500 random forces ----------
N = 500
max_d1 = 0.0
cnt = 0
while cnt < N:
    Fc = rng.uniform(-5.0, 5.0, 4)            # F(t) poly deg 3
    m = rng.uniform(0.5, 3.0)
    v0 = rng.uniform(-2.0, 2.0)
    t_end = 1.0

    def f_v(s):                                # dv/dt = F(t)/m at fixed t? use closure
        t = s[1]
        return np.array([np.polyval(Fc, t) / m, 1.0])

    s = rk4(f_v, [v0, 0.0], 1e-3, 1000)        # integrate v and t together
    delta_p = m * (s[0] - v0)
    ts = np.linspace(0.0, t_end, 100001)       # trapezoid integral of F
    Fs = np.polyval(Fc, ts)
    impulse = np.trapezoid(Fs, ts)             # numpy 2.x renamed trapz
    max_d1 = max(max_d1, abs(impulse - delta_p))
    cnt += 1
ok1 = max_d1 < 1e-8
print("[Exp 1] particle impulse-momentum: %d random F(t)" % N)
print("  max | impulse(integral) - delta p | = %.1e  %s"
      % (max_d1, "PASS" if ok1 else "FAIL"))

# ---------- Exp 2: two-body collision via contact spring ----------
m1, m2, v1_0, v2_0, L_nat = 2.0, 4.0, 3.0, 0.0, 1.0


def run_collision(k, c_diss=0.0):
    def f(s):
        x1, x2, w1, w2 = s
        dx = x2 - x1 - L_nat
        if dx < 0:
            F = -k * dx - c_diss * (w2 - w1)   # push-apart + dissipation
        else:
            F = 0.0
        return np.array([w1, w2, -F / m1, F / m2])
    s = rk4(f, [0.0, L_nat, v1_0, v2_0], 1e-4, 10000)   # 1.0 s
    return s


print("[Exp 2] two-body collision via contact spring, momentum bookkeeping")
ok2 = True
for k in (100.0, 1000.0, 10000.0):
    s = run_collision(k)
    P_b = m1 * v1_0 + m2 * v2_0
    P_a = m1 * s[2] + m2 * s[3]
    d = abs(P_a - P_b)
    ok2 = ok2 and d < 1e-12
    print("  k=%6.0f: P_before=%.3f, P_after=%.3f, |diff|=%.1e  %s"
          % (k, P_b, P_a, d, "PASS" if d < 1e-12 else "FAIL"))
# dissipative version + energy accounting
s_el = run_collision(1000.0)
s_di = run_collision(1000.0, c_diss=30.0)
KE_b = 0.5 * m1 * v1_0 ** 2 + 0.5 * m2 * v2_0 ** 2
KE_el = 0.5 * m1 * s_el[2] ** 2 + 0.5 * m2 * s_el[3] ** 2
KE_di = 0.5 * m1 * s_di[2] ** 2 + 0.5 * m2 * s_di[3] ** 2
P_di = m1 * s_di[2] + m2 * s_di[3]
d_di = abs(P_di - (m1 * v1_0 + m2 * v2_0))
ok2 = ok2 and d_di < 1e-12
print("  with contact dissipation: P_after=%.3f, |diff|=%.1e  %s"
      % (P_di, d_di, "PASS" if d_di < 1e-12 else "FAIL"))
print("  (kinetic energy: elastic keeps %.1f%%, dissipative keeps %.1f%% --"
      % (100 * KE_el / KE_b, 100 * KE_di / KE_b))
print("   the energy account DOES depend on the contact model)")

# ---------- Exp 3: person-boat push ----------
m_p, m_b = 60.0, 120.0


def f_push(s):
    t = s[4]
    F = 200.0 * np.sin(np.pi * t / 0.5) if t < 0.5 else 0.0   # unknown profile
    return np.array([s[2], s[3], -F / m_p, F / m_b, 1.0])


# track P and COM over the push (0.5 s, sample every step)
s = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
dt = 1e-3
max_P = 0.0
max_xC = 0.0
x_C0 = 0.0
for _ in range(1000):
    k1 = f_push(s)
    k2 = f_push(s + dt / 2 * k1)
    k3 = f_push(s + dt / 2 * k2)
    k4 = f_push(s + dt * k3)
    s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    P = m_p * s[2] + m_b * s[3]
    x_C = (m_p * s[0] + m_b * s[1]) / (m_p + m_b)
    max_P = max(max_P, abs(P))
    max_xC = max(max_xC, abs(x_C - x_C0))
ok3 = max_P < 1e-12 and max_xC < 1e-12
print("[Exp 3] person-boat mutual push (unknown internal force profile)")
print("  total P: max |P(t)| over push = %.1e  %s (zero throughout)"
      % (max_P, "PASS" if max_P < 1e-12 else "FAIL"))
print("  center of mass: max displacement = %.1e  %s"
      % (max_xC, "PASS" if max_xC < 1e-12 else "FAIL"))

# ---------- Exp 4: mid-air explosion, COM follows original parabola ----------
v0x, v0y, g = 30.0, 40.0, 9.8
m_frags = np.array([6.0, 5.0, 4.0])
M_tot = m_frags.sum()
t_ex = 1.0
# pre-explosion: analytical (projectile)
x_ex = v0x * t_ex
y_ex = v0y * t_ex - 0.5 * g * t_ex ** 2
v_ex = np.array([v0x, v0y - g * t_ex])
# random impulse pairs, sum(m_i * dv_i) = 0
dv1 = rng.uniform(-15.0, 15.0, 2)
dv2 = rng.uniform(-15.0, 15.0, 2)
dv3 = -(m_frags[0] * dv1 + m_frags[1] * dv2) / m_frags[2]
dvs = np.stack([dv1, dv2, dv3])


def f_grav(s):
    return np.array([s[2], s[3], 0.0, -g])


def traj_com(t_end):
    # integrate each fragment from t_ex to t_end
    xs = []
    for i in range(3):
        s0 = np.array([x_ex, y_ex, v_ex[0] + dvs[i][0], v_ex[1] + dvs[i][1]])
        n = int(round((t_end - t_ex) / 1e-3))
        s = rk4(f_grav, s0, 1e-3, n)
        xs.append(s[:2])
    return (m_frags[0] * xs[0] + m_frags[1] * xs[1] + m_frags[2] * xs[2]) / M_tot


max_d4 = 0.0
for t_check in (2.0, 3.0, 4.0):
    com = traj_com(t_check)
    # original parabola (no explosion)
    tau = t_check - t_ex
    x_ana = x_ex + v_ex[0] * tau
    y_ana = y_ex + v_ex[1] * tau - 0.5 * g * tau ** 2
    # whole-flight original: x=v0x*t, y=v0y*t-4.9t^2 (same thing)
    d = np.linalg.norm(com - np.array([x_ana, y_ana]))
    max_d4 = max(max_d4, d)
ok4 = max_d4 < 1e-9
print("[Exp 4] mid-air explosion into 3 fragments (t=1 s, random impulses)")
print("  fragment COM vs original parabola: max |diff| = %.1e  %s"
      % (max_d4, "PASS" if ok4 else "FAIL"))
print("  (individual fragment trajectories wildly different)")

# ---------- Exp 5: rocket variable mass ----------
u, m0, m1_r, mdot = 2000.0, 100.0, 25.0, 1.0


def f_rocket(s):
    return np.array([u * mdot / s[1], -mdot])


t_burn = (m0 - m1_r) / mdot
s = rk4(f_rocket, [0.0, m0], 1e-4, int(round(t_burn / 1e-4)))
dv_num = s[0]
dv_ana = u * np.log(m0 / m1_r)
ok5 = abs(dv_num - dv_ana) < 1e-6
print("[Exp 5] rocket variable mass, u=2000 m/s, mass ratio 4")
print("  numeric dv = %.3f m/s vs Tsiolkovsky %.3f m/s  %s"
      % (dv_num, dv_ana, "PASS" if ok5 else "FAIL"))

flags = [ok1, ok2, ok3, ok4, ok5]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
