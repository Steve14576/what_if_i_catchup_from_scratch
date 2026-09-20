# 规模纪律：纯 numpy，最大 3x3 [A|I]，目标 < 3 秒。
# 验证内容（逆矩阵 inverse）：
#   EXP1  2x2 公式法 A^-1 = 1/det * [d -b; -c a]，验证 A@Ainv=I（及 Ainv@A=I）
#   EXP2  3x3 高斯-若尔当 [A|I]->[I|A^-1] 全程化出（整数解），对照 np.linalg.inv，验证 A@Ainv=I
#   EXP3  (AB)^-1 == B^-1 A^-1（反序），且 != A^-1 B^-1（一般）
#   EXP4  奇异矩阵求逆 -> numpy 报错（LinAlgError）信息
#   EXP5  (A^-1)^T == (A^T)^-1；det(A^-1)==1/det(A)
#   EXP6  x = A^-1 b 确实是 Ax=b 的解（回代核对）
import time
import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=4, suppress=True)


def rref_ai(A):
    """把 [A|I] 化为 [I|Ainv]。返回 Ainv（若奇异返回 None 语义由奇异处理）。"""
    n = A.shape[0]
    M = np.column_stack([A.astype(float), np.eye(n)])
    for c in range(n):
        piv = np.argmax(np.abs(M[c:, c])) + c
        if abs(M[piv, c]) < 1e-12:
            return None
        M[[c, piv]] = M[[piv, c]]
        M[c] = M[c] / M[c, c]
        for i in range(n):
            if i != c:
                M[i] -= M[i, c] * M[c]
    return M[:, n:]


print("=== EXP1 2x2 公式法 ===")
A = np.array([[3.0, 1.0], [2.0, 4.0]])
detA = A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]  # =10
Ainv_hand = np.array([[4.0, -1.0], [-2.0, 3.0]]) / detA
print(f"  detA={detA}, Ainv(手算公式)={Ainv_hand.tolist()}")
print(f"  A@Ainv={A @ Ainv_hand} (期望 I)")
print(f"  Ainv@A={Ainv_hand @ A} (期望 I, 双边验证)")
print(f"  Ainv(numpy)={np.linalg.inv(A).tolist()}")

print("\n=== EXP2 3x3 高斯-若尔当 [A|I] ===")
A3 = np.array([[1.0, 2.0, 3.0], [0.0, 1.0, 4.0], [5.0, 6.0, 0.0]])
Ainv3 = rref_ai(A3)
print(f"  [A|I] 化出的 A^-1 = {Ainv3.tolist()}")
print(f"  A@Ainv = \n{A3 @ Ainv3.round(6)}")
print(f"  numpy inv = {np.linalg.inv(A3).tolist()}")

print("\n=== EXP3 (AB)^-1 反序 ===")
B = np.array([[2.0, 0.0], [1.0, 3.0]])
P = np.array([[3.0, 1.0], [2.0, 4.0]])
BP = B @ P
print(f"  (BP)^-1={np.linalg.inv(BP).tolist()}")
print(f"  P^-1@B^-1={np.linalg.inv(P) @ np.linalg.inv(B)}  (应相等)")
print(f"  B^-1@P^-1={np.linalg.inv(B) @ np.linalg.inv(P)}  (一般不等)")
print(f"  相等? allclose(B^-1A^-1): {np.allclose(np.linalg.inv(BP), np.linalg.inv(P) @ np.linalg.inv(B))}")

print("\n=== EXP4 奇异矩阵求逆报错 ===")
S = np.array([[1.0, 2.0], [2.0, 4.0]])
try:
    np.linalg.inv(S)
    print("  (异常：没报错)")
except np.linalg.LinAlgError as e:
    print(f"  LinAlgError: {e}")

print("\n=== EXP5 (A^-1)^T == (A^T)^-1；det(A^-1) == 1/det A ===")
print(f"  相等? {np.allclose(np.linalg.inv(A3).T, np.linalg.inv(A3.T))}")
print(f"  det(A^-1)={np.linalg.det(np.linalg.inv(A3)):.6f}, 1/detA={1 / np.linalg.det(A3):.6f}")

print("\n=== EXP6 x = A^-1 b 解 Ax=b ===")
b = np.array([6.0, 11.0, 6.0])  # 凑 A3 的列组合
x = np.linalg.inv(A3) @ b
print(f"  x={x}"); print(f"  A@x={A3 @ x} (期望 b={b})")

print(f"\n  TOTAL runtime: {time.perf_counter() - T0:.2f}s")