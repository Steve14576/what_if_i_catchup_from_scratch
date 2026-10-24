# AA_一览：复变函数与积分变换 概念与公式字典

> 本文件是附录字典，不是速查口令。每条概念写清"是什么"，每条公式写清符号、条件与出处。
> 若只想知道"它叫什么、在哪讲"，看"首次出现"列；若要真正用，回到对应讲次的正文。
> 本文件随讲次增补，不占讲号。

## 一、概念

| 概念（中文） | 英文 / 缩写 | 定义（说清是什么） | 首次出现 | 理解层次 |
|---|---|---|---|---|
| 复数 | complex number | 形如 $a+bi$ 的数，其中 $a,b\in\mathbb R$，$i^2=-1$ | 第 01 讲 | 要会用 |
| 实部 | real part，$\operatorname{Re}z$ | 复数 $z=a+bi$ 中的实数 $a$ | 第 01 讲 | 要会用 |
| 虚部 | imaginary part，$\operatorname{Im}z$ | 复数 $z=a+bi$ 中的实数 $b$（不是 $bi$） | 第 01 讲 | 要会用 |
| 纯虚数 | pure imaginary number | 实部为 $0$ 且虚部不为 $0$ 的复数 $bi$ | 第 01 讲 | 认识层 |
| 复平面 | complex plane | 以实部为横坐标、虚部为纵坐标的平面 | 第 01 讲 | 要建立直觉 |
| 实轴 | real axis | 复平面中虚部为 $0$ 的横轴 | 第 01 讲 | 要会用 |
| 虚轴 | imaginary axis | 复平面中实部为 $0$ 的纵轴 | 第 01 讲 | 要会用 |
| 模 | modulus，$\lvert z\rvert$ | 复数到原点的距离 $\sqrt{a^2+b^2}$，是非负实数 | 第 01 讲 | 要会用 |
| 辐角 | argument，$\arg z$ | 从正实轴转到向量 $z$ 的角度，多值，相差 $2k\pi$ | 第 01 讲 | 要会用 |
| 辐角主值 | principal argument，$\operatorname{Arg}z$ | 辐角中落在 $(-\pi,\pi]$ 内的那一个；本课程固定此区间 | 第 01 讲 | 要会用 |
| 共轭 | conjugate，$\bar z$ | 把虚部变号得到的 $a-bi$，几何上是关于实轴的对称点 | 第 01 讲 | 要会用 |
| 三角形式 | trigonometric form | $z=r(\cos\theta+i\sin\theta)$，用模与辐角表示复数 | 第 01 讲 | 要会用 |
| 指数形式 | exponential form | $z=re^{i\theta}$，由欧拉公式得到的紧凑写法 | 第 01 讲 | 要会用 |
| 欧拉公式 | Euler's formula | $e^{i\theta}=\cos\theta+i\sin\theta$；本课程在第 04 讲给出完整解释 | 第 01 讲 | 要会用 |
| 棣莫弗公式 | de Moivre's formula | $(\cos\theta+i\sin\theta)^n=\cos n\theta+i\sin n\theta$ | 第 01 讲 | 要会用 |
| 邻域 | neighborhood | $U(z_0,\delta)=\{z:\lvert z-z_0\rvert<\delta\}$，开圆盘 | 第 01 讲 | 要知道定义 |
| 去心邻域 | punctured neighborhood | $0<\lvert z-z_0\rvert<\delta$，挖掉圆心的邻域 | 第 01 讲 | 要知道定义 |
| 开集 | open set | 每一点都有一个完全含于自身的邻域的点集 | 第 01 讲 | 要会判断 |
| 闭集 | closed set | 补集为开集的点集，等价于包含自身全部边界点 | 第 01 讲 | 要会判断 |
| 连通 | connected | 任意两点可用完全落在集合内的折线相连 | 第 01 讲 | 要会判断 |
| 区域 | domain | 连通的非空开集 | 第 01 讲 | 要会用 |
| 单连通 | simply connected | 区域内任意简单闭曲线可在区域内连续收缩为一点，即区域没有洞 | 第 01 讲 | 要会判断 |
| 多连通 | multiply connected | 不是单连通的区域，即区域内有洞 | 第 01 讲 | 要会判断 |
| 复变函数 | complex function | 从复平面点集 $D$ 到复平面的单值对应 $w=f(z)$ | 第 02 讲 | 要会用 |
| 映射 | mapping | 把 $z$ 平面上的图形送到 $w$ 平面上的图形；用网格变形观察 | 第 02 讲 | 要建立直觉 |
| 极限（复变函数） | limit | 对任意 $\varepsilon>0$ 存在 $\delta>0$，当 $0<\lvert z-z_0\rvert<\delta$ 时 $\lvert f(z)-A\rvert<\varepsilon$；要求所有路径给出同一值 | 第 02 讲 | 要会用 |
| 路径无关 | path independence | 沿任意路径趋于同一点都得到同一极限值 | 第 02 讲 | 要理解 |
| 连续（复变函数） | continuity | $\lim_{z\to z_0}f(z)=f(z_0)$；等价于实部虚部都在对应点连续 | 第 02 讲 | 要会判断 |
| 分支切割 | branch cut | 多值函数为得到单值分支而人为去掉的射线；$\operatorname{Arg}z$ 的切割线是负实轴 | 第 02 讲提及，第 04 讲定义 | 认识层 |
| 可导（复变函数） | differentiable | 差商 $\dfrac{f(z_0+\Delta z)-f(z_0)}{\Delta z}$ 当 $\Delta z\to0$ 时极限存在，且与方向无关 | 第 03 讲 | 要会用 |
| 导数（复变函数） | derivative，$f'(z_0)$ | 上述差商极限的值 | 第 03 讲 | 要会算 |
| 柯西-黎曼条件 | Cauchy-Riemann equations（C-R） | $u_x=v_y$，$u_y=-v_x$；复可导的必要条件 | 第 03 讲 | 要会推导与使用 |
| 可微（二元函数） | differentiable | 增量可写成线性主部加 $o(\lvert\Delta z\rvert)$，强于偏导存在 | 第 03 讲 | 要能区分 |
| 解析 | analytic / holomorphic | 在 $z_0$ 及其某邻域内处处可导；区域解析指区域内处处可导 | 第 03 讲 | 要会用 |
| 调和函数 | harmonic function | 满足 $u_{xx}+u_{yy}=0$ 的二元函数 | 第 03 讲 | 要会用 |
| 共轭调和函数 | conjugate harmonic function | 与给定调和函数 $u$ 一起构成解析函数 $u+iv$ 的 $v$，相差一个常数 | 第 03 讲 | 要会求 |
| 复指数函数 | complex exponential，$e^z$ | $e^z=e^x(\cos y+i\sin y)$，$z=x+iy$ | 第 04 讲 | 要会用 |
| 复对数（多值） | complex logarithm，$\operatorname{Ln}z$ | $\operatorname{Ln}z=\ln\lvert z\rvert+i(\operatorname{Arg}z+2k\pi)$，$k\in\mathbb Z$ | 第 04 讲 | 要会用 |
| 主值对数 | principal logarithm，$\ln z$ | $\ln z=\ln\lvert z\rvert+i\operatorname{Arg}z$，单值，在负实轴切开后解析 | 第 04 讲 | 要会用 |
| 复幂函数 | complex power，$z^a$ | $z^a=e^{a\operatorname{Ln}z}$，$z\ne0$ | 第 04 讲 | 要会用 |
| 复三角函数 | complex sine/cosine | $\sin z=\dfrac{e^{iz}-e^{-iz}}{2i}$，$\cos z=\dfrac{e^{iz}+e^{-iz}}{2}$ | 第 04 讲 | 要会用 |
| 双曲函数 | hyperbolic functions | $\sinh z=\dfrac{e^z-e^{-z}}{2}$，$\cosh z=\dfrac{e^z+e^{-z}}{2}$ | 第 04 讲 | 要会用 |
| 反三角函数（复） | inverse trigonometric functions | 可用对数表示，如 $\arcsin z=-i\operatorname{Ln}(iz+\sqrt{1-z^2})$，一般多值 | 第 04 讲 | 认识层 |
| 复积分 | complex integral | 沿有向曲线对 $f(\zeta_k)\Delta z_k$ 求和取极限，$\lambda=\max\lvert\Delta z_k\rvert\to0$ | 第 05 讲 | 要会算 |
| 有向曲线 | oriented curve | 指定了起点到终点方向的曲线；反向积分变号 | 第 05 讲 | 要会用 |
| 参数化 | parametrization | 把曲线写成 $z(t)$，$a\le t\le b$，则 $dz=z'(t)dt$ | 第 05 讲 | 要会用 |
| 积分与路径无关 | path independence of integrals | 区域内任意两条同起终点的路径积分相等 | 第 05 讲 | 要会判断 |
| ML 不等式 | ML inequality | $\left\lvert\int_\Gamma f\,dz\right\rvert\le ML$，$M=\max\lvert f\rvert$，$L$ 为弧长 | 第 05 讲 | 要会用 |
| 柯西积分定理 | Cauchy integral theorem | 单连通区域内解析函数的闭路积分为零 | 第 06 讲 | 要会用 |
| 柯西-古萨定理 | Cauchy-Goursat theorem | 去掉 "$f'$ 连续" 这一额外要求的柯西定理版本 | 第 06 讲 | 认识层 |
| 原函数（复） | primitive / antiderivative | 满足 $F'=f$ 的解析函数 $F$ | 第 06 讲 | 要会求 |
| 牛顿-莱布尼茨公式（复） | Newton-Leibniz formula | $\int_a^b f\,dz=F(b)-F(a)$ | 第 06 讲 | 要会用 |
| 闭路变形原理 | deformation of contours | 不越过奇点时，闭曲线可任意变形，积分不变 | 第 06 讲提及，第 07 讲使用 | 要理解 |
| 复合闭路定理 | compound contour theorem | 多连通区域上，沿外边界逆时针的积分等于沿各内边界逆时针积分之和 | 第 07 讲 | 要会用 |
| 原函数存在判据 | criterion for a primitive | 区域 $D$ 内解析的 $f$ 有原函数，当且仅当 $D$ 内任意闭路积分为零 | 第 07 讲 | 要会判断 |
| 柯西积分公式 | Cauchy integral formula | $f(z_0)=\dfrac{1}{2\pi i}\oint_\Gamma\dfrac{f(z)}{z-z_0}dz$，内部值由边界值决定 | 第 08 讲 | 要会用 |
| 平均值定理 | mean value theorem | 解析函数在圆心的值等于圆周上值的平均 | 第 08 讲 | 要会用 |
| 高阶导数公式 | higher derivative formula | $f^{(n)}(z_0)=\dfrac{n!}{2\pi i}\oint_\Gamma\dfrac{f(z)}{(z-z_0)^{n+1}}dz$ | 第 08 讲 | 要会用 |
| 整函数 | entire function | 在整个复平面上解析的函数 | 第 08 讲 | 要知道定义 |
| 刘维尔定理 | Liouville theorem | 有界整函数必为常数 | 第 08 讲 | 要知道陈述与用途 |
| 最大模原理 | maximum modulus principle | 非常数解析函数的模不能在区域内部取到最大值 | 第 08 讲 | 要知道陈述与用途 |
| 部分和 | partial sum | 前 $n$ 项之和 $S_n=a_1+\cdots+a_n$ | 第 09 讲 | 要会用 |
| 级数收敛 | convergence of a series | 部分和数列 $\{S_n\}$ 有有限极限 | 第 09 讲 | 要会判断 |
| 调和级数 | harmonic series | $\sum 1/n$，通项趋于零但发散 | 第 09 讲 | 要知道反例 |
| 几何级数 | geometric series | $\sum r^n$，$\lvert r\rvert<1$ 收敛于 $1/(1-r)$ | 第 09 讲 | 要会用 |
| $p$ 级数 | p-series | $\sum 1/n^p$，$p>1$ 收敛，$p\le1$ 发散 | 第 09 讲 | 要会用 |
| 绝对收敛 | absolute convergence | $\sum\lvert a_n\rvert$ 收敛 | 第 09 讲 | 要会判断 |
| 条件收敛 | conditional convergence | $\sum a_n$ 收敛但 $\sum\lvert a_n\rvert$ 发散 | 第 09 讲 | 要会判断 |
| 幂级数 | power series | $\sum a_n(z-z_0)^n$ | 第 09 讲 | 要会用 |
| 收敛半径 | radius of convergence | 圆内绝对收敛、圆外发散的那个半径 $R$ | 第 09 讲 | 要会求 |
| 收敛圆 | circle of convergence | $\lvert z-z_0\rvert=R$，边界需逐点判断 | 第 09 讲 | 要会用 |
| 阿贝尔定理 | Abel theorem | 一点收敛则更近处绝对收敛；一点发散则更远处发散 | 第 09 讲 | 要理解 |
| 泰勒级数 | Taylor series | $\sum\dfrac{f^{(n)}(z_0)}{n!}(z-z_0)^n$，解析函数的幂级数展开 | 第 10 讲 | 要会用 |
| 泰勒定理 | Taylor theorem | 圆盘内解析的函数等于其泰勒级数，收敛半径至少为圆盘半径 | 第 10 讲 | 要理解 |
| 间接展开 | indirect expansion | 用代换、求导、积分、部分分式从已知展开拼出新展开 | 第 10 讲 | 要会用 |
| 洛朗级数 | Laurent series | $\sum_{n=-\infty}^{\infty}a_n(z-z_0)^n$，允许负幂，在圆环内收敛 | 第 11 讲 | 要会用 |
| 洛朗定理 | Laurent theorem | 圆环内解析的函数可展开为洛朗级数 | 第 11 讲 | 要理解 |
| 主部 | principal part | 洛朗级数的负幂部分 $\sum_{n=1}^{\infty}a_{-n}(z-z_0)^{-n}$ | 第 11 讲 | 要会用 |
| 圆环域 | annulus | $r<\lvert z-z_0\rvert<R$，洛朗级数的展开域 | 第 11 讲 | 要会用 |
| 孤立奇点 | isolated singularity | 去心邻域内解析、本身不解析，且附近无其它奇点 | 第 12 讲 | 要会判断 |
| 可去奇点 | removable singularity | 洛朗主部无负幂项；极限存在有限；补定义后解析 | 第 12 讲 | 要会判断 |
| $m$ 阶极点 | pole of order $m$ | 洛朗主部最高为 $(z-z_0)^{-m}$，极限为 $\infty$ | 第 12 讲 | 要会判断 |
| 本性奇点 | essential singularity | 洛朗主部有无穷多项负幂，极限不存在 | 第 12 讲 | 要会判断 |
| $m$ 阶零点 | zero of order $m$ | $f=(z-z_0)^m g$，$g(z_0)\ne0$ | 第 12 讲 | 要会判断 |
| 无穷远点 | point at infinity | 扩充复平面中的点；用 $t=1/z$ 化为 $t=0$ 研究 | 第 12 讲 | 要会判断 |
| 皮卡大定理 | Picard's great theorem | 本性奇点的去心邻域内取到除至多一个值外的所有复数值 | 第 12 讲 | 认识层 |
| 留数 | residue，$\operatorname{Res}[f,z_0]$ | 洛朗展开中 $(z-z_0)^{-1}$ 项的系数 $a_{-1}$ | 第 13 讲 | 要会算 |
| 留数定理 | residue theorem | 闭路积分等于 $2\pi i$ 乘内部各奇点留数之和 | 第 13 讲 | 要会用 |
| 无穷远留数 | residue at infinity | $\operatorname{Res}[f,\infty]=-a_{-1}$（$\lvert z\rvert>R$ 展开中 $z^{-1}$ 系数取负） | 第 13 讲 | 要会算 |
| 留数总和为零 | sum of residues | 所有有限奇点留数之和加上无穷远留数等于零 | 第 13 讲 | 要会用 |

## 二、公式

| 公式 | 符号含义 | 适用条件 | 出处 |
|---|---|---|---|
| $z=a+bi,\ a,b\in\mathbb R,\ i^2=-1$ | $a$ 实部，$b$ 虚部 | 复数的基本定义 | 第 01 讲 |
| $\lvert z\rvert=\sqrt{a^2+b^2}$ | $z=a+bi$ | 任意复数 | 第 01 讲 |
| $z=r(\cos\theta+i\sin\theta)$ | $r=\lvert z\rvert$，$\theta=\arg z$ | $r\ge0$；$r=0$ 时 $\theta$ 任意 | 第 01 讲 |
| $z=re^{i\theta}$ | $r=\lvert z\rvert$，$\theta\in\arg z$ | 同上 | 第 01 讲 |
| $e^{i\theta}=\cos\theta+i\sin\theta$ | $\theta\in\mathbb R$ | 欧拉公式；完整解释见第 04 讲 | 第 01 讲 |
| $z\bar z=\lvert z\rvert^2$ | $\bar z$ 为共轭 | 任意复数 | 第 01 讲 |
| $\operatorname{Re}z=\dfrac{z+\bar z}{2}$，$\operatorname{Im}z=\dfrac{z-\bar z}{2i}$ | 实部与虚部 | 任意复数 | 第 01 讲 |
| $z_1z_2=r_1r_2e^{i(\theta_1+\theta_2)}$ | $z_k=r_ke^{i\theta_k}$ | 任意复数；几何意义为模相乘、辐角相加 | 第 01 讲 |
| $\dfrac{z_1}{z_2}=\dfrac{r_1}{r_2}e^{i(\theta_1-\theta_2)}$ | 同上 | $z_2\ne0$ | 第 01 讲 |
| $\bigl\lvert\lvert z_1\rvert-\lvert z_2\rvert\bigr\rvert\le\lvert z_1+z_2\rvert\le\lvert z_1\rvert+\lvert z_2\rvert$ | 模 | 任意复数 | 第 01 讲 |
| $\lvert z_1+z_2\rvert^2+\lvert z_1-z_2\rvert^2=2(\lvert z_1\rvert^2+\lvert z_2\rvert^2)$ | 平行四边形恒等式 | 任意复数 | 第 01 讲 |
| $(\cos\theta+i\sin\theta)^n=\cos n\theta+i\sin n\theta$ | 棣莫弗公式 | $n\in\mathbb Z$ | 第 01 讲 |
| $z^n=r^ne^{in\theta}$ | $z=re^{i\theta}$ | $n\in\mathbb Z$ | 第 01 讲 |
| $w_k=r^{1/n}\exp\!\left(i\dfrac{\theta+2k\pi}{n}\right)$ | $w^n=z=re^{i\theta}$ 的 $n$ 个根 | $k=0,1,\dots,n-1$；$r>0$ 或按 $z=0$ 单独处理 | 第 01 讲 |
| $z^2$ 的实虚部：$u=x^2-y^2,\ v=2xy$ | $z=x+iy$ | 恒成立 | 第 02 讲 |
| $\dfrac1z$ 的实虚部：$u=\dfrac{x}{x^2+y^2},\ v=-\dfrac{y}{x^2+y^2}$ | $z=x+iy$ | $z\ne0$ | 第 02 讲 |
| $\lim f=A\iff\lim u=\operatorname{Re}A,\ \lim v=\operatorname{Im}A$ | $f=u+iv$，$A=\alpha+i\beta$ | 二重极限，从平面任意方向趋近 | 第 02 讲 |
| $w=\dfrac1z$ 把 $x=c$ 映成 $\left(u-\dfrac{1}{2c}\right)^2+v^2=\dfrac{1}{4c^2}$ | $c\ne0$，$w=u+iv$ | 直线不过原点 | 第 02 讲 |
| $f'(z_0)=\lim_{\Delta z\to0}\dfrac{f(z_0+\Delta z)-f(z_0)}{\Delta z}$ | $\Delta z$ 为复数 | 极限存在且与方向无关 | 第 03 讲 |
| $u_x=v_y,\quad u_y=-v_x$ | $f=u+iv$ | 复可导的必要条件（C-R） | 第 03 讲 |
| $f'(z_0)=u_x+iv_x=v_y-iu_y$ | 同上 | 在可导点成立 | 第 03 讲 |
| $u,v$ 可微且满足 C-R $\iff f$ 可导 | $f=u+iv$ | 充要条件 | 第 03 讲 |
| $u_r=\dfrac1r v_\theta,\quad v_r=-\dfrac1r u_\theta$ | 极坐标下的 C-R | $r>0$ | 第 03 讲 |
| $f'(z)=e^{-i\theta}(u_r+iv_r)$ | 极坐标导数公式 | $r>0$，可导点 | 第 03 讲 |
| $u_{xx}+u_{yy}=0$ | 拉普拉斯方程 | 调和函数的定义 | 第 03 讲 |
| $v=\int u_x\,dy+\varphi(x)$，再用 $v_x=-u_y$ 定 $\varphi$ | 由实部求虚部 | $u$ 调和、区域单连通 | 第 03 讲 |
| $e^z=e^x(\cos y+i\sin y)$ | $z=x+iy$ | 定义式 | 第 04 讲 |
| $e^{z+2k\pi i}=e^z$ | 周期性 | $k\in\mathbb Z$ | 第 04 讲 |
| $\lvert e^z\rvert=e^{\operatorname{Re}z}$，$\operatorname{Arg}e^z=\operatorname{Im}z+2k\pi$ | 模与辐角 | 任意 $z$ | 第 04 讲 |
| $\operatorname{Ln}z=\ln\lvert z\rvert+i(\operatorname{Arg}z+2k\pi)$ | 多值对数 | $z\ne0$，$k\in\mathbb Z$ | 第 04 讲 |
| $\ln z=\ln\lvert z\rvert+i\operatorname{Arg}z$ | 主值对数 | $z\ne0$，$\operatorname{Arg}\in(-\pi,\pi]$ | 第 04 讲 |
| $(\ln z)'=\dfrac1z$ | 主值对数导数 | $z\in\mathbb C\setminus(-\infty,0]$ | 第 04 讲 |
| $z^a=e^{a\operatorname{Ln}z}$ | 复幂 | $z\ne0$；值的个数取决于 $a$ | 第 04 讲 |
| $i^i=e^{-\pi/2-2k\pi}$ | 复幂例子 | 主值为 $e^{-\pi/2}\approx0.2079$ | 第 04 讲 |
| $\sin z=\dfrac{e^{iz}-e^{-iz}}{2i}$，$\cos z=\dfrac{e^{iz}+e^{-iz}}{2}$ | 复三角定义 | 任意 $z$ | 第 04 讲 |
| $\sin(iy)=i\sinh y$，$\cos(iy)=\cosh y$ | 三角与双曲的关系 | $y\in\mathbb R$ | 第 04 讲 |
| $\int_\Gamma f\,dz=\int_a^b f(z(t))z'(t)\,dt$ | $z=z(t)$ 参数化 | 分段光滑曲线 | 第 05 讲 |
| $\int_\Gamma f\,dz=\int_\Gamma(u\,dx-v\,dy)+i\int_\Gamma(v\,dx+u\,dy)$ | $f=u+iv$ | 任意可积函数 | 第 05 讲 |
| $\oint_{\lvert z-z_0\rvert=r}\dfrac{dz}{(z-z_0)^n}=2\pi i\ (n=1);\ 0\ (n\ne1)$ | $n\in\mathbb Z$ | 逆时针闭路 | 第 05 讲 |
| $\left\lvert\int_\Gamma f\,dz\right\rvert\le ML$ | $M=\max_\Gamma\lvert f\rvert$，$L$ 为弧长 | $f$ 在 $\Gamma$ 上连续 | 第 05 讲 |
| $\oint_\Gamma f\,dz=0$ | 柯西积分定理 | $f$ 在单连通区域 $D$ 内解析，$\Gamma\subset D$ 为闭路 | 第 06 讲 |
| $F(z)=\int_{z_0}^{z}f(\zeta)\,d\zeta$，$F'=f$ | 原函数构造 | 单连通区域内解析 | 第 06 讲 |
| $\int_a^b f\,dz=F(b)-F(a)$ | 牛顿-莱布尼茨公式 | $F'=f$，路径不越过奇点 | 第 06 讲 |
| $\oint_\Gamma f\,dz=\sum_k\oint_{\gamma_k}f\,dz$ | 复合闭路定理 | $\Gamma$ 为外边界，$\gamma_k$ 为各洞边界，均取逆时针 | 第 07 讲 |
| $\oint_\Gamma f\,dz=0\ \forall\Gamma\iff f$ 有原函数 | 原函数判据 | $f$ 在区域内解析 | 第 07 讲 |
| $f(z_0)=\dfrac{1}{2\pi i}\oint_\Gamma\dfrac{f(z)}{z-z_0}dz$ | 柯西积分公式 | $f$ 在 $\Gamma$ 内部及上解析，$z_0$ 在内部，$\Gamma$ 逆时针 | 第 08 讲 |
| $\oint_\Gamma\dfrac{f(z)}{z-z_0}dz=2\pi i f(z_0)$ | 公式的积分用法 | 同上 | 第 08 讲 |
| $f(z_0)=\dfrac{1}{2\pi}\int_0^{2\pi}f(z_0+re^{i\theta})\,d\theta$ | 平均值定理 | 圆盘内解析 | 第 08 讲 |
| $f^{(n)}(z_0)=\dfrac{n!}{2\pi i}\oint_\Gamma\dfrac{f(z)}{(z-z_0)^{n+1}}dz$ | 高阶导数公式 | 同上 | 第 08 讲 |
| $\oint_\Gamma\dfrac{f(z)}{(z-z_0)^{n+1}}dz=\dfrac{2\pi i}{n!}f^{(n)}(z_0)$ | 高阶公式的积分用法 | 同上 | 第 08 讲 |
| $\sum_{n=0}^{\infty}r^n=\dfrac{1}{1-r}$ | 几何级数 | $\lvert r\rvert<1$ | 第 09 讲 |
| $\sum 1/n^p$ 收敛 $\iff p>1$ | $p$ 级数判据 | $p>0$ | 第 09 讲 |
| $\lim\lvert a_{n+1}/a_n\rvert=L\Rightarrow R=1/L$ | 比值法求收敛半径 | $L$ 存在；$L=0$ 时 $R=\infty$ | 第 09 讲 |
| $\lim\sqrt[n]{\lvert a_n\rvert}=L\Rightarrow R=1/L$ | 根值法求收敛半径 | 同上 | 第 09 讲 |
| $f(z)=\sum a_n(z-z_0)^n$ 可逐项求导 | 幂级数性质 | $\lvert z-z_0\rvert<R$ | 第 09 讲 |
| $f(z)=\sum_{n=0}^{\infty}\dfrac{f^{(n)}(z_0)}{n!}(z-z_0)^n$ | 泰勒级数 | $f$ 在 $\lvert z-z_0\rvert<R$ 内解析 | 第 10 讲 |
| $a_n=\dfrac{f^{(n)}(z_0)}{n!}$ | 泰勒系数 | 同上 | 第 10 讲 |
| $e^z=\sum\dfrac{z^n}{n!}$，$R=\infty$ | 指数展开 | 全平面 | 第 10 讲 |
| $\sin z=\sum\dfrac{(-1)^nz^{2n+1}}{(2n+1)!}$，$R=\infty$ | 正弦展开 | 全平面 | 第 10 讲 |
| $\cos z=\sum\dfrac{(-1)^nz^{2n}}{(2n)!}$，$R=\infty$ | 余弦展开 | 全平面 | 第 10 讲 |
| $\dfrac{1}{1-z}=\sum z^n$，$R=1$ | 几何展开 | $\lvert z\rvert<1$ | 第 10 讲 |
| $\ln(1+z)=\sum\dfrac{(-1)^{n-1}z^n}{n}$，$R=1$ | 对数展开 | $\lvert z\rvert<1$ | 第 10 讲 |
| $f(z)=\sum_{n=-\infty}^{\infty}a_n(z-z_0)^n$ | 洛朗级数 | 圆环 $r<\lvert z-z_0\rvert<R$ 内 | 第 11 讲 |
| $a_n=\dfrac{1}{2\pi i}\oint_C\dfrac{f(\zeta)}{(\zeta-z_0)^{n+1}}d\zeta$ | 洛朗系数 | $C$ 为圆环内绕 $z_0$ 的逆时针闭路 | 第 11 讲 |
| $\dfrac{1}{1-z}=-\sum_{n=0}^{\infty}z^{-n-1}$ | 几何级数的圆外展开 | $\lvert z\rvert>1$ | 第 11 讲 |
| $e^{1/z}=\sum\dfrac{1}{n!z^n}$ | 本性奇点例子 | $0<\lvert z\rvert<\infty$ | 第 11 讲 |
| $\dfrac{\sin z}{z}=1-\dfrac{z^2}{3!}+\dfrac{z^4}{5!}-\cdots$ | 可去奇点例子 | 全平面 | 第 11 讲 |
| $m$ 阶零点 $\iff$ 倒数为 $m$ 阶极点 | 零点与极点 | 零点处分子不为零 | 第 12 讲 |
| $z_0$ 可去 $\iff\lim f$ 存在有限 | 可去奇点判据 | $z_0$ 为孤立奇点 | 第 12 讲 |
| $z_0$ 为极点 $\iff\lim f=\infty$ | 极点判据 | 同上 | 第 12 讲 |
| $f$ 在 $\infty$ 的类型 $=$ $f(1/t)$ 在 $t=0$ 的类型 | 无穷远点判据 | $t=1/z$ | 第 12 讲 |
| $\operatorname{Res}[f,z_0]=\lim_{z\to z_0}(z-z_0)f(z)$ | 一阶极点留数 | $z_0$ 为一阶极点 | 第 13 讲 |
| $\operatorname{Res}[P/Q,z_0]=P(z_0)/Q'(z_0)$ | $P/Q$ 公式 | $Q$ 在 $z_0$ 有一阶零点 | 第 13 讲 |
| $\operatorname{Res}[f,z_0]=\dfrac{1}{(m-1)!}\lim\dfrac{d^{m-1}}{dz^{m-1}}[(z-z_0)^mf]$ | $m$ 阶极点留数 | $z_0$ 为 $m$ 阶极点 | 第 13 讲 |
| $\oint_\Gamma f\,dz=2\pi i\sum_k\operatorname{Res}[f,z_k]$ | 留数定理 | $\Gamma$ 逆时针，内部只有有限个孤立奇点 | 第 13 讲 |
| $\operatorname{Res}[f,\infty]=-a_{-1}=-\operatorname{Res}[f(1/t)/t^2,0]$ | 无穷远留数 | $f$ 在 $\lvert z\rvert>R$ 解析 | 第 13 讲 |
| $\sum_k\operatorname{Res}[f,z_k]+\operatorname{Res}[f,\infty]=0$ | 留数总和为零 | 扩充复平面上只有有限个奇点 | 第 13 讲 |

## 三、编号与讲次索引

- 本课程共 28 讲，讲次编号见 `00_导览.md`。
- `AA_` 不占讲号，随讲次增补。
- 跨讲引用只指向已交付讲次；尚未交付的讲次以"第 XX 讲（待交付）"标注。
