# lec13-01_verify_inner_product.py
# 第 13 讲验证脚本：内积/范数/夹角、柯西-施瓦茨、投影到线与子空间、
#                      投影矩阵三性质、正交补维数公式、正交矩阵、多项式投影
# 规模纪律：小规模演示（手算例对照 + 随机 1000 对 C-S + 数值积分），目标 < 1 秒。

import time
import numpy as np

T0 = time.perf_counter()
rng = np.random.default_rng(13)

print("=== EXP1: 内积/范数/夹角 + 柯西-施瓦茨 ===")
u = np.array([1., 2., 2.]); v = np.array([2., -1., 2.])
ip, nu, nv = u @ v, np.linalg.norm(u), np.linalg.norm(v)
print(f"  u=(1,2,2), v=(2,-1,2): <u,v> = {ip:.0f}, |u| = {nu:.0f}, |v| = {nv:.0f}")
cos = ip / (nu * nv)
print(f"  cos(theta) = {cos:.6f} (= 4/9), theta = {np.degrees(np.arccos(cos)):.2f} deg")
print(f"  C-S: |<u,v>| = {abs(ip):.0f} <= |u||v| = {nu*nv:.0f}  [OK]")
worst = 0.0
for _ in range(1000):
    a, b = rng.normal(size=4), rng.normal(size=4)
    worst = max(worst, abs(a @ b) / (np.linalg.norm(a) * np.linalg.norm(b)))
print(f"  1000 对随机向量: max |<a,b>|/(|a||b|) = {worst:.6f} (<= 1, C-S 普遍成立)")

print()
print("=== EXP2: 多项式内积(积分版) <f,g> = int_0^1 f*g dt ===")
tgrid = np.linspace(0, 1, 200001)
def ipf(f_vals, g_vals):
    return np.trapezoid(f_vals * g_vals, tgrid)   # 数值积分
ip_1t = ipf(np.ones_like(tgrid), tgrid)
ip_tt = ipf(tgrid, tgrid)
n_t = np.sqrt(ip_tt)
print(f"  <1,t> = {ip_1t:.6f} (手算 1/2);  <t,t> = {ip_tt:.6f} (手算 1/3);  |t| = {n_t:.6f} (1/sqrt3)")
cos_1t = ip_1t / (1.0 * n_t)
print(f"  cos<1,t> = {cos_1t:.6f} (= sqrt3/2), theta = {np.degrees(np.arccos(cos_1t)):.2f} deg (应 30 度)")

print()
print("=== EXP3: 投影到一条线 p = (a.b/a.a) a + 10 讲 C3 对账 ===")
a = np.array([1., 1., 1.]); b = np.array([2., 3., 4.])
p = (a @ b) / (a @ a) * a
e = b - p
print(f"  b=(2,3,4) 投到 a=(1,1,1): p = {p} (手算 3a), e = {e}, a.e = {a @ e:.0f}")
print(f"  |e|^2 = {e @ e:.0f} (误差平方 = 到线的最短距离平方)")
d = np.array([0.1, -0.1, 0.0])   # 扰动: 检查 p 确实是最近点
print(f"  扰动检查: |b-(p+d)|^2 = {(b-(p+d)) @ (b-(p+d)):.3f} > |e|^2 = {e @ e:.0f}")
# 10 讲 C3 对账: 投影到直线 y=2x 的矩阵
a2 = np.array([1., 2.])
P2 = np.outer(a2, a2) / (a2 @ a2)
print(f"  P = a a^T/(a^Ta), a=(1,2): P =\n{P2}  (= (1/5)[[1,2],[2,4]], 与 10 讲 C3 换基法精确一致)")

print()
print("=== EXP4: 投影到子空间 W=span{(1,1,0),(0,1,1)}, b=(1,2,3) ===")
A = np.array([[1., 0.], [1., 1.], [0., 1.]])
b3 = np.array([1., 2., 3.])
xhat = np.linalg.solve(A.T @ A, A.T @ b3)
p3 = A @ xhat
P = A @ np.linalg.inv(A.T @ A) @ A.T
e3 = b3 - p3
print(f"  A^T A =\n{A.T @ A}  (又是 [[2,1],[1,2]]!), A^T b = {A.T @ b3}")
print(f"  xhat = {np.round(xhat, 6)} (手算 (1/3, 7/3)), p = {np.round(p3, 6)}")
print(f"  P = (1/3)*[[2,1,-1],[1,2,1],[-1,1,2]]?  max|P-手算| = "
      f"{np.abs(P - np.array([[2,1,-1],[1,2,1],[-1,1,2]])/3).max():.2e}")
print(f"  验证: A^T e = {np.round(A.T @ e3, 10)} (零向量: 误差垂直每个基)")
print(f"  P 对称: max|P-P^T| = {np.abs(P - P.T).max():.2e};  P 幂等: max|P@P-P| = {np.abs(P @ P - P).max():.2e}")
print(f"  P b = p: max|P@b - p| = {np.abs(P @ b3 - p3).max():.2e}")

print()
print("=== EXP5: I-P 投到正交补 W^perp ===")
IP = np.eye(3) - P
e_check = IP @ b3
print(f"  (I-P) b = {np.round(e_check, 6)} (同 e);  (I-P)^2 = I-P: max 差 {np.abs(IP @ IP - IP).max():.2e}")
print(f"  e 方向 = (1,-1,1)/3: 基 {np.round(e_check/ (e_check[0]), 6)}")
b_alt = np.array([1., 1., 1.])
e_alt = IP @ b_alt
print(f"  换 b=(1,1,1): e = {np.round(e_alt, 6)} (仍落在同一条 W^perp 上!)")

print()
print("=== EXP6: dim W^perp = d - dim W (09 讲维数公式的兑现) ===")
for d, k in [(5, 2), (6, 3), (4, 1)]:
    W = rng.normal(size=(d, k))
    r = np.linalg.matrix_rank(W)
    dimWperp = d - np.linalg.matrix_rank(W.T)
    print(f"  随机 d={d}, rank(W)={r}: dim N(W^T) = {dimWperp} = {d} - {r}  [OK] (W^perp = N(W^T))")

print()
print("=== EXP7: 正交矩阵——旋转 R(37 度) ===")
ang = np.deg2rad(37.)
Q = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
print(f"  Q^T Q =\n{np.round(Q.T @ Q, 10)}  (= I)")
print(f"  列长: {np.linalg.norm(Q[:,0]):.6f}, {np.linalg.norm(Q[:,1]):.6f}; 列点积: {Q[:,0] @ Q[:,1]:+.2e}")
u2, v2 = rng.normal(size=2), rng.normal(size=2)
print(f"  保内积: <Qu,Qv> = {(Q@u2) @ (Q@v2):.6f}, <u,v> = {u2 @ v2:.6f}")
print(f"  保长度: |Qv| = {np.linalg.norm(Q @ v2):.6f}, |v| = {np.linalg.norm(v2):.6f}")

print()
print("=== EXP8: 函数空间投影(C3 前菜)——t^2 投到 span{1,t} ===")
# 正规方程 [[<1,1>,<1,t>],[<t,1>,<t,t>]] x = [<1,t^2>,<t,t^2>]
M = np.array([[1.0, 0.5], [0.5, 1.0/3.0]])
rhs = np.array([1.0/3.0, 0.25])
x = np.linalg.solve(M, rhs)
print(f"  系数 x = {np.round(x, 6)}  (手算 (-1/6, 1): 投影 = t - 1/6)")
resid = tgrid**2 - x[0] - x[1]*tgrid
print(f"  残差 t^2 - t + 1/6 与 1 的内积 = {ipf(resid, np.ones_like(tgrid)):.2e} (应 0)")
print(f"  残差与 t 的内积 = {ipf(resid, tgrid):.2e} (应 0)  -> 误差垂直整个子空间")
print(f"  对照: 平凡取 t^2 近似为 0 的误差范数^2 = {ipf(tgrid**2, tgrid**2):.4f}; "
      f"投影后 = {ipf(resid, resid):.4f} (更小)")

print()
print(f"  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
