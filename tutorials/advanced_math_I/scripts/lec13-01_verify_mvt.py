# 规模纪律：小规模扫描+二分（每实验 <= 20000 点），目标 < 2 秒。
# 第 13 讲《中值定理 I》数值验证，四个实验：
#   EXP1  拉格朗日找 xi: f=x^3-x 在 [0,2], k=3, 扫描+定位 xi=2/sqrt(3)。
#   EXP2  罗尔反例对照: |x| 在 [-1,1], 导数集合 {-1,+1}, 无零点。
#   EXP3  推论 1 双核: H=arctan x + arctan(1/x) 恒 pi/2, 差商趋 0。
#   EXP4  中值画面: sin 在 [0,pi], 割线斜率 0, xi=pi/2。
import math
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: 拉格朗日找 xi ============
print("=== EXP1: f = x^3 - x 在 [0,2], k = 3, 找 xi = 2/sqrt(3) ===")
f1 = lambda x: x ** 3 - x
df1 = lambda x: 3 * x ** 2 - 1
k1 = (f1(2) - f1(0)) / 2
xs = np.linspace(0.001, 1.999, 20000)
g = df1(xs) - k1
idx = np.where(np.diff(np.sign(g)) != 0)[0]
a, b = xs[idx[0]], xs[idx[0] + 1]
for _ in range(50):
    m = (a + b) / 2
    if (df1(a) - k1) * (df1(m) - k1) <= 0:
        b = m
    else:
        a = m
xi = (a + b) / 2
print(f"  扫描变号区间 [{xs[idx[0]]:.6f}, {xs[idx[0]+1]:.6f}], 二分定位 xi = {xi:.8f}")
print(f"  f'(xi) = {df1(xi):.8f}, 与 k 的差 = {df1(xi) - k1:+.2e}; 理论值 2/sqrt(3) = {2 / math.sqrt(3):.8f}")
print("  -> 存在定理在具体例子里可求: 考试'找 xi'型")
print()

# ============ EXP2: 罗尔反例 |x| ============
print("=== EXP2: |x| 在 [-1,1]: 缺可导 -> 无 f'=0 的点 ===")
for x in [-0.5, -0.1, 0.1, 0.5]:
    print(f"  x = {x:+.1f}: f'(x) = {np.sign(x):+.0f}")
print("  x = 0: 不可导 (折角)")
print("  -> 导数取值集合 {-1, +1}: 无零, 罗尔的结论失效 (但条件'开区间可导'被折角击穿)")
print()

# ============ EXP3: 推论 1 双核 (arctan 恒等式) ============
print("=== EXP3: H(x) = arctan x + arctan(1/x) 恒 pi/2 (x>0) ===")
for x in [0.5, 1.0, 2.0, 10.0, 100.0]:
    H = math.atan(x) + math.atan(1.0 / x)
    h = 1e-6
    dq = (math.atan(x + h) + math.atan(1 / (x + h)) - H) / h
    print(f"  x = {x:6.1f}: H = {H:.15f}, 与 pi/2 的差 = {H - math.pi / 2:+.2e}, 差商 = {dq:+.2e}")
print("  -> H 恒 pi/2 (差为浮点噪声级), 差商恒趋 0: 导数零+常数 双核实弹")
print()

# ============ EXP4: 中值画面 sin 在 [0, pi] ============
print("=== EXP4: sin 在 [0, pi]: 割线斜率 0, 找切线水平点 xi = pi/2 ===")
k4 = (math.sin(math.pi) - math.sin(0.0)) / math.pi
print(f"  割线斜率 k = {k4:.3e}")
xs4 = np.linspace(0.001, math.pi - 0.001, 10000)
idx4 = np.where(np.diff(np.sign(np.cos(xs4))) != 0)[0]
xi4 = (xs4[idx4[0]] + xs4[idx4[0] + 1]) / 2
print(f"  cos 变号定位 xi ≈ {xi4:.6f} (pi/2 = {math.pi / 2:.6f}), f'(xi) = cos(xi) = {math.cos(xi4):+.2e}")
print("  -> 切线平行于弦的数值画面: 割线斜率 = 切线斜率 = 0")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")