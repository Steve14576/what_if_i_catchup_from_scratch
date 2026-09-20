# 规模纪律：纯 numpy，最大 3x4 增广矩阵，目标 < 3 秒。
# 验证内容（高斯消元/行阶梯形/解的三种命运）：
#   CASE1 唯一解：REF + 回代，解应=(1,2,3)
#   CASE2 无穷解：出现全零行且相容，自由变量个数=n-主元数=1
#   CASE3 无解：出现 [0 0 0 | 非零] 即 0=1，rank(A) < rank([A|b])
#   并统一用秩判据 rank(A)==rank([A|b]) 复核相容性（Frobenius 定理）。
import time
import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=4, suppress=True)


def rref(M, tol=1e-9):
    """把增广矩阵 M 化为简化行阶梯形，返回 (R, pivot_cols)。"""
    M = M.astype(float).copy()
    rows, cols = M.shape
    r = 0
    pivots = []
    for c in range(cols):
        piv = np.argmax(np.abs(M[r:, c])) + r
        if abs(M[piv, c]) < tol:
            continue
        M[[r, piv]] = M[[piv, r]]
        M[r] = M[r] / M[r, c]
        for i in range(rows):
            if i != r:
                M[i] -= M[i, c] * M[r]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return M, pivots


def classify(A, b, name):
    n = A.shape[1]
    rA = np.linalg.matrix_rank(A)
    aug = np.column_stack([A, b])
    rAb = np.linalg.matrix_rank(aug)
    R, piv = rref(aug)
    print(f"--- {name}: rank(A)={rA} rank([A|b])={rAb} 主元列={piv}")
    print("  RREF([A|b]) =\n", R)
    if rA != rAb:
        print("  -> 无解（不相容，rA < rA|b）")
    elif rA == n:
        sol = R[:, -1]
        print(f"  -> 唯一解 x={sol}")
    else:
        print(f"  -> 无穷多解，自由变量个数 = n - r = {n - rA}")
    return rA, rAb


print("=== CASE1 唯一解 ===")
A1 = np.array([[1, 1, 1], [2, 3, 1], [1, -2, 3]])
b1 = np.array([6, 11, 6])
classify(A1, b1, "唯一")  # 期望 (1,2,3)

print("\n=== CASE2 无穷解（第2行=2*第1行，相容）===")
A2 = np.array([[1, 2, 3], [2, 4, 6], [1, 1, 1]])
b2 = np.array([6, 12, 3])
classify(A2, b2, "无穷")  # 自由变量 1 个

print("\n=== CASE3 无解（第3行LHS=前两行之和，RHS对不上）===")
A3 = np.array([[1, 1, 1], [1, 2, 2], [2, 3, 3]])
b3 = np.array([3, 5, 7])
classify(A3, b3, "无解")  # 0 = 非零

# 交叉核对 CASE1 解回代
x1 = np.array([1.0, 2.0, 3.0])
print("\n  [check] A1 @ (1,2,3) ==", A1 @ x1, " (期望", b1, ")")
print("  -> 三例分别演示 唯一/无穷/无解；秩判据 rank(A)==rank([A|b]) 与阶梯形一致")

print(f"\n  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
