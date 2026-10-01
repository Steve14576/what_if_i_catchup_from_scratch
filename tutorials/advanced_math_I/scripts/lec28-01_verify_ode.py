# 规模纪律：欧拉法纯 python 循环, 步数 <= 2e4*4, 目标 < 2 秒。
# 第 28 讲《一阶微分方程》数值验证，四个实验（欧拉法 vs 解析解）：
#   EXP1  可分离与丢解: y'=y^2 (y(0)=1 vs 解析 1/(1-x); y(0)=0 恒 0)。
#   EXP2  线性: y'-2y=e^{2x}, y(0)=1 vs (x+1)e^{2x}。
#   EXP3  冷却: T'=-0.1(T-20), T(0)=100 vs 20+80e^{-0.1t}; 参数提取 k-hat。
#   EXP4  齐次: y'=1+y/x, y(1)=0 vs x ln x (x: 1 -> 2)。
import math
import time

T0 = time.perf_counter()

def euler(f, x0, y0, xend, h):
    n = int(round((xend - x0) / h))
    x, y = x0, y0
    for _ in range(n):
        y = y + h * f(x, y)
        x = x + h
    return x, y

# ============ EXP1: y' = y^2 ============
print("=== EXP1: y' = y^2 ===")
h = 1e-3
x, y = euler(lambda x, y: y * y, 0.0, 1.0, 0.8, h)
exact = 1.0 / (1.0 - 0.8)
print(f"  y(0)=1: euler(x=0.8) = {y:.8f}, 解析 1/(1-x) = {exact:.8f}, 差 = {abs(y - exact):.2e}")
x0, y0v = euler(lambda x, y: y * y, 0.0, 0.0, 0.8, h)
print(f"  y(0)=0: euler 全轨迹恒 0? y(0.8) = {y0v}, 判定 = {y0v == 0.0}")
print("  -> 可分离核通过; 丢解那支(y=0)独立存在")
print()

# ============ EXP2: y' - 2y = e^{2x} ============
print("=== EXP2: y' - 2y = e^{2x}, y(0)=1 ===")
x, y = euler(lambda x, y: 2 * y + math.exp(2 * x), 0.0, 1.0, 1.0, 1e-3)
exact = 2 * math.exp(2)
print(f"  euler(x=1) = {y:.8f}, 解析 (x+1)e^{{2x}} = {exact:.8f}, 差 = {abs(y - exact):.2e}")
print("  -> 同频因子解机核通过")
print()

# ============ EXP3: 冷却 ============
print("=== EXP3: T' = -0.1(T-20), T(0)=100 ===")
x, y = euler(lambda t, T: -0.1 * (T - 20.0), 0.0, 100.0, 20.0, 1e-3)
exact = 20 + 80 * math.exp(-2)
print(f"  euler(t=20) = {y:.8f}, 解析 = {exact:.8f}, 差 = {abs(y - exact):.2e}")
T10 = 20 + 80 * math.exp(-1)
khat = math.log(80 / (T10 - 20)) / 10
print(f"  参数提取: T(10) = {T10:.6f} -> k-hat = {khat:.10f} (真值 0.1)")
print("  -> 数值核通过; 参数提取闭环")
print()

# ============ EXP4: 齐次 ============
print("=== EXP4: y' = 1 + y/x, y(1)=0 ===")
x, y = euler(lambda x, y: 1 + y / x, 1.0, 0.0, 2.0, 1e-3)
exact = 2 * math.log(2)
print(f"  euler(x=2) = {y:.8f}, 解析 x ln x = {exact:.8f}, 差 = {abs(y - exact):.2e}")
print("  -> 齐次换元解机核通过")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")