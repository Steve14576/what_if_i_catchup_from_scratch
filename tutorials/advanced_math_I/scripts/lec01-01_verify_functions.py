# 规模纪律：小规模演示（采样 + 多项式求根），目标 < 2 秒。
# 第 01 讲《函数》数值验证，四个实验：
#   EXP1  狄利克雷函数 D(x) 在计算机浮点采样上恒为 1（浮点数都是有限二进制小数，即有理数）
#   EXP2  复合顺序不可交换：A(x) = sqrt(sin x) 与 B(x) = sin(sqrt x) 的定义域差异与数值差异
#   EXP3  水平线测试：y = x^2 在 [-1, 1] 上一个 y 对应两个 x；限制到 [0, 1] 后唯一
#   EXP4  取整函数 [x] 的阶梯行为与负数坑
import math
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: 狄利克雷函数在计算机上 ============
print("=== EXP1: 狄利克雷函数 D(x) 在计算机浮点上 ===")
print("  D(x) = 1 (x 为有理数), 0 (x 为无理数)")
# 每一个 float64 都可以写成 x = m * 2^e（0.5 <= m < 1），其中 m 的有效尾数是 53 位
# （52 位存储 + 1 位隐含位），所以 m * 2^53 必为整数，故 x 是 p/2^q 型有理数。
# 诚实记录：初版这里曾随手写“乘 2^50 验证整数”，实测 sqrt(2)*2^50 = ...443.2、
# e*2^50 = ...036.5 都不是整数（只有 pi 碰巧是——它的尾数末 3 位恰为 0）。
# 根因：尾数是 53 位不是 50 位。修正为用 math.frexp 取尾数验证。
for name, x in [("sqrt(2)", np.sqrt(2)), ("pi", np.pi), ("e", np.e)]:
    m, k = math.frexp(x)  # x = m * 2^k, 0.5 <= m < 1
    m_int = m * 2**53
    ok = m_int == math.floor(m_int)
    print(f"  x = {name:8s} float 值 {x:.15f} = m * 2^{k}, m * 2^53 = {m_int:.0f}, 是整数? {ok}")
print("  -> 所有 float 都是有理数 p/2^q，所以计算机上 D(x) 永远输出 1")
print("  -> 数学上 D(sqrt(2)) = 0；采样永远看不见这个 0：数值实验有边界，采样 != 全体")
print()

# ============ EXP2: 复合顺序不可交换 ============
print("=== EXP2: 复合顺序不可交换 A=sqrt(sin x) vs B=sin(sqrt x) ===")
for x in [1.0, 4.0, 8.0]:
    sx = np.sin(x)
    if sx >= 0:
        a_val = np.sqrt(sx)
        b_val = np.sin(np.sqrt(x))
        print(f"  x = {x}: sin(x) = {sx:+.6f} >= 0  ->  A(x) = {a_val:.6f};  B(x) = {b_val:.6f}")
    else:
        b_val = np.sin(np.sqrt(x))
        print(f"  x = {x}: sin(x) = {sx:+.6f} < 0   ->  A(x) 无定义(负数开方);  B(x) = {b_val:.6f}")
grid = np.linspace(0, 4 * np.pi, 40001)
frac = (np.sin(grid) >= 0).mean()
print(f"  在 [0, 4*pi] 均匀扫描 {len(grid)} 点: A 有定义的点占比 = {frac * 100:.2f}% (数学上恰为 50.00%)")
print("  -> A 的定义域是一串周期区间 [2k*pi, (2k+1)*pi], B 的定义域是 [0, inf)")
print("  -> 复合不可交换: 定义域不同, 数值也不同")
print()

# ============ EXP3: 水平线测试 y = x^2 ============
print("=== EXP3: 水平线测试, f(x) = x^2 ===")
for y in [0.25, 0.81, 1.0, 1.2]:
    roots = np.roots([1, 0, -y])
    reals = sorted(r.real for r in roots if abs(r.imag) < 1e-9)
    in_range = [r for r in reals if -1 <= r <= 1]
    fmt = lambda lst: "[" + ", ".join(f"{r:.6f}" for r in lst) + "]" if lst else "无实根"
    print(f"  y = {y:4.2f}: 实根全体 = {fmt(reals)}; 落在 [-1,1] 内的原像 = {fmt(in_range) if in_range else '空'}")
print("  -> 在 [-1,1] 上 y = 0.25 对应 x = -0.5 和 +0.5 两个原像: 非单射, 无反函数")
print("  -> 限制到 [0,1] 后每个 y 唯一对应 x = sqrt(y), 反函数存在")
print()

# ============ EXP4: 取整函数 ============
print("=== EXP4: 取整函数 [x] (向下取整) ===")
for x in [-2.0, -1.75, -1.25, -0.25, 0.0, 0.25, 0.99, 1.0]:
    print(f"  [{x:6.2f}] = {np.floor(x):6.0f}")
print(f"  边界行为: [0.9999999] = {np.floor(0.9999999)}, [1.0] = {np.floor(1.0)}")
print("  -> 负数坑: [-0.25] = -1 (向 -inf 方向取整, 不是'丢掉小数')")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
