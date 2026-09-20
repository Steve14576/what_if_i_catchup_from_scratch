# lec14-01_verify_qr.py
# 第 14 讲验证脚本：Gram-Schmidt 手算全程、A=QR 装配、P=QQ^T 化简对账、
#                      相关向量检测、QR vs 正规方程稳定性对照(希尔伯特)、GS 数值漂移
# 规模纪律：小规模演示（手算例对照 + 4~6 阶希尔伯特 + 随机 5x3），目标 < 1 秒。

import time
import numpy as np

T0 = time.perf_counter()
rng = np.random.default_rng(14)

def gram_schmidt(A, modified=False):
    """经典/修正 Gram-Schmidt: 返回单位正交列 Q (遇零向量自动跳过)."""
    Q = []
    for j in range(A.shape[1]):
        e = A[:, j].astype(float).copy()
        if modified:
            for q in Q:
                e = e - (q @ e) * q        # 修正版: 逐步减, 用更新中的 e
        else:
            e = e - sum((q @ A[:, j]) * q for q in Q)  # 经典版: 一次性减, 用原始 a_j
        n = np.linalg.norm(e)
        if n < 1e-12:
            continue                        # 相关向量 -> 零向量 -> 跳过(剔冗余)
        Q.append(e / n)
    return np.column_stack(Q) if Q else np.zeros((A.shape[0], 0))

print("=== EXP1: 主例(13 讲老朋友) W=span{(1,1,0),(0,1,1)}——GS 手算全程对账 ===")
A = np.array([[1., 0.], [1., 1.], [0., 1.]])
e1 = A[:, 0]
e2 = A[:, 1] - (A[:, 1] @ e1) / (e1 @ e1) * e1
print(f"  e1 = (1,1,0);  e2 = (0,1,1) - (1/2)(1,1,0) = {e2}")
print(f"  正交验证: e1.e2 = {e1 @ e2:.0f}  (手算 -1/2+1/2 = 0)")
q1, q2 = e1/np.linalg.norm(e1), e2/np.linalg.norm(e2)
Q = np.column_stack([q1, q2])
R = np.array([[q1 @ A[:, 0], q1 @ A[:, 1]], [0., q2 @ A[:, 1]]])
print(f"  q1 = {np.round(q1, 4)}, q2 = {np.round(q2, 4)}  (手算 (-1,1,2)/sqrt6)")
print(f"  R =\n{np.round(R, 6)}  (手算 [[sqrt2, 1/sqrt2],[0, sqrt(3/2)]])")
print(f"  A = QR? max|A - Q@R| = {np.abs(A - Q @ R).max():.2e}")
P = Q @ Q.T
P13 = np.array([[2., 1., -1.], [1., 2., 1.], [-1., 1., 2.]]) / 3.
print(f"  P = Q Q^T 与 13 讲 A(A^TA)^-1A^T 对账: max 差 = {np.abs(P - P13).max():.2e}")
b = np.array([1., 2., 3.])
print(f"  P b = {np.round(P @ b, 6)}  (13 讲手算 (1/3, 8/3, 7/3))")

print()
print("=== EXP2: 3x3 例 A=[(1,0,1),(1,1,0),(0,1,1) 列] ===")
A3 = np.array([[1., 1., 0.], [0., 1., 1.], [1., 0., 1.]])
Q3 = gram_schmidt(A3, modified=True)
R3 = Q3.T @ A3
print(f"  Q3^T Q3 =\n{np.round(Q3.T @ Q3, 10)}  (单位正交)")
print(f"  R3 =\n{np.round(R3, 6)}")
print(f"  手算: q1=(1,0,1)/sqrt2, q2=(1,2,-1)/sqrt6, q3=(-1,1,1)/sqrt3")
print(f"  max|Q3 - 手算| = {np.abs(Q3 - np.array([[1., 1., -1.], [0., 2., 1.], [1., -1., 1.]]) / np.array([np.sqrt(2), np.sqrt(6), np.sqrt(3)])).max():.2e}"
      f"  (列符号可能整体差个负号)")
print(f"  A3 = QR? max|A3 - Q3@R3| = {np.abs(A3 - Q3 @ R3).max():.2e}")
print(f"  R3 上三角? 下三角部分 max|R3[下]| = {np.abs(np.tril(R3, -1)).max():.2e}")

print()
print("=== EXP3: np.linalg.qr 对照(LAPACK) ===")
Qn, Rn = np.linalg.qr(A3)
print(f"  与手跑 GS 的 Q 逐列符号对齐后 max 差 = "
      f"{max(np.abs(np.abs(Qn[:, j]) - np.abs(Q3[:, j])).max() for j in range(3)):.2e}")
print(f"  |Qn^T Qn - I| = {np.abs(Qn.T @ Qn - np.eye(3)).max():.2e}")

print()
print("=== EXP4: 相关向量检测——GS 遇零向量自动剔冗余(13 讲坑 2 兑现) ===")
Ac = np.array([[1., 2., 1.], [2., 4., 1.], [3., 6., 1.]])   # 列2 = 2*列1
Qc = gram_schmidt(Ac, modified=True)
print(f"  A 列数 3, rank = {np.linalg.matrix_rank(Ac)}, GS 产出正交向量 {Qc.shape[1]} 个")
print(f"  Qc^T Qc = I? max 差 = {np.abs(Qc.T @ Qc - np.eye(Qc.shape[1])).max():.2e}")
Rn2 = np.linalg.qr(Ac)[1]
print(f"  np.linalg.qr 的 R 对角元: {np.round(np.abs(np.diag(Rn2)), 6)}  (近 0 的对角元 = 冗余信号)")

print()
print("=== EXP5: P=QQ^T 化简对账(随机 5x3 列满秩) ===")
Ar = rng.normal(size=(5, 3))
Qr = gram_schmidt(Ar, modified=True)
lhs = Qr @ Qr.T
rhs = Ar @ np.linalg.inv(Ar.T @ Ar) @ Ar.T
print(f"  max|QQ^T - A(A^TA)^-1A^T| = {np.abs(lhs - rhs).max():.2e}  (两公式恒等)")

print()
print("=== EXP6: 稳定性对照——希尔伯特 4x4: QR 解 vs 正规方程解 ===")
def hilbert(n):
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])
H = hilbert(4)
x_true = np.ones(4)
bH = H @ x_true
Qh, Rh = np.linalg.qr(H)
x_qr = np.linalg.solve(Rh, Qh.T @ bH)                  # QR 路线: x = R^-1 Q^T b
x_ne = np.linalg.solve(H.T @ H, H.T @ bH)              # 正规方程路线
print(f"  真解 x = (1,1,1,1)")
print(f"  QR 解误差      ||x_qr - x|| = {np.linalg.norm(x_qr - x_true):.2e}")
print(f"  正规方程解误差 ||x_ne - x|| = {np.linalg.norm(x_ne - x_true):.2e}")
print(f"  两者差 {np.log10(max(np.linalg.norm(x_ne - x_true), 1e-300) / max(np.linalg.norm(x_qr - x_true), 1e-300)):.1f} 个数量级")

print()
print("=== EXP7: 经典 GS 数值漂移 vs 修正 GS vs LAPACK(正交性偏差) ===")
for n in [4, 6]:
    Hn = hilbert(n)
    Q_cl = gram_schmidt(Hn, modified=False)   # 经典 GS
    Q_mg = gram_schmidt(Hn, modified=True)    # 修正 GS
    Q_lap = np.linalg.qr(Hn)[0]               # Householder(LAPACK)
    dev = lambda Q: np.abs(Q.T @ Q - np.eye(Q.shape[1])).max()
    print(f"  Hilbert {n}x{n}: |Q^TQ-I| 经典 GS = {dev(Q_cl):.2e}, "
          f"修正 GS = {dev(Q_mg):.2e}, LAPACK = {dev(Q_lap):.2e}")

print()
print(f"  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
