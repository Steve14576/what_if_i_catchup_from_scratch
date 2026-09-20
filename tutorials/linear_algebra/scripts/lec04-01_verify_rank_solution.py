# 规模纪律：纯 numpy，最大 3x3 / 3x4，目标 < 3 秒。
# 验证内容（秩与解的结构）：
#   A 取秩 1、n=3，零空间维数 = n - r = 2。
#   CASE1 齐次 Ax=0：给出手工零空间基 n1,n2，验证 A@n=0 且线性无关，秩-零化度对账。
#   CASE2 非齐次 Ax=b（相容）：给特解 p，验证通解 p + c1 n1 + c2 n2 仍解出 b（结构验证）。
#   CASE3 判定：b 不在列空间时 rank(A) < rank([A|b]) -> 无解。
import time
import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=4, suppress=True)

A = np.array([[1, 2, 3], [2, 4, 6], [1, 2, 3]], float)  # 行2=2*行1, 行3=行1 -> rank 1
r = np.linalg.matrix_rank(A)
n = A.shape[1]
print(f"A=\n{A}")
print(f"  rank(A)={r}, n={n}, 零空间维数应为 n-r={n - r}")

# 齐次 Ax=0 的解: x1 = -2 x2 - 3 x3, x2,x3 自由
n1 = np.array([-2, 1, 0], float)
n2 = np.array([-3, 0, 1], float)
print("\n=== CASE1 齐次 Ax=0 零空间基 ===")
print(f"  A@n1 = {A @ n1} (期望 0)")
print(f"  A@n2 = {A @ n2} (期望 0)")
print(f"  n1,n2 线性无关? rank([n1|n2])={np.linalg.matrix_rank(np.column_stack([n1, n2]))} (期望 2)")
print(f"  秩-零化度对账: r + (n-r) = {r} + {n - r} = {r + (n - r)} (期望 n={n})")

print("\n=== CASE2 非齐次 Ax=b 通解结构（相容）===")
b = np.array([1, 2, 1], float)  # 在列空间内 (b2=2*b1, b3=b1)
p = np.array([1, 0, 0], float)  # 特解
print(f"  rank(A)={r}, rank([A|b])={np.linalg.matrix_rank(np.column_stack([A, b]))} -> 相容")
print(f"  A@p = {A @ p} (期望 b={b})")
x_general = p + 2 * n1 - 1 * n2  # 任取 c1=2, c2=-1
print(f"  通解示例 p+2n1-n2 = {x_general}")
print(f"  A@(该通解) = {A @ x_general} (仍应=b={b})")

print("\n=== CASE3 b 不在列空间 -> 无解 ===")
b_bad = np.array([1, 0, 0], float)
rA = np.linalg.matrix_rank(A)
rAb = np.linalg.matrix_rank(np.column_stack([A, b_bad]))
print(f"  rank(A)={rA}, rank([A|b_bad])={rAb}, rank(A)<rank([A|b])? {rA < rAb} -> 无解")
print("  -> 齐次解集是过原点的子空间; 非齐次通解=特解+齐次解(平移的子空间)")

print(f"\n  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
