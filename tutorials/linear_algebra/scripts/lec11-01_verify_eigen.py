# lec11-01_verify_eigen.py
# 第 11 讲验证脚本：特征值/特征向量全流程、det=Pi*lambda、迹=Sum*lambda、
#                      相似不改特征值、复特征值、重数(代数 vs 几何)、幂法
# 规模纪律：小规模演示（2x2 / 3x3 / 5x5 随机 + 12 步幂法），目标 < 1 秒。

import time
import numpy as np

T0 = time.perf_counter()
rng = np.random.default_rng(11)

print("=== EXP1: 主例手算核对——A=[2,1;1,2] 与 10 讲 B3 对账 ===")
A = np.array([[2., 1.], [1., 2.]])
lam, V = np.linalg.eig(A)
print(f"  eigenvalues = {np.round(np.sort(lam), 6)}  (手算: 3 与 1)")
# 特征向量核对: A v = lambda v
for l, v in zip(lam, V.T):
    print(f"  lambda={l:.4f}, v~{np.round(v/np.abs(v).max(), 3)}, |Av-lv| = {np.abs(A@v - l*v).max():.2e}")

print()
print("=== EXP2: 3x3 重根例 + 坏例——代数重数 vs 几何重数 ===")
A3 = np.array([[2., 1., 0.], [1., 2., 0.], [0., 0., 3.]])
lam3, _ = np.linalg.eig(A3)
print(f"  A3=[2,1,0;1,2,0;0,0,3] eigenvalues = {np.round(np.sort(lam3), 6)}  (手算: 1, 3, 3)")
r3 = np.linalg.matrix_rank(A3 - 3*np.eye(3))
print(f"  lambda=3: rank(A3-3I) = {r3} -> 几何重数 = 3-{r3} = 2 (代数 2, 不缺 -> 特征空间基 (1,1,0),(0,0,1))")
J = np.array([[3., 1.], [0., 3.]])
lamJ, _ = np.linalg.eig(J)
rJ = np.linalg.matrix_rank(J - 3*np.eye(2))
print(f"  坏例 J=[3,1;0,3] eigenvalues = {np.round(lamJ, 6)}; rank(J-3I) = {rJ} -> 几何重数 = 2-{rJ} = 1 < 代数 2 (缺口!)")

print()
print("=== EXP3: 两笔旧账——det = 特征值之积, 迹 = 特征值之和 ===")
for name, X in [("A(主例)", A), ("A3(3x3)", A3), ("随机5x5", rng.normal(size=(5, 5)))]:
    l = np.linalg.eig(X)[0]
    print(f"  {name:8s}: det = {np.linalg.det(X):+.6f}, Pi*lambda = {np.prod(l):+.6f}; "
          f"tr = {np.trace(X):+.6f}, Sum*lambda = {np.sum(l):+.6f}")
B0 = np.array([[1., 2.], [2., 4.]])
l0 = np.linalg.eig(B0)[0]
print(f"  det=0 例 [1,2;2,4]: eigenvalues = {np.round(np.sort(l0), 6)} (含 0 <-> det=0 <-> 奇异)")

print()
print("=== EXP4: 相似不改特征值(10 讲 EXP6 尾注的正式验收) ===")
A5 = rng.normal(size=(5, 5))
P5 = rng.normal(size=(5, 5)) + 5*np.eye(5)
B5 = np.linalg.inv(P5) @ A5 @ P5
la, lb = np.sort_complex(np.linalg.eig(A5)[0]), np.sort_complex(np.linalg.eig(B5)[0])
print(f"  5x5 随机: max|eig(A)-eig(P^-1AP)| = {np.abs(la - lb).max():.2e} (排序后逐个对照)")
# 剪切 vs I: 特征多项式相同却(后面证明)不相似
S = np.array([[1., 1.], [0., 1.]])
pS, pI = np.poly(S), np.poly(np.eye(2))
print(f"  剪切 vs I: 特征多项式系数 {np.round(pS,6)} vs {np.round(pI,6)} (相同!)")
print(f"             但剪切的特征向量全在 span{(1,0)} (几何重数 1), I 的特征向量到处都是")
print(f"             -> 特征多项式相同是相似的必要条件, 不是充分条件")

print()
print("=== EXP5: 复特征值——旋转矩阵 ===")
R90 = np.array([[0., -1.], [1., 0.]])
lamR, VR = np.linalg.eig(R90)
print(f"  R90 eigenvalues = {np.round(lamR, 6)}  (手算: +i 与 -i)")
a = np.deg2rad(37.)
R37 = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
lam37 = np.linalg.eig(R37)[0]
print(f"  R37 eigenvalues = {np.round(lam37, 6)}  (应约 cos37 +- i sin37 = {np.cos(a):.4f} +- {np.sin(a):.4f}i)")
for l, v in zip(lamR, VR.T):
    print(f"  验证 R90 v = lambda v: |R90v - lambda v| = {np.abs(R90@v - l*v).max():.2e} (v 为复向量)")

print()
print("=== EXP6: 幂法——反复施加 A, 主特征方向浮出水面 ===")
x = np.array([1., 0.])
print(f"  A=[2,1;1,2] 幂法 (x <- Ax/|Ax|), 初值 (1,0):")
for k in range(1, 13):
    y = A @ x
    x = y / np.linalg.norm(y)
    rho = x @ A @ x  # Rayleigh 商: 单位向量上的 x^T A x
    if k <= 6 or k == 12:
        print(f"    step {k:2d}: x ~ {np.round(x, 6)}, Rayleigh = {rho:.6f}")
print(f"  -> 收敛到 x=(1,1)/sqrt2 方向, Rayleigh -> 3 (= lambda_max)")
x = np.array([1., 0.])
M = np.array([[0., 1.], [1., 0.]])
print(f"  反射 M=[0,1;1,0] 同法迭代 (|lambda1|=|lambda2|=1, 无占优):")
for k in range(1, 7):
    y = M @ x
    x = y / np.linalg.norm(y)
    print(f"    step {k}: x = {np.round(x, 3)}  (在 (0,1),(1,0) 之间打转, 不收敛)")

print()
print("=== EXP7: 预告 12 讲——马尔可夫矩阵的稳态 ===")
Mk = np.array([[0.9, 0.2], [0.1, 0.8]])
lamM, _ = np.linalg.eig(Mk)
print(f"  Mk=[0.9,0.2;0.1,0.8] (列和=1): eigenvalues = {np.round(np.sort(lamM), 6)}  (手算: 1 与 0.7)")
x20 = np.linalg.matrix_power(Mk, 20) @ np.array([1., 0.])
print(f"  Mk^20 @ (1,0) = {np.round(x20, 6)}  (趋近稳态 (2/3, 1/3); 0.7^20={0.7**20:.2e} 已衰减)")
print(f"  -> lambda=1 的特征向量就是'反复施加后留下来'的稳态 (12 讲矩阵幂的主菜)")

print()
print(f"  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
