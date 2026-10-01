# 规模纪律：Simpson + 一处 2e5 加密, 目标 < 2 秒。
# 第 27 讲（重写版）矩系列数值验证，三个实验：
#   EXP1  半圆盘三矩: A=pi/2, My=0(对称), Mx=2/3, ybar=4/(3pi)。
#   EXP2  平行轴定理双路: Ix=pi/8; Ic 直接积分 vs Ix - A*ybar^2。
#   EXP3  曲线形心: 半圆弧 ybar_c = 2/pi。
# 注: 被积函数一律 np.*。
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

# ============ EXP1: 半圆盘三矩 ============
print("=== EXP1: semicircle disk moments (R=1) ===")
# 端点奇性: sqrt(1-x^2) 在 x=±1 有垂直切线, 加密到 n=2e5
A = simpson(lambda x: np.sqrt(1 - x ** 2), -1, 1, n=200000)
My = simpson(lambda x: x * np.sqrt(1 - x ** 2), -1, 1, n=200000)
Mx = simpson(lambda x: (1 - x ** 2) / 2, -1, 1)
print(f"  A  = {A:.10f} (pi/2 = {math.pi / 2:.10f})")
print(f"  My = {My:.2e} (odd symmetry -> machine zero)")
print(f"  Mx = {Mx:.10f} (2/3 = {2 / 3:.10f})")
print(f"  ybar = Mx/A = {Mx / A:.10f} (4/(3pi) = {4 / (3 * math.pi):.10f})")
print()

# ============ EXP2: 平行轴定理双路 ============
print("=== EXP2: parallel-axis theorem, two routes (R=1) ===")
ybar = 4 / (3 * math.pi)
Ix = simpson(lambda x: (1 - x ** 2) ** 1.5, -1, 1, n=200000) / 3
Ic_direct = simpson(lambda x: (np.sqrt(1 - x ** 2) ** 3) / 3
                    - ybar * (1 - x ** 2) + ybar ** 2 * np.sqrt(1 - x ** 2), -1, 1, n=200000)
Ic_shift = Ix - A * ybar ** 2
print(f"  Ix = {Ix:.10f} (pi/8 = {math.pi / 8:.10f})")
print(f"  Ic (direct) = {Ic_direct:.10f}")
print(f"  Ic (Ix - A*ybar^2) = {Ic_shift:.10f}, 差 = {abs(Ic_direct - Ic_shift):.2e}")
print()

# ============ EXP3: 曲线形心 ============
print("=== EXP3: semicircle arc centroid (R=1) ===")
ybar_c = simpson(np.sin, 0.0, math.pi, n=20000) / math.pi
print(f"  ybar_c = {ybar_c:.10f} (2/pi = {2 / math.pi:.10f})")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")