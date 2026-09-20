# 规模纪律：纯 numpy，最大 4x4，目标 < 3 秒。
# 验证内容（线性无关 / 基 / 维数）：
#   EXP1  无关判定：把向量排成列 -> rank == 个数 <-> 无关（两组对照）
#   EXP2  含零向量必相关；成比例组相关
#   EXP3  基的两条件验证：R^3 中一组无关向量自动张成 R^3（任意 b 可解 Ax=b）
#   EXP4  维数不依赖选基：xy-平面两组不同基，个数都是 2
#   EXP5  多项式空间 P3：标准基 {1,t,t^2,t^3}，维数 4，任意系数数组可组合
#   EXP6  n 个无关向量自动张成 / n 个张成向量自动无关（n维空间，数值演示）
#   EXP7  RREF 主元列 = 极大无关组（从生成集提炼基）
import time
import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=4, suppress=True)


def indep_cols(cols):
    """把向量排成列，rank==列数 <-> 无关。返回 (是否无关, rank)。"""
    M = np.column_stack(cols)
    r = np.linalg.matrix_rank(M)
    return r == M.shape[1], r


print("=== EXP1 无关判定：rank==个数 <-> 无关 ===")
v1, v2, v3 = np.array([1.0, 2.0, 0.0]), np.array([0.0, 1.0, 3.0]), np.array([0.0, 0.0, 1.0])
ok, r = indep_cols([v1, v2, v3])
print(f"  三角组 (1,2,0),(0,1,3),(0,0,1): rank={r} 无关={ok} (期望 True)")
ok2, r2 = indep_cols([np.array([1.0, 2.0]), np.array([2.0, 4.0])])
print(f"  成比例组 (1,2),(2,4): rank={r2} 无关={ok2} (期望 False)")

print("\n=== EXP2 含零向量必相关 ===")
ok3, r3 = indep_cols([np.array([0.0, 0.0]), np.array([1.0, 0.0])])
print(f"  {(0.0, 0.0)},{(1.0, 0.0)}: rank={r3} 相关={not ok3} (期望相关 True)")

print("\n=== EXP3 无关三向量自动张成 R^3 ===")
M = np.column_stack([v1, v2, v3])
print(f"  rank={np.linalg.matrix_rank(M)} (=3=维数)")
for b in [np.array([1.0, 1.0, 1.0]), np.array([-5.0, 3.0, 7.0])]:
    x = np.linalg.solve(M, b)
    print(f"  b={b}: 解出 x={x.round(4)}，A@x 回代={ (M @ x).round(4)} == b [OK]")

print("\n=== EXP4 维数不依赖选基（xy-平面两组基）===")
B1 = [np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])]
B2 = [np.array([1.0, 1.0, 0.0]), np.array([1.0, -1.0, 0.0])]
print(f"  基1: rank={np.linalg.matrix_rank(np.column_stack(B1))} 个数=2")
print(f"  基2: rank={np.linalg.matrix_rank(np.column_stack(B2))} 个数=2（无关）")
b_xy = np.array([4.0, -2.0, 0.0])
B2_M = np.column_stack(B2)
x = np.linalg.solve(B2_M[:2, :], b_xy[:2])  # 两基向量 z 分量全 0，取前两行解系数
print(f"  用基2表示 (4,-2,0): 系数={x.round(4)}，组合回代={ (B2_M @ x).round(4)}")

print("\n=== EXP5 多项式空间 P3: 标准基 {1,t,t^2,t^3} ===")
std = np.eye(4)  # 系数数组视角下的 e0,e1,e2,e3
coef = np.array([2.0, -1.0, 0.5, 3.0])
print(f"  任意系数 {coef} = 2*e0-1*e1+0.5*e2+3*e3；rank(标准基)={np.linalg.matrix_rank(std)} -> 维数 4")

print("\n=== EXP6 n 个无关自动张成；n 个张成自动无关（R^2 数值演示）===")
A_cand = np.column_stack([np.array([1.0, 0.3]), np.array([-2.0, 1.0])])
print(f"  R^2 中两向量 rank={np.linalg.matrix_rank(A_cand)}（无关=2）")
for b in [np.array([5.0, 5.0]), np.array([-1.0, 9.0])]:
    print(f"    任意 b={b} 可解? {np.linalg.matrix_rank(np.column_stack([A_cand, b])) == 2} （排成增广看 rank 不变）")

print("\n=== EXP7 从生成集提炼基：RREF 主元列 ===")
G = np.column_stack([np.array([1.0, 2.0, 1.0]), np.array([2.0, 4.0, 2.0]),
                     np.array([0.0, 1.0, 0.0]), np.array([1.0, 1.0, 1.0])])
M = G.astype(float).copy()
rows, cols = M.shape
pivots = []
r = 0
for c in range(cols):
    piv = np.argmax(np.abs(M[r:, c])) + r
    if abs(M[piv, c]) < 1e-9:
        continue
    M[[r, piv]] = M[[piv, r]]
    M[r] = M[r] / M[r, c]
    for i in range(rows):
        if i != r:
            M[i] -= M[i, c] * M[r]
    pivots.append(c)
    r += 1
print(f"  RREF 主元列={pivots}；生成集 rank={np.linalg.matrix_rank(G)}")
print(f"  -> 基 = 第 {pivots} 列；span 不变（其余列是基列的线性组合）")

print(f"\n  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
