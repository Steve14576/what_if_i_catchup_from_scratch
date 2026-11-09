# 规模纪律：小规模数值核对, 目标 < 2 秒。
# 第 03 讲《曲面与曲线》数值核对：方程与点的归属、旋转对称、截痕、投影柱面。
#   EXP1 柱面 y=x^2: 任意 z 的点都在曲面上
#   EXP2 旋转面 z=x^2+y^2: (x,±y) 与 (±x,y) 同高
#   EXP3 椭球 x^2/4+y^2+z^2=1: 参数点满足; z=0 截痕半轴 2 与 1
#   EXP4 单叶双曲面 x^2+y^2-z^2=1: 参数点满足; z=0/2 截圆半径 1/sqrt(5)
#   EXP5 螺旋线 (cos t,sin t,t): x^2+y^2=1 逐点成立 (投影柱面)
#   EXP6 作业7: z=1-x^2-y^2 与 z=0 截出单位圆
import math
import time

import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=10, suppress=True)

print("=== EXP1: cylinder y = x^2 (any z) ===")
x0 = 0.7
y0 = 0.49          # independent literal value: 0.7^2
for z0 in [-2.0, 0.0, 3.0]:
    print(f"  point ({x0}, {y0}, {z0}): y - x^2 = {y0 - x0 ** 2:.2e}, z varies freely")
print()

print("=== EXP2: surface of revolution z = x^2 + y^2 ===")
x0, y0 = 0.6, 0.8
z0 = x0 ** 2 + y0 ** 2
for (px, py) in [(x0, y0), (x0, -y0), (-x0, y0), (-x0, -y0)]:
    print(f"  ({px:+.1f},{py:+.1f}): z - (x^2+y^2) = {z0 - (px**2 + py**2):.2e}")
print()

print("=== EXP3: ellipsoid x^2/4 + y^2 + z^2 = 1 ===")
u, v = 0.9, 1.3
p = np.array([2 * math.sin(u) * math.cos(v), math.sin(u) * math.sin(v), math.cos(u)])
val = p[0] ** 2 / 4 + p[1] ** 2 + p[2] ** 2
print(f"  param point {p}; residual = {val - 1:.2e} (expect 0)")
print("  z=0 section: x^2/4 + y^2 = 1 -> semi-axes 2 and 1")
print()

print("=== EXP4: one-sheet hyperboloid x^2 + y^2 - z^2 = 1 ===")
for t0 in [-1.0, 0.0, 2.0]:
    rad = math.sqrt(1 + t0 ** 2)
    v0 = 0.7
    q = np.array([rad * math.cos(v0), rad * math.sin(v0), t0])
    print(f"  t={t0:+.1f}: residual = {q[0]**2 + q[1]**2 - q[2]**2 - 1:.2e}; section radius = {rad:.4f}")
print("  (z=0 radius 1, z=2 radius sqrt(5) = 2.2361)")
print()

print("=== EXP5: helix projected to xOy ===")
for t0 in [0.0, 1.0, 2.5, 6.0]:
    p = np.array([math.cos(t0), math.sin(t0), t0])
    print(f"  t={t0:.1f}: x^2+y^2-1 = {p[0]**2 + p[1]**2 - 1:.2e}")
print()

print("=== EXP6: z = 1 - x^2 - y^2 cut by z = 0 (Q7) ===")
for (px, py) in [(1.0, 0.0), (0.0, -1.0), (0.6, 0.8)]:
    print(f"  ({px},{py}): z = {1 - px**2 - py**2:.2e}; x^2+y^2-1 = {px**2 + py**2 - 1:.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
