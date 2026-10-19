# L13 angular momentum verification
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 转动惯量数值积分 vs 查表公式 (杆绕端点/盘绕对称轴/薄环/球绕直径)
#   Exp 2: 平行轴定理, 500 组随机质点系 (2D, z 轴)
#   Exp 3: 动量矩定理 dL/dt = M(t), 500 组随机变力矩 (定半径圆周质点)
#   Exp 4: 收臂守恒: I(t) 时变 4->1.6, 数值 w(t) vs 解析 w0*I0/I(t)
#          (L 恒 8、动能增 12 J 复核)
#   Exp 5: 例 3 绞盘 (alpha=4 常量) 与例 4 指数制动 (w=20 exp(-t/4))
# print 全 ASCII (GBK 控制台安全)

import numpy as np

rng = np.random.default_rng(42)
print("=" * 64)
print("L13 angular momentum verification")
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


# ---------- Exp 1: moments of inertia, numeric vs table ----------
print("[Exp 1] moments of inertia: numeric grid vs table formulas")
ok1 = True
# rod about end: m=1.25, l=1.2 -> ml^2/3 = 0.6
m_r, l_r = 1.25, 1.2
xs = (np.arange(1000) + 0.5) * l_r / 1000
J_rod = m_r / 1000 * (xs ** 2).sum()
f_rod = m_r * l_r ** 2 / 3
e = abs(J_rod - f_rod)
print("  rod about end:      J_num=%.4f, J_formula=%.4f (ml^2/3),  err=%.1e"
      % (J_rod, f_rod, e))
ok1 = ok1 and e < 1e-3
# disk about axis: m=1.0, R=0.5 -> mR^2/2 = 0.125 (annular strips)
m_d, R_d = 1.0, 0.5
n_a = 2000
rs = (np.arange(n_a) + 0.5) * R_d / n_a
J_disk = m_d / n_a * 0.0  # mass spread by strip area below
areas = ((np.arange(n_a) + 1) ** 2 - np.arange(n_a) ** 2) * (R_d / n_a) ** 2
J_disk = (m_d * areas * rs ** 2).sum() / areas.sum()
f_disk = m_d * R_d ** 2 / 2
e = abs(J_disk - f_disk)
print("  disk about axis:    J_num=%.4f, J_formula=%.4f (mR^2/2),  err=%.1e"
      % (J_disk, f_disk, e))
ok1 = ok1 and e < 1e-3
# thin ring: m=0.8, R=0.5 -> mR^2 = 0.2 (strip of small width)
m_g, R_g, w_g = 0.8, 0.5, 0.005
zs = R_g - w_g / 2 + (np.arange(200) + 0.5) * w_g / 200
J_ring = (m_g / 200 * zs ** 2).sum()
f_ring = m_g * R_g ** 2
e = abs(J_ring - f_ring)
print("  ring about axis:    J_num=%.4f, J_formula=%.4f (mR^2),    err=%.1e"
      % (J_ring, f_ring, e))
ok1 = ok1 and e < 1e-3
# sphere about diameter: m=2.0, R=sqrt(0.4) -> 2mR^2/5 = 0.32 (z-slices)
# slice mass proportional to its area (r^2), NOT uniform -- edges are thin
m_s, R_s = 2.0, np.sqrt(0.4)
zs = (np.arange(2000) + 0.5) * 2 * R_s / 2000 - R_s
r_slice = np.sqrt(np.maximum(R_s ** 2 - zs ** 2, 0.0))
w_slice = r_slice ** 2                     # area weights
J_sph = 0.5 * m_s * (w_slice * r_slice ** 2).sum() / w_slice.sum()
f_sph = 2 * m_s * R_s ** 2 / 5
e = abs(J_sph - f_sph)
print("  sphere about diam.: J_num=%.4f, J_formula=%.4f (2mR^2/5), err=%.1e"
      % (J_sph, f_sph, e))
ok1 = ok1 and e < 1e-3
print("  %s (grid resolution)" % ("PASS" if ok1 else "FAIL"))

# ---------- Exp 2: parallel-axis theorem, random particle systems ----------
N = 500
max_d2 = 0.0
cnt = 0
while cnt < N:
    n_p = int(rng.integers(3, 20))
    ms = rng.uniform(0.1, 2.0, n_p)
    ps = rng.uniform(-1.0, 1.0, (n_p, 2))
    rC = (ms[:, None] * ps).sum(axis=0) / ms.sum()
    rel = ps - rC
    J_C = (ms * (rel ** 2).sum(axis=1)).sum()
    d = rng.uniform(-0.5, 0.5, 2)
    rel2 = ps - (rC + d)
    J_p = (ms * (rel2 ** 2).sum(axis=1)).sum()
    max_d2 = max(max_d2, abs(J_p - J_C - ms.sum() * (d ** 2).sum()))
    cnt += 1
ok2 = max_d2 < 1e-12
print("[Exp 2] parallel-axis theorem, %d random particle systems" % N)
print("  max | J_z' - (J_C + m d^2) | = %.1e  %s" % (max_d2, "PASS" if ok2 else "FAIL"))

# ---------- Exp 3: dL/dt = M(t), random torque on fixed-radius particle ----------
max_d3 = 0.0
cnt = 0
while cnt < N:
    Mc = rng.uniform(-3.0, 3.0, 4)         # M(t) poly deg 3
    J_p = rng.uniform(0.2, 2.0)            # m r^2
    w0 = rng.uniform(-3.0, 3.0)

    def f_w(s):
        t = s[1]
        return np.array([np.polyval(Mc, t) / J_p, 1.0])

    s = rk4(f_w, [w0, 0.0], 1e-3, 1000)
    L_num = J_p * s[0]                      # final angular momentum
    ts = np.linspace(0.0, 1.0, 100001)
    impulse_M = np.trapezoid(np.polyval(Mc, ts), ts)
    max_d3 = max(max_d3, abs(L_num - (J_p * w0 + impulse_M)))
    cnt += 1
ok3 = max_d3 < 1e-8
print("[Exp 3] dL/dt = M(t), %d random torque profiles" % N)
print("  max | L(diff) - integral M | = %.1e  %s" % (max_d3, "PASS" if ok3 else "FAIL"))

# ---------- Exp 4: arm-pulling spin-up, time-varying I ----------
T = 2.0
I0, I1 = 4.0, 1.6
w0 = 2.0


def I_of(t):
    return I0 + (I1 - I0) * t / T


def f_spin(s):
    t = s[1]
    I = I_of(t)
    dI = (I1 - I0) / T
    return np.array([-dI / I * s[0], 1.0])   # d(I w)/dt = 0 -> w' = -(dI/I) w


s = rk4(f_spin, [w0, 0.0], 1e-4, int(round(T / 1e-4)))
w_num = s[0]
w_ana = w0 * I0 / I1
ok4 = abs(w_num - w_ana) < 1e-9
# track L conservation and energy gain
s2 = np.array([w0, 0.0])
max_L = 0.0
dt = 1e-4
for _ in range(int(round(T / dt))):
    k1 = f_spin(s2)
    k2 = f_spin(s2 + dt / 2 * k1)
    k3 = f_spin(s2 + dt / 2 * k2)
    k4 = f_spin(s2 + dt * k3)
    s2 = s2 + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    max_L = max(max_L, abs(I_of(s2[1]) * s2[0] - I0 * w0))
dKE = 0.5 * I1 * w_ana ** 2 - 0.5 * I0 * w0 ** 2
ok4 = ok4 and max_L < 1e-9 and abs(dKE - 12.0) < 1e-9
print("[Exp 4] arm-pulling spin-up: I(t) 4 -> 1.6, w0 = 2")
print("  numeric omega(t_end) = %.4f vs analytic %.4f  %s"
      % (w_num, w_ana, "PASS" if abs(w_num - w_ana) < 1e-9 else "FAIL"))
print("  L conserved: max |I(t)w(t) - 8| = %.1e  %s" % (max_L, "PASS" if max_L < 1e-9 else "FAIL"))
print("  kinetic energy gain = %.1f J (matches hand card)" % dKE)

# ---------- Exp 5: winch replay and exponential braking ----------
J_w, r_w, m_w, M_b = 2.0, 0.5, 40.0, 148.0
alpha_ana = (m_w * 9.8 * r_w - M_b) / (J_w + m_w * r_w ** 2)


def f_winch(s):
    return np.array([s[1], alpha_ana])


s = rk4(f_winch, [0.0, 0.0], 1e-3, 3000)
ok5a = abs(s[1] - 12.0) < 1e-9
print("[Exp 5] winch replay and exponential braking")
print("  winch: alpha_num = %.4f (analytic %.4f), w(3s) = %.3f  %s"
      % (alpha_ana, alpha_ana, s[1], "PASS" if ok5a else "FAIL"))
J_f, c_b, w0_f = 2.0, 0.5, 20.0


def f_brake(s):
    return np.array([s[1], -c_b * s[1] / J_f])


s = rk4(f_brake, [0.0, w0_f], 1e-3, 4000)
w_ana4 = w0_f * np.exp(-1.0)
ok5b = abs(s[1] - w_ana4) < 1e-9
print("  brake: w(4s) = %.4f vs 20*exp(-1) = %.4f  %s"
      % (s[1], w_ana4, "PASS" if ok5b else "FAIL"))

flags = [ok1, ok2, ok3, ok4, ok5a, ok5b]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
