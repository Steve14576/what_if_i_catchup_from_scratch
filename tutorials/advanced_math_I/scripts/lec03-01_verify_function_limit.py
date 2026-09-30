# 规模纪律：小规模扫描（每实验 <= 2000 点），目标 < 2 秒。
# 第 03 讲《函数的极限》数值验证，四个实验：
#   EXP1  sin(1/x) 的振荡现场: 一列 x -> 0 的函数值无趋势; (0, 0.01) 内 2000 点的满幅波动。
#   EXP2  x^2 的 eps-delta 实况: 对 eps = 0.1/0.01/1e-3 取 delta = min(1, eps/5),
#         扫描去心邻域 (2-d, 2) U (2, 2+d) 各 1000 点, 核对 |x^2 - 4| < eps 一个不漏。
#   EXP3  |x|/x 的左右分裂: x = +-0.1, +-0.01, ... 时右恒 +1、左恒 -1。
#   EXP4  双序列判负 (cos(1/x) 版, 作业 B3 的现场预演): x_k = 1/(2k*pi) 与 y_k = 1/((2k+1)*pi),
#         函数值分别恒为 +1 与 -1, 两列点都趋于 0 -> 极限不存在。
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: sin(1/x) 的振荡现场 ============
print("=== EXP1: sin(1/x) 在 x -> 0 处的振荡现场 ===")
for x in [0.1, 0.05, 0.02, 0.01, 1e-3, 1e-6]:
    print(f"  x = {x:8.1e}: sin(1/x) = {np.sin(1.0 / x):+.6f}")
grid = np.linspace(1e-5, 1e-2, 2000)
vals = np.sin(1.0 / grid)
print(f"  在 (1e-5, 1e-2) 均匀取 {len(grid)} 点: max = {vals.max():+.6f}, min = {vals.min():+.6f}")
assert vals.max() > 0.99 and vals.min() < -0.99
print("  -> 函数值无趋势; 但无论多靠近 0, 波动范围始终满幅 [-1, 1]: 极限真的不存在 (第六节已证)")
print()

# ============ EXP2: x^2 的 eps-delta 实况 ============
print("=== EXP2: x^2 的 eps-delta 实况, delta = min(1, eps/5) ===")
for eps in [0.1, 0.01, 1e-3]:
    d = min(1.0, eps / 5.0)
    left = np.linspace(2 - d, 2, 1000, endpoint=False)   # (2-d, 2)
    right = np.linspace(2, 2 + d, 1000 + 1)[1:]          # (2, 2+d)
    xs = np.concatenate([left, right])
    worst = np.max(np.abs(xs ** 2 - 4.0))
    ok = worst < eps
    print(f"  eps = {eps:g}: delta = {d:g}, 扫描去心邻域 {2 * len(xs)} 点, max|x^2-4| = {worst:.6f} (< eps? {ok})")
    assert ok
print("  -> 两步控制的 delta 轮轮接得住; eps < 5 后 delta = eps/5 生效 (线性关系); 最大偏差严格小于 eps")
print()

# ============ EXP3: |x|/x 的左右分裂 ============
# 诚实记录: 初版这里写成 abs(-x) / x (分母忘变号), 左侧恒打印 +1; 修正为 abs(-x) / (-x)。
print("=== EXP3: |x|/x 的左右分裂 ===")
for x in [0.1, 0.01, 1e-3, 1e-6]:
    left_val = abs(-x) / (-x)   # 左侧点 -x 代入: | -x | / (-x) = x / (-x) = -1
    print(f"  x = +{x:.0e}: |x|/x = {abs(x) / x:+.0f}   |   x = -{x:.0e}: |x|/x = {left_val:+.0f}")
print("  -> 右侧恒 +1, 左侧恒 -1, 两侧各奔东西: 判据定理判不存在 (第五节判例 1)")
print()

# ============ EXP4: 双序列判负, cos(1/x) ============
print("=== EXP4: 双序列判负, cos(1/x), 归结原则的机器版 ===")
print("  序列 1: x_k = 1/(2k*pi), cos(1/x_k) = cos(2k*pi) 应恒为 +1")
for k in range(1, 6):
    xk = 1.0 / (2 * k * np.pi)
    print(f"    k = {k}: x = {xk:.6e}, cos(1/x) = {np.cos(1.0 / xk):+.6f}")
print("  序列 2: y_k = 1/((2k+1)*pi), cos(1/y_k) = cos((2k+1)*pi) 应恒为 -1")
for k in range(1, 6):
    yk = 1.0 / ((2 * k + 1) * np.pi)
    print(f"    k = {k}: y = {yk:.6e}, cos(1/y) = {np.cos(1.0 / yk):+.6f}")
print("  -> 两列点都趋于 0, 函数值分别恒为 +1 与 -1: 由归结原则, lim_{x->0} cos(1/x) 不存在")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
