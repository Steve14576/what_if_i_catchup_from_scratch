# 规模纪律：纯 numpy，向量维度 ≤4，目标 < 3 秒。
# 验证内容（向量空间与子空间的三条件打勾）：
#   EXP1  过原点直线 L={(t,2t)} 是子空间：0 在其中、加封闭、数乘封闭（随机点验证）
#   EXP2  不过原点的直线 M={p+(t,2t)} 不是子空间：0 不在；且两解之和跳出 M
#   EXP3  N(A) 是子空间（A@(x1+x2)=0）；col(A) 是子空间（列的线性组合仍在）
#   EXP4  反例：两条坐标轴（都是子空间）的"并"不是子空间（取 x 轴点+ y 轴点 -> 一般不在并里）
#   EXP5  多项式空间 P3（系数数组）加/数乘封闭
#   EXP6  两个子空间的"交"是子空间（两条过原点直线之交 = {0}）
import time
import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=4, suppress=True)
rng = np.random.default_rng(20260920)


def on_line_L(x):
    return np.allclose(x[1], 2 * x[0])


print("=== EXP1 过原点直线 L={(t,2t)} 三条件 ===")
zero = np.array([0.0, 0.0])
print(f"  ① 0 in L? {on_line_L(zero)}")
for _ in range(3):
    a, b = rng.standard_normal(2), rng.standard_normal(2)
    u = np.array([a[0], 2 * a[0]]); v = np.array([b[0], 2 * b[0]])
    ok_add = on_line_L(u + v); ok_scale = on_line_L(5.0 * u)
    print(f"     u={u} v={v}: u+v in L? {ok_add}; 5u in L? {ok_scale}")
print("  -> 封闭性成立，L 是子空间")

print("\n=== EXP2 不过原点直线 M={p+(t,2t)}, p=(1,0) ===")
p = np.array([1.0, 0.0])
print(f"  ① 0 in M? {on_line_L(np.array([0.0, 0.0]) - p)} (0-p 不在直线上)")
u = p + np.array([1.0, 2.0]); v = p + np.array([-1.0, -2.0])
w = u + v
print(f"  ② u={u}, v={v} 都在 M；u+v={w}，仍在 M? {on_line_L(w - p)}")
print("  -> 不封闭，M 不是子空间（仿射集）")

print("\n=== EXP3 N(A) 与 col(A) 是子空间 ===")
A = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [1.0, 2.0, 3.0]])  # rank1
x1 = np.array([-2.0, 1.0, 0.0]); x2 = np.array([-3.0, 0.0, 1.0])    # N(A) 基
print(f"  A@(x1+x2)={A @ (x1 + x2)} (期望 0)；A@(7x1)={A @ (7 * x1)}")
c1, c2 = A[:, 0], A[:, 2]
combo = 3 * c1 - 2 * c2
print(f"  col(A): 3c1-2c2={combo}，仍在 col(A)？由定义恒真（就是列的线性组合）")

print("\n=== EXP4 反例：两坐标轴的‘并’不是子空间 ===")
x_axis = np.array([3.0, 0.0]); y_axis = np.array([0.0, 4.0])
print(f"  x轴上点={x_axis}、y轴上点={y_axis}；都在‘并’里")
s = x_axis + y_axis
not_on_axes = (s[0] != 0) and (s[1] != 0)
print(f"  和={s}，不在任何一条轴上（x,y 分量都非零）: {not_on_axes} -> 并集不封闭，不是子空间")

print("\n=== EXP5 多项式空间 P3（系数数组）封闭 ===")
f = np.array([1.0, -2.0, 0.0, 4.0])  # 1 - 2t + 4t^3
g = np.array([0.0, 3.0, 1.0, 0.0])   # 3t + t^2
print(f"  f+g 是 4 维系数数组: {f + g}；7f: {7 * f}   (仍在 P3)")

print("\n=== EXP6 两个子空间之交是子空间 ===")
L1 = lambda x: np.allclose(x[1], 0)      # x 轴
L2 = lambda x: np.allclose(x[1], 2 * x[0])  # y=2x 轴
inter = np.array([0.0, 0.0])
print(f"  L1∩L2={inter}（只有原点，含 0、加数乘封闭，是子空间——最平凡的子空间）")

print(f"\n  TOTAL runtime: {time.perf_counter() - T0:.2f}s")