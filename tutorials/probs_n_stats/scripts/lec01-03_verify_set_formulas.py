# =====================================================================
# lec01-03 集合公式枚举验证 + 几何概型区间频率（第 01 讲 §3.3 / §5 / §6）
# 规模纪律：总耗时 < 3 秒。
# 方法：
#   实验 1-2：对 36 个骰子有序结果做穷举，验证加法公式与三事件容斥
#             （公式两边各自枚举计数再对照，不预先写答案）。
#   实验 3：U(0,1) 取点落在 [0.3,0.7] 的频率 vs 理论 0.4（几何概型）。
#   实验 4：宽度 w 的小区间 [0.5-w/2, 0.5+w/2] 频率 vs w，
#           演示"区间越窄频率越低，缩到单点趋于 0"（§6 零概率直觉）。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
# =====================================================================
import numpy as np

rng = np.random.default_rng(seed=20260920)

# 所有 36 个有序结果 (d1, d2)
outcomes = [(a, b) for a in range(1, 7) for b in range(1, 7)]
print("样本容量 |Omega| =", len(outcomes))

# ---- 实验 1：加法公式 P(A∪B) = P(A)+P(B)-P(AB) ----
A = [(a, b) for (a, b) in outcomes if a <= 2]
B = [(a, b) for (a, b) in outcomes if a + b == 7]
AB = [x for x in A if x in B]
AorB = [x for x in outcomes if (x in A) or (x in B)]
lhs = len(AorB) / len(outcomes)
rhs = len(A) / len(outcomes) + len(B) / len(outcomes) - len(AB) / len(outcomes)
print("实验 1：A=第一枚<=2, B=和为7")
print("  |A|=%d |B|=%d |AB|=%d |A∪B|=%d" % (len(A), len(B), len(AB), len(AorB)))
print("  左端 P(A∪B)=%.4f  右端 P(A)+P(B)-P(AB)=%.4f" % (lhs, rhs))
print("  -> 结论：两算法结果相等，加法公式对 36 个结果穷举成立。")

# ---- 实验 2：三事件容斥 P(A∪B∪C) ----
C = [(a, b) for (a, b) in outcomes if (a + b) % 2 == 0]
ABs = len([x for x in A if x in B]) / len(outcomes)
ACs = len([x for x in A if x in C]) / len(outcomes)
BCs = len([x for x in B if x in C]) / len(outcomes)
ABC = len([x for x in outcomes if (x in A) and (x in B) and (x in C)]) / len(outcomes)
AorBorC = len([x for x in outcomes if (x in A) or (x in B) or (x in C)]) / len(outcomes)
pA = len(A) / len(outcomes)
pB = len(B) / len(outcomes)
pC = len(C) / len(outcomes)
rhs3 = pA + pB + pC - ABs - ACs - BCs + ABC
print("实验 2：A=第一枚<=2, B=和为7, C=和为偶数")
print("  P(A)=%.4f P(B)=%.4f P(C)=%.4f" % (pA, pB, pC))
print("  P(AB)=%.4f P(AC)=%.4f P(BC)=%.4f P(ABC)=%.4f" % (ABs, ACs, BCs, ABC))
print("  左端 P(A∪B∪C)=%.4f  右端(三事件容斥)=%.4f" % (AorBorC, rhs3))
print("  -> 结论：三事件容斥对 36 个结果穷举成立，多事件的交集要来回加减。")

# ---- 实验 3：几何概型 [0.3,0.7] ----
N = 100_000
u = rng.uniform(0.0, 1.0, size=N)
f = np.mean((u >= 0.3) & (u <= 0.7))
print("实验 3：U(0,1) 落在 [0.3,0.7]，理论 = 0.4000，模拟频率 = %.4f" % f)
print("  -> 结论：连续均匀取点，区间概率 = 区间长度（面积/长度比），模拟坐实。")

# ---- 实验 4：区间越窄，频率越低（零概率的极限直觉）----
print("实验 4：以 0.5 为中心、宽度 w 的小区间频率")
for w in [0.1, 0.01, 0.001]:
    fw = np.mean((u >= 0.5 - w / 2) & (u <= 0.5 + w / 2))
    print("    w=%.3f  理论=%.4f  模拟=%.4f" % (w, w, fw))
print("  -> 结论：区间宽度缩到 0（单点），理论概率 -> 0；"
      "但该单点被取到 并非'不可能'（§6 零概率 != 不可能，即概率为 0 的事件可以发生）。")
print("[OK] 集合公式与几何概型实验完成。")