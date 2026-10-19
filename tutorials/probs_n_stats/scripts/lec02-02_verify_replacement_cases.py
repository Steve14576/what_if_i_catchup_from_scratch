# =====================================================================
# lec02-02 放回/不放回 x 有序/无序 四种情形的穷举验证（第 02 讲 §4）
# 规模纪律：小规模穷举，目标 < 5 秒。
# 方法：对同一组 (n=4, k=3) 用 itertools 逐情形列出并计数，与公式对照。
#   有序-放回     : n^k                       （product）
#   有序-不放回   : A_n^k = n!/(n-k)!         （permutations）
#   无序-不放回   : C_n^k = n!/(k!(n-k)!)     （combinations）
#   无序-放回     : C_(n+k-1)^k               （combinations_with_replacement）
# 隔板法：把 k 个相同物体分给 n 个人（可空）的方案数 = C_(k+n-1)^k。
# 输出用 GBK 安全字符（-> / [OK]）。
# =====================================================================
import math
from itertools import product, permutations, combinations, combinations_with_replacement

n, k = 4, 3
ordered_replace = len(list(product(range(n), repeat=k)))            # 有放回、有序
ordered_no_replace = len(list(permutations(range(n), k)))           # 无放回、有序
unordered_no_replace = len(list(combinations(range(n), k)))         # 无放回、无序
unordered_replace = len(list(combinations_with_replacement(range(n), k)))  # 有放回、无序

print("=== 实验：n=%d, k=%d 四种情形 ===" % (n, k))
print("  有序-放回   : 穷举=%d  公式 n^k=%d  一致=%s"
      % (ordered_replace, n ** k, ordered_replace == n ** k))
print("  有序-不放回 : 穷举=%d  公式 A_n^k=%d  一致=%s"
      % (ordered_no_replace,
         math.factorial(n) // math.factorial(n - k),
         ordered_no_replace == math.factorial(n) // math.factorial(n - k)))
print("  无序-不放回 : 穷举=%d  公式 C_n^k=%d  一致=%s"
      % (unordered_no_replace,
         math.comb(n, k),
         unordered_no_replace == math.comb(n, k)))
print("  无序-放回   : 穷举=%d  公式 C_(n+k-1)^k=%d  一致=%s"
      % (unordered_replace,
         math.comb(n + k - 1, k),
         unordered_replace == math.comb(n + k - 1, k)))
print("-> 结论：四种情形各有对应公式；把'有序/无序''放回/不放回'两条轴分清楚，就不会套错。")

print("=== 实验：隔板法 ===")
balls, people = 5, 3
slots = math.comb(balls + people - 1, balls)
brute = len(list(combinations_with_replacement(range(people), balls)))
print("  把 %d 个相同球分给 %d 个人（可空）：公式 C(%d,%d)=%d  穷举=%d  一致=%s"
      % (balls, people, balls + people - 1, balls, slots, brute, slots == brute))
print("-> 结论：'分相同物体'的方案数就是'无序-放回'，等于插板法公式 C_(k+n-1)^k。")
print("[OK] 四种情形与隔板法验证完成。")