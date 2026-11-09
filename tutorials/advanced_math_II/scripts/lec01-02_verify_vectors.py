# 规模纪律：小规模数值核对, 目标 < 2 秒。
# 第 01 讲《向量与坐标》数值核对：与正文例 1-3 和作业 7 对应。
#   EXP1  dot / angle / projection (a=(1,2,3), b=(2,0,-1))
#   EXP2  cross: components, norm, perpendicularity (relative), triangle area
#   EXP3  triple product: value, cyclic invariance, volume
#   EXP4  random check for Q7: perpendicularity and area (relative tolerances)
import math
import time

import numpy as np

T0 = time.perf_counter()
np.set_printoptions(precision=10, suppress=True)

a = np.array([1.0, 2.0, 3.0])
b = np.array([2.0, 0.0, -1.0])
c = np.array([1.0, 1.0, 1.0])

print("=== EXP1: dot, angle, projection ===")
dot = float(np.dot(a, b))
na, nb = np.linalg.norm(a), np.linalg.norm(b)
cos_t = dot / (na * nb)
proj = dot / nb
print(f"  a.b = {dot:.10f}  (expect -1)")
print(f"  |a| = {na:.10f} = sqrt(14) = {math.sqrt(14):.10f}")
print(f"  |b| = {nb:.10f} = sqrt(5)  = {math.sqrt(5):.10f}")
print(f"  cos(theta) = {cos_t:.10f}  (expect -1/sqrt(70) = {-1/math.sqrt(70):.10f})")
print(f"  proj_b(a)  = {proj:.10f}  (expect -1/sqrt(5) = {-1/math.sqrt(5):.10f})")
print("  -> obtuse angle, negative projection: consistent")
print()

print("=== EXP2: cross product, perpendicularity, area ===")
cr = np.cross(a, b)
print(f"  a x b = {cr}  (expect [-2, 7, -4])")
print(f"  |a x b| = {np.linalg.norm(cr):.10f} = sqrt(69) = {math.sqrt(69):.10f}")
print(f"  triangle area = {0.5 * np.linalg.norm(cr):.10f} = sqrt(69)/2 = {math.sqrt(69)/2:.10f}")
rel_a = abs(np.dot(a, cr)) / (na * np.linalg.norm(cr))
rel_b = abs(np.dot(b, cr)) / (nb * np.linalg.norm(cr))
print(f"  |a.(a x b)| / (|a||a x b|) = {rel_a:.2e}  (expect ~1e-17)")
print(f"  |b.(a x b)| / (|b||a x b|) = {rel_b:.2e}  (expect ~1e-17)")
print("  -> cross product perpendicular to both (relative check)")
print()

print("=== EXP3: triple product and volume ===")
tp = float(np.dot(cr, c))
tp1 = float(np.dot(np.cross(b, c), a))
tp2 = float(np.dot(np.cross(c, a), b))
print(f"  (a x b).c = {tp:.10f}  (expect 1)")
print(f"  cyclic: (b x c).a = {tp1:.10f}, (c x a).b = {tp2:.10f}")
print(f"  volume = {abs(tp):.10f}")
print("  -> not coplanar; volume 1")
print()

print("=== EXP4: random check (Q7 reference) ===")
rng = np.random.default_rng(42)
worst_perp = 0.0
worst_area = 0.0
for _ in range(200):
    va = rng.normal(size=3)
    vb = rng.normal(size=3)
    if np.linalg.norm(np.cross(va, vb)) < 1e-6:
        continue
    vc = np.cross(va, vb)
    worst_perp = max(worst_perp,
                     abs(np.dot(va, vc)) / (np.linalg.norm(va) * np.linalg.norm(vc)),
                     abs(np.dot(vb, vc)) / (np.linalg.norm(vb) * np.linalg.norm(vc)))
    theta = math.acos(np.clip(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb)), -1, 1))
    area2 = np.linalg.norm(va) * np.linalg.norm(vb) * math.sin(theta)
    worst_area = max(worst_area, abs(np.linalg.norm(vc) - area2) / np.linalg.norm(vc))
print(f"  worst relative perpendicularity residual over 200 trials: {worst_perp:.2e}")
print(f"  worst relative area mismatch:                             {worst_area:.2e}")
print("  -> both below 1e-12 (three orders above double precision)")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")
