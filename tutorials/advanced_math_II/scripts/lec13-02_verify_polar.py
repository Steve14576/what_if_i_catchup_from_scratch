# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 13 讲《极坐标与一般换元（雅可比）》数值核对。
#   EXP1  x^2+y^2 over the unit disk -> pi/2
#   EXP2  exp(-(x^2+y^2)) over the first-quadrant disk -> (pi/4)(1-1/e)
#   EXP3  xy over the first-quadrant disk -> 1/8
#   EXP4  sqrt(x^2+y^2) over the unit disk -> 2*pi/3
#   EXP5  exp(x+y) over the parallelogram -> (e-1)/2
import math
import time

import numpy as np

T0 = time.perf_counter()


def polar_int(f, th0, th1, r0, r1, nth=2000, nr=2000):
    th = th0 + (th1 - th0) * (np.arange(nth) + 0.5) / nth
    r = r0 + (r1 - r0) * (np.arange(nr) + 0.5) / nr
    R, TH = np.meshgrid(r, th)
    vals = f(R * np.cos(TH), R * np.sin(TH))
    return np.sum(vals * R) * ((th1 - th0) / nth) * ((r1 - r0) / nr)


print("=== EXP1: x^2+y^2 over the unit disk -> pi/2 ===")
f1 = lambda x, y: x * x + y * y
v1 = polar_int(f1, 0, 2 * math.pi, 0, 1)
print(f"  polar = {v1:.8f}, exact = pi/2 = {math.pi/2:.8f}, diff = {abs(v1-math.pi/2):.2e}")
print()

print("=== EXP2: exp(-(x^2+y^2)) over the first-quadrant disk ===")
f2 = lambda x, y: np.exp(-(x * x + y * y))
v2 = polar_int(f2, 0, math.pi / 2, 0, 1)
ex2 = math.pi / 4 * (1 - math.exp(-1))
print(f"  polar = {v2:.8f}, exact = (pi/4)(1-1/e) = {ex2:.8f}, diff = {abs(v2-ex2):.2e}")
print()

print("=== EXP3: xy over the first-quadrant disk -> 1/8 ===")
f3 = lambda x, y: x * y
v3 = polar_int(f3, 0, math.pi / 2, 0, 1)
print(f"  polar = {v3:.8f}, exact = 0.125, diff = {abs(v3-0.125):.2e}")
print()

print("=== EXP4: sqrt(x^2+y^2) over the unit disk -> 2*pi/3 ===")
f4 = lambda x, y: np.sqrt(x * x + y * y)
v4 = polar_int(f4, 0, 2 * math.pi, 0, 1)
ex4 = 2 * math.pi / 3
print(f"  polar = {v4:.8f}, exact = 2pi/3 = {ex4:.8f}, diff = {abs(v4-ex4):.2e}")
print()

print("=== EXP5: general substitution, exp(x+y) over the parallelogram ===")
# u = x+y, v = x-y; x=(u+v)/2, y=(u-v)/2; |J| = 1/2; u,v in [0,1]
n = 4000
u = (np.arange(n) + 0.5) / n
v = (np.arange(n) + 0.5) / n
U, V = np.meshgrid(u, v)
integrand = np.exp(U) * 0.5
v5 = np.sum(integrand) / n ** 2
ex5 = 0.5 * (math.e - 1)
print(f"  uv-grid = {v5:.8f}, exact = (e-1)/2 = {ex5:.8f}, diff = {abs(v5-ex5):.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
