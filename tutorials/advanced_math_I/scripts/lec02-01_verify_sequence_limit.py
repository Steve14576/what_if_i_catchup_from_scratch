# 规模纪律：小规模扫描（每实验扫描 <= 5000 项；EXP1 的 N 最大 1e9 但只扫尾部 1000 项），目标 < 2 秒。
# 第 02 讲《数列的极限》数值验证，四个实验：
#   EXP1  对抗游戏实况: a_n = 1/n -> 0。对手出一串 eps，程序用 N = ceil(1/eps) 接招，
#         扫描尾部 1000 项全体核对 |a_n| < eps；并用更宽裕的 N' = 2N 复验（N 不唯一）。
#   EXP2  摆动数列收敛（机器版验证）vs (-1)^n 发散（机器版判负：任何 N 后都有漏网项）。
#   EXP3  0.999... = 1 的实弹射击: s_n = 1 - 10^-n，N = ceil(log10(1/eps))；附浮点彩蛋
#         （机器上 s_n 被舍入成 1.0 的起始位置——舍入不是到达）。
#   EXP4  量词顺序的机器版: 常数列（同一个 N 接住一切 eps）vs 1/n（N 必须随 eps 增大）。
import math
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: 对抗游戏实况 ============
print("=== EXP1: 对抗游戏实况, a_n = 1/n -> 0 ===")
for eps in [0.1, 0.01, 1e-3, 1e-6, 1e-9]:
    N = math.ceil(1.0 / eps)
    worst = np.max(1.0 / np.arange(N + 1, N + 1001))       # 尾部 1000 项全体
    N2 = 2 * N                                              # 更宽裕的 N（N 不唯一）
    worst2 = np.max(1.0 / np.arange(N2 + 1, N2 + 1001))
    print(f"  eps = {eps:g}: N = {N}, 尾部1000项 max|a_n| = {worst:.3e} (< eps? {worst < eps})"
          f" ; 宽裕版 N' = {N2}: max = {worst2:.3e} (< eps? {worst2 < eps})")
print("  -> 每轮都接得住; eps 缩小 10 倍 N 长大 10 倍 (N 依赖 eps); 取更大的 N 同样合法 (N 不唯一)")
print()

# ============ EXP2: 摆动数列收敛 vs (-1)^n 发散 ============
print("=== EXP2: 摆动数列收敛 vs (-1)^n 发散(机器版) ===")

def swing(n):            # 第五节例 3: n 奇 -> 2/(n+1), n 偶 -> 0
    return 2.0 / (n + 1) if n % 2 == 1 else 0.0

eps = 1e-2
N = math.ceil(2.0 / eps)
ns = np.arange(N + 1, N + 5001)
vals = np.array([swing(int(n)) for n in ns])
worst = np.max(np.abs(vals))
print(f"  摆动数列: eps = {eps:g}, N = ceil(2/eps) = {N}, 扫描 {len(ns)} 项, max|a_n| = {worst:.6f} (< eps? {worst < eps})")
print("  -> 一跳一停地走路, 尾部照样全体进带: 收敛 (第五节例 3 的机器版)")
# (-1)^n 判负: eps0 = 0.9, 任何 N 后都找得到距候选靶心 >= eps0 的漏网项
eps0 = 0.9
a = lambda n: 1.0 if n % 2 == 0 else -1.0
for N2 in [1, 10, 100, 1000, 1000000]:
    n_odd = N2 + 1 if (N2 + 1) % 2 == 1 else N2 + 2       # 距候选 A=1 的漏网项(奇数项, 值 -1)
    n_even = N2 + 1 if (N2 + 1) % 2 == 0 else N2 + 2      # 距候选 A=-1 的漏网项(偶数项, 值 1)
    d1 = abs(a(n_odd) - 1.0)
    d2 = abs(a(n_even) + 1.0)
    print(f"  (-1)^n: N = {N2:7d}: 漏网项 n = {n_odd:7d} 距 A=1 为 {d1:.0f} (>= {eps0});"
          f" n = {n_even:7d} 距 A=-1 为 {d2:.0f} (>= {eps0})")
    assert d1 >= eps0 and d2 >= eps0
print("  -> 对任何 N 都接不住 eps0 = 0.9 (两个候选靶心都判负): 发散 = 定义否定式的机器版")
print()

# ============ EXP3: 0.999... = 1 ============
print("=== EXP3: 0.999... = 1, s_n = 1 - 10^-n ===")
for eps in [1e-3, 1e-6, 1e-9]:
    N = math.ceil(math.log10(1.0 / eps))
    ns = np.arange(N + 1, N + 1000)
    worst = np.max(np.abs((1.0 - np.power(10.0, -ns)) - 1.0))
    print(f"  eps = {eps:g}: N = ceil(log10(1/eps)) = {N}, 尾部扫描 max|s_n - 1| = {worst:.3e} (< eps? {worst < eps})")
    assert worst < eps
# 浮点彩蛋: 机器上 s_n 提前"到达" 1
n_star = None
for n in range(1, 40):
    if 1.0 - 10.0 ** (-n) == 1.0:
        n_star = n
        break
print(f"  浮点彩蛋: 机器上 1 - 10^-n == 1.0 从 n = {n_star} 开始 (float64 到 1 的最后一级台阶约 1.1e-16 宽)")
print(f"  -> 数学上 s_n 永不等于 1 (差恒为 10^-n > 0); 机器上 n >= {n_star} 就被舍入成 1.0: 舍入不是到达")
print()

# ============ EXP4: 量词顺序的机器版 ============
print("=== EXP4: 量词顺序的机器版, 常数列 5 vs 1/n ===")
print("  常数列 a_n = 5: 同一个 N = 1 接住一切 eps (尾部恒为 5, 距离恒为 0):")
for eps in [0.5, 0.1, 0.01, 1e-4, 1e-8]:
    ok = abs(5.0 - 5.0) < eps
    print(f"    eps = {eps:g}: N = 1, |5 - 5| = 0 < eps? {ok}")
    assert ok
print("  对照 1/n -> 0: N 必须看着 eps 出 (N 随 eps 缩小而增大):")
for eps in [0.5, 0.1, 0.01, 1e-4, 1e-8]:
    print(f"    eps = {eps:g}: N = ceil(1/eps) = {math.ceil(1.0 / eps)}")
print("  -> 常数列是'万能 N'的唯一居民 (量词可交换的那类); 1/n 的 N 依赖 eps: 逼近不是到达")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
