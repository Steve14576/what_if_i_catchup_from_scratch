# 规模纪律：小规模数值核对，目标 < 2 秒。
# 第 08 讲《方向导数与梯度》数值核对。
#   EXP1  f=x^2+y^2 at (1,1): directional derivative vs grad f . e
#   EXP2  scan theta: the maximum is attained along grad f, value |grad f|
#   EXP3  along the level curve: directional derivative = 0
#   EXP4  sqrt(|xy|) at origin: directional derivative exists but the formula fails
#   EXP5  2D gradient vs 3D surface normal (first two components agree)
import math
import time

import numpy as np

T0 = time.perf_counter()


def dir_deriv(f, p, e, h=1e-6):
    p = np.array(p, dtype=float)
    e = np.array(e, dtype=float)
    e = e / np.linalg.norm(e)
    return (f(*(p + h * e)) - f(*p)) / h


def f1(x, y):
    return x * x + y * y


print("=== EXP1: directional derivative vs grad f . e at (1,1), f = x^2+y^2 ===")
g1 = np.array([2.0, 2.0])
for th in [0.0, math.pi / 4, math.pi / 2]:
    e = [math.cos(th), math.sin(th)]
    num = dir_deriv(f1, (1.0, 1.0), e)
    formula = g1.dot(np.array(e))
    print(f"  theta={th:.2f}: num={num:.10f}, formula={formula:.10f}, diff={abs(num - formula):.2e}")
print()

print("=== EXP2: scan theta, find the steepest ascent direction ===")
best_th, best_val = None, -1e9
for th in np.linspace(0, 2 * math.pi, 2001):
    e = np.array([math.cos(th), math.sin(th)])
    val = g1.dot(e)
    if val > best_val:
        best_th, best_val = th, val
print(f"  max at theta={best_th:.6f} rad, value={best_val:.10f}")
print(f"  |grad f| = {np.linalg.norm(g1):.10f}  (expect pi/4 and 2*sqrt2 = {2*math.sqrt(2):.10f})")
print()

print("=== EXP3: along the level curve, directional derivative is zero ===")
e_tan = np.array([-1.0, 1.0]) / math.sqrt(2)
num_tan = dir_deriv(f1, (1.0, 1.0), e_tan)
print(f"  along tangent (-1,1)/sqrt2: num={num_tan:.2e}  (expect ~ 0)")
print(f"  grad . tangent = {g1.dot(e_tan):.2e}")
print()

print("=== EXP4: sqrt(|xy|) at origin: directional derivative vs the formula ===")
f4 = lambda x, y: math.sqrt(abs(x * y))
for name, e in [("(1,0)", (1.0, 0.0)),
                ("(1,1)/sqrt2", (1 / math.sqrt(2), 1 / math.sqrt(2))),
                ("(0,1)", (0.0, 1.0))]:
    num = dir_deriv(f4, (0.0, 0.0), e)
    print(f"  e={name}: num={num:.10f}, formula grad f . e = 0.0000000000, diff={abs(num):.2e}")
print("  -> every direction exists, but grad f = (0,0): the formula fails (not differentiable)")
print()

print("=== EXP5: 2D gradient vs the 3D surface normal (first two components) ===")
gf2 = np.array([2.0, 2.0])
gF3 = np.array([2.0, 2.0, -1.0])
print(f"  grad f (2D)      = {gf2}")
print(f"  first two of grad F = {gF3[:2]}")
print(f"  max |difference| = {np.max(np.abs(gf2 - gF3[:2])):.2e}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
