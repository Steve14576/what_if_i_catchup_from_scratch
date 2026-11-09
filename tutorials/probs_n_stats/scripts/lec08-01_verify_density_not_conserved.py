# =====================================================================
# lec08-01 破误实验：把 y=g(x) 直接代进密度为什么错（第 08 讲 §1）
# 规模纪律：数值积分 + 100 万次模拟，目标 < 6 秒。
# 方法：
#   X ~ U(0,1)。
#   情形 A：Y = 2X。真密度 1/2（0<y<2）。若直接令 f_Y(y)=f_X(y)=1，积分=2。
#   情形 B：Y = X^2。真密度 1/(2*sqrt(y))。若直接令 f_Y(y)=f_X(y)=1，
#           积分碰巧=1，但分布完全错：F(0.25) 真值 0.5，错值 0.25。
#   -> 结论：密度不守恒；"积分等于 1"都不足以发现错误。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
# =====================================================================
import math
import numpy as np

rng = np.random.default_rng(seed=20261108)


def trapz(y, x):
    return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(x)))


print("=== 情形 A：Y = 2X，X~U(0,1) ===")
n = 1000000
x = rng.uniform(0.0, 1.0, n)
y = 2 * x
print("  模拟 P(Y<=1) = %.4f（真值 0.5，因为 Y 在 (0,2) 上均匀）" % np.mean(y <= 1))
# 错做法：把 f_X(y)=1 直接当 Y 的密度，定义在 (0,2)
yg = np.linspace(0, 2, 400001)
naive = np.ones_like(yg)
print("  错误密度 f_X(y)=1 在 (0,2) 上积分 = %.4f（合法密度必须为 1）" % trapz(naive, yg))
print("  正确密度 1/2 在 (0,2) 上积分 = %.4f" % trapz(np.full_like(yg, 0.5), yg))
print("  -> 结论：Y=2X 把区间拉长一倍，密度必须整体压到 1/2；直接代入不守恒。")

print("=== 情形 B：Y = X^2，X~U(0,1) ===")
y2 = x ** 2
print("  模拟 P(Y<=0.25) = %.4f（真值 P(X<=0.5)=0.5）" % np.mean(y2 <= 0.25))
print("  模拟 Y 的中位数 = %.4f（真值 0.5^2=0.25）" % np.quantile(y2, 0.5))
# 真密度：f_Y(y)=1/(2*sqrt(y)) 在 y=0 处有奇点，直接在 y 网格上梯形积分会失真。
# 换元 y=t^2、dy=2t dt：int_0^1 1/(2t) * 2t dt = int_0^1 dt = 1。
t = np.linspace(0.0, 1.0, 400001)
area_true = trapz(np.ones_like(t), t)
print("  真密度 1/(2*sqrt(y)) 的总面积（换元 y=t^2 后）= %.6f（理论 1）" % area_true)
yg2 = np.linspace(0.0, 1.0, 400001)
print("  错误密度 f_X(y)=1 在 (0,1) 上积分 = %.4f（归一度碰巧对）"
      % trapz(np.ones_like(yg2), yg2))
# 分布函数对照：真 F(y)=sqrt(y)，错 F(y)=y
for yy in [0.25, 0.5, 0.81]:
    print("  y=%.2f  真 F=sqrt(y)=%.4f  错 F=y=%.4f" % (yy, math.sqrt(yy), yy))
print("  -> 结论：B 情形连'积分等于 1'的检查都通过了，但分布形状仍然错；")
print("     必须用分布函数或雅可比重新推，不能凭归一化蒙对。")
