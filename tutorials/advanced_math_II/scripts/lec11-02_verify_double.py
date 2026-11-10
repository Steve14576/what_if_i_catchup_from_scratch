# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 11 讲《二重积分的定义与性质》数值核对。
#   EXP1  Riemann sums for x^2+y^2 on [0,1]^2: n=10,100,1000 -> 2/3
#   EXP2  Riemann sums for x on [0,1]^2 (right endpoints) -> 1/2
#   EXP3  estimate of 1/(1+x^2+y^2) on the unit disk vs bounds [pi/2, pi]
#   EXP4  Dirichlet-type function: two sample rules give 1 and 0
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: Riemann sums for x^2+y^2 on [0,1]^2, n = 10, 100, 1000 ===")
for n in [10, 100, 1000]:
    i = np.arange(1, n + 1) / n
    s = 2 * np.sum(i ** 2) / n  # (1/n) * sum over i of (i/n)^2, doubled for x and y
    print(f"  n={n:4d}: S_n = {s:.10f}, err vs 2/3 = {abs(s - 2/3):.2e}")
print()

print("=== EXP2: Riemann sums for x on [0,1]^2 (right endpoints) ===")
for n in [10, 100, 1000]:
    s = (n + 1) / (2 * n)
    print(f"  n={n:4d}: S_n = {s:.10f}, err vs 1/2 = {abs(s - 0.5):.2e}")
print()

print("=== EXP3: estimate of 1/(1+x^2+y^2) on the unit disk vs bounds ===")
n = 1000
x = np.linspace(-1, 1, n)
y = np.linspace(-1, 1, n)
X, Y = np.meshgrid(x, y)
mask = X ** 2 + Y ** 2 <= 1
cell = (2.0 / (n - 1)) ** 2
est = np.sum(1.0 / (1.0 + X[mask] ** 2 + Y[mask] ** 2)) * cell
print(f"  grid estimate = {est:.6f}")
print(f"  bounds: pi/2 = {math.pi/2:.6f} <= I <= pi = {math.pi:.6f}")
print(f"  analytic check: pi*ln2 = {math.pi*math.log(2):.6f}")
print()

print("=== EXP4: Dirichlet-type function: two choices of sample points ===")
n = 10
area = 1.0 / (n * n)
sum_rational = sum(1.0 * area for _ in range(n * n))   # simulate: all sample points rational
sum_irrational = sum(0.0 * area for _ in range(n * n))  # simulate: all sample points irrational
print(f"  all rational sample points:   S = {sum_rational:.6f}")
print(f"  all irrational sample points: S = {sum_irrational:.6f}")
print("  -> same partition, different sample points, different limits: not integrable")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
