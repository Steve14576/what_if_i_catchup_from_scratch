# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 09 讲《导数——定义即极限》数值验证，四个实验：
#   EXP1  割线斜率 -> 切线斜率: f=x^2 在 x0=1, h=0.5..1e-6, 割线斜率 = 2 + h 恒等。
#   EXP2  |x| 在 0 的左右增量比: 右恒 +1, 左恒 -1 (左右导数不齐 -> 不可导)。
#   EXP3  三种不可导的数值对照: |x| (±1), cbrt(x) (增量比 -> +inf), x*sin(1/x) 补 0 (乱跳无趋势)。
#   EXP4  可导 => 连续的数值侧写: f=x^2 在 x0=1, dx 缩小表 (dy -> 0 且 dy/dx -> 2)。
import math
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: 割线 -> 切线 ============
print("=== EXP1: f(x)=x^2 在 x0=1, 割线斜率 -> 切线斜率 2 ===")
for h in [0.5, 0.1, 0.01, 1e-3, 1e-6]:
    s = ((1 + h) ** 2 - 1) / h
    print(f"  h = {h:.0e}: 割线斜率 = {s:.10f}, 与 2 的差 = {s - 2:+.1e} (差恰为 h)")
print("  -> 割线斜率 = 2 + h 的恒等: h->0 时割线绕点转动到切线")
print()

# ============ EXP2: |x| 的左右增量比 ============
print("=== EXP2: |x| 在 0 的左右增量比 ===")
for h in [0.5, -0.5, 0.1, -0.1, 0.01, -0.01, 1e-6, -1e-6]:
    r = abs(h) / h
    print(f"  h = {h:+.0e}: (|h|-0)/h = {r:+.0f}")
print("  -> 右恒 +1, 左恒 -1: 左右导数存在但不相等, 折角型不可导")
print()

# ============ EXP3: 三种不可导 ============
print("=== EXP3: 三种不可导的增量比对照 ===")
print("    h       |x|           cbrt(x)        x*sin(1/x)")
for h in [0.1, -0.1, 0.01, -0.01, 1e-3, -1e-3]:
    r1 = abs(h) / h
    r2 = np.cbrt(h) / h                       # cbrt(h)/h = |h|^(-2/3) * sign -> +inf
    f = lambda x: x * np.sin(1.0 / x) if x != 0 else 0.0
    r3 = f(h) / h                             # = sin(1/h), 乱跳
    print(f"  {h:+.0e}    {r1:+.0f}        {r2:+.3e}     {r3:+.6f}")
print("  -> 折角(±1 不齐) / 垂直(两侧同向爆) / 振荡(乱跳): 同一套极限病理学")
print()

# ============ EXP4: 可导 => 连续的数值侧写 ============
print("=== EXP4: f(x)=x^2 在 x0=1, dy 与 dy/dx ===")
print("    dx        dy              dy/dx")
for dx in [1e-1, 1e-2, 1e-3, 1e-6]:
    dy = (1 + dx) ** 2 - 1
    print(f"  {dx:.0e}   {dy:+.10f}   {(dy / dx):.10f}")
print("  -> dy -> 0 (连续侧写) 且 dy/dx -> 2 (可导侧写): |dy| ~ 2|dx| 的线性控制")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")