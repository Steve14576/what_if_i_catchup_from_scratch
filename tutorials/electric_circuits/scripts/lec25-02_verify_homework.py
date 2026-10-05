# =====================================================================
# lec25-02 作业数字预验证（Q2-Q8）
# 规模纪律：总耗时 < 5 秒（矩阵运算）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import numpy as np

print("=== Q2/Q3/Q4：小电路的 A 与 A*Y*A^T ===")
A = np.array([[1.0, 1.0, 0.0], [0.0, -1.0, 1.0]])
G = np.array([0.2, 0.1, 0.4])
Yn = A @ np.diag(G) @ A.T
print("  A = %s；Yn = A*Yb*A^T = %s" % (A.tolist(), np.array2string(Yn, precision=2)))
print("  手写观察法核对：[[0.3,-0.1],[-0.1,0.5]]，偏差 %.1e" % np.max(np.abs(Yn - np.array([[0.3, -0.1], [-0.1, 0.5]]))))
U = np.array([4.0, 2.0])
print("  KVL 核对：A^T U = %s（支路电压 = 两端电位差）" % np.array2string(A.T @ U, precision=2))

print()
print("=== Q5：图论计数 ===")
b, n = 8, 5
print("  b = %d、n = %d：树支 = %d、连支 = %d、独立回路数 = b-n+1 = %d"
      % (b, n, n - 1, b - n + 1, b - n + 1))

print()
print("=== Q6：RC 充电的状态方程（10 V、R=1k、C=1uF） ===")
R, C = 1000.0, 1e-6
print("  du/dt = -u/(RC) + 10/(RC) = -1000 u + 10000；tau = %.1e s；稳态 u(inf) = %.0f V"
      % (R * C, 10000 / 1000))

print()
print("=== Q7：状态矩阵特征值与稳定判定 ===")
S = np.array([[0.0, -1.0], [-4.0, -2.0]])
ev = np.linalg.eigvals(S)
print("  S = [[0,-1],[-4,-2]] 特征值：%s -> 含正实部 %.4f，不稳定（相当于负阻尼）"
      % (np.array2string(ev, precision=4), max(e.real for e in ev)))

print()
print("=== Q8：三通道综合（A / 手写 Yn / 解） ===")
A8 = np.array([[1.0, 1.0, 0.0, 0.0],
               [0.0, -1.0, 1.0, 0.0],
               [0.0, 0.0, -1.0, 1.0]])
G8 = np.array([0.1, 0.2, 0.1, 0.2])
Yn8 = A8 @ np.diag(G8) @ A8.T
print("  A = %s" % np.array2string(A8, precision=0))
print("  Yn = A*Yb*A^T = %s" % np.array2string(Yn8, precision=3))
IS8 = np.array([1.0, 0.0, 0.0])
U8 = np.linalg.solve(Yn8, IS8)
print("  解：U = %s V" % np.array2string(U8, precision=4))

print()
print("[DONE] lec25-02 完成。")