# =====================================================================
# lec07-01 正态密度的归一化、参数含义与峰高（第 07 讲 §1 / §2）
# 规模纪律：数值积分，目标 < 3 秒（网格 20 万点，纯 numpy）。
# 方法：
#   1) N(0,1) 密度数值积分 = 1，对照 BB.4 高斯积分 sqrt(2*pi)。
#   2) N(mu,sigma^2) 密度数值积分 = 1（平移缩放不改总面积）。
#   3) 峰高 f(mu) = 1/(sigma*sqrt(2*pi))：sigma 越大峰越低越宽。
# 输出用 GBK 安全字符（无 ✓ 无 ² 无 →，用 [OK] / ^2 / ->）。
# =====================================================================
import math
import numpy as np


def trapz(y, x):
    """手写梯形积分，避免 numpy 版本间 trapz/trapezoid 的差异。"""
    return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(x)))


def normal_pdf(x, mu, sigma):
    return np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))


print("=== 实验 1：N(0,1) 的归一化 ===")
x = np.linspace(-8, 8, 200001)
area = trapz(normal_pdf(x, 0.0, 1.0), x)
print("  数值积分(-8..8) = %.6f" % area)
print("  BB.4 高斯积分: int exp(-x^2/2) dx = sqrt(2*pi) = %.6f" % math.sqrt(2 * math.pi))
print("  1/sqrt(2*pi) = %.6f" % (1 / math.sqrt(2 * math.pi)))
print("  -> 结论：系数 1/sqrt(2*pi) 的唯一作用是把全轴面积调成 1。")

print("=== 实验 2：N(mu, sigma^2) 的归一化（平移 + 缩放） ===")
for mu, sigma in [(2.0, 1.0), (-3.0, 0.5), (0.0, 3.0)]:
    xa = np.linspace(mu - 8 * sigma, mu + 8 * sigma, 200001)
    a = trapz(normal_pdf(xa, mu, sigma), xa)
    print("  N(mu=%.1f, sigma=%.1f): 数值积分 = %.6f  理论 1" % (mu, sigma, a))
print("  -> 结论：mu 只管左右平移，sigma 只管胖瘦，两者都不改变总面积 1。")

print("=== 实验 3：峰高随 sigma 变化 f(mu)=1/(sigma*sqrt(2*pi)) ===")
for sigma in [0.5, 1.0, 2.0, 4.0]:
    peak = 1 / (sigma * math.sqrt(2 * math.pi))
    print("  sigma=%.1f  峰高 f(mu)=%.4f  半高宽约=%.4f（2.355*sigma）"
          % (sigma, peak, 2.355 * sigma))
print("  -> 结论：sigma 越大峰越低、越平；sigma 越小峰越高、越尖。")
