# 规模纪律：纯 numpy 2x2/3x3 矩阵乘法与转置验证，目标 < 3 秒。
# 验证内容：
#   EXP1  旋转矩阵：R(a) @ R(b) == R(a+b)  —— 矩阵乘法 = 变换的先后复合
#   EXP2  一个旋转 R 与一个非均匀缩放 S：R@S != S@R —— 矩阵乘法不交换
#   EXP3  转置反序律：(A@B).T == B.T @ A.T
#   EXP4  单位阵：A @ I == A
#   EXP5  用具体 3x3 手工对照一个矩阵向量乘（行 x 列），核对结果
import time
import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=4, suppress=True)


def rot(deg):
    th = np.radians(deg)
    return np.array([[np.cos(th), -np.sin(th)],
                     [np.sin(th),  np.cos(th)]])


print("=== EXP1: R(30)@R(60) == R(90) (composition = multiply) ===")
R30, R60, R90 = rot(30), rot(60), rot(90)
print("R(30)@R(60)=\n", R30 @ R60)
print("R(90)=\n", R90)
print("  allclose:", np.allclose(R30 @ R60, R90))
# 对一支具体向量验证：先转30度再转60度 = 转90度
v = np.array([1.0, 0.0])
print("  v=(1,0) -> R30@R60@v =", R30 @ R60 @ v, " R90@v =", R90 @ v)

print("\n=== EXP2: R(90)@S vs S@R (rotation x non-uniform scale, NOT commute) ===")
S = np.array([[2.0, 0.0], [0.0, 1.0]])  # x 方向放大 2 倍
print("R(90)@S=\n", R90 @ S)
print("S@R(90)=\n", S @ R90)
print("  equal?", np.allclose(R90 @ S, S @ R90), " (expect False)")

print("\n=== EXP3: (A@B).T == B.T @ A.T ===")
A = np.array([[1, 2, 3], [4, 5, 6]], dtype=float)   # 2x3
B = np.array([[0, 1], [1, 1], [2, 0]], dtype=float)  # 3x2
print("  (A@B).T == B.T@A.T ?", np.allclose((A @ B).T, B.T @ A.T))

print("\n=== EXP4: A @ I == A ===")
A3 = np.array([[2, -1, 0], [1, 3, 4], [0, 0, 5]], dtype=float)
print("  A@I == A ?", np.allclose(A3 @ np.eye(3), A3))

print("\n=== EXP5: hand-check A@x (row times column) ===")
M = np.array([[1, 2], [3, 4], [5, 6]], dtype=float)  # 3x2
x = np.array([10, 100], dtype=float)
print("  M@x =", M @ x, " expect [1*10+2*100, 3*10+4*100, 5*10+6*100]=[210,430,650]")

print(f"\n  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
