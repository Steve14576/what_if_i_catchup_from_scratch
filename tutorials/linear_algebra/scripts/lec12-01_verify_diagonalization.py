# lec12-01_verify_diagonalization.py
# 第 12 讲验证脚本：对角化 A=P*Lambda*P^-1、幂公式 A^k=P*Lambda^k*P^-1、
#                      可对角化判据、递推数列(Binet)、马尔可夫稳态、不可对角化者的幂
# 规模纪律：小规模演示（2x2 / 3x3 + matrix_power 到 k=50），目标 < 1 秒。

import time
import numpy as np

T0 = time.perf_counter()
sqrt5 = np.sqrt(5.0)

print("=== EXP1: 主例对角化 + 幂公式——A=[2,1;1,2], P=[(1,1),(1,-1)], Lambda=diag(3,1) ===")
A = np.array([[2., 1.], [1., 2.]])
P = np.array([[1., 1.], [1., -1.]])
Lam = np.diag([3., 1.])
print(f"  P^-1 A P =\n{np.round(np.linalg.inv(P) @ A @ P, 10)}   (应为 diag(3,1))")
print(f"  A P =\n{A @ P}\n  P Lambda =\n{P @ Lam}   (AP = P*Lambda, 每列都是特征向量配对)")
for k in [2, 5, 10]:
    lhs = np.linalg.matrix_power(A, k)
    rhs = P @ np.diag([3.0**k, 1.0**k]) @ np.linalg.inv(P)
    print(f"  A^{k}: 公式与硬乘最大差 = {np.abs(lhs - rhs).max():.2e}")
A10 = np.linalg.matrix_power(A, 10)
print(f"  A^10 =\n{A10}   (手算 (1/2)[[3^10+1, 3^10-1],[3^10-1, 3^10+1]], 3^10=59049)")

print()
print("=== EXP2: 列序无关性——换一列顺序仍是合法对角化 ===")
P2 = np.array([[1., 1.], [-1., 1.]])       # 列序换成 (1,-1),(1,1)
Lam2 = np.diag([1., 3.])
print(f"  P2^-1 A P2 =\n{np.round(np.linalg.inv(P2) @ A @ P2, 10)}   (diag(1,3)——Lambda 跟着列序走)")

print()
print("=== EXP3: 可对角化判定器——数'能凑到的无关特征向量总数' ===")
def diag_check(name, A):
    lam, V = np.linalg.eig(A)
    lam = np.round(lam.real, 8)
    total = 0
    for l in np.unique(lam):
        g = A.shape[0] - np.linalg.matrix_rank(A - l*np.eye(A.shape[0]))
        total += g
        print(f"    lambda={l}: 几何重数 {g}")
    print(f"  {name}: 无关特征向量总数 {total}/{A.shape[0]} -> "
          f"{'可对角化' if total == A.shape[0] else '不可对角化'}")
diag_check("A(主例, 互异 3,1)", A)
A3 = np.array([[2., 1., 0.], [1., 2., 0.], [0., 0., 3.]])
diag_check("A3(重根不亏: 1,3,3)", A3)
diag_check("剪切 S(重根缺口)", np.array([[1., 1.], [0., 1.]]))
diag_check("J=[3,1;0,3](重根缺口)", np.array([[3., 1.], [0., 3.]]))

print()
print("=== EXP4: 递推数列——斐波那契 F=[1,1;1,0], Binet 公式 ===")
F = np.array([[1., 1.], [1., 0.]])
lamF, _ = np.linalg.eig(F)
phi, psi = (1 + sqrt5)/2, (1 - sqrt5)/2
print(f"  eigenvalues = {np.round(np.sort(lamF), 6)}  (phi=(1+sqrt5)/2={phi:.6f}, psi={psi:.6f})")
print(f"  F^10 =\n{np.linalg.matrix_power(F, 10).astype(int)}   (应为 [[89,55],[55,34]])")
fib = [(phi**k - psi**k)/sqrt5 for k in range(12)]
print(f"  Binet: f_k=(phi^k-psi^k)/sqrt5, k=0..11 -> {np.round(fib, 4)}")
print(f"  全部是整数数列 0,1,1,2,3,5,8,13,21,34,55,89? 最大偏差 {max(abs(np.array(fib)-np.round(fib))):.2e}")

print()
print("=== EXP5: 马尔可夫稳态——Mk=[0.9,0.2;0.1,0.8], lambda=1,0.7 ===")
Mk = np.array([[0.9, 0.2], [0.1, 0.8]])
Pm = np.array([[2., 1.], [1., -1.]])          # 列: (2,1) 属 lambda=1; (1,-1) 属 0.7
Lm = np.diag([1., 0.7])
print(f"  Pm^-1 Mk Pm =\n{np.round(np.linalg.inv(Pm) @ Mk @ Pm, 10)}   (diag(1, 0.7))")
for k in [5, 20]:
    lhs = np.linalg.matrix_power(Mk, k)
    rhs = Pm @ np.diag([1.0, 0.7**k]) @ np.linalg.inv(Pm)
    print(f"  Mk^{k}: 公式与硬乘最大差 = {np.abs(lhs - rhs).max():.2e}")
M50 = np.linalg.matrix_power(Mk, 50)
print(f"  Mk^50 =\n{np.round(M50, 6)}   (每列都趋于稳态 (2/3, 1/3); 0.7^50={0.7**50:.2e})")

print()
print("=== EXP6: 不可对角化者的幂——显式结构 ===")
S = np.array([[1., 1.], [0., 1.]])
ok = all(np.array_equal(np.linalg.matrix_power(S, k), np.array([[1., float(k)], [0., 1.]]))
         for k in range(1, 6))
print(f"  剪切 S^k = [[1,k],[0,1]] 对 k=1..5 全部成立: {ok}")
J = np.array([[3., 1.], [0., 3.]])
for k in [2, 3]:
    formula = np.array([[3.0**k, k*3.0**(k-1)], [0., 3.0**k]])
    print(f"  J^{k}: 公式 [[3^k, k*3^(k-1)],[0,3^k]] 与硬乘最大差 = "
          f"{np.abs(np.linalg.matrix_power(J, k) - formula).max():.2e}")

print()
print("=== EXP7: 三态马尔可夫——手算特征多项式 (0.7-lambda)(lambda-1)(lambda-0.5) 验收 ===")
M3 = np.array([[0.7, 0.1, 0.], [0.3, 0.8, 0.3], [0., 0.1, 0.7]])
lam3, V3 = np.linalg.eig(M3)
print(f"  eigenvalues = {np.round(np.sort(lam3), 6)}  (手算: 0.5, 0.7, 1)")
i1 = np.argmin(np.abs(lam3 - 1.0))
v = V3[:, i1]; v = v / v.sum()
print(f"  lambda=1 特征向量归一化(分量和=1): {np.round(v, 6)}  (手算稳态 (0.2,0.6,0.2))")
M3_30 = np.linalg.matrix_power(M3, 30)
print(f"  M3^30 =\n{np.round(M3_30, 6)}\n  (每列 -> 稳态; 0.7^30={0.7**30:.2e}, 0.5^30={0.5**30:.2e})")

print()
print(f"  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
