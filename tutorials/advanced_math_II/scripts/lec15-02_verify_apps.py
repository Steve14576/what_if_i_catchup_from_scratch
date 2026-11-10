# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 15 讲《重积分的应用》数值核对。
#   EXP1  area of ellipse (a=2,b=1) -> pi*a*b
#   EXP2  volume between z=x^2+y^2 and z=4 -> 8*pi
#   EXP3  mass and centroid of hemisphere rho=z (R=1)
#   EXP4  I_z of the uniform ball (R=1) and I_z/m -> 2/5
#   EXP5  disk rho=r^2 (R=1): mass and I_z
import math
import time

import numpy as np

T0 = time.perf_counter()

print("=== EXP1: area of the ellipse (a=2,b=1) -> pi*a*b ===")
a, b = 2.0, 1.0
n = 2000
r = (np.arange(n) + 0.5) / n
th = (np.arange(n) + 0.5) / n * 2 * math.pi
R, TH = np.meshgrid(r, th)
# x = a r cos, y = b r sin, |J| = a b r
v1 = np.sum(a * b * R) * (1.0 / n) * (2 * math.pi / n)
print(f"  numeric = {v1:.8f}, exact = pi*a*b = {math.pi*a*b:.8f}, diff = {abs(v1-math.pi*a*b):.2e}")
print()

print("=== EXP2: volume between z=x^2+y^2 and z=4 -> 8*pi ===")
n = 2000
r = (np.arange(n) + 0.5) / n * 2
th = (np.arange(n) + 0.5) / n * 2 * math.pi
R, TH = np.meshgrid(r, th)
v2 = np.sum((4 - R ** 2) * R) * (2.0 / n) * (2 * math.pi / n)
print(f"  numeric = {v2:.8f}, exact = 8*pi = {8*math.pi:.8f}, diff = {abs(v2-8*math.pi):.2e}")
print()

print("=== EXP3: mass and centroid of hemisphere rho=z (R=1) ===")
n = 400
rho = (np.arange(n) + 0.5) / n
phi = (np.arange(n) + 0.5) / n * (math.pi / 2)
RHO, PHI = np.meshgrid(rho, phi)
m = np.sum(RHO ** 3 * np.sin(PHI) * np.cos(PHI)) * (1 / n) * (math.pi / 2 / n) * 2 * math.pi
mz = np.sum(RHO ** 4 * np.sin(PHI) * np.cos(PHI) ** 2) * (1 / n) * (math.pi / 2 / n) * 2 * math.pi
print(f"  mass = {m:.8f}, exact = pi/4 = {math.pi/4:.8f}")
print(f"  z-bar = {mz/m:.8f}, exact = 8/15 = {8/15:.8f}")
print()

print("=== EXP4: I_z of the uniform ball (R=1) and I_z/m ===")
n = 300
rho = (np.arange(n) + 0.5) / n
phi = (np.arange(n) + 0.5) / n * math.pi
RHO, PHI = np.meshgrid(rho, phi)
Iz = np.sum(RHO ** 4 * np.sin(PHI) ** 3) * (1 / n) * (math.pi / n) * 2 * math.pi
m = 4 * math.pi / 3
print(f"  I_z = {Iz:.8f}, exact = 8*pi/15 = {8*math.pi/15:.8f}")
print(f"  I_z/m = {Iz/m:.8f}, exact = 2/5 = {0.4:.8f}")
print()

print("=== EXP5: disk rho=r^2 (R=1): mass and I_z ===")
n = 2000
r = (np.arange(n) + 0.5) / n
th = (np.arange(n) + 0.5) / n * 2 * math.pi
R, TH = np.meshgrid(r, th)
m = np.sum(R ** 2 * R) * (1 / n) * (2 * math.pi / n)
Iz = np.sum(R ** 2 * R ** 2 * R) * (1 / n) * (2 * math.pi / n)
print(f"  mass = {m:.8f}, exact = pi/2 = {math.pi/2:.8f}")
print(f"  I_z = {Iz:.8f}, exact = pi/3 = {math.pi/3:.8f}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
