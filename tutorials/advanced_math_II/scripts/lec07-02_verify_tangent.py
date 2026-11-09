# 规模纪律：小规模数值核对，目标 < 2 秒。
# 第 07 讲《多元微分的几何应用》数值核对。
#   EXP1  z=x^2+y^2 at (1,1): tangent plane error is o(rho)
#   EXP2  sphere at (0.5,0.5,sqrt2/2): grad F is parallel to the radius
#   EXP3  helix at t0=pi/4: analytic tangent vs difference; normal-plane sign change
#   EXP4  sphere: implicit slope -F_x/F_z equals the tangent-plane slope
#   EXP5  cone tip: normalized gradient direction depends on the approach angle
import math
import time

import numpy as np

T0 = time.perf_counter()


def diff1(g, t, h=1e-5):
    return (g(t + h) - g(t - h)) / (2 * h)


print("=== EXP1: tangent plane is o(rho) approximation for z = x^2+y^2 at (1,1) ===")
f1 = lambda x, y: x * x + y * y
for h in [1e-1, 1e-2, 1e-3]:
    for th in [0.0, math.pi / 4]:
        x, y = 1 + h * math.cos(th), 1 + h * math.sin(th)
        err = abs(f1(x, y) - (2 + 2 * h * math.cos(th) + 2 * h * math.sin(th)))
        print(f"  h={h:.0e} theta={th:.2f}: err/rho = {err / h:.3e}  (expect ~ h)")
print()

print("=== EXP2: sphere normal is parallel to the radius at (0.5,0.5,sqrt2/2) ===")
P2 = np.array([0.5, 0.5, math.sqrt(0.5)])
g2 = np.array([2 * P2[0], 2 * P2[1], 2 * P2[2]])
cross2 = np.cross(g2, P2)
print(f"  grad F = ({g2[0]:.6f}, {g2[1]:.6f}, {g2[2]:.6f})")
print(f"  cross(grad F, radius) = ({cross2[0]:.2e}, {cross2[1]:.2e}, {cross2[2]:.2e})")
print(f"  |cross| = {np.linalg.norm(cross2):.2e}  (expect 0)")
print()

print("=== EXP3: helix tangent vs finite difference at t0 = pi/4 ===")
r3 = lambda t: np.array([math.cos(t), math.sin(t), t])
t0 = math.pi / 4
T3 = np.array([-math.sin(t0), math.cos(t0), 1.0])
fd3 = (r3(t0 + 1e-5) - r3(t0 - 1e-5)) / 2e-5
print(f"  analytic T = ({T3[0]:.8f}, {T3[1]:.8f}, {T3[2]:.8f})")
print(f"  difference = ({fd3[0]:.8f}, {fd3[1]:.8f}, {fd3[2]:.8f})")
print(f"  |T|^2 = {np.dot(T3, T3):.6f}")
for h in [1e-2, 1e-3]:
    gp = np.dot(T3, r3(t0 + h) - r3(t0))
    gm = np.dot(T3, r3(t0 - h) - r3(t0))
    print(f"  h={h:.0e}: T.(r(t0+h)-r(t0))={gp:+.3e}, h=-{h:.0e}: {gm:+.3e}  (opposite signs -> curve crosses the plane)")
print()

print("=== EXP4: implicit slope -F_x/F_z vs tangent-plane slope on the sphere ===")
# x^2+y^2+z^2=1, upper branch, point (0.6, 0, 0.8)
x4, y4, z4 = 0.6, 0.0, 0.8
slope_formula = -2 * x4 / (2 * z4)
z4_of_x = lambda x: math.sqrt(1 - x * x - y4 * y4)
slope_diff = diff1(z4_of_x, x4)
print(f"  -F_x/F_z = {slope_formula:.6f}")
print(f"  numerical dz/dx = {slope_diff:.6f}")
print()

print("=== EXP5: cone tip: gradient direction depends on the approach angle ===")
# F = z^2 - x^2 - y^2; at (r cos th, r sin th, r)
r5 = 1e-3
for th in [0.0, math.pi / 2, math.pi]:
    x5, y5, z5 = r5 * math.cos(th), r5 * math.sin(th), r5
    g5 = np.array([-2 * x5, -2 * y5, 2 * z5])
    g5 = g5 / np.linalg.norm(g5)
    print(f"  theta={th:.2f}: normalized grad F = ({g5[0]:+.4f}, {g5[1]:+.4f}, {g5[2]:+.4f})")
print("  -> the limiting direction depends on theta: no common tangent plane at the tip")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
