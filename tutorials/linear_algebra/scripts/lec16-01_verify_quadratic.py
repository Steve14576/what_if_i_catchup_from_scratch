# lec16-01_verify_quadratic.py
# 第 16 讲验证脚本：二次型=对称矩阵、配方/合同、Sylvester 与谱判据、
#                   正交法(谱定理)、水平集几何、球面 Rayleigh 区间、A^T A 正定回收
# 规模纪律：2x2/3x3 手算例 + 随机 5x5 + 2 万点球面采样，目标 < 1 秒。

import time
import numpy as np

T0 = time.perf_counter()
rng = np.random.default_rng(16)

print("=== EXP1: 二次型 = 对称矩阵——反对称部分被 x^T A x 杀死 ===")
A_ns = np.array([[2., 4.], [0., 5.]])          # 非对称
x0 = np.array([0.3, -0.7])
print(f"  非对称 [[2,4],[0,5]]:  x^T A x = {x0 @ A_ns @ x0:.6f}")
print(f"  对称部分 [[2,2],[2,5]]: x^T As x = {x0 @ ((A_ns + A_ns.T) / 2) @ x0:.6f}  (相同)")
print(f"  手算 2*0.09 + 4*0.3*(-0.7) + 5*0.49 = {2*0.09 + 4*0.3*(-0.7) + 5*0.49:.6f}")

print()
print("=== EXP2: 主例配方与合同——f = 2x^2+4xy+5y^2 = 2(x+y)^2 + 3y^2 ===")
A = np.array([[2., 2.], [2., 5.]])
P = np.array([[1., -1.], [0., 1.]])            # x = u - v, y = v  (u = x+y)
D = P.T @ A @ P
print(f"  P^T A P = {np.round(D, 10).tolist()}  (手算 diag(2,3))")
for pt in [(0.3, -0.7), (1.0, 2.0)]:
    lhs = 2 * pt[0]**2 + 4 * pt[0] * pt[1] + 5 * pt[1]**2
    rhs = 2 * (pt[0] + pt[1])**2 + 3 * pt[1]**2
    print(f"  点 {pt}: 2x^2+4xy+5y^2 = {lhs:.6f},  2(x+y)^2+3y^2 = {rhs:.6f}  (零差)")

print()
print("=== EXP3: 正交法——lambda=(1,6), Q^T A Q = diag(1,6) ===")
lam, Q = np.linalg.eigh(A)
print(f"  eigvals = {np.round(lam, 6).tolist()}  (手算 1, 6: 迹 7 = 1+6, det 6 = 1*6)")
print(f"  Q = {np.round(Q, 6).tolist()}")
print(f"  (Q 列 = 单位特征向量 (2,-1)/sqrt5 与 (1,2)/sqrt5, 符号可反)")
print(f"  Q^T Q - I max = {np.abs(Q.T @ Q - np.eye(2)).max():.1e};  Q^T A Q = {np.round(Q.T @ A @ Q, 10).tolist()}")
for pt in [(0.3, -0.7), (2.0, 1.0)]:
    xv = np.array(pt); yv = Q.T @ xv
    print(f"  点 {pt}: f = {xv @ A @ xv:.6f},  {lam[0]:.0f}*y1^2+{lam[1]:.0f}*y2^2 = {lam[0]*yv[0]**2 + lam[1]*yv[1]**2:.6f}  (零差)")
print(f"  两种标准形: 配方 diag(2,3) vs 正交 diag(1,6) -> 正系数个数 p 都是 2 (惯性定理)")

print()
print("=== EXP4: Sylvester 顺序主子式 vs 特征值 对账 ===")
cases = [("正定        ", [[2, 2], [2, 5]]), ("不定        ", [[1, 2], [2, 1]]),
         ("负定        ", [[-2, 1], [1, -2]]), ("半正定(边界)  ", [[1, 1], [1, 1]]),
         ("坑:det>0负定 ", [[-1, 0], [0, -2]])]
for name, M in cases:
    M = np.array(M, dtype=float)
    d1, d2 = M[0, 0], np.linalg.det(M)
    ev = np.linalg.eigvalsh(M)
    print(f"  {name}: D1={d1:+.0f}, D2={d2:+.0f};  eigvals = {np.round(ev, 6).tolist()}")
print("  手算特征值: 不定{3,-1}; 负定{-1,-3}; 半正定{2,0}; 坑例{-1,-2}(det=2>0 仍负定)")

print()
print("=== EXP5: 3x3 正定例——[2,-1,0;-1,2,-1;0,-1,2] ===")
T3 = np.array([[2., -1., 0.], [-1., 2., -1.], [0., -1., 2.]])
print(f"  顺序主子式: D1={np.linalg.det(T3[:1, :1]):.0f}, D2={np.linalg.det(T3[:2, :2]):.0f}, D3={np.linalg.det(T3):.0f}  (手算 2,3,4)")
print(f"  eigvals = {np.round(np.linalg.eigvalsh(T3), 6).tolist()}  (手算 2-sqrt2, 2, 2+sqrt2)")

print()
print("=== EXP6: 水平集几何——椭圆/双曲线/平行线参数化 ===")
for t in [0.3, 1.1, 2.4]:
    yv = np.array([np.cos(t) / np.sqrt(lam[0]), np.sin(t) / np.sqrt(lam[1])])
    xv = Q @ yv
    print(f"  椭圆(主例) t={t}: x = {np.round(xv, 4).tolist()} -> f = {xv @ A @ xv:.10f}  (应=1)")
B = np.array([[1., 2.], [2., 1.]])
lb, Qb = np.linalg.eigh(B)                       # 升序 (-1, 3)
yv = np.array([np.sinh(0.8) / np.sqrt(abs(lb[0])), np.cosh(0.8) / np.sqrt(lb[1])])
print(f"  双曲线(不定) 一支: f = {(Qb @ yv) @ B @ (Qb @ yv):.10f}  (应=1)")
yv2 = np.array([-np.sinh(0.8) / np.sqrt(abs(lb[0])), np.cosh(0.8) / np.sqrt(lb[1])])
print(f"  双曲线(不定) 另一支: f = {(Qb @ yv2) @ B @ (Qb @ yv2):.10f}  (应=1)")
Cs = np.array([[1., 1.], [1., 1.]])
for a in [0.3, -0.7]:
    xv = np.array([a, 1.0 - a])
    print(f"  半正定 (x+y)^2: 点 {np.round(xv, 2).tolist()} -> f = {xv @ Cs @ xv:.10f}  (x+y=1 上, 应=1)")

print()
print("=== EXP7: 谱定理随机实测——对称 vs 非对称 ===")
n = 5
S = rng.normal(size=(n, n)); S = (S + S.T) / 2
ev, Qs = np.linalg.eigh(S)
print(f"  对称 5x5: Q L Q^T 重构误差 {np.abs(Qs @ np.diag(ev) @ Qs.T - S).max():.1e};"
      f"  Q^T Q - I 最大偏离 {np.abs(Qs.T @ Qs - np.eye(n)).max():.1e}: 特征值全实")
N = rng.normal(size=(n, n))
evn, V = np.linalg.eig(N)
print(f"  非对称 5x5: 特征值 = {np.round(evn, 3).tolist()}")
print(f"            特征向量矩阵 V^H V - I 最大偏离 = {np.abs(V.conj().T @ V - np.eye(n)).max():.3f}  (远非零: 一般不正交)")

print()
print("=== EXP8: 球面 Rayleigh 区间——11 讲幂法的理论依据 ===")
Sr = np.array([[2., 1.], [1., 2.]])
Z = rng.normal(size=(20000, 2)); Z = Z / np.linalg.norm(Z, axis=1, keepdims=True)
vals = np.einsum('ij,jk,ik->i', Z, Sr, Z)
print(f"  单位圆上 x^T S x 随机 2 万点: min = {vals.min():.6f}, max = {vals.max():.6f}")
print(f"  eigvalsh(S) = {np.linalg.eigvalsh(Sr).tolist()}  (1 与 3: 采样贴住上下界)")

print()
print("=== EXP9: A^T A 正定回收(15 讲拟合矩阵) ===")
A15 = np.array([[1., 0.], [1., 1.], [1., 2.], [1., 3.]])
AtA = A15.T @ A15
print(f"  A^T A = {AtA.tolist()}: D1 = {AtA[0, 0]:.0f}, D2 = {np.linalg.det(AtA):.0f}  (手算 4, 20: 正定)")
xr = rng.normal(size=2)
print(f"  恒等式数值: x^T(A^T A)x = {xr @ AtA @ xr:.6f};  ||A x||^2 = {np.linalg.norm(A15 @ xr)**2:.6f}  (零差)")
print(f"  eigvalsh(A^T A) = {np.round(np.linalg.eigvalsh(AtA), 6).tolist()}  (全正: 15 讲'碗底'唯一)")

print()
print(f"  TOTAL runtime: {time.perf_counter() - T0:.2f}s")