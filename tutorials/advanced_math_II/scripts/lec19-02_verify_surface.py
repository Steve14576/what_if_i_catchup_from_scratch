# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 19 讲《第一类曲面积分》数值核对。
#   EXP1  area of z=x+y over the unit disk -> sqrt(3)*pi
#   EXP2  z over the disk z=1 -> pi
#   EXP3  z^2 over the sphere (R=1) -> 4*pi/3
#   EXP4  z over the sphere -> 0
#   EXP5  mass of upper hemisphere with rho=z (R=1) -> pi
import math
import time

import numpy as np

T0 = time.perf_counter()
n = 400

print("=== EXP1: area of z=x+y over the unit disk -> sqrt(3)*pi ===")
r = (np.arange(n) + 0.5) / n
th = (np.arange(n) + 0.5) / n * 2 * math.pi
R, TH = np.meshgrid(r, th)
# dS = sqrt(1+1+1) * r dr dth
v1 = np.sum(math.sqrt(3.0) * R) * (1.0 / n) * (2 * math.pi / n)
print(f"  numeric = {v1:.8f}, exact = sqrt(3)*pi = {math.sqrt(3)*math.pi:.8f}, diff = {abs(v1-math.sqrt(3)*math.pi):.2e}")
print()

print("=== EXP2: z over the disk z=1 -> pi ===")
v2 = np.sum(R * 0 + 1.0 * R) * (1.0 / n) * (2 * math.pi / n)
print(f"  numeric = {v2:.8f}, exact = pi = {math.pi:.8f}, diff = {abs(v2-math.pi):.2e}")
print()

print("=== EXP3: z^2 over the sphere (R=1) -> 4*pi/3 ===")
phi = (np.arange(n) + 0.5) / n * math.pi
th2 = (np.arange(n) + 0.5) / n * 2 * math.pi
PHI, TH2 = np.meshgrid(phi, th2)
z = np.cos(PHI)
dS = np.sin(PHI)  # R^2 sin(phi)
v3 = np.sum(z ** 2 * dS) * (math.pi / n) * (2 * math.pi / n)
print(f"  numeric = {v3:.8f}, exact = 4*pi/3 = {4*math.pi/3:.8f}, diff = {abs(v3-4*math.pi/3):.2e}")
print()

print("=== EXP4: z over the sphere -> 0 by symmetry ===")
v4 = np.sum(z * dS) * (math.pi / n) * (2 * math.pi / n)
print(f"  numeric = {v4:.3e}, exact = 0, diff = {abs(v4):.2e}")
print()

print("=== EXP5: mass of upper hemisphere with rho=z (R=1) -> pi ===")
phi = (np.arange(n) + 0.5) / n * (math.pi / 2)
PHI2, TH3 = np.meshgrid(phi, th2)
z2 = np.cos(PHI2)
dS2 = np.sin(PHI2)
v5 = np.sum(z2 * dS2) * ((math.pi / 2) / n) * (2 * math.pi / n)
print(f"  numeric = {v5:.8f}, exact = pi = {math.pi:.8f}, diff = {abs(v5-math.pi):.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
