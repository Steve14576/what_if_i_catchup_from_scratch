# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 14 讲《三重积分》数值核对。
#   EXP1  z over 0<=z<=x+y, x,y in [0,1] -> 7/12
#   EXP2  z over the upper half ball -> pi/4
#   EXP3  x^2+y^2 over the cylinder r<=1, 0<=z<=2 -> pi
#   EXP4  volume of the unit ball -> 4*pi/3
#   EXP5  z over the ball above the cone z>=sqrt(x^2+y^2) -> pi/8
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: example 1, z over 0<=z<=x+y on the unit square ===")
n = 400
x = (np.arange(n) + 0.5) / n
y = (np.arange(n) + 0.5) / n
X, Y = np.meshgrid(x, y)
inner = (X + Y) ** 2 / 2
v1 = np.sum(inner) / n ** 2
print(f"  numeric = {v1:.8f}, exact = 7/12 = {7/12:.8f}, diff = {abs(v1-7/12):.2e}")
print()

print("=== EXP2: z over the upper half ball -> pi/4 ===")
n = 400
zz = (np.arange(n) + 0.5) / n
# inner integral over r: int_0^{sqrt(1-z^2)} z*r dr = z*(1-z^2)/2, then int dz and 2*pi
v2 = np.sum(zz * (1 - zz ** 2) / 2) * (1.0 / n) * 2 * math.pi
print(f"  numeric = {v2:.8f}, exact = pi/4 = {math.pi/4:.8f}, diff = {abs(v2-math.pi/4):.2e}")
print()

print("=== EXP3: x^2+y^2 over the cylinder r<=1, 0<=z<=2 -> pi ===")
n = 500
r = (np.arange(n) + 0.5) / n
th = (np.arange(n) + 0.5) / n * 2 * math.pi
R, TH = np.meshgrid(r, th)
v3 = np.sum(R ** 3) * (1.0 / n) * (2 * math.pi / n) * 2.0  # z length is 2
print(f"  numeric = {v3:.8f}, exact = pi = {math.pi:.8f}, diff = {abs(v3-math.pi):.2e}")
print()

print("=== EXP4: volume of the unit ball -> 4*pi/3 ===")
n = 300
rho = (np.arange(n) + 0.5) / n
phi = (np.arange(n) + 0.5) / n * math.pi
th = (np.arange(n) + 0.5) / n * 2 * math.pi
RHO, PHI = np.meshgrid(rho, phi)
v4 = np.sum(RHO ** 2 * np.sin(PHI)) * (1.0 / n) * (math.pi / n) * (2 * math.pi)  # theta length
print(f"  numeric = {v4:.8f}, exact = 4pi/3 = {4*math.pi/3:.8f}, diff = {abs(v4-4*math.pi/3):.2e}")
print()

print("=== EXP5: z over the ball above the cone -> pi/8 ===")
n = 300
rho = (np.arange(n) + 0.5) / n
phi = (np.arange(n) + 0.5) / n * (math.pi / 4)
th = (np.arange(n) + 0.5) / n * 2 * math.pi
RHO, PHI = np.meshgrid(rho, phi)
# z = rho cos(phi); dV = rho^2 sin(phi) drho dphi dtheta
v5 = np.sum(RHO ** 3 * np.sin(PHI) * np.cos(PHI)) * (1.0 / n) * ((math.pi / 4) / n) * (2 * math.pi)  # theta length
print(f"  numeric = {v5:.8f}, exact = pi/8 = {math.pi/8:.8f}, diff = {abs(v5-math.pi/8):.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
