# =====================================================================
# lec05-02 二项分布到泊松分布的极限（第 05 讲 §4）
# 规模纪律：小规模精确计算，目标 < 3 秒。
# 令 p = lambda/n，当 n -> 无穷、p -> 0 而 np=lambda 固定时，
#   B(n,p) 的分布律趋于泊松分布 P(lambda)：P(X=k)=e^(-lambda) lambda^k/k!
# 输出用 GBK 安全字符（-> / [OK]）。
# =====================================================================
import math

lam = 3.0
print("=== 二项 B(n, lambda/n) 趋于 泊松(lambda=%.1f) ===" % lam)
print("  泊松分布：P(k)=e^(-%.1f) %.1f^k/k!" % (lam, lam))
for k in range(6):
    print("    k=%d  Poisson=%.5f" % (k, math.exp(-lam) * lam ** k / math.factorial(k)))

print("  随 n 增大，二项分布与泊松的最大偏差（k=0..8）：")
for n in [10, 100, 1000, 10000, 100000]:
    p = lam / n

    def binom(k):
        return math.comb(n, k) * p ** k * (1 - p) ** (n - k)

    diffs = [abs(binom(k) - math.exp(-lam) * lam ** k / math.factorial(k)) for k in range(9)]
    print("    n=%7d  最大偏差=%.6f   P(X=3)二项=%.5f" % (n, max(diffs), binom(3)))
print("-> 结论：n 越大、p 越小、np 固定，二项分布越贴近泊松分布（稀有事件近似）。")
print("[OK] 泊松极限验证完成。")