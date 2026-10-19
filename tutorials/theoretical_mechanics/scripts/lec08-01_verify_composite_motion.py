# L08 composite motion verification
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 速度合成 v_a = v_e + v_r (转动动系), 500 组随机 theta(t), rho(t)
#   Exp 2: 加速度合成 a_a = a_e + a_r + a_c (含科氏);
#          反面对照: 去掉 a_c 后的差恰为 a_c (该项必要且不多不少)
#   Exp 3: 平移动系: a_a = a_e + a_r, a_c 公式自动为零 (omega = 0)
#   Exp 4: 阿基米德螺线: 匀转 + 匀速径向滑的绝对轨迹 r = r0 + (v_r/w)*theta
#   Exp 5: 讲义例 4 复算: w=2, v_r=0.5, r=0.3 -> v_a=0.781, a_c=2.0, a_a=2.332
# 数值策略: 由轨迹 r(t) = R(theta(t)) rho(t) 出发, 中心差分得 "真实" v_a/a_a,
#           与合成公式 (v_e, v_r, a_e, a_r, a_c) 各算各的两路对账.
# 随机种子固定可复现; print 全 ASCII (GBK 控制台安全)

import numpy as np

rng = np.random.default_rng(42)
N = 500
J = np.array([[0.0, -1.0], [1.0, 0.0]])   # 90-degree rotation matrix


def Rmat(th):
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s], [s, c]])


print("=" * 64)
print("L08 composite motion verification")
print("=" * 64)

# ---------- Exp 1 & 2: rotating frame, velocity & acceleration composition ----------
h = 1e-5
max_dv = 0.0
max_da = 0.0
max_gap = 0.0          # counter-test gap |a_a - (a_e + a_r)|
max_gap_is_ac = 0.0    # | gap - a_c |  (should be ~ diff accuracy)
cnt = 0
while cnt < N:
    th_c = rng.uniform(-1.0, 1.0, 3)        # theta(t) poly deg 2
    rho_x = rng.uniform(-2.0, 2.0, 4)       # rho(t) comps deg 3
    rho_y = rng.uniform(-2.0, 2.0, 4)
    dth = np.polyder(th_c)
    ddth = np.polyder(th_c, 2)
    drx, dry = np.polyder(rho_x), np.polyder(rho_y)
    ddrx, ddry = np.polyder(rho_x, 2), np.polyder(rho_y, 2)
    t0 = 0.3
    th0 = np.polyval(th_c, t0)
    w0 = np.polyval(dth, t0)
    al0 = np.polyval(ddth, t0)
    rho0 = np.array([np.polyval(rho_x, t0), np.polyval(rho_y, t0)])
    drho0 = np.array([np.polyval(drx, t0), np.polyval(dry, t0)])
    ddrho0 = np.array([np.polyval(ddrx, t0), np.polyval(ddry, t0)])
    if np.linalg.norm(rho0) < 0.1 or np.linalg.norm(drho0) < 0.05:
        continue

    def pos(t):
        rr = np.array([np.polyval(rho_x, t), np.polyval(rho_y, t)])
        return Rmat(np.polyval(th_c, t)) @ rr

    v_a = (pos(t0 + h) - pos(t0 - h)) / (2.0 * h)
    a_a = (pos(t0 + h) - 2.0 * pos(t0) + pos(t0 - h)) / h ** 2
    # composition formulas (all expressed in world frame)
    v_e = Rmat(th0) @ (w0 * (J @ rho0))
    v_r = Rmat(th0) @ drho0
    a_e = Rmat(th0) @ (al0 * (J @ rho0) - w0 ** 2 * rho0)
    a_r = Rmat(th0) @ ddrho0
    a_c = 2.0 * Rmat(th0) @ (w0 * (J @ drho0))
    max_dv = max(max_dv, np.linalg.norm(v_a - (v_e + v_r)))
    max_da = max(max_da, np.linalg.norm(a_a - (a_e + a_r + a_c)))
    gap = a_a - (a_e + a_r)
    max_gap = max(max_gap, np.linalg.norm(gap))
    max_gap_is_ac = max(max_gap_is_ac, np.linalg.norm(gap - a_c))
    cnt += 1

ok1 = max_dv < 1e-5
ok2 = max_da < 1e-3
ok2b = max_gap_is_ac < 1e-3
print("[Exp 1] velocity composition, %d random rotating frames" % N)
print("  max | v_a(diff) - (v_e + v_r) | = %.1e  %s" % (max_dv, "PASS" if ok1 else "FAIL"))
print("[Exp 2] acceleration composition, %d random rotating frames" % N)
print("  max | a_a(diff) - (a_e + a_r + a_c) | = %.1e  %s" % (max_da, "PASS" if ok2 else "FAIL"))
print("  counter-test (without a_c): max | a_a - (a_e + a_r) | = %.3f" % max_gap)
print("  max | missing term - a_c | = %.1e  %s (the gap IS a_c)"
      % (max_gap_is_ac, "PASS" if ok2b else "FAIL"))

# ---------- Exp 3: translating frame ----------
max_dv3 = 0.0
max_da3 = 0.0
cnt = 0
while cnt < N:
    cx = rng.uniform(-1.0, 1.0, 4)
    cy = rng.uniform(-1.0, 1.0, 4)
    px = rng.uniform(-2.0, 2.0, 4)
    py = rng.uniform(-2.0, 2.0, 4)
    t0 = 0.3

    def pos3(t):
        return np.array([np.polyval(cx, t) + np.polyval(px, t),
                         np.polyval(cy, t) + np.polyval(py, t)])

    v_a = (pos3(t0 + h) - pos3(t0 - h)) / (2.0 * h)
    a_a = (pos3(t0 + h) - 2.0 * pos3(t0) + pos3(t0 - h)) / h ** 2
    v_e = np.array([np.polyval(np.polyder(cx), t0), np.polyval(np.polyder(cy), t0)])
    v_r = np.array([np.polyval(np.polyder(px), t0), np.polyval(np.polyder(py), t0)])
    a_e = np.array([np.polyval(np.polyder(cx, 2), t0), np.polyval(np.polyder(cy, 2), t0)])
    a_r = np.array([np.polyval(np.polyder(px, 2), t0), np.polyval(np.polyder(py, 2), t0)])
    # omega = 0 for a translating frame: a_c = 2*omega x v_r is identically zero
    max_dv3 = max(max_dv3, np.linalg.norm(v_a - (v_e + v_r)))
    max_da3 = max(max_da3, np.linalg.norm(a_a - (a_e + a_r)))
    cnt += 1

# tolerance matches the 3-point 2nd-difference accuracy O(h^2) ~ 1e-5 (same as Exp 2)
ok3 = max_dv3 < 1e-6 and max_da3 < 1e-3
print("[Exp 3] translating frame, %d random cases" % N)
print("  max | v_a - (v_e + v_r) | = %.1e; max | a_a - (a_e + a_r) | = %.1e  %s (no Coriolis term)"
      % (max_dv3, max_da3, "PASS" if ok3 else "FAIL"))

# ---------- Exp 4: Archimedes spiral ----------
w, vr, r0 = 2.0, 0.5, 0.25
ts = np.linspace(0.0, 2.0 * np.pi, 721)
th = w * ts
r = r0 + vr * ts
pts_x = r * np.cos(th)
pts_y = r * np.sin(th)
r_num = np.hypot(pts_x, pts_y)
r_ana = r0 + (vr / w) * th
max_d4 = np.max(np.abs(r_num - r_ana))
ok4 = max_d4 < 1e-12
print("[Exp 4] Archimedes spiral: drum w=2 rad/s, v_r=0.5 m/s, r0=0.25")
print("  max | r_numeric(theta) - (r0 + v_r/w*theta) | = %.1e  %s"
      % (max_d4, "PASS" if ok4 else "FAIL"))

# ---------- Exp 5: textbook example 4 replay ----------
w5, vr5, r0_5, r_hit = 2.0, 0.5, 0.25, 0.30
t_hit = (r_hit - r0_5) / vr5


def pos5(t):
    rr = r0_5 + vr5 * t
    thh = w5 * t
    return np.array([rr * np.cos(thh), rr * np.sin(thh)])


v5 = (pos5(t_hit + h) - pos5(t_hit - h)) / (2.0 * h)
a5 = (pos5(t_hit + h) - 2.0 * pos5(t_hit) + pos5(t_hit - h)) / h ** 2
th5 = w5 * t_hit
er = np.array([np.cos(th5), np.sin(th5)])
et = np.array([-np.sin(th5), np.cos(th5)])
v_a_card = np.linalg.norm(v5)
a_a_card = np.linalg.norm(a5)
a_c_formula = 2.0 * w5 * vr5
ok5 = (abs(v_a_card - 0.781) < 1e-3 and abs(a_c_formula - 2.0) < 1e-9
       and abs(a_a_card - 2.332) < 1e-2
       and abs(v5 @ er - 0.5) < 1e-4 and abs(v5 @ et - 0.6) < 1e-4
       and abs(a5 @ er + 1.2) < 1e-3 and abs(a5 @ et - 2.0) < 1e-3)
print("[Exp 5] turntable slider replay (w=2, v_r=0.5, r=0.3)")
print("  v_a: diff %.4f vs formula %.4f  %s" % (v_a_card, np.hypot(0.5, 0.6), "PASS" if abs(v_a_card - 0.781) < 1e-3 else "FAIL"))
print("  a_c = 2.0 (formula 2.000, radial/tangential split: %.3f / %.3f)"
      % (abs(a5 @ er), a5 @ et))
print("  a_a: diff %.3f vs formula %.3f  %s (hand card 2.33)"
      % (a_a_card, np.hypot(1.2, 2.0), "PASS" if abs(a_a_card - 2.332) < 1e-2 else "FAIL"))

flags = [ok1, ok2, ok2b, ok3, ok4, ok5]
print("OVERALL: %s" % ("ALL PASS" if all(flags) else "FAILURES PRESENT: %d/%d checks failed"
                       % (flags.count(False), len(flags))))
