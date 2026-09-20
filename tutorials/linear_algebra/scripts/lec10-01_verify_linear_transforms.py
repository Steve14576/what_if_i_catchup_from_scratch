# lec10-01_verify_linear_transforms.py
# 第 10 讲验证脚本：线性变换、列=基的像、核与像、换基与相似 B=P^{-1}AP
# 规模纪律：小规模演示（2x2 / 3x4 / 5x5），目标 < 1 秒。

import time
import numpy as np

T0 = time.perf_counter()
rng = np.random.default_rng(10)

print("=== EXP1: 矩阵画廊——每台机器作用在 e1, e2 与一般向量 v=(0.6,0.8) ===")
R90 = np.array([[0., -1.], [1., 0.]])    # 逆时针转 90 度
Ref = np.array([[0., 1.], [1., 0.]])     # 关于直线 y=x 翻折
Proj = np.array([[1., 0.], [0., 0.]])    # 压到 x 轴
Diag = np.array([[2., 0.], [0., 0.5]])   # x 拉长 2 倍, y 压半
Shear = np.array([[1., 1.], [0., 1.]])   # 剪切: x 方向拖着 y 走
v = np.array([0.6, 0.8])
for name, M in [("R90", R90), ("Ref(y=x)", Ref), ("Proj(x轴)", Proj),
                 ("Diag(2,0.5)", Diag), ("Shear", Shear)]:
    e1, e2 = M @ np.array([1., 0.]), M @ np.array([0., 1.])
    print(f"  {name:12s} e1->{np.round(e1,3)}  e2->{np.round(e2,3)}  "
          f"v->{np.round(M @ v, 3)}")
print("  -> 规律: 每台机器的矩阵, 第1列= e1 被送去的位置, 第2列= e2 被送去的位置")
print("     (想知道 v 去哪: v = 0.6*e1+0.8*e2, 所以 v 的去向 = 0.6*(第1列)+0.8*(第2列)")

print()
print("=== EXP2: 旋转矩阵 R(alpha) 用'基像法'现场拼出来, 与教科书公式对照 ===")
a = np.deg2rad(37.0)
e1_img = np.array([np.cos(a), np.sin(a)])    # e1 转 37 度后落点
e2_img = np.array([-np.sin(a), np.cos(a)])   # e2 转 37 度后落点
R_basis = np.column_stack([e1_img, e2_img])  # 基像法: 列=像
R_formula = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
print(f"  alpha=37 度, 基像法拼的矩阵与公式矩阵最大差: {np.abs(R_basis - R_formula).max():.2e}")
w = rng.normal(size=2)
n_before = np.linalg.norm(w)
n_after = np.linalg.norm(R_formula @ w)
ang = np.degrees(np.arctan2(w[1], w[0]))
ang2 = np.degrees(np.arctan2((R_formula @ w)[1], (R_formula @ w)[0]))
print(f"  保长度: |R v| = {n_after:.6f}, |v| = {n_before:.6f}")
print(f"  转角度: {ang:.2f} 度 -> {ang2:.2f} 度, 差取模 360 = {(ang2 - ang) % 360:.2f} (应为 37)")

print()
print("=== EXP3: 线性检验器——两个反例 + 一个正例 ===")
b = np.array([3., 4.])
print(f"  反例1 平移 T(x)=x+(3,4): T(0,0)=(3,4) != 0 -> 线性变换必须把零向量送零向量, 一步否决")
x1 = np.array([1., 0.])
sq = lambda z: z ** 2  # 逐分量平方
print(f"  反例2 平方 T(x)=x^2: T(2*x)={np.round(sq(2 * x1), 3)}, 2*T(x)={2 * sq(x1)} -> 数乘破坏")
u = rng.normal(size=2)
c1, c2 = 2.3, -1.7
A = np.array([[1.5, -0.5], [0.5, 1.5]])
err = np.abs(A @ (c1 * u + c2 * v) - (c1 * (A @ u) + c2 * (A @ v))).max()
print(f"  正例 A=[1.5,-0.5;0.5,1.5]: |A(c1 u+c2 v)-(c1 Au+c2 Av)| = {err:.2e} -> 线性")

print()
print("=== EXP4: 求导是线性变换——D: P3 -> P2 的 3x4 矩阵, 核与像 ===")
D = np.array([[0., 1., 0., 0.],
              [0., 0., 2., 0.],
              [0., 0., 0., 3.]])  # 标准基 {1,t,t^2,t^3} -> {1,t,t^2}
p = np.array([0., 2., 0., 1.])     # p = t^3 + 2t
q = np.array([5., -1., 3., -2.])   # q = 5 - t + 3t^2 - 2t^3
print(f"  p = t^3+2t 坐标 (0,2,0,1): D@[p] = {D @ p}, 应为 p'=3t^2+2 的坐标 (2,0,3)")
print(f"  q = 5-t+3t^2-2t^3: D@[q] = {D @ q}, 应为 q'=-1+6t-6t^2 的坐标 (-1,6,-6)")
err = np.abs(D @ (c1 * p + c2 * q) - (c1 * (D @ p) + c2 * (D @ q))).max()
print(f"  线性抽查: |D(c1 p+c2 q)-(c1 Dp+c2 Dq)| = {err:.2e}")
r = np.linalg.matrix_rank(D)
print(f"  rank(D) = {r} -> 像 = P2 全空间 (满射); dim ker = {4 - r} (常数函数)")
print(f"  核: D@(1,0,0,0) = {D @ np.array([1., 0., 0., 0.])} (常数求导为 0, 核里恰只有常数)")
print(f"  -> rank-nullity: {r} + {4 - r} = 4 = dim P3 [OK] (第 09 讲同一定理的变换版)")

print()
print("=== EXP5: 换基与相似——同一个变换, 两套坐标 ===")
M = np.array([[0., 1.], [1., 0.]])          # 关于 y=x 的反射
P = np.array([[1., 1.], [1., -1.]])         # 列 = 新基 b1=(1,1), b2=(1,-1) 的旧坐标
Pinv = np.linalg.inv(P)
B = Pinv @ M @ P
print("  例1 反射 M=[0,1;1,0], 斜基 b1=(1,1), b2=(1,-1):")
print(f"  B = P^-1 M P =\n{np.round(B, 6)}")
print("  对角! b1 躺在镜面上(不动, 特征方向1), b2 垂直镜面(被翻, 特征方向-1)")
v = rng.normal(size=2)
lhs = Pinv @ (M @ v)     # [M v]_B: 变换结果的 B 坐标
rhs = B @ (Pinv @ v)     # B 作用在 v 的 B 坐标上
print(f"  坐标恒等式 [Mv]_B == B[v]_B: max差 = {np.abs(lhs - rhs).max():.2e}")
print(f"  列=像核对: M b1 = {M @ np.array([1., 1.])} = 1*b1 (B 第1列 (1,0)); "
      f"M b2 = {M @ np.array([1., -1.])} = -b2 (B 第2列 (0,-1))")
S = np.array([[1., 1.], [0., 1.]])          # 剪切
B2 = Pinv @ S @ P
print(f"  例2 剪切 S=[1,1;0,1] 同一组斜基: B2 =\n{np.round(B2, 6)}")
print("  非对角——换基不保证变简单; 要'挑对基'才对角化(第 11/12 讲)")
print(f"  列=像核对: S b1=(2,1) 的 B 坐标 = {np.round(Pinv @ (S @ np.array([1., 1.])), 3)} (=B2 第1列); "
      f"S b2=(0,-1) 的 B 坐标 = {np.round(Pinv @ (S @ np.array([1., -1.])), 3)} (=B2 第2列)")

print()
print("=== EXP6: 相似不变量——det / 迹 / 秩在换基下不变 ===")
for name, X, Y in [("反射 M ~ B", M, B), ("剪切 S ~ B2", S, B2)]:
    print(f"  {name}: det {np.linalg.det(X):+.4f} vs {np.linalg.det(Y):+.4f}; "
          f"tr {np.trace(X):+.4f} vs {np.trace(Y):+.4f}; "
          f"rank {np.linalg.matrix_rank(X)} vs {np.linalg.matrix_rank(Y)}")
A5 = rng.normal(size=(5, 5))
P5 = rng.normal(size=(5, 5)) + 5 * np.eye(5)   # 加 5I 保证良态可逆
B5 = np.linalg.inv(P5) @ A5 @ P5
print(f"  5x5 随机: det A={np.linalg.det(A5):+.6f}, det B={np.linalg.det(B5):+.6f}")
print(f"           tr  A={np.trace(A5):+.6f}, tr  B={np.trace(B5):+.6f}")
print("  (特征值是否也换基不变 -> 第 11 讲用特征方程正式验收)")

print()
print(f"  TOTAL runtime: {time.perf_counter() - T0:.2f}s")
