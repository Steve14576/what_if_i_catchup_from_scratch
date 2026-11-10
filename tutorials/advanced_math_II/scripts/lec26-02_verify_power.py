# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 26 讲《幂级数》数值核对。
#   EXP1  sum x^n at x=0.5 -> 2
#   EXP2  sum x^n/n at x=-0.5 -> -ln(1.5)
#   EXP3  radius of sum (x-1)^n/(n 2^n) -> R = 2
#   EXP4  derivative sum n x^(n-1) at x=0.5 -> 1/(1-0.5)^2 = 4
#   EXP5  endpoint x=1 diverges, x=-1 converges
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: sum x^n at x=0.5 -> 2 ===")
x = 0.5
N = 100
s1 = np.sum(x ** np.arange(0, N + 1))
print(f"  partial sum (N={N}) = {s1:.12f}, exact = 1/(1-x) = {1/(1-x):.12f}, diff = {abs(s1-1/(1-x)):.2e}")
print()

print("=== EXP2: sum x^n/n at x=-0.5 -> -ln(1.5) ===")
x = -0.5
N = 100000
n = np.arange(1, N + 1, dtype=float)
s2 = np.sum(x ** n / n)
exact = -math.log(1 - x)
print(f"  partial sum (N={N}) = {s2:.12f}, exact = {exact:.12f}, diff = {abs(s2-exact):.2e}")
print()

print("=== EXP3: radius of sum (x-1)^n/(n 2^n) -> R = 2 ===")
# coefficient ratio
for n in [10, 100, 1000]:
    a_n = 1.0 / (n * 2.0 ** n)
    a_n1 = 1.0 / ((n + 1) * 2.0 ** (n + 1))
    print(f"  n={n:<5}: |a_n/a_(n+1)| = {a_n/a_n1:.6f} -> R = 2")
# numeric check inside/outside via the ratio |x-1|/2 (avoids overflow)
for x in [2.9, 3.1]:
    ratio = abs(x - 1) / 2.0
    verdict = "converges" if ratio < 1 else "diverges"
    print(f"  x={x}: |x-1|/2 = {ratio:.3f} {'<' if ratio < 1 else '>'} 1 -> {verdict}")
print()

print("=== EXP4: derivative sum n x^(n-1) at x=0.5 -> 4 ===")
x = 0.5
N = 200
n = np.arange(1, N + 1, dtype=float)
s4 = np.sum(n * x ** (n - 1))
print(f"  partial sum (N={N}) = {s4:.12f}, exact = 1/(1-x)^2 = {1/(1-x)**2:.12f}, diff = {abs(s4-4):.2e}")
print()

print("=== EXP5: endpoint x=1 diverges, x=-1 converges ===")
for N in [100, 1000, 10000]:
    pos = np.sum(1.0 / np.arange(1, N + 1))
    neg = np.sum((-1.0) ** np.arange(1, N + 1) / np.arange(1, N + 1))
    print(f"  N={N:<6}: x=1 sum={pos:.6f} (growing)   x=-1 sum={neg:.6f} (-> -ln2={-math.log(2):.6f})")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
