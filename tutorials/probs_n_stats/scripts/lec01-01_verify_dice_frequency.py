# =====================================================================
# lec01-01 骰子频率 vs 理论概率（第 01 讲 §3.1 / §4.2）
# 规模纪律：总耗时 < 3 秒（最大 N=100000 组实验常驻秒级）。
# 方法：两枚六面骰子，随机掷 N 次，统计事件频率，对照理论概率。
# 理论值：P(和=7)=6/36=1/6；P(和为偶数)=18/36=1/2；P(两骰相同)=6/36=1/6。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
# =====================================================================
import numpy as np

rng = np.random.default_rng(seed=20260920)


def freq_of_sum_is(N, target_sum):
    """掷 N 次两骰，返回 '和为 target_sum' 的频率。"""
    d1 = rng.integers(1, 7, size=N)
    d2 = rng.integers(1, 7, size=N)
    s = d1 + d2
    return np.mean(s == target_sum)


def freq_of_even_sum(N):
    """掷 N 次两骰，返回 '和为偶数' 的频率。"""
    d1 = rng.integers(1, 7, size=N)
    d2 = rng.integers(1, 7, size=N)
    s = d1 + d2
    return np.mean(s % 2 == 0)


def freq_of_doubles(N):
    """掷 N 次两骰，返回 '两骰相同' 的频率。"""
    d1 = rng.integers(1, 7, size=N)
    d2 = rng.integers(1, 7, size=N)
    return np.mean(d1 == d2)


print("实验 1：两骰和 = 7，理论 P = %.6f = 1/6" % (1 / 6))
print("  N 越大，频率越接近理论值（频率 -> 概率）：")
for N in [100, 1_000, 10_000, 100_000]:
    f = freq_of_sum_is(N, 7)
    print("    N=%7d  频率=%.6f  与1/6差距=%.6f" % (N, f, abs(f - 1 / 6)))
print("-> 结论：频率围绕 1/6 波动，N 增大后波动收窄，这是概率公理化前的经验基础。")

print("实验 2：两骰和为偶数，理论 P = 0.500000 = 1/2")
for N in [1_000, 100_000]:
    f = freq_of_even_sum(N)
    print("    N=%7d  频率=%.6f" % (N, f))
print("-> 结论：补集事件 P(偶数)=1-P(奇数)=1/2 与模拟一致（§3.3 性质）。")

print("实验 3：两骰相同（double），理论 P = %.6f = 1/6" % (1 / 6))
for N in [1_000, 100_000]:
    f = freq_of_doubles(N)
    print("    N=%7d  频率=%.6f" % (N, f))
print("-> 结论：'两骰相同'这类 6 个结果之和占 36 个结果的 6/36=1/6，模拟坐实。")
print("[OK] 三组实验全部完成，耗时在秒级。")