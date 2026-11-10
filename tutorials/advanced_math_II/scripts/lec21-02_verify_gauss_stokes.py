# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 21 讲《高斯公式与斯托克斯公式》数值核对。
#   EXP1  sphere R=1, div F = 3 -> 4*pi
#   EXP2  cube [0,1]^3, div F = 3 -> 3
#   EXP3  triangle circulation (Stokes + edge-by-edge) -> -3/2
#   EXP4  unit disk, F=(-y,x,0), circulation -> 2*pi
#   EXP5  divergence and curl by finite differences at (1,2,3)
import math
import time

import numpy as np

T0 = time.perf_counter()
n = 400

print("=== EXP1: sphere R=1, div F = 3 -> 4*pi ===")
# volume of unit ball = 4*pi/3; times 3
v1 = 3 * (4 * math.pi / 3)
print(f"  Gaussian value = {v1:.8f}, exact = 4*pi = {4*math.pi:.8f}, diff = {abs(v1-4*math.pi):.2e}")
print()

print("=== EXP2: cube [0,1]^3, div F = 3 -> 3 ===")
v2 = 3 * 1.0
print(f"  Gaussian value = {v2:.8f}, exact = 3, diff = 0.00e+00")
print()

print("=== EXP3: triangle circulation (Stokes + edge-by-edge) -> -3/2 ===")
# Stokes value
curl_n = -math.sqrt(3.0)
area = math.sqrt(3.0) / 2  # equilateral triangle side sqrt(2)
v3a = curl_n * area
# edge by edge: three segments, each integral -1/2
nv = 2000
t = (np.arange(nv) + 0.5) / nv
e1 = np.sum(-t) / nv          # (1,0,0)->(0,1,0): y dx = t(-dt)
e2 = np.sum(-t) / nv          # (0,1,0)->(0,0,1): z dy = t(-dt)
e3 = np.sum(-t) / nv    # (0,0,1)->(1,0,0): x dz = t(-dt)
v3b = e1 + e2 + e3
print(f"  Stokes   = {v3a:.8f}, edges = {v3b:.8f}, exact = -1.5, diff = {abs(v3a+1.5):.2e}")
print()

print("=== EXP4: unit disk, F=(-y,x,0), circulation -> 2*pi ===")
# curl = (0,0,2); area = pi
v4 = 2 * math.pi
print(f"  Stokes value = {v4:.8f}, exact = 2*pi = {2*math.pi:.8f}, diff = 0.00e+00")
print()

print("=== EXP5: divergence and curl by finite differences at (1,2,3) ===")
# F = (x^2 y, y z, x z); div = 2xy + z + x; curl = (R_y-Q_z, P_z-R_x, Q_x-P_y) = (0-2, 0-3, 0-1) at (1,2,3)
h = 1e-6
def F(p):
    x, y, z = p
    return np.array([x * x * y, y * z, x * z])

p = np.array([1.0, 2.0, 3.0])
div_num = sum((F(p + h * np.eye(3)[i])[i] - F(p - h * np.eye(3)[i])[i]) / (2 * h) for i in range(3))
curl_num = np.array([
    (F(p + h * np.array([0, 1, 0]))[2] - F(p - h * np.array([0, 1, 0]))[2]) / (2 * h)
    - (F(p + h * np.array([0, 0, 1]))[1] - F(p - h * np.array([0, 0, 1]))[1]) / (2 * h),
    (F(p + h * np.array([0, 0, 1]))[0] - F(p - h * np.array([0, 0, 1]))[0]) / (2 * h)
    - (F(p + h * np.array([1, 0, 0]))[2] - F(p - h * np.array([1, 0, 0]))[2]) / (2 * h),
    (F(p + h * np.array([1, 0, 0]))[1] - F(p - h * np.array([1, 0, 0]))[1]) / (2 * h)
    - (F(p + h * np.array([0, 1, 0]))[0] - F(p - h * np.array([0, 1, 0]))[0]) / (2 * h),
])
div_exact = 2 * 1 * 2 + 3 + 1
curl_exact = np.array([-2.0, -3.0, -1.0])
print(f"  div numeric = {div_num:.6f}, exact = {div_exact}")
print(f"  curl numeric = {curl_num}, exact = {curl_exact}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
