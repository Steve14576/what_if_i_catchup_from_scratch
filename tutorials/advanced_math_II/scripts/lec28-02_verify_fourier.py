# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 28 讲《傅里叶级数》数值核对。
#   EXP1  square wave partial sums at x=0.5
#   EXP2  sawtooth f(x)=x at x=1
#   EXP3  x^2 cosine series at x=0
#   EXP4  orthogonality integral sin x sin 2x
#   EXP5  square wave at the jump x=0 -> midpoint 0
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: square wave partial sums at x=0.5 ===")
x = 0.5
for N in [1, 3, 5, 9, 50]:
    s = sum(math.sin((2 * k + 1) * x) / (2 * k + 1) for k in range(N))
    val = 4 / math.pi * s
    print(f"  N={N:<3}: partial sum = {val:.10f}  (square wave = 1)")
print()

print("=== EXP2: sawtooth f(x)=x at x=1 ===")
x = 1.0
for N in [1, 3, 5, 9, 100]:
    s = sum(((-1) ** (n - 1)) / n * math.sin(n * x) for n in range(1, N + 1))
    val = 2 * s
    print(f"  N={N:<4}: partial sum = {val:.10f}  (f(x) = 1)")
print()

print("=== EXP3: x^2 cosine series at x=0 ===")
# at x=0: pi^2/3 + 4 * sum (-1)^n/n^2 should be 0
for N in [10, 100, 1000, 10000]:
    s = math.pi ** 2 / 3 + 4 * sum(((-1) ** n) / n ** 2 for n in range(1, N + 1))
    print(f"  N={N:<6}: partial sum = {s:.10f}  (f(0) = 0)")
print()

print("=== EXP4: orthogonality integral sin x sin 2x ===")
x = np.linspace(-np.pi, np.pi, 200001)
integral = np.trapezoid(np.sin(x) * np.sin(2 * x), x)
print(f"  integral = {integral:.3e}  (expect 0)")
# and the norm
norm = np.trapezoid(np.sin(x) ** 2, x)
print(f"  integral sin^2 x = {norm:.10f}  (expect pi = {math.pi:.10f})")
print()

print("=== EXP5: square wave at the jump x=0 -> midpoint 0 ===")
for N in [1, 3, 9, 99]:
    s = sum(math.sin((2 * k + 1) * 0.0) / (2 * k + 1) for k in range(N))
    print(f"  N={N:<3}: partial sum at x=0 = {4/math.pi*s:.3e}  (midpoint = 0)")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
