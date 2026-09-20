# lec15-01_verify_least_squares.py
# 第 15 讲验证脚本：无解诊断、正规方程直线/二次拟合全程、精确解退化、
#                      解不唯一但投影唯一、QR 双路线对账、病态拟合对照
# 规模纪律：小规模演示（4 点手算例 + 12x9 范德蒙德病态例），目标 < 1 秒。

import time
import numpy as np

T0 = time.perf_counter()
rng = np.random.default_rng(15)

print("=== EXP1: 无解诊断——b 不在列空间 ===")
A = np.array([[1., 0.], [1., 1.], [1., 2.], [1., 3.]])
b = np.array([1., 2., 4., 4.])
print(f"  rank(A) = {np.linalg.matrix_rank(A)}, rank([A b]) = {np.linalg.matrix_rank(np.column_stack([A, b]))}")
print(f"  -> 增广秩 > 系数秩: 无解 (第 04 讲判据); b 不在 col(A)")

print()
print("=== EXP2: 手算拟合全程对账——正规方程 [[4,6],[6,14]](c,d)=(11,22) ===")
AtA, Atb = A.T @ A, A.T @ b
xhat = np.linalg.solve(AtA, Atb)
p = A @ xhat
e = b - p
print(f"  A^T A =\n{AtA}  (Sigma 1 = 4, Sigma t = 6, Sigma t^2 = 14)")
print(f"  A^T b = {Atb}  (Sigma y = 11, Sigma ty = 22)")
print(f"  xhat = (c, d) = {np.round(xhat, 6)}  (手算 (1.1, 1.1)): 直线 y = 1.1 + 1.1 t")
print(f"  预测 p = {np.round(p, 4)}, 残差 e = {np.round(e, 4)}")
print(f"  自检 A^T e = {np.round(A.T @ e, 10)}  (零: 残差垂直两列 -> Sigma e = 0, Sigma t e = 0)")
print(f"  ||e||^2 = {e @ e:.4f}  (手算 0.7)")
for c2, d2 in [(1.0, 1.0), (1.2, 1.1), (0.9, 1.2)]:
    r = b - (c2 + d2*np.array([0., 1., 2., 3.]))
    print(f"  扰动对照 (c,d)=({c2},{d2}): ||b-Ax||^2 = {r @ r:.4f}  (> 0.7)")

print()
print("=== EXP3: 精确解退化——3 点共线, 最小二乘 = 精确解 ===")
A3 = np.array([[1., 0.], [1., 1.], [1., 2.]])
b3 = np.array([1., 3., 5.])            # 恰好共线 y = 1 + 2t
x3 = np.linalg.solve(A3.T @ A3, A3.T @ b3)
e3 = b3 - A3 @ x3
print(f"  xhat = {x3}  (精确解 (1,2)), 残差 = {np.round(e3, 10)}  (全零: b 本来就在 col(A))")
print(f"  -> 最小二乘兼容有解情形: 有解时'最好'就是'正好'")

print()
print("=== EXP4: A^T A 不可逆——解不唯一但投影唯一 ===")
Ac = np.array([[1., 1.], [1., 1.]])    # 列 2 = 列 1 (相关)
bc = np.array([2., 0.])
AtA_c = Ac.T @ Ac
print(f"  A^T A =\n{AtA_c}  (奇异); 正规方程 A^T A x = A^T b = {Ac.T @ bc}")
for x_try in [(0.5, 0.5), (1.0, 0.0), (0.0, 1.0)]:
    xs = np.array(x_try)
    print(f"    x = {x_try}: A x = {Ac @ xs}, A^T(b-Ax) = {np.round(Ac.T @ (bc - Ac @ xs), 10)} (都是解!)")
print(f"  -> x_hat 不唯一(差一个 N(A^T A) 里的向量), 但 Ax_hat 全等于 (1,1): 投影与残差唯一")
print(f"     残差 e = (1,-1), A^T e = {Ac.T @ (bc - np.array([1., 1.]))} (垂直列空间)")

print()
print("=== EXP5: QR 双路线对账 + P=QQ^T 投影 ===")
Q, R = np.linalg.qr(A)
x_qr = np.linalg.solve(R, Q.T @ b)
print(f"  QR 路线 x_hat = {np.round(x_qr, 6)}  (与正规方程路线零差级一致)")
P = Q @ Q.T
print(f"  P b = 预测 {np.round(P @ b, 4)}  (与 A x_hat 相同);  P^2=P: {np.abs(P@P-P).max():.1e}")
print(f"  (I-P) b = 残差 {np.round((np.eye(4)-P) @ b, 4)}  (与 e 相同)")

print()
print("=== EXP6: 病态拟合对照——12 点配 9 次多项式(范德蒙德) ===")
t = np.arange(12.0)
V = np.column_stack([t**k for k in range(10)])
c_true = rng.normal(size=10) * 0.5
bV = V @ c_true + 0.001 * rng.normal(size=12)
print(f"  (参考) cond(V) = {np.linalg.cond(V):.2e}  (条件数第 20 讲正式讲, 此处只看大小)")
x_ne = np.linalg.solve(V.T @ V, V.T @ bV)
Qv, Rv = np.linalg.qr(V)
x_qr = np.linalg.solve(Rv, Qv.T @ bV)
print(f"  恢复真系数的误差:  正规方程 ||x_ne - c_true|| = {np.linalg.norm(x_ne - c_true):.2e}")
print(f"                      QR       ||x_qr - c_true|| = {np.linalg.norm(x_qr - c_true):.2e}")
print(f"  -> 正规方程已完全失真, QR 仍可用 (14 讲结论的拟合版现场; 病到 cond>1e16 时 QR 也救不了, 20 讲)")

print()
print("=== EXP7: 二次拟合对照——嵌套子空间, SSE 只降不升 ===")
V2 = np.column_stack([np.ones(4), np.array([0., 1., 2., 3.]), np.array([0., 1., 4., 9.])])
x2 = np.linalg.solve(V2.T @ V2, V2.T @ b)
e2 = b - V2 @ x2
print(f"  二次 y = {np.round(x2, 4)}  (手算 0.85 + 1.85 t - 0.25 t^2)")
print(f"  残差 e2 = {np.round(e2, 4)};  A^T e2 = {np.round(V2.T @ e2, 10)}  (零)")
print(f"  SSE: 直线 {e @ e:.4f}  ->  二次 {e2 @ e2:.4f}  (span 嵌套: 投影距离必不增)")

print()
print(f"  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
