# 规模纪律：欧拉一阶系统 h=1e-4, 目标 < 2 秒。
# 第 30 讲《常数变易法、降阶与欧拉方程》数值验证，四个实验：
#   EXP1  常数变易 sec x: y''+y=sec x, y(0)=1, y'(0)=0 解析 cos+cos*ln|cos|+x sin x。
#   EXP2  降阶型 II: y''=1+(y')^2, y(0)=y'(0)=0 解析 -ln cos x (与 26 讲孪生)。
#   EXP3  欧拉方程: x^2 y'' + x y' - y = 0, y(1)=2, y'(1)=0 解析 x+1/x。
#   EXP4  朗斯基观测: (cos,sin) 恒 1; (e^x,e^-x) 恒 -2。
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

# ============ EXP1: 常数变易 sec x ============
print("=== EXP1: y'' + y = sec x, y(0)=1, y'(0)=0, at x=0.5 ===")
_, y1 = euler_system(lambda x, y, v: -y + 1.0 / math.cos(x), 0.0, 1.0, 0.0, 0.5, h)
e1 = math.cos(0.5) + math.cos(0.5) * math.log(abs(math.cos(0.5))) + 0.5 * math.sin(0.5)
print(f"  euler = {y1:.8f}, exact = {e1:.8f}, err = {abs(y1 - e1):.2e}")
print("  -> 变易法 sec x 解机核")
print()

# ============ EXP2: 降阶型 II ============
print("=== EXP2: y'' = 1 + (y')^2, y(0)=y'(0)=0, at x=0.5 ===")
_, y2 = euler_system(lambda x, y, v: 1.0 + v * v, 0.0, 0.0, 0.0, 0.5, h)
e2 = -math.log(math.cos(0.5))
print(f"  euler = {y2:.8f}, exact = {e2:.8f}, err = {abs(y2 - e2):.2e}")
print("  -> 降阶链机核 (与 26 讲弧长例孪生)")
print()

# ============ EXP3: 欧拉方程 ============
print("=== EXP3: x^2 y'' + x y' - y = 0, y(1)=2, y'(1)=0, at x=2 ===")
_, y3 = euler_system(lambda x, y, v: (y - x * v) / (x * x), 1.0, 2.0, 0.0, 2.0, h)
e3 = 2 + 1 / 2
print(f"  euler = {y3:.8f}, exact = {e3:.8f}, err = {abs(y3 - e3):.2e}")
print("  -> x=e^t 换元机核")
print()

# ============ EXP4: 朗斯基观测 ============
print("=== EXP4: Wronskian stays nonzero ===")
for x in [0.0, 1.0, 2.0]:
    Wcs = math.cos(x) * math.cos(x) - math.sin(x) * (-math.sin(x))
    Wex = math.exp(x) * (-math.exp(-x)) - math.exp(-x) * math.exp(x)
    print(f"  x = {x}: W(cos,sin) = {Wcs}, W(e^x,e^-x) = {Wex}")
print("  -> 要么处处非零的比赛: 恒 1 与恒 -2")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")