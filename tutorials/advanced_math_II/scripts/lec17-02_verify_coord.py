# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 17 讲《第二类曲线积分》数值核对。
#   EXP1  y dx + x dy on y=x^2, (0,0)->(1,1) -> 1
#   EXP2  same integral on y=x -> 1 (path independence preview)
#   EXP3  reversed direction on y=x^2 -> -1
#   EXP4  closed unit circle CCW: oint -y dx + x dy -> 2*pi
#   EXP5  two kinds agree (second vs first with direction cosines)
import math
import time

import numpy as np

T0 = time.perf_counter()
n = 200000

print("=== EXP1: y dx + x dy on y=x^2, (0,0)->(1,1) -> 1 ===")
t = (np.arange(n) + 0.5) / n
x, y = t, t ** 2
dx, dy = 1.0, 2 * t
v1 = np.sum(y * dx + x * dy) * (1.0 / n)
print(f"  numeric = {v1:.8f}, exact = 1, diff = {abs(v1-1):.2e}")
print()

print("=== EXP2: same integral on y=x, (0,0)->(1,1) -> 1 ===")
x, y = t, t
dx, dy = 1.0, 1.0
v2 = np.sum(y * dx + x * dy) * (1.0 / n)
print(f"  numeric = {v2:.8f}, exact = 1, diff = {abs(v2-1):.2e}")
print()

print("=== EXP3: reversed direction on y=x^2 -> -1 ===")
x, y = t, t ** 2
dx, dy = 1.0, 2 * t
# integrate from t=1 to t=0: the parameter step is negative
v3 = np.sum(y * dx + x * dy) * (-1.0 / n)
print(f"  numeric = {v3:.8f}, exact = -1, diff = {abs(v3+1):.2e}")
print()

print("=== EXP4: closed unit circle, CCW: oint -y dx + x dy -> 2*pi ===")
th = (np.arange(n) + 0.5) / n * 2 * math.pi
x, y = np.cos(th), np.sin(th)
dx = -np.sin(th)
dy = np.cos(th)
v4 = np.sum(-y * dx + x * dy) * (2 * math.pi / n)
print(f"  numeric = {v4:.8f}, exact = 2*pi = {2*math.pi:.8f}, diff = {abs(v4-2*math.pi):.2e}")
print()

print("=== EXP5: two kinds agree (second vs first with direction cosines) ===")
# P=-y, Q=x on the unit circle; e_tau=(-sin, cos)
P, Q = -y, x
second = np.sum(P * dx + Q * dy) * (2 * math.pi / n)
cos_a, cos_b = -np.sin(th), np.cos(th)
first = np.sum((P * cos_a + Q * cos_b) * 1.0) * (2 * math.pi / n)
print(f"  second = {second:.8f}, first = {first:.8f}, diff = {abs(second-first):.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
