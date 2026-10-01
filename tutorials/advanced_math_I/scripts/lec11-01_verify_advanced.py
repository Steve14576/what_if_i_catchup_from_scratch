# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 11 讲《求导进阶》数值验证，四个实验：
#   EXP1  高阶表核验: sin 在 pi/4 的 f''、f''' 中心差分 vs 公式 (-sin, -cos)。
#   EXP2  幂指函数: x^x 在 x0=2 差商 -> 2^2*(ln2+1) = 6.7726。
#   EXP3  参数方程: 单位圆 t0=pi/3, 一阶差分 vs -cot; 二阶 正确(-csc^3) vs 错误(tan) 对照。
#   EXP4  隐函数: 圆在 (3,4) 割线斜率 -> -0.75; y'' = -25/y^3 取值打印。
import math
import time

T0 = time.perf_counter()

# ============ EXP1: 高阶表核验 (sin 在 pi/4) ============
print("=== EXP1: sin 在 pi/4 的二、三阶导 (中心差分) ===")
f = math.sin
x0 = math.pi / 4
for h in [1e-3, 1e-4]:
    d2 = (f(x0 + h) - 2 * f(x0) + f(x0 - h)) / h ** 2
    print(f"  h = {h:.0e}: f''(数值) = {d2:.8f}, 公式 -sin(pi/4) = {-math.sin(x0):.8f}, 差 = {d2 + math.sin(x0):+.2e}")
h = 1e-2   # 三阶差分噪声较大, 用较粗步长并如实读量级
d3 = (f(x0 + 2 * h) - 2 * f(x0 + h) + 2 * f(x0 - h) - f(x0 - 2 * h)) / (2 * h ** 3)
print(f"  h = {h:.0e}: f'''(数值, 粗) = {d3:.6f}, 公式 -cos(pi/4) = {-math.cos(x0):.6f} (高阶差分精度天然粗, 读量级)")
print("  -> 表的 sin(x+n*pi/2) 公式在 n=2,3 的实弹 (f'' 细, f''' 粗)")
print()

# ============ EXP2: 幂指函数 x^x ============
print("=== EXP2: x^x 在 x0=2, 差商 -> 4*(ln2+1) = 6.7726 ===")
g = lambda x: x ** x
formula = 4 * (math.log(2) + 1)
for h in [1e-1, 1e-3, 1e-5]:
    dq = (g(2 + h) - g(2)) / h
    print(f"  h = {h:.0e}: 差商 = {dq:.8f}, 公式值 = {formula:.8f}, 差 = {dq - formula:+.2e}")
print("  -> 对数求导 (幂指函数) 的数值对账")
print()

# ============ EXP3: 参数方程 (单位圆 t0=pi/3) ============
print("=== EXP3: 参数方程单位圆 t0=pi/3 ===")
t0 = math.pi / 3
X = lambda t: math.cos(t)
Y = lambda t: math.sin(t)
for h in [1e-3, 1e-5]:
    dydt = (Y(t0 + h) - Y(t0)) / h
    dxdt = (X(t0 + h) - X(t0)) / h
    print(f"  h = {h:.0e}: 一阶差分 = {dydt / dxdt:.8f}, 公式 -cot(t0) = {-math.cos(t0) / math.sin(t0):.8f}")
correct = -1 / math.sin(t0) ** 3
wrong = math.tan(t0)
print(f"  二阶对照: 正确值 -csc^3(t0) = {correct:.6f}; 错误公式 (d2y/dt2)/(d2x/dt2) = {wrong:.6f}")
print("  -> 一阶对上; 二阶两法异号且量级不同: '只是除错了'的代价")
print()

# ============ EXP4: 隐函数 (圆在 (3,4)) ============
print("=== EXP4: 隐函数 圆 x^2+y^2=25 在 (3,4) ===")
t_p = math.atan2(4.0, 3.0)      # 点 (3,4) 对应角度
for h in [1e-3, 1e-5]:
    x1, y1 = 5 * math.cos(t_p - h), 5 * math.sin(t_p - h)
    x2, y2 = 5 * math.cos(t_p + h), 5 * math.sin(t_p + h)
    slope = (y2 - y1) / (x2 - x1)
    print(f"  h = {h:.0e}: 割线斜率 = {slope:.8f}, 公式 -x0/y0 = {-3 / 4:.8f}")
ypp = -25 / 4 ** 3
print(f"  y''(3,4) = -25/y^3 = {ypp:.6f} (二阶隐导公式取值)")
print("  -> 割线趋 -0.75 (隐函数求导数值对账); y'' 公式入列")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")