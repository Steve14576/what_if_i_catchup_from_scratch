# =====================================================================
# lec05-01 二项分布的分布律与模拟（第 05 讲 §3）
# 规模纪律：精确 + 20 万次模拟，目标 < 5 秒。
# 二项分布 B(n,p)：n 次独立重复试验中成功次数 X 的分布律
#   P(X=k) = C(n,k) p^k (1-p)^(n-k)
# 输出用 GBK 安全字符（-> / [OK]）。
# =====================================================================
import math
import numpy as np

rng = np.random.default_rng(seed=20261018)
n, p = 10, 0.3


def binom(k):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


print("=== 二项分布 B(n=%d, p=%.1f) ===" % (n, p))
print("  分布律：")
for k in range(n + 1):
    print("    k=%2d  P=%.5f" % (k, binom(k)))
print("  概率总和 = %.6f" % sum(binom(k) for k in range(n + 1)))

trials = 200000
s = rng.binomial(n, p, trials)
print("  模拟 %d 次（成功次数频率对照理论）：" % trials)
for k in [0, 3, 5, 7]:
    print("    k=%2d  模拟频率=%.4f  理论=%.4f" % (k, np.mean(s == k), binom(k)))
print("-> 结论：B(n,p) 的分布律由组合数 C(n,k) 乘上成功/失败概率的乘积构成，模拟频率贴合理论。")
print("[OK] 二项分布验证完成。")