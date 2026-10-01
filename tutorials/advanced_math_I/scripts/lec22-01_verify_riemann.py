# 规模纪律：n 最大 1e4 的向量化求和, 目标 < 2 秒。
# 第 22 讲《定积分：黎曼和》数值验证，四个实验：
#   EXP1  int_0^1 x^2 dx 右端点和收敛表 (趋向 1/3, 误差 ~1/(2n))。
#   EXP2  int_0^1 x dx 三种取点 (左/右/中点, 同趋 1/2)。
#   EXP3  int_{-1}^1 x dx 有向抵消 (右端点趋 0; 中点恒 0)。
#   EXP4  不均匀分割反例: n->无穷 但 lambda 恒 0.5, 和 -> 1/3 (真值 1/2)。
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: x^2 右端点和 ============
print("=== EXP1: int_0^1 x^2 dx, 右端点和 ===")
for n in [10, 100, 1000, 10000]:
    i = np.arange(1, n + 1)
    S = np.sum((i / n) ** 2) / n
    print(f"  n = {n:6d}: S = {S:.8f}, 与 1/3 的差 = {S - 1 / 3:+.2e} (理论 ~1/(2n) 级)")
print("  -> 单调下降趋 1/3: 收敛但慢 (定义级计算的代价)")
print()

# ============ EXP2: 三取点 ============
print("=== EXP2: int_0^1 x dx, 三种取点 ===")
for n in [10, 100, 1000]:
    i = np.arange(1, n + 1)
    SL = np.sum((i - 1) / n) / n
    SR = np.sum(i / n) / n
    SM = np.sum((2 * i - 1) / (2 * n)) / n
    print(f"  n = {n:5d}: 左 = {SL:.8f}, 右 = {SR:.8f}, 中 = {SM:.8f}")
print("  -> 三列夹向 1/2: 取点任意性的数值现场")
print()

# ============ EXP3: 有向抵消 ============
print("=== EXP3: int_{-1}^1 x dx, 有向抵消 ===")
for n in [10, 100, 1000]:
    i = np.arange(1, n + 1)
    SR = np.sum((-1 + 2 * i / n) * (2 / n))          # 右端点
    SM = np.sum((-1 + (2 * i - 1) / n) * (2 / n))    # 中点
    print(f"  n = {n:5d}: 右端点和 = {SR:.8f}, 中点和 = {SM:.8f}")
print("  -> 右端点趋 0, 中点恒 0: 对称抵消")
print()

# ============ EXP4: 不均匀分割反例 ============
print("=== EXP4: 不均匀分割: n 增而 lambda 恒 0.5, 和 -> 1/3 ===")
S = 0.0
for k in range(1, 41):
    x_left = 1 - 2.0 ** (-k)
    dx = 2.0 ** (-(k + 1))
    S += x_left * dx
    if k in [1, 2, 3, 5, 10]:
        print(f"  k = {k:2d}: 段数 = {k}, lambda = 0.5 (恒), 累计和 = {S:.8f}")
print(f"  k = 40: 段数 = 40, 累计和 = {S:.10f}")
print(f"  与 1/3 的差 = {S - 1 / 3:+.2e}; 与真值 1/2 的差 = {S - 0.5:+.4f}")
print("  -> n->无穷 但 lambda 不趋 0: 和收敛到错值 1/3, 真值 1/2")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")