# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 18 讲《渐近线、作图与曲率》数值验证，四个实验：
#   EXP1  斜渐近线: f = x^2/(x-1), 余项 1/(x-1) -> 0; 断点两侧 ±大数。
#   EXP2  双水平渐近线: arctan -> ±pi/2。
#   EXP3  抛物线曲率表: y=x^2, kappa = 2/(1+4x^2)^{3/2}, 公式 vs 差分。
#   EXP4  圆 R=2 恒定曲率 (参数差分) + e^x 曲率峰值 (x=-ln sqrt2)。
import math
import time

T0 = time.perf_counter()

# ============ EXP1: 斜渐近线 ============
print("=== EXP1: f = x^2/(x-1) = x + 1 + 1/(x-1) ===")
f1 = lambda x: x ** 2 / (x - 1)
for x in [10.0, 100.0, 1000.0]:
    rem = f1(x) - (x + 1)
    print(f"  x = {x:6.0f}: f(x)-(x+1) = {rem:.3e} (= 1/(x-1) = {1 / (x - 1):.3e})")
print(f"  断点两侧: f(1.1) = {f1(1.1):+.4f}, f(0.9) = {f1(0.9):+.4f} (趋向 ±无穷)")
print("  -> 余项趋于 0 (斜渐近线 y=x+1); 断点两侧发散 (垂直渐近线 x=1)")
print()

# ============ EXP2: 双水平渐近线 ============
print("=== EXP2: arctan 的双水平渐近线 ===")
for x in [10.0, 100.0, 1000.0]:
    print(f"  x = {x:6.0f}: arctan = {math.atan(x):+.8f};  x = {-x:6.0f}: arctan = {math.atan(-x):+.8f}")
print(f"  pi/2 = {math.pi / 2:.8f}")
print("  -> 两端分别贴 ±pi/2: 两侧独立的实弹")
print()

# ============ EXP3: 抛物线曲率表 ============
print("=== EXP3: y = x^2, kappa 公式值 vs 数值差分 ===")
h = 1e-3
for x in [0.0, 0.5, 1.0]:
    k_formula = 2 / (1 + 4 * x ** 2) ** 1.5
    f = lambda t: t ** 2
    yp = (f(x + h) - f(x - h)) / (2 * h)
    ypp = (f(x + h) - 2 * f(x) + f(x - h)) / h ** 2
    k_num = abs(ypp) / (1 + yp ** 2) ** 1.5
    print(f"  x = {x}: 公式 = {k_formula:.6f}, 差分 = {k_num:.6f}, 差 = {k_num - k_formula:+.2e}")
print("  -> 曲率随 |x| 消减 (顶点弯得最厉害)")
print()

# ============ EXP4: 圆恒定曲率 + e^x 峰值 ============
print("=== EXP4a: 圆 R=2 的恒定曲率 (参数差分) ===")
hh = 1e-4
X = lambda t: 2 * math.cos(t)
Y = lambda t: 2 * math.sin(t)
for th in [0.3, 1.1, 2.5, 4.5]:
    dx = (X(th + hh) - X(th - hh)) / (2 * hh)
    d2x = (X(th + hh) - 2 * X(th) + X(th - hh)) / hh ** 2
    dy = (Y(th + hh) - Y(th - hh)) / (2 * hh)
    d2y = (Y(th + hh) - 2 * Y(th) + Y(th - hh)) / hh ** 2
    yp = dy / dx
    ypp = (d2y * dx - dy * d2x) / dx ** 3
    kappa = abs(ypp) / (1 + yp ** 2) ** 1.5
    print(f"  theta = {th}: kappa = {kappa:.6f} (理论 1/R = 0.5)")

print("=== EXP4b: e^x 曲率峰值 ===")
g = lambda x: math.exp(x) / (1 + math.exp(2 * x)) ** 1.5
x_star = -math.log(math.sqrt(2))
peak = 2 / (3 * math.sqrt(3))
print(f"  峰值点 x = -ln(sqrt2) = {x_star:.6f}: kappa = {g(x_star):.6f} (解析 2/(3sqrt3) = {peak:.6f})")
print(f"  两侧: g(-1) = {g(-1):.6f}, g(0) = {g(0):.6f} (均低于峰值)")
print("  -> 圆处处 0.5; e^x 最弯点 x=-ln(sqrt2)")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")