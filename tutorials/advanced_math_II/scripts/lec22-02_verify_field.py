# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 22 讲《场论初步与综合》数值核对。
#   EXP1  curl(grad f) = 0 for f=x^2 y + y z^2 at (1,2,3)
#   EXP2  div(curl F) = 0 for F=(x^2 y, y z, x z)
#   EXP3  Laplacian of f=x^2+y^2-2z^2 -> 0
#   EXP4  conservative check for F=(2xy, x^2+3y^2) and potential
#   EXP5  div and curl at (1,1,1) vs finite differences
import time

import numpy as np

T0 = time.perf_counter()
h = 1e-6
E = np.eye(3)


def d(fn, p, i):
    return (fn(p + h * E[i]) - fn(p - h * E[i])) / (2 * h)


print("=== EXP1: curl(grad f) = 0 for f=x^2 y + y z^2 at (1,2,3) ===")
def f1(p):
    x, y, z = p
    return x * x * y + y * z * z

def grad(p):
    return np.array([d(f1, p, i) for i in range(3)])

p = np.array([1.0, 2.0, 3.0])
g = grad(p)
curl_g = np.array([
    d(lambda q: grad(q)[2], p, 1) - d(lambda q: grad(q)[1], p, 2),
    d(lambda q: grad(q)[0], p, 2) - d(lambda q: grad(q)[2], p, 0),
    d(lambda q: grad(q)[1], p, 0) - d(lambda q: grad(q)[0], p, 1),
])
print(f"  grad = {g}")
print(f"  curl(grad) = {curl_g}, expect = [0 0 0]")
print()

print("=== EXP2: div(curl F) = 0 for F=(x^2 y, y z, x z) ===")
def F2(p):
    x, y, z = p
    return np.array([x * x * y, y * z, x * z])

def curlF(p):
    F = lambda q: F2(q)
    return np.array([
        d(lambda q: F(q)[2], p, 1) - d(lambda q: F(q)[1], p, 2),
        d(lambda q: F(q)[0], p, 2) - d(lambda q: F(q)[2], p, 0),
        d(lambda q: F(q)[1], p, 0) - d(lambda q: F(q)[0], p, 1),
    ])

p2 = np.array([1.0, 2.0, 3.0])
c2 = curlF(p2)
div_c = sum(d(lambda q: curlF(q)[i], p2, i) for i in range(3))
print(f"  curl F = {c2}")
print(f"  div(curl F) = {div_c:.6e}, expect = 0")
print()

print("=== EXP3: Laplacian of f=x^2+y^2-2z^2 -> 0 (harmonic) ===")
def f3(p):
    x, y, z = p
    return x * x + y * y - 2 * z * z

lap = sum(d(lambda q: d(f3, q, i), p2, i) for i in range(3))
print(f"  Laplacian = {lap:.6e}, expect = 0")
print()

print("=== EXP4: conservative check for F=(2xy, x^2+3y^2) and potential ===")
def F4(p):
    x, y = p[0], p[1]
    return np.array([2 * x * y, x * x + 3 * y * y])

def d2(fn, p, i):
    return (fn(p + h * E[i][:2]) - fn(p - h * E[i][:2])) / (2 * h)

p4 = np.array([1.0, 2.0])
Py = d2(lambda q: F4(q)[0], p4, 1)
Qx = d2(lambda q: F4(q)[1], p4, 0)
u = p4[0] ** 2 * p4[1] + p4[1] ** 3
ux = d2(lambda q: q[0] ** 2 * q[1] + q[1] ** 3, p4, 0)
uy = d2(lambda q: q[0] ** 2 * q[1] + q[1] ** 3, p4, 1)
print(f"  P_y = {Py:.6f}, Q_x = {Qx:.6f} (equal -> conservative)")
print(f"  potential u = x^2 y + y^3; at (1,2): u = {u}")
print(f"  u_x = {ux:.6f} (P = {F4(p4)[0]}), u_y = {uy:.6f} (Q = {F4(p4)[1]})")
print()

print("=== EXP5: div and curl at (1,1,1) vs finite differences ===")
p5 = np.array([1.0, 1.0, 1.0])
div5 = sum(d(lambda q: F2(q)[i], p5, i) for i in range(3))
c5 = curlF(p5)
print(f"  div = {div5:.6f}, exact = 4")
print(f"  curl = {c5}, exact = [-1 -1 -1]")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
