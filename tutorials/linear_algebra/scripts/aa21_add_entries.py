# -*- coding: utf-8 -*-
# 一次性脚本: 向 AA_一览.md 追加第 21 讲条目(概念 13 条 + 公式 11 条) + 补 Rayleigh 商(1 条)
# dry-run 默认; --apply 才写盘; 全程字节级(保持 CRLF 行尾); apply 后自动校验
import sys

P = "e:/E_Vault/CC_Formed_Projs2/WHATIFICATCHUPFROMSCRATCH/tutorials/linear_algebra/AA_一览.md"
CRLF = bytes([13, 10])
LF = bytes([10])
CR = bytes([13])

A1_ANCHOR = "第 11 讲 | 要知道+会跑 |"
A2_ANCHOR = r"级降到 $\sqrt{\kappa}$ 级 | 第 20 讲 | 要知道有这回事 |"
A3_ANCHOR = "实测 CG 10 步 vs Jacobi 1633 步 | 第 20 讲 |"

A1_BLOCK = r'''
| Rayleigh 商 | Rayleigh quotient | 把对称矩阵"投影"成一个数的比值 $\vec v^TA\vec v/\vec v^T\vec v$；单位球上最大/最小值 $=\lambda_{\max}/\lambda_{\min}$（16 讲 Rayleigh 区间的来源；幂法用它贴 $\lambda_{\max}$）；PCA 里投影方差 $\mathrm{Var}(Z\vec v)=\vec v^TC\vec v$ 就是它 | 第 11 讲（幂法）；第 16/21 讲复用 | 要会算 |
'''

A2_BLOCK = r'''
| 梯度 | gradient, $\nabla f$ | $f:\mathbb R^n\to\mathbb R$ 的全部一阶偏导排成的向量（$\nabla f_i=\partial f/\partial x_i$），指向最陡上升方向；本课约定"与自变量同形"（谁变就对谁逐项摆），并满足全微分 $df=\langle\nabla f,d\vec x\rangle$ | 第 21 讲 | 要能推导/手算 |
| 全微分 | total differential, $df$ | 一阶变化的线性主部：$df=\sum_i(\partial f/\partial x_i)\,dx_i=\langle\nabla f,d\vec x\rangle$；矩阵变量时 $\langle G,dX\rangle=\operatorname{tr}(G^TdX)$（Frobenius 内积）；"全微分法（识别法）"的根基——把 $df$ 凑成内积，另一个因子就是梯度 | 第 21 讲 | 要能推导/手算 |
| 布局约定 | layout convention | 本课求导的第一条纪律：**梯度的形状 = 自变量的形状**；文献另有分子/分母布局等流派，约定不是真理是纪律、一段推导内不换规矩才有意义；转置错位 bug 九成来自约定混用 | 第 21 讲 | 要会用+防错 |
| Jacobian 矩阵 | Jacobian matrix, $\partial\vec y/\partial\vec x$ | 向量值函数 $\vec y(\vec x)$（$m$ 维出、$n$ 维入）的逐分量梯度表（$m\times n$，第 $i$ 行 $=y_i$ 的梯度）；线性函数 $\vec y=A\vec x$ 的 Jacobian 就是 $A$；链式矩阵版的主角 $\nabla_{\vec x}f=J^T\nabla_{\vec y}f$ | 第 21 讲 | 要能推导/手算 |
| Hessian 矩阵 | Hessian, $\nabla^2f$ | 梯度的 Jacobian——二阶偏导排成的矩阵 $H_{ij}=\partial^2f/(\partial x_j\,\partial x_i)$；二阶偏导连续时对称（住进 16 讲领地）；正定=碗（极小）、负定=倒碗（极大）、不定=鞍；判极值复用 Sylvester 与谱判据；二次函数的 Hessian 恒定 | 第 16 讲（预告）；第 21 讲（正式） | 要能推导/手算 |
| 数值梯度 / 中心差分 | numerical gradient / central difference | 用差分替代求导的独立对账路线：$(\nabla f)_i\approx[f(\vec x+h\vec e_i)-f(\vec x-h\vec e_i)]/(2h)$；截断误差 $\sim h^2$ 与舍入误差 $\sim\mathrm{eps}/h$ 平衡出最优 $h\sim\mathrm{eps}^{1/3}$（本课取 $10^{-6}$、实测精度 $10^{-10}$ 级）；偏差超 $10^{-8}$ 量级必有一方错（"验尸台"） | 第 21 讲 | 要会用 |
| 反向传播 | backpropagation | 链式法则的矩阵版流水线：参数梯度 = 误差信号 $\otimes$ 本层输入（外积装配）、往内层传话 $\delta_{\text{in}}=J_{\text{layer}}^T\delta_{\text{out}}$；框架 autograd 是对它的自动化；自查手段 = 数值梯度对账 | 第 21 讲 | 要能推导/手算 |
| 最大似然估计 | maximum likelihood estimation, MLE | 选出让观测数据"出现概率（似然）最大"的参数；高斯噪声下 $-{\log L}=\mathrm{SSE}/(2\sigma^2)+\frac n2\log(2\pi\sigma^2)$，对 $\vec w$ 的梯度置零与 $\sigma$ 无关 $\Rightarrow$ MLE=OLS（"平方"的统计户口）；$\hat\sigma^2$ 的自由度账：$\mathrm{SSE}/n$ 有偏、$\mathrm{SSE}/(n-p)$ 无偏 | 第 21 讲 | 要能推导/手算 |
| 标准误 / 置信区间 | standard error (se) / confidence interval | 参数估计的波动尺度：$\mathrm{Cov}(\hat{\vec w})=\sigma^2(A^TA)^{-1}$（由协方差传播一步推出）；$\mathrm{se}_j=\sigma\sqrt{[(A^TA)^{-1}]_{jj}}$（与数据同量纲）；95% 区间 $\hat w_j\pm1.96\,\mathrm{se}_j$；语义：信息越多越确定、噪声越大越宽 | 第 21 讲 | 要会用 |
| 协方差矩阵 | covariance matrix, $C$ | 中心化数据的波动汇总表：$C=Z^TZ/(n-1)$（$d\times d$）——对角元 $=$ 各特征自身方差、非对角元 $=$ 成对协方差；对称半正定（$\vec v^TC\vec v=\lVert Z\vec v\rVert^2/(n-1)\ge0$）；PCA 的原料 | 第 15/16 讲（预告）；第 21 讲（正式） | 要会用 |
| 主成分分析 | principal component analysis, PCA | 无监督降维：中心化 $\to$ 协方差 $C\to$ 解 $C\vec v=\lambda\vec v$；主方向 $=$ 特征向量、$\lambda=$ 该方向方差、占比 $=\lambda_i/\sum_j\lambda_j$；工程路线对 $Z$ 直接 SVD（$\sigma_i^2/(n-1)=\lambda_i$，避开 $\kappa^2$）；尺度敏感、$\pm\vec v$ 等价、只抓线性结构 | 第 16/17 讲（预告）；第 21 讲（正式） | 要能推导/手算 |
| 梯度下降 | gradient descent, GD | 最朴素的优化循环 $\vec x_{k+1}=\vec x_k-\alpha\nabla f(\vec x_k)$（$\alpha$ 为步长/学习率）；二次碗上收敛因子 $1-1/\kappa$、步数 $\sim\kappa\ln(1/\varepsilon)$——病态 $\kappa$ 是慢的根源（与 20 讲解方程迭代"同一个 $\kappa$、两种赛道"） | 第 21 讲 | 要建立直觉+会用 |
| 牛顿法 | Newton's method | 用二阶情报的优化：解 $H\vec d=-\nabla f$ 一步跳到局部二次模型的碗底；二次函数一步到位（Hessian 恒定）；每步一次 $O(n^3)$ 分解且要存 $n\times n$ 的 $H$——参数多就破产，故大模型走一阶方法（22 讲路标） | 第 21 讲 | 要知道有这回事 |
'''

A3_BLOCK = r'''
| 全微分 $df=\langle\nabla f,d\vec x\rangle$；矩阵版 $\langle G,dX\rangle=\operatorname{tr}(G^TdX)$ | $d$ 作用时只有变量在动：$d(AXB)=A(dX)B$、$d(X^T)=(dX)^T$、$d(\operatorname{tr}X)=\operatorname{tr}(dX)$ | "识别法"三步：微分 $\to$ 凑内积 $\to$ 读出 $G$；矩阵梯度的主推工具 | 第 21 讲 |
| 三块积木：$\nabla(a^T\vec x)=a$、$\nabla(\vec x^T\vec x)=2\vec x$、$\nabla(\vec x^TA\vec x)=(A+A^T)\vec x$（对称时 $2A\vec x$） | 梯度一律与自变量同形；二次型只感受 $A$ 的对称部分（反对称部分透明） | 组合出本讲全部大公式；EXP1/EXP2 对账（$10^{-10}$ 级） | 第 21 讲 |
| 主公式 $\nabla\lVert A\vec x-\vec b\rVert^2=2A^T(A\vec x-\vec b)$；置零 $\iff A^TA\vec x=A^T\vec b$ | 展开法 = 三块积木的组合；置零即 15 讲正规方程 | 最小二乘的"第三副面孔"：碗底 $=$ 梯度零点；EXP3 偏差 $1.05\times10^{-9}$ | 第 21 讲 |
| 标量对矩阵 $\nabla_W\lVert W\vec x-\vec y\rVert^2=2(W\vec x-\vec y)\vec x^T$ | 结构 = **残差 $\otimes$ 输入**（外积）；形状 $m\times n$ 与 $W$ 同形 | 反传"每层一个外积"的最小版本；EXP2 偏差 $2.86\times10^{-10}$ | 第 21 讲 |
| Hessian：$\nabla^2\lVert A\vec x-\vec b\rVert^2=2A^TA$ | 梯度 $2A^TA\vec x-2A^T\vec b$ 的 Jacobian；常数矩阵（二次函数特征）；列满秩正定 $\Rightarrow$ 唯一碗底 | 微积分 $2\times2$ 判据 = Sylvester 特例；牛顿法一步的根源 | 第 21 讲 |
| 链式 $\nabla_{\vec x}f=J^T\nabla_{\vec y}f$；反传装配 $\partial L/\partial W=\delta\,\text{input}^T$、$\delta_{\text{in}}=J_{\text{layer}}^T\delta_{\text{out}}$ | $J=\partial\vec y/\partial\vec x$；线性层 $J=W$、逐元素激活乘局部斜率（如 $1-\vec h^2$） | 反向传播全部（"传话"从标量损失往回走）；26 参数实测 $3.39\times10^{-11}$ | 第 21 讲 |
| MLE：$\nabla_{\vec w}(-\log L)=(A^TA\vec w-A^T\vec b)/\sigma^2$；$\hat\sigma^2$：$\mathrm{SSE}/n$（有偏）$\to\mathrm{SSE}/(n-p)$（无偏） | 模型 $\vec b=A\vec w+\vec\varepsilon$、$\vec\varepsilon\sim\mathcal N(\vec0,\sigma^2I)$；等价前提是高斯假设（重尾换稳健损失） | 置零与 $\sigma$ 无关 $\Rightarrow$ MLE=OLS；500 轮模拟对账 $0.1531/0.2450$ vs 理论 | 第 21 讲 |
| 参数不确定度：$\mathrm{Cov}(\hat{\vec w})=\sigma^2(A^TA)^{-1}$、$\mathrm{se}_j=\sigma\sqrt{[(A^TA)^{-1}]_{jj}}$、$\hat w_j\pm1.96\,\mathrm{se}_j$ | $\hat{\vec w}=M\vec b$、$M=(A^TA)^{-1}A^T$；协方差传播 $\mathrm{Cov}(M\vec b)=M\,\mathrm{Cov}(\vec b)\,M^T$ | 2 万次蒙特卡洛对账（对角比值 1.006/0.998、联合覆盖率 0.921 vs 理论 0.902） | 第 21 讲 |
| PCA：$C\vec v=\lambda\vec v$；$\mathrm{Var}(Z\vec v)=\vec v^TC\vec v$（Rayleigh 商）；$\sigma_i^2/(n-1)=\lambda_i$（SVD 视角） | $C=Z^TZ/(n-1)$（中心化后）；拉格朗日 $\mathcal L=\vec v^TC\vec v-\lambda(\vec v^T\vec v-1)$ | 主方向 $=$ 特征向量；工程走 SVD($Z$)——避开 $\kappa^2$、免显式造 $C$ | 第 21 讲 |
| 下山 $\vec x_{k+1}=\vec x_k-\alpha\nabla f$；收敛因子 $1-1/\kappa$、步数 $\sim\kappa\ln(1/\varepsilon)$；牛顿法 $H\vec d=-\nabla f$ 一步到碗底 | $\kappa=\lambda_{\max}/\lambda_{\min}$ 取 Hessian 的谱；步长 $\alpha=1/L$（$L=\lambda_{\max}$） | 二次碗；实测 128 vs 13463 步（$\kappa$ 10 vs 1000）；牛顿每步 $O(n^3)$ | 第 21 讲 |
| 中心差分 $(\nabla f)_i\approx[f(\vec x+h\vec e_i)-f(\vec x-h\vec e_i)]/(2h)$ | $h\sim\mathrm{eps}^{1/3}\approx6\times10^{-6}$（当场选取：截断 $h^2$ 与舍入 $\mathrm{eps}/h$ 平衡） | 解析公式的独立对账路线；偏差超 $10^{-8}$ 量级必有一方错 | 第 21 讲 |
'''


def insert_after_line(data, anchor, lines):
    b = anchor.encode("utf-8")
    pos = data.find(b)
    if pos < 0:
        raise SystemExit("anchor not found: " + anchor)
    if data.find(b, pos + 1) >= 0:
        raise SystemExit("anchor not unique: " + anchor)
    enc = [ln.encode("utf-8") for ln in lines]
    nl = data.find(CRLF, pos + len(b))
    if nl < 0:
        # 锚在文件最后一行(无行尾): 追加 CRLF + 新行, 末行同样不带行尾
        return data[:pos + len(b)] + CRLF + CRLF.join(enc)
    # 常规: 在锚所在行行尾 CRLF 之后插入 新行1+CRLF+...+新行n+CRLF
    return data[:nl + 2] + CRLF.join(enc) + CRLF + data[nl + 2:]


def main():
    apply = "--apply" in sys.argv
    a1 = A1_BLOCK.strip().splitlines()
    a2 = A2_BLOCK.strip().splitlines()
    a3 = A3_BLOCK.strip().splitlines()
    print("A1 lines = %d, A2 lines = %d, A3 lines = %d" % (len(a1), len(a2), len(a3)))
    for ln in a1 + a2 + a3:
        if ln.count("@BS@") > 0:
            raise SystemExit("placeholder leak: " + ln[:40])
    data = open(P, "rb").read()
    before = len(data)
    new = data
    for anchor, lines in ((A1_ANCHOR, a1), (A2_ANCHOR, a2), (A3_ANCHOR, a3)):
        new = insert_after_line(new, anchor, lines)
    print("mode = %s" % ("APPLY" if apply else "dry-run"))
    print("size: %d -> %d (delta %d)" % (before, len(new), len(new) - before))
    print("preview A1: " + (a1[0][:60]))
    print("preview A2 first: " + (a2[0][:60]))
    print("preview A2 last : " + (a2[-1][:60]))
    print("preview A3 first: " + (a3[0][:60]))
    print("backslash count in new lines = %d" % sum(ln.count(chr(92)) for ln in a1 + a2 + a3))
    if not apply:
        print("dry-run only, nothing written. use --apply to write.")
        return
    with open(P, "wb") as f:
        f.write(new)
    d2 = open(P, "rb").read()
    crlf2 = d2.count(CRLF)
    lf2 = d2.count(LF)
    cr2 = d2.count(CR)
    print("done. size=%d CRLF=%d bare_LF=%d bare_CR=%d" % (len(d2), crlf2, lf2 - crlf2, cr2 - crlf2))
    for probe in ("| Rayleigh 商 |", "| 梯度 | gradient", "| 牛顿法 | Newton", "| 全微分 $df=", "| 中心差分 $(", "| PCA：$C"):
        print("check %s -> %d" % (probe, d2.count(probe.encode("utf-8"))))


main()