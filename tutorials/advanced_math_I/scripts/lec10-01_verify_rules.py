# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 10 讲《求导法则》数值验证，四个实验（数值差商 vs 公式值 对账）：
#   EXP1  乘积法则: f = x^2*sin(x) 在 x0=1, 差商 -> 2*sin(1)+cos(1)。
#   EXP2  链式法则: f = sin(x^2) 在 x0=1, 差商 -> 2*cos(1)。
#   EXP3  反函数求导: f = arcsin(x) 在 x0=0.5, 差商 -> 1/sqrt(1-0.25)。
#   EXP4  表抽样: sin、exp、log 在 x0=1 的差商 -> cos(1)、e、1。
import math
import time

T0 = time.perf_counter()

def report(name, f, x0, formula):
    print(f"{name}: 公式值 = {formula:.10f}")
    for h in [0.1, 0.01, 1e-3, 1e-6]:
        dq = (f(x0 + h) - f(x0)) / h
        print(f"  h = {h:.0e}: 差商 = {dq:.10f}, 与公式之差 = {dq - formula:+.3e}")
    print()

# ============ EXP1: 乘积法则 ============
report("EXP1 乘积法则 x^2*sin(x) 在 x0=1", lambda x: x ** 2 * math.sin(x), 1.0,
       2 * math.sin(1) + math.cos(1))

# ============ EXP2: 链式法则 ============
report("EXP2 链式法则 sin(x^2) 在 x0=1", lambda x: math.sin(x ** 2), 1.0,
       2 * math.cos(1))

# ============ EXP3: 反函数求导 ============
report("EXP3 反函数 arcsin(x) 在 x0=0.5", math.asin, 0.5,
       1 / math.sqrt(0.75))

# ============ EXP4: 表抽样 ============
print("EXP4 表抽样 (x0=1): sin' -> cos(1), exp' -> e, ln' -> 1")
for name, f, formula in [("sin", math.sin, math.cos(1)),
                         ("exp", math.exp, math.e),
                         ("ln", math.log, 1.0)]:
    h = 1e-6
    dq = (f(1 + h) - f(1)) / h
    print(f"  {name}: 差商 = {dq:.10f}, 公式值 = {formula:.10f}, 差 = {dq - formula:+.3e}")
print("  -> 三格表单的实弹核验 (exp 行的差商含 e*(e^h-1)/h 的结构)")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")