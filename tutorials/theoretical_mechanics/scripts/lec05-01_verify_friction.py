# L05 摩擦判据数值验证
# 规模纪律: 目标 < 1 秒; 纯 numpy, 无其他依赖
# 验证内容:
#   Exp 1: 斜面自锁两套判据等价 (|F_req| <= f N  <=>  tan(alpha) <= f), 随机 2000 组
#   Exp 2: 例 2 斜拉平衡范围: T 步进数值扫描 vs 解析端点
#   Exp 3: 例 4 先滑先翻: f_s 扫描, 出局方式切换点 vs 解析分界 w/(2d)
# 随机种子固定, print 全 ASCII (GBK 控制台安全)

import numpy as np

rng = np.random.default_rng(42)

print("=" * 64)
print("L05 friction verification")
print("=" * 64)

# ---------------- Exp 1: 斜面自锁判据等价 ----------------
n = 2000
f = rng.uniform(0.05, 1.2, n)          # 摩擦系数
alpha = rng.uniform(0.0, np.pi / 3, n)  # 倾角 0~60 deg
W = 100.0
F_req = W * np.sin(alpha)               # 维持平衡所需摩擦力 (沿斜面)
N = W * np.cos(alpha)
judge_size = F_req <= f * N + 1e-12     # 大小口径
judge_angle = np.tan(alpha) <= f + 1e-12  # 角度口径
mismatch = np.sum(judge_size != judge_angle)
print("[Exp 1] incline self-locking: |F_req| <= f N  vs  tan(alpha) <= f")
print("  random pairs: %d, mismatches: %d  %s" % (n, mismatch,
      "PASS (two criteria equivalent)" if mismatch == 0 else "FAIL"))

# ---------------- Exp 2: 例 2 平衡范围扫描 ----------------
W, fs = 100.0, 0.4
th = np.deg2rad(30.0)
Ts = np.arange(0.0, 60.0 + 0.1, 0.5)
ok = np.zeros_like(Ts, dtype=bool)
for i, T in enumerate(Ts):
    N = W - T * np.sin(th)              # 斜拉: N 随 T 减小
    F = T * np.cos(th)
    ok[i] = (F <= fs * N) and (N >= 0)
T_num = Ts[ok].max()                     # 数值临界 (最后一个平衡格点)
T_ana = fs * W / (np.cos(th) + fs * np.sin(th))
print("[Exp 2] equilibrium range of oblique pull (example 2)")
print("  numeric upper bound (step 0.5 N): T <= %.1f N" % T_num)
print("  analytic: T <= fW/(cos30 + f sin30) = %.3f N" % T_ana)
print("  diff = %.3f N (within step size)  %s" % (abs(T_num - T_ana),
      "PASS" if abs(T_num - T_ana) <= 0.5 else "FAIL"))

# ---------------- Exp 3: 先滑先翻参数扫描 ----------------
W2, w2, d2 = 200.0, 0.5, 0.8
P_tip = W2 * (w2 / 2) / d2               # 翻倒门槛 (常数 62.5 N)
fs_grid = np.arange(0.10, 0.60 + 1e-9, 0.01)
P_slide = fs_grid * W2
events = np.where(P_slide < P_tip, "slide", "tip")
# 找 slide -> tip 的切换点 (最后一个 slide 格点)
idx_switch = None
for i in range(1, len(events)):
    if events[i - 1] == "slide" and events[i] == "tip":
        idx_switch = i - 1
        break
fs_switch = fs_grid[idx_switch]
fs_ana = (w2 / 2) / d2
print("[Exp 3] slide-vs-tip race (example 4, w/(2d) = %.4f)" % fs_ana)
print("  switch at f_s = %.2f (grid 0.01)  [slide below, tip above]" % fs_switch)
print("  analytic boundary f_s = %.4f  %s" % (fs_ana,
      "PASS (diff within grid step)" if abs(fs_switch - fs_ana) <= 0.01 else "FAIL"))

print("=" * 64)
all_pass = (mismatch == 0) and (abs(T_num - T_ana) <= 0.5) and (abs(fs_switch - fs_ana) <= 0.01)
print("OVERALL: %s" % ("ALL PASS" if all_pass else "SOME FAILED"))
