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
| 约当引理 | Jordan's lemma | $a>0$ 且 $\max_{C_R}\lvert R(z)\rvert\to0$ 时，上半圆上 $\int R(z)e^{iaz}dz\to0$，上界 $\frac{\pi}{a}\max\lvert R\rvert$ | 第 14 讲 | 要会用，证明要看懂 |
| 约当不等式 | Jordan's inequality | $\sin\theta\ge\frac{2\theta}{\pi}$，$0\le\theta\le\frac{\pi}{2}$ | 第 14 讲 | 要知道 |
| 柯西主值 | Cauchy principal value，PV | 在实轴奇点两侧对称挖去长 $\varepsilon$ 的一段再取极限所得的积分 | 第 14 讲 | 要会算 |
| 小半圆引理 | indentation lemma | 一阶极点上方半径 $\varepsilon$ 的顺时针半圆上积分 $\to-\pi i\operatorname{Res}$ | 第 14 讲 | 要会用 |
| 伸缩率 | scale factor | 映射在一点附近对长度的局部放大倍数，等于 $\lvert f'(z_0)\rvert$ | 第 15 讲 | 要会算 |
| 旋转角 | rotation angle | 映射在一点附近对切向的局部旋转量，等于 $\arg f'(z_0)$ | 第 15 讲 | 要会算 |
| 保角映射 | conformal mapping，共形映射 | 在区域内解析且导数处处不为零的映射；保持两条曲线的夹角大小与方向 | 第 15 讲 | 要会用 |
| 反保角 | anti-conformal | 保持夹角大小但反转方向的映射，如 $w=\bar z$；本课程不把它算作保角映射 | 第 15 讲 | 认识层 |
| 分式线性映射 | fractional linear mapping，Möbius transformation | 形如 $w=\frac{az+b}{cz+d}$、$ad-bc\ne0$ 的映射，在扩充复平面上是双射 | 第 15 讲 | 要会用 |
| 保圆性 | circle-preserving property | 分式线性映射把圆或直线映成圆或直线（直线视为过无穷远点的圆） | 第 15 讲 | 要会用 |
| 不动点 | fixed point | 满足 $w(z)=z$ 的点；分式线性映射最多有两个 | 第 15 讲 | 要会算 |
| 保对称性 | symmetry preservation | 关于圆或直线对称的两点，其像关于像圆或像直线对称 | 第 15 讲 | 要会用 |
| 交比 | cross ratio | 四点相对位置的量 $(z_1,z_2,z_3,z_4)=\frac{(z_1-z_2)(z_3-z_4)}{(z_1-z_3)(z_2-z_4)}$，在分式线性映射下不变 | 第 15 讲 | 提高档 |
| 标准域 | standard domain | 区域映射时作为中转的两个标准区域：上半平面与单位圆 | 第 16 讲 | 要会用 |
| 边界对应原理 | boundary correspondence | 单叶解析映射把边界一一映成边界且保持走向时，区域映成目标区域 | 第 16 讲 | 要会用 |
| 儒可夫斯基映射 | Joukowski map | $w=\frac12(z+1/z)$，把圆映成椭圆、偏移圆映成翼型 | 第 16 讲 | 认识层 |
| 傅里叶级数 | Fourier series | 用常数与各次谐波的正弦余弦之和表示周期信号 | 第 17 讲 | 要会用 |
| 正交性 | orthogonality | 三角函数系中不同函数在一个周期上积分为零 | 第 17 讲 | 要会用 |
| 狄利克雷条件 | Dirichlet conditions | 有界、有限个第一类间断点与极值点、其余连续；保证傅里叶级数收敛 | 第 17 讲 | 要会判断 |
| 单边谱 | one-sided spectrum | 只画 $n\ge0$，把负频份量并到正频；幅度 $A_n=2\lvert c_n\rvert$ | 第 17 讲 | 要会画 |
| 双边谱 | two-sided spectrum | 画全部整数 $n$ 的复系数 $c_n$，含负频率 | 第 17 讲 | 要会画 |
| 吉布斯现象 | Gibbs phenomenon | 跳变处部分和过冲约跳变高度的 $9\%$，不随项数消失 | 第 17 讲 | 认识层 |
| 帕塞瓦尔定理（级数版） | Parseval's theorem (series) | 平均功率等于各频率分量功率之和 | 第 17 讲 | 要会用 |
| 基波 | fundamental | 周期信号中角频率为 $2\pi/T$ 的分量（$n=1$） | 第 17 讲 | 要会用 |
| 谐波 | harmonic | 周期信号中角频率为 $2n\pi/T$ 的分量（$n\ge1$） | 第 17 讲 | 要会用 |
| 正弦积分 | sine integral，$\operatorname{Si}$ | $\operatorname{Si}(x)=\int_0^x\frac{\sin t}{t}dt$，无初等闭式 | 第 17 讲 | 认识层 |
| 傅里叶变换 | Fourier transform，$\mathcal F$ | 把时间信号变为频率密度 $F(\omega)=\int f e^{-i\omega t}dt$ | 第 18 讲 | 要会用 |
| 频谱密度 | spectral density | 非周期信号的 $F(\omega)$，量纲为幅度乘时间 | 第 18 讲 | 要理解 |
| 绝对可积 | absolutely integrable | $\int\lvert f\rvert dt<\infty$，傅里叶变换存在的充分条件 | 第 18 讲 | 要会判断 |
| sinc 函数 | sinc function | $\operatorname{sinc}x=\sin x/x$（本课程定义） | 第 18 讲 | 要会用 |
| 截止角频率 | cut-off angular frequency | 一阶低通幅度降到 $1/\sqrt2$ 处的 $\omega=a$ | 第 18 讲 | 要理解 |
| 分贝 | decibel，dB | 幅度比 $R$ 的 $20\log_{10}R$；$1/\sqrt2$ 对应 $-3.01\,\mathrm{dB}$ | 第 18 讲 | 要会用 |
| 卷积 | convolution，$f*g$ | 翻转—平移—相乘—积分的运算 $(f*g)(t)=\int f(\tau)g(t-\tau)d\tau$；频域里是乘法 | 第 19 讲 | 要会算 |
| 调制 | modulation | 信号乘正弦（载波）以搬移频谱的操作；乘余弦为最简单的幅度调制 | 第 19 讲 | 要会用 |
| 对偶（对称性） | duality | 把 $F$ 当时间信号，其变换为 $2\pi f(-\omega)$；与奇偶对称不是一回事 | 第 19 讲 | 要会用 |
| 三角脉冲 | triangular pulse，$\Lambda$ | $\Lambda(t)=1-\lvert t\rvert$（$\lvert t\rvert<1$）；宽 $1$ 矩形的自卷积 | 第 19 讲 | 要会用 |
| 零均值 | zero mean | $F(0)=\int f=0$，正负面积相消；积分性质无 $\delta$ 项的条件 | 第 19 讲 | 要会判断 |
| 因果信号 | causal signal | $t<0$ 时为零的信号；两个因果信号的卷积仍因果 | 第 19 讲 | 要会判断 |
| 权函数（系统响应核） | weighting kernel / impulse response | 系统对"距今 $t-\tau$ 的一份输入"的响应 $h(t-\tau)$；卷积 $y=\int x(\tau)h(t-\tau)d\tau$ 即加权延迟叠加 | 第 19 讲 | 要会用 |
| 相关 | correlation | 不翻转的重叠积分；本课程不用 | 第 19 讲 | 认识层 |
| 帕塞瓦尔定理（变换版） | Parseval's theorem (transform) | 总能量等于频谱能量密度积分除 $2\pi$ | 第 19 讲 | 要会用 |
| $\delta$ 函数 | Dirac delta，$\delta(t)$ | 单位面积矩形 $\tau\to0$ 的极限对象；用 $\int\delta(t)\varphi(t)dt=\varphi(0)$ 定义，不是逐点函数 | 第 20 讲 | 要会用 |
| 筛选性质 | sifting property | $\int\delta(t-t_0)\varphi(t)dt=\varphi(t_0)$，用 $\delta$ 在 $t_0$ 处“筛出”函数值 | 第 20 讲 | 要会用 |
| 广义意义 | generalized sense | 等式只在“乘连续函数再积分”后成立；$\delta$ 与冲激串的运算均在此意义下 | 第 20 讲 | 要知道边界 |
| 冲激串 | impulse train | 等间隔冲激之和 $\sum\delta(t-nT)$；周期信号的频谱就是冲激串 | 第 20 讲 | 要会用 |
| 冲激强度（面积） | impulse strength | 冲激在积分中贡献的面积；周期信号第 $n$ 根为 $2\pi c_n$ | 第 20 讲 | 要会用 |
| 抽样角频率 | sampling angular frequency，$\omega_s$ | $\omega_s=2\pi/T_s$；抽样后频谱以 $\omega_s$ 为周期复制 | 第 20 讲 | 要会用 |
| Nyquist 条件 | Nyquist condition | 带限 $\omega_m$ 的信号可恢复的充分条件 $\omega_s>2\omega_m$（严格大于） | 第 20 讲 | 要会判断 |
| 混叠（折叠频率） | aliasing / folding frequency | 副本重叠时高频折成低频；折叠频率取 $\lvert f_0-kf_s\rvert$ 中最小且 $\le f_s/2$ | 第 20 讲 | 要会算 |
| 理想低通 | ideal low-pass filter | 频域矩形 $H=T_s\operatorname{rect}(\omega/(2\omega_c))$；时域核为 sinc，非因果不可实现 | 第 20 讲 | 认识层 |
| 插值核 | interpolation kernel | $h(t)=\operatorname{sinc}(\omega_c t)$，在采样点 $h(nT_s)=0\ (n\ne0)$、$h(0)=1$ | 第 20 讲 | 要会用 |

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
| $\int_{-\infty}^{\infty}\frac{P}{Q}dx=2\pi i\sum_{\operatorname{Im}z_k>0}\operatorname{Res}$ | 类型一 | $\deg Q\ge\deg P+2$，$Q$ 无实零点 | 第 14 讲 |
| $z=e^{i\theta}$：$\cos\theta=\frac{z+z^{-1}}{2}$，$\sin\theta=\frac{z-z^{-1}}{2i}$，$d\theta=\frac{dz}{iz}$ | 类型二代换 | 被积函数在单位圆上无奇点；只算圆内留数 | 第 14 讲 |
| $\int_{-\infty}^{\infty}R(x)e^{iax}dx=2\pi i\sum_{\operatorname{Im}z_k>0}\operatorname{Res}[Re^{iaz}]$ | 类型三 | $a>0$，$R\to0$，实轴无奇点；$a<0$ 改用下半平面 | 第 14 讲 |
| $\left\lvert\int_{C_R}Re^{iaz}dz\right\rvert\le\frac{\pi}{a}\max_{C_R}\lvert R\rvert$ | 约当引理 | $a>0$，$C_R$ 为上半圆 | 第 14 讲 |
| $\operatorname{PV}\int f\,dx=2\pi i\sum_{\text{上}}\operatorname{Res}+\pi i\sum_{\text{实轴}}\operatorname{Res}$ | 主值公式 | 实轴上只有一阶极点，大半圆积分 $\to0$ | 第 14 讲 |
| $\int_{-\infty}^{\infty}\frac{\sin x}{x}dx=\pi$ | 主值经典例 | — | 第 14 讲 |
| $\lvert\Delta w\rvert\approx\lvert f'(z_0)\rvert\lvert\Delta z\rvert$，$\arg\Delta w\approx\arg f'(z_0)+\arg\Delta z$ | $\Delta w=f(z_0+\Delta z)-f(z_0)$；$\lvert f'\rvert$ 是伸缩率，$\arg f'$ 是旋转角 | $\Delta z\to0$，$f'(z_0)\ne0$ | 第 15 讲 |
| $w=\frac{az+b}{cz+d}$，$ad-bc\ne0$ | 分式线性映射的系数 | 扩充复平面上的双射 | 第 15 讲 |
| $w=\frac ac+\frac{bc-ad}{c^2}\cdot\frac{1}{z+d/c}$ | 四步分解：平移 → 反演 → 旋转伸缩 → 平移 | $c\ne0$ | 第 15 讲 |
| $cz^2+(d-a)z-b=0$ | 不动点方程 | $w=(az+b)/(cz+d)$，最多两个解（含 $\infty$） | 第 15 讲 |
| $(z_1,z_2,z_3,z_4)=\frac{(z_1-z_2)(z_3-z_4)}{(z_1-z_3)(z_2-z_4)}$ | 交比定义 | 分式线性映射下不变 | 第 15 讲 |
| $(z,z_2,\infty,z_4)=\frac{z-z_2}{z_4-z_2}$，$(z,\infty,z_3,z_4)=\frac{z_3-z_4}{z-z_3}$ | 含 $\infty$ 的交比规则 | 四点中有一个为 $\infty$ | 第 15 讲 |
| $w=\frac{1+iz}{1-iz}$ | 把 $0,1,\infty$ 映到 $1,i,-1$ 的映射 | 由三对点唯一确定 | 第 15 讲 |
| $w=e^{i\theta}\frac{z-z_0}{z-\bar z_0}$ | 上半平面 → 单位圆，$z_0\mapsto0$ | $\operatorname{Im}z_0>0$ | 第 16 讲 |
| $z=\frac{w\bar z_0-z_0}{w-1}$ | 单位圆 → 上半平面（逆映射） | 由标准映射解出 | 第 16 讲 |
| $w=z^{\pi/\theta_0}$ | 顶角 $\theta_0$ 的角形域 → 上半平面 | 取 $\arg z\in(0,\theta_0)$ 的分支 | 第 16 讲 |
| $w=e^{\pi z/a}$ | 宽 $a$ 的水平带形 → 上半平面 | $a>0$ | 第 16 讲 |
| $w=\frac12(z+1/z)$，$a=\frac12(r+1/r)$，$b=\frac12\lvert r-1/r\rvert$ | 儒可夫斯基：半径 $r$ 的圆 → 半轴 $a,b$ 的椭圆 | 认识层；$r=1$ 退化为线段 | 第 16 讲 |
| $a_n=\frac2T\int_0^Tf\cos n\omega t\,dt$，$b_n=\frac2T\int_0^Tf\sin n\omega t\,dt$ | 三角系数 | $n\ge1$；$a_0=\frac2T\int_0^Tf\,dt$ | 第 17 讲 |
| $c_n=\frac1T\int_0^Tf(t)e^{-in\omega t}dt$ | 复指数系数 | 任意整数 $n$ | 第 17 讲 |
| $c_0=\frac{a_0}{2}$，$c_n=\frac{a_n-ib_n}{2}$，$c_{-n}=\frac{a_n+ib_n}{2}$ | 两种系数换算 | $n>0$ | 第 17 讲 |
| $A_n=2\lvert c_n\rvert=\sqrt{a_n^2+b_n^2}$，$\varphi_n=\arg c_n$ | 单边幅度与相位 | $n\ge1$；$A_0=a_0$ | 第 17 讲 |
| $\frac1T\int_0^T\lvert f\rvert^2dt=\sum\lvert c_n\rvert^2=\frac{A_0^2}{4}+\sum\frac{A_n^2}{2}$ | 帕塞瓦尔（级数版） | $f$ 在周期上平方可积 | 第 17 讲 |
| $\sum_{k=0}^{\infty}\frac1{(2k+1)^2}=\frac{\pi^2}{8}$ | 方波功率推出的级数 | — | 第 17 讲 |
| $F(\omega)=\int_{-\infty}^{\infty}f e^{-i\omega t}dt$，$f=\frac1{2\pi}\int F e^{i\omega t}d\omega$ | 正逆变换（$2\pi$ 在逆变换前） | 绝对可积 | 第 18 讲 |
| $F(\omega)=\tau\operatorname{sinc}\frac{\omega\tau}{2}$ | 矩形脉冲的变换 | $F(0)=\tau$，零点 $2k\pi/\tau$，主瓣 $4\pi/\tau$ | 第 18 讲 |
| $F(\omega)=\frac1{a+i\omega}$ | $e^{-at}u(t)$ 的变换 | $a>0$ | 第 18 讲 |
| $F(-\omega)=\overline{F(\omega)}$ | 实信号共轭对称 | $f$ 实 | 第 18 讲 |
| $f(t-t_0)\leftrightarrow e^{-i\omega t_0}F(\omega)$ | 时移 | 只改相位不改幅度；因子与积分变量无关 | 第 19 讲 |
| $e^{i\omega_0t}f(t)\leftrightarrow F(\omega-\omega_0)$ | 频移（调制） | 频谱整体搬移 | 第 19 讲 |
| $f(at)\leftrightarrow\frac1{\lvert a\rvert}F(\omega/a)$ | 尺度 | $a\ne0$；$a<0$ 时微分负号与限对调负号相消 | 第 19 讲 |
| $F(t)\leftrightarrow2\pi f(-\omega)$ | 对偶 | 逆变换成立；$2\pi$ 随口径 | 第 19 讲 |
| $f'\leftrightarrow i\omega F$ | 时域微分 | $f(\pm\infty)=0$ 且 $f'$ 绝对可积 | 第 19 讲 |
| $\int_{-\infty}^t f\leftrightarrow\frac{F}{i\omega}+\pi F(0)\delta(\omega)$ | 时域积分 | $F(0)=0$ 时 $\delta$ 项消失 | 第 19 讲 |
| $tf\leftrightarrow iF'(\omega)$ | 频域微分 | $tf$ 绝对可积 | 第 19 讲 |
| $\mathcal F[f*g]=F(\omega)G(\omega)$ | 卷积定理 | $f,g$ 绝对可积 | 第 19 讲 |
| $\mathcal F[fg]=\frac1{2\pi}(F*G)(\omega)$ | 对偶式 | 系数跟"频域卷积"走 | 第 19 讲 |
| $\int\lvert f\rvert^2=\frac1{2\pi}\int\lvert F\rvert^2$ | 帕塞瓦尔（变换版） | 能量有限 | 第 19 讲 |
| $\operatorname{sinc}t\leftrightarrow\pi\operatorname{rect}(\omega/2)$ | 对偶算例 | 广义积分意义；$\lvert\omega\rvert<1$ 为 $\pi$ | 第 19 讲 |
| $\Lambda(t)\leftrightarrow\operatorname{sinc}^2(\omega/2)$ | 三角脉冲 | $\Lambda=q*q$，$q$ 宽 $1$ | 第 19 讲 |
| $(\Lambda*q)(t)$：$\lvert t\rvert\le\tfrac12$ 时 $\tfrac34-t^2$；$\tfrac12\le\lvert t\rvert\le\tfrac32$ 时 $\tfrac12(\tfrac32-\lvert t\rvert)^2$；其余 $0$ $\leftrightarrow\operatorname{sinc}^3(\omega/2)$ | 三重卷积 | 分段二次、$C^1$；每卷一次光滑一档、衰减快一档 | 第 19 讲 |
| $\int_0^t f\leftrightarrow\frac{F}{i\omega}+\pi F(0)\delta-2\pi g(0)\delta$ | 因果积分 | $g_0=g-g(0)$；因果信号时 $g_0=g$；拉普拉斯 $F(s)/s$ 为其 $s$ 域版 | 第 19 讲 |
| $\delta(at)=\delta(t)/\lvert a\rvert$ | $\delta$ 的尺度 | $a\ne0$；换元时限与 $dt$ 符号相消 | 第 20 讲 |
| $f*\delta=f$ | 卷积单位元 | $f$ 在 $t$ 处连续 | 第 20 讲 |
| $\mathcal F[\delta]=1$ | $\delta$ 的频谱 | 筛选，$\varphi=e^{-i\omega t}$ | 第 20 讲 |
| $\mathcal F[1]=2\pi\delta(\omega)$ | 常数的频谱 | 广义意义；面积 $2\pi$ | 第 20 讲 |
| $\cos\omega_0t\leftrightarrow\pi[\delta(\omega-\omega_0)+\delta(\omega+\omega_0)]$ | 余弦频谱 | 实偶→实偶冲激，各面积 $\pi$ | 第 20 讲 |
| $\sin\omega_0t\leftrightarrow-i\pi[\delta(\omega-\omega_0)-\delta(\omega+\omega_0)]$ | 正弦频谱 | 实奇→纯虚奇冲激 | 第 20 讲 |
| $\mathcal F[\sum c_ne^{in\omega_0t}]=2\pi\sum c_n\delta(\omega-n\omega_0)$ | 周期信号频谱 | 广义意义；强度 $2\pi c_n$ | 第 20 讲 |
| $X_s(\omega)=\frac1{T_s}\sum_nX(\omega-n\omega_s)$ | 抽样频谱 | $\omega_s=2\pi/T_s$；带限且 $\omega_s>2\omega_m$ 可恢复 | 第 20 讲 |
| $x(t)=\sum_nx(nT_s)\operatorname{sinc}(\omega_c(t-nT_s))$ | 理想重建 | $\omega_c=\pi/T_s$；理想低通不可实现 | 第 20 讲 |
| $te^{-at}u(t)\leftrightarrow\frac1{(a+i\omega)^2}$ | 频域微分算例 | $a>0$ | 第 19 讲 |
| $\frac1{1+t^2}\leftrightarrow\pi e^{-\lvert\omega\rvert}$ | 对偶算例 | 与第 14 讲留数结果一致 | 第 19 讲 |
| $\int\operatorname{sinc}^2x\,dx=\pi$，$\int\operatorname{sinc}^4x\,dx=\frac{2\pi}{3}$ | 两个 sinc 积分 | 由帕塞瓦尔推出 | 第 19 讲 |

## 三、编号与讲次索引

- 本课程共 28 讲，讲次编号见 `00_导览.md`。
- `AA_` 不占讲号，随讲次增补。
- 跨讲引用只指向已交付讲次；尚未交付的讲次以"第 XX 讲（待交付）"标注。
