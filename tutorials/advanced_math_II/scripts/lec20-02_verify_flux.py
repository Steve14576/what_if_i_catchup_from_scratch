# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 20 讲《第二类曲面积分（通量）》数值核对。
#   EXP1  sphere R=1, closed outward, x dydz + y dzdx + z dxdy -> 4*pi
#   EXP2  disk z=1, upper side, z dxdy -> pi
#   EXP3  disk z=1, lower side, z dxdy -> -pi
#   EXP4  cylinder side R=1 h=1, outer, x dydz -> pi
#   EXP5  sphere z dxdy: projection vs (z cos gamma) dS -> same (4*pi/3)
import math
import time

import numpy as np

T0 = time.perf_counter()
n = 400

print("=== EXP1: sphere R=1, closed outward, x dydz + y dzdx + z dxdy -> 4*pi ===")
# On R=1, n=(x,y,z) and F=(x,y,z), so F.n = 1; integrate dS = sin(phi) dphi dtheta
phi = (np.arange(n) + 0.5) / n * math.pi
th = (np.arange(n) + 0.5) / n * 2 * math.pi
PHI, TH = np.meshgrid(phi, th)
dS = np.sin(PHI)
v1 = np.sum(np.ones_like(PHI) * dS) * (math.pi / n) * (2 * math.pi / n)
print(f"  numeric = {v1:.8f}, exact = 4*pi = {4*math.pi:.8f}, diff = {abs(v1-4*math.pi):.2e}")
print()

print("=== EXP2: disk z=1, upper side, z dxdy -> pi ===")
r = (np.arange(n) + 0.5) / n
R, T = np.meshgrid(r, th)
v2 = np.sum(1.0 * R) * (1.0 / n) * (2 * math.pi / n)
print(f"  numeric = {v2:.8f}, exact = pi = {math.pi:.8f}, diff = {abs(v2-math.pi):.2e}")
print()

print("=== EXP3: disk z=1, lower side, z dxdy -> -pi ===")
v3 = -v2
print(f"  numeric = {v3:.8f}, exact = -pi = {-math.pi:.8f}, diff = {abs(v3+math.pi):.2e}")
print()

print("=== EXP4: cylinder side R=1 h=1, outer, x dydz -> pi ===")
th4 = (np.arange(n) + 0.5) / n * 2 * math.pi
zz = (np.arange(n) + 0.5) / n * 1.0
TH4, ZZ = np.meshgrid(th4, zz)
# x = cos(th), cos(alpha)=cos(th), dS = R dth dz = 1
v4 = np.sum(np.cos(TH4) * np.cos(TH4)) * (2 * math.pi / n) * (1.0 / n)
print(f"  numeric = {v4:.8f}, exact = pi = {math.pi:.8f}, diff = {abs(v4-math.pi):.2e}")
print()

print("=== EXP5: sphere z dxdy by projection vs by (z cos gamma) dS -> same ===")
# projection: upper + lower each contribute +sqrt(R^2-r^2) over the disk
# direct: z cos(gamma) = z * z / R = z^2 on R=1; integrate z^2 dS = 4*pi/3
PHI2, TH2 = np.meshgrid(phi, th)
z2 = np.cos(PHI2)
v5a = np.sum(z2 * z2 * np.sin(PHI2)) * (math.pi / n) * (2 * math.pi / n)
# projection numeric: 2 * integral over disk of sqrt(1-r^2)
rad = (np.arange(n) + 0.5) / n
RR, TT = np.meshgrid(rad, th)
v5b = 2 * np.sum(np.sqrt(1 - RR ** 2) * RR) * (1.0 / n) * (2 * math.pi / n)
print(f"  direct   = {v5a:.8f}")
print(f"  project  = {v5b:.8f}")
print(f"  exact    = 4*pi/3 = {4*math.pi/3:.8f}, diff = {abs(v5a-v5b):.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
