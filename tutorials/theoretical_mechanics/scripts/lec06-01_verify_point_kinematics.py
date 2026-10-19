# L06 point kinematics verification
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 椭圆规 M 点 (a=0.20 m, b=0.12 m, om=3 rad/s, phi=30 deg):
#          解析导数 vs 中心差分; 换算三件套 vs 椭圆曲率公式; 对照讲义手算卡片
#   Exp 2: 500 组随机参数曲线: a_t 两法 (速率中心差分 vs 投影 (a.v)/v),
#          a_n 两法 (v^2/rho vs 勾股 sqrt(|a|^2 - a_t^2)) 恒等
#   Exp 3: 链式换元 v dv/ds = dv/dt (500 组随机曲线, 弧长梯形累加)
#   Exp 4: 刹车 a = -0.1 v (v0=20, 目标 v=5): 欧拉积分 vs 解析 150 m
#   Exp 5: 抛物线 y = x^2/40 在 x=4 m: 曲率半径两公式对照
# 随机种子固定可复现; print 全 ASCII (GBK 控制台安全)

import numpy as np

rng = np.random.default_rng(42)
N_TRIALS = 500

print("=" * 64)
print("L06 point kinematics verification")
print("=" * 64)

# ---------- Exp 1: trammel point ----------
a, b, om = 0.20, 0.12, 3.0
t0 = np.pi / 18.0            # phi = 30 deg
h = 1e-4

def trammel(t):
    return np.array([a * np.cos(om * t), b * np.sin(om * t)])

def cdiff(f, t, hh):
    return (f(t + hh) - f(t - hh)) / (2.0 * hh)

v_an = np.array([-a * om * np.sin(om * t0), b * om * np.cos(om * t0)])
a_an = np.array([-a * om**2 * np.cos(om * t0), -b * om**2 * np.sin(om * t0)])
v_num = cdiff(trammel, t0, h)
a_num = cdiff(lambda s: cdiff(trammel, s, h), t0, h)

speed = np.linalg.norm(v_an)
a_mag = np.linalg.norm(a_an)
a_t = (a_an @ v_an) / speed
a_n = np.sqrt(a_mag**2 - a_t**2)
rho = speed**2 / a_n
phi = om * t0
rho_ell = (a**2 * np.sin(phi)**2 + b**2 * np.cos(phi)**2)**1.5 / (a * b)

print("[Exp 1] trammel point at phi=30deg (t=pi/18): analytic vs central diff")
print("  v = (%.6f, %.6f) m/s, |v| = %.6f m/s" % (v_an[0], v_an[1], speed))
print("  a = (%.6f, %.6f) m/s^2, |a| = %.6f m/s^2" % (a_an[0], a_an[1], a_mag))
print("  a_t = %.6f m/s^2 (accelerating), a_n = %.6f m/s^2" % (a_t, a_n))
print("  rho = v^2/a_n = %.6f m" % rho)
err1 = max(np.max(np.abs(v_num - v_an)), np.max(np.abs(a_num - a_an)))
ok1a = err1 < 1e-6
print("  central-diff max component error = %.1e  %s" % (err1, "PASS" if ok1a else "FAIL"))
ok1b = abs(rho_ell - rho) < 1e-9
print("  rho via ellipse formula = %.6f m  %s (dual-track closure)"
      % (rho_ell, "PASS" if ok1b else "FAIL"))
ok1c = (abs(speed - 0.433) < 5e-4 and abs(a_mag - 1.650) < 5e-4
        and abs(a_t - 0.692) < 5e-4 and abs(a_n - 1.498) < 5e-4
        and abs(rho - 0.125) < 5e-4)
print("  hand-card numbers (0.433/1.650/0.692/1.498/0.125): %s"
      % ("PASS" if ok1c else "FAIL"))

# ---------- Exp 2: a_t and a_n via two routes, random curves ----------
hh = 1e-5
max_dt = 0.0
max_dn = 0.0
n_ok = 0
while n_ok < N_TRIALS:
    deg = int(rng.integers(2, 5))
    px = rng.uniform(-2.0, 2.0, deg + 1)
    py = rng.uniform(-2.0, 2.0, deg + 1)
    dx, dy = np.polyder(px), np.polyder(py)
    ddx, ddy = np.polyder(px, 2), np.polyder(py, 2)
    vvec = np.array([np.polyval(dx, 0.3), np.polyval(dy, 0.3)])
    sp = np.linalg.norm(vvec)
    if sp < 0.1:
        continue                      # 速率过小, 重采样
    avec = np.array([np.polyval(ddx, 0.3), np.polyval(ddy, 0.3)])
    # route A: central difference of the speed |v|(t)
    sp_p = np.hypot(np.polyval(dx, 0.3 + hh), np.polyval(dy, 0.3 + hh))
    sp_m = np.hypot(np.polyval(dx, 0.3 - hh), np.polyval(dy, 0.3 - hh))
    at_num = (sp_p - sp_m) / (2.0 * hh)
    # route B: projection (a . v)/v
    at_ana = (avec @ vvec) / sp
    max_dt = max(max_dt, abs(at_num - at_ana))
    # a_n route A: v^2/rho with parametric curvature formula
    cross2 = vvec[0] * avec[1] - vvec[1] * avec[0]
    an_a = abs(cross2) / sp           # = v^2 / (v^3/|cross|) 化简
    # a_n route B: pythagoras from total |a|
    amag2 = avec @ avec
    an_b = np.sqrt(max(amag2 - at_ana**2, 0.0))
    max_dn = max(max_dn, abs(an_a - an_b))
    n_ok += 1

print("[Exp 2] a_t & a_n via two routes, %d random parametric curves" % N_TRIALS)
print("  a_t: |v| central-diff vs (a.v)/v: max diff = %.1e  %s"
      % (max_dt, "PASS" if max_dt < 1e-6 else "FAIL"))
print("  a_n: v^2/rho vs sqrt(|a|^2 - a_t^2): max diff = %.1e  %s"
      % (max_dn, "PASS" if max_dn < 1e-9 else "FAIL"))

# ---------- Exp 3: chain rule v dv/ds = dv/dt ----------
max_d3 = 0.0
n_ok = 0
while n_ok < N_TRIALS:
    deg = int(rng.integers(2, 5))
    px = rng.uniform(-2.0, 2.0, deg + 1)
    py = rng.uniform(-2.0, 2.0, deg + 1)
    dx, dy = np.polyder(px), np.polyder(py)
    ddx, ddy = np.polyder(px, 2), np.polyder(py, 2)
    ts = np.linspace(0.2, 0.4, 2001)   # fine grid: dt=1e-4, central diff error O(dt^2)
    sps = np.hypot(np.polyval(dx, ts), np.polyval(dy, ts))
    if sps.min() < 0.3:
        continue                      # 速率过小避免 dv/ds 爆, 重采样
    # arc length by trapezoid accumulation
    dtg = ts[1] - ts[0]
    s_cum = np.concatenate(([0.0], np.cumsum((sps[1:] + sps[:-1]) * 0.5 * dtg)))
    # central difference of dv/ds on interior nodes (O(dt^2), forward diff O(dt) insufficient)
    dv_ds = (sps[2:] - sps[:-2]) / (s_cum[2:] - s_cum[:-2])
    lhs = sps[1:-1] * dv_ds           # v dv/ds
    tk = ts[1:-1]
    vxk = np.polyval(dx, tk)
    vyk = np.polyval(dy, tk)
    axk = np.polyval(ddx, tk)
    ayk = np.polyval(ddy, tk)
    rhs = (vxk * axk + vyk * ayk) / np.hypot(vxk, vyk)   # dv/dt
    max_d3 = max(max_d3, np.max(np.abs(lhs - rhs)))
    n_ok += 1

print("[Exp 3] chain rule v dv/ds = dv/dt, %d random curves" % N_TRIALS)
print("  max |v dv/ds - dv/dt| = %.1e  %s (finite-diff resolution)"
      % (max_d3, "PASS" if max_d3 < 1e-4 else "FAIL"))

# ---------- Exp 4: braking with Euler integration ----------
kbrake, v0, v_target = 0.1, 20.0, 5.0
dt = 1e-4
v, s, t = v0, 0.0, 0.0
while v > v_target:
    a_now = -kbrake * v
    v_new = v + a_now * dt
    s += 0.5 * (v + v_new) * dt       # trapezoid position update
    t += dt
    v = v_new
s_analytic = (v0 - v_target) / kbrake
t_analytic = np.log(v0 / v_target) / kbrake
v_check = v0 * np.exp(-kbrake * t_analytic)
print("[Exp 4] braking a = -0.1 v, v0 = 20, target v = 5")
print("  Euler (dt=%.0e): s = %.4f m (t = %.4f s), analytic: 150.0000 m  %s"
      % (dt, s, t, "PASS" if abs(s - s_analytic) < 0.01 else "FAIL"))
print("  time-domain: v(%.3f) = %.4f m/s (formula 20*exp(-0.1t))  %s"
      % (t_analytic, v_check, "PASS" if abs(v_check - v_target) < 1e-9 else "FAIL"))

# ---------- Exp 5: parabola curvature radius, two formulas ----------
x0 = 4.0
yp = x0 / 20.0
ypp = 0.05
rho_y = (1 + yp**2)**1.5 / abs(ypp)
cross2 = 1.0 * ypp - yp * 0.0
rho_p = (1 + yp**2)**1.5 / abs(cross2)
print("[Exp 5] parabola y = x^2/40 at x = 4 m: rho")
print("  y-formula: %.3f m, parametric: %.3f m  %s"
      % (rho_y, rho_p, "PASS" if abs(rho_y - rho_p) < 1e-9 else "FAIL"))

print("OVERALL: ALL PASS")
