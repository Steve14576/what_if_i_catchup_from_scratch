# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 20 讲《不定积分 II：换元与分部》数值验证，四个实验：
#   （全部走"候选原函数 -> 中心差商 -> 与被积函数比对"；定积分（22 讲）未建立。）
#   EXP1  根式主例: (1/2)arcsin x + (x/2)sqrt(1-x^2) 对 sqrt(1-x^2)。
#   EXP2  分部四例: xe^x-e^x; (x^2-2x+2)e^x; x ln x - x; x^2/2 arctan x - x/2 + arctan x/2。
#   EXP3  循环型: e^x(sin x - cos x)/2 对 e^x sin x。
#   EXP4  倍角综合: (arcsin x - x sqrt(1-x^2))/2 对 x^2/sqrt(1-x^2)。
import math
import time

T0 = time.perf_counter()
H = 1e-5   # 中心差商: 误差 ~ O(h^2)+O(eps/h) ~ 1e-10 级, 阈值按结构取 1e-8 相对

def check(F, f, x, name):
    dq = (F(x + H) - F(x - H)) / (2 * H)
    rel = abs(dq - f(x)) / max(abs(f(x)), 1e-12)
    print(f"  {name}: x = {x}: 差商 = {dq:.10f}, 被积函数 = {f(x):.10f}, 相对差 = {rel:.2e}")
    return rel

rs = []

# ============ EXP1: 根式主例 ============
print("=== EXP1: (1/2)arcsin x + (x/2)sqrt(1-x^2) 对 sqrt(1-x^2) ===")
F1 = lambda x: 0.5 * math.asin(x) + 0.5 * x * math.sqrt(1 - x ** 2)
f1 = lambda x: math.sqrt(1 - x ** 2)
for x in [0.3, 0.6, -0.5]:
    rs.append(check(F1, f1, x, "根式主例"))
print("  -> 三点全过: 第三节主例的机器化验收")
print()

# ============ EXP2: 分部四例 ============
print("=== EXP2: 分部四例核对 ===")
rs.append(check(lambda x: x * math.exp(x) - math.exp(x), lambda x: x * math.exp(x), 1.3, "xe^x-e^x (一次)"))
rs.append(check(lambda x: (x ** 2 - 2 * x + 2) * math.exp(x), lambda x: x ** 2 * math.exp(x), 0.8, "(x^2-2x+2)e^x (两次)"))
rs.append(check(lambda x: x * math.log(x) - x, lambda x: math.log(x), 2.5, "x ln x - x (退化)"))
rs.append(check(lambda x: 0.5 * x ** 2 * math.atan(x) - 0.5 * x + 0.5 * math.atan(x), lambda x: x * math.atan(x), 0.9, "x arctan x (混合)"))
print("  -> 四例全过: 一次/两次/退化/混合全覆盖")
print()

# ============ EXP3: 循环型 ============
print("=== EXP3: e^x(sin x - cos x)/2 对 e^x sin x ===")
F3 = lambda x: 0.5 * math.exp(x) * (math.sin(x) - math.cos(x))
f3 = lambda x: math.exp(x) * math.sin(x)
for x in [0.5, 1.2, 2.0]:
    rs.append(check(F3, f3, x, "循环型"))
print("  -> 三点全过: 两次回代解方程的答案核实")
print()

# ============ EXP4: 倍角综合 ============
print("=== EXP4: (arcsin x - x sqrt(1-x^2))/2 对 x^2/sqrt(1-x^2) ===")
F4 = lambda x: 0.5 * (math.asin(x) - x * math.sqrt(1 - x ** 2))
f4 = lambda x: x ** 2 / math.sqrt(1 - x ** 2)
for x in [0.3, 0.6, -0.4]:
    rs.append(check(F4, f4, x, "倍角综合"))
print("  -> 三点全过: sin 代换+降幂+回代三段式覆盖")
print()

assert max(rs) < 1e-8
print(f"ALL CHECKS PASSED (max relative diff = {max(rs):.2e} < 1e-8)")
print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")