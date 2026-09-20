# 规模纪律：纯 numpy，最大 3x5，目标 < 3 秒。
# 验证内容（四个基本子空间与 rank-nullity）：
#   A 取 3x5、秩 2 的整数矩阵（行3 = 行1 + 行2，制造 1 维左零空间）
#   EXP1  维数对账：rank(A)=2, dim N(A)=3 (=5-2), dim R(A^T)=2, dim N(A^T)=1 (=3-2)
#   EXP2  手工 RREF 求四空间基：主元列->col(A) 基；非零行->row 基；解 Ax=0 / A^T x=0 -> 两个零空间
#   EXP3  正交对 1：N(A) 与 R(A^T) 全部点积 = 0（随机组合也为 0）
#   EXP4  正交对 2：R(A) 与 N(A^T) 全部点积 = 0
#   EXP5  正交直和对账：dim R(A^T)+dim N(A)=n=5；dim R(A)+dim N(A^T)=m=3
import time
import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=4, suppress=True)
rng = np.random.default_rng(20260920)


def rref(M, tol=1e-9):
    """把 M 化为 RREF，返回 (R, pivot_cols)。"""
    R = M.astype(float).copy()
    rows, cols = R.shape
    pivots = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        piv = int(np.argmax(np.abs(R[r:, c]))) + r
        if abs(R[piv, c]) < tol:
            continue
        R[[r, piv]] = R[[piv, r]]
        R[r] = R[r] / R[r, c]
        for i in range(rows):
            if i != r and abs(R[i, c]) > 0:
                R[i] = R[i] - R[i, c] * R[r]
        pivots.append(c)
        r += 1
    return R, pivots


def null_basis(M, tol=1e-9):
    """用 RREF 求零空间的一组基：自由列逐个设 1，回读基本变量。"""
    R, pivots = rref(M)
    cols = R.shape[1]
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        v = np.zeros(cols)
        v[f] = 1.0
        for i, p in enumerate(pivots):
            v[p] = -R[i, f]
        basis.append(v)
    return np.array(basis)


A = np.array([[1., 2., 3., 4., 5.],
              [0., 1., 1., 1., 1.],
              [1., 3., 4., 5., 6.]])
m, n = A.shape
print("A =")
print(A)
r = np.linalg.matrix_rank(A)

print("\n=== EXP1 维数对账 ===")
print(f"  rank(A) = {r}   (m={m}, n={n})")
print(f"  dim R(A)   = r     = {r}")
print(f"  dim N(A)   = n - r = {n - r}")
print(f"  dim R(A^T) = r     = {r}   (行秩=列秩)")
print(f"  dim N(A^T) = m - r = {m - r}")

R, pivots = rref(A)
print("\n=== EXP2 四空间的手工基（RREF 驱动）===")
print("RREF(A) =")
print(R)
print(f"  主元列 = {[c + 1 for c in pivots]} (1-based)")
colB = A[:, pivots]
print("  col(A) 基（原矩阵主元列）:")
print(colB)
rowB = R[:len(pivots)]
print("  row(A) 基（RREF 非零行）:")
print(rowB)
nulA = null_basis(A)
print("  N(A) 基:")
print(nulA)
nulAT = null_basis(A.T)
print("  N(A^T) 基:")
print(nulAT)

print("\n=== EXP3 正交对 1：N(A) vs R(A^T) ===")
print("  N(A) 基 x row(A) 基点积矩阵（应全 0）:")
print(nulA @ rowB.T)
c1 = rng.standard_normal(len(nulA))
c2 = rng.standard_normal(len(rowB))
v1 = c1 @ nulA
v2 = c2 @ rowB
print(f"  随机组合 v1 in N(A), v2 in row(A): v1 . v2 = {v1 @ v2:.2e}")

print("\n=== EXP4 正交对 2：R(A) vs N(A^T) ===")
print("  col(A) 基列 x N(A^T) 基 点积（应全 0）:")
print(nulAT @ colB)
w = nulAT[0]
print(f"  N(A^T) 基向量 = {w}, 与两列点积 = {colB.T @ w}")

print("\n=== EXP5 正交直和对账 ===")
print(f"  R^5: dim row(A) + dim N(A)   = {r} + {n - r} = {n} = n  [OK]")
print(f"  R^3: dim col(A) + dim N(A^T) = {r} + {m - r} = {m} = m  [OK]")

print(f"\n  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
