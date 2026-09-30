# 规模纪律：小规模打印表（每实验 <= 8 行数据），目标 < 2 秒。
# 第 04 讲《无穷小、无穷大与四则运算法则》数值验证，四个实验：
#   EXP1  无穷小的"快慢"初观察: x, x^2, x^3 在 x = 10^-1..10^-8 的值表（同为无穷小, 速度不同）。
#   EXP2  无穷大相减的三种下场: 1/x^2 - 1/x, 1/x - 1/x^2, 1/x^2 - 1/x^2 在 x = 10^-1..10^-6。
#   EXP3  拆分失败但乘积存在: x, sin(1/x), x*sin(1/x) 三列（振荡因子被趋零因子压制）。
#   EXP4  无界但非无穷大的判决: f(x) = x*sin(x) 在 x -> +inf, 冲天列 x_k = 2k*pi + pi/2
#         与贴地列 y_k = k*pi。
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: 无穷小的快慢 ============
print("=== EXP1: 无穷小的快慢 (x -> 0+): x, x^2, x^3 ===")
print("     x          x^2         x^3")
for n in range(1, 9):
    x = 10.0 ** (-n)
    print(f"  10^{-n}   {x ** 2:.1e}    {x ** 3:.1e}")
print("  -> 三者都是无穷小, 但趋零速度: 10^-n vs 10^-2n vs 10^-3n (第 06 讲'阶'的伏笔)")
print()

# ============ EXP2: 无穷大相减的三种下场 ============
print("=== EXP2: 无穷大相减的三种下场 (x -> 0+) ===")
print("     x        1/x^2-1/x      1/x-1/x^2     1/x^2-1/x^2")
for n in range(1, 7):
    x = 10.0 ** (-n)
    g1 = 1.0 / x ** 2 - 1.0 / x
    g2 = 1.0 / x - 1.0 / x ** 2
    g3 = 1.0 / x ** 2 - 1.0 / x ** 2
    print(f"  10^{-n}   {g1:>12.3e}   {g2:>12.3e}   {g3:>10.1f}")
print("  -> 同一形态三种归宿: +inf / -inf / 恒 0 —— '未定式'的数据版")
print()

# ============ EXP3: 拆分失败但乘积存在 ============
print("=== EXP3: 拆分失败但乘积存在 (x -> 0): x, sin(1/x), x*sin(1/x) ===")
print("     x        sin(1/x)      x*sin(1/x)")
for n in range(1, 7):
    x = 10.0 ** (-n)
    s = np.sin(1.0 / x)
    print(f"  10^{-n}   {s:>+10.6f}    {x * s:>+10.2e}")
print("  -> sin(1/x) 持续乱跳无极限(03 讲已证), 乘积被 x 压制稳定趋 0: 失效现场一的数值形态")
print()

# ============ EXP4: 无界但非无穷大的判决 ============
print("=== EXP4: 无界但非无穷大的判决, f(x) = x*sin(x), x -> +inf ===")
f = lambda x: x * np.sin(x)
print("  冲天列: x_k = 2k*pi + pi/2 (sin = 1, f = x_k):")
for k in range(1, 6):
    xk = 2 * k * np.pi + np.pi / 2
    print(f"    k = {k}: x = {xk:8.4f}, f(x) = {f(xk):8.4f}")
print("  贴地列: y_k = k*pi (sin = 0, f = 0):")
for k in range(11, 16):
    yk = k * np.pi
    print(f"    k = {k:2d}: y = {yk:8.4f}, f(y) = {f(yk):.6f}")
print("  -> 冲天列任意大(无界), 贴地列在任意远处取 0(非无穷大): 3.2 节判决的数据版")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
