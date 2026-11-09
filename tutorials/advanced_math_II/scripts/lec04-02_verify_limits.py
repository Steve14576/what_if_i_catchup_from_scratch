# 规模纪律：小规模数值核对, 目标 < 2 秒。
# 第 04 讲《多元函数、极限与连续》数值核对。
#   EXP1  xy/(x^2+y^2) 沿不同斜率: k/(1+k^2) 随 k 变
#   EXP2  x^2y/(x^4+y^2): 直线上 -> 0, 抛物线上恒 1/2
#   EXP3  y sin(1/x): 重极限界 max|f| <= max|y|; 固定 y 时振荡 +-y
#   EXP4  (x^3+y^3)/(x^2+y^2): |f|/r <= 2 (grid worst ratio)
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: xy/(x^2+y^2) along y = kx ===")
for k in [0.0, 0.5, 1.0, 2.0]:
    print(f"  k={k:g}: limit value = k/(1+k^2) = {k/(1+k**2):.6f}")
print("  -> different k give different limits (k and 1/k agree: 0.5 vs 2 -> 0.4)")
print()

print("=== EXP2: x^2 y/(x^4+y^2) ===")
for xv in [1e-3, 1e-6]:
    print(f"  line k=1 at x={xv:g}: f = {xv/(xv**2+1):.3e}  (-> 0)")
for xv in [1e-2, 1e-4, 1e-8]:
    print(f"  parabola y=x^2 at x={xv:g}: f = {xv**4/(xv**4+xv**4):.6f}  (constant 0.5)")
print()

print("=== EXP3: y sin(1/x) ===")
ys = np.linspace(-1.0, 1.0, 201)
xs = np.array([1e-3, 1e-4, 1e-5])
mesh = np.abs(ys[:, None] * np.sin(1.0 / xs[None, :]))
print(f"  sup over grid: max |f| = {mesh.max():.6f}; max |y| = {np.abs(ys).max():.6f}")
print(f"  ratio max|f|/max|y| = {mesh.max() / np.abs(ys).max():.6f} (<= 1)")
y0 = 0.3
for big in [0, 1]:
    k_int = 0
    xv = 1.0 / (math.pi / 2 + 2 * math.pi * k_int) if big == 0 else 1.0 / (3 * math.pi / 2 + 2 * math.pi * k_int)
    print(f"  fixed y={y0}, x_k={xv:.6f}: f = {y0 * math.sin(1.0 / xv):+.6f}")
print("  -> oscillates between +y and -y: inner limit does not exist")
print()

print("=== EXP4: (x^3+y^3)/(x^2+y^2), grid worst |f|/r ===")
rs = np.linspace(0.01, 1.0, 60)
ths = np.linspace(0, 2 * math.pi, 181)
worst = 0.0
for r in rs:
    f = np.abs(r * (np.cos(ths) ** 3 + np.sin(ths) ** 3))
    worst = max(worst, float(np.max(f / r)))
print(f"  worst |f|/r over grid = {worst:.6f} (bound 2; actual max of |c^3+s^3| is 1, so the bound is loose)")
print("  -> |f| <= 2r -> 0")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
