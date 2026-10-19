# L04 空间力系理论验证
# 规模纪律: 目标 < 1 秒; 纯 numpy 矢量运算, 无其他依赖
# 验证内容:
#   Exp 1: 力对轴之矩两种算法一致 (解析 (r x F).u vs 投影到垂直轴平面的平面算法)
#   Exp 2: 空间主矩换心公式 M_O' = M_O + (r_O - r_O') x F_R'
#   Exp 3: 力螺旋最简形态: r* = F x M_perp / |F|^2 平移后主矩与主矢平行
#   Exp 4: 例 4 挖孔板重心: 负面积公式 vs 网格数值积分
# 随机种子固定, print 全 ASCII (GBK 控制台安全)

import numpy as np

rng = np.random.default_rng(42)
TOL = 1e-9
N_TRIALS = 500


def rand_vec():
    return rng.uniform(-10.0, 10.0, 3)


def rand_unit():
    v = rand_vec()
    return v / np.linalg.norm(v)


def cross(a, b):
    return np.cross(a, b)


def moment_about_axis(r, F, u):
    """力对过原点、方向 u 的轴之矩 (解析式)."""
    return np.dot(cross(r, F), u)


def moment_about_axis_plane(r, F, u):
    """力对轴之矩 (平面投影法): 把 r, F 投到垂直 u 的平面按 2D 叉乘算."""
    # 构造平面右手基: e1 x e2 = u
    tmp = np.array([1.0, 0.0, 0.0]) if abs(u[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    e1 = cross(u, tmp)
    e1 = e1 / np.linalg.norm(e1)
    e2 = cross(u, e1)  # e1 x e2 = u (右手系)
    r1, r2 = np.dot(r, e1), np.dot(r, e2)
    F1, F2 = np.dot(F, e1), np.dot(F, e2)
    return r1 * F2 - r2 * F1  # 2D 叉乘, 从 u 正向看逆时针为正


print("=" * 64)
print("L04 spatial force system verification")
print("trials per experiment: %d (exp 4 deterministic)" % N_TRIALS)
print("=" * 64)

# ---------------- Exp 1: 轴矩两种算法一致 ----------------
max_d1 = 0.0
ok1 = 0
for _ in range(N_TRIALS):
    r, F, u = rand_vec(), rand_vec(), rand_unit()
    m_a = moment_about_axis(r, F, u)
    m_p = moment_about_axis_plane(r, F, u)
    d = abs(m_a - m_p)
    max_d1 = max(max_d1, d)
    if d < TOL:
        ok1 += 1
print("[Exp 1] moment about axis: analytic vs plane-projection")
print("  max |diff| = %.1e  %s (%d/%d groups)"
      % (max_d1, "PASS" if ok1 == N_TRIALS else "FAIL", ok1, N_TRIALS))

# ---------------- Exp 2: 空间换心公式 ----------------
max_d2 = 0.0
ok2 = 0
for _ in range(N_TRIALS):
    n = int(rng.integers(3, 7))
    forces = [rand_vec() for _ in range(n)]
    points = [rand_vec() for _ in range(n)]
    O = np.zeros(3)
    Op = rand_vec()
    MO = sum(cross(points[i], forces[i]) for i in range(n))
    FR = sum(forces)
    MOp_direct = sum(cross(points[i] - Op, forces[i]) for i in range(n))
    MOp_formula = MO + cross(O - Op, FR)
    d = np.linalg.norm(MOp_direct - MOp_formula)
    max_d2 = max(max_d2, d)
    if d < TOL:
        ok2 += 1
print("[Exp 2] spatial moment shift formula")
print("  max |M_O' - (M_O + (r_O - r_O') x F_R')| = %.1e  %s (%d/%d)"
      % (max_d2, "PASS" if ok2 == N_TRIALS else "FAIL", ok2, N_TRIALS))

# ---------------- Exp 3: 力螺旋最简形态 ----------------
max_d3 = 0.0
max_par_err = 0.0
ok3 = 0
for _ in range(N_TRIALS):
    while True:
        n = int(rng.integers(3, 7))
        forces = [rand_vec() for _ in range(n)]
        points = [rand_vec() for _ in range(n)]
        FR = sum(forces)
        if np.linalg.norm(FR) >= 1.0:
            break
    MO = sum(cross(points[i], forces[i]) for i in range(n))
    F_hat = FR / np.linalg.norm(FR)
    M_par = np.dot(MO, F_hat) * F_hat   # 平行分量
    M_perp = MO - M_par                  # 垂直分量
    r_star = cross(FR, M_perp) / np.dot(FR, FR)
    # 新中心 O' = r_star; 主矩 = M_O + (r_O - r_O') x F_R' = MO - r_star x FR
    M_new = MO - cross(r_star, FR)
    perp_res = M_new - np.dot(M_new, F_hat) * F_hat   # 残余垂直分量, 应为零
    par_err = abs(np.dot(M_new, F_hat) - np.dot(MO, F_hat))  # 平行分量应保持
    d = np.linalg.norm(perp_res)
    max_d3 = max(max_d3, d)
    max_par_err = max(max_par_err, par_err)
    if d < TOL and par_err < TOL:
        ok3 += 1
print("[Exp 3] force screw reduction: M(P*) parallel to F")
print("  max |cross(F_hat, M_at_P*)| = %.1e  %s (%d/%d)" % (max_d3, "PASS" if ok3 == N_TRIALS else "FAIL", ok3, N_TRIALS))
print("  parallel component preserved (max rel err %.1e)" % max_par_err)

# ---------------- Exp 4: 挖孔板重心 (例 4) ----------------
W, H, nw, nh = 60.0, 40.0, 20.0, 20.0
x_notch, y_notch = 40.0, 0.0  # 挖孔块位置 (x in [40,60], y in [0,20])
A1 = W * H
cx1, cy1 = W / 2, H / 2
A2 = -nw * nh
cx2, cy2 = x_notch + nw / 2, y_notch + nh / 2
xC = (A1 * cx1 + A2 * cx2) / (A1 + A2)
yC = (A1 * cy1 + A2 * cy2) / (A1 + A2)
# 网格积分 (0.5 cm)
step = 0.5
xs = np.arange(step / 2, W, step)
ys = np.arange(step / 2, H, step)
XX, YY = np.meshgrid(xs, ys)
mask = ~((XX >= x_notch) & (XX <= x_notch + nw) & (YY >= y_notch) & (YY <= y_notch + nh))
xg = XX[mask].mean()
yg = YY[mask].mean()
print("[Exp 4] centroid of notched plate (60x40, notch 20x20)")
print("  formula (negative area):  (%.3f, %.3f) cm" % (xC, yC))
print("  grid integration (0.5 cm): (%.3f, %.3f) cm" % (xg, yg))
print("  diff = (%.3f, %.3f) cm  %s" % (xC - xg, yC - yg, "PASS" if abs(xC - xg) < 0.01 and abs(yC - yg) < 0.01 else "FAIL"))

print("=" * 64)
all_pass = ok1 == N_TRIALS and ok2 == N_TRIALS and ok3 == N_TRIALS and abs(xC - xg) < 0.01
print("OVERALL: %s" % ("ALL PASS" if all_pass else "SOME FAILED"))
