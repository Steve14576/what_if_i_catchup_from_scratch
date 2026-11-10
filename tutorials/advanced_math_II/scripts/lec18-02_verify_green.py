# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 18 讲《格林公式与路径无关》数值核对。
#   EXP1  oint (x-y)dx+(x+y)dy on unit circle -> 2*pi
#   EXP2  ellipse area by boundary integral -> pi*a*b
#   EXP3  path independence: 2xy dx + x^2 dy -> 1 (two paths)
#   EXP4  vortex field around origin -> 2*pi (not 0)
#   EXP5  Green: boundary integral equals double integral
import math
import time

import numpy as np

T0 = time.perf_counter()
n = 200000

print("=== EXP1: oint (x-y)dx+(x+y)dy on unit circle -> 2*pi ===")
t = (np.arange(n) + 0.5) / n * 2 * math.pi
x, y = np.cos(t), np.sin(t)
dx, dy = -np.sin(t), np.cos(t)
P, Q = x - y, x + y
v1 = np.sum(P * dx + Q * dy) * (2 * math.pi / n)
print(f"  numeric = {v1:.8f}, exact = 2*pi = {2*math.pi:.8f}, diff = {abs(v1-2*math.pi):.2e}")
print()

print("=== EXP2: ellipse area by the boundary integral -> pi*a*b ===")
a, b = 2.0, 1.0
x, y = a * np.cos(t), b * np.sin(t)
dx, dy = -a * np.sin(t), b * np.cos(t)
area = 0.5 * np.sum(x * dy - y * dx) * (2 * math.pi / n)
print(f"  numeric = {area:.8f}, exact = pi*a*b = {math.pi*a*b:.8f}, diff = {abs(area-math.pi*a*b):.2e}")
print()

print("=== EXP3: path independence: 2xy dx + x^2 dy, (0,0)->(1,1) -> 1 ===")
s = (np.arange(n) + 0.5) / n
# path 1: straight y=x
x1, y1 = s, s
v3a = np.sum(2 * x1 * y1 * 1.0 + x1 ** 2 * 1.0) * (1.0 / n)
# path 2: parabola y=x^2
x2, y2 = s, s ** 2
v3b = np.sum(2 * x2 * y2 * 1.0 + x2 ** 2 * (2 * s)) * (1.0 / n)
print(f"  straight = {v3a:.8f}, parabola = {v3b:.8f}, exact = 1, diff = {abs(v3a-v3b):.2e}")
print()

print("=== EXP4: vortex field around the origin -> 2*pi (not 0) ===")
x, y = np.cos(t), np.sin(t)
dx, dy = -np.sin(t), np.cos(t)
P = -y / (x ** 2 + y ** 2)
Q = x / (x ** 2 + y ** 2)
v4 = np.sum(P * dx + Q * dy) * (2 * math.pi / n)
print(f"  numeric = {v4:.8f}, exact = 2*pi = {2*math.pi:.8f}, diff = {abs(v4-2*math.pi):.2e}")
print()

print("=== EXP5: Green: boundary integral equals double integral ===")
# same field as EXP1: Q_x - P_y = 1 - (-1) = 2, area of unit disk = pi
boundary = v1
double_int = 2.0 * math.pi
print(f"  boundary = {boundary:.8f}, double = {double_int:.8f}, diff = {abs(boundary-double_int):.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
