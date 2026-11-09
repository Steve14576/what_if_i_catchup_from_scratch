# =====================================================================
# lec07-02 标准化、查表与 3-sigma 法则（第 07 讲 §3 / §4 / §5）
# 规模纪律：100 万次模拟 + math.erf 精确值，目标 < 5 秒。
# 方法：
#   1) 用 math.erf 算标准正态分布函数 Phi(z)，给出查表用的关键点。
#   2) 对称性：Phi(-z) = 1 - Phi(z)。
#   3) 模拟 X~N(5, 2^2)，标准化 Z=(X-5)/2，检验 Z 的均值/标准差
#      与 P(Z<=1.5) 是否对上 N(0,1) 的理论值。
#   4) 3-sigma：P(|X-mu|<k*sigma) 随 k=1,2,3 的理论值与模拟值。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
# =====================================================================
import math
import numpy as np

rng = np.random.default_rng(seed=20261101)


def phi(z):
    """标准正态分布函数 Phi(z)=P(Z<=z)，用 erf 精确计算。"""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


print("=== 实验 1：查表用的关键 Phi(z) 值（z>=0） ===")
for z in [0.0, 0.5, 1.0, 1.28, 1.645, 1.96, 2.0, 2.58, 3.0]:
    print("  z=%.3f  Phi(z)=%.4f" % (z, phi(z)))
print("  -> 结论：1.645->0.95、1.96->0.975、2.58->0.995，这三个最常用。")

print("=== 实验 2：负 z 用对称性 ===")
for z in [1.0, 1.5, 2.0]:
    print("  Phi(-%.1f)=%.4f   1-Phi(%.1f)=%.4f" % (z, phi(-z), z, 1 - phi(z)))
print("  -> 结论：Phi(-z)=1-Phi(z)，所以表只印 z>=0 就够。")

print("=== 实验 3：标准化把 N(5, 2^2) 变成 N(0,1) ===")
mu, sigma = 5.0, 2.0
n = 1000000
x = rng.normal(mu, sigma, n)
z = (x - mu) / sigma
print("  原始 X: 模拟均值=%.4f  模拟标准差=%.4f（理论 5 / 2）"
      % (np.mean(x), np.std(x)))
print("  标准化 Z: 模拟均值=%.4f  模拟标准差=%.4f（理论 0 / 1）"
      % (np.mean(z), np.std(z)))
print("  P(Z<=1.5): 模拟=%.4f  查表=%.4f" % (np.mean(z <= 1.5), phi(1.5)))
print("  P(X<=8):   模拟=%.4f  查表=%.4f（z=(8-5)/2=1.5）"
      % (np.mean(x <= 8), phi(1.5)))
print("  -> 结论：标准化只做平移和缩放，分布形状不变，故可统一查一张表。")

print("=== 实验 4：3-sigma 法则 P(|X-mu| < k*sigma) ===")
for k in [1, 2, 3]:
    theory = phi(k) - phi(-k)
    sim = np.mean(np.abs(x - mu) < k * sigma)
    print("  k=%d 理论=%.4f  模拟=%.4f  落在区间外=%.4f"
          % (k, theory, sim, 1 - theory))
print("  -> 结论：3-sigma 覆盖 99.73%，但这不是铁律，只是正态下的概率。")

print("=== 实验 5：换成指数分布，同样的 1-sigma 区间就不是 68% ===")
# Exp(1)：密度 e^{-x}（x>0），分布函数 F(x)=1-e^{-x}，中心 mu=1，尺度 sigma=1。
# P(|X-1|<1) = P(0<X<2) = F(2)-F(0) = 1-e^{-2}。
e = rng.exponential(scale=1.0, size=n)
print("  理论 P(0<X<2) = 1-e^{-2} = %.4f" % (1 - math.exp(-2)))
print("  模拟 P(|X-1|<1) = %.4f" % np.mean(np.abs(e - 1.0) < 1.0))
print("  同样 k=1，正态给 0.6827，指数给约 0.8647")
print("  -> 结论：1-sigma 的 68% 是正态专属结论，换分布就不成立。")
