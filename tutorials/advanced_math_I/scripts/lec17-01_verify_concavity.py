# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 17 讲《凹凸性、拐点与极值点偏移》数值验证，四个实验：
#   EXP1  凹凸判定实弹: e^x / ln x / x^3(同侧两段) 的 f'' 符号与中点不等式。
#   EXP2  拐点三角: x^3 / x^4 / cbrt(x) 在 0 两侧的 f'' 符号。
#   EXP3  右偏: f = x e^{-x}, x1 = 0.5, 数值解 x2, 验证 x1+x2 > 2。
#   EXP4  左偏: g = e^x - 2x, x1 = 0, 数值解 x2, 验证 x1+x2 < 2ln2。
import math
import time

T0 = time.perf_counter()

# ============ EXP1: 凹凸判定实弹 ============
print("=== EXP1: 凹凸判定: f'' 符号与中点不等式 ===")
def mid_check(f, fpp_desc, x1, x2):
    m = (x1 + x2) / 2
    fm = f(m)
    avg = (f(x1) + f(x2)) / 2
    rel = "<" if fm < avg else ">"
    print(f"  {fpp_desc}: x1={x1:.6g}, x2={x2:.6g}: f(mid) = {fm:.6f} {rel} 平均 = {avg:.6f} -> {'凹' if rel == '<' else '凸'}")

mid_check(math.exp, "e^x (f''>0)", 0.0, 2.0)
mid_check(math.log, "ln x (f''<0)", 1.0, math.e ** 2)
mid_check(lambda x: x ** 3, "x^3 在正段 (f''>0)", 0.5, 2.0)
mid_check(lambda x: x ** 3, "x^3 在负段 (f''<0)", -2.0, -0.5)
print("  -> f'' 符号与中点不等式方向一致 (凹: f(mid)<平均; 凸: >)")
print()

# ============ EXP2: 拐点三角 ============
print("=== EXP2: 拐点三角 (0 两侧 f'' 符号) ===")
e = 1e-3
print(f"  x^3: f''(-1e-3) = {-6 * e:+.2e}, f''(+1e-3) = {+6 * e:+.2e} -> 变号, 拐点")
print(f"  x^4: f''(-1e-3) = {12 * e ** 2:+.2e}, f''(+1e-3) = {12 * e ** 2:+.2e} -> 同号, 非拐点")
cb = lambda x: -(2.0 / 9.0) * (abs(x) ** (-5.0 / 3.0)) * ((-1) if x < 0 else 1)   # 符号: x<0 时 f'' 为正 (负数的奇次负幂仍为负)
print(f"  cbrt(x): f''(-1e-3) = {cb(-e):+.2e}, f''(+1e-3) = {cb(e):+.2e} -> 变号, 拐点 (f''(0) 不存在)")
print("  -> 判别只看符号是否变, 巨大读数仅供定位 (读数纪律)")
print()

# ============ EXP3: 右偏 ============
print("=== EXP3: 右偏 f = x e^{-x}, x1 = 0.5 ===")
f = lambda x: x * math.exp(-x)
x1 = 0.5
target = f(x1)
lo, hi = 1.0 + 1e-12, 3.0
for _ in range(200):
    m = (lo + hi) / 2
    if (f(m) - target) * (f(hi) - target) <= 0:
        lo = m
    else:
        hi = m
x2 = (lo + hi) / 2
print(f"  f(x1) = {target:.8f}, 解出 x2 = {x2:.8f}, 和 = {x1 + x2:.8f} > 2")
print("  -> 右偏数值铁证 (对照第四节对称化证明)")
print()

# ============ EXP4: 左偏 ============
print("=== EXP4: 左偏 g = e^x - 2x, x1 = 0 ===")
g = lambda x: math.exp(x) - 2 * x
x1g = 0.0
targetg = g(x1g)
log2 = math.log(2)
lo, hi = log2 + 1e-12, 3.0
for _ in range(200):
    m = (lo + hi) / 2
    if (g(m) - targetg) * (g(hi) - targetg) <= 0:
        lo = m
    else:
        hi = m
x2g = (lo + hi) / 2
print(f"  g(0) = {targetg:.8f}, 解出 x2 = {x2g:.8f}, 和 = {x1g + x2g:.8f} < 2ln2 = {2 * log2:.8f}")
amgm = math.exp(log2) + 4 * math.exp(-log2) - 4
print(f"  AM-GM 等号位置: e^x + 4*e^(-x) - 4 在 x = ln2 处 = {amgm:.2e}")
print("  -> 左偏数值铁证 + AM-GM 等号在 x0 的确认")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")