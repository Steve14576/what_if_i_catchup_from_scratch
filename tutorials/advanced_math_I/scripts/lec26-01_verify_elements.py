# 规模纪律：Simpson 与弦长和, 目标 < 2 秒。
# 第 26 讲《几何应用：元素法》数值验证，四个实验：
#   EXP1  变量选择: int_{-1}^2 [(y+2)-y^2] dy = 9/2。
#   EXP2  盘/环: 球 4pi/3; 环 64pi/15。
#   EXP3  弧长双对照: 弦长和 -> ln(1+sqrt2); delta-x 和恒 pi/4。
#   EXP4  极坐标与功: 心形线 3pi/2; 弹簧 9。
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

# ============ EXP1: 变量选择 ============
print("=== EXP1: int_{-1}^2 [(y+2)-y^2] dy = 9/2 ===")
A = simpson(lambda y: (y + 2) - y ** 2, -1, 2)
print(f"  数值 = {A:.10f}, 解析 = 4.5, 差 = {A - 4.5:+.2e}")
print("  -> 横切一句完的对账")
print()

# ============ EXP2: 盘/环 ============
print("=== EXP2: 球体与圆环 ===")
V1 = math.pi * simpson(lambda x: 1 - x ** 2, -1, 1)
V2 = math.pi * simpson(lambda x: (2 * x) ** 2 - (x ** 2) ** 2, 0, 2)
print(f"  球: 数值 = {V1:.10f}, 4pi/3 = {4 * math.pi / 3:.10f}, 相对差 = {abs(V1 - 4 * math.pi / 3) / (4 * math.pi / 3):.2e}")
print(f"  环: 数值 = {V2:.10f}, 64pi/15 = {64 * math.pi / 15:.10f}, 相对差 = {abs(V2 - 64 * math.pi / 15) / (64 * math.pi / 15):.2e}")
print("  -> 盘/环公式双验证")
print()

# ============ EXP3: 弧长双对照 ============
print("=== EXP3: 弦长和 vs delta-x 和 (y = ln cos x, [0, pi/4]) ===")
exact_arc = math.log(1 + math.sqrt(2))
for n in [1000, 10000]:
    x = np.linspace(0, math.pi / 4, n + 1)
    y = np.log(np.cos(x))
    chord = np.sum(np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2))
    dxsum = np.sum(np.diff(x))
    print(f"  n = {n}: 弦长和 = {chord:.8f} (弧长 {exact_arc:.8f}, 差 {chord - exact_arc:+.2e}); delta-x 和 = {dxsum:.8f} (恒 pi/4)")
print("  -> 弦长收敛; delta-x 和永不收敛 (一阶误差)")
print()

# ============ EXP4: 极坐标与功 ============
print("=== EXP4: 心形线面积与弹簧做功 ===")
A2 = 0.5 * simpson(lambda t: (1 + np.cos(t)) ** 2, 0, 2 * math.pi)
W = simpson(lambda x: 2 * x, 0, 3)
print(f"  心形线: 数值 = {A2:.10f}, 3pi/2 = {3 * math.pi / 2:.10f}, 相对差 = {abs(A2 - 3 * math.pi / 2) / (3 * math.pi / 2):.2e}")
print(f"  弹簧 (k=2, L=3): 数值 = {W:.10f}, 解析 = 9")
print("  -> 两个插件的对账")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")