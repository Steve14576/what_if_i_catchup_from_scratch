# =====================================================================
# lec04-02 离散型的分布函数（CDF）及其性质（第 04 讲 §3）
# 规模纪律：穷举 36 个结果 + 20 万次模拟，目标 < 5 秒。
# X = 两骰点数之和。分布函数 F(x) = P(X <= x)。
# 检查：单调不减、F 左端为 0 右端为 1、区间概率 P(a<X<=b)=F(b)-F(a)。
# 输出用 GBK 安全字符（-> / [OK]）。
# =====================================================================
import numpy as np

rng = np.random.default_rng(seed=20261018)
out = [(a, b) for a in range(1, 7) for b in range(1, 7)]
N = len(out)

pmf = {}
for o in out:
    s = o[0] + o[1]
    pmf[s] = pmf.get(s, 0) + 1
pmf = {k: v / N for k, v in pmf.items()}


def F(x):
    return sum(p for k, p in pmf.items() if k <= x)


print("=== X = 两骰之和 的分布函数 F(x)=P(X<=x) ===")
for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
    print("  F(%2d) = %.4f" % (x, F(x)))

xs = list(range(-1, 15))
vals = [F(x) for x in xs]
mono = all(vals[i] <= vals[i + 1] + 1e-12 for i in range(len(vals) - 1))
print("  单调不减：%s" % mono)
print("  左端（x<=1）F=%.4f ；右端（x>=12）F=%.4f" % (F(1), F(12)))

a, b = 5, 9
print("  区间概率 P(%d<X<=%d) = F(%d)-F(%d) = %.4f-%.4f = %.4f"
      % (a, b, b, a, F(b), F(a), F(b) - F(a)))

trials = 200000
s = rng.integers(1, 7, trials) + rng.integers(1, 7, trials)
print("  模拟 200000 次：P(X<=7) = %.4f（理论 %.4f）；P(5<X<=9) = %.4f（理论 %.4f）"
      % (np.mean(s <= 7), F(7), np.mean((s > a) & (s <= b)), F(b) - F(a)))
print("-> 结论：分布函数由分布律累加得到，单调不减、两端为 0/1，区间概率可用 F 相减。")
print("[OK] 分布函数与性质验证完成。")