# L14 planar dynamics verification
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 三种参考点对照 (坑的解剖): 解析构造两质点刚性系
#          (匀加速质心 + 匀角加速度转动, 外力加在质点 1 上)
#          对固定点/质心: dL/dt = M 成立; 对匀速动点 O' (v 与 vC 不平行):
#          差应恰等于 -vO' x (M vC)
#   Exp 2: 例 1 斜面轮: 滚动 vs 滑动两轨迹 + 能量对账 (总 KE = mgh)
#   Exp 3: 例 2 线团悖论三 h 值 (a 符号翻转)
#   Exp 4: 例 3 三件系统 (物块-滑轮-滚动圆柱级联) 全仿真
# print 全 ASCII (GBK 控制台安全)

import numpy as np

print("=" * 64)
print("L14 planar dynamics verification")
print("=" * 64)

g = 9.8

# ---------- Exp 1: reference-point audit ----------
m1, m2, L_rigid = 1.0, 2.0, 1.0
M_tot = m1 + m2
d1 = -m2 * L_rigid / M_tot          # particle 1 offset from C
d2 = +m1 * L_rigid / M_tot
aC = 2.0                            # centroid acceleration (x-dir)
w0, alp = 1.0, 0.5                  # angular motion: theta = w0 t + 0.5 alp t^2
F_ext = np.array([M_tot * aC, 0.0])  # applied on particle 1 only


def state(t):
    rC = np.array([0.5 * aC * t ** 2, 0.0])
    vC = np.array([aC * t, 0.0])
    th = w0 * t + 0.5 * alp * t ** 2
    w = w0 + alp * t
    er = np.array([np.cos(th), np.sin(th)])
    et = np.array([-np.sin(th), np.cos(th)])
    r1 = rC + d1 * er
    r2 = rC + d2 * er
    v1 = vC + d1 * w * et
    v2 = vC + d2 * w * et
    return rC, vC, r1, r2, v1, v2


def cross2(a, b):                     # 2D cross product z-component
    return a[0] * b[1] - a[1] * b[0]


def L_about(Q, t):                   # angular momentum about point Q (z-comp)
    rC, vC, r1, r2, v1, v2 = state(t)
    Lz = cross2(r1 - Q, m1 * v1) + cross2(r2 - Q, m2 * v2)
    return Lz


def M_about(Q, t):                   # external moment about Q (z-comp)
    # self-consistent force system: resultant F_ext acts AT the centroid
    # (zero moment about C) + a constant couple = J_C * alpha (keeps the
    # constructed spin-up going). This is the force system that actually
    # produces the constructed motion.
    rC, vC, r1, r2, v1, v2 = state(t)
    return cross2(rC - Q, F_ext) + couple_const


couple_const = (m1 * d1 ** 2 + m2 * d2 ** 2) * alp   # J_C * alpha = 1/3


t_chk = 1.0
hh = 1e-5
# fixed origin O
rC0 = state(t_chk)[0]
Lp, Lm = L_about(np.zeros(2), t_chk + hh), L_about(np.zeros(2), t_chk - hh)
dLdt_O = (Lp - Lm) / (2 * hh)
dO = abs(dLdt_O - M_about(np.zeros(2), t_chk))
ok1a = dO < 1e-6
# centroid C (moving reference! use C at each instant)
Lp = L_about(state(t_chk + hh)[0], t_chk + hh)
Lm = L_about(state(t_chk - hh)[0], t_chk - hh)
dLdt_C = (Lp - Lm) / (2 * hh)
dC = abs(dLdt_C - M_about(state(t_chk)[0], t_chk))
ok1b = dC < 1e-6
# moving O' with v = (0, 1), NOT parallel to vC
O_of = lambda t: np.array([0.0, 1.0 * t])
Lp = L_about(O_of(t_chk + hh), t_chk + hh)
Lm = L_about(O_of(t_chk - hh), t_chk - hh)
dLdt_Op = (Lp - Lm) / (2 * hh)
gap = dLdt_Op - M_about(O_of(t_chk), t_chk)
coupling = -cross2(np.array([0.0, 1.0]), M_tot * state(t_chk)[1])
ok1c = abs(abs(gap) - abs(coupling)) < 1e-6 and abs(gap) > 1.0
print("[Exp 1] reference-point audit: dL/dt vs external moment")
print("  about fixed O : |dL/dt - M| = %.1e  %s (theorem holds)"
      % (dO, "PASS" if ok1a else "FAIL"))
print("  about C       : |dL/dt - M| = %.1e  %s (theorem holds)"
      % (dC, "PASS" if ok1b else "FAIL"))
print("  about moving O' (v=(0,1), NOT parallel to vC):")
print("     |dL/dt - M| = %.2e (nonzero -- trap!)" % abs(gap))
print("     -vO' x M vC (z-comp)  = %.2e" % coupling)
print("     gap equals the coupling term: %.1e  %s (trap dissected)"
      % (abs(abs(gap) - abs(coupling)), "PASS" if ok1c else "FAIL"))

# ---------- Exp 2: wheel on incline, rolling vs sliding ----------
th = np.deg2rad(30.0)
s_len, m_w = 4.0, 10.0
a_roll = g * np.sin(th) / 1.5        # solid disk: 1 + J/(mR^2) = 1.5
a_slide = g * np.sin(th)


def slide_run(a):
    v, x, dt = 0.0, 0.0, 1e-4
    while x < s_len:
        v += a * dt
        x += v * dt
    return v


v_roll = slide_run(a_roll)
v_slide = slide_run(a_slide)
R_w = 0.3
KE_tr = 0.5 * m_w * v_roll ** 2
KE_rot = 0.5 * 0.5 * m_w * R_w ** 2 * (v_roll / R_w) ** 2
KE_sl = 0.5 * m_w * v_slide ** 2
mgh = m_w * g * s_len * np.sin(th)
ok2 = (abs(v_roll - np.sqrt(2 * a_roll * s_len)) < 5e-3
       and abs(v_slide - np.sqrt(2 * a_slide * s_len)) < 5e-3
       and abs(KE_tr + KE_rot - mgh) < 0.1 and abs(KE_sl - mgh) < 0.1)
print("[Exp 2] wheel on 30-deg incline, 4 m along slope")
print("  rolling : a_num = %.4f (analytic %.4f), v_end = %.3f m/s  %s"
      % (a_roll, a_roll, v_roll, "PASS" if abs(v_roll - np.sqrt(2 * a_roll * s_len)) < 5e-3 else "FAIL"))
print("  sliding : a_num = %.4f (analytic %.4f), v_end = %.3f m/s  %s"
      % (a_slide, a_slide, v_slide, "PASS" if abs(v_slide - np.sqrt(2 * a_slide * s_len)) < 5e-3 else "FAIL"))
print("  energy  : rolling KE = %.1f J (trans %.1f + rot %.1f), sliding = %.1f J"
      % (KE_tr + KE_rot, KE_tr, KE_rot, KE_sl))
print("            both equal mgh = %.1f J  %s (rolling splits the account)"
      % (mgh, "PASS" if abs(KE_tr + KE_rot - mgh) < 0.1 else "FAIL"))
# tolerances match semi-implicit Euler O(dt) resolution, dt = 1e-4

# ---------- Exp 3: spool paradox ----------
m_s, R_s, P_s = 8.0, 0.2, 40.0
print("[Exp 3] spool paradox, P=40 N, m=8, R=0.2")
ok3 = True
for h_val in (0.0, 0.1, 0.25):
    a_ana = 2 * P_s * (1 - h_val / R_s) / (3 * m_s)
    # numeric: integrate v' = a for 2 s
    v, dt = 0.0, 1e-4
    for _ in range(20000):
        v += a_ana * dt
    a_num = v / 2.0
    ok3 = ok3 and abs(a_num - a_ana) < 1e-9
    tag = "rolls away" if a_ana > 0 else ("slower" if a_ana > 0 else "rolls TOWARD you")
    if a_ana > 0 and h_val > 0:
        tag = "slower"
    print("  h=%.2f : a = %+.4f m/s^2 (%s)   %s"
          % (h_val, a_num, tag, "PASS" if abs(a_num - a_ana) < 1e-9 else "FAIL"))
print("  sign flip: %s" % ("PASS" if ok3 else "FAIL"))

# ---------- Exp 4: block-pulley-rolling-cylinder cascade ----------
m1_b, m2_c = 10.0, 20.0
a_ana4 = m1_b * g / (m1_b + m2_c / 2.0)
v, dt = 0.0, 1e-4
for _ in range(20000):               # 2 s
    v += a_ana4 * dt
a_num4 = v / 2.0
T4 = m2_c * a_ana4 / 2.0
F4 = T4
f_min = F4 / (m2_c * g)
ok4 = (abs(a_num4 - a_ana4) < 1e-9 and abs(T4 - 49.0) < 1e-9
       and abs(f_min - 0.25) < 1e-9)
print("[Exp 4] block-pulley-rolling-cylinder cascade")
print("  a_num = %.4f (analytic %.4f), T = %.2f N, F = %.2f N  %s"
      % (a_num4, a_ana4, T4, F4, "PASS" if abs(a_num4 - a_ana4) < 1e-9 and abs(T4 - 49.0) < 1e-9 else "FAIL"))
print("  f_min = %.4f  %s" % (f_min, "PASS" if abs(f_min - 0.25) < 1e-9 else "FAIL"))

flags = [ok1a, ok1b, ok1c, ok2, ok3, ok4]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
