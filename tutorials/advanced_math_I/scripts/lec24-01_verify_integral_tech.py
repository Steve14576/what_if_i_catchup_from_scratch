# 规模纪律：纯打印表 + Simpson n<=2000, 目标 < 2 秒。
# 第 24 讲《定积分的计算技术》数值验证，四个实验：
#   EXP1  换限对账 + "忘换限"代价: int_0^2 x sqrt(x^2+1)。
#   EXP2  对称性: int_{-1}^1 x^3 = 0; int_{-1}^1 x^2 = 2/3。
#   EXP3  华里士: W4, W5; 及 int_0^pi sin^4 = 2W4 (区间误用对照)。
#   EXP4  区间再现: int_0^pi x sin x = pi; 再现两版数值相等。
import math
import time

import numpy as np

T0 = time.perf_counter()

def simpson(f, a, b, n=2000):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h / 3 * (y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]))

# ============ EXP1: 换限对账 ============
print("=== EXP1: int_0^2 x sqrt(x^2+1) dx ===")
num = simpson(lambda x: x * np.sqrt(x ** 2 + 1), 0, 2)
exact = (5 * math.sqrt(5) - 1) / 3
wrong = 4 * math.sqrt(2) / 3
print(f"  数值 = {num:.10f}, 解析 (5sqrt5-1)/3 = {exact:.10f}, 相对差 = {abs(num - exact) / exact:.2e}")
print(f"  忘换限值 4sqrt2/3 = {wrong:.10f}, 与真值差 = {abs(wrong - exact):.4f}")
print("  -> 必换限的量化证据")
print()

# ============ EXP2: 对称性 ============
print("=== EXP2: int_{-1}^1 x^3 = 0; int_{-1}^1 x^2 = 2/3 ===")
n1 = simpson(lambda x: x ** 3, -1, 1)
n2 = simpson(lambda x: x ** 2, -1, 1)
print(f"  x^3: 数值 = {n1:.3e} (理论 0); x^2: 数值 = {n2:.10f} (理论 {2/3:.10f})")
print("  -> 奇消偶倍的两行实弹")
print()

# ============ EXP3: 华里士与区间误用 ============
print("=== EXP3: W4 = 3pi/16, W5 = 8/15; int_0^pi sin^4 vs W4/2W4 ===")
W4 = 3 * math.pi / 16
W5 = 8 / 15
nW4 = simpson(lambda x: np.sin(x) ** 4, 0, math.pi / 2)
nW5 = simpson(lambda x: np.sin(x) ** 5, 0, math.pi / 2)
nfull = simpson(lambda x: np.sin(x) ** 4, 0, math.pi)
print(f"  W4: 数值 = {nW4:.10f}, 解析 = {W4:.10f}; W5: 数值 = {nW5:.10f}, 解析 = {W5:.10f}")
print(f"  int_0^pi sin^4: 数值 = {nfull:.10f}, 直接套W4 = {W4:.10f}, 2W4 = {2*W4:.10f}")
print("  -> '直接套差两倍'的活体")
print()

# ============ EXP4: 区间再现 ============
print("=== EXP4: int_0^pi x sin x = pi; 再现两版相等 ===")
nA = simpson(lambda x: x * np.sin(x), 0, math.pi)
nB = simpson(lambda x: (math.pi - x) * np.sin(x), 0, math.pi)
print(f"  数值 = {nA:.10f}, pi = {math.pi:.10f}, 差 = {nA - math.pi:+.2e}")
print(f"  再现版数值 = {nB:.10f}, 与直接版差 = {nB - nA:+.2e}")
print("  -> 翻面不变账的实弹")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")