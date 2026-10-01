# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 21 讲《不定积分 III：有理函数与三角有理式》数值验证，四个实验：
#   （全部走"候选原函数 -> 中心差商 -> 与被积函数比对"；定积分（22 讲）未建立。）
#   EXP1  分解型: (1/2)ln|(x-1)/(x+1)| 对 1/(x^2-1)。
#   EXP2  配方型: ln(x^2+2x+5)+(1/2)arctan((x+1)/2) 对 (2x+3)/(x^2+2x+5)。
#   EXP3  万能代换: (2/sqrt3)arctan(tan(x/2)/sqrt3) 对 1/(2+cos x)。
#   EXP4  除法型: x^3/3 - x^2/2 + x - ln|x+1| 对 x^3/(x+1)。
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

# ============ EXP1: 分解型 ============
print("=== EXP1: (1/2)ln|(x-1)/(x+1)| 对 1/(x^2-1) ===")
F1 = lambda x: 0.5 * math.log(abs((x - 1) / (x + 1)))
f1 = lambda x: 1 / (x ** 2 - 1)
for x in [2.0, -2.0, 0.5, -0.5]:
    rs.append(check(F1, f1, x, "分解型"))
print("  -> 四点全过 (跨零两侧 + 负半轴): 部分分式机器第一关节验收")
print()

# ============ EXP2: 配方型 ============
print("=== EXP2: ln(x^2+2x+5)+(1/2)arctan((x+1)/2) 对 (2x+3)/(x^2+2x+5) ===")
F2 = lambda x: math.log(x ** 2 + 2 * x + 5) + 0.5 * math.atan((x + 1) / 2)
f2 = lambda x: (2 * x + 3) / (x ** 2 + 2 * x + 5)
for x in [0.0, 1.0, -2.0]:
    rs.append(check(F2, f2, x, "配方型"))
print("  -> 三点全过: 模式三 (对数件+反正切件) 的验收")
print()

# ============ EXP3: 万能代换 ============
print("=== EXP3: (2/sqrt3)arctan(tan(x/2)/sqrt3) 对 1/(2+cos x) ===")
F3 = lambda x: (2 / math.sqrt(3)) * math.atan(math.tan(x / 2) / math.sqrt(3))
f3 = lambda x: 1 / (2 + math.cos(x))
for x in [0.5, 1.2, -0.7]:
    rs.append(check(F3, f3, x, "万能代换"))
print("  -> 三点全过: 保底机器的验收")
print()

# ============ EXP4: 除法型 ============
print("=== EXP4: x^3/3 - x^2/2 + x - ln|x+1| 对 x^3/(x+1) ===")
F4 = lambda x: x ** 3 / 3 - x ** 2 / 2 + x - math.log(abs(x + 1))
f4 = lambda x: x ** 3 / (x + 1)
for x in [0.5, 2.0, -0.5]:
    rs.append(check(F4, f4, x, "除法型"))
print("  -> 三点全过 (x > -1 区间): 先除法后积分的验收")
print()

assert max(rs) < 1e-8
print(f"ALL CHECKS PASSED (max relative diff = {max(rs):.2e} < 1e-8)")
print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")