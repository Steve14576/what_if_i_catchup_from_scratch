# 规模纪律：小规模打印表（最大采样 3000 点），目标 < 2 秒。
# 第 07 讲《连续性与间断点》数值验证，四个实验：
#   EXP1  三类间断数值对照: x^2/x (可去), [x] 在 1 (跳跃), 1/x 在 0 (无穷)。
#   EXP2  振荡压制对照: sin(1/x) 满幅乱跳 vs x*sin(1/x) 被压制（可去）。
#   EXP3  兑换链数值坐实: (1+x)^{1/x} vs e; ln(1+x)/x -> 1; (e^x-1)/x -> 1; ((1+x)^{1/2}-1)/x -> 0.5。
#   EXP4  跳跃度量: [x] 在整数点 k=1,2,3 的左右值与跳跃量恒为 1。
import math
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: 三类间断数值对照 ============
print("=== EXP1: 三类间断的数值指纹 ===")
f1 = lambda x: x ** 2 / x       # 可去 (0 处无定义, 两侧趋 0)
f2 = lambda x: np.floor(x)      # 跳跃 (整数点)
f3 = lambda x: 1.0 / x          # 无穷 (0 处)
for e in [1e-3, 1e-6]:
    print(f"  x0 ± {e:.0e}: f1 = x^2/x: {f1(-e):+.3e}, {f1(e):+.3e} (可去: 两侧合流趋 0)")
    print(f"             f2 = [x] at 1: {f2(1 - e):.0f}, {f2(1 + e):.0f} (跳跃: 0 vs 1)")
    print(f"             f3 = 1/x: {f3(-e):+.3e}, {f3(e):+.3e} (无穷: 反向爆炸)")
print("  -> 三类断点的指纹各不相同: 合流/分居/爆炸")
print()

# ============ EXP2: 振荡的压制对照 ============
print("=== EXP2: sin(1/x) vs x*sin(1/x) ===")
for e in [1e-3, 1e-6]:
    s = np.sin(1.0 / e)
    print(f"  x = ±{e:.0e}: sin(1/x) = {np.sin(-1.0/e):+.6f} / {s:+.6f}  (满幅乱跳)")
    print(f"              x*sin(1/x) = {-e*np.sin(-1.0/e):+.3e} / {e*s:+.3e}  (被 x 压制)")
grid = np.linspace(1e-9, 1e-3, 3000)
vals = np.abs(grid * np.sin(1.0 / grid))
print(f"  在 [1e-9, 1e-3] 采样 {len(grid)} 点: max |x*sin(1/x)| = {vals.max():.3e} (<= 1e-3)")
assert vals.max() <= 1e-3
print("  -> 同源振荡, 命运相反: 分水岭是乘上去的那个 x")
print()

# ============ EXP3: 兑换链数值坐实 ============
print("=== EXP3: B 区兑换链的数值坐实 ===")
for x in [1e-1, 1e-2, 1e-3, 1e-4]:
    a = (1.0 + x) ** (1.0 / x)          # -> e
    b = np.log1p(x) / x                  # -> 1
    c = (np.exp(x) - 1.0) / x            # -> 1
    d = ((1.0 + x) ** 0.5 - 1.0) / x     # -> 0.5
    print(f"  x = {x:.0e}: (1+x)^(1/x)-e = {a - math.e:+.3e}; ln(1+x)/x = {b:.8f}; (e^x-1)/x = {c:.8f}; ((1+x)^0.5-1)/x = {d:.8f}")
print("  -> 四列分别贴住 e, 1, 1, 0.5: (1+x)^(1/x)->e 与三条等价的实弹坐实")
print()

# ============ EXP4: 跳跃的度量 ============
print("=== EXP4: [x] 在整数点的跳跃量 ===")
for k in [1, 2, 3]:
    left = np.floor(k - 1e-6)
    right = np.floor(k + 1e-6)
    print(f"  k = {k}: [k-1e-6] = {left:.0f}, [k+1e-6] = {right:.0f}, 跳跃量 = {right - left:.0f}")
    assert right - left == 1.0
print("  -> 每处跳跃量恒为 1: 台阶高度处处相同的阶梯")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")