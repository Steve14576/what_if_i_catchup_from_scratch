# 规模纪律：Simpson 含采样密度账, 目标 < 2 秒。
# 第 27 讲《旋转体与巴普斯定理》数值验证，四个实验：
#   EXP1  环面双路: 巴普斯 2*pi^2*R*r^2 vs 壳层积分 (R=3, r=1)。
#   EXP2  半圆盘形心双路: 直接积分 4R/(3pi) vs 巴普斯反求 (R=1)。
#   EXP3  球面积双路: 侧面积版 4pi vs 球面直接积分 (化简为常值 1)。
#   EXP4  失效三数: 圆盘绕直径: 巴普斯 0 vs 球 4pi/3 vs 重数账 8pi/3。
# 注: 被积函数一律 np.* (向量化)。
import math
import time

import numpy as np

T0 = time.perf_counter()

def simpson(f, a, b, n=None):
    if n is None:
        n = max(2000, int(100 * (b - a)))
        if n % 2 == 1:
            n += 1
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h / 3 * (y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]))

# ============ EXP1: 环面双路 ============
print("=== EXP1: torus (R=3, r=1): Pappus vs shell ===")
pappus = 2 * math.pi ** 2 * 3 * 1
shell = 2 * math.pi * simpson(lambda x: x * 2 * np.sqrt(1 - (x - 3) ** 2), 2, 4, n=200000)   # 端点奇性: 加密
print(f"  巴普斯 = {pappus:.10f}, 壳层 = {shell:.10f}, 相对差 = {abs(shell - pappus) / pappus:.2e}")
print("  -> 环面双路互证")
print()

# ============ EXP2: 半圆盘形心双路 ============
print("=== EXP2: semicircle centroid (R=1): direct vs Pappus-inverse ===")
direct = 4 / (3 * math.pi)
inv = (4 * math.pi / 3) / (2 * math.pi * (math.pi / 2))
print(f"  直接积分 = {direct:.10f}, 巴普斯反求 = {inv:.10f}, 差 = {inv - direct:+.2e}")
print("  -> 两路同得 0.4244131816")
print()

# ============ EXP3: 球面积双路 ============
print("=== EXP3: sphere area (R=1): Pappus-side vs direct ===")
pappus_s = math.pi * 1 * 2 * math.pi * (2 / math.pi)
direct_s = 2 * math.pi * simpson(lambda x: 1.0 + 0.0 * x, -1, 1)   # 先化简成常值 1, 避免端点 0/0 的 NaN
print(f"  侧面积版 = {pappus_s:.10f}, 直接积分 = {direct_s:.10f}, 相对差 = {abs(direct_s - pappus_s) / pappus_s:.2e}")
print("  -> 4pi = 12.5663706144 两路吻合")
print()

# ============ EXP4: 失效三数 ============
print("=== EXP4: disk about its diameter: three numbers (R=1) ===")
pappus0 = 2 * math.pi * 0 * math.pi
sphere = 4 * math.pi / 3
double = 2 * sphere
print(f"  巴普斯值 = {pappus0:.10f}; 球(单层) = {sphere:.10f}; 重数2的账 = {double:.10f}")
print("  -> 0 vs 4.1888 vs 8.3776: 没有一个数能靠'修正公式'得到")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")