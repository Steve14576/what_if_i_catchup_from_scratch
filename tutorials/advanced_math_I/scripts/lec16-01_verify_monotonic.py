# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 16 讲《单调性与极值》数值验证，四个实验：
#   EXP1  单调区间采样: f=x^3-3x^2+1, 三段符号 +/-/+, 极值 (0,1) (2,-3)。
#   EXP2  等号边界: x^3 (f'>=0 等号孤立, 仍严格增) vs 常数函数。
#   EXP3  判据矩阵: x^3/x^4 左右差商与 f''(0), |x| 特案。
#   EXP4  含参分箱: f=x^3-3ax, a=-1/0/1 三箱。
import math
import time

T0 = time.perf_counter()

# ============ EXP1: 单调区间 ============
print("=== EXP1: f = x^3-3x^2+1, f' = 3x(x-2), 分界点 0 与 2 ===")
f1 = lambda x: x ** 3 - 3 * x ** 2 + 1
df1 = lambda x: 3 * x ** 2 - 6 * x
for x in [-1.0, 1.0, 3.0]:
    print(f"  段代表 x = {x:+.1f}: f' = {df1(x):+.4f}")
print(f"  f(0) = {f1(0):.4f} (极大), f(2) = {f1(2):.4f} (极小)")
print(f"  极大核对: f(-0.5) = {f1(-0.5):.4f} < f(0), f(0.5) = {f1(0.5):.4f} < f(0)")
print(f"  极小核对: f(1.5) = {f1(1.5):.4f} > f(2), f(2.5) = {f1(2.5):.4f} > f(2)")
print("  -> 三段符号 +/-/+ 与极值点值吻合")
print()

# ============ EXP2: 等号边界 ============
print("=== EXP2: 等号边界: x^3 vs 常数函数 ===")
g = lambda x: x ** 3
for x in [-1.0, -0.5, 0.0, 0.5, 1.0]:
    print(f"  x = {x:+.1f}: (x^3)' = {3 * x ** 2:.4f}, x^3 = {g(x):+.4f} (严格升)")
print(f"  常数函数 1: f' = 0, 值恒为 1 (非严格增)")
print("  -> x^3: f'>=0 且等号孤立 -> 仍严格增; 常数: 等号成片 -> 非严格")
print()

# ============ EXP3: 判据矩阵 ============
print("=== EXP3: 判据矩阵 (0 处) ===")
h = 1e-4
for name, f in [("x^3", lambda x: x ** 3), ("x^4", lambda x: x ** 4)]:
    dql = (f(-h) - f(0)) / (-h)
    dqr = (f(h) - f(0)) / h
    d2 = (f(h) - 2 * f(0) + f(-h)) / h ** 2
    same = dql * dqr > 0
    verdict = "非极值" if same else "极小"
    print(f"  {name}: 左差商 = {dql:+.2e}, 右差商 = {dqr:+.2e}, f''(0) ~ {d2:.2e} -> {verdict}")
print(f"  |x|: 左差商 = {(abs(-h) - 0) / (-h):+.2e}, 右差商 = {(abs(h) - 0) / h:+.2e} -> 不可导但极小")
print("  -> x^3/x^4 都 f''(0)=0 (二阶失效), 一阶符号翻不翻定命运; |x| 不可导照判")
print()

# ============ EXP4: 含参分箱 ============
print("=== EXP4: f = x^3-3ax 三箱代表 ===")
for a in [-1.0, 0.0, 1.0]:
    if a > 1e-12:
        roots = sorted([a ** 0.5, -(a ** 0.5)])   # 驻点 ±sqrt(a) (a>0 时才有)
    elif abs(a) < 1e-12:
        roots = [0.0]
    else:
        roots = []
    f4 = lambda x, a=a: x ** 3 - 3 * a * x
    if not roots:
        print(f"  a = {a:+.0f}: 无驻点, f' = 3x^2-3a > 0 恒成立 -> 全区间严格增")
    else:
        vals = [f4(r) for r in roots]
        tag = "极值 ±2a√a" if len(roots) == 2 else "水平拐点 (非极值)"
        print(f"  a = {a:+.0f}: 驻点 {roots}, f 值 {[round(v, 4) for v in vals]} -> {tag}")
print("  -> a<=0 一箱 (严格增); a>0 一箱 (两根 ±sqrt(a), 极值 ±2a√a)")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")