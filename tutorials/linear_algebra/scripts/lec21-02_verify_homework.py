# 第 21 讲作业验证脚本：A1/A2/A3/A4 与 C1/C2/C3 的具体数值对账
# (作业参考答案中的所有读数来源; 10 组实验的主脚本见 lec21-01_verify_matrix_calculus.py)
# 规模纪律：全部小矩阵 + 蒙特卡洛 2000 次, 亚秒级, 目标 < 1 秒。

import time
import numpy as np

T0 = time.perf_counter()
rng = np.random.default_rng(2102)


def numgrad(f, x, h=1e-6):
    """中心差分数值梯度, 支持任意形状输入 (逐元素扰动, 输出与输入同形)"""
    x = np.asarray(x, dtype=float)
    xf = x.ravel()
    g = np.zeros(x.size)
    for i in range(x.size):
        e = np.zeros(x.size)
        e[i] = h
        g[i] = (f((xf + e).reshape(x.shape)) - f((xf - e).reshape(x.shape))) / (2 * h)
    return g.reshape(x.shape)


print("=== A1: 形状三连 ===")
# A1(a) f(x) = c^T x + 0.5 x^T B x, B 对称
n = 4
c = rng.normal(size=n)
B = rng.normal(size=(n, n)); B = B + B.T
f1 = lambda x: c @ x + 0.5 * x @ B @ x
x0 = rng.normal(size=n)
g1 = numgrad(f1, x0)
print(f"  A1(a) grad  vs c+Bx 最大偏差 = {np.abs(g1 - (c + B @ x0)).max():.2e}")
H1 = np.column_stack([numgrad(lambda v: c[j] + (B @ v)[j], x0) for j in range(n)])
print(f"  A1(a) Hessian vs B 最大偏差 = {np.abs(H1 - B).max():.2e}")

# A1(b) f(X) = a^T X b
m, nn = 3, 2
a = rng.normal(size=m); bb = rng.normal(size=nn)
X0 = rng.normal(size=(m, nn))
f2 = lambda X: a @ X @ bb
g2 = numgrad(f2, X0)
print(f"  A1(b) grad vs a b^T 最大偏差 = {np.abs(g2 - np.outer(a, bb)).max():.2e}")

# A1(c) f(W) = ||Wx-y||^2 + lam ||W||_F^2
W0 = rng.normal(size=(m, nn)); xw = rng.normal(size=nn); yw = rng.normal(size=m); lam = 0.7
f3 = lambda W: np.sum((W @ xw - yw) ** 2) + lam * np.sum(W ** 2)
g3 = numgrad(f3, W0)
ana3 = 2 * np.outer(W0 @ xw - yw, xw) + 2 * lam * W0
print(f"  A1(c) grad vs 2(Wx-y)x^T + 2 lam W 最大偏差 = {np.abs(g3 - ana3).max():.2e}")

print()
print("=== A2: 15 讲主例复核 ===")
A15 = np.array([[1., 0.], [1., 1.], [1., 2.], [1., 3.]])
b15 = np.array([1., 2., 4., 4.])
xhat = np.array([1.1, 1.1])
print(f"  SSE(1.1, 1.1) = {np.sum((b15 - A15 @ xhat) ** 2):.4f}")
print(f"  grad SSE(1.1, 1.1) = {2 * A15.T @ (A15 @ xhat - b15)}")

print()
print("=== A3: Hessian 判定两例 ===")
v0 = rng.normal(size=2)
fa = lambda v: v[0] ** 2 + v[0] * v[1] + 3 * v[1] ** 2
Ha = np.column_stack([numgrad(lambda v: numgrad(fa, v)[j], v0) for j in range(2)])
print(f"  A3(a) Hessian 数值 = {Ha.round(4).tolist()}, det = {np.linalg.det(Ha):.2f}")
fb = lambda v: v[0] ** 2 + 4 * v[0] * v[1] + v[1] ** 2
Hb = np.column_stack([numgrad(lambda v: numgrad(fb, v)[j], v0) for j in range(2)])
print(f"  A3(b) Hessian 数值 = {Hb.round(4).tolist()}, det = {np.linalg.det(Hb):.2f}")

print()
print("=== A4: 链式试金石 y=Wx+b, f=0.5||y||^2 ===")
W4 = rng.normal(size=(m, nn)); x4 = rng.normal(size=nn); b4 = rng.normal(size=m)
f4 = lambda W, x, b: 0.5 * np.sum((W @ x + b) ** 2)
y4 = W4 @ x4 + b4
gx = numgrad(lambda x: f4(W4, x, b4), x4)
gW = numgrad(lambda W: f4(W, x4, b4), W4)
gb = numgrad(lambda b: f4(W4, x4, b), b4)
print(f"  A4 grad_x vs W^T y   最大偏差 = {np.abs(gx - W4.T @ y4).max():.2e}")
print(f"  A4 grad_W vs y x^T   最大偏差 = {np.abs(gW - np.outer(y4, x4)).max():.2e}")
print(f"  A4 grad_b vs y       最大偏差 = {np.abs(gb - y4).max():.2e}")

print()
print("=== C1: 单隐层网络 (2-3-1) 反传对账 ===")
rng1 = np.random.default_rng(7)
xc = rng1.normal(size=2)
W1 = rng1.normal(size=(3, 2)); b1c = rng1.normal(size=3)
W2 = rng1.normal(size=(1, 3)); b2c = rng1.normal(size=1)
yc = np.array([1.0])


def Lc(params):
    W1 = params[:6].reshape(3, 2); b1 = params[6:9]
    W2 = params[9:12].reshape(1, 3); b2 = params[12:]
    h = np.tanh(W1 @ xc + b1)
    z = (W2 @ h + b2)[0]
    return 0.5 * (z - yc[0]) ** 2


def grads_c():
    pre = W1 @ xc + b1c; h = np.tanh(pre); z = (W2 @ h + b2c)[0]
    dz = np.array([z - yc[0]])
    dW2 = np.outer(dz, h); db2 = dz
    dh = W2.T @ dz
    dpre = dh * (1 - h * h)
    dW1 = np.outer(dpre, xc); db1 = dpre
    return np.concatenate([dW1.ravel(), db1, dW2.ravel(), db2])


p0 = np.concatenate([W1.ravel(), b1c, W2.ravel(), b2c])
g_back = grads_c()
g_num = numgrad(Lc, p0)
print(f"  13 个参数: 反传 vs 数值梯度最大偏差 = {np.abs(g_back - g_num).max():.2e}")

print()
print("=== C2: PCA 双路线 (n=100) ===")
rng2 = np.random.default_rng(8)
n2 = 100
z2 = rng2.normal(size=n2)
X2 = np.column_stack([z2, -1.5 * z2 + 0.4 * rng2.normal(size=n2)])
Z2 = X2 - X2.mean(axis=0)
C2 = Z2.T @ Z2 / (n2 - 1)
lam2, V2 = np.linalg.eigh(C2)
lam2 = lam2[::-1]; V2 = V2[:, ::-1]
U2, S2, Vt2 = np.linalg.svd(Z2, full_matrices=False)
print(f"  方差占比 = {np.round(lam2 / lam2.sum(), 4)}")
print(f"  第一主方向 |点积| = {np.abs(V2[:, 0] @ Vt2[0]):.4f}")
print(f"  sigma^2/(n-1) vs 特征值 最大偏差 = {np.abs(S2 ** 2 / (n2 - 1) - lam2).max():.2e}")

print()
print("=== C3: 似然覆盖率 (主例 + sigma=0.3, 2000 次) ===")
rng3 = np.random.default_rng(9)
w_true3 = np.array([1.5, -0.4]); sig3 = 0.3
ATA_inv3 = np.linalg.inv(A15.T @ A15)
se3 = sig3 * np.sqrt(np.diag(ATA_inv3))
cover = 0
M3 = 2000
for _ in range(M3):
    bbb = A15 @ w_true3 + sig3 * rng3.normal(size=4)
    wh = ATA_inv3 @ (A15.T @ bbb)
    if np.all(np.abs((wh - w_true3) / se3) < 1.96):
        cover += 1
print(f"  联合覆盖率 = {cover / M3:.3f}  (理论 0.95^2 = {0.95 ** 2:.3f})")

print()
print(f"[done] total {time.perf_counter() - T0:.2f} s")