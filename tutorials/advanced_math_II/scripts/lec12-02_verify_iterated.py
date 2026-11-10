# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 12 讲《二重积分的计算（直角坐标）》数值核对。
#   EXP1  x+y over the triangle 0<=x<=1, 0<=y<=x  -> 1/2
#   EXP2  xy between y=x^2 and y=x              -> 1/24
#   EXP3  reversed order for exp(-y^2)           -> (1-e^-1)/2
#   EXP4  area between y=x^2 and y=2-x^2: X-type vs Y-type -> 8/3
#   EXP5  x^3 y over the unit disk               -> 0
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: example 1, double integral of x+y over the triangle ===")
n = 2000
x = (np.arange(n) + 0.5) / n
y = x[:, None] * (np.arange(n) + 0.5)[None, :] / n
val = np.sum((x[:, None] + y) * x[:, None] / n ** 2)  # cell area is (1/n) * (x_i/n)
print(f"  numeric = {val:.8f}, exact = 0.5, diff = {abs(val-0.5):.2e}")
print()

print("=== EXP2: example 2, double integral of xy between y=x^2 and y=x ===")
n = 2000
xi = (np.arange(n) + 0.5) / n
# exact inner integral: int_{x^2}^{x} x*y dy = x*(x^2 - x^4)/2
inner = xi * (xi ** 2 - xi ** 4) / 2
val = np.sum(inner) / n
print(f"  numeric = {val:.8f}, exact = 1/24 = {1/24:.8f}, diff = {abs(val-1/24):.2e}")
print()

print("=== EXP3: example 3, reversed order for exp(-y^2) ===")
# integral_0^1 dy integral_0^y exp(-y^2) dx = integral_0^1 y exp(-y^2) dy
n = 200000
y = (np.arange(n) + 0.5) / n
val = np.sum(y * np.exp(-y ** 2)) / n
exact = 0.5 * (1 - math.exp(-1))
print(f"  numeric = {val:.8f}, exact = (1-e^-1)/2 = {exact:.8f}, diff = {abs(val-exact):.2e}")
print()

print("=== EXP4: example 4, area by X-type vs Y-type ===")
# X-type: int_{-1}^{1} (2-2x^2) dx
n = 400000
x = -1 + 2 * (np.arange(n) + 0.5) / n
vx = np.sum(2 - 2 * x ** 2) * (2 / n)
# Y-type: int_0^1 2 sqrt(y) dy + int_1^2 2 sqrt(2-y) dy
y1 = (np.arange(n) + 0.5) / n
v1 = np.sum(2 * np.sqrt(y1)) / n
y2 = 1 + (np.arange(n) + 0.5) / n
v2 = np.sum(2 * np.sqrt(2 - y2)) / n
print(f"  X-type = {vx:.8f}, Y-type = {v1+v2:.8f}, exact = 8/3 = {8/3:.8f}")
print()

print("=== EXP5: symmetry, x^3 y over the unit disk ===")
n = 400
x = np.linspace(-1, 1, n)
X, Y = np.meshgrid(x, x)
mask = X ** 2 + Y ** 2 <= 1
val = np.sum((X ** 3 * Y)[mask]) * (2.0 / (n - 1)) ** 2
print(f"  numeric = {val:.3e}  (expect ~ 0)")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
