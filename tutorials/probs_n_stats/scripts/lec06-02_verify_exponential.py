# =====================================================================
# lec06-02 指数分布的密度、归一化与分布函数（第 06 讲 §3）
# 规模纪律：数值积分 + 30 万次模拟，目标 < 5 秒。
#   Exp(lambda)：f(x)=lambda e^{-lambda x}（x>0），F(x)=1-e^{-lambda x}
#   尾概率：P(X>t)=e^{-lambda t}
# 输出用 GBK 安全字符（-> / [OK]）。
# =====================================================================
import numpy as np

rng = np.random.default_rng(seed=20261031)


def trapz(y, x):
    return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(x)))


lam = 0.5
print("=== 指数分布 Exp(lambda=%.1f) ===" % lam)
print("  密度 f(x) = lambda e^{-lambda x} = %.1f e^{-%.1f x}（x>0）" % (lam, lam))

x = np.linspace(0, 200, 400001)          # 上界取足够大，尾部可忽略
f = lam * np.exp(-lam * x)
print("  数值积分(0..200) = %.6f（理论 1）" % trapz(f, x))

print("  分布函数与尾概率：")
for t in [1, 2, 5]:
    print("    F(%d)=P(X<=%d)=%.4f   P(X>%d)=%.4f"
          % (t, t, 1 - np.exp(-lam * t), t, np.exp(-lam * t)))

trials = 300000
xs = rng.exponential(scale=1 / lam, size=trials)
print("  模拟 300000 次：")
print("    P(X>2)     = %.4f（理论 %.4f）" % (np.mean(xs > 2), np.exp(-lam * 2)))
print("    P(1<X<3)   = %.4f（理论 %.4f）"
      % (np.mean((xs > 1) & (xs < 3)), np.exp(-lam * 1) - np.exp(-lam * 3)))
print("-> 结论：指数密度的全轴积分为 1；F 与尾概率都由 e^{-lambda x} 给出，模拟贴合。")
print("[OK] 指数分布验证完成。")