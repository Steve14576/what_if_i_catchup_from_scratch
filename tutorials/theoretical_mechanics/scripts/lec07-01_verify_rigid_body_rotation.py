# L07 rigid body rotation verification
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 例2例3 电机启动与滚筒刹车 (角量匀变速三式 vs 欧拉积分)
#   Exp 2: 例4 卷扬机全链传动账 (逐级转速/传动比/绳速复算)
#   Exp 3: 叉乘公式 vs 几何分量, 500 组随机空间斜轴
#          (|v| = omega*r_perp, v 垂直轴, w x (w x r) = -w^2 r_perp, |a x r| = alpha*r_perp)
#   Exp 4: 轨迹生成 -> 中心差分求 v, 对照解析 omega x r, 500 组随机 phi(t)
#   Exp 5: 平移复制 (两点速度差精确为零) vs 转动复制 (速度=叉乘公式, 与平移点不同)
# 随机种子固定可复现; print 全 ASCII (GBK 控制台安全)

import numpy as np

rng = np.random.default_rng(42)
N = 500

print("=" * 64)
print("L07 rigid body rotation verification")
print("=" * 64)

# ---------- Exp 1: motor start & drum brake ----------
n_rpm = 1440.0
w_target = n_rpm * 2.0 * np.pi / 60.0        # 150.796 rad/s
t_start = 4.0
alpha_m = w_target / t_start                 # 37.699 rad/s^2
phi_exact = 0.5 * alpha_m * t_start ** 2     # 301.593 rad
turns = phi_exact / (2.0 * np.pi)            # 48.0
dt = 1e-4
w, phi, t = 0.0, 0.0, 0.0
while t < t_start - 1e-12:
    w += alpha_m * dt
    phi += w * dt
    t += dt
print("[Exp 1] motor start (0 -> 1440 rpm in 4 s) & drum brake (5 s)")
print("  motor: alpha = %.3f rad/s^2, phi(4s) = %.3f rad = %.2f turns"
      % (alpha_m, phi_exact, turns))
print("  Euler (dt=%.0e): omega(4) = %.3f, phi(4) = %.3f rad  %s"
      % (dt, w, phi, "PASS" if (abs(w - w_target) < 0.01 and abs(phi - phi_exact) < 0.03) else "FAIL"))
n_drum = 57.6
w_drum = n_drum * 2.0 * np.pi / 60.0         # 6.032 rad/s
alpha_b = -w_drum / 5.0
phi_b = w_drum * 5.0 + 0.5 * alpha_b * 25.0  # 15.080 rad
rope = 0.2 * phi_b
print("  drum brake: alpha = %.3f rad/s^2, phi(5s) = %.3f rad = %.2f turns"
      % (alpha_b, phi_b, phi_b / (2.0 * np.pi)))
print("  rope payout = r*phi = %.3f m  %s"
      % (rope, "PASS" if abs(rope - 3.016) < 0.001 else "FAIL"))

# ---------- Exp 2: drive train arithmetic ----------
n1 = 1440.0
n2 = n1 * 17.0 / 85.0                        # 288 rpm
n3 = n2 * 17.0 / 85.0                        # 57.6 rpm
i_tot = (85.0 / 17.0) * (85.0 / 17.0)        # 25
w_d = n3 * 2.0 * np.pi / 60.0
v_rope = w_d * 0.2
print("[Exp 2] hoist drive train: 1440 rpm, gears 17/85 x 17/85, drum r=0.2")
print("  shaft II = %.1f rpm, shaft III = %.1f rpm, i_total = %.1f" % (n2, n3, i_tot))
print("  drum omega = %.3f rad/s, rope speed = %.4f m/s" % (w_d, v_rope))
ok2 = (abs(n2 - 288.0) < 1e-9 and abs(n3 - 57.6) < 1e-9
       and abs(i_tot - 25.0) < 1e-9 and abs(v_rope - 1.2064) < 1e-3)
print("  matches hand calculation: %s" % ("PASS" if ok2 else "FAIL"))

# ---------- Exp 3: cross-product vs geometric components ----------
max_v, max_dot, max_dd, max_at = 0.0, 0.0, 0.0, 0.0
cnt = 0
while cnt < N:
    u = rng.standard_normal(3)
    u = u / np.linalg.norm(u)
    wmag = rng.uniform(0.5, 5.0)
    amag = rng.uniform(-3.0, 3.0)
    r = rng.uniform(-2.0, 2.0, 3)
    r_perp = r - np.dot(r, u) * u
    if np.linalg.norm(r_perp) < 0.3:
        continue
    w_vec = wmag * u
    a_vec = amag * u
    v = np.cross(w_vec, r)
    max_v = max(max_v, abs(np.linalg.norm(v) - wmag * np.linalg.norm(r_perp)))
    max_dot = max(max_dot, abs(np.dot(v, u)))
    dd = np.cross(w_vec, np.cross(w_vec, r)) + wmag ** 2 * r_perp
    max_dd = max(max_dd, np.linalg.norm(dd))
    at = np.cross(a_vec, r)
    max_at = max(max_at, abs(np.linalg.norm(at) - abs(amag) * np.linalg.norm(r_perp)))
    cnt += 1
print("[Exp 3] cross-product vs geometric components, %d random axes" % N)
print("  max | |v| - omega*r_perp | = %.1e  %s" % (max_v, "PASS" if max_v < 1e-12 else "FAIL"))
print("  max | v . u | = %.1e  %s (velocity perpendicular to axis)"
      % (max_dot, "PASS" if max_dot < 1e-12 else "FAIL"))
print("  max | w x (w x r) + w^2 r_perp | = %.1e  %s" % (max_dd, "PASS" if max_dd < 1e-12 else "FAIL"))
print("  max | |alpha x r| - alpha*r_perp | = %.1e  %s" % (max_at, "PASS" if max_at < 1e-12 else "FAIL"))

# ---------- Exp 4: trajectory -> central-diff v vs analytic omega x r ----------
max_d4 = 0.0
cnt = 0
while cnt < N:
    cc = rng.uniform(-1.0, 1.0, 4)           # phi poly (deg 3)
    phi_c = np.array([cc[3], cc[2], cc[1], cc[0]])
    dphi = np.polyder(phi_c)
    ts = np.linspace(0.2, 0.4, 401)
    phis = np.polyval(phi_c, ts)
    r0 = rng.uniform(-2.0, 2.0, 2)
    rperp = np.linalg.norm(r0)
    if rperp < 0.3:
        continue
    phi0 = rng.uniform(0.0, 2.0 * np.pi)
    xs = rperp * np.cos(phis + phi0)
    ys = rperp * np.sin(phis + phi0)
    h4 = ts[1] - ts[0]
    vxs = (xs[2:] - xs[:-2]) / (2.0 * h4)
    vys = (ys[2:] - ys[:-2]) / (2.0 * h4)
    tm = 0.5 * (ts[2:] + ts[:-2])
    w_mid = np.polyval(dphi, tm)
    vx_a = -w_mid * ys[1:-1]                 # v = omega k x P
    vy_a = w_mid * xs[1:-1]
    d4 = max(np.max(np.abs(vxs - vx_a)), np.max(np.abs(vys - vy_a)))
    max_d4 = max(max_d4, d4)
    cnt += 1
print("[Exp 4] trajectory central-diff v vs analytic omega x r, %d random phi(t)" % N)
print("  max component diff = %.1e  %s" % (max_d4, "PASS" if max_d4 < 1e-3 else "FAIL"))

# ---------- Exp 5: translation copy vs rotation copy ----------
pa = rng.uniform(-1.0, 1.0, 3)
pb = rng.uniform(-1.0, 1.0, 3)
c_off = rng.uniform(-1.0, 1.0, 2)
ts5 = np.linspace(0.0, 1.0, 1001)
h5 = ts5[1] - ts5[0]
Ax = np.polyval(pa, ts5)
Ay = np.polyval(pb, ts5)
vAx = (Ax[2:] - Ax[:-2]) / (2.0 * h5)
vAy = (Ay[2:] - Ay[:-2]) / (2.0 * h5)
# translation copy B1 = A + c
B1x = Ax + c_off[0]
B1y = Ay + c_off[1]
vB1x = (B1x[2:] - B1x[:-2]) / (2.0 * h5)
vB1y = (B1y[2:] - B1y[:-2]) / (2.0 * h5)
diff_tr = max(np.max(np.abs(vB1x - vAx)), np.max(np.abs(vB1y - vAy)))
# rotation copy B2: theta = 1.5t + 0.4t^2, d = (0.3, 0.2)
th = 1.5 * ts5 + 0.4 * ts5 ** 2
om = 1.5 + 0.8 * ts5
d_vec = np.array([0.3, 0.2])
rperp5 = np.linalg.norm(d_vec)
B2x = d_vec[0] * np.cos(th) - d_vec[1] * np.sin(th)
B2y = d_vec[0] * np.sin(th) + d_vec[1] * np.cos(th)
vB2x = (B2x[2:] - B2x[:-2]) / (2.0 * h5)
vB2y = (B2y[2:] - B2y[:-2]) / (2.0 * h5)
om_mid = om[1:-1]
vx_ana = -om_mid * B2y[1:-1]
vy_ana = om_mid * B2x[1:-1]
diff_rot = max(np.max(np.abs(vB2x - vx_ana)), np.max(np.abs(vB2y - vy_ana)))
print("[Exp 5] translation copy vs rotation copy")
print("  translation copy r_A + c: max |v_B - v_A| = %.1e  %s (math-exact, float noise)"
      % (diff_tr, "PASS" if diff_tr < 1e-10 else "FAIL"))
print("  rotation copy (theta = 1.5t + 0.4t^2, d_perp = %.3f):" % rperp5)
print("    central-diff v vs analytic omega x r: max diff = %.1e  %s"
      % (diff_rot, "PASS" if diff_rot < 1e-6 else "FAIL"))
# last valid central diff lands at ts5[999] = 0.999 (not t=1.0) -- compare at that node
t_end = ts5[999]
v_B2_end = np.hypot(vB2x[-1], vB2y[-1])
w_end = om[999]
v_A_end = np.hypot(vAx[-1], vAy[-1])
ok5c = abs(v_B2_end - w_end * rperp5) < 5e-6
ok5d = abs(v_B2_end - v_A_end) > 0.01
print("    |v_B2(%.3f)| = %.3f vs omega(%.3f)*r_perp = %.3f  %s"
      % (t_end, v_B2_end, t_end, w_end * rperp5, "PASS" if ok5c else "FAIL"))
print("    v_B2(%.3f) = %.3f vs v_A(%.3f) = %.3f (differ: translation theorem does NOT apply) %s"
      % (t_end, v_B2_end, t_end, v_A_end, "PASS" if ok5d else "FAIL"))

# ---------- honest overall (collect every check) ----------
ok1a = abs(w - w_target) < 0.01 and abs(phi - phi_exact) < 0.03
ok1b = abs(rope - 3.016) < 0.001
ok3 = max_v < 1e-12 and max_dot < 1e-12 and max_dd < 1e-12 and max_at < 1e-12
ok4 = max_d4 < 1e-3
ok5 = diff_tr < 1e-10 and diff_rot < 1e-6 and ok5c and ok5d
flags = [ok1a, ok1b, ok2, ok3, ok4, ok5]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
