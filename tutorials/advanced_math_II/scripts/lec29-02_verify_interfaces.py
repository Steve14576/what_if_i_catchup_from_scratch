# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 29 讲《与后续课程的接口》数值核对。
#   EXP1  closed contour integral of 1/z on |z|=1 -> 2*pi*i
#   EXP2  uniform on unit disk, P(X>0) -> 1/2
#   EXP3  Hessian determinant test at the origin
import cmath
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: closed contour integral of 1/z on |z|=1 -> 2*pi*i ===")
N = 200000
theta = (np.arange(N) + 0.5) / N * 2 * math.pi
z = np.exp(1j * theta)
dz = 1j * z * (2 * math.pi / N)
integral = np.sum(dz / z)
print(f"  numeric = {integral.real:.6e} + {integral.imag:.6f}i")
print(f"  exact   = 0 + {2*math.pi:.6f}i, diff = {abs(integral - 2j*math.pi):.2e}")
print()

print("=== EXP2: uniform on unit disk, P(X>0) -> 1/2 ===")
rng = np.random.default_rng(0)
M = 500000
x = rng.uniform(-1, 1, M)
y = rng.uniform(-1, 1, M)
inside = x ** 2 + y ** 2 <= 1
p = np.mean(x[inside] > 0)
print(f"  Monte Carlo = {p:.6f}, exact = 0.5, diff = {abs(p-0.5):.2e}")
print()

print("=== EXP3: Hessian determinant test at the origin ===")
# f1 = x^2 + y^2: H = diag(2,2), det = 4 > 0 -> min
# f2 = x^2 - y^2: H = diag(2,-2), det = -4 < 0 -> saddle
print("  f=x^2+y^2 : H = [[2,0],[0,2]], det = 4 > 0, f_xx = 2 > 0 -> local min")
print("  f=x^2-y^2 : H = [[2,0],[0,-2]], det = -4 < 0 -> saddle")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
