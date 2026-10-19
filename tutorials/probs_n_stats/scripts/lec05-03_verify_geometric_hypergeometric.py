# =====================================================================
# lec05-03 几何分布的无记忆性 + 超几何 vs 二项（第 05 讲 §5 / §6）
# 规模纪律：30 万次模拟，目标 < 6 秒。
# 几何分布 G(p)：首次成功所需的试验次数，P(X=k)=(1-p)^(k-1) p。
#   无记忆性：P(X>m+n | X>m) = P(X>n)。
# 超几何：N=50 个球（10 红 40 白），不放回抽 n=5 个，X=红球数；
#   分布律 = C(10,k)C(40,5-k)/C(50,5)。对比"放回"的二项 B(5, 0.2)。
# 输出用 GBK 安全字符（-> / [OK]）。
# =====================================================================
import math
import numpy as np

rng = np.random.default_rng(seed=20261018)

# ---- 几何分布与无记忆性 ----
p = 0.2
trials = 300000
X = rng.geometric(p, trials)        # 首次成功的试验次数，取值 >= 1
print("=== 几何分布 G(p=%.1f) ===" % p)
for k in [1, 2, 3, 5]:
    print("    P(X=%d)=%.4f  模拟=%.4f" % (k, (1 - p) ** (k - 1) * p, np.mean(X == k)))

m, n_ = 3, 2
lhs = np.mean(X > m + n_) / np.mean(X > m)      # P(X>m+n | X>m)
rhs = np.mean(X > n_)                            # P(X>n)
print("    无记忆性 P(X>%d | X>%d)=%.4f  vs  P(X>%d)=%.4f" % (m + n_, m, lhs, n_, rhs))
print("    理论: P(X>t)=(1-p)^t；P(X>5)/P(X>3)=(%.1f)^2=%.4f" % (1 - p, (1 - p) ** (m + n_) / (1 - p) ** m))

# ---- 超几何 vs 二项 ----
N, K, ns = 50, 10, 5
print("=== 超几何（N=%d, 红=%d, 抽=%d, 不放回）vs 二项 B(%d, %.1f) ===" % (N, K, ns, ns, K / N))
print("    k   超几何      二项(放回近似)")
for k in range(0, ns + 1):
    hyper = math.comb(K, k) * math.comb(N - K, ns - k) / math.comb(N, ns)
    binom = math.comb(ns, k) * (K / N) ** k * (1 - K / N) ** (ns - k)
    print("    %d   %.5f    %.5f" % (k, hyper, binom))
sim = rng.hypergeometric(K, N - K, ns, trials)
print("  超几何模拟 k=2 频率=%.4f（理论 %.5f）"
      % (np.mean(sim == 2), math.comb(K, 2) * math.comb(N - K, ns - 2) / math.comb(N, ns)))
print("-> 结论：几何分布无记忆（条件概率等于条件后的原概率）；不放回用超几何，放回用二项，"
      "总体很大时超几何接近二项。")
print("[OK] 几何与超几何验证完成。")