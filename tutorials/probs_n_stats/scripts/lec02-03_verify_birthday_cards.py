# =====================================================================
# lec02-03 计数法的两个应用：生日问题与抽牌问题（第 02 讲 §6）
# 规模纪律：精确计算 + 向量化模拟，目标 < 8 秒。
# 方法：
#   生日问题：n 个人中"至少两人同一天生日"。
#             补集（所有人不同）= 365*364*...*(365-n+1)/365^n，概率 = 1 - 它。
#   抽牌问题：从 52 张里抽 5 张，"恰好 2 张 A"。
#             组合计数 = C(4,2)*C(48,3)/C(52,5)。
# 两题都手算（公式）+ 模拟（频率）双向对照。
# 输出用 GBK 安全字符（-> / [OK]，无 ✓ 无 ² 无 →）。
# =====================================================================
import math
import numpy as np

rng = np.random.default_rng(seed=20261018)

print("=== 实验 1：生日问题（n 个人至少两人同生日） ===")
print("  理论：P(至少两人同天) = 1 - (365 x 364 x ... x (365-n+1)) / 365^n")
trials = 20000
for n in [10, 23, 40, 60]:
    p_distinct = 1.0
    for i in range(n):
        p_distinct *= (365 - i) / 365
    p_share = 1 - p_distinct
    bd = rng.integers(0, 365, size=(trials, n))
    s = np.sort(bd, axis=1)
    has_dup = np.any(np.diff(s, axis=1) == 0, axis=1)
    mc = has_dup.mean()
    print("    n=%2d: 理论=%.4f  模拟(%d 组)=%.4f" % (n, p_share, trials, mc))
print("-> 结论：n=23 时理论概率约 0.507（刚过半），补集计数与模拟一致。")

print("=== 实验 2：从 52 张牌抽 5 张，恰好 2 张 A ===")
exact = math.comb(4, 2) * math.comb(48, 3) / math.comb(52, 5)
print("  理论：C(4,2)*C(48,3)/C(52,5) = %d*%d/%d = %.6f"
      % (math.comb(4, 2), math.comb(48, 3), math.comb(52, 5), exact))

trials2 = 100000
# 向量化抽牌：对每行随机排序 52 个位置，取前 5 列作为手牌
order = np.argsort(rng.random((trials2, 52)), axis=1)[:, :5]
rank = np.repeat(np.arange(13), 4)      # 0..12 对应 A,2,...,K；A=0
is_ace = (rank[order] == 0).sum(axis=1)
mc2 = np.mean(is_ace == 2)
print("  模拟 %d 副手牌，频率 = %.4f" % (trials2, mc2))
print("-> 结论：组合计数给准确值，模拟频率在它附近波动，双向印证。")
print("[OK] 生日问题与抽牌问题验证完成。")