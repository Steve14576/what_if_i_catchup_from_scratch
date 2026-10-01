# 规模纪律：纯打印表（无大规模计算），目标 < 2 秒。
# 第 12 讲《微分》数值验证，四个实验：
#   EXP1  dy vs Delta y: y=x^2 在 1, 差值精确等于 dx^2 (主部与尾料)。
#   EXP2  线性近似实弹: (1.02)^3 与 sqrt(1.02) 的近似值/真实值/误差 + 主项估计。
#   EXP3  相对误差的 ln 形态: 正方形 A=x^2, 比较 Delta A/A 与 2dx/x 与 d(lnA)。
#   EXP4  o(dx) 的机器版: sin(dx) 的主部 dx 与尾料, 尾料/dx -> 0, 尾料/dx^2 量级。
import math
import time

T0 = time.perf_counter()

# ============ EXP1: dy vs Delta y ============
print("=== EXP1: y = x^2, x0 = 1: Delta y vs dy = 2*dx ===")
for dx in [0.1, 0.01, 1e-3, 1e-4]:
    dy_true = (1 + dx) ** 2 - 1
    dy_lin = 2 * dx
    gap = dy_true - dy_lin
    print(f"  dx = {dx:.0e}: Delta y = {dy_true:.10f}, dy = {dy_lin:.10f}, 差 = {gap:.3e} (= dx^2 = {dx ** 2:.3e})")
print("  -> 差值恰为 dx^2: 尾料比 dx 高一阶 (o(dx) 的活体)")
print()

# ============ EXP2: 线性近似实弹 ============
print("=== EXP2: 线性近似的精度账 ===")
approx1 = 1 + 3 * 0.02
exact1 = 1.02 ** 3
est1 = 0.5 * 6 * 0.02 ** 2
print(f"  (1.02)^3: 近似 = {approx1:.10f}, 真实 = {exact1:.10f}, 误差 = {exact1 - approx1:.3e}, 主项估计 = {est1:.3e}")
approx2 = 1 + 0.5 * 0.02
exact2 = math.sqrt(1.02)
est2 = 0.5 * (-1 / 4) * 0.02 ** 2
print(f"  sqrt(1.02): 近似 = {approx2:.10f}, 真实 = {exact2:.10f}, 误差 = {exact2 - approx2:.3e}, 主项估计 = {est2:.3e}")
print("  -> 误差与 0.5*f''*dx^2 的主项估计吻合: 以直代曲的精度账")
print()

# ============ EXP3: 相对误差的 ln 形态 ============
print("=== EXP3: 正方形 A = x^2, x = 1, dx = 0.01 ===")
dA_over_A = ((1.01) ** 2 - 1) / 1.0
lin = 2 * 0.01
dlnA = 2 * 0.01 / 1.0
print(f"  Delta A / A = {dA_over_A:.6f}, 2*dx/x = {lin:.6f}, d(lnA) = {dlnA:.6f}")
print(f"  差值 (高阶尾料) = {dA_over_A - lin:.2e}")
print("  -> Delta A/A 与 2% 差一个尾料; d(lnA) 精确入列: 相对误差 = d(ln y)")
print()

# ============ EXP4: o(dx) 的机器版 ============
print("=== EXP4: sin(dx) 的主部与尾料 ===")
for dx in [0.1, 0.01, 1e-3]:
    main = dx
    tail = math.sin(dx) - dx
    print(f"  dx = {dx:.0e}: sin = {math.sin(dx):.10f}, 主部 dx = {main:.1e}, 尾料 = {tail:+.3e}, 尾料/dx = {tail / dx:+.3e}, 尾料/dx^2 = {tail / dx ** 2:+.6f}")
print("  -> 尾料/dx -> 0 (o(dx) 定义实弹); 尾料/dx^2 ~ -dx/6 (三阶差结构的预告)")
print()

print(f"TOTAL runtime: {time.perf_counter() - T0:.2f}s")