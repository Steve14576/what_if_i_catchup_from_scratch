# 规模纪律：小规模打印表（最大求和 n=10^4 项），目标 < 2 秒。
# 第 05 讲《存在判据与两个重要极限》数值验证，四个实验：
#   EXP1  sin(x)/x 的两个过程两种命运: x -> 0 双侧趋 1; x -> +inf 趋 0。
#   EXP2  (1+1/n)^n 单调增长与 e 逼近: n 上升, a_n 上升, a_n - e < 0 且缩向 0。
#   EXP3  sqrt2 递推收敛轨迹: a1 = sqrt2, a_{n+1} = sqrt(2 + a_n)，20 步爬向 2。
#   EXP4  n 项分母型夹逼三列: 左界 n/sqrt(n^2+n) <= S_n <= n/sqrt(n^2+1) 右界，同趋 1。
import math
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: sin(x)/x 的两个过程 ============
print("=== EXP1: sin(x)/x, 两个过程两种命运 ===")
print("  x -> 0 双侧:")
for x in [0.5, -0.5, 0.1, -0.1, 0.01, -0.01, 1e-4, -1e-4, 1e-6, -1e-6]:
    print(f"    x = {x:+.1e}: sin(x)/x = {np.sin(x) / x:.10f}")
print("  x -> +inf:")
for x in [10.0, 100.0, 1000.0, 10000.0, 1000000.0]:
    print(f"    x = {x:10.1e}: sin(x)/x = {np.sin(x) / x:+.3e}")
print("  -> 同一式子: x->0 压向 1 (第五节定理), x->+inf 压向 0 (有界乘无穷小)")
print()

# ============ EXP2: (1+1/n)^n 与 e ============
print("=== EXP2: (1+1/n)^n 单调增长与 e 逼近 ===")
for n in [1, 2, 5, 10, 100, 10 ** 3, 10 ** 4, 10 ** 6]:
    v = (1.0 + 1.0 / n) ** n
    print(f"  n = {n:>9}: a_n = {v:.12f}, a_n - e = {v - math.e:+.3e}")
print("  -> 逐步上升、不越过 e、差值缩向 0: 单调有界原理的数据版")
print()

# ============ EXP3: sqrt2 递推 ============
print("=== EXP3: a1 = sqrt2, a_{n+1} = sqrt(2 + a_n) 的收敛轨迹 ===")
a = math.sqrt(2.0)
for i in range(1, 21):
    print(f"  n = {i:2d}: a_n = {a:.10f}, 2 - a_n = {2.0 - a:+.3e}")
    a = math.sqrt(2.0 + a)
print("  -> 从 1.4142... 单调爬向 2: 例 3 全过程的数据版")
print()

# ============ EXP4: n 项分母型夹逼三列 ============
print("=== EXP4: n 项分母型, 左界 <= S_n <= 右界 ===")
for n in [10, 100, 1000, 10 ** 4]:
    k = np.arange(1, n + 1)
    S = np.sum(1.0 / np.sqrt(n * n + k))
    lo = n / math.sqrt(n * n + n)
    hi = n / math.sqrt(n * n + 1)
    print(f"  n = {n:>6}: 左界 = {lo:.10f}, S_n = {S:.10f}, 右界 = {hi:.10f}")
    assert lo <= S <= hi
print("  -> 三列同趋 1 (S_n 始终夹在中间): 例 1 的'夹住'数值形态")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")