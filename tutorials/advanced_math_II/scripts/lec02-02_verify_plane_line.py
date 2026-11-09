# 规模纪律：小规模数值核对, 目标 < 2 秒。
# 第 02 讲《平面与直线》数值核对：对应正文例 1-4 与作业 7。
#   EXP1  过三点平面: 三点在 x+y+z=1 上; 法向与两边垂直 (相对)
#   EXP2  两平面夹角与交线: cos=1/3; 交线方向与两法向垂直; 交点在两平面上
#   EXP3  点到平面距离: 公式 2/3; 投影法独立核对
#   EXP4  线面交点与夹角: t=1/6; 残差 0; sin=6/sqrt(42)
#   EXP5  平面束 (Q7): lambda=6 -> 7x-5y+z-1=0
import math
import time

import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=10, suppress=True)

print("=== EXP1: plane through three points ===")
A = np.array([1.0, 0.0, 0.0]); B = np.array([0.0, 1.0, 0.0]); C = np.array([0.0, 0.0, 1.0])
n = np.cross(B - A, C - A)
print(f"  n = AB x AC = {n}  (expect [1,1,1])")
res = [float(p.sum() - 1.0) for p in (A, B, C)]
print(f"  x+y+z-1 at A,B,C = {res}  (expect 0)")
print(f"  |n.AB|/(|n||AB|) = {abs(np.dot(n, B - A)) / (np.linalg.norm(n) * np.linalg.norm(B - A)):.2e}")
print(f"  |n.AC|/(|n||AC|) = {abs(np.dot(n, C - A)) / (np.linalg.norm(n) * np.linalg.norm(C - A)):.2e}")
print()

print("=== EXP2: angle between planes and their intersection line ===")
n1 = np.array([1.0, 1.0, 1.0]); n2 = np.array([1.0, 1.0, -1.0])
cos_t = abs(np.dot(n1, n2)) / (np.linalg.norm(n1) * np.linalg.norm(n2))
print(f"  cos(theta) = {cos_t:.10f}  (expect 1/3 = {1/3:.10f}); theta = {math.degrees(math.acos(cos_t)):.2f} deg")
s = np.cross(n1, n2)
print(f"  line direction n1 x n2 = {s}  (expect [-2,2,0])")
print(f"  |s.n1|/... = {abs(np.dot(s, n1)) / (np.linalg.norm(s) * np.linalg.norm(n1)):.2e}; |s.n2|/... = {abs(np.dot(s, n2)) / (np.linalg.norm(s) * np.linalg.norm(n2)):.2e}")
P0 = np.array([0.5, 0.0, 0.5])
print(f"  point (0.5,0,0.5) on both planes: {P0.sum() - 1:.2e}, {(P0[0] + P0[1] - P0[2]):.2e}")
print()

print("=== EXP3: distance point-plane ===")
Pn = np.array([1.0, 1.0, 1.0]); npl = np.array([1.0, 2.0, 2.0]); d0 = -3.0
d_formula = abs(npl.dot(Pn) + d0) / np.linalg.norm(npl)
M1 = np.array([3.0, 0.0, 0.0])          # on the plane
d_proj = abs(npl.dot(Pn - M1)) / np.linalg.norm(npl)
print(f"  formula d = {d_formula:.10f}  (expect 2/3 = {2/3:.10f})")
print(f"  projection d = {d_proj:.10f}")
print()

print("=== EXP4: line-plane intersection and angle ===")
sd = np.array([1.0, 2.0, 3.0])
t = 1.0 / 6.0
Pi = t * sd
res4 = Pi.sum() - 1.0
sin_t = abs(sd.dot(np.array([1.0, 1.0, 1.0]))) / (np.linalg.norm(sd) * math.sqrt(3))
print(f"  t = {t:.10f}; point = {Pi}; residual = {res4:.2e}")
print(f"  sin(theta) = {sin_t:.10f}  (expect 6/sqrt(42) = {6/math.sqrt(42):.10f}); theta = {math.degrees(math.asin(sin_t)):.2f} deg")
print()

print("=== EXP5: pencil of planes (Q7) ===")
lam = 6.0
coef = np.array([1 + lam, 1 - lam, 1.0]); const = -1.0
print(f"  coefficients = {coef}, constant = {const}  (expect [7,-5,1], -1)")
print(f"  dot with (1,2,3) = {coef.dot(np.array([1.0, 2.0, 3.0])):.2e}  (expect 0)")
for pt in [np.array([0.0, 0.0, 1.0]), np.array([0.5, 0.5, 0.0])]:
    print(f"  line point {pt}: value = {coef.dot(pt) + const:.2e}  (expect 0); on both planes: {pt.sum()-1:.2e}, {pt[0]-pt[1]:.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
