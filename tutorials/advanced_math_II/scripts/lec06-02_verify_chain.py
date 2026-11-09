# 规模纪律：小规模数值核对, 目标 < 2 秒。
# 第 06 讲《复合函数与隐函数求导》数值核对。
#   EXP1  z=f(u,v)=u^2 v, u=x+y, v=xy at (1,2): z_x=30, z_y=21, z_xx=28 (finite differences)
#   EXP2  z=u^2 v, u=sin t, v=cos t at t=0.7: dz/dt vs difference
#   EXP3  x^2+y^2+z^2=1 at (0.6,0), z=0.8: z_x=-0.75, z_y=0 (explicit branch)
#   EXP4  x^2+y^2=1 at (0.6,0.8): y'=-0.75, y''=-1/y^3=-1.953125 (difference)
import math
import time

import numpy as np

T0 = time.perf_counter()

def diff1(g, t, h=1e-5):
    return (g(t + h) - g(t - h)) / (2 * h)

def diff2(g, t, h=1e-3):
    return (g(t + h) - 2 * g(t) + g(t - h)) / (h * h)

print("=== EXP1: z = u^2 v, u = x+y, v = xy at (1,2) ===")
def z_of_xy(x, y):
    u = x + y
    v = x * y
    return u * u * v

zx_num = diff1(lambda x: z_of_xy(x, 2.0), 1.0)
zy_num = diff1(lambda y: z_of_xy(1.0, y), 2.0)
zxx_num = diff2(lambda x: z_of_xy(x, 2.0), 1.0)
print(f"  z_x: num = {zx_num:.8f}, formula = 30")
print(f"  z_y: num = {zy_num:.8f}, formula = 21")
print(f"  z_xx: num = {zxx_num:.8f}, formula = 28")
print()

print("=== EXP2: z = u^2 v, u = sin t, v = cos t at t = 0.7 ===")
t0 = 0.7
def z_of_t(t):
    return (math.sin(t) ** 2) * math.cos(t)
dz_num = diff1(z_of_t, t0)
dz_exact = 2 * math.sin(t0) * math.cos(t0) ** 2 - math.sin(t0) ** 3
print(f"  dz/dt: num = {dz_num:.10f}, exact = {dz_exact:.10f}, diff = {abs(dz_num - dz_exact):.2e}")
print()

print("=== EXP3: x^2+y^2+z^2=1, point (0.6, 0), z = 0.8 ===")
def z_branch(x, y):
    return math.sqrt(1 - x * x - y * y)
zx3 = diff1(lambda x: z_branch(x, 0.0), 0.6)
zy3 = diff1(lambda y: z_branch(0.6, y), 0.0)
print(f"  z_x: num = {zx3:.10f}, exact = -0.75")
print(f"  z_y: num = {zy3:.10f}, exact = 0")
print()

print("=== EXP4: x^2+y^2=1 at (0.6,0.8) ===")
def y_branch(x):
    return math.sqrt(1 - x * x)
yp = diff1(y_branch, 0.6)
ypp = diff2(y_branch, 0.6)
print(f"  y': num = {yp:.10f}, exact = -0.75")
print(f"  y'': num = {ypp:.10f}, exact = -1/0.8^3 = {-1/0.8**3:.10f}")
print()

print("=== EXP5: three-level chain z = exp(sin(t^2)) at t = 0.7 ===")
t5 = 0.7
def z5(t):
    return math.exp(math.sin(t * t))
dz5_num = diff1(z5, t5)
dz5_exact = math.exp(math.sin(t5 ** 2)) * math.cos(t5 ** 2) * 2 * t5
print(f"  dz/dt: num = {dz5_num:.10f}, exact = {dz5_exact:.10f}, diff = {abs(dz5_num - dz5_exact):.2e}")
print()

print("=== EXP6: direct + indirect z = x^2 u, u = x+y at (1,2) ===")
def z6(x, y):
    return x * x * (x + y)
zx6_num = diff1(lambda x: z6(x, 2.0), 1.0)
zx6_full = 2 * 1.0 * 3.0 + 1.0 ** 2
zx6_direct_only = 2 * 1.0 * 3.0
print(f"  z_x: num = {zx6_num:.10f}, f_x + f_u u_x = {zx6_full:.1f}")
print(f"  if the indirect term f_u u_x is dropped: f_x = {zx6_direct_only:.1f}  (wrong by {zx6_full - zx6_direct_only:.1f})")
print()

print("=== EXP7: combined z = x^2+y^2+u, u = xy, y = x^2 at x = 0.5 ===")
def z7(x):
    y = x * x
    u = x * y
    return x * x + y * y + u
zx7_num = diff1(z7, 0.5)
zx7_chain = 2 * 0.5 + (2 * 0.25) * (2 * 0.5) + 1 * (0.25 + 0.5 * (2 * 0.5))
zx7_exact = 2 * 0.5 + 4 * 0.5 ** 3 + 3 * 0.5 ** 2
print(f"  z_x: num = {zx7_num:.10f}, chain formula = {zx7_chain:.4f}, direct substitution = {zx7_exact:.4f}")
print()

print("=== EXP8: layered branching z = u^2 + v, u = s^2 + t, v = st, s = x+y, t = x-y at (1,2) ===")
def z8(x, y):
    s = x + y
    t = x - y
    u = s * s + t
    v = s * t
    return u * u + v
zx8_num = diff1(lambda x: z8(x, 2.0), 1.0)
zx8_exact = 16 * (6 + 1) + 1 * ((-1) + 3)
print(f"  z_x: num = {zx8_num:.10f}, exact = {zx8_exact:.0f}")
print()

print("=== EXP9: Sec.4 example z = xy + u^2, u = x+y, y = x^2 at x = 0.5 ===")
def z9(x):
    y = x * x
    u = x + y
    return x * y + u * u
zx9_num = diff1(z9, 0.5)
zx9_chain = 0.25 + 2 * 0.25 + 2 * 0.75 + 4 * 0.75 * 0.5
zx9_direct = 2 * 0.5 + 9 * 0.25 + 4 * 0.125
print(f"  z_x: num = {zx9_num:.10f}, chain = {zx9_chain:.4f}, direct substitution = {zx9_direct:.4f}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")