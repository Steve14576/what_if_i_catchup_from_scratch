# 规模纪律：纯 numpy，最大 3x3，目标 < 3 秒。
# 验证内容（行列式 determinant）：
#   EXP1  2x2 手算 ad-bc 对照 np.linalg.det
#   EXP2  3x3 按第一行余子式展开 手算 对照 numpy（Strang 例，det=1）
#   EXP3  性质：det(AB)=detA·detB；det(A^T)=detA；det(A^-1)=1/detA
#   EXP4  反例（破"想当然线性"）：det(A+B) != detA+detB
#   EXP5  三角阵 det=对角元之积；交换两行 det 变号
#   EXP6  奇异（秩亏）矩阵 det≈0
#   EXP7  几何：|det[u v]| = 以 u,v 为邻边的平行四边形面积（与叉积模对照）
#   EXP8  消元记账法：化上三角，记录换行次数与倍加，对角积×(-1)^交换 对照 np.linalg.det
import time
import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=4, suppress=True)


def det2(m):  # 2x2 手算 ad-bc
    return m[0, 0] * m[1, 1] - m[0, 1] * m[1, 0]


def det3_cofactor_row1(m):  # 3x3 按第一行余子式展开 手算
    a, b, c = m[0, 0], m[0, 1], m[0, 2]
    M00 = m[1, 1] * m[2, 2] - m[1, 2] * m[2, 1]
    M01 = m[1, 0] * m[2, 2] - m[1, 2] * m[2, 0]
    M02 = m[1, 0] * m[2, 1] - m[1, 1] * m[2, 0]
    return a * M00 - b * M01 + c * M02


print("=== EXP1 2x2: ad-bc ===")
P = np.array([[3.0, 1.0], [2.0, 4.0]])
print(f"  det2({P})={det2(P)}  numpy={np.linalg.det(P):.4f}")

print("\n=== EXP2 3x3 余子式(第一行) vs numpy ===")
A = np.array([[1.0, 2.0, 3.0], [0.0, 1.0, 4.0], [5.0, 6.0, 0.0]])
# 手算：1*(1*0-4*6) - 2*(0*0-4*5) + 3*(0*6-1*5) = 1*(-24)-2*(-20)+3*(-5)
print(f"  手算余子式={det3_cofactor_row1(A)}  numpy={np.linalg.det(A):.4f}  (期望 1)")

print("\n=== EXP3 性质 ===")
B = np.array([[2.0, 0.0], [1.0, 3.0]])  # det=6
P = np.array([[3.0, 1.0], [2.0, 4.0]])  # det=10
print(f"  det(B)={np.linalg.det(B):.4f} det(P)={np.linalg.det(P):.4f}")
print(f"  det(BP)={np.linalg.det(B @ P):.4f} vs detB*detP={np.linalg.det(B) * np.linalg.det(P):.4f}  (期望 60)")
print(f"  det(B^T)={np.linalg.det(B.T):.4f} vs detB={np.linalg.det(B):.4f}")
print(f"  det(B^-1)={np.linalg.det(np.linalg.inv(B)):.4f} vs 1/detB={1 / np.linalg.det(B):.4f}")

print("\n=== EXP4 反例 det(A+B) != detA+detB ===")
I2 = np.eye(2)
print(f"  det(I+I)={np.linalg.det(I2 + I2):.4f}  detI+detI={np.linalg.det(I2) + np.linalg.det(I2):.4f}  (4 != 2)")

print("\n=== EXP5 三角阵=对角积；换行变号 ===")
U = np.array([[2.0, 5.0, 1.0], [0.0, 3.0, 7.0], [0.0, 0.0, 4.0]])
print(f"  det(上三角)={np.linalg.det(U):.4f}  对角积=2*3*4={2 * 3 * 4}")
Aswap = A[[1, 0, 2], :]  # 交换 A 的第1、2行
print(f"  det(A)={np.linalg.det(A):.4f}  det(换两行后)={np.linalg.det(Aswap):.4f}  (应变号)")

print("\n=== EXP6 奇异矩阵 det≈0 ===")
S = np.array([[1.0, 2.0], [2.0, 4.0]])  # 第二行=2*第一行 -> 秩1
print(f"  det(奇异)={np.linalg.det(S):.6f}  rank={np.linalg.matrix_rank(S)} (秩亏=>det=0)")

print("\n=== EXP7 几何: |det[u v]| = 平行四边形面积 ===")
u = np.array([3.0, 0.0]); v = np.array([1.0, 2.0])
Mat = np.column_stack([u, v])
area_det = abs(np.linalg.det(Mat))
area_cross = abs(u[0] * v[1] - u[1] * v[0])  # 2D 叉积模
print(f"  |det|={area_det:.4f}  叉积面积={area_cross:.4f}  (期望都是 6)")

print("\n=== EXP8 消元记账法（含换行变号）===")
M = np.array([[0.0, 2.0, 3.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]])
U = M.copy()
swaps = 0
print("  初始:", U.tolist())
U[[0, 1]] = U[[1, 0]]; swaps += 1          # 换行: 主元 1
print("  换r1<->r2 (swap=1):", U.tolist())
U[2] = U[2] - 2 * U[0]                       # 倍加: 消掉 r3 第1列
print("  r3-=2r1:", U.tolist())
U[[1, 2]] = U[[2, 1]]; swaps += 1          # 换行: 主元 1
print("  换r2<->r3 (swap=2):", U.tolist())
U[2] = U[2] - 2 * U[1]                       # 倍加: 消掉 r3 第2列
print("  r3-=2r2:", U.tolist())
det_manual = U[0, 0] * U[1, 1] * U[2, 2] * ((-1) ** swaps)
print(f"  对角积=1*1*7={U[0, 0] * U[1, 1] * U[2, 2]:.0f}, swaps={swaps}, det(记账)={det_manual:.4f}")
print(f"  det(numpy)={np.linalg.det(M):.4f}")

print(f"\n  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
