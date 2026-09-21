# lec20-01_verify_numerics.py
# 第 20 讲验证脚本：浮点误差与灾难性抵消、主元选取对照、希尔伯特条件数与扰动放大、
#                   朴素 LU 与部分主元(含分解复用)、Cholesky(含非正定失败与 n=500 计时)、
#                   kappa(A^T A)=kappa(A)^2 与 eigh 路线的精度崩塌、
#                   Jacobi/GS/CG 迭代收敛对比(含发散反例)、旧账对账(kappa*eps 界)、
#                   特征值敏感(对称按 1 倍 vs 剪切按 sqrt, 18 讲悬崖的续集)
# 规模纪律：小手算矩阵 + n=20 迭代例 + 单个 n=500 计时, 目标 < 2 秒。

import time
import numpy as np
from scipy.linalg import lu, lu_factor, lu_solve, cholesky, cho_solve, LinAlgError

T0 = time.perf_counter()
rng = np.random.default_rng(20)
EPS = np.finfo(float).eps


def timeit(f, k=3):
    ts = []
    for _ in range(k):
        t = time.perf_counter()
        f()
        ts.append(time.perf_counter() - t)
    return min(ts)


print("=== EXP1: 浮点基础 -- 0.1+0.2, eps, 灾难性抵消 ===")
print(f"  0.1 + 0.2 = {0.1 + 0.2!r}   (用 ==0.3 判断: {0.1 + 0.2 == 0.3})")
print(f"  0.1 + 0.2 - 0.3 = {0.1 + 0.2 - 0.3:.3e}")
print(f"  eps = {EPS:.3e}  (= 2^-52, 1.0 后面最小的可见增量)")
print(f"  1 + eps/2 == 1 ?  {1 + EPS / 2 == 1}   (半个 eps 被舍掉)")
print(f"  1 + eps   == 1 ?  {1 + EPS == 1}   (一个整 eps 恰好进位)")
x = 1e8
naive = np.sqrt(x * x + 1.0) - x
stable = 1.0 / (np.sqrt(x * x + 1.0) + x)
print(f"  sqrt(1e16+1) - 1e8: 直算 = {naive:.3e},  等价变形 1/(sqrt+1e8) = {stable:.3e}")
print("  -> 大数相减 = 灾难性抵消: 有效位数当场蒸发; 同一数学式的变形公式可以救回全部精度")

print()
print("=== EXP2: 主元选取 -- 同一道 2x2, 两种消元顺序 ===")
A2 = np.array([[1e-20, 1.0], [1.0, 1.0]])
b2 = np.array([1.0 + 1e-20, 2.0])
# 无主元(按原顺序消元): 乘数 = 1/1e-20
mu = A2[1, 0] / A2[0, 0]
a22 = A2[1, 1] - mu * A2[0, 1]
b2e = b2[1] - mu * b2[0]
x2_bad = b2e / a22
x1_bad = (b2[0] - A2[0, 1] * x2_bad) / A2[0, 0]
# 部分主元(换行, 大主元上位)
mu2 = A2[0, 0] / A2[1, 0]
a22b = A2[0, 1] - mu2 * A2[1, 1]
b2f = b2[0] - mu2 * b2[1]
x2_good = b2f / a22b
x1_good = (b2[1] - A2[1, 1] * x2_good) / A2[1, 0]
print(f"  真解 = (1, 1)")
print(f"  无主元:   x = ({x1_bad:.3g}, {x2_bad:.3g})   最大误差 = {max(abs(x1_bad - 1), abs(x2_bad - 1)):.3g}")
print(f"  部分主元: x = ({x1_good:.3g}, {x2_good:.3g})   最大误差 = {max(abs(x1_good - 1), abs(x2_good - 1)):.3g}")
print(f"  (无主元乘数 mu = 1/1e-20 = {mu:.0e}; 大乘数 = 舍入误差的放大器)")

print()
print("=== EXP3: 条件数 -- 希尔伯特矩阵的扰动放大 ===")
H4 = np.array([[1 / (i + j + 1) for j in range(4)] for i in range(4)])
H8 = np.array([[1 / (i + j + 1) for j in range(8)] for i in range(8)])
k4, k8 = np.linalg.cond(H4), np.linalg.cond(H8)
print(f"  kappa_2(H4) = {k4:.3e};   kappa_2(H8) = {k8:.3e}")
U4, s4, Vt4 = np.linalg.svd(H4)
b4 = H4 @ np.ones(4)
x1 = np.linalg.solve(H4, b4)
d = 1e-10
amps = []
for _ in range(3):
    db = rng.normal(size=4)
    db = d * np.linalg.norm(b4) * db / np.linalg.norm(db)
    x2 = np.linalg.solve(H4, b4 + db)
    amps.append((np.linalg.norm(x2 - x1) / np.linalg.norm(x1)) / d)
db = d * np.linalg.norm(b4) * U4[:, -1]
x2 = np.linalg.solve(H4, b4 + db)
amp_worst = (np.linalg.norm(x2 - x1) / np.linalg.norm(x1)) / d
print(f"  相对扰动 1e-10: 随机方向(3 次取最大)放大 {max(amps):.2e} 倍")
print(f"                  最坏方向(u_min)放大 {amp_worst:.2e} 倍   (与 kappa = {k4:.2e} 同量级)")
b8 = H8 @ np.ones(8)
U8, s8, Vt8 = np.linalg.svd(H8)
x_fake = np.ones(8) + 1e-4 * Vt8[-1]
r_rel = np.linalg.norm(b8 - H8 @ x_fake) / np.linalg.norm(b8)
e_rel = np.linalg.norm(x_fake - np.ones(8)) / np.linalg.norm(np.ones(8))
print(f"  小残差陷阱(H8): 人为解沿 v_min 偏 1e-4 -> 相对残差 {r_rel:.2e}, 相对误差 {e_rel:.2e}")
print(f"  -> 残差 1e-14 级看着像解对了, 误差 1e-4 级; 误差/残差 ~ kappa(H8) = {k8:.1e}")

print()
print("=== EXP4: 朴素 LU vs 部分主元 LU ===")


def naive_lu(A):
    n = A.shape[0]
    L = np.eye(n)
    U = A.astype(float).copy()
    for k in range(n - 1):
        for i in range(k + 1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]
    return L, U


L2, U2 = naive_lu(A2)
print(f"  朴素 LU 的 L 第二行 = {L2[1].tolist()}   (乘数 1e20 写进 L, 埋雷)")
P2, Lp, Up = lu(A2)
print(f"  scipy PLU: ||P A - L U||max = {np.abs(P2 @ A2 - Lp @ Up).max():.1e},  置换 P = {P2.astype(int).tolist()}")
luA = lu_factor(A2)
xb1 = lu_solve(luA, b2)
b2b = np.array([3.0, 4.0])
xb2 = lu_solve(luA, b2b)
print(f"  一次分解多次回代: x = {np.round(xb1, 6).tolist()};  换右端 b = {b2b.tolist()}: 残差 {np.abs(A2 @ xb2 - b2b).max():.1e}")

print()
print("=== EXP5: Cholesky -- 正定'平方根', 以及它为什么快 ===")
A5 = np.array([[4.0, 12.0, -16.0], [12.0, 37.0, -43.0], [-16.0, -43.0, 98.0]])
L5 = cholesky(A5, lower=True)
b5 = np.array([1.0, 2.0, 3.0])
x5 = cho_solve((L5, True), b5)
print(f"  ||L L^T - A||max = {np.abs(L5 @ L5.T - A5).max():.1e};  解方程残差 = {np.abs(A5 @ x5 - b5).max():.1e}")
try:
    cholesky(np.array([[1.0, 2.0], [2.0, 1.0]]), lower=True)
    print("  非正定未报错? (异常)")
except LinAlgError:
    print("  非正定矩阵 (1,2;2,1): Cholesky 直接报 LinAlgError (开到负数平方根就停, 不假装成功)")
n = 500
M = rng.normal(size=(n, n))
M = M @ M.T + n * np.eye(n)
bb = rng.normal(size=n)
t_solve = timeit(lambda: np.linalg.solve(M, bb))
t_chol = timeit(lambda: cho_solve((cholesky(M, lower=True), True), bb))
print(f"  n=500 SPD 求解计时(3 次取最小): solve {t_solve * 1e3:.0f} ms vs cholesky+cho_solve {t_chol * 1e3:.0f} ms")

print()
print("=== EXP6: kappa(A^T A) = kappa(A)^2 -- 为什么别用 eigh(A^T A) 算 SVD ===")
print(f"  H4: kappa = {k4:.3e};   kappa(H4^T H4) = {np.linalg.cond(H4.T @ H4):.3e};   kappa^2 = {k4 ** 2:.3e}")
H6 = np.array([[1 / (i + j + 1) for j in range(6)] for i in range(6)])
s6 = np.linalg.svd(H6, compute_uv=False)
ev6 = np.linalg.eigvalsh(H6.T @ H6)
s6e = np.sqrt(np.clip(ev6, 0.0, None))[::-1]
print(f"  H6 最小奇异值: svd 直算 = {s6[-1]:.3e};  sqrt(eigh(H^T H)) = {s6e[-1]:.3e};  相对偏差 = {abs(s6e[-1] - s6[-1]) / s6[-1]:.1e}")
ev8 = np.linalg.eigvalsh(H8.T @ H8)
s8_min = np.linalg.svd(H8, compute_uv=False)[-1]
print(f"  H8: eigh 最小特征值 = {ev8[0]:.2e} (真实 sigma_min^2 = {s8_min ** 2:.2e}) -> 平方后连正负都不保")
print("  -> A^T A 让条件数平方, 小奇异值的信息在平方这一步就被烧掉; 正路: 直接 svd(A)")

print()
print("=== EXP7: 迭代法 -- 1D 拉普拉斯 n=20 上 Jacobi / GS / CG ===")
n = 20
T = 2 * np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1)
bT = np.ones(n)
tol = 1e-8
dT = np.diag(np.diag(T))
RT = T - dT
x = np.zeros(n)
it_j = 0
while True:
    x = (bT - RT @ x) / np.diag(dT)
    it_j += 1
    if np.linalg.norm(bT - T @ x) / np.linalg.norm(bT) < tol:
        break
x = np.zeros(n)
it_g = 0
while True:
    for i in range(n):
        x[i] = (bT[i] - (T[i] @ x) + T[i, i] * x[i]) / T[i, i]
    it_g += 1
    if np.linalg.norm(bT - T @ x) / np.linalg.norm(bT) < tol:
        break
x = np.zeros(n)
r = bT - T @ x
p = r.copy()
rs = r @ r
it_c = 0
while True:
    Ap = T @ p
    alpha = rs / (p @ Ap)
    x = x + alpha * p
    r = r - alpha * Ap
    rs_new = r @ r
    it_c += 1
    if np.sqrt(rs_new) / np.linalg.norm(bT) < tol:
        break
    p = r + (rs_new / rs) * p
    rs = rs_new
BJ = np.linalg.solve(dT, -RT)
rho_j = np.abs(np.linalg.eigvals(BJ)).max()
kT = np.linalg.cond(T)
print(f"  到相对残差 1e-8: Jacobi {it_j} 步;  GS {it_g} 步;  CG {it_c} 步")
print(f"  Jacobi 谱半径 rho = {rho_j:.4f} (理论 cos(pi/21) = {np.cos(np.pi / (n + 1)):.4f} < 1 -> 收敛)")
print(f"  kappa_2(T) = {kT:.1f}, CG 步数量级 ~ sqrt(kappa) = {np.sqrt(kT):.1f} (精确算术上限 n = {n} 步)")
Tb = np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1)
dbT = np.diag(np.diag(Tb))
Rb = Tb - dbT
x = np.zeros(n)
res_seq = []
for _ in range(5):
    x = (bT - Rb @ x) / np.diag(dbT)
    res_seq.append(np.linalg.norm(bT - Tb @ x))
BB = np.linalg.solve(dbT, -Rb)
rho_b = np.abs(np.linalg.eigvals(BB)).max()
print(f"  反例(对角 1, off -1): Jacobi 谱半径 rho = {rho_b:.3f} > 1 -> 残差序列 {' -> '.join(f'{v:.1e}' for v in res_seq)}")

print()
print("=== EXP8: 旧账对账 -- kappa*eps 界 vs 前面各讲实测 ===")
print(f"  H4: QR 解误差量级 ~ kappa*eps = {k4 * EPS:.1e}   [14 讲实测 6.2e-13, 吻合]")
print(f"      正规方程 ~ kappa^2*eps = {k4 ** 2 * EPS:.1e}   [14 讲实测 1.9e-9, 界内(界是上界)]")
t = np.arange(12.0)
V = np.column_stack([t ** k for k in range(10)])
kV = np.linalg.cond(V)
print(f"  15 讲 V(12x10): kappa = {kV:.1e};  kappa^2 = {kV ** 2:.1e} (远超 1/eps = {1 / EPS:.1e})")
print("  -> kappa^2 > 1/eps: 正规方程'本钱全亏光'; kappa > 1/eps 时连 QR 也救不了(信息在双精度里不可表示)")

print()
print("=== EXP9: 特征值敏感 -- 对称按 1 倍走, 剪切按 sqrt 走 (18 讲续集) ===")
delta = 1e-12
As = np.array([[2.0, 0.3], [0.3, 4.0]])
ev0s = np.linalg.eigvalsh(As)
dev_s = 0.0
for _ in range(3):
    S = rng.normal(size=(2, 2))
    S = (S + S.T) / 2
    S /= np.linalg.norm(S, 2)
    dev_s = max(dev_s, np.abs(np.linalg.eigvalsh(As + delta * S) - ev0s).max())
J = np.array([[1.0, 1.0], [0.0, 1.0]])
dev_n = 0.0
for _ in range(3):
    S = rng.normal(size=(2, 2))
    S /= np.linalg.norm(S, 2)
    dev_n = max(dev_n, np.abs(np.linalg.eigvals(J + delta * S) - np.linalg.eigvals(J)).max())
print(f"  扰动幅度 {delta:.0e}:")
print(f"  对称矩阵:   特征值最大位移 {dev_s:.2e}   (放大 {dev_s / delta:.1f} 倍, 对称理论上界就是 1 倍)")
print(f"  剪切(缺陷): 特征值最大位移 {dev_n:.2e}   (放大 {dev_n / delta:.1e} 倍, 约 1/sqrt(delta) 级别)")
print("  -> 同样是 1e-12 的扰动: 对称矩阵纹丝不动, 剪切特征值当场挪 1e-6 (18 讲悬崖的机制)")

print()
print(f"[done] total {time.perf_counter() - T0:.2f} s")