# lec17-01_verify_svd.py
# 第 17 讲验证脚本：从 A^T A 构造 SVD、旋转-缩放-旋转、非方阵 full/economy、
#                   奇异值 vs 特征值、四子空间正交基、低秩逼近(Eckart-Young)、
#                   伪逆(第 15 讲牌位闭环)、随机对照、条件数预告
# 规模纪律：2x2/3x2/3x4 手算例 + 随机 4x6 + 64x64 合成图，目标 < 1 秒。

import time
import numpy as np

T0 = time.perf_counter()
rng = np.random.default_rng(17)

print("=== EXP1: 主例 A=[[2,2],[-1,1]] -- 从 A^T A 构造 SVD ===")
A = np.array([[2., 2.], [-1., 1.]])
AtA = A.T @ A
print(f"  A^T A = {AtA.tolist()}  (手算 [[5,3],[3,5]])")
lam, V = np.linalg.eigh(AtA)                 # 升序
print(f"  eigvals(A^T A) = {np.round(lam, 10).tolist()}  (手算 2, 8)")
sig = np.sqrt(lam[::-1])                     # 降序
V = V[:, ::-1]                               # 列序也改降序
print(f"  sigma = sqrt(eig) 降序 = {np.round(sig, 6).tolist()}  (手算 2*sqrt2=2.828427, sqrt2=1.414214)")
U = A @ V / sig                              # u_i = A v_i / sigma_i
print(f"  V = {np.round(V, 6).tolist()}")
print(f"  U = A V / sigma = {np.round(U, 6).tolist()}  (实测为 I; 符号组合与 V 配对联动, 不唯一)")
U_np, s_np, Vt_np = np.linalg.svd(A)         # 内置对照
print(f"  numpy svd 内置: s = {np.round(s_np, 6).tolist()}  (与手算同)")
print(f"  ||U^T U - I|| = {np.abs(U.T @ U - np.eye(2)).max():.1e};  ||V^T V - I|| = {np.abs(V.T @ V - np.eye(2)).max():.1e}")
recon = U @ np.diag(sig) @ V.T
print(f"  ||U S V^T - A||max = {np.abs(recon - A).max():.1e}  (重构零差)")
print(f"  det A = {np.linalg.det(A):.6f};  sigma1*sigma2 = {sig[0]*sig[1]:.6f}  (05 讲回收: |det| = prod sigma)")

print()
print("=== EXP2: 几何 -- 旋转-缩放-旋转 (V^T -> S -> U) ===")
for nm, xv in [("x = v1 (右奇异向量1)", V[:, 0]), ("x = v2", V[:, 1])]:
    w1 = V.T @ xv
    w2 = np.diag(sig) @ w1
    w3 = U @ w2
    print(f"  {nm}: ||V^T x|| = {np.linalg.norm(w1):.6f} -> ||S V^T x|| = {np.linalg.norm(w2):.6f} -> ||A x|| = {np.linalg.norm(w3):.6f}")
Z = rng.normal(size=(20000, 2)); Z = Z / np.linalg.norm(Z, axis=1, keepdims=True)
norms = np.linalg.norm(Z @ A.T, axis=1)
print(f"  单位圆 2 万点: ||A x|| 范围 = [{norms.min():.6f}, {norms.max():.6f}]  (贴住 [sigma2, sigma1])")
w1s = Z @ V
print(f"  V^T 保长度: ||V^T x|| - 1 最大偏离 = {np.abs(np.linalg.norm(w1s, axis=1) - 1).max():.1e}")

print()
print("=== EXP3: 非方阵 3x2 -- full 与 economy 两种 SVD ===")
B = np.array([[1., 1.], [0., 1.], [1., 0.]])
BtB = B.T @ B
print(f"  B^T B = {BtB.tolist()}  (手算 [[2,1],[1,2]]);  eigvals = {np.linalg.eigvalsh(BtB).tolist()}  (手算 1, 3)")
Uf, sf, Vtf = np.linalg.svd(B, full_matrices=True)
Ue, se, Vte = np.linalg.svd(B, full_matrices=False)
print(f"  full:    U {Uf.shape}, S {sf.shape}, V^T {Vtf.shape}")
print(f"  economy: U {Ue.shape}, S {se.shape}, V^T {Vte.shape}")
print(f"  sigma = {np.round(sf, 6).tolist()}  (手算 sqrt3=1.732051, 1)")
Sfull = np.vstack([np.diag(sf), np.zeros((1, 2))])
print(f"  full Sigma 3x2 = {np.round(Sfull, 6).tolist()}")
print(f"  full    重构零差 = {np.abs(Uf @ Sfull @ Vtf - B).max():.1e}")
print(f"  economy 重构零差 = {np.abs(Ue @ np.diag(se) @ Vte - B).max():.1e}")
u3 = Uf[:, 2]
print(f"  补全的 u3 = {np.round(u3, 6).tolist()}  (手算 (1,-1,-1)/sqrt3 = (0.577350,-0.577350,-0.577350), 符号可反)")
print(f"  ||B^T u3|| = {np.linalg.norm(B.T @ u3):.1e}  (u3 在左零空间: 与列空间正交)")

print()
print("=== EXP4: 奇异值 vs 特征值 -- 三个对照 ===")
cases = [("非对称 nilpotent [[0,2],[0,0]]", np.array([[0., 2.], [0., 0.]])),
         ("对称        [[2,1],[1,2]]", np.array([[2., 1.], [1., 2.]])),
         ("剪切        [[1,3],[0,1]]", np.array([[1., 3.], [0., 1.]]))]
for nm, M in cases:
    ev = np.linalg.eigvals(M)
    sv = np.linalg.svd(M, compute_uv=False)
    print(f"  {nm}: eig = {np.round(ev, 6).tolist()}, sigma = {np.round(sv, 6).tolist()}")
print(f"  读法: nilpotent 特征值全 0 但 sigma=(2,0) 把圆拍成线段; 对称时 sigma=|eig|; 剪切 eig=(1,1) '没拉伸'是假象")
print(f"  剪切例 kappa = sigma1/sigma2 = {np.linalg.cond(cases[2][1]):.6f}  (20 讲预告: 条件数=SVD 视角)")

print()
print("=== EXP5: 四个基本子空间的正交基一次配齐 (09 讲回收) ===")
C = np.array([[1., 2., 0., 1.], [0., 1., 1., 0.], [1., 3., 1., 1.]])   # rank 2 (row3 = row1 + row2)
Uc, sc, Vtc = np.linalg.svd(C, full_matrices=True)
r = int((sc > 1e-12).sum())
print(f"  rank = {r};  sigma = {np.round(sc, 6).tolist()}  (第 3 个为 0: 3x4 秩 2, s 只给 min(m,n)=3 个)")
print(f"  ||C v3|| = {np.linalg.norm(C @ Vtc[2]):.1e},  ||C v4|| = {np.linalg.norm(C @ Vtc[3]):.1e}  (v3,v4 = 零空间正交基, n-r=2)")
print(f"  ||C^T u3|| = {np.linalg.norm(C.T @ Uc[:, 2]):.1e}  (u3 = 左零空间正交基, m-r=1)")
print(f"  rank-nullity 对账: r + dim N(C) = {r} + {4-r} = 4")

print()
print("=== EXP6: 低秩逼近与 Eckart-Young ===")
xa = np.arange(64.); xb = np.arange(64.)
img = (0.7 * np.outer(np.sin(np.pi * xa / 8), np.cos(np.pi * xb / 12))
       + 0.4 * np.outer(np.sin(np.pi * xa / 24), np.sin(np.pi * xb / 6))
       + 0.15 * rng.normal(size=(64, 64)))
Uim, sim, Vtim = np.linalg.svd(img)
print(f"  合成图 64x64: 前 6 个 sigma = {np.round(sim[:6], 4).tolist()}")
print(f"  读法: 前两个 = 两个正弦分量(各精确 rank1); 尾部 = 噪声平台 (谱断崖)")
for k in [1, 2, 4, 8, 16]:
    approx = Uim[:, :k] @ np.diag(sim[:k]) @ Vtim[:k, :]
    err_formula = np.sqrt((sim[k:] ** 2).sum())
    print(f"  rank-{k}: ||img - img_k||_F = {np.linalg.norm(img - approx):.4f}  = sqrt(sum_{{i>{k}}} sigma_i^2) = {err_formula:.4f}")
base2 = Uim[:, :2] @ np.diag(sim[:2]) @ Vtim[:2, :]
e_opt = np.linalg.norm(img - base2)
best_rand = 1e9
for _ in range(200):
    P = rng.normal(size=(64, 2)); Q = rng.normal(size=(2, 64))
    best_rand = min(best_rand, np.linalg.norm(img - P @ Q))
print(f"  Eckart-Young 采样检验: 最优 rank-2 误差 = {e_opt:.4f};  200 个随机 rank-2 的最小误差 = {best_rand:.4f}  (全部更大)")
print(f"  存储账: 全存 64x64 = {64*64} 个数; rank-2 只需 2*(64+64+1) = {2*(64+64+1)} 个数")

print()
print("=== EXP7: 伪逆 -- 第 15 讲牌位揭幕 ===")
Ap = np.linalg.pinv(A)
print(f"  A^+ (主例) = {np.round(Ap, 6).tolist()}  (手算 [[1/4,-1/2],[1/4,1/2]] = A^(-1))")
print(f"  ||A^+ - inv(A)||max = {np.abs(Ap - np.linalg.inv(A)).max():.1e}  (满秩方阵: 伪逆工程退化回逆, 06 讲对账)")
Rm = rng.normal(size=(4, 3)); Rp = np.linalg.pinv(Rm)
print(f"  随机 4x3, 四条 Moore-Penrose 性质:")
print(f"    ||A A^+ A - A||      = {np.abs(Rm @ Rp @ Rm - Rm).max():.1e}")
print(f"    ||A^+ A A^+ - A^+||  = {np.abs(Rp @ Rm @ Rp - Rp).max():.1e}")
print(f"    ||(A A^+)^T - A A^+||= {np.abs((Rm @ Rp).T - Rm @ Rp).max():.1e}")
print(f"    ||(A^+ A)^T - A^+ A||= {np.abs((Rp @ Rm).T - Rp @ Rm).max():.1e}")
D15 = np.array([[1., 1.], [1., 1.]]); b15 = np.array([2., 0.])
xd = np.linalg.pinv(D15) @ b15
print(f"  15 讲坑例 A=[[1,1],[1,1]], b=(2,0): A^+ b = {np.round(xd, 6).tolist()}  (最短解 (0.5,0.5))")
for xc in [(0.5, 0.5), (1., 0.), (0., 1.)]:
    print(f"    解 {xc}: ||x|| = {np.linalg.norm(xc):.6f},  ||A x - b|| = {np.linalg.norm(D15 @ np.array(xc) - b15):.6f}")
A46 = np.array([[1., 0.], [1., 1.], [1., 2.], [1., 3.]])
b46 = np.array([1., 2., 2., 4.])
x_pinv = np.linalg.pinv(A46) @ b46
x_ne = np.linalg.solve(A46.T @ A46, A46.T @ b46)
print(f"  超定例: A^+ b = {np.round(x_pinv, 6).tolist()};  正规方程解 = {np.round(x_ne, 6).tolist()}  (同一解)")
e46 = b46 - A46 @ x_pinv
print(f"  A^T e = {np.round(A46.T @ e46, 10).tolist()}  (最小二乘自检: 误差垂直列空间)")

print()
print("=== EXP8: 随机对照 -- SVD 对任何矩阵都成立 ===")
Mrand = rng.normal(size=(4, 6))
Ur, sr, Vtr = np.linalg.svd(Mrand)
print(f"  4x6 随机: U^T U - I = {np.abs(Ur.T @ Ur - np.eye(4)).max():.1e};  V^T V - I = {np.abs(Vtr @ Vtr.T - np.eye(6)).max():.1e}")
Sr = np.hstack([np.diag(sr), np.zeros((4, 2))])
print(f"  Sigma 4x6 带零列;  重构零差 = {np.abs(Ur @ Sr @ Vtr - Mrand).max():.1e}")
print(f"  sigma 非负降序: {bool(np.all(sr >= 0) and np.all(np.diff(sr) <= 0))}")
specAtA = np.sqrt(np.clip(np.sort(np.linalg.eigvalsh(Mrand.T @ Mrand))[::-1], 0, None))
print(f"  A^T A 的 6 个谱开根号 = {np.round(specAtA, 6).tolist()}")
print(f"  (前 4 个 = sigma, 后 2 个 ~ 0: 与 A A^T 的非零谱一致)")

print()
print(f"  TOTAL runtime: {time.perf_counter() - T0:.2f}s")