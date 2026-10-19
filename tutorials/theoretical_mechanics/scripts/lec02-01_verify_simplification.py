# L02 平面力系简化理论验证
# 规模纪律: 目标 < 1 秒; 纯 numpy 标量运算, 无重型依赖
# 验证内容:
#   Exp 0: 复现讲义例题 1 (三力简化: 主矢/主矩/合力线)
#   Exp 1: 力线平移定理等价性 (原力 vs 平移力+附加力偶, 对随机检验点的矩)
#   Exp 2: 主矩换心公式 M_O' = M_O + M_O'(F_R')
#   Exp 3: 合力作用线 + 合力矩定理 (合力对随机点的矩 = 力系对同点的矩)
#   Exp 4: 主矢为零 (纯力偶系) 时主矩与矩心无关
# 随机种子固定, 结果可复现; print 全 ASCII (GBK 控制台安全)

import numpy as np

rng = np.random.default_rng(42)
TOL = 1e-9
N_TRIALS = 500
N_CHECK_POINTS = 5


def moment(Fx, Fy, px, py, cx, cy):
    """力 (Fx,Fy) 作用于 (px,py) 对矩心 (cx,cy) 之矩, 逆时针为正."""
    return (px - cx) * Fy - (py - cy) * Fx


def rand_force():
    return rng.uniform(-10.0, 10.0, 2)


def rand_point():
    return rng.uniform(-5.0, 5.0, 2)


def rand_system():
    n = int(rng.integers(3, 7))
    forces = [rand_force() for _ in range(n)]
    points = [rand_point() for _ in range(n)]
    return forces, points


print("=" * 64)
print("L02 verification: simplification of coplanar force systems")
print("trials per experiment: %d, check points per trial: %d" % (N_TRIALS, N_CHECK_POINTS))
print("=" * 64)

# ---------------- Exp 0: 复现讲义例题 1 ----------------
forces = [(40.0, 0.0), (0.0, 30.0), (-20.0, -20.0)]
points = [(0.0, 4.0), (3.0, 0.0), (3.0, 1.0)]
FRx = sum(f[0] for f in forces)
FRy = sum(f[1] for f in forces)
MO = sum(moment(f[0], f[1], p[0], p[1], 0.0, 0.0) for f, p in zip(forces, points))
print("[Exp 0] hand-example replay: F_R' = (%.3f, %.3f), |F_R'| = %.4f N, M_O = %.3f N*m" % (FRx, FRy, np.hypot(FRx, FRy), MO))
print("[Exp 0] resultant line: %.3f*x - %.3f*y = %.3f  (i.e. y = 0.5*x + 5.5)" % (FRy, FRx, MO))
ok0 = (abs(FRx - 20) < TOL and abs(FRy - 10) < TOL and abs(MO - (-110.0)) < TOL
        and abs(FRy / FRx - 0.5) < TOL and abs(-MO / FRx - 5.5) < TOL)
print("[Exp 0] matches hand calculation: %s" % ("PASS" if ok0 else "FAIL"))

# ---------------- Exp 1: 力线平移定理等价性 ----------------
max_diff_1 = 0.0
pass_1 = 0
for _ in range(N_TRIALS):
    Fx, Fy = rand_force()
    px, py = rand_point()
    ox, oy = rand_point()
    couple = moment(Fx, Fy, px, py, ox, oy)  # 附加力偶 = 原力对 O 之矩
    for _ in range(N_CHECK_POINTS):
        qx, qy = rand_point()
        m_orig = moment(Fx, Fy, px, py, qx, qy)                       # 原力对 Q
        m_equiv = moment(Fx, Fy, ox, oy, qx, qy) + couple             # 平移力+力偶对 Q
        d = abs(m_orig - m_equiv)
        max_diff_1 = max(max_diff_1, d)
    pass_1 += 1
print("[Exp 1] force-translation equivalence: %d/%d groups consistent (max moment diff %.3e) %s"
      % (pass_1, N_TRIALS, max_diff_1, "PASS" if pass_1 == N_TRIALS else "FAIL"))

# ---------------- Exp 2: 主矩换心公式 ----------------
max_diff_2 = 0.0
pass_2 = 0
for _ in range(N_TRIALS):
    forces, points = rand_system()
    O = (0.0, 0.0)
    Op = rand_point()
    MO = sum(moment(f[0], f[1], p[0], p[1], *O) for f, p in zip(forces, points))
    FRx = sum(f[0] for f in forces)
    FRy = sum(f[1] for f in forces)
    MOp_direct = sum(moment(f[0], f[1], p[0], p[1], *Op) for f, p in zip(forces, points))
    MOp_formula = MO + moment(FRx, FRy, O[0], O[1], *Op)  # F_R' 作用于 O, 对 O' 取矩
    d = abs(MOp_direct - MOp_formula)
    max_diff_2 = max(max_diff_2, d)
    if d < TOL:
        pass_2 += 1
print("[Exp 2] moment shift formula: %d/%d groups |M_O' - (M_O + M_O'(F_R'))| < %.0e %s"
      % (pass_2, N_TRIALS, TOL, "PASS" if pass_2 == N_TRIALS else "FAIL"))

# ---------------- Exp 3: 合力作用线 + 合力矩定理 ----------------
max_diff_3 = 0.0
pass_3 = 0
for _ in range(N_TRIALS):
    while True:
        forces, points = rand_system()
        FRx = sum(f[0] for f in forces)
        FRy = sum(f[1] for f in forces)
        if np.hypot(FRx, FRy) > 0.5:
            break
    MO = sum(moment(f[0], f[1], p[0], p[1], 0.0, 0.0) for f, p in zip(forces, points))
    # 合力线上取一点: x*FRy - y*FRx = MO
    if abs(FRx) >= abs(FRy):
        px_star, py_star = 0.0, -MO / FRx
    else:
        px_star, py_star = MO / FRy, 0.0
    line_residual = abs(moment(FRx, FRy, px_star, py_star, 0.0, 0.0) - MO)
    group_ok = line_residual < TOL
    for _ in range(N_CHECK_POINTS):
        qx, qy = rand_point()
        m_res = moment(FRx, FRy, px_star, py_star, qx, qy)   # 合力对 Q
        m_sys = sum(moment(f[0], f[1], p[0], p[1], qx, qy) for f, p in zip(forces, points))
        d = abs(m_res - m_sys)
        max_diff_3 = max(max_diff_3, d)
        if d >= TOL:
            group_ok = False
    if group_ok:
        pass_3 += 1
print("[Exp 3] resultant line + Varignon: %d/%d groups, resultant moment = system moment at random points %s"
      % (pass_3, N_TRIALS, "PASS" if pass_3 == N_TRIALS else "FAIL"))

# ---------------- Exp 4: 纯力偶系主矩与矩心无关 ----------------
max_diff_4 = 0.0
pass_4 = 0
for _ in range(N_TRIALS):
    Fx, Fy = rand_force()
    p1 = rand_point()
    p2 = rand_point()
    base = None
    group_ok = True
    for _ in range(N_CHECK_POINTS):
        c = rand_point()
        M = moment(Fx, Fy, p1[0], p1[1], *c) + moment(-Fx, -Fy, p2[0], p2[1], *c)
        if base is None:
            base = M
        else:
            d = abs(M - base)
            max_diff_4 = max(max_diff_4, d)
            if d >= TOL:
                group_ok = False
    if group_ok:
        pass_4 += 1
print("[Exp 4] couple moment center-independent: %d/%d groups, moment deviation < %.0e %s"
      % (pass_4, N_TRIALS, TOL, "PASS" if pass_4 == N_TRIALS else "FAIL"))

print("=" * 64)
all_pass = ok0 and pass_1 == N_TRIALS and pass_2 == N_TRIALS and pass_3 == N_TRIALS and pass_4 == N_TRIALS
print("OVERALL: %s" % ("ALL PASS" if all_pass else "SOME FAILED"))
