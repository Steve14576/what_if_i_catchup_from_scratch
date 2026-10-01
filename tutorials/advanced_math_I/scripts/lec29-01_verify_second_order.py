# 规模纪律：欧拉一阶系统, h=1e-4; EXP3 到 2pi 约 6.3 万步; 目标 < 2 秒。
# 第 29 讲《二阶常系数线性微分方程》数值验证，四个实验（欧拉 vs 解析）：
#   EXP1  齐次三情形: 不同实根(1/3)e^{2x}+(2/3)e^{-x}; 重根(1-x)e^x; 复根 cos x。
#   EXP2  非齐次共振: y''-y'-2y=e^{2x}: (5/9)e^2-(2/9)e^{-1} at x=1。
#   EXP3  三角共振: y''+y=cos x: y=(x/2)sin x at pi 与 2pi。
#   EXP4  叠加拆件: y''-2y'+y=e^x+x: y=(-2+x+x^2/2)e^x+x+2 at x=1。
import math
import time

T0 = time.perf_counter()

def euler_system(f, x0, y0, v0, xend, h):
    # y' = v, v' = f(x, y, v)
    n = int(round((xend - x0) / h))
    x, y, v = x0, y0, v0
    for _ in range(n):
        dv = f(x, y, v)
        y = y + h * v
        v = v + h * dv
        x = x + h
    return x, y

h = 1e-4

# ============ EXP1: 三情形 ============
print("=== EXP1: homogeneous three cases at x=1 ===")
_, y1 = euler_system(lambda x, y, v: v + 2 * y, 0.0, 1.0, 0.0, 1.0, h)          # y''=y'+2y
e1 = math.exp(2) / 3 + 2 * math.exp(-1) / 3
print(f"  r=2,-1 : euler = {y1:.8f}, exact = {e1:.8f}, err = {abs(y1 - e1):.2e}")
_, y2 = euler_system(lambda x, y, v: 2 * v - y, 0.0, 1.0, 0.0, 1.0, h)          # y''=2y'-y (重根 r=1)
e2 = 0.0
print(f"  重根 r=1: euler = {y2:.8f}, exact = {e2:.8f}, err = {abs(y2 - e2):.2e}")
_, y3 = euler_system(lambda x, y, v: -y, 0.0, 1.0, 0.0, 1.0, h)                 # y''=-y (复根)
e3 = math.cos(1.0)
print(f"  复根 ±i : euler = {y3:.8f}, exact = {e3:.8f}, err = {abs(y3 - e3):.2e}")
print("  -> 三情形全部机核")
print()

# ============ EXP2: 非齐次共振 ============
print("=== EXP2: y'' - y' - 2y = e^{2x}, y(0)=0, y'(0)=1 ===")
_, y4 = euler_system(lambda x, y, v: v + 2 * y + math.exp(2 * x), 0.0, 0.0, 1.0, 1.0, h)
e4 = (5 / 9) * math.exp(2) - (2 / 9) * math.exp(-1)
print(f"  euler = {y4:.8f}, exact = {e4:.8f}, err = {abs(y4 - e4):.2e}")
print("  -> 共振升 k 的解机核")
print()

# ============ EXP3: 三角共振 ============
print("=== EXP3: y'' + y = cos x, y(0)=0, y'(0)=0 ===")
# 观察点选 pi/2 与 3pi/2 (解析 pi/4 与 -3pi/4, 三倍增长), 不用 k*pi 的零点
for xend in [math.pi / 2, 3 * math.pi / 2]:
    _, yv = euler_system(lambda x, y, v: -y + math.cos(x), 0.0, 0.0, 0.0, xend, h)
    ex = (xend / 2) * math.sin(xend)
    print(f"  x = {xend:.4f}: euler = {yv:.8f}, 解析 (x/2)sin x = {ex:.8f}, err = {abs(yv - ex):.2e}")
print("  -> 振幅线性增长 (pi/4 -> -3pi/4): 共振的机核")
print()

# ============ EXP4: 叠加 ============
print("=== EXP4: y'' - 2y' + y = e^x + x, y(0)=0, y'(0)=0 ===")
_, y6 = euler_system(lambda x, y, v: 2 * v - y + math.exp(x) + x, 0.0, 0.0, 0.0, 1.0, h)
e6 = (-2 + 1 + 0.5) * math.exp(1) + 1 + 2
print(f"  euler = {y6:.8f}, exact = {e6:.8f}, err = {abs(y6 - e6):.2e}")
print("  -> 叠加拆件机核")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")