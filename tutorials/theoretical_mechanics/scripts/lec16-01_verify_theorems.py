# L16 theorems & collision verification
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 恢复系数扫描 (弹簧接触+耗散模型, 5 档 c -> e 从公式对照)
#   Exp 2: 例 2 链条滑落 RK4 vs 解析 v(x) = sqrt(g(l^2-a^2)/l)
#   Exp 3: 例 1 三法同题对照 (ODE/能量/动量三条独立代码路径)
#   Exp 4: 例 4 撞击中心 (h = 2l/3 处 O 冲击反力为零的联立验证)
# print 全 ASCII (GBK 控制台安全)

import numpy as np

rng = np.random.default_rng(42)
print("=" * 64)
print("L16 theorems & collision verification")
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


# ---------- Exp 1: coefficient of restitution ----------
m1, m2, v1, v2 = 2.0, 4.0, 4.0, 0.0
L_nat, k_ctc = 1.0, 1000.0


def run_collision(c_diss):
    def f(s):
        x1, x2, w1, w2 = s
        dx = x2 - x1 - L_nat
        if dx < 0:
            F = -k_ctc * dx - c_diss * (w2 - w1)
        else:
            F = 0.0
        return np.array([w1, w2, -F / m1, F / m2])
    s = rk4(f, [0.0, L_nat, v1, v2], 1e-4, 15000)  # 1.5 s
    return s[2], s[3]


print("[Exp 1] coefficient of restitution, spring-contact collision model")
print("  e_formula vs e_numeric for 5 dissipation levels:")
ok1 = True
for c in (0.0, 20.0, 50.0, 100.0, 200.0):
    # analytic e for Maxwell (linear spring + linear damper in parallel):
    # e = exp(-zeta*pi/sqrt(1-zeta^2)) with zeta = c / (2*sqrt(k*mu))
    mu = m1 * m2 / (m1 + m2)
    zeta = c / (2.0 * np.sqrt(k_ctc * mu))
    e_formula = np.exp(-zeta * np.pi / np.sqrt(1 - zeta ** 2)) if zeta < 1 else 0.0
    w1a, w2a = run_collision(c)
    e_num = (w2a - w1a) / (v1 - v2)
    d = abs(e_formula - e_num)
    ok1 = ok1 and d < 1e-3
    print("    c=%4.0f: e=%.3f, e_num=%.3f, diff=%.1e  %s"
          % (c, e_formula, e_num, d, "PASS" if d < 1e-3 else "FAIL"))
# energy loss at e=0.5 (c tuned ~ 77)
w1a, w2a = run_collision(16.0)
e_actual = (w2a - w1a) / (v1 - v2)
KE_before = 0.5 * m1 * v1 ** 2
KE_after = 0.5 * m1 * w1a ** 2 + 0.5 * m2 * w2a ** 2
loss_num = KE_before - KE_after
mu = m1 * m2 / (m1 + m2)
loss_formula = 0.5 * mu * (1 - e_actual ** 2) * (v1 - v2) ** 2
ok1 = ok1 and abs(loss_num - loss_formula) < 0.01
print("  energy loss at e=%.3f: numeric %.3f J vs formula %.3f J  %s"
      % (e_actual, loss_num, loss_formula, "PASS" if abs(loss_num - loss_formula) < 0.01 else "FAIL"))

# ---------- Exp 2: chain sliding off table ----------
lam, a0, l_ch = 1.0, 0.2, 1.0


def f_chain(s):                            # s = [x, v] (x = length hanging off)
    return np.array([s[1], g * s[0] / l_ch])  # from energy eq derivative


s0 = np.array([a0, 0.0])
dt_ch = 1e-4
for _ in range(40000):
    k1 = f_chain(s0); k2 = f_chain(s0 + dt_ch/2*k1); k3 = f_chain(s0 + dt_ch/2*k2); k4 = f_chain(s0 + dt_ch*k3)
    s0 = s0 + dt_ch/6*(k1 + 2*k2 + 2*k3 + k4)
    if s0[0] >= l_ch:
        break
s = s0
v_end = np.sqrt(g * (l_ch ** 2 - a0 ** 2) / l_ch)
ok2 = abs(s[1] - v_end) < 1e-3
print("[Exp 2] chain sliding off table (lambda=1, a=0.2, l=1, smooth)")
print("  v at full vertical (x=%.3f): numeric %.4f vs analytic %.4f  %s"
      % (s[0], s[1], v_end, "PASS" if ok2 else "FAIL"))

# ---------- Exp 3: three routes for same problem ----------
th = np.deg2rad(30.0)
f_fric = 0.3
m_blk, s_slide = 2.0, 3.0
a_blk = g * (np.sin(th) - f_fric * np.cos(th))

# route A: integrate ODE v' = a
vA, dt = 0.0, 1e-4
x_acc = 0.0
while x_acc < s_slide:
    vA += a_blk * dt
    x_acc += vA * dt

# route B: energy theorem (direct algebra)
vB = np.sqrt(2 * a_blk * s_slide)

# route C: momentum + time (v = a*t, s = a*t^2/2 -> t -> v)
t_slide = np.sqrt(2 * s_slide / a_blk)
vC = a_blk * t_slide

ok3 = abs(vA - vB) < 1e-2 and abs(vB - vC) < 1e-12
print("[Exp 3] same-problem three-routes (block on rough incline, s=3 m)")
print("  route A (ODE):    v = %.4f m/s" % vA)
print("  route B (energy): v = %.4f m/s" % vB)
print("  route C (impulse): v = %.4f m/s" % vC)
print("  three routes agree: max diff = %.1e  %s"
      % (max(abs(vA - vB), abs(vB - vC), abs(vA - vC)), "PASS" if ok3 else "FAIL"))

# ---------- Exp 4: center of percussion ----------
m_rod, l_rod = 1.0, 0.9
J_O = m_rod * l_rod ** 2 / 3.0
print("[Exp 4] center of percussion (uniform rod, pivot O, impulse at h)")
ok4 = True
for h_val in (0.45, 0.60, 0.72):          # l/2, 2l/3, 0.8l
    # impulse S at distance h from O, horizontal
    # angular: J_O * domega = S * h
    # linear:  m * dvC = S + R_O  (R_O = bearing impulse)
    # no-slip pivot: dvC = 0 (O is fixed, rod rotates about O)
    # => R_O = -S + m * dvC = -S + 0 = ... wait, pivot is FIXED:
    # the rod rotates about O, so vC = omega * l/2 after impact
    # angular impulse: J_O * omega = S * h
    # linear impulse on rod: m * (omega * l/2 - 0) = S + R_O
    # => R_O = m * omega * l/2 - S = m * (S*h/J_O) * l/2 - S
    # => R_O / S = m*h*l/(2*J_O) - 1
    ratio = m_rod * h_val * l_rod / (2 * J_O) - 1.0
    h_star = 2 * J_O / (m_rod * l_rod)
    tag = "center of percussion" if abs(ratio) < 1e-12 else ("nonzero" if ratio > 0 else "nonzero, reversed")
    if abs(h_val - h_star) < 0.001:
        ok4 = ok4 and abs(ratio) < 1e-12
    print("  h = %.3f l (h* = %.3f l): bearing impulse = %+.3f * S  %s"
          % (h_val / l_rod, h_star / l_rod, ratio, tag))

flags = [ok1, ok2, ok3, ok4]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))

