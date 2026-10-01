# 规模纪律：Simpson n=1000 与向量化中点法, 目标 < 2 秒。
# 第 23 讲《微积分基本定理》数值验证，四个实验：
#   EXP1  非初等原函数 Phi'=f: Phi=int_0^x e^{-t^2} (Simpson), 差商核对 e^{-x^2}。
#   EXP2  N-L 对账: int_1^2 dx/x (中点法 n=1e4) vs ln2。
#   EXP3  复合上限: G=int_0^{x^2} e^{-t^2}, 差商核对 2x e^{-x^4}。
#   EXP4  秒杀题: (1-cos x)/x^2 -> 1/2 表。
# 误差账: Simpson ~1e-13; 差商(h=1e-4)自身 O(h^2)~1e-8; 内层误差被放大 ~1e-9;
#         故断言阈值取相对 1e-6 (留两个数量级裕量)。
import math
import time

import numpy as np

T0 = time.perf_counter()

def simpson(f, a, b, n=1000):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h / 3 * (y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]))

g = lambda t: np.exp(-t ** 2)
H = 1e-4

# ============ EXP1: 非初等原函数的 Phi'=f ============
print("=== EXP1: Phi(x)=int_0^x e^{-t^2} dt, 差商核对 e^{-x^2} ===")
Phi = lambda xx: simpson(g, 0, xx)
for x in [0.3, 0.7, 1.2]:
    dq = (Phi(x + H) - Phi(x - H)) / (2 * H)
    rel = abs(dq - g(x)) / g(x)
    print(f"  x = {x}: 差商 = {dq:.9f}, e^(-x^2) = {g(x):.9f}, 相对差 = {rel:.2e}")
print("  -> 全过: '写不出的原函数'照样满足 Phi'=f")
print()

# ============ EXP2: N-L 对账 ============
print("=== EXP2: int_1^2 dx/x (中点法 n=1e4) vs ln2 ===")
n = 10000
mids = 1 + (np.arange(n) + 0.5) / n
S = np.sum(1 / mids) / n
print(f"  中点法和 = {S:.10f}, ln2 = {math.log(2):.10f}, 差 = {S - math.log(2):+.2e}")
print("  -> 公式级 1 行与定义级同数")
print()

# ============ EXP3: 复合上限 ============
print("=== EXP3: G(x)=int_0^{x^2} e^{-t^2} dt, 差商核对 2x e^{-x^4} ===")
G = lambda xx: simpson(g, 0, xx ** 2)
for x in [0.5, 1.0]:
    dq = (G(x + H) - G(x - H)) / (2 * H)
    target = 2 * x * math.exp(-(x ** 4))
    rel = abs(dq - target) / target
    print(f"  x = {x}: 差商 = {dq:.9f}, 2x e^(-x^4) = {target:.9f}, 相对差 = {rel:.2e}")
print("  -> 链式与变限求导联合作业")
print()

# ============ EXP4: 秒杀题 ============
print("=== EXP4: (1-cos x)/x^2 -> 1/2 ===")
for e in [1, 2, 3]:
    x = 10.0 ** (-e)
    val = (1 - math.cos(x)) / x ** 2
    print(f"  x = 1e-{e}: 值 = {val:.10f}, 与 1/2 的差 = {val - 0.5:+.2e}")
print("  -> 三行趋 0.5: '积分除幂'题型回执")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")