# =====================================================================
# lec03-03 贝叶斯公式验证：疾病检测与蒙提霍尔（第 03 讲 §5 / §6）
# 规模纪律：精确 + 200 万次模拟，目标 < 8 秒。
# 疾病检测：患病率 0.1%，灵敏度 99%（真病人测阳概率），特异度 99%（健康人测阴概率）。
#   贝叶斯：P(患病|阳性) = P(患病)P(阳性|患病) / [P(患病)P(阳性|患病)+P(健康)P(阳性|健康)]
# 蒙提霍尔：三扇门，一辆车；选手先选一扇，主持人打开一扇没车的门，换门获胜概率 2/3。
# 输出用 GBK 安全字符（-> / [OK]）。
# =====================================================================
import numpy as np

rng = np.random.default_rng(seed=20261018)

print("=== 实验 1：疾病检测（基率谬误） ===")
prev, sens, spec = 0.001, 0.99, 0.99
fpr = 1 - spec
p_pos = prev * sens + (1 - prev) * fpr
p_d_pos = prev * sens / p_pos
print("  患病率=%.4f  灵敏度=%.2f  特异度=%.2f" % (prev, sens, spec))
print("  P(阳性) = %.6f" % p_pos)
print("  P(患病 | 阳性) = %.6f  (约 %.2f%%)" % (p_d_pos, 100 * p_d_pos))

trials = 2_000_000
disease = rng.random(trials) < prev
pos = np.where(disease, rng.random(trials) < sens, rng.random(trials) < fpr)
mc = disease[pos].mean()
print("  模拟 2000000 人：P(患病|阳性) = %.4f" % mc)
print("-> 结论：检测很准（准确率 99%），但阳性者真正患病的只有约 9%——因为基础患病率极低，")
print("   大量健康人的假阳性把阳性池'稀释'了。这就是重视先验（基础率）的贝叶斯推理。")

print("=== 实验 2：蒙提霍尔问题 ===")
trials2 = 200000
car = rng.integers(0, 3, trials2)
pick = rng.integers(0, 3, trials2)
switch_win = (pick != car)      # 换门获胜 <=> 最初就选错
print("  换门获胜概率：理论 2/3 = %.4f   模拟 = %.4f" % (2 / 3, switch_win.mean()))
print("  不换获胜概率：理论 1/3 = %.4f   模拟 = %.4f" % (1 / 3, (~switch_win).mean()))
print("-> 结论：主持人开门提供了信息；换门把胜率从 1/3 提到 2/3，模拟坐实。")
print("[OK] 贝叶斯与蒙提霍尔验证完成。")