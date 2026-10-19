# =====================================================================
# lec03-01 条件概率与乘法公式的穷举/模拟验证（第 03 讲 §1 / §2）
# 规模纪律：穷举 36 个结果 + 20 万次模拟，目标 < 5 秒。
# 两枚六面骰子 36 个有序结果：
#   P(和=7 | 第一枚=3) = P(第一枚=3 且 和=7) / P(第一枚=3)
#   乘法公式 P(AB) = P(A) P(B|A)
# 输出用 GBK 安全字符（-> / [OK]）。
# =====================================================================
import numpy as np

rng = np.random.default_rng(seed=20261018)
out = [(a, b) for a in range(1, 7) for b in range(1, 7)]
N = len(out)


def count(cond):
    return sum(1 for o in out if cond(o))


# ---- 实验 1：条件概率 = 缩小样本空间 ----
pA = count(lambda o: o[0] == 3) / N
pAB = count(lambda o: o[0] == 3 and sum(o) == 7) / N
cond = pAB / pA
sub = [o for o in out if o[0] == 3]
cond_direct = sum(1 for o in sub if sum(o) == 7) / len(sub)
print("=== 实验 1：P(和=7 | 第一枚=3) ===")
print("  P(第一枚=3) = %d/36 = %.4f" % (count(lambda o: o[0] == 3), pA))
print("  P(第一枚=3 且 和=7) = %d/36 = %.4f" % (count(lambda o: o[0] == 3 and sum(o) == 7), pAB))
print("  公式 P(AB)/P(A) = %.4f" % cond)
print("  缩小样本空间直接数 = %.4f  （样本空间 %d -> %d 个结果）" % (cond_direct, N, len(sub)))
trials = 200000
d1 = rng.integers(1, 7, trials)
d2 = rng.integers(1, 7, trials)
mask = d1 == 3
print("  模拟 P(和=7 | 第一枚=3) = %.4f" % np.mean((d1 + d2 == 7)[mask]))
print("-> 结论：除以 P(A) 等价于把样本空间缩到 A 再重新归一；三种算法一致。")

# ---- 实验 2：乘法公式 P(AB) = P(A) P(B|A) ----
lhs = pAB
rhs = pA * cond
print("=== 实验 2：乘法公式 P(AB) = P(A) P(B|A) ===")
print("  P(AB) = %.4f ; P(A) P(B|A) = %.4f ; 一致 = %s" % (lhs, rhs, abs(lhs - rhs) < 1e-12))
print("-> 结论：乘法公式直接由条件概率定义变形得到。")

# ---- 实验 3：独立 vs 不独立（含一个反直觉的真独立） ----
# 组1（显然独立）：第一枚偶  与  第二枚偶
# 组2（反直觉地也独立）：第一枚偶  与  和为偶
#     给定第一枚是偶数后，和的奇偶只由第二枚决定，第二枚为偶的概率仍是 1/2，故两者独立。
# 组3（真正不独立）：第一枚=6  与  和为12
pE1 = count(lambda o: o[0] % 2 == 0) / N
pE2 = count(lambda o: o[1] % 2 == 0) / N
pE12 = count(lambda o: o[0] % 2 == 0 and o[1] % 2 == 0) / N
pC = count(lambda o: sum(o) % 2 == 0) / N
pE1C = count(lambda o: o[0] % 2 == 0 and sum(o) % 2 == 0) / N
pF1 = count(lambda o: o[0] == 6) / N
pF2 = count(lambda o: sum(o) == 12) / N
pF12 = count(lambda o: o[0] == 6 and sum(o) == 12) / N
print("=== 实验 3：独立 vs 不独立 ===")
print("  组1 第一枚偶 与 第二枚偶 : P=%.4f  P(A)P(B)=%.4f  差=%.4f" % (pE12, pE1 * pE2, abs(pE12 - pE1 * pE2)))
print("  组2 第一枚偶 与 和为偶   : P=%.4f  P(A)P(C)=%.4f  差=%.4f" % (pE1C, pE1 * pC, abs(pE1C - pE1 * pC)))
print("  组3 第一枚=6 与 和为12   : P=%.4f  P(E)P(F)=%.4f  差=%.4f" % (pF12, pF1 * pF2, abs(pF12 - pF1 * pF2)))
print("  组3 条件对照: P(和为12)=%.4f, P(和为12|第一枚=6)=%.4f" % (pF2, pF12 / pF1))
print("-> 结论：组1显然独立；组2反直觉地也独立（和的奇偶只由第二枚决定）；组3明显不独立。")
# ---- 实验 4：两两独立 不等于 相互独立 ----
# 掷两枚硬币：A=第一枚正, B=第二枚正, C=恰有一枚正
coins = [(a, b) for a in ('H', 'T') for b in ('H', 'T')]
M = len(coins)
def Pc(cond):
    return sum(1 for c in coins if cond(c)) / M
pA = Pc(lambda c: c[0] == 'H')
pB = Pc(lambda c: c[1] == 'H')
pC = Pc(lambda c: (c[0] == 'H') + (c[1] == 'H') == 1)
pAB = Pc(lambda c: c[0] == 'H' and c[1] == 'H')
pAC = Pc(lambda c: c[0] == 'H' and (c[0] == 'H') + (c[1] == 'H') == 1)
pBC = Pc(lambda c: c[1] == 'H' and (c[0] == 'H') + (c[1] == 'H') == 1)
pABC = Pc(lambda c: c[0] == 'H' and c[1] == 'H' and (c[0] == 'H') + (c[1] == 'H') == 1)
print("=== 实验 4：两两独立 不等于 相互独立 ===")
print("  P(A)=%.2f P(B)=%.2f P(C)=%.2f" % (pA, pB, pC))
print("  P(AB)=%.2f vs P(A)P(B)=%.2f" % (pAB, pA * pB))
print("  P(AC)=%.2f vs P(A)P(C)=%.2f" % (pAC, pA * pC))
print("  P(BC)=%.2f vs P(B)P(C)=%.2f" % (pBC, pB * pC))
print("  P(ABC)=%.2f vs P(A)P(B)P(C)=%.2f" % (pABC, pA * pB * pC))
print("-> 结论：前三个乘积都吻合（两两独立），但三事件同时发生的概率不等于三者之积，故非相互独立。")
print("[OK] 条件概率与乘法公式验证完成。")