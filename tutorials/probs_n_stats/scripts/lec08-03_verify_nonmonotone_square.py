# =====================================================================
# lec08-03 非单调情形：Y=X^2 且 X~N(0,1)，两支合并（第 08 讲 §4）
# 规模纪律：数值积分 + 100 万次模拟，目标 < 6 秒。
# 方法：
#   真分布：F_Y(y)=2*Phi(sqrt(y))-1（y>=0），
#           密度 f_Y(y)=1/sqrt(2*pi*y) * exp(-y/2)（y>0）。
#   1) 换元 y=t^2 验证总面积为 1（避开 y=0 处的奇点）。
#   2) 只取"正支"（漏掉负支）的密度积分只有 0.5 —— 说明两支必须合并。
#   3) 用分位点对照验证形状；并指出这就是 chi^2(1) 分布（第 15 讲）。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
# =====================================================================
import math
import numpy as np

rng = np.random.default_rng(seed=20261108)
n = 1000000


def trapz(y, x):
    return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(x)))


def phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def inv_phi(p):
    """标准正态分位点：二分法，phi 单调增。"""
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if phi(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


x = rng.normal(0.0, 1.0, n)
y = x ** 2

print("=== 实验 1：Y=X^2 的分布（X~N(0,1)） ===")
print("  真分布 F_Y(y)=2*Phi(sqrt(y))-1（y>=0）")
for yy in [0.5, 1.0, 2.0, 4.0]:
    print("    F_Y(%.1f)=%.4f   模拟=%.4f"
          % (yy, 2 * phi(math.sqrt(yy)) - 1, np.mean(y <= yy)))

print("=== 实验 2：密度总面积（换元 y=t^2 避开奇点） ===")
t = np.linspace(0.0, math.sqrt(20.0), 400001)
print("  f_Y(y)=1/sqrt(2*pi*y)*exp(-y/2)，换元后积分 = %.6f（理论 1）"
      % trapz(2.0 * np.exp(-t * t / 2) / math.sqrt(2 * math.pi), t))

print("=== 实验 3：只取正支（漏掉负支）会怎样 ===")
# 只保留 x>=0 的那一支：该支的密度是 phi(sqrt(y))/(2*sqrt(y))，积分应为 0.5
area_one_branch = trapz(
    2.0 * np.exp(-t * t / 2) / math.sqrt(2 * math.pi) / 2.0, t)
print("  单支密度积分 = %.4f（应为 0.5，正好漏掉一半概率）" % area_one_branch)
print("  -> 结论：非单调时必须把每一支反函数的贡献相加，否则丢概率。")

print("=== 实验 4：分位点对照（验证形状，不只看均值方差） ===")
for q in [0.1, 0.5, 0.9]:
    z = inv_phi((q + 1) / 2)          # 由 F_Y(y)=2Phi(sqrt(y))-1=q 反解
    print("    分位点 %.2f：模拟=%.4f  理论=%.4f" % (q, np.quantile(y, q), z * z))
print("  备注：这个分布就是自由度 1 的卡方分布 chi^2(1)，第 15 讲会正式引入。")
