# lec18-01_verify_jordan.py
# 第 18 讲验证脚本：重数缺口诊断、广义特征向量链、P^{-1}AP=J 全程对账、
#                   链的非唯一性、J^k 二项式公式(k 到 100)、A^100 via 若尔当、
#                   e^{Jt} 形状(scipy expm 权威对照)、读块规则(块数=几何重数)、
#                   数值脆弱性(扰动 eps -> 特征值跑 sqrt(eps))
# 规模纪律：全 2x2/3x3/4x4 小手算例，目标 < 1 秒。

import time
import numpy as np
from scipy.linalg import expm

T0 = time.perf_counter()
rng = np.random.default_rng(18)
I2 = np.eye(2)

print("=== EXP1: 主例 A=[[3,1],[-1,5]] -- 双根 4, 重数缺口诊断 ===")
A = np.array([[3., 1.], [-1., 5.]])
lam = np.linalg.eigvals(A).real
print(f"  eig(A) 实部 = {np.round(lam, 10).tolist()}  (手算: det(A-λI)=(λ-4)^2 双根)")
N = A - 4.0 * I2
rk = np.linalg.matrix_rank(N)
print(f"  N = A - 4I = {N.tolist()}  (手算 [[-1,1],[-1,1]])")
print(f"  rank(N) = {rk};  几何重数 = 2 - rank = {2 - rk};  代数重数 = 2  -> 缺口 1, 不可对角化")

print()
print("=== EXP2: 广义特征向量链 -- v1=(1,1), v2=(0,1) ===")
v1 = np.array([1., 1.]); v2 = np.array([0., 1.])
print(f"  N @ v1 = {(N @ v1).tolist()}   (v1 是真特征向量: 一代归零)")
print(f"  N @ v2 = {(N @ v2).tolist()}   (= v1! v2 被 N 打成 v1, 两代才归零)")
P = np.column_stack([v1, v2])
Pinv = np.linalg.inv(P)
J = np.array([[4., 1.], [0., 4.]])
print(f"  P = [v1 v2] = {P.tolist()};  P^-1 = {Pinv.tolist()}  (手算 [[1,0],[-1,1]])")
print(f"  ||AP - PJ||max = {np.abs(A @ P - P @ J).max():.1e}  (配对验算 AP=PJ, 12 讲同款)")
print(f"  ||P^-1 A P - J||max = {np.abs(Pinv @ A @ P - J).max():.1e}  (若尔当形到手)")
print(f"  ||P^-1 P - I||max = {np.abs(Pinv @ P - I2).max():.1e}")

print()
print("=== EXP3: 幂零部分 N^2 = 0 -- 链长 2 的代数标志 ===")
print(f"  ||N @ N||max = {np.abs(N @ N).max():.1e}  (N^2 = 0: N 把整个平面两级扫空)")

print()
print("=== EXP4: 链不唯一 -- 任意 v (Nv≠0) 都给出另一组若尔当基 ===")
shown = 0
for trial in range(6):
    v = rng.normal(size=2)
    w = N @ v
    if np.linalg.norm(w) > 1e-9:
        P2 = np.column_stack([w, v])
        err = np.abs(np.linalg.inv(P2) @ A @ P2 - J).max()
        print(f"  trial {trial}: v={np.round(v, 3).tolist()}, w=Nv={np.round(w, 3).tolist()}, ||P2^-1AP2 - J||max = {err:.1e}")
        shown += 1
        if shown == 2:
            break

print()
print("=== EXP5: J^k 二项式公式 -- J^k = 4^k I + k*4^(k-1) N ===")
N1 = np.array([[0., 1.], [0., 0.]])
for k in (2, 5, 10, 100):
    hard = np.linalg.matrix_power(J, k)
    form = 4.0**k * I2 + k * 4.0**(k - 1) * N1
    rel = np.linalg.norm(hard - form) / np.linalg.norm(hard)
    print(f"  k={k:3d}: 相对偏差 = {rel:.1e}")
J100 = np.linalg.matrix_power(J, 100)
print(f"  k=100: 右上/左上 = {J100[0, 1] / J100[0, 0]:.6f}  (= k/4 = 25: '乘方 x 多项式')")

print()
print("=== EXP6: A^100 via 若尔当 -- A^k = P J^k P^-1 ===")
A100_hard = np.linalg.matrix_power(A, 100)
A100_jor = P @ J100 @ Pinv
rel = np.linalg.norm(A100_hard - A100_jor) / np.linalg.norm(A100_hard)
print(f"  相对偏差 = {rel:.1e}  (12 讲'乘方 x 多项式'路径的完备版)")
print(f"  A^100 / 4^100 = {np.round(A100_hard / 4.0**100, 6).tolist()}  (手算 [[1-25,25],[-25,1+25]] = [[-24,25],[-25,26]])")

print()
print("=== EXP7: e^{Jt} -- scipy expm 对照 e^{4t}[[1,t],[0,1]] ===")
for t in (0.5, 1.0):
    E1 = expm(J * t)
    E2 = np.exp(4.0 * t) * np.array([[1., t], [0., 1.]])
    print(f"  t={t}: ||expm(Jt) - e^(4t)*[[1,t],[0,1]]||max = {np.abs(E1 - E2).max():.1e}")
Et1 = expm(A)
Et2 = P @ expm(J) @ Pinv
print(f"  t=1, A 版: ||expm(A) - P expm(J) P^-1||max = {np.abs(Et1 - Et2).max():.1e}")

print()
print("=== EXP8: 读块规则 -- 块数 = 几何重数, 尺寸和 = 代数重数 ===")
J22 = np.array([[2., 1.], [0., 2.]])
B4 = np.zeros((4, 4)); B4[:2, :2] = J22; B4[2:, 2:] = J22
C3 = np.array([[5., 1., 0.], [0., 5., 0.], [0., 0., 5.]])
D3 = np.array([[2., 1., 0.], [0., 2., 1.], [0., 0., 2.]])
for name, M, l, blocks in (("diag(J2(2),J2(2))", B4, 2., 2), ("J2(5)+J1(5)", C3, 5., 2), ("J3(2)", D3, 2., 1)):
    n = M.shape[0]
    alg = int(np.sum(np.abs(np.linalg.eigvals(M).real - l) < 1e-9))
    geo = n - np.linalg.matrix_rank(M - l * np.eye(n))
    print(f"  {name}: 代数重数={alg}, 几何重数={geo}, 块数应为 {blocks}")

print()
print("=== EXP9: 数值脆弱性 -- 扰动 eps 让特征值跑到 1±sqrt(eps) ===")
for eps in (1e-4, 1e-8, 1e-12):
    M = np.array([[1., 1.], [eps, 1.]])
    ev = np.linalg.eigvals(M).real
    dev = np.abs(ev - 1).max()
    print(f"  eps={eps:.0e}: max|eig-1| = {dev:.3e};  sqrt(eps) = {np.sqrt(eps):.3e}")

print()
print(f"[done] total {time.perf_counter() - T0:.2f} s")