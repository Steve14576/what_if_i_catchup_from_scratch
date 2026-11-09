# =====================================================================
# lec08-02 单调情形：分布函数法 + 公式法对照（第 08 讲 §2 / §3）
# 规模纪律：数值积分 + 100 万次模拟，目标 < 6 秒。
# 方法：
#   实验 1：X~U(0,1)，Y=X^2。分布函数法得 F_Y(y)=sqrt(y)，
#           求导得 f_Y(y)=1/(2*sqrt(y))；用换元验证总面积为 1；
#           用分位点对照 q -> q^2 验证分布形状。
#   实验 2：X~N(3,2^2)，Y=-2X+5。公式法给 N(-1,4^2)；
#           用模拟均值/标准差与 P(Y<=0) 对照理论值。
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


print("=== 实验 1：X~U(0,1)，Y=X^2（分布函数法） ===")
x = rng.uniform(0.0, 1.0, n)
y = x ** 2
# 换元：y=t^2, dy=2t dt  =>  int_0^1 1/(2 sqrt(y)) dy = int_0^1 dt = 1
t = np.linspace(0.0, 1.0, 400001)
print("  真密度总面积（换元后）= %.6f（理论 1）" % trapz(np.ones_like(t), t))
for q in [0.1, 0.25, 0.5, 0.75, 0.9]:
    print("    分位点 %.2f：模拟=%.4f  理论 q^2=%.4f"
          % (q, np.quantile(y, q), q * q))
print("  -> 结论：F_Y(y)=sqrt(y)、f_Y(y)=1/(2 sqrt(y))；分位点整条对上。")

print("=== 实验 2：X~N(3,2^2)，Y=-2X+5（公式法） ===")
x2 = rng.normal(3.0, 2.0, n)
y2 = -2.0 * x2 + 5.0
print("  Y 模拟均值=%.4f  标准差=%.4f（理论 -1 与 4）"
      % (np.mean(y2), np.std(y2)))
print("  P(Y<=0): 模拟=%.4f  理论 Phi((0-(-1))/4)=Phi(0.25)=%.4f"
      % (np.mean(y2 <= 0), phi(0.25)))
print("  -> 结论：a=-2 时尺度=|a|*sigma=4（取绝对值），中心=-2*3+5=-1。")

print("=== 实验 3：公式法 vs 分布函数法 的一致性 ===")
# 对 Y=X^2 用公式法：y=h(x)=x^2 在 (0,1) 上单调增，反函数 x=sqrt(y)，h'(y)=1/(2 sqrt(y))
yg = np.linspace(1e-6, 1 - 1e-6, 200001)
f_formula = 1.0 / (2.0 * np.sqrt(yg))
# 分布函数法：F_Y(y)=P(X<=sqrt(y))=sqrt(y)，求导同样得 1/(2 sqrt(y))
f_cdf = 0.5 / np.sqrt(yg)
print("  公式法与分布函数法最大差 = %.2e" % np.max(np.abs(f_formula - f_cdf)))
print("  -> 结论：单调可导时两种方法必然一致，公式法只是分布函数法求导的成品。")
