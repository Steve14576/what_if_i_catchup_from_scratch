# 线性代数——附录：关键概念·公式·中英对照字典（AA）

> 定位：本课程的附录、字典——不必像正文循循善诱从头讲，但每条都**说清"是什么"**（完整、自足的定义，忘了翻回来能重新明白这东西到底指什么）；**只写"怎么用"不写"是什么"是禁止的**。首次出现的叙述性教学（动机/例子/推导）在对应讲正文里，本表不重复也不替代。
> 编号固定 `AA_`，不随讲次增加而重排。维护：每讲交付后补入本讲新条目；第 2 遍回查时批量对账去重（每条"首次出现讲次"与正文交叉核对）。
> 理解层次三档：**要能推导/手算** ／ **要知道有这回事+何时找它** ／ **要建立直觉**。

## 一、概念与术语（中英对照）

| 概念（中文） | 英文/缩写 | 定义（说清"是什么"） | 首次出现 | 理解层次 |
|---|---|---|---|---|
| 向量 | vector | 一列有序的数（列向量），几何上表示既有大小又有方向的位移；$\mathbb{R}^n$ 的元素是 $n$ 个数排成一列 | 第 01 讲 | 要建立直觉 |
| 分量 | component / entry | 向量（或矩阵）里的某一个具体的数 | 第 01 讲 | 要知道有这回事 |
| 标量 | scalar | 单独一个数（相对于"一列数"的向量而言），用来对向量做缩放 | 第 01 讲 | 要会用 |
| 实向量空间 | $\mathbb{R}^n$ | 所有 $n$ 个实数组成的列构成的集合，配上逐分量加法与数乘 | 第 01 讲 | 要建立直觉 |
| 向量加法 | vector addition | 两向量对应分量相加，几何上是"首尾相接再连总位移" | 第 01 讲 | 要能手算 |
| 数乘 | scalar multiplication | 标量乘向量的每个分量，几何上是缩放（负号则反向） | 第 01 讲 | 要能手算 |
| 线性组合 | linear combination | $c_1\vec v_1+\cdots+c_k\vec v_k$，只含数乘与加法的叠加；结果仍是一个向量 | 第 01 讲 | 要建立直觉 |
| 张成 | span | 一组向量所有线性组合构成的集合，几何上是过原点的点/线/面/空间 | 第 01 讲 | 要建立直觉 |
| 矩阵 | matrix | $m\times n$ 个数组成的 $m$ 行 $n$ 列矩形数表；可视为列向量打包、行方程打包、线性变换、权重表 | 第 02 讲 | 要建立直觉 |
| 尺寸 | dimension (of a matrix) | 矩阵的行数 $m$ 与列数 $n$，记 $m\times n$，决定运算能否进行与结果大小 | 第 02 讲 | 要会用 |
| 行向量 / 列向量 | row / column vector | $1\times n$（横写）/ $n\times1$（竖写）的矩阵 | 第 02 讲 | 要知道有这回事 |
| 方阵 | square matrix | 行数等于列数（$n\times n$）的矩阵 | 第 02 讲 | 要知道有这回事 |
| 单位矩阵 | identity matrix, $I$ | 对角线全 1、其余全 0 的方阵；满足 $AI=IA=A$，代表"恒等/什么都不变"的变换 | 第 02 讲 | 要会用 |
| 对角矩阵 | diagonal matrix | 仅对角线上可能非零的方阵，如 $\mathrm{diag}(d_1,\dots,d_n)$；代表各坐标轴各自缩放 | 第 02 讲 | 要会用 |
| 转置 | transpose, $A^T$ | 把矩阵行列互换：第 $i$ 行变第 $i$ 列 | 第 02 讲 | 要能手算 |
| 矩阵乘法 | matrix multiplication | $(AB)_{ij}=\sum_k a_{ik}b_{kj}$，左行点右列；要求左列数=右行数；代表变换的复合 | 第 02 讲 | 要能推导/手算 |
| 内维 / 外维 | inner / outer dimension | $(m\times n)(n\times p)$ 中相等的 $n$ 叫内维（能否乘的关卡），$m,p$ 叫外维（结果尺寸） | 第 02 讲 | 要会用 |
| 交换律不成立 | non-commutativity | 一般 $AB\neq BA$（甚至一个有定义另一个无定义）；只有特殊对（同心旋转、与 $I$、与自身幂）才交换 | 第 02 讲 | 要知道+防错 |
| 零因子 | zero divisors | 存在 $A\neq0,B\neq0$ 却 $AB=0$，故矩阵乘法不能像数那样"约去公因子" | 第 02 讲 | 要知道+防错 |
| Hadamard 积 | Hadamard (elementwise) product | 同尺寸矩阵逐元素相乘，numpy 里是 `*`，**不是**矩阵乘法（`@`） | 第 02 讲 | 要知道有这回事 |
| 矩阵的幂 | power of a matrix, $A^k$ | 方阵连乘自身 $k$ 次，$A^0=I$ | 第 02 讲 | 要会用 |
| 置换矩阵 | permutation matrix | 每行每列恰一个 1、其余 0 的方阵；左乘换行、右乘换列 | 第 02 讲(作业) | 要知道有这回事 |
| 剪切矩阵 | shear matrix | 形如 $\begin{pmatrix}1&k\\0&1\end{pmatrix}$，把一个坐标轴方向按另一坐标"斜推"的变换（第 10 讲细讲） | 第 02 讲(作业) | 要建立直觉 |
| 线性方程组 | system of linear equations | 若干个"未知数一次"的方程的集合；矩阵形式 $A\vec x=\vec b$ | 第 03 讲 | 要能手算 |
| 增广矩阵 | augmented matrix, $[A\mid\vec b]$ | 把系数矩阵 $A$ 与右端列 $\vec b$ 用竖线（=等号）拼成的表，消元在其上就地操作 | 第 03 讲 | 要会用 |
| 初等行变换 | elementary row operation | 换两行 / 某行乘非零数 / 某行加另一行的倍数；三种都保解且可逆 | 第 03 讲 | 要能推导/手算 |
| 行阶梯形 | row echelon form (REF) | 主元逐行右移、主元下方全 0 的阶梯形状；高斯消元的终点 | 第 03 讲 | 要能手算 |
| 简化行阶梯形 | reduced row echelon form (RREF) | 在 REF 基础上主元为 1 且主元上下都为 0；对给定矩阵唯一，可直读解 | 第 03 讲 | 要能手算 |
| 主元 | pivot | 每行第一个非零元素，消元时用它清除同列下方（RREF 还清上方）的元 | 第 03 讲 | 要会用 |
| 回代 | back substitution | 从 REF 最底行往上逐行解出各未知数 | 第 03 讲 | 要能手算 |
| 自由变量 | free variable | 所在列无主元的未知数，可任意取值；个数 $=n-r$ | 第 03 讲 | 要建立直觉 |
| 基本变量 | basic (leading) variable | 对应主元列的未知数，被方程用自由变量表示 | 第 03 讲 | 要知道有这回事 |
| 相容 / 不相容 | consistent / inconsistent | 有解称相容、无解称不相容；判据 $\mathrm{rank}(A)=\mathrm{rank}([A\mid\vec b])$ | 第 03 讲 | 要会用 |
| 齐次 / 非齐次 | homogeneous / non-homogeneous | $\vec b=\vec 0$ 的方程组叫齐次，否则非齐次 | 第 03 讲 | 要知道有这回事 |
| 高斯消元 | Gaussian elimination | 用初等行变换化 REF 再回代求解的流程 | 第 03 讲 | 要能手算 |
| 高斯-若尔当消元 | Gauss-Jordan elimination | 继续化到 RREF、直接从右端列读解的流程 | 第 03 讲 | 要能手算 |
| 秩 | rank, $\mathrm{rank}(A)$ | 矩阵化 REF 后的主元个数 = 独立行(列)数 = 列空间维数；行秩恒等于列秩 | 第 04 讲 | 要能推导/手算 |
| 行秩 / 列秩 | row rank / column rank | 极大线性无关行(列)的个数；两者对任意矩阵相等（故"秩"定义良好） | 第 04 讲 | 要建立直觉 |
| 满秩 | full rank | $\mathrm{rank}(A)=\min(m,n)$；方阵满秩即 $\mathrm{rank}=n$（⇔可逆，第 06 讲证） | 第 04 讲 | 要知道有这回事 |
| 零空间 / 核 | null space / kernel, $N(A)$ | 齐次方程 $A\vec x=\vec 0$ 的全体解集；是 $\mathbb R^n$ 的子空间，维数 $=n-\mathrm{rank}(A)$ | 第 04 讲 | 要建立直觉 |
| 秩-零化度定理 | rank-nullity theorem | $\mathrm{rank}(A)+\dim N(A)=n$，即主元数 + 自由变量数 = 未知数个数 | 第 04 讲 | 要能用+能复述 |
| 特解 | particular solution | 非齐次方程 $A\vec x=\vec b$ 的任意一个具体解 $\vec p$ | 第 04 讲 | 要会用 |
| 通解 | general solution | 非齐次方程的全体解，形式为 特解 + 零空间中任意向量 | 第 04 讲 | 要能手算 |
| 仿射集 | affine set | 子空间平移一个向量后的集合（不过原点）；非齐次解集即此类 | 第 04 讲 | 要知道有这回事 |

## 二、公式

| 公式 | 符号各指什么 | 适用条件 | 出处讲次 |
|---|---|---|---|
| $A\vec x = x_1\vec c_1+x_2\vec c_2+\cdots+x_n\vec c_n$ | $A$ 是 $m\times n$ 矩阵，$\vec c_j$ 是 $A$ 的第 $j$ 列，$x_j$ 是 $\vec x$ 的第 $j$ 分量 | 恒成立（矩阵乘向量的列视角） | 第 02 讲 |
| $(AB)_{ij}=\sum_{k=1}^{n} a_{ik}b_{kj}$ | $a_{ik}$ 是 $A$ 第 $i$ 行第 $k$ 列，$b_{kj}$ 是 $B$ 第 $k$ 行第 $j$ 列 | $A$ 为 $m\times n$、$B$ 为 $n\times p$（内维相等） | 第 02 讲 |
| $(AB)^T = B^T A^T$ | 转置反序律；$(\cdot)^T$ 是转置 | 尺寸相容时恒成立 | 第 02 讲 |
| $(AB)\vec x = A(B\vec x)$ | 矩阵乘法的结合性（变换复合的黄金性质） | 尺寸相容时恒成立 | 第 02 讲 |
| $\vec b\in\mathrm{span}(\vec v_1,\dots,\vec v_n)\iff A\vec x=\vec b\ \text{有解}$ | $A=[\vec v_1\ \cdots\ \vec v_n]$ | span 成员判定与方程组可解性的等价 | 第 03 讲 |
| 自由变量个数 $=n-r$ | $n$ 未知数个数、$r$ 主元（秩）个数 | 方程组相容（有解）时 | 第 03 讲 |
| 相容判据 $\mathrm{rank}(A)=\mathrm{rank}([A\mid\vec b])$ | $\mathrm{rank}$ 为秩（此处＝主元个数） | 判线性方程组有无解 | 第 03 讲 |
| 秩-零化度 $\mathrm{rank}(A)+\dim N(A)=n$ | $n$ 为列数=未知数个数；$\dim N(A)$ 零空间维数 | 对任意 $m\times n$ 矩阵成立 | 第 04 讲 |
| 非齐次通解 $\vec x=\vec p+\vec x_h,\ \vec x_h\in N(A)$ | $\vec p$ 一特解，$\vec x_h$ 齐次解 | $A\vec x=\vec b$ 相容时 | 第 04 讲 |
