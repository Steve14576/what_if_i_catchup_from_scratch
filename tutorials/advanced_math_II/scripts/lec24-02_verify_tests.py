# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 24 讲《正项级数判别法》数值核对。
#   EXP1  sum 1/(2n+1) grows like (1/2) ln N
#   EXP2  sum n/(n^2+1) grows like ln N
#   EXP3  sum 1/(n ln n) grows like ln ln N
#   EXP4  sum (1-cos(1/n)) -> pi^2/12
#   EXP5  sum (n/(3n+1))^n converges
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: sum 1/(2n+1) grows like (1/2) ln N ===")
for N in [100, 1000, 10000]:
    n = np.arange(1, N + 1, dtype=float)
    s = np.sum(1.0 / (2 * n + 1))
    print(f"  N={N:<6}: sum={s:.6f}   0.5 ln N={0.5*math.log(N):.6f}")
print("  -> both grow; difference is bounded")
print()

print("=== EXP2: sum n/(n^2+1) grows like ln N ===")
for N in [100, 1000, 10000]:
    n = np.arange(1, N + 1, dtype=float)
    s = np.sum(n / (n ** 2 + 1))
    print(f"  N={N:<6}: sum={s:.6f}   ln N={math.log(N):.6f}")
print()

print("=== EXP3: sum 1/(n ln n) grows like ln ln N ===")
for N in [100, 1000, 10000]:
    n = np.arange(2, N + 1, dtype=float)
    s = np.sum(1.0 / (n * np.log(n)))
    print(f"  N={N:<6}: sum={s:.6f}   ln ln N={math.log(math.log(N)):.6f}")
print()

print("=== EXP4: sum (1-cos(1/n)) converges (limit ~0.7788) ===")
N = 2000000
n = np.arange(1, N + 1, dtype=float)
s4 = np.sum(1.0 - np.cos(1.0 / n))
print(f"  partial sum (N={N}) = {s4:.10f}")
print(f"  pi^2/12 = {math.pi**2/12:.10f} (only the leading 1/(2n^2) term; difference is the n^-4 term)")
print()

print("=== EXP5: sum (n/(3n+1))^n converges ===")
N = 400
n = np.arange(1, N + 1, dtype=float)
s5 = np.sum((n / (3 * n + 1)) ** n)
print(f"  partial sum (N={N}) = {s5:.10f}")
print(f"  next 100 terms add   = {np.sum((np.arange(N+1, N+101)/(3*np.arange(N+1, N+101)+1))**np.arange(N+1, N+101)):.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
