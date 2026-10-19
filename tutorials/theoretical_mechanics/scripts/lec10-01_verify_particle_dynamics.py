# L10 particle dynamics verification
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 例3 抛体: 欧拉/RK4 vs 解析 (t=1 s)
#   Exp 2: 例4 跳伞线性阻力: 数值 vs v_t(1-exp(-t/tau)), y 同 (t=1.53 s)
#   Exp 3: v^2 阻力: RK4 vs tanh 解析 (v_t=5, t=1.53 s)
#   Exp 4: 收敛阶体检: 欧拉 O(dt) vs RK4 O(dt^4), dt 扫 {0.1, 0.01, 0.001}
#   Exp 5: 例2 拱桥 N(v) 扫描 + 数值过零 vs sqrt(gR)
# 状态向量法: 二阶方程拆一阶组 s' = f(t, s); print 全 ASCII

import numpy as np

print("=" * 64)
print("L10 particle dynamics verification")
print("=" * 64)


def integrate(f, s0, t_end, dt, method):
    """通用积分器: s' = f(t, s), 从 0 到 t_end."""
    s = np.array(s0, dtype=float)
    t = 0.0
    n = int(round(t_end / dt))
    for _ in range(n):
        if method == "euler":
            s = s + dt * f(t, s)
        else:
            k1 = f(t, s)
            k2 = f(t + dt / 2, s + dt / 2 * k1)
            k3 = f(t + dt / 2, s + dt / 2 * k2)
            k4 = f(t + dt, s + dt * k3)
            s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += dt
    return s


g = 9.8

# ---------- Exp 1: projectile ----------
v0, th = 20.0, np.deg2rad(30.0)
vx0, vy0 = v0 * np.cos(th), v0 * np.sin(th)


def f_proj(t, s):
    return np.array([s[2], s[3], 0.0, -g])


xa, ya = vx0 * 1.0, vy0 * 1.0 - 0.5 * g * 1.0
s_e = integrate(f_proj, [0, 0, vx0, vy0], 1.0, 1e-3, "euler")
s_r = integrate(f_proj, [0, 0, vx0, vy0], 1.0, 1e-3, "rk4")
ok1 = abs(s_r[0] - xa) < 1e-9 and abs(s_r[1] - ya) < 1e-9 and abs(s_e[1] - ya) < 0.01
print("[Exp 1] projectile (v0=20 m/s, 30 deg): numeric vs analytic at t=1 s")
print("  analytic:  x = %.4f, y = %.4f" % (xa, ya))
print("  Euler  (dt=1e-3): x = %.4f, y = %.4f  (err %.1e)" % (s_e[0], s_e[1], abs(s_e[1] - ya)))
print("  RK4    (dt=1e-3): x = %.4f, y = %.4f  (err %.1e)  %s"
      % (s_r[0], s_r[1], abs(s_r[1] - ya), "PASS" if ok1 else "FAIL"))

# ---------- Exp 2: skydiver, linear drag ----------
m, vt = 80.0, 5.0
k = m * g / vt
tau = m / k


def f_lin(t, s):
    return np.array([s[1], g - (k / m) * s[1]])


t_q = 1.53                         # grid-aligned (3*tau=1.5306 is NOT a multiple
                                   # of dt=1e-3 -- off-grid endpoints inflate error;
                                   # lecture rounds to 1.53 s, y=5.23 m holds either way)
v_ana = vt * (1 - np.exp(-t_q / tau))
y_ana = vt * t_q - vt * tau * (1 - np.exp(-t_q / tau))
s_e2 = integrate(f_lin, [0.0, 0.0], t_q, 1e-4, "euler")
s_r2 = integrate(f_lin, [0.0, 0.0], t_q, 1e-3, "rk4")
ok2 = abs(s_r2[1] - v_ana) < 1e-8 and abs(s_r2[0] - y_ana) < 1e-8 and abs(s_e2[1] - v_ana) < 0.01
print("[Exp 2] skydiver linear drag (v_t=5, tau=%.3f): t=%.2f s" % (tau, t_q))
print("  analytic:  v = %.4f, y = %.4f" % (v_ana, y_ana))
print("  Euler  (dt=1e-4): v = %.4f, y = %.4f  (v err %.1e)"
      % (s_e2[1], s_e2[0], abs(s_e2[1] - v_ana)))
print("  RK4    (dt=1e-3): v = %.4f, y = %.4f  %s"
      % (s_r2[1], s_r2[0], "PASS" if ok2 else "FAIL"))

# ---------- Exp 3: quadratic drag vs tanh ----------
c = m * g / vt ** 2


def f_quad(t, s):
    return np.array([s[1], g - (c / m) * s[1] ** 2])


v_tanh = vt * np.tanh(g * t_q / vt)
s_r3 = integrate(f_quad, [0.0, 0.0], t_q, 1e-3, "rk4")
ok3 = abs(s_r3[1] - v_tanh) < 1e-8
print("[Exp 3] quadratic drag (v_t=5): t=%.2f s" % t_q)
print("  analytic (tanh): v = %.4f" % v_tanh)
print("  RK4    (dt=1e-3): v = %.4f  %s" % (s_r3[1], "PASS" if ok3 else "FAIL"))
print("  note: quadratic drag reaches %.1f%% of v_t at t=%.2f s (linear: %.1f%%)"
      % (100 * v_tanh / vt, t_q, 100 * v_ana / vt))

# ---------- Exp 4: convergence order check ----------
v_exact = vt * (1 - np.exp(-1.0 / tau))
print("[Exp 4] convergence order check: v(1 s) of linear-drag fall, err vs dt")
euler_errs = []
rk4_errs = []
for dt in (0.1, 0.01, 0.001):
    ve = integrate(f_lin, [0.0, 0.0], 1.0, dt, "euler")[1]
    vr = integrate(f_lin, [0.0, 0.0], 1.0, dt, "rk4")[1]
    euler_errs.append(abs(ve - v_exact))
    rk4_errs.append(abs(vr - v_exact))
    print("  dt=%.3f: Euler err=%.2e, RK4 err=%.2e" % (dt, euler_errs[-1], rk4_errs[-1]))
r_e = euler_errs[0] / euler_errs[1]
r_e2 = euler_errs[1] / euler_errs[2]
r_r = rk4_errs[0] / rk4_errs[1]
r_r2 = rk4_errs[1] / rk4_errs[2]
ok4 = (8 < r_e < 12) and (8 < r_e2 < 12) and r_r > 500 and r_r2 > 500
print("  Euler ratios: %.1f, %.1f -> order ~1" % (r_e, r_e2))
print("  RK4   ratios: %.1e, %.1e -> order ~4%s"
      % (r_r, r_r2, " (float floor)" if rk4_errs[2] < 1e-12 else ""))
print("  %s: Euler order 1, RK4 order 4 (empirical)" % ("PASS" if ok4 else "FAIL"))

# ---------- Exp 5: hump bridge N(v) scan and liftoff ----------
mB, R = 1500.0, 50.0
vs = np.arange(0.0, 25.0001, 0.001)
Ns = mB * (g - vs ** 2 / R)
N20 = mB * (g - 400.0 / R)
# numeric zero crossing by sign change + linear interpolation
idx = np.where(Ns < 0)[0][0]
v1, v2 = vs[idx - 1], vs[idx]
N1, N2 = Ns[idx - 1], Ns[idx]
v_lift = v1 + (0.0 - N1) * (v2 - v1) / (N2 - N1)
v_ana_lift = np.sqrt(g * R)
ok5 = abs(N20 - 2700.0) < 1e-6 and abs(v_lift - v_ana_lift) < 0.01
print("[Exp 5] hump bridge N(v) scan (m=1500, R=50)")
print("  N at v=20 m/s: %.1f N (analytic 2700.0)  %s"
      % (N20, "PASS" if abs(N20 - 2700.0) < 1e-6 else "FAIL"))
print("  numeric liftoff speed: %.3f m/s vs sqrt(gR)=%.3f  %s"
      % (v_lift, v_ana_lift, "PASS" if abs(v_lift - v_ana_lift) < 0.01 else "FAIL"))

flags = [ok1, ok2, ok3, ok4, ok5]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
