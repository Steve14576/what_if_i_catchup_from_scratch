# =====================================================================
# lec06-03 指数分布的无记忆性 + 与几何分布对照（第 06 讲 §3.5 / §3.6）
# 规模纪律：50 万次模拟，目标 < 5 秒。
#   指数：P(X>s+t | X>s) = P(X>t)
#   几何：P(X>m+n | X>m) = P(X>n)
# 两者都是"无记忆"的：指数是连续版几何。
# 输出用 GBK 安全字符（-> / [OK]）。
# =====================================================================
import numpy as np

rng = np.random.default_rng(seed=20261031)
trials = 500000

print("=== 实验 1：指数分布的无记忆性 ===")
lam, s, t = 0.5, 2.0, 3.0
xs = rng.exponential(scale=1 / lam, size=trials)
lhs = np.mean(xs > s + t) / np.mean(xs > s)     # P(X>s+t | X>s)
rhs = np.mean(xs > t)                            # P(X>t)
theory = np.exp(-lam * t)
print("  lambda=%.1f, s=%.1f, t=%.1f" % (lam, s, t))
print("  P(X>%.0f | X>%.0f) = %.4f" % (s + t, s, lhs))
print("  P(X>%.0f)          = %.4f" % (t, rhs))
print("  理论 e^{-lambda t} = %.4f" % theory)
print("  两者之差 = %.4f（在模拟误差内）" % abs(lhs - rhs))

print("=== 实验 2：几何分布的无记忆性（对照） ===")
p = 0.2
m, n_ = 3, 2
Xg = rng.geometric(p, trials)
lhs_g = np.mean(Xg > m + n_) / np.mean(Xg > m)
rhs_g = np.mean(Xg > n_)
print("  p=%.1f, m=%d, n=%d" % (p, m, n_))
print("  P(X>%d | X>%d) = %.4f   P(X>%d) = %.4f   理论 (1-p)^%d = %.4f"
      % (m + n_, m, lhs_g, n_, rhs_g, n_, (1 - p) ** n_))

print("=== 对照表：两种无记忆分布 ===")
print("  几何（离散）：P(X>k)=(1-p)^k，k 为非负整数")
print("  指数（连续）：P(X>t)=e^{-lambda t}，t>=0")
print("  把 (1-p) 看成 e^{-lambda}，两者形状一致：指数是几何的连续版本。")
print("-> 结论：指数与几何都满足'已经等了多久，不影响还要等多久'。")
print("[OK] 无记忆性验证完成。")