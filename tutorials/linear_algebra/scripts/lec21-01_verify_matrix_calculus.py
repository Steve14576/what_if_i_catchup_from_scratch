# lec21-01_verify_matrix_calculus.py
# 第 21 讲验证脚本：数值梯度工具自检、布局约定(grad(x^TAx) 对称/非对称 + 标量对矩阵同形)、
#                   grad||Ax-b||^2=2A^T(Ax-b) 与正规方程闭环、15 讲主例重逢(驻点与 SSE=0.7)、
#                   Hessian=2A^TA 与 2x2 极值判定(AC-B^2 即 Sylvester)、
#                   高斯噪声: 最小二乘=最大似然、参数协方差 sigma^2(A^TA)^-1(蒙特卡洛含覆盖率)、
#                   PCA 双视角(协方差谱分解 vs SVD 右奇异向量)、
#                   梯度下降步数 vs 条件数(含牛顿法一步对照)、反向传播=链式法则(26 参数全对账)
# 规模纪律：小矩阵 + 蒙特卡洛 2 万次(亚秒级), 无大矩阵, 目标 < 3 秒。

import time
import numpy as np

T0 = time.perf_counter()
rng = np.random.default_rng(21)


def numgrad(f, x, h=1e-6):
    """中心差分数值梯度: 逐分量扰动, 解析公式的'验尸官'"""
    x = np.asarray(x, dtype=float)
    g = np.zeros_like(x)
    for i in range(x.size):
        e = np.zeros_like(x)
        e[i] = h
        g[i] = (f(x + e) - f(x - e)) / (2 * h)
    return g


print("=== EXP1: 数值梯度工具自检 ===")
a1 = rng.normal(size=4)
x1 = rng.normal(size=4)
g_a = numgrad(lambda v: a1 @ v, x1)
g_q = numgrad(lambda v: v @ v, x1)
print(f"  f(x)=a^T x: 数值梯度 vs 解析 a 的最大偏差 = {np.abs(g_a - a1).max():.2e}")
print(f"  f(x)=x^T x: 数值梯度 vs 解析 2x 的最大偏差 = {np.abs(g_q - 2 * x1).max():.2e}")
print("  -> 中心差分精度 ~1e-10 级: 给任何解析梯度'验尸'绰绰有余")

print()
print("=== EXP2: 布局约定 -- 梯度与自变量同形 ===")
Ans = rng.normal(size=(3, 3))
Asym = Ans + Ans.T
x2 = rng.normal(size=3)
d1 = numgrad(lambda v: v @ Ans @ v, x2) - (Ans + Ans.T) @ x2
d2 = numgrad(lambda v: v @ Asym @ v, x2) - 2 * Asym @ x2
print(f"  grad(x^T A x), A 非对称: 与 (A+A^T)x 的偏差 = {np.abs(d1).max():.2e}")
print(f"  grad(x^T A x), A 对称:   与 2Ax 的偏差 = {np.abs(d2).max():.2e}")
Wm = rng.normal(size=(3, 2)); xm = rng.normal(size=2); ym = rng.normal(size=3)
Fw = lambda Wf: np.sum((Wf @ xm - ym) ** 2)
gW = np.zeros_like(Wm)
for i in range(3):
    for j in range(2):
        E = np.zeros_like(Wm); E[i, j] = 1e-6
        gW[i, j] = (Fw(Wm + E) - Fw(Wm - E)) / 2e-6
gW_ana = 2 * np.outer(Wm @ xm - ym, xm)
print(f"  标量对矩阵 f(W)=||Wx-y||^2: grad W 形状 {gW.shape} (与 W 同形), 与解析 2(Wx-y)x^T 偏差 = {np.abs(gW - gW_ana).max():.2e}")
print("  -> 梯度结果形状 = 自变量形状: 向量摆成向量、矩阵摆成矩阵(谁变就对谁逐项摆)")

print()
print("=== EXP3: grad||Ax-b||^2 = 2A^T(Ax-b) 与正规方程闭环 ===")
A3 = rng.normal(size=(5, 3))
x3 = rng.normal(size=3)
b3 = rng.normal(size=5)
F3 = lambda v: np.sum((A3 @ v - b3) ** 2)
g_num = numgrad(F3, x3)
g_ana = 2 * A3.T @ (A3 @ x3 - b3)
print(f"  f(x)=||Ax-b||^2, 随机 5x3: 解析 vs 数值最大偏差 = {np.abs(g_num - g_ana).max():.2e}")
x_ls = np.linalg.solve(A3.T @ A3, A3.T @ b3)
x_pinv = np.linalg.lstsq(A3, b3, rcond=None)[0]
print(f"  置零解(正规方程) vs lstsq: 最大偏差 = {np.abs(x_ls - x_pinv).max():.2e}")
print(f"  驻点处 ||grad f|| = {np.linalg.norm(2 * A3.T @ (A3 @ x_ls - b3)):.2e}")
print("  -> 梯度置零 <=> 垂线条件 A^T(b-Ax)=0 <=> 正规方程: 15 讲'第三副面孔'闭环")

print()
print("=== EXP4: 15 讲主例重逢 -- (1.1, 1.1) 恰是碗底 ===")
A15 = np.array([[1., 0.], [1., 1.], [1., 2.], [1., 3.]])
b15 = np.array([1., 2., 4., 4.])
F15 = lambda v: np.sum((A15 @ v - b15) ** 2)
x15 = np.array([1.1, 1.1])
print(f"  SSE(1.1,1.1) = {F15(x15):.4f}   (15 讲手算 0.7)")
print(f"  grad SSE(1.1,1.1) = {np.round(2 * A15.T @ (A15 @ x15 - b15), 12)}   (机器零)")
up_all = True
for _ in range(200):
    d = rng.normal(size=2); d = d / np.linalg.norm(d)
    up_all = up_all and (F15(x15 + 1e-3 * d) > F15(x15))
print(f"  200 个随机方向各走 0.001: SSE 全部上升? {up_all}")
print("  -> 手算的'碗底'就是梯度零点: 任意方向都走高, 200 个随机对抗测试一个不破")

print()
print("=== EXP5: Hessian: grad^2||Ax-b||^2 = 2A^TA 与极值判定 ===")
H_ana = 2 * A3.T @ A3
gradF = lambda v: 2 * A3.T @ (A3 @ v - b3)
H_num = np.zeros((3, 3))
for j in range(3):
    H_num[:, j] = numgrad(lambda v, j=j: gradF(v)[j], x3)
print(f"  数值 Hessian vs 解析 2A^TA: 最大偏差 = {np.abs(H_num - H_ana).max():.2e}")
print(f"  2A^TA 特征值: {np.round(np.linalg.eigvalsh(H_ana), 4)}  (全正: 碗形)")
Hp = np.array([[2., 1.], [1., 3.]])
Hn = np.array([[1., 2.], [2., 1.]])
print(f"  2x2 正定例 H=[[2,1],[1,3]]:  A={Hp[0, 0]:.0f}>0 且 AC-B^2={np.linalg.det(Hp):.0f}>0 -> 极小")
print(f"  2x2 不定例 H=[[1,2],[2,1]]:  AC-B^2={np.linalg.det(Hn):.0f}<0 -> 鞍点")
print("  -> 微积分背的'AC-B^2>0 且 A>0': 就是 16 讲 Sylvester 判据的 2x2 特例")

print()
print("=== EXP6: 高斯噪声 -> 最小二乘 = 最大似然 ===")
A6 = rng.normal(size=(8, 3))
w_true = np.array([1.0, 2.0, -0.5])
sig6 = 0.5
b6 = A6 @ w_true + sig6 * rng.normal(size=8)
w_ols = np.linalg.lstsq(A6, b6, rcond=None)[0]
for s in (0.1, 10.0):
    neglogL = lambda w, s=s: np.sum((b6 - A6 @ w) ** 2) / (2 * s * s) + len(b6) / 2 * np.log(2 * np.pi * s * s)
    g6 = numgrad(neglogL, w_ols)
    print(f"  sigma={s}: -logL 在 OLS 解处梯度范数 = {np.linalg.norm(g6):.2e}")
n6 = len(b6)
p6 = A6.shape[1]
M6 = 500
sig_mle = np.empty(M6)
sig_unb = np.empty(M6)
for m in range(M6):
    bb = A6 @ w_true + sig6 * rng.normal(size=n6)
    ss = np.sum((bb - A6 @ np.linalg.lstsq(A6, bb, rcond=None)[0]) ** 2)
    sig_mle[m] = ss / n6
    sig_unb[m] = ss / (n6 - p6)
print(f"  sigma 也一起优化 (500 轮): 平均 SSE/n   = {sig_mle.mean():.4f}  (理论 (n-p)/n*sigma^2 = {(n6 - p6) / n6 * sig6 ** 2:.4f}, 向下偏差)")
print(f"                             平均 SSE/(n-p) = {sig_unb.mean():.4f}  (理论 sigma^2 = {sig6 ** 2:.4f}, 无偏)")
print("  -> -logL 的梯度 = (A^TAw - A^Tb)/sigma^2: 与 sigma 无关地置零 -> 最大似然解 = 最小二乘解")

print()
print("=== EXP7: 参数不确定度 sigma^2(A^TA)^-1 (蒙特卡洛 2 万次) ===")
A7 = np.array([[1., 0.], [1., 1.], [1., 2.], [1., 3.]])
w7 = np.array([1.5, -0.4])
sig7 = 0.3
N7 = 20000
ATA_inv = np.linalg.inv(A7.T @ A7)
se_thy = sig7 * np.sqrt(np.diag(ATA_inv))
XS = np.zeros((N7, 2))
cover = 0
for i in range(N7):
    bb = A7 @ w7 + sig7 * rng.normal(size=4)
    xi = ATA_inv @ (A7.T @ bb)
    XS[i] = xi
    if np.all(np.abs((xi - w7) / se_thy) < 1.96):
        cover += 1
cov_s = np.cov(XS.T)
cov_t = sig7 ** 2 * ATA_inv
print(f"  样本协方差 / 理论 sigma^2(A^TA)^-1 对角比值: {np.round(np.diag(cov_s) / np.diag(cov_t), 3)}")
print(f"  理论标准误 = {np.round(se_thy, 4)}")
print(f"  联合覆盖率 = {cover / N7:.3f}  (两分量各自 95%, 联合 0.95^2 = {0.95 ** 2:.3f})")
print("  -> 15 讲的'完整统计解释': 系数不确定度公式现场复现, 置信区间 = 估计 ± 1.96 se")

print()
print("=== EXP8: PCA -- 协方差谱分解 = SVD 右奇异向量 (16/17 讲合流) ===")
n8 = 200
z8 = rng.normal(size=n8)
X8 = np.column_stack([z8, 2 * z8 + 0.5 * rng.normal(size=n8)])
Z8 = X8 - X8.mean(axis=0)
C8 = Z8.T @ Z8 / (n8 - 1)
lam, V8 = np.linalg.eigh(C8)
order = np.argsort(lam)[::-1]
lam = lam[order]; V8 = V8[:, order]
U8, S8, Vt8 = np.linalg.svd(Z8, full_matrices=False)
print(f"  协方差特征值 = {np.round(lam, 4)}   占比 = {np.round(lam / lam.sum(), 4)}")
print(f"  第一主方向: eigh 得 {np.round(V8[:, 0], 4)}; SVD 得 {np.round(Vt8[0], 4)}; |点积| = {np.abs(V8[:, 0] @ Vt8[0]):.4f}")
print(f"  sigma^2/(n-1) = {np.round(S8 ** 2 / (n8 - 1), 4)}  vs 特征值 {np.round(lam, 4)}  (对账)")
print(f"  投影方差 Var(Z v1) = {np.var(Z8 @ V8[:, 0], ddof=1):.4f}  = lambda1")
print("  -> 16 讲'谱定理的舞台' + 17 讲'右奇异向量=主方向, sigma^2=方差': 一件事的两副面孔")

print()
print("=== EXP9: 梯度下降步数 vs 条件数 (20 讲重逢) ===")
def gd_iters(H, tol=1e-6):
    alpha = 1.0 / np.linalg.eigvalsh(H).max()   # 步长 = 1/L (L = 最大特征值)
    xg = np.array([1.0, 1.0])
    s0 = np.linalg.norm(xg)
    it = 0
    while np.linalg.norm(xg) > tol * s0:
        xg = xg - alpha * (H @ xg)
        it += 1
    return it
H_well = np.diag([1.0, 10.0])    # kappa = 10
H_ill = np.diag([0.01, 10.0])    # kappa = 1000
i1 = gd_iters(H_well)
i2 = gd_iters(H_ill)
print(f"  kappa=10:   GD 到相对误差 1e-6 用 {i1} 步")
print(f"  kappa=1000: 用 {i2} 步   (比 {i2 / i1:.0f} 倍, 与 kappa 比 100 同量级)")
print(f"  理论: 收敛因子 1-1/kappa, 步数 ~ kappa*ln(1/eps) = [{10 * np.log(1e6):.0f}, {1000 * np.log(1e6):.0f}]")
xg = np.array([1.0, 1.0])
xg_newton = xg - np.linalg.solve(H_ill, H_ill @ xg)   # 牛顿法: x - H^{-1} g
print(f"  同一 kappa=1000 的碗: 牛顿法 1 步到 ||x||={np.linalg.norm(xg_newton):.1e} (二次函数 Hessian 恒定, 一步到位)")
print("  -> 病态的碗连'下山'都慢(GD 被 kappa 卡脖子); 牛顿法用二阶信息一步跳底, 代价是每步要解方程(20 讲分解复用的主场)")

print()
print("=== EXP10: 反向传播 = 链式法则 (26 参数全对账) ===")
x10 = rng.normal(size=3)
W1 = 0.5 * rng.normal(size=(4, 3));  b1 = 0.1 * rng.normal(size=4)
W2 = 0.5 * rng.normal(size=(2, 4));  b2 = 0.1 * rng.normal(size=2)
y10 = rng.normal(size=2)

def loss10(W1, b1, W2, b2):
    h = np.tanh(W1 @ x10 + b1)
    z = W2 @ h + b2
    return 0.5 * np.sum((z - y10) ** 2), h, z

def loss_flat(fv):
    return loss10(fv[0:12].reshape(4, 3), fv[12:16], fv[16:24].reshape(2, 4), fv[24:26])[0]

L0, h, z = loss10(W1, b1, W2, b2)
dz = z - y10                        # 输出层误差
dW2 = np.outer(dz, h); db2 = dz     # 输出层参数梯度
dh = W2.T @ dz                      # 传回隐层的上游梯度(链式的中段)
dpre = dh * (1 - h * h)             # tanh 的局部导数(逐元素, 1-tanh^2)
dW1 = np.outer(dpre, x10); db1 = dpre
g_back = np.concatenate([dW1.ravel(), db1, dW2.ravel(), db2])
flat0 = np.concatenate([W1.ravel(), b1, W2.ravel(), b2])
g_num10 = numgrad(loss_flat, flat0)
print(f"  两层 tanh 网络, 26 个参数: 反向传播 vs 数值梯度最大偏差 = {np.abs(g_back - g_num10).max():.2e}")
print(f"  相对偏差 = {np.abs(g_back - g_num10).max() / np.abs(g_num10).max():.2e}")
print("  -> 反向传播没有魔法: 链式法则 + 每层简单矩阵装配(外积); 深度学习框架的心脏就是这十行")

print()
print(f"[done] total {time.perf_counter() - T0:.2f} s")