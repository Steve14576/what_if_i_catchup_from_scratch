# 规模纪律：小规模打印表（最大网格 10^5 点 / 二分 30 步 / 6 组采样），目标 < 2 秒。
# 第 08 讲《闭区间上连续函数的性质》数值验证，四个实验：
#   EXP1  最值的开闭对照: f(x)=x 在 (0,1) 采样 max 永远 < 1 且差值随网格加密等比例缩; [0,1] 直接取 1。
#   EXP2  二分法实弹: F(x)=x-e^{-x} 在 [0,1] 二分, 第 10/20/30 步区间长 = 1/2^n, 中点趋根 0.567143...。
#   EXP3  不连续跳值: f={x, 0<=x<1; x+1, 1<=x<=2}, 值域跳过 (1,2), 与 1.5 的最小距离恒 0.5。
#   EXP4  不一致连续的数值指纹: 等比例小段 [1e-k, 2e-k] 上 1/x 的函数差 = 10^k/2 反而爆炸, x 的差 = 1e-k 缩零。
import math
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: 最值的开闭对照 ============
print("=== EXP1: f(x)=x 的开闭对照 (最大值) ===")
for m in [10 ** 3, 10 ** 4, 10 ** 5]:
    xs_open = np.linspace(1.0 / m, 1.0 - 1.0 / m, m)     # (0,1) 内采样
    print(f"  (0,1) 网格 {m:>7} 点: max = {xs_open.max():.10f}, 与 1 的差 = {1 - xs_open.max():.1e}")
xs_closed = np.linspace(0.0, 1.0, 10001)
print(f"  [0,1] 网格含端点: max = {xs_closed.max():.1f} (= 1.0, 直接取到)")
print("  -> 开区间: 在逼近、永远够不着; 闭区间: 取到 —— 上确界 vs 最大值的数值形态")
print()

# ============ EXP2: 二分法实弹 ============
print("=== EXP2: 二分法解 x = e^{-x} (F = x - e^{-x} = 0), [0, 1] ===")
F = lambda x: x - math.exp(-x)
a, b = 0.0, 1.0
for n in range(1, 31):
    c = (a + b) / 2
    if F(c) == 0:
        break
    if F(a) * F(c) < 0:
        b = c
    else:
        a = c
    if n in (10, 20, 30):
        length = b - a
        expected = 1.0 / 2 ** n
        print(f"  n = {n:2d}: 区间 [{a:.9f}, {b:.9f}], 长 = {length:.3e} (= 1/2^{n}? {abs(length - expected) < 1e-12}), 中点 = {(a + b) / 2:.9f}")
print(f"  30 步后根 ≈ {(a + b) / 2:.10f}, 中点处 |F| = {abs(F((a + b) / 2)):.2e}")
print("  -> 区间长严格按 1/2^n 缩减; 中点稳定收敛 —— 零点定理证明的算法形态")
print()

# ============ EXP3: 不连续跳值 ============
print("=== EXP3: 不连续函数跳值的现场 (介值失效) ===")
f = lambda x: x if x < 1 else x + 1
xs = np.linspace(0.0, 2.0, 20001)
vals = np.array([f(x) for x in xs])
d_15 = np.min(np.abs(vals - 1.5))
print(f"  [0,2] 网格 {len(xs)} 点: 与 1.5 的最小距离 = {d_15:.6f} (恰为 0.5, 1.5 在值域之外)")
print(f"  跳变两侧取样: f(0.999) = {f(0.999):.3f}, f(1.0) = {f(1.0):.3f}, f(1.001) = {f(1.001):.3f}")
assert d_15 > 0.49
print("  -> 值域 [0,1)∪[2,3] 跳过 (1,2): 连续被破坏处, 取遍中间值当场破产")
print()

# ============ EXP4: 不一致连续的数值指纹 ============
print("=== EXP4: 等比例小段上的函数差 (f=1/x vs f=x) ===")
print("    k     段长          |1/x1 - 1/x2|      |x1 - x2|")
for k in range(1, 7):
    x1, x2 = 10.0 ** (-k), 2.0 * 10.0 ** (-k)
    d_inv = abs(1.0 / x1 - 1.0 / x2)
    d_id = abs(x1 - x2)
    print(f"    {k}     {x2 - x1:.0e}      {d_inv:.3e}          {d_id:.0e}")
print("  -> 1/x: 段长越短、函数差反而越大 (10^k/2 爆炸) —— 统一 delta 无从谈起")
print("  -> x:   函数差 = 段长本身, 随段缩零 —— 这就是一致连续的直白对照")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")