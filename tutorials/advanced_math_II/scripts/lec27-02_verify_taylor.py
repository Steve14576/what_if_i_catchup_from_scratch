# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 27 讲《函数展开成幂级数》数值核对。
#   EXP1  e^x at x=1, partial sums
#   EXP2  sin x at x=1, partial sums
#   EXP3  ln(1+x) at x=1 (slow) -> ln 2
#   EXP4  arctan 1 (alternating) -> pi/4
#   EXP5  integral of e^{-x^2} on [0,1] via series vs quadrature
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: e^x at x=1, partial sums ===")
for N in [5, 10, 20]:
    s = sum(1.0 / math.factorial(k) for k in range(N + 1))
    print(f"  n={N:<3}: partial sum = {s:.12f}, e = {math.e:.12f}, diff = {abs(s-math.e):.2e}")
print()

print("=== EXP2: sin x at x=1, partial sums ===")
for N in [3, 5, 7]:
    s = sum(((-1) ** k) / math.factorial(2 * k + 1) for k in range(N // 2 + 1))
    print(f"  n={N:<3}: partial sum = {s:.12f}, sin 1 = {math.sin(1):.12f}, diff = {abs(s-math.sin(1)):.2e}")
print()

print("=== EXP3: ln(1+x) at x=1 (slow) -> ln 2 ===")
for N in [10, 100, 1000, 10000]:
    s = sum(((-1.0) ** (k - 1)) / k for k in range(1, N + 1))
    print(f"  N={N:<6}: partial sum = {s:.10f}, ln2 = {math.log(2):.10f}, diff = {abs(s-math.log(2)):.2e}")
print("  -> error ~ 1/N: slow")
print()

print("=== EXP4: arctan 1 (alternating) -> pi/4 ===")
for N in [10, 100, 1000]:
    s = sum(((-1.0) ** k) / (2 * k + 1) for k in range(N + 1))
    print(f"  N={N:<5}: partial sum = {s:.10f}, pi/4 = {math.pi/4:.10f}, diff = {abs(s-math.pi/4):.2e}")
print("  -> error ~ 1/(2N): faster than ln2")
print()

print("=== EXP5: integral of e^{-x^2} on [0,1] via series vs quadrature ===")
# series: sum (-1)^n / (n! (2n+1))
N = 30
s_series = sum(((-1.0) ** k) / (math.factorial(k) * (2 * k + 1)) for k in range(N + 1))
# quadrature via fine Simpson
x = np.linspace(0, 1, 200001)
y = np.exp(-x ** 2)
s_quad = np.trapezoid(y, x)
print(f"  series     = {s_series:.12f}")
print(f"  quadrature = {s_quad:.12f}")
print(f"  diff = {abs(s_series-s_quad):.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
