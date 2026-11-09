# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 10 讲《闭区域最值与应用》数值核对。
#   EXP1  disk: interior -2 vs boundary 4 +/- 4*sqrt2
#   EXP2  triangle: candidates 0, 2, 4
#   EXP3  box with V=1: S_min = 6 at (1,1)
#   EXP4  cylinder with V=1: r*, h*/r*, S*
import math
import time

import numpy as np

T0 = time.perf_counter()
rng = np.random.default_rng(7)

print("=== EXP1: disk case: interior -2 vs boundary 4 -/+ 4*sqrt2 ===")
f1 = lambda x, y: x * x + y * y - 2 * x - 2 * y
print(f"  interior: f(1,1) = {f1(1,1):.6f}")
print(f"  boundary min = {4 - 4*math.sqrt(2):.6f}, max = {4 + 4*math.sqrt(2):.6f}")
# random points in the disk
r = 2 * np.sqrt(rng.uniform(0, 1, 300000))
th = rng.uniform(0, 2 * np.pi, 300000)
vals = f1(r * np.cos(th), r * np.sin(th))
print(f"  random 300000 points in disk: min = {vals.min():.6f}, max = {vals.max():.6f}")
print()

print("=== EXP2: triangle case: candidates 0, 2, 4 ===")
f2 = lambda x, y: x * x + y * y
print(f"  corners: (0,0)={f2(0,0):.1f}, (2,0)={f2(2,0):.1f}, (0,2)={f2(0,2):.1f}")
xs = np.linspace(0, 2, 200001)
print(f"  edge x+y=2: min = {np.min(xs**2 + (2-xs)**2):.6f} at x = {xs[np.argmin(xs**2 + (2-xs)**2)]:.3f}")
u = rng.uniform(0, 1, 300000)
v = rng.uniform(0, 1, 300000)
xs = 2 * u
ys = 2 * v * (1 - u)
vals = f2(xs, ys)
print(f"  random 300000 points in triangle: min = {vals.min():.6f}, max = {vals.max():.6f}")
print()

print("=== EXP3: box with V=1: S_min = 6 at x=y=z=1 ===")
S = lambda x, y: 2 * (x * y + 1 / x + 1 / y)
print(f"  S(1,1) = {S(1,1):.6f}")
# random log-uniform x,y
lx = rng.uniform(-2, 2, 300000)
ly = rng.uniform(-2, 2, 300000)
vals = S(10 ** lx, 10 ** ly)
print(f"  random 300000 (x,y): min = {vals.min():.6f} (expect >= 6)")
print()

print("=== EXP4: cylinder with V=1: r* and h*/r* ===")
r_star = (1 / (2 * math.pi)) ** (1 / 3)
h_star = 1 / (math.pi * r_star ** 2)
S_star = 2 * math.pi * r_star ** 2 + 2 / r_star
print(f"  r* = {r_star:.10f}, h* = {h_star:.10f}, h*/r* = {h_star/r_star:.10f}")
print(f"  S* = {S_star:.10f}")
rr = np.linspace(0.05, 2.0, 500000)
SS = 2 * math.pi * rr ** 2 + 2 / rr
print(f"  scan: min = {SS.min():.10f} at r = {rr[SS.argmin()]:.6f}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
