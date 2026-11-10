# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 23 讲《数项级数》数值核对。
#   EXP1  geometric 1/2 + 1/4 + ... -> 1
#   EXP2  harmonic partial sums grow
#   EXP3  sum 1/n^2 -> pi^2/6
#   EXP4  sum n/2^n -> 2
#   EXP5  telescoping sum 1/(n(n+1)) -> 1
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: geometric 1/2 + 1/4 + ... -> 1 ===")
N = 60
n = np.arange(1, N + 1)
s = np.sum(0.5 ** n)
print(f"  partial sum (N={N}) = {s:.12f}, exact = 1, diff = {abs(s-1):.2e}")
print()

print("=== EXP2: harmonic partial sums grow (H_10, H_100, H_1000, H_10000) ===")
for N in [10, 100, 1000, 10000]:
    h = np.sum(1.0 / np.arange(1, N + 1))
    print(f"  H_{N:<6} = {h:.6f}   (ln N + gamma = {math.log(N) + 0.5772156649:.6f})")
print("  -> slow growth, no bound")
print()

print("=== EXP3: sum 1/n^2 -> pi^2/6 ===")
N = 1_000_000
n = np.arange(1, N + 1, dtype=float)
s3 = np.sum(1.0 / (n ** 2))
exact = math.pi ** 2 / 6
print(f"  partial sum (N={N}) = {s3:.10f}, exact = {exact:.10f}, diff = {abs(s3-exact):.2e}")
print()

print("=== EXP4: sum n/2^n -> 2 ===")
N = 80
n = np.arange(1, N + 1, dtype=float)
s4 = np.sum(n / (2.0 ** n))
print(f"  partial sum (N={N}) = {s4:.12f}, exact = 2, diff = {abs(s4-2):.2e}")
print()

print("=== EXP5: telescoping sum 1/(n(n+1)) -> 1 ===")
N = 100000
n = np.arange(1, N + 1, dtype=float)
s5 = np.sum(1.0 / (n * (n + 1)))
print(f"  partial sum (N={N}) = {s5:.12f}, exact = 1, diff = {abs(s5-1):.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
