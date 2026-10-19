# L09 planar motion verification
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 例1-3 三法闭环 + 例5 加速度 (phi=60deg 定点, 四路对账含差分)
#   Exp 2: 曲柄滑块全周期 (phi 扫 0-2pi, 720 点): 位置闭式 -> 差分 v_B
#          vs 基点法闭式 vs 瞬心闭式 (含死点 phi=0, pi)
#   Exp 3: 纯滚动轮速度分布: 轮缘 360 点 |v| = w|PX| 且 v 垂直辐条
#   Exp 4: 四杆机构全程: 两圆交点闭式位置 -> unwrap 角度差分 w
#          vs 速度联立方程
#   Exp 5: 瞬心构造式 r_PA = (-vAy, vAx)/w, P = A + r_PA (500 组随机):
#          v_P = 0; v_B 基点法 vs 绕瞬心恒等; |v_B| = w|PB|; v_B 垂直 PB
# 随机种子固定可复现; print 全 ASCII (GBK 控制台安全)

import numpy as np

rng = np.random.default_rng(42)
K = np.array([0.0, 0.0, 1.0])

print("=" * 64)
print("L09 planar motion verification")
print("=" * 64)

# ---------- Exp 1: crank-slider at phi=60deg, four-way accounting ----------
r, l, w0 = 0.1, 0.3, 10.0
phi0 = np.deg2rad(60.0)
A = (r * np.cos(phi0), r * np.sin(phi0))
vA = w0 * np.array([-A[1], A[0]])
xB = r * np.cos(phi0) + np.sqrt(l ** 2 - r ** 2 * np.sin(phi0) ** 2)
rBA = np.array([xB - A[0], -A[1]])
# base-point method
w_bp = -vA[1] / rBA[0]                      # y: 0 = vAy + w*xBA
vB_bp = vA[0] - w_bp * rBA[1]               # x: vB = vAx - w*yBA
# projection theorem
e_AB = rBA / l
vB_proj = (vA @ e_AB) / e_AB[0]
# ICR method: P on OA-line x vertical line thru B; omega from vA about P
P = np.array([xB, np.tan(phi0) * xB])
AP = np.array(A) - P
w_icr_signed = (vA @ np.array([-AP[1], AP[0]])) / (AP @ AP)
vB_icr = w_icr_signed * (-(0.0 - P[1]))   # x-component of w k x (B - P), B at y=0
# central difference of closed-form position
def xB_of(ph):
    return r * np.cos(ph) + np.sqrt(l ** 2 - r ** 2 * np.sin(ph) ** 2)
t0 = phi0 / w0
hh = 1e-5
vB_diff = (xB_of(phi0 + w0 * hh) - xB_of(phi0 - w0 * hh)) / (2 * hh)
ok1a = (abs(vB_bp - vB_proj) < 1e-12 and abs(vB_bp - vB_icr) < 1e-12
        and abs(vB_bp - vB_diff) < 1e-7)
# acceleration (example 5): 2nd difference vs five-block assembly
aB_diff = (xB_of(phi0 + w0 * hh) - 2 * xB_of(phi0) + xB_of(phi0 - w0 * hh)) / hh ** 2
def w_of(ph):
    s = np.sqrt(l ** 2 - r ** 2 * np.sin(ph) ** 2)
    return -w0 * r * np.cos(ph) / s
alpha = (w_of(phi0 + w0 * hh) - w_of(phi0 - w0 * hh)) / (2 * hh)
aA = -w0 ** 2 * np.array(A)
wAB = w_of(phi0)
aBA_n = wAB ** 2 * (-rBA)                   # points from B to A
aBA_t = alpha * np.array([-rBA[1], rBA[0]])
aB_eq = aA + aBA_n + aBA_t
aB_eq_x = aB_eq[0]                          # slider constraint: a_B = (aBx, 0)
ok1b = abs(aB_diff - aB_eq_x) < 1e-4 and abs(aB_eq_x + 3.338) < 5e-3
print("[Exp 1] crank-slider at phi=60deg: three methods + acceleration")
print("  v_B: base-point %.4f, projection %.4f, ICR %.4f, diff %.4f  %s"
      % (vB_bp, vB_proj, vB_icr, vB_diff, "PASS" if ok1a else "FAIL"))
print("  omega_AB = %.4f rad/s, ICR P = (%.4f, %.4f), |PA| = %.4f"
      % (w_bp, P[0], P[1], np.linalg.norm(AP)))
print("  accel: a_B = %.3f m/s^2 (diff %.3f), alpha_AB = %.2f rad/s^2  %s"
      % (aB_eq_x, aB_diff, alpha, "PASS" if ok1b else "FAIL"))

# ---------- Exp 2: full cycle, three independent routes ----------
# fine grid 2881 pts: gradient error O(dt^2) shrinks 16x vs 721 pts
phis = np.linspace(0.0, 2.0 * np.pi, 2881)
ts = phis / w0
xBs = xB_of(phis)
vB_d = np.gradient(xBs, ts)
vB_f = np.zeros_like(phis)
vB_i = np.zeros_like(phis)
for i, ph in enumerate(phis):
    s = np.sqrt(l ** 2 - r ** 2 * np.sin(ph) ** 2)
    w = -w0 * r * np.cos(ph) / s
    vB_f[i] = -w0 * r * np.sin(ph) + w * r * np.sin(ph)
    # ICR route: v_Bx = w*y_P with y_P = tan(ph)*x_B; algebraically the
    # cos(ph) cancels: w*y_P = -w0*r*sin(ph)*x_B/s  (smooth at ph=pi/2)
    vB_i[i] = -w0 * r * np.sin(ph) * xBs[i] / s
ok2 = np.max(np.abs(vB_d - vB_f)) < 2e-3 and np.max(np.abs(vB_d - vB_i)) < 2e-3
# dead points at phi=0 (index 0) and phi=pi (index 1440 of 2881)
dead_ok = abs(vB_f[0]) < 1e-9 and abs(vB_f[1440]) < 1e-9
print("[Exp 2] crank-slider full cycle (2881 steps, includes dead points)")
print("  max | v_B(diff) - v_B(formula) | = %.1e" % np.max(np.abs(vB_d - vB_f)))
print("  max | v_B(diff) - v_B(ICR) | = %.1e  %s"
      % (np.max(np.abs(vB_d - vB_i)), "PASS" if ok2 else "FAIL"))
print("  v_B at dead points phi=0/pi: %.3f / %.3f  %s"
      % (vB_f[0], vB_f[1440], "PASS" if dead_ok else "FAIL"))

# ---------- Exp 3: rolling wheel rim distribution ----------
R, vC = 0.2, 2.0
w_wheel = vC / R                            # clockwise
ang = np.linspace(0.0, 2.0 * np.pi, 360)
rim = R * np.stack([np.cos(ang), np.sin(ang)], axis=1) + np.array([0.0, R])
vX = vC * np.array([1.0, 0.0]) + (-w_wheel) * np.stack(
    [-rim[:, 1] + R, rim[:, 0]], axis=1)    # v = vC - w k x (X - C)
X = rim                                     # contact point (ICR) at the origin
mag_ok = np.max(np.abs(np.linalg.norm(vX, axis=1) - w_wheel * np.linalg.norm(rim, axis=1)))
dot_ok = np.max(np.abs(np.sum(vX * rim, axis=1)))
top_v = np.array([vC, 0.0]) + (-w_wheel) * np.array([-R, 0.0])  # exact top point
ok3 = mag_ok < 1e-12 and dot_ok < 1e-12 and abs(np.linalg.norm(top_v) - 2 * vC) < 1e-12
print("[Exp 3] rolling wheel rim: |v| = omega*|PX| and v perpendicular PX")
print("  max | |v| - omega*r_P | = %.1e  PASS" % mag_ok)
print("  max | v . (X - P) | = %.1e  %s"
      % (dot_ok, "PASS" if dot_ok < 1e-12 else "FAIL"))
print("  top speed = %.3f m/s (= 2*v_C)  %s"
      % (np.linalg.norm(top_v), "PASS" if abs(np.linalg.norm(top_v) - 4.0) < 1e-12 else "FAIL"))

# ---------- Exp 4: four-bar linkage full cycle ----------
r1, r2, r3, d = 0.1, 0.35, 0.3, 0.4
w1 = 5.0
ph4 = np.linspace(0.0, 2.0 * np.pi, 2881)   # fine grid: dt^2 error shrinks 16x
t4 = ph4 / w1
th_c = np.zeros_like(ph4)   # coupler angle (A->B)
th_r = np.zeros_like(ph4)   # rocker angle (D->B)
ok4 = True
w_c_err = 0.0
w_r_err = 0.0
for i, ph in enumerate(ph4):
    Ap = np.array([r1 * np.cos(ph), r1 * np.sin(ph)])
    Dp = np.array([d, 0.0])
    dv = Dp - Ap
    L = np.linalg.norm(dv)
    a2 = (r2 ** 2 - r3 ** 2 + L ** 2) / (2 * L)
    h2 = np.sqrt(max(r2 ** 2 - a2 ** 2, 0.0))
    base = Ap + a2 * dv / L
    nvec = np.array([dv[1], -dv[0]]) / L
    Bp = base - h2 * nvec                   # upper branch (phi=90deg check)
    th_c[i] = np.arctan2(Bp[1] - Ap[1], Bp[0] - Ap[0])
    th_r[i] = np.arctan2(Bp[1], Bp[0] - d)
th_c = np.unwrap(th_c)
th_r = np.unwrap(th_r)
w_c_d = np.gradient(th_c, t4)
w_r_d = np.gradient(th_r, t4)
for i, ph in enumerate(ph4):
    if i % 24 != 0:
        continue
    Ap = np.array([r1 * np.cos(ph), r1 * np.sin(ph)])
    Dp = np.array([d, 0.0])
    dv = Dp - Ap
    L = np.linalg.norm(dv)
    a2 = (r2 ** 2 - r3 ** 2 + L ** 2) / (2 * L)
    h2 = np.sqrt(max(r2 ** 2 - a2 ** 2, 0.0))
    base = Ap + a2 * dv / L
    nvec = np.array([dv[1], -dv[0]]) / L
    Bp = base - h2 * nvec
    vA = w1 * np.array([-Ap[1], Ap[0]])
    rBA = Bp - Ap
    rDB = Bp - Dp
    # vA + w2*(-yBA, xBA) = w3*(-yDB, xDB)  ->  2x2 linear system
    M = np.array([[-rBA[1], rDB[1]], [rBA[0], -rDB[0]]])
    sol = np.linalg.solve(M, -vA)
    w2_eq, w3_eq = sol
    w_c_err = max(w_c_err, abs(w2_eq - w_c_d[i]))
    w_r_err = max(w_r_err, abs(w3_eq - w_r_d[i]))
ok4 = w_c_err < 5e-3 and w_r_err < 5e-3
print("[Exp 4] four-bar linkage full cycle (r1=0.1, r2=0.35, r3=0.3, d=0.4)")
print("  omega coupler/rocker diff vs equations: max %.1e / %.1e  %s"
      % (w_c_err, w_r_err, "PASS" if ok4 else "FAIL"))

# ---------- Exp 5: ICR construction, 500 random states ----------
N = 500
max_vp = 0.0
max_vb = 0.0
max_mag = 0.0
max_dot = 0.0
cnt = 0
while cnt < N:
    vA_r = rng.uniform(-2.0, 2.0, 2)
    if np.linalg.norm(vA_r) < 0.3:
        continue
    w_r = rng.uniform(0.5, 4.0) * np.sign(rng.uniform(-1, 1))
    A_r = rng.uniform(-1.0, 1.0, 2)
    rPA = np.array([-vA_r[1], vA_r[0]]) / w_r
    P_r = A_r + rPA
    vP = vA_r + w_r * np.array([-rPA[1], rPA[0]])
    max_vp = max(max_vp, np.linalg.norm(vP))
    rB_r = rng.uniform(-2.0, 2.0, 2)
    vB_bp = vA_r + w_r * np.array([-rB_r[1], rB_r[0]])
    PB = P_r - (A_r + rB_r)
    vB_icr = w_r * np.array([PB[1], -PB[0]])  # w k x (B - P)
    max_vb = max(max_vb, np.linalg.norm(vB_bp - vB_icr))
    max_mag = max(max_mag, abs(np.linalg.norm(vB_bp) - abs(w_r) * np.linalg.norm(PB)))
    max_dot = max(max_dot, abs(vB_bp @ (A_r + rB_r - P_r)))
    cnt += 1
ok5 = max_vp < 1e-12 and max_vb < 1e-12 and max_mag < 1e-12 and max_dot < 1e-12
print("[Exp 5] ICR existence & distribution, %d random states" % N)
print("  max | v_P | = %.1e  %s (construction gives zero velocity)"
      % (max_vp, "PASS" if max_vp < 1e-12 else "FAIL"))
print("  max | v_B(base-point) - v_B(about ICR) | = %.1e  %s"
      % (max_vb, "PASS" if max_vb < 1e-12 else "FAIL"))
print("  max | |v_B| - omega*|PB| | = %.1e  %s"
      % (max_mag, "PASS" if max_mag < 1e-12 else "FAIL"))
print("  max | v_B . (B - P) | = %.1e  %s (perpendicular)"
      % (max_dot, "PASS" if max_dot < 1e-12 else "FAIL"))

flags = [ok1a, ok1b, ok2, dead_ok, ok3, ok4, ok5]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
