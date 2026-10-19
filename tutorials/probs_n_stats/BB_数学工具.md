# 数学工具（BB）——本课程用到的分析与代数工具

> 定位：本课程的**附录**，承载概率统计正文要用、但不属于概率统计本身的分析工具（极限、级数、积分）。正文遇到时**就地给最小说明**并指向这里，不重复整段推导，也不空降一个没见过的积分或极限。
> 编号固定 `BB`，不随讲次增加而重排（和 `AA_一览.md` 同一纪律）。维护：用到哪节补哪节。
> 与 `AA_一览.md` 的分工：`AA` 是概率统计自身的概念与公式字典；`BB` 是它们背后借用的数学工具。

---

## BB.1 常用极限

**BB.1.1 $\displaystyle\lim_{n\to\infty}\Bigl(1+\frac{a}{n}\Bigr)^{n}=e^{a}$**

这是什么：当 $n$ 趋于无穷时，$\bigl(1+\frac{a}{n}\bigr)^{n}$ 的极限就等于 $e^{a}$，其中 $e\approx2.718281828$ 是自然常数（$e=\lim_{n\to\infty}(1+\frac1n)^n$，即取 $a=1$）。

为什么成立：两边取对数，$n\ln\bigl(1+\frac{a}{n}\bigr)$；当 $\frac{a}{n}$ 很小时 $\ln(1+x)\approx x$（见 BB.2），于是它约等于 $n\cdot\frac{a}{n}=a$，故整体趋于 $e^{a}$。

常用特例：$\displaystyle\lim_{n\to\infty}\Bigl(1-\frac{\lambda}{n}\Bigr)^{n}=e^{-\lambda}$（令 $a=-\lambda$）。

用途：连续复利；**二项分布到泊松分布的极限**（第 05 讲 §4）；指数分布的归一化。

**BB.1.2 $\displaystyle\lim_{n\to\infty}\frac{n(n-1)(n-2)\cdots(n-k+1)}{n^{k}}=1$（$k$ 固定）**

这是什么：分子是 $k$ 个数连乘，当 $n$ 很大时每个因子都约等于 $n$，除以 $n^{k}$ 后整体趋于 1。

用途：由二项分布推出泊松分布时，消掉组合数带来的因子。

---

## BB.2 指数函数与级数

**BB.2.1 指数函数的级数展开**
$$e^{x}=\sum_{k=0}^{\infty}\frac{x^{k}}{k!}=1+x+\frac{x^{2}}{2!}+\frac{x^{3}}{3!}+\cdots$$
（$k!$ 是阶乘；这个级数对所有实数 $x$ 都收敛。）用途：验证泊松分布的归一化——$\sum_{k=0}^{\infty}\frac{\lambda^{k}}{k!}=e^{\lambda}$（第 05 讲 §4）。

**BB.2.2 对数**
- $\ln(ab)=\ln a+\ln b$，$\ln(a^{b})=b\ln a$；
- 当 $x\to0$ 时 $\ln(1+x)\approx x$（一阶近似）。

---

## BB.3 定积分技巧

**换元（凑微分）**：$\displaystyle\int f\bigl(g(x)\bigr)\,g'(x)\,\mathrm{d}x=\int f(u)\,\mathrm{d}u$，其中 $u=g(x)$。

**分部积分**：$\displaystyle\int u\,\mathrm{d}v=uv-\int v\,\mathrm{d}u$。

**二重积分与累次积分**：平面区域上的积分可写成两次一维积分（先对一个变量、再对另一个）：
$$\iint_{D} f(x,y)\,\mathrm{d}x\,\mathrm{d}y=\int\Bigl(\int f(x,y)\,\mathrm{d}y\Bigr)\mathrm{d}x.$$
（第 09、10 讲求二维分布、卷积时会用到。）

---

## BB.4 高斯积分

**标准形式**
$$\int_{-\infty}^{+\infty}e^{-x^{2}/2}\,\mathrm{d}x=\sqrt{2\pi}.$$
一般形式（平移与缩放）：
$$\int_{-\infty}^{+\infty}e^{-\frac{(x-\mu)^{2}}{2\sigma^{2}}}\,\mathrm{d}x=\sigma\sqrt{2\pi}.$$
另有 $\displaystyle\int_{-\infty}^{+\infty}e^{-x^{2}}\,\mathrm{d}x=\sqrt{\pi}$，$\displaystyle\int_{0}^{+\infty}e^{-x^{2}}\,\mathrm{d}x=\frac{\sqrt{\pi}}{2}$。

来历（一句话）：把 $\bigl(\int e^{-x^2}\mathrm{d}x\bigr)^2$ 写成二重积分后转到极坐标，可积出 $\pi$，开方即得。**不必会推，要会认、会用。**

用途：正态密度里那个"看起来突兀"的常数 $\frac{1}{\sqrt{2\pi}}$，正是为了让它全轴积分为 1（第 07 讲 §1）。

---

## BB.5 Gamma 函数

**定义**（$\alpha>0$）：
$$\Gamma(\alpha)=\int_{0}^{+\infty}x^{\alpha-1}e^{-x}\,\mathrm{d}x.$$

**基本性质**：
- $\Gamma(n)=(n-1)!$（$n$ 为正整数，例如 $\Gamma(1)=1,\Gamma(2)=1,\Gamma(3)=2$）；
- 递推：$\Gamma(\alpha+1)=\alpha\,\Gamma(\alpha)$；
- $\Gamma\!\left(\dfrac12\right)=\sqrt{\pi}$。

用途：Gamma 分布、$\chi^{2}$ 分布密度的归一化常数（第 06、15 讲）。

---

## BB.6 常用级数求和

**几何级数**（$|r|<1$）：
$$\sum_{k=0}^{\infty}r^{k}=\frac{1}{1-r},\qquad \sum_{k=1}^{\infty}r^{k}=\frac{r}{1-r}.$$
**带权几何级数**：
$$\sum_{k=1}^{\infty}k\,r^{k-1}=\frac{1}{(1-r)^{2}},\qquad |r|<1.$$

用途：几何分布的归一化与期望（第 05、11 讲）。