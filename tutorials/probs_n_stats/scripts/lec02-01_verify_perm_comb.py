# =====================================================================
# lec02-01 排列数与组合数公式的穷举验证（第 02 讲 §2 / §3）
# 规模纪律：小规模穷举，目标 < 5 秒。
# 方法：用 itertools 直接列出所有排列/组合，数个数，与公式对照。
#   A_n^k = n!/(n-k)!   （选排列：从 n 个里有序取 k 个）
#   C_n^k = n!/(k!(n-k)!)(组合：从 n 个里无序取 k 个)
# 输出用 GBK 安全字符（无 -> 之外的箭头符号，用 -> / [OK]）。
# =====================================================================
import math
from itertools import permutations, combinations


def A(n, k):
    return math.factorial(n) // math.factorial(n - k)


def C(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


print("=== 实验 1：排列数 A_n^k = n!/(n-k)!（有序取） ===")
for (n, k) in [(5, 3), (6, 2), (6, 6)]:
    brute = len(list(permutations(range(n), k)))
    formula = A(n, k)
    print("  n=%d, k=%d: 穷举=%d  公式=%d  一致=%s" % (n, k, brute, formula, brute == formula))
print("-> 结论：A_n^k 公式对多组规模都成立，穷举与公式完全一致。")

print("=== 实验 2：组合数 C_n^k = n!/(k!(n-k)!)（无序取） ===")
for (n, k) in [(5, 2), (6, 3), (10, 4)]:
    brute = len(list(combinations(range(n), k)))
    formula = C(n, k)
    print("  n=%d, k=%d: 穷举=%d  公式=%d  一致=%s" % (n, k, brute, formula, brute == formula))
print("-> 结论：C_n^k 公式对多组规模都成立。")

print("=== 实验 3：对称性 C_n^k = C_n^(n-k) ===")
for (n, k) in [(10, 3), (10, 7), (6, 2), (6, 4)]:
    print("  C(%d,%d)=%d, C(%d,%d)=%d  相等=%s"
          % (n, k, C(n, k), n, n - k, C(n, n - k), C(n, k) == C(n, n - k)))
print("-> 结论：从 n 个里挑 k 个，等价于从 n 个里'留下' n-k 个，两者个数相同。")

print("=== 实验 4：Pascal 递推 C_n^k = C_(n-1)^(k-1) + C_(n-1)^k ===")
for (n, k) in [(6, 3), (8, 5), (10, 4)]:
    lhs = C(n, k)
    rhs = C(n - 1, k - 1) + C(n - 1, k)
    print("  n=%d, k=%d: 直接=%d  递推=%d  一致=%s" % (n, k, lhs, rhs, lhs == rhs))
print("-> 结论：递推关系成立（挑出某个特定元素'选中/不选中'两种情况相加）。")
print("[OK] 排列/组合公式验证完成。")