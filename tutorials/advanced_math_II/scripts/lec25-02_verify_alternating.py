# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 25 讲《交错级数与绝对收敛》数值核对。
#   EXP1  alternating harmonic -> ln 2
#   EXP2  remainder bound |S - S_n| <= a_{n+1}
#   EXP3  alternating 1/n^2 -> pi^2/12
#   EXP4  alternating 1/sqrt(n) converges (slowly)
#   EXP5  rearrangement changes the sum (ln 2 vs 1.5 ln 2)
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: alternating harmonic -> ln 2 ===")
N = 1_000_000
n = np.arange(1, N + 1, dtype=float)
s1 = np.sum((-1.0) ** (np.arange(1, N + 1) - 1) / n)
print(f"  partial sum (N={N}) = {s1:.10f}, ln 2 = {math.log(2):.10f}, diff = {abs(s1-math.log(2)):.2e}")
print()

print("=== EXP2: remainder bound |S - S_n| <= a_{n+1} ===")
S = math.log(2)
for N in [10, 100, 1000]:
    n = np.arange(1, N + 1, dtype=float)
    Sn = np.sum((-1.0) ** (np.arange(1, N + 1) - 1) / n)
    print(f"  n={N:<5}: |S-S_n|={abs(S-Sn):.6e}   a_(n+1)=1/{N+1}={1/(N+1):.6e}")
print()

print("=== EXP3: alternating 1/n^2 -> pi^2/12 ===")
N = 1_000_000
n = np.arange(1, N + 1, dtype=float)
s3 = np.sum((-1.0) ** (np.arange(1, N + 1) - 1) / n ** 2)
exact = math.pi ** 2 / 12
print(f"  partial sum = {s3:.10f}, pi^2/12 = {exact:.10f}, diff = {abs(s3-exact):.2e}")
print()

print("=== EXP4: alternating 1/sqrt(n) converges (slowly) ===")
for N in [1000, 10000, 100000]:
    n = np.arange(1, N + 1, dtype=float)
    s = np.sum((-1.0) ** (np.arange(1, N + 1) - 1) / np.sqrt(n))
    print(f"  N={N:<7}: partial sum = {s:.6f}")
print("  -> oscillates with shrinking amplitude; limit ~0.6049")
print()

print("=== EXP5: rearrangement changes the sum (ln 2 vs 1.5 ln 2) ===")
# two positive terms, then one negative: 1 + 1/3 - 1/2 + 1/5 + 1/7 - 1/4 + ...
M = 200000
pos = np.arange(1, 4 * M, 2, dtype=float)   # 1,3,5,... (2M terms)
pos_terms = 1.0 / pos                        # 1, 1/3, 1/5, ...
neg_terms = 1.0 / (2 * np.arange(1, M + 1, dtype=float))  # 1/2, 1/4, ...
terms = []
for i in range(M):
    terms.append(pos_terms[2 * i])
    terms.append(pos_terms[2 * i + 1])
    terms.append(-neg_terms[i])
s5 = np.sum(terms)
print(f"  rearranged partial sum = {s5:.10f}")
print(f"  1.5*ln2 = {1.5*math.log(2):.10f}, ln2 = {math.log(2):.10f}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
