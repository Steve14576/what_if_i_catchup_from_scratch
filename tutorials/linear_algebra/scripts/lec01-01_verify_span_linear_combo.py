# 规模纪律：纯 numpy 线性组合/张成判定，3x3 以内，目标 < 3 秒。
# 验证内容：
#   EXP1  两个向量 v1,v2 的线性组合 a*v1+b*v2 能否拼出目标 b_target
#         - 平行向量 (1,2),(2,4)：张成退化成一条线，(3,6) 能拼出，(1,0) 拼不出
#         - 无关向量 (1,0),(0,1)：张成铺满整个平面，任意目标都能拼出
#   EXP2  用解线性方程组 M x = target 判定 target 是否在 span 里（M 列是 v1,v2）
#         比较 rank(M) 与 rank([M|target])：相等=能拼出，不等=拼不出
import time
import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=4, suppress=True)


def in_span(cols, target):
    """cols: list of vectors (each 1d array). target: 1d array.
    返回 (是否可拼出, 系数 a,b,...). 用增广矩阵秩判定 + lstsq 求系数。"""
    M = np.column_stack(cols)
    aug = np.column_stack([M, target])
    r_M = np.linalg.matrix_rank(M)
    r_aug = np.linalg.matrix_rank(aug)
    can = (r_M == r_aug)
    coef, res, rank, sv = np.linalg.lstsq(M, target, rcond=None)
    return can, r_M, r_aug, coef, M @ coef


print("=== EXP1: span of two vectors in R^2 ===")
v1 = np.array([1.0, 2.0])
v2 = np.array([2.0, 4.0])  # = 2*v1, 平行 -> 张成退化成一条线
for target in [np.array([3.0, 6.0]), np.array([1.0, 0.0])]:
    can, rM, rA, coef, recon = in_span([v1, v2], target)
    print(f"  target={target}  rank(M)={rM} rank(aug)={rA}  in_span={can}")
    print(f"    coef a,b={coef}  -> a*v1+b*v2={recon}")

print("\n=== EXP2: two independent vectors span the whole plane ===")
e1 = np.array([1.0, 0.0])
e2 = np.array([0.0, 1.0])
for target in [np.array([3.0, 6.0]), np.array([1.0, 0.0]), np.array([-2.5, 7.1])]:
    can, rM, rA, coef, recon = in_span([e1, e2], target)
    print(f"  target={target}  in_span={can}  coef={coef}  recon={recon}")

# 结论自检
v_par = np.array([2.0, 4.0])
print("\n  [check] v2 == 2*v1 ?", np.allclose(v2, 2 * v1))
print("  -> 平行向量 rank=1 张成退化; 无关向量 rank=2 铺满平面; lstsq 残差近 0 才可拼出")

print(f"\n  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
