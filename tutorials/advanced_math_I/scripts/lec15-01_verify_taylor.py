# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 15 讲《泰勒公式》数值验证，四个实验：
#   EXP1  e 的部分和: sum 1/k!, n=1..12, 误差被 (n+1)! 打下去。
#   EXP2  sin(0.1) 逐阶: n=1,3,5,7 的多项式值与误差。
#   EXP3  三阶差比值: (sin x - x) / (-x^3/6) -> 1 (x=1e-1,1e-2,1e-3)。
#   EXP4  事故现场: (tan x - sin x)/x^3 -> 0.5。
import math
import time

T0 = time.perf_counter()

# ============ EXP1: e 的部分和 ============
print("=== EXP1: e = sum 1/k! 的部分和逼近 ===")
partial = 0.0
fact = 1.0
for n in range(0, 13):
    if n > 0:
        fact *= n
    partial += 1.0 / fact
    if n >= 1:
        print(f"  n = {n:2d}: 部分和 = {partial:.15f}, 与 e 的差 = {math.e - partial:+.3e}")
print("  -> 误差被 (n+1)! 逐级打下去: e 的计算机制")
print()

# ============ EXP2: sin(0.1) 逐阶 ============
print("=== EXP2: sin(0.1) 的奇阶泰勒多项式 ===")
x = 0.1
true = math.sin(x)
for n in [1, 3, 5, 7]:
    val = sum((-1) ** k * x ** (2 * k + 1) / math.factorial(2 * k + 1) for k in range((n - 1) // 2 + 1))
    print(f"  n = {n}: 多项式 = {val:.15f}, 误差 = {val - true:+.3e}")
print("  -> 每加一对奇次项, 误差乘 ~x^2 = 0.01 的节奏")
print()

# ============ EXP3: 三阶差比值 ============
print("=== EXP3: (sin x - x) / (-x^3/6) -> 1 ===")
for e in [1, 2, 3]:
    x = 10.0 ** (-e)
    ratio = (math.sin(x) - x) / (-x ** 3 / 6)
    print(f"  x = 1e-{e}: 比值 = {ratio:.10f}, 偏差 = {ratio - 1:+.3e}")
print("  -> 比值趋 1: sin x - x ~ -x^3/6 的实测对账 (06 讲欠条)")
print()

# ============ EXP4: 事故现场清算 ============
print("=== EXP4: (tan x - sin x)/x^3 -> 0.5 ===")
for e in [1, 2, 3, 4]:
    x = 10.0 ** (-e)
    val = (math.tan(x) - math.sin(x)) / x ** 3
    print(f"  x = 1e-{e}: 比值 = {val:.10f}, 偏差 = {val - 0.5:+.3e}")
print("  -> 比值趋 0.5: '替换吃掉低阶、泰勒保留到差'的清算实弹")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")