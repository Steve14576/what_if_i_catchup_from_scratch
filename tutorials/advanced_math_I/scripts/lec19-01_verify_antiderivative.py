# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 19 讲《不定积分 I：原函数与凑微分》数值验证，四个实验：
#   （全部走"候选原函数 -> 中心差商 -> 与被积函数比对"，因为定积分（22 讲）尚未建立。）
#   EXP1  凑微分三组核对: (1/2)e^(x^2), ln|cos x|, 多项式。
#   EXP2  ln|x| 的负半轴核对: x = ±2, ±0.5。
#   EXP3  基础积分表抽样: arctan, arcsin, x^2.5, 1/sqrt(x)。
#   EXP4  三层打包: ln|ln x| (x=2,3,5)。
import math
import time

T0 = time.perf_counter()
H = 1e-5   # 中心差商步长: 误差 ~ O(h^2) + O(eps/h) ~ 1e-10 级, 阈值按结构取 1e-8 相对

def check(F, f, x, name):
    dq = (F(x + H) - F(x - H)) / (2 * H)
    rel = abs(dq - f(x)) / max(abs(f(x)), 1e-12)
    print(f"  {name}: x = {x}: 差商 = {dq:.10f}, 被积函数 = {f(x):.10f}, 相对差 = {rel:.2e}")
    return rel

# ============ EXP1: 凑微分三组核对 ============
print("=== EXP1: 凑微分结果的差商核对 ===")
rs = []
rs.append(check(lambda x: 0.5 * math.exp(x ** 2), lambda x: x * math.exp(x ** 2), 0.7, "(1/2)e^(x^2)"))
rs.append(check(lambda x: math.log(abs(math.cos(x))), lambda x: -math.tan(x), 0.5, "ln|cos x|"))
rs.append(check(lambda x: x ** 3 - x ** 2 + x, lambda x: 3 * x ** 2 - 2 * x + 1, 0.8, "x^3-x^2+x"))
print("  -> 三组相对差全部 < 1e-8: 候选原函数逐点过关")
print()

# ============ EXP2: ln|x| 的负半轴核对 ============
print("=== EXP2: (ln|x|)' = 1/x 的四个点 (含负半轴) ===")
for x in [2.0, -2.0, 0.5, -0.5]:
    rs.append(check(lambda t: math.log(abs(t)), lambda t: 1 / t, x, "ln|x|"))
print("  -> 四个点全部对上: |x| 不是装饰的数值证据")
print()

# ============ EXP3: 基础积分表抽样 ============
print("=== EXP3: 基础积分表倒背核对 (四行) ===")
rs.append(check(math.atan, lambda x: 1 / (1 + x ** 2), 0.3, "arctan x"))
rs.append(check(math.asin, lambda x: 1 / math.sqrt(1 - x ** 2), 0.5, "arcsin x"))
rs.append(check(lambda x: x ** 3.5 / 3.5, lambda x: x ** 2.5, 1.2, "x^3.5/3.5"))
rs.append(check(lambda x: 2 * math.sqrt(x), lambda x: 1 / math.sqrt(x), 2.0, "2 sqrt(x)"))
print("  -> 四行全过 (含任意实数幂 alpha = 2.5, 0.5)")
print()

# ============ EXP4: 三层打包 ============
print("=== EXP4: (ln|ln x|)' = 1/(x ln x) ===")
for x in [2.0, 3.0, 5.0]:
    rs.append(check(lambda t: math.log(abs(math.log(t))), lambda t: 1 / (t * math.log(t)), x, "ln|ln x|"))
print("  -> 三点全过: 疑问 5 的机器化回执")
print()

assert max(rs) < 1e-8
print(f"ALL CHECKS PASSED (max relative diff = {max(rs):.2e} < 1e-8)")
print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")