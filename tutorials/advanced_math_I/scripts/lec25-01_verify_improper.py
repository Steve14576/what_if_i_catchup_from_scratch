# 规模纪律：Simpson n=2000、截断观察法, 目标 < 2 秒。
# 第 25 讲《反常积分》数值验证，四个实验：
#   EXP1  p 剖面: int_1^b x^{-p}, p=1.5/1/0.5, b=10..1e4 (收敛/对数/幂增长)。
#   EXP2  拆区间: int_{-1}^{-eps} + int_{eps}^1 对 1/x (发散去向) 与 1/sqrt(|x|) (趋 4)。
#   EXP3  振荡两型: sin x (摆动) vs sin x / x (趋 ~0.625)。
#   EXP4  判别对账: int_1^1e4 1/(x^2+1) -> pi/4; int_1^1e4 1/(x+1) 继续增长。
# 口径: 数值只"呈现行为肖像"(收敛不能由数值证明)。
import math
import time

import numpy as np

T0 = time.perf_counter()

def simpson(f, a, b, n=None):
    # 采样密度账: 大区间必须按密度分段 (n ~ 100*(b-a)), 否则大 b 时 h 大、
    # Simpson 误差 ~h^4 爆炸 (教训: 24 讲误差账纪律)。
    if n is None:
        n = max(2000, int(100 * (b - a)))
        if n % 2 == 1:
            n += 1
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h / 3 * (y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]))

# ============ EXP1: p 剖面 ============
print("=== EXP1: int_1^b x^{-p} dx, b = 10, 100, 1000, 10000 ===")
for p in [1.5, 1.0, 0.5]:
    row = [simpson(lambda x: x ** (-p), 1, b) for b in [10, 100, 1000, 10000]]
    print(f"  p = {p}: " + ", ".join(f"{v:.4f}" for v in row))
print("  -> p=1.5 趋 2; p=1 对数增长(~每十倍 +2.303); p=0.5 幂增长")
print()

# ============ EXP2: 拆区间 ============
print("=== EXP2: 拆区间纪律: 1/x 与 1/sqrt|x| ===")
for eps in [1e-1, 1e-3, 1e-5]:
    left = -simpson(lambda x: 1 / x, -1, -eps)     # 左半 (取负便于显示去向)
    right = simpson(lambda x: 1 / x, eps, 1)       # 右半
    half = simpson(lambda x: 1 / np.sqrt(np.abs(x)), eps, 1)  # sqrt 的右半
    print(f"  eps = {eps:.0e}: 1/x 左半(显示为 -值) = {-left:.4f}, 右半 = {right:.4f}; 1/sqrt 右半 = {half:.4f}")
print(f"  1/sqrt 两半之和 (eps=1e-5) = {2 * simpson(lambda x: 1 / np.sqrt(np.abs(x)), 1e-5, 1):.6f} (趋 4)")
print("  -> 1/x 两半向 ±无穷走 (不是 0!); 1/sqrt 收敛")
print()

# ============ EXP3: 振荡两型 ============
print("=== EXP3: sin x (摆动) vs sin x / x (趋 ~0.625) ===")
vals_sin, vals_sinc = [], []
for b in [10, 50, 100, 200, 500]:
    vals_sin.append(simpson(np.sin, 1, b))
    vals_sinc.append(simpson(lambda x: np.sin(x) / x, 1, b))
print(f"  sin:   " + ", ".join(f"{v:+.4f}" for v in vals_sin))
print(f"  sin/x: " + ", ".join(f"{v:.4f}" for v in vals_sinc))
print("  -> sin 摆幅不消; sin/x 稳定趋 ~0.625 (条件收敛的肖像)")
print()

# ============ EXP4: 判别对账 ============
print("=== EXP4: int_1^1e4 1/(x^2+1) vs 1/(x+1) ===")
s1 = simpson(lambda x: 1 / (x ** 2 + 1), 1, 10000)
s2 = simpson(lambda x: 1 / (x + 1), 1, 10000)
print(f"  1/(x^2+1): {s1:.6f} (pi/4 = {math.pi / 4:.6f}); 1/(x+1): {s2:.6f} (= ln(10001/2) = {math.log(10001 / 2):.6f}, 还在涨)")
print("  -> 比较法预言的'一个收敛一个发散'分道扬镳")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")