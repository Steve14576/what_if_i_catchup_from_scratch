# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 06 讲《无穷小的比较与等价替换》数值验证，四个实验：
#   EXP1  等价对与高阶差比值表: sinx/x -> 1; (1-cosx)/x^2 -> 1/2;
#         (tanx-sinx)/x^3 -> 1/2; (sinx-x)/x^3 -> -1/6; (tanx-x)/x^3 -> 1/3。
#   EXP2  事故现场对照: (tanx-sinx)/x -> 0 (主项确实相消) vs /x^3 -> 0.5 (真值)。
#   EXP3  方框条件: ln(1+2x)/sin(3x) -> 2/3。
#   EXP4  阶数敏感性: sin(x^2)/x^2 -> 1, sin(x^2)/x -> 0, sin(3x)/x -> 3。
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: 等价对与高阶差比值表 ============
print("=== EXP1: 五列比值表 (x -> 0) ===")
print("    x        sinx/x    (1-cosx)/x^2  (tanx-sinx)/x^3  (sinx-x)/x^3   (tanx-x)/x^3")
for x in [1e-1, 1e-2, 1e-3, 1e-4]:
    r1 = np.sin(x) / x
    r2 = (1 - np.cos(x)) / x ** 2
    r3 = (np.tan(x) - np.sin(x)) / x ** 3
    r4 = (np.sin(x) - x) / x ** 3
    r5 = (np.tan(x) - x) / x ** 3
    print(f"  {x:.0e}   {r1:.8f}  {r2:.8f}   {r3:.8f}    {r4:.8f}    {r5:.8f}")
print("  -> 五列分别趋 1, 0.5, 0.5, -1/6, 1/3 (A 区条目与三阶差的数值坐实)")
print()

# ============ EXP2: 事故现场对照 ============
print("=== EXP2: (tanx-sinx) 的事故对照 ===")
print("    x        (tanx-sinx)/x     (tanx-sinx)/x^3")
for x in [1e-1, 1e-2, 1e-3, 1e-4]:
    a = (np.tan(x) - np.sin(x)) / x
    b = (np.tan(x) - np.sin(x)) / x ** 3
    print(f"  {x:.0e}      {a:+.3e}          {b:.8f}")
print("  -> 第一列趋 0 (主项确实相消); 第二列趋 0.5 (真值): 相消是真的, 用相消的结论是真错的")
print()

# ============ EXP3: 方框条件的实弹 ============
print("=== EXP3: ln(1+2x)/sin(3x) -> 2/3 ===")
for x in [1e-1, 1e-2, 1e-3, 1e-4]:
    r = np.log1p(2 * x) / np.sin(3 * x)
    print(f"  x = {x:.0e}: ln(1+2x)/sin(3x) = {r:.8f}")
print("  -> 趋 2/3 (替换链 (2x)/(3x) 的数值形态)")
print()

# ============ EXP4: 阶数敏感性 ============
print("=== EXP4: sin(x^2) 的两面 与 sin(3x) ===")
print("    x        sin(x^2)/x^2    sin(x^2)/x     sin(3x)/x")
for x in [1e-1, 1e-2, 1e-3, 1e-4]:
    a = np.sin(x ** 2) / x ** 2
    b = np.sin(x ** 2) / x
    c = np.sin(3 * x) / x
    print(f"  {x:.0e}     {a:.8f}     {b:+.3e}       {c:.8f}")
print("  -> 三列分别趋 1, 0, 3: 方框里是什么就配什么")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")