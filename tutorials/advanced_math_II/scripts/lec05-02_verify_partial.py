# 规模纪律：小规模数值核对, 目标 < 2 秒。
# 第 05 讲《偏导数与全微分》数值核对。
#   EXP1  z=x^3y^2+x ln y at (1,2): partials and mixed partial vs finite differences
#   EXP2  sqrt(|xy|): f/rho along y=x is 1/sqrt(2) for all t; axis partials are 0
#   EXP3  piecewise f (1 on axes, 0 otherwise): partials 0 at origin, but f(t,t)=0 != f(0,0)=1
#   EXP4  z=e^x sin y at (0.5,0.5): dz coefficients vs finite differences
import math
import time

import numpy as np

T0 = time.perf_counter()

def partial_x(f, x0, y0, h=1e-5):
    return (f(x0 + h, y0) - f(x0 - h, y0)) / (2 * h)

def partial_y(f, x0, y0, h=1e-5):
    return (f(x0, y0 + h) - f(x0, y0 - h)) / (2 * h)

print("=== EXP1: z = x^3 y^2 + x ln y at (1,2) ===")
f1 = lambda x, y: x ** 3 * y ** 2 + x * math.log(y)
zx_num = partial_x(f1, 1.0, 2.0)
zy_num = partial_y(f1, 1.0, 2.0)
zx = 3 * 1.0 ** 2 * 2.0 ** 2 + math.log(2.0)
zy = 2 * 1.0 ** 3 * 2.0 + 1.0 / 2.0
zxy = 6 * 1.0 ** 2 * 2.0 + 1.0 / 2.0
hh = 1e-4
zxy_num = (partial_y(f1, 1.0 + hh, 2.0) - partial_y(f1, 1.0 - hh, 2.0)) / (2 * hh)
print(f"  z_x: num = {zx_num:.10f}, formula = {zx:.10f}, diff = {abs(zx_num - zx):.2e}")
print(f"  z_y: num = {zy_num:.10f}, formula = {zy:.10f}, diff = {abs(zy_num - zy):.2e}")
print(f"  z_xy: num = {zxy_num:.10f}, formula = {zxy:.10f}, diff = {abs(zxy_num - zxy):.2e}")
print()

print("=== EXP2: sqrt(|xy|) at the origin ===")
for t in [1e-2, 1e-4, 1e-6]:
    f = math.sqrt(abs(t * t))
    ratio = f / (math.sqrt(2) * abs(t))
    print(f"  t={t:g}: f/rho along y=x = {ratio:.10f} (1/sqrt(2) = {1/math.sqrt(2):.10f})")
for t in [1e-2, 1e-4]:
    fx = (math.sqrt(abs(t * 0.0)) - 0.0) / t
    print(f"  axis partial at t={t:g}: f_x = {fx:.2e} (0)")
print("  -> ratio does not tend to 0: not differentiable")
print()

print("=== EXP3: piecewise f (1 on axes, 0 otherwise) ===")
def pw(x, y):
    return 1.0 if x * y == 0 else 0.0
h = 1e-3
fx = (pw(h, 0.0) - pw(0.0, 0.0)) / h
fy = (pw(0.0, h) - pw(0.0, 0.0)) / h
print(f"  f_x(0,0) = {fx:.2e}, f_y(0,0) = {fy:.2e} (both 0)")
print(f"  f(1e-3,1e-3) = {pw(1e-3, 1e-3):.0f}, f(0,0) = {pw(0.0, 0.0):.0f} -> discontinuous")
print()

print("=== EXP4: z = e^x sin y at (0.5,0.5) ===")
f4 = lambda x, y: math.exp(x) * math.sin(y)
zx4 = partial_x(f4, 0.5, 0.5)
zy4 = partial_y(f4, 0.5, 0.5)
zx4_ex = math.exp(0.5) * math.sin(0.5)
zy4_ex = math.exp(0.5) * math.cos(0.5)
print(f"  z_x: num = {zx4:.10f}, exact = {zx4_ex:.10f}, diff = {abs(zx4 - zx4_ex):.2e}")
print(f"  z_y: num = {zy4:.10f}, exact = {zy4_ex:.10f}, diff = {abs(zy4 - zy4_ex):.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
