# 规模纪律：向量化 np.sum 为主, 目标 < 2 秒。
# 第 31 讲《与高数下的接口》收官三实验：
#   EXP1  级数收敛肖像: sum 1/n^2 -> pi^2/6; 对照 sum 1/n (log 增长)。
#   EXP2  泰勒级数部分和: sin at x=1, 阶数 1,3,5,7,9。
#   EXP3  eps-N 机器仪式: 1/n < eps 的最小 N = ceil(1/eps)。
import math
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: 级数收敛肖像 ============
print("=== EXP1: series convergence portraits ===")
target = math.pi ** 2 / 6
for N in [10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5]:
    S = np.sum(1.0 / np.arange(1, N + 1) ** 2)
    print(f"  sum 1/n^2, N = {N:>6}: S = {S:.10f}, pi^2/6 - S = {target - S:.2e}")
for N in [10 ** 2, 10 ** 3, 10 ** 4]:
    H = np.sum(1.0 / np.arange(1, N + 1))
    print(f"  sum 1/n,   N = {N:>6}: S = {H:.6f} (log 增长, 发散)")
print("  -> 1/n^2 慢收敛 (O(1/N)); 1/n 永不停")
print()

# ============ EXP2: 泰勒级数部分和 ============
print("=== EXP2: Taylor partial sums of sin at x=1 ===")
x = 1.0
s = 0.0
term = x
for k in range(1, 12, 2):   # 阶数 1..11
    s = s + term
    print(f"  order {k}: S = {s:.12f}, err = {abs(s - math.sin(x)):.2e}")
    term = -term * x * x / ((k + 1) * (k + 2))
print("  -> 误差被下一项接管: 9 阶 err ~ 1/11!; 11 阶 err ~ 1/13!")
print()

# ============ EXP3: eps-N 机器仪式 ============
print("=== EXP3: smallest N with 1/n < eps ===")
for eps in [1e-2, 1e-3, 1e-6]:
    N = 1
    while 1.0 / N >= eps:
        N += 1
    print(f"  eps = {eps:.0e}: N = {N} (= floor(1/eps)+1 = {math.floor(1 / eps) + 1})")
print("  -> 严格小于的边界: n=1/eps 时值恰好等于 eps, 不算小 -> 最小整数多 1")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")