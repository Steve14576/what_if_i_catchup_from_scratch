# 规模纪律：小规模扫描+表格打印，目标 < 2 秒。
# 第 14 讲《中值定理 II 与洛必达》数值验证，四个实验：
#   EXP1  柯西找 xi: f=x^2, g=x^3 在 [1,2], K=3/7, xi=14/9, 扫描+核对比值。
#   EXP2  振荡案例: (x+sin x)/x 原比值趋 1 vs 导数比值 1+cos x 无收敛。
#   EXP3  数列转化: a_n = n sin(1/n) 与 f(n) 两列一致, 同趋 1。
#   EXP4  导数极限定理反面: f=x^2 sin(1/x) 差商趋 0, 但 f'(x) 振荡无极限。
import math
import time

import numpy as np

T0 = time.perf_counter()

# ============ EXP1: 柯西找 xi ============
print("=== EXP1: f = x^2, g = x^3 在 [1,2], K = 3/7, xi = 14/9 ===")
f1 = lambda x: x ** 2
g1 = lambda x: x ** 3
K1 = (f1(2) - f1(1)) / (g1(2) - g1(1))
print(f"  K = (f(2)-f(1))/(g(2)-g(1)) = {K1:.8f}")
xs = np.linspace(1.0005, 1.9995, 20000)
r = (2 * xs) / (3 * xs ** 2) - K1            # f'/g' - K
idx = np.where(np.diff(np.sign(r)) != 0)[0]
a, b = xs[idx[0]], xs[idx[0] + 1]
for _ in range(50):
    m = (a + b) / 2
    if ((2 * a) / (3 * a ** 2) - K1) * ((2 * m) / (3 * m ** 2) - K1) <= 0:
        b = m
    else:
        a = m
xi = (a + b) / 2
print(f"  二分定位 xi = {xi:.8f}, 14/9 = {14 / 9:.8f}")
print(f"  f'(xi)/g'(xi) = {(2 * xi) / (3 * xi ** 2):.8f}, 与 K 的差 = {(2 * xi) / (3 * xi ** 2) - K1:+.2e}")
print("  -> 柯西定理的数值实弹: 比值吻合")
print()

# ============ EXP2: 振荡案例双列 ============
print("=== EXP2: (x+sin x)/x 原比值 vs 导数比值 1+cos x ===")
for k in range(1, 7):
    x = 10.0 ** k
    ratio = (x + math.sin(x)) / x
    deriv = 1 + math.cos(x)
    print(f"  x = 1e{k}: 原比值 = {ratio:.10f} (趋 1), 导数比值 = {deriv:+.6f} (振荡)")
print("  -> 原比值收敛, 导数比值乱摆: 'f'/g' 不存在 ≠ 原极限不存在")
print()

# ============ EXP3: 数列转化 ============
print("=== EXP3: a_n = n sin(1/n) vs f(n) = n*sin(1/n) ===")
for k in range(1, 7):
    n = 10.0 ** k
    a_n = n * math.sin(1 / n)
    f_val = math.sin(1 / n) * n
    print(f"  n = 1e{k}: a_n = {a_n:.10f}, f(n) = {f_val:.10f}, 差 = {a_n - f_val:+.1e}")
print("  -> 两列逐位一致且同趋 1: 数列->函数->归结原则链条的第一步")
print()

# ============ EXP4: 导数极限定理反面 ============
print("=== EXP4: f = x^2 sin(1/x): f'(0) 存在 vs lim f'(x) 不存在 ===")
print("  差商 (h -> 0):")
for k in range(1, 7):
    h = 10.0 ** (-k)
    dq = (h ** 2 * math.sin(1 / h)) / h
    print(f"    h = 1e-{k}: 差商 = {dq:+.3e}")
print("  f'(x) = 2x sin(1/x) - cos(1/x) 在 x -> 0 附近:")
for x in [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4]:
    d = 2 * x * math.sin(1 / x) - math.cos(1 / x)
    print(f"    x = {x:.0e}: f'(x) = {d:+.6f}")
print("  -> 差商趋 0 (f'(0)=0 存在), 但 f'(x) 在 [-1,1] 乱摆 (无极限): 充分不必要")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")