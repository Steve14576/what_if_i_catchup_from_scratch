# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 16 讲《第一类曲线积分》数值核对。
#   EXP1  (x^2+y^2) on the unit circle -> 2*pi
#   EXP2  x on y=x from (0,0) to (1,1) -> sqrt(2)/2
#   EXP3  x on the unit circle -> 0 (symmetry)
#   EXP4  arc length of r=a (a=2) -> 2*pi*a
#   EXP5  direction independence (same curve, reversed)
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: (x^2+y^2) on the unit circle -> 2*pi ===")
n = 200000
t = (np.arange(n) + 0.5) / n * 2 * math.pi
x, y = np.cos(t), np.sin(t)
ds = np.sqrt(np.sin(t) ** 2 + np.cos(t) ** 2)  # |r'(t)|
v1 = np.sum((x * x + y * y) * ds) * (2 * math.pi / n)
print(f"  numeric = {v1:.8f}, exact = 2*pi = {2*math.pi:.8f}, diff = {abs(v1-2*math.pi):.2e}")
print()

print("=== EXP2: x on y=x from (0,0) to (1,1) -> sqrt(2)/2 ===")
t = (np.arange(n) + 0.5) / n
v2 = np.sum(t * math.sqrt(2.0)) * (1.0 / n)
print(f"  numeric = {v2:.8f}, exact = sqrt(2)/2 = {math.sqrt(2)/2:.8f}, diff = {abs(v2-math.sqrt(2)/2):.2e}")
print()

print("=== EXP3: x on the unit circle -> 0 by symmetry ===")
t = (np.arange(n) + 0.5) / n * 2 * math.pi
v3 = np.sum(np.cos(t) * 1.0) * (2 * math.pi / n)
print(f"  numeric = {v3:.3e}, exact = 0, diff = {abs(v3):.2e}")
print()

print("=== EXP4: arc length of r=a (a=2) -> 2*pi*a ===")
a = 2.0
t = (np.arange(n) + 0.5) / n * 2 * math.pi
ds = np.sqrt(a ** 2 + 0.0 ** 2)  # r'=0, constant
v4 = np.sum(np.full(n, ds)) * (2 * math.pi / n)
print(f"  numeric = {v4:.8f}, exact = 4*pi = {4*math.pi:.8f}, diff = {abs(v4-4*math.pi):.2e}")
print()

print("=== EXP5: direction independence (same curve, reversed) ===")
# upper half circle, f = y, t from 0 to pi (forward) and pi to 0 (backward)
tt = (np.arange(n) + 0.5) / n * math.pi
fwd = np.sum(np.sin(tt) * 1.0) * (math.pi / n)
tt2 = math.pi - tt
bwd = np.sum(np.sin(tt2) * 1.0) * (math.pi / n)
print(f"  forward = {fwd:.8f}, backward = {bwd:.8f}, diff = {abs(fwd-bwd):.2e}")
print("  expect: identical (ds is a length, not a signed increment)")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
