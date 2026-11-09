# 规模纪律：小规模数值核对，目标 < 3 秒。
# 第 09 讲《多元极值与条件极值》数值核对。
#   EXP1  f=x^2+y^2-2x-4y: stationary point, Delta, and a neighbourhood check
#   EXP2  f=x^3+y^3-3xy: saddle at (0,0), minimum at (1,1)
#   EXP3  Lagrange on x^2+y^2 with x+y=1
#   EXP4  maximize xyz subject to x+y+z=1
#   EXP5  x^2-y^2 on the unit circle: four candidates
import math
import time

import numpy as np

T0 = time.perf_counter()
rng = np.random.default_rng(42)

print("=== EXP1: f=x^2+y^2-2x-4y: stationary point and the AC-B^2 test ===")
f1 = lambda x, y: x * x + y * y - 2 * x - 4 * y
x0, y0 = 1.0, 2.0
print(f"  stationary point: ({x0:.0f},{y0:.0f}); f = {f1(x0, y0):.4f}")
print(f"  A=2, B=0, C=2, Delta={2*2-0:.1f} > 0, A>0 -> minimum")
pts = rng.uniform(-0.5, 0.5, size=(20000, 2))
vals = f1(x0 + pts[:, 0], y0 + pts[:, 1])
print(f"  min over 20000 random points near the point: {vals.min():.6f} (expect >= -5)")
print()

print("=== EXP2: f=x^3+y^3-3xy: saddle at (0,0), minimum at (1,1) ===")
f2 = lambda x, y: x ** 3 + y ** 3 - 3 * x * y
print(f"  at (0,0): A=0, B=-3, C=0, Delta={0*0-(-3)**2:.1f} < 0 -> saddle")
for t in [0.1, 0.05]:
    print(f"  t={t}: f(t,t)={f2(t,t):+.6f}, f(t,-t)={f2(t,-t):+.6f}  (opposite signs)")
print(f"  at (1,1): A=6, B=-3, C=6, Delta={6*6-9:.1f} > 0, A>0 -> minimum, f={f2(1,1):.4f}")
print()

print("=== EXP3: Lagrange on x^2+y^2 with x+y=1 ===")
f3 = lambda x, y: x * x + y * y
print(f"  solution: (0.5,0.5), f = {f3(0.5,0.5):.4f}")
ts = np.linspace(0, 1, 200001)
vals = f3(ts, 1 - ts)
print(f"  scan along the constraint: min = {vals.min():.6f}, at x = {ts[vals.argmin()]:.3f}")
print()

print("=== EXP4: maximize xyz subject to x+y+z=1 ===")
samples = rng.dirichlet([1.0, 1.0, 1.0], size=200000)
prod = samples[:, 0] * samples[:, 1] * samples[:, 2]
print(f"  candidate: (1/3,1/3,1/3), xyz = {1/27:.10f}")
print(f"  max over 200000 random points on the simplex: {prod.max():.10f} (expect <= 1/27)")
print(f"  largest sample point: {samples[prod.argmax()]}")
print()

print("=== EXP5: x^2-y^2 on the unit circle: four candidates ===")
f5 = lambda x, y: x * x - y * y
for (x, y) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    print(f"  candidate ({x:+d},{y:+d}): f = {f5(x, y):+.1f}")
th = np.linspace(0, 2 * math.pi, 200001)
vals = f5(np.cos(th), np.sin(th))
print(f"  scan: max = {vals.max():.6f}, min = {vals.min():.6f}")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
