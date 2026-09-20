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
| 零空间 / 核 | null space / kernel, $N(A)$ | 齐次方程 $A\vec x=\vec 0$ 的全体解集；是 $\mathbb R^n$ 的子空间，维数 $=n-\mathrm{rank}(A)$；变换语言写作 $\ker(T)$（第 10 讲对账：同一概念两张皮） | 第 04 讲 | 要建立直觉 |
| 秩-零化度定理 | rank-nullity theorem | $\mathrm{rank}(A)+\dim N(A)=n$，即主元数 + 自由变量数 = 未知数个数 | 第 04 讲 | 要能用+能复述 |
| 特解 | particular solution | 非齐次方程 $A\vec x=\vec b$ 的任意一个具体解 $\vec p$ | 第 04 讲 | 要会用 |
| 通解 | general solution | 非齐次方程的全体解，形式为 特解 + 零空间中任意向量 | 第 04 讲 | 要能手算 |
| 仿射集 | affine set | 子空间平移一个向量后的集合（不过原点）；非齐次解集即此类 | 第 04 讲 | 要知道有这回事 |
| 行列式 | determinant, $\det A$ | 仅对方阵定义、把方阵映成一个实数的函数；等于变换对单位体积的缩放倍数（带符号表方向），$=0$ ⇔ 压扁（降维） | 第 05 讲 | 要能推导/手算 |
| 余子式 / 代数余子式 | minor / cofactor | 删去某元素所在行与列后子矩阵的行列式；再乘棋盘符号 $(-1)^{i+j}$ 即代数余子式 | 第 05 讲 | 要会手算 |
| 拉普拉斯展开 | Laplace (cofactor) expansion | 按某一行/列用代数余子式展开求行列式；挑零多的行最省 | 第 05 讲 | 要会手算 |
| 萨鲁斯法则 | Sarrus' rule | 仅适用 $3\times3$ 的"对角线乘积相减"速记；$n\ge4$ 无对应画法（$4!=24$ 项） | 第 05 讲 | 要知道+防错 |
| 多线性 / 交错 / 规范化 | multilinear / alternating / normalized | 确定行列式的三条公理：逐行线性、交换两行变号、单位阵取 1；用于推性质，不要求默写 | 第 05 讲 | 要知道有这回事 |
| 有向面积/体积 | signed area / volume | 行列式的几何意义；符号表定向（手性），绝对值表大小 | 第 05 讲 | 要建立直觉 |
| 逆矩阵 | inverse matrix, $A^{-1}$ | 与 $A$ 同尺寸、满足 $AA^{-1}=A^{-1}A=I$ 的矩阵；存在则唯一，几何上就是"撤销该变换" | 第 06 讲 | 要能推导/手算 |
| 可逆 / 非奇异 | invertible / nonsingular | 有逆矩阵的方阵；等价于 $\det\neq0$/满秩/列无关/$N(A)=\{\vec0\}$ | 第 06 讲 | 要会用 |
| 奇异 | singular | 不可逆的方阵（$\det=0$）；两种解释：行列式矛盾式、变换压扁丢信息 | 第 06 讲 | 要会用 |
| 伴随矩阵 | adjugate | 代数余子式转置成的矩阵；一般公式 $A^{-1}=\tfrac1{\det A}\mathrm{adj}(A)$，手算不靠它、$2\times2$ 特例公式可用 | 第 06 讲 | 要知道有这回事 |
| 左逆 / 右逆 | left / right inverse | 长方阵只能单侧有意义的概念；双侧逆只对可逆方阵存在 | 第 06 讲 | 要知道有这回事 |
| 初等矩阵 | elementary matrix | 单位阵做一次行变换得到的矩阵；左乘它等价于对该矩阵做同一行变换 | 第 06 讲 | 要知道有这回事 |
| 自逆（对合） | involution / self-inverse | 满足 $A^2=I$ 的矩阵；$A^{-1}=A$ 但不一定等于 $I$ | 第 06 讲 | 要知道+防错 |
| 向量空间 | vector space | 配加法与数乘、满足八条公理（加法四条+数乘四条）的集合；人话版：能加、能缩放、结果还在里面 | 第 07 讲 | 要建立直觉+会用清单 |
| 八条公理 | eight axioms | 向量空间的打勾清单（交换/结合/零元/负元 + 归一/结合/两条分配），遇到新集合逐条查；不背 | 第 07 讲 | 要知道有这回事+打勾用 |
| 子空间 | subspace | 向量空间的子集，满足三条件：含零向量 / 加封闭 / 数乘封闭；等价于"非空且对线性组合封闭" | 第 07 讲 | 要能手判 |
| 张成子空间 | spanning (span) subspace | 一组向量所有线性组合构成的子空间=包含它们的最小子空间 | 第 07 讲 | 要建立直觉 |
| 列空间 | column space, $\mathrm{col}(A)$ | $A$ 的全部列张成的子空间=所有 $A\vec x$ 的集合；$\vec b\in\mathrm{col}(A)\iff A\vec x=\vec b$ 有解 | 第 07 讲 | 要建立直觉 |
| 子空间的交 / 并 / 和 | intersection / union / sum of subspaces | 交是子空间、并一般不是（反例：两坐标轴）、和 $W_1+W_2$ 是子空间 | 第 07 讲 | 要知道+防错 |
| 线性无关 / 相关 | (in)dependent | 无关：方程 $c_1\vec v_1+\cdots+c_k\vec v_k=\vec0$ 只有平凡解 ⇔ 谁也不能被其余拼出；相关：存在非平凡组合给出零（有冗余） | 第 08 讲 | 要能手判 |
| 基 | basis | 子空间中"张成且无关"的向量组=恰好够用的生成集=最大无关组；不唯一、零向量不能进 | 第 08 讲 | 要能推导/手算 |
| 标准基 | standard basis | $\mathbb R^n$ 的 $\vec e_1,\dots,\vec e_n$、$P_n$ 的 $1,t,\dots,t^n$；最顺手的一副基，坐标=分量 | 第 08 讲 | 要会用 |
| 维数 | dimension, $\dim W$ | 基的大小；良定义（任何两组基个数相同），$n$ 维空间里 $n$ 个向量"张成⇔无关"自动互推 | 第 08 讲 | 要能推导/手算 |
| 坐标向量 | coordinate vector | 向量在给定基下的表示系数组成的向量；换基时坐标按换基矩阵变换 | 第 08 讲 | 要知道有这回事 |
| 四个基本子空间 | four fundamental subspaces | $\mathrm{col}(A)$、$N(A)$、$\mathrm{col}(A^T)$、$N(A^T)$ 四个子空间的合称；线性代数基本定理的载体 | 第 09 讲 | 要建立直觉 |
| 行空间 | row space, $\mathrm{col}(A^T)$ | $A$ 全部行向量的所有线性组合；恰好等于 $A^T$ 的列空间；住在 $\mathbb{R}^n$ | 第 09 讲 | 要建立直觉 |
| 左零空间 | left null space, $N(A^T)$ | 所有满足 $A^T\vec y=\vec 0$（即 $\vec y^{\,T}A=\vec 0^{\,T}$）的 $\vec y$；“左”来自 $\vec y$ 乘在 $A$ 左边；住在 $\mathbb{R}^m$ | 第 09 讲 | 要建立直觉 |
| 点积（简版） | dot product | $\vec u\cdot\vec v=u_1v_1+\cdots+u_dv_d$（逐分量乘再求和）；几何意义（长度/夹角/投影）第 13 讲详讲 | 第 09 讲 | 要会用 |
| 正交 | orthogonal | 两向量点积为 0，几何上垂直；是对“同一 $\mathbb{R}^d$ 里”两向量说的 | 第 09 讲 | 要建立直觉 |
| 正交补 | orthogonal complement, $W^{\perp}$ | 与 $W$ 中每个向量都正交的全部向量构成的子空间（与 $W$ 同住 $\mathbb{R}^d$） | 第 09 讲 | 要建立直觉 |
| 直和 | direct sum, $\oplus$ | $V=W_1\oplus W_2$：$V$ 中每个向量可**唯一**写成 $\vec w_1+\vec w_2$；判据：交为零 + 维数和 = 全维 | 第 09 讲 | 要会用 |
| 线性变换 | linear transformation / map | 保加法与数乘（$T(\vec u+\vec v)=T(\vec u)+T(\vec v)$、$T(c\vec v)=cT(\vec v)$，合起来即保线性组合）的映射 $T:V\to W$；必把零向量送零向量 | 第 10 讲 | 要能推导/手算 |
| 仿射变换 | affine map | "线性部分 + 平移"的映射（如 $\vec x\mapsto2\vec x+(1,2)$，即中学 $y=2x+3$ 型）；仿射但**不是**线性变换（平移破坏数乘） | 第 10 讲 | 要知道+防错 |
| 标准矩阵 | standard matrix | $T:\mathbb R^n\to\mathbb R^m$ 在标准基下的矩阵 $A=\big[T(\vec e_1)\cdots T(\vec e_n)\big]$（**列 = 基向量的像**），满足 $T(\vec x)=A\vec x$ | 第 10 讲 | 要能推导/手算 |
| 像 / 值域 | image / range, $\mathrm{im}(T)$ | 变换全部输出的集合 $\{T(\vec v)\}$；矩阵版即列空间 $\mathrm{col}(A)$（第 07/09 讲的值域），是输出空间的子空间 | 第 10 讲 | 要建立直觉 |
| 单射 | one-to-one / injective | 不同输入必到不同输出的变换；判据：$\ker(T)=\{\vec0\}$ | 第 10 讲 | 要会用 |
| 满射 | onto / surjective | 输出全部被打到的变换（$\mathrm{im}(T)=W$）；$n$ 到 $n$ 维时与单射互锁（06 讲等价表的深层结构） | 第 10 讲 | 要会用 |
| 双射 / 逆变换 | bijective / inverse map | 又单又满 ⟺ 每点可逐点撤销，存在逆变换 $T^{-1}$；方阵情形即第 06 讲可逆矩阵 | 第 10 讲 | 要知道有这回事 |
| 换基矩阵 | change-of-basis matrix, $P$ | 列 = 新基向量（旧坐标）的矩阵；$\vec x=P[\vec x]_{\mathcal B}$（拼装）、$[\vec x]_{\mathcal B}=P^{-1}\vec x$（拆卸） | 第 10 讲 | 要会用 |
| 相似 | similar, $B=P^{-1}AP$ | 同一线性变换在两组基下的矩阵之间的关系；不变量：秩、$\det$、迹（特征值第 11 讲揭晓） | 第 10 讲 | 要能推导/手算 |
| 迹 | trace, $\mathrm{tr}(A)$ | 方阵对角元之和；相似不变量（由循环律 $\mathrm{tr}(XY)=\mathrm{tr}(YX)$ 保证）；det 或迹不等可一票否决相似 | 第 10 讲 | 要会用 |
| 行等价 | row equivalent | $B=EA$（$E$ 可逆 = 可经行变换互达）；保的是方程组解集，**不是**换基（不保 det/迹；消元不是换基） | 第 03 讲（第 10 讲命名） | 要知道+防错 |
| 矩阵等价 | equivalent | $B=PAQ$（$P,Q$ 可逆）：两侧各换各的基的同一台机器；只保秩（不变量最少的关系） | 第 10 讲 | 要知道有这回事 |
| 合同 | congruent | $B=P^TA P$：二次型换变量（第 16 讲正式登场），保正负惯性 | 第 10 讲（预告） | 要知道有这回事 |
| 特征值 | eigenvalue | 满足 $A\vec v=\lambda\vec v$（存在非零 $\vec v$）的数 $\lambda$；“变换自己的数”——某方向上机器退化成一个乘法；可为 $0$/负/复 | 第 11 讲 | 要能推导/手算 |
| 特征向量 | eigenvector | 满足 $A\vec v=\lambda\vec v$ 的非零向量；方向不变只伸缩；可任意缩放（同一方向皆可），零向量不算 | 第 11 讲 | 要能推导/手算 |
| 特征方程 / 特征多项式 | characteristic equation / polynomial | $\det(A-\lambda I)=0$；展开为 $n$ 次多项式 $p(\lambda)$；来历：$(A-\lambda I)\vec v=\vec0$ 要非零解 ⟺ 奇异 | 第 11 讲 | 要能推导/手算 |
| 特征空间 | eigenspace, $E_\lambda$ | 属于 $\lambda$ 的全部特征向量加零向量：$E_\lambda=N(A-\lambda I)$（就是零空间，第 09 讲机器直接复用）；维数 = 几何重数 | 第 11 讲 | 要能手算 |
| 谱 | spectrum, $\sigma(A)$ | $A$ 的全体特征值（不计重数的集合）；相似不变量（本体的属性，换名片不变） | 第 11 讲 | 要知道有这回事 |
| 代数重数 | algebraic multiplicity | $\lambda$ 作为特征多项式根的重次（多项式里数的配额） | 第 11 讲 | 要会算 |
| 几何重数 | geometric multiplicity | $\dim E_\lambda=n-\mathrm{rank}(A-\lambda I)$（实际领到的无关方向数）；恒 ≤ 代数重数；缺口 ⟹ 凑不齐特征基 | 第 11 讲 | 要会算 |
| 幂法 | power iteration | 迭代 $\vec x\leftarrow A\vec x/\|A\vec x\|$ 收敛到主特征方向的方法；要求 $|\lambda_1|>|\lambda_2|$ 严格占优；大矩阵求最大特征值的工业级方法 | 第 11 讲 | 要知道+会跑 |
| 可对角化 | diagonalizable | 存在可逆 $P$ 使 $P^{-1}AP=\Lambda$ 对角（即相似于对角阵）；三等价：可对角化 ⟺ $n$ 个无关特征向量 ⟺ 每个 $\lambda$ 几何重数=代数重数；互异 $n$ 根自动可 | 第 12 讲 | 要能推导/手算 |
| 马尔可夫矩阵 | Markov / stochastic matrix | 每列元素和为 1 的方阵；$1$ 必是特征值（稳态存在），稳态 = $\lambda=1$ 的特征向量归一化到分量和 1；涨落分量按 $|\lambda_2|^k$ 退场 | 第 12 讲 | 要会用 |
| 若尔当块 | Jordan block | 形如 $\begin{pmatrix}\lambda&1\\0&\lambda\end{pmatrix}$ 的“几乎对角”块；重数缺口矩阵的幂长出“乘方×多项式”因子；完备理论第 18 讲 | 第 12 讲（预告） | 要知道有这回事 |
| 内积 | inner product | 满足对称、线性、正定三公理的“吃两向量吐一数”运算；三款：$\mathbb R^n$ 点积、$P_n$ 积分款 $\int_0^1fg$、加权款；公理=合格度量衡的打勾清单 | 第 13 讲 | 要能手算 |
| 范数 | norm | $\|\vec v\|=\sqrt{\langle\vec v,\vec v\rangle}$（长度）；正定性保证非负且零向量唯一零长；先有内积后有长度 | 第 13 讲 | 要能手算 |
| 柯西-施瓦茨不等式 | Cauchy–Schwarz inequality | $|\langle\vec u,\vec v\rangle|\le\|\vec u\|\,\|\vec v\|$（等号⟺共线）；夹角定义 $\cos\theta$ 落在 $[-1,1]$ 的合法性证书；证法：正定性+二次函数判别式 | 第 13 讲 | 要能推导 |
| 正交（正式版） | orthogonal | $\langle\vec u,\vec v\rangle=0$；对任意内积空间成立（第 09 讲简版升格）；只对同一空间里的向量说 | 第 13 讲 | 要建立直觉 |
| 正交向量组 / 单位正交组 | orthogonal / orthonormal set | 两两正交的向量组（再加各长 1 即单位正交）；天然线性无关；坐标=内积，无需求解 | 第 13 讲 | 要会算 |
| 投影 / 垂线脚 | projection | 把 $\vec b$ 拆成 $\vec p+\vec e$（$\vec p\in W$、$\vec e\perp W$）；垂线脚（几何）、最近点（用途）、正规方程（算法）、$P$ 矩阵（机器）四张皮 | 第 13 讲 | 要能推导/手算 |
| 投影矩阵 | projection matrix | $P=A(A^TA)^{-1}A^T$（列满秩）；对称+幂等是充要身份证；$I-P$ 投到 $W^\perp$；误差永远落 $W^\perp$ | 第 13 讲 | 要能推导/手算 |
| 正交矩阵 | orthogonal matrix | 列为单位正交组的方阵；$Q^TQ=I$、$Q^{-1}=Q^T$（求逆免费）；保内积/长度/夹角（刚体运动：旋转与反射）；旋转矩阵是真身 | 第 13 讲 | 要会用 |
| Gram-Schmidt 正交化 | Gram-Schmidt process | 输入斜基、输出两两正交基，每步地盘不变（$\mathrm{span}\{e_1..e_j\}=\mathrm{span}\{a_1..a_j\}$）；投影当减法器：减掉新向量在已承认正交方向上的全部投影 | 第 14 讲 | 要能推导/手算 |
| QR 分解 | QR factorization | $A=QR$（$Q$ 列单位正交、$R$ 上三角）；$R$ 是 GS 的内积账本；上三角性=新方向垂直全部旧地盘（时间脚印）；列相关时 $R$ 对角出零元 | 第 14 讲 | 要能推导/手算 |
| 经典 / 修正 Gram-Schmidt | classical / modified GS | 数学上恒等；浮点上修正版（逐步减、用更新中的残差）稳得多；工业标准是 LAPACK 的 Householder（第 20 讲） | 第 14 讲 | 要知道+会选 |
| 希尔伯特矩阵 | Hilbert matrix | $H_{ij}=1/(i+j-1)$；著名病态矩阵（误差剧烈放大），病态/条件数第 20 讲正式定义；本课数值稳定性对照的试验田 | 第 14 讲（预告） | 要知道有这回事 |
| 超定方程组 | overdetermined system | 方程多于未知数（拟合场景常态）；$\vec b$ 通常不在 $\mathrm{col}(A)$——无精确解是常态而非事故 | 第 15 讲 | 要建立直觉 |
| 最小二乘 | least squares | 无解时换好问题：$\min_{\vec x}\|\vec b-A\vec x\|^2$（平方三理由：同序/二次好解/高斯下最大似然）；最优 $\hat{\vec x}$ 恒存在（投影存在） | 第 15 讲 | 要能推导/手算 |
| 残差 | residual | $\vec e=\vec b-A\hat{\vec x}$；最优时垂直列空间；回归性质 $\sum e_i=0$、$\sum t_ie_i=0$（均值零、与自变量不相关）——最快的验算器 | 第 15 讲 | 要会算 |
| 伪逆（预告） | pseudoinverse, $A^+$ | $A^TA$ 奇异时挑长度最短的代表性解；正式定义与构造第 17 讲（SVD） | 第 15 讲（预告） | 要知道有这回事 |

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
| $\det(AB)=\det A\cdot\det B$ | $A,B$ 同为 $n\times n$ 方阵 | 乘积的行列式=各自行列式之积 | 第 05 讲 |
| $\det(A^T)=\det A$；$\det(kA)=k^n\det A$ | $k$ 标量，$A$ 为 $n\times n$ 方阵 | 转置不变；整矩阵数乘提 $n$ 次因子 | 第 05 讲 |
| 换行变号、倍加不变 | 行列式的行变换行为：交换两行取负、某行加另一行倍数不变 | 消元记账法求 $\det$ 的依据 | 第 05 讲 |
| $\det(A^{-1})=1/\det A$ | $A$ 可逆方阵 | 逆的行列式互为倒数 | 第 05/06 讲 |
| $A^{-1}=\tfrac1{\det A}\mathrm{adj}(A)$ | $\mathrm{adj}$ 为伴随矩阵 | $\det A\neq0$ 时；$2\times2$ 特例直接用 | 第 06 讲 |
| $(AB)^{-1}=B^{-1}A^{-1}$；$(A^{-1})^T=(A^T)^{-1}$；$(A^k)^{-1}=(A^{-1})^k$ | $A,B$ 同尺寸可逆 | 逆的反序律；逆与转置可交换；逆与幂可交换 | 第 06 讲 |
| $[A\mid I]\to[I\mid A^{-1}]$ | 高斯-若尔当求逆流程 | $A$ 可逆时；化一半发现全零行=不可逆 | 第 06 讲 |
| $\dim W=n$ 时 $n$ 个向量：张成 ⇔ 无关 | $W$ 是 $n$ 维空间 | 基验证可只查一个条件 | 第 08 讲 |
| 维数四件套 | $A$ 为 $m\times n$、$r=\mathrm{rank}(A)$ | $\dim\mathrm{col}(A)=\dim\mathrm{col}(A^T)=r$；$\dim N(A)=n-r$；$\dim N(A^T)=m-r$ | 第 09 讲 |
| 两条对账线 | 同上 | $r+(n-r)=n$（输入侧）；$r+(m-r)=m$（输出侧） | 第 09 讲 |
| 正交对 | 同上 | $N(A)\perp\mathrm{col}(A^T)$（都在 $\mathbb{R}^n$）；$N(A^T)\perp\mathrm{col}(A)$（都在 $\mathbb{R}^m$） | 第 09 讲 |
| 正交补给出等号 | 同上 | $N(A)=\mathrm{col}(A^T)^{\perp}$；$\mathrm{col}(A)=N(A^T)^{\perp}$（两个包含方向互夹，不用维数） | 第 09 讲 |
| 正交分解（直和） | 同上 | $\mathbb{R}^n=\mathrm{col}(A^T)\oplus N(A)$；$\mathbb{R}^m=\mathrm{col}(A)\oplus N(A^T)$ | 第 09 讲 |
| 维数公式（预告） | $W$ 为 $\mathbb{R}^d$ 的子空间 | $\dim W^{\perp}=d-\dim W$；完整证明留第 13 讲 | 第 09 讲 |
| $T(\vec x)=A\vec x$，$A=\big[T(\vec e_1)\cdots T(\vec e_n)\big]$ | $A$ 为 $m\times n$ 标准矩阵，列 = 各基向量的像 | $T$ 线性、两端用标准基 | 第 10 讲 |
| $R(\alpha)=\begin{pmatrix}\cos\alpha&-\sin\alpha\\\sin\alpha&\cos\alpha\end{pmatrix}$ | 平面逆时针旋转 $\alpha$ 的矩阵（基像法现场拼出，第 02 讲预告、第 10 讲兑现） | 2 维平面 | 第 10 讲 |
| $\vec x=P[\vec x]_{\mathcal B}$，$[\vec x]_{\mathcal B}=P^{-1}\vec x$ | $P$ 列 = 新基向量，$[\cdot]_{\mathcal B}$ 为 $\mathcal B$ 坐标 | $P$ 可逆（列是基必无关） | 第 10 讲 |
| $B=P^{-1}AP$（相似） | $A/B$ 为同一变换在标准基/新基 $\mathcal B$ 下的矩阵，$P$ 为换基矩阵 | 方阵、同一空间换基 | 第 10 讲 |
| $\dim\ker(T)+\dim\mathrm{im}(T)=\dim V$ | 变换版秩-零化度；矩阵版见第 04/09 讲 | $T:V\to W$ 有限维线性变换 | 第 10 讲 |
| $\mathrm{tr}(XY)=\mathrm{tr}(YX)$ | 迹的循环律；$X$ 为 $m\times n$、$Y$ 为 $n\times m$ | 尺寸相容时 | 第 10 讲 |
| 相似不变量：$\mathrm{rank}$、$\det$、$\mathrm{tr}$ 换基不变 | $B=P^{-1}AP$ 时三者与 $A$ 相同 | 用于一票否决"相似" | 第 10 讲 |
| $A\vec v=\lambda\vec v$（定义式） | $\lambda$ 是数，$\vec v\neq\vec0$；$\lambda<0$ 表示反向共线（翻折也算方向不变） | 方阵；$\lambda$ 可为 $0$/负/复 | 第 11 讲 |
| $\det(A-\lambda I)=0$ | 特征方程；$\lambda I$ 护矩阵外衣后移项，非零解 ⟺ 奇异；另一约定 $\det(\lambda I-A)$ 差 $(-1)^n$ 同方程 | 方阵 | 第 11 讲 |
| $\det A=\prod\lambda_i$，$\mathrm{tr}(A)=\sum\lambda_i$ | 特征值计重数；代 $\lambda=0$ 与比对系数得 | 猜根后验算两笔账 | 第 11 讲 |
| $E_\lambda=N(A-\lambda I)$，$\dim E_\lambda=n-\mathrm{rank}(A-\lambda I)$ | 特征空间 = 零空间；求特征向量 = 第 03 讲消元流程 | 每个 $\lambda$ 分别求 | 第 11 讲 |
| 相似 ⟹ 特征多项式逐系数相同 | $\det(P^{-1}AP-\lambda I)=\det(A-\lambda I)$；必要不充分（剪切与 $I$ 同多项式不相似） | 相似判定/反判定 | 第 11 讲 |
| 上三角 ⟹ 特征值 = 对角元 | $\det(A-\lambda I)=\prod(a_{ii}-\lambda)$；仅对与 $A$ 相似的三角化有效，RREF 不算 | 三角阵直读 | 第 11 讲 |
| $\lambda=0$ 是特征值 $\iff$ $A$ 奇异 | 可逆等价表 +1：可逆 $\iff$ 0 非特征值；$\lambda=0$ 的特征空间 = $N(A)$ | 方阵 | 第 11 讲 |
| 不同 $\lambda$ 的特征向量必无关 | $\lambda_1\neq\lambda_2$ 时 $\vec v_1,\vec v_2$ 无关（消去法）；$n$ 个互异 $\lambda$ ⟹ 特征基 | 凑对角化原料 | 第 11 讲 |
| 幂法收敛条件 $|\lambda_1|>|\lambda_2|$ | $A^k\vec x=c_1\lambda_1^k\vec v_1+c_2\lambda_2^k\vec v_2$，次项按 $(\lambda_2/\lambda_1)^k$ 退场；模相等则打转 | 主特征方向逼近 | 第 11 讲 |
| $A=P\Lambda P^{-1}$（对角化） | $P$ 列 = 特征向量，$\Lambda$ 对角 = 配对特征值（顺序跟列序走）；恒等式 $AP=P\Lambda$ 逐列读出 | $A$ 可对角化；每题验算 $AP=P\Lambda$ | 第 12 讲 |
| $A^k=P\Lambda^kP^{-1}$ | 中间 $P^{-1}P=I$ 相消；对角阵幂 = 逐元素乘方；赠品 $A^{-1}=P\Lambda^{-1}P^{-1}$、$f(A)=Pf(\Lambda)P^{-1}$（$e^A$ 预告 22 讲） | $A$ 可对角化；$k$ 任意 | 第 12 讲 |
| 判据：可对角化 ⟺ $n$ 个无关特征向量 ⟺ 几何=代数全领满 | 判定流程：解 $\lambda$ → 每个 $\dim E_\lambda=n-\mathrm{rank}(A-\lambda I)$ → 对账；互异 $n$ 根自动可；重根要查账 | 方阵 | 第 12 讲 |
| Binet 公式 $f_k=(\varphi^k-\psi^k)/\sqrt5$ | $\varphi,\psi$ 为 $\lambda^2-\lambda-1=0$ 的根；递推先化为 $\vec u_{k+1}=F\vec u_k$，$F=[[1,1],[1,0]]$ | 二阶线性递推通项 | 第 12 讲 |
| 列和 1 ⟹ $1$ 是特征值 | $\vec{\mathbb 1}^TM=\vec{\mathbb 1}^T$ + 转置不改行列式 ⟹ $M$ 与 $M^T$ 同特征多项式 | 马尔可夫稳态存在的代数根 | 第 12 讲 |
| 不可对角化者的幂 | $S^k=[[1,k],[0,1]]$；$J^k=[[\lambda^k, k\lambda^{k-1}],[0,\lambda^k]]$（乘方×多项式 = 缺口的形状） | 重数缺口矩阵 | 第 12 讲 |
| $\cos\theta=\langle\vec u,\vec v\rangle/(\|\vec u\|\|\vec v\|)$ | 夹角定义；合法性由 C-S 保证（$|\cos|\le1$） | 任意内积空间、非零向量 | 第 13 讲 |
| 勾股定理（内积版） | $\vec u\perp\vec v\Rightarrow\|\vec u+\vec v\|^2=\|\vec u\|^2+\|\vec v\|^2$（交叉项归零） | 正交对 | 第 13 讲 |
| 线投影 $\vec p=\dfrac{\vec a\cdot\vec b}{\vec a\cdot\vec a}\vec a$ | 解"误差$\perp\vec a$"所得；分母是解方程自然长出的系数；矩阵版 $P=\vec a\vec a^T/(\vec a^T\vec a)$ | $\vec a\neq\vec0$；$\|\vec e\|=$最近距离 | 第 13 讲 |
| 正规方程 $A^TA\hat{\vec x}=A^T\vec b$ | "误差垂直每列"逐列翻译而成；解出 $\hat{\vec x}$ 后 $\vec p=A\hat{\vec x}$；15 讲最小二乘主菜 | $A$ 列满秩时唯一解 | 第 13 讲 |
| $A^TA$ 可逆 $\iff$ $A$ 列线性无关 | 零空间链条：$A^TA\vec x=0\Rightarrow\|A\vec x\|^2=0\Rightarrow A\vec x=0$ | 判定器（列相关时公式失效，先 GS 剔冗余） | 第 13 讲 |
| 投影矩阵三性质 | $P^T=P$（转置链）、$P^2=P$（中间相消）、$(I-P)\vec b=\vec e$ 投 $W^\perp$ | 列满秩；对称+幂等=充要身份证 | 第 13 讲 |
| $\dim W^\perp=d-\dim W$ | $W$ 基排成矩阵 $W_{mat}$：$W^\perp=N(W_{mat}^T)$，四件套一行销账；$\mathbb R^d=W\oplus W^\perp$（分解存在+唯一） | $W\subseteq\mathbb R^d$ 子空间；09 讲预告在此兑现 | 第 13 讲 |
| $Q^TQ=I\Rightarrow$ 保内积保长度 | $(Q\vec u)^T(Q\vec v)=\vec u^T\vec u$；$Q^{-1}=Q^T$；旋转矩阵手验 $\cos^2+\sin^2=1$ | 方阵、列单位正交 | 第 13 讲 |
| GS 公式 $\vec e_j=\vec a_j-\sum_{i<j}\frac{\vec a_j\cdot\vec e_i}{\vec e_i\cdot\vec e_i}\vec e_i$ | 单模板：新向量减掉在每个已承认正交方向上的投影；分母是产出 $\vec e_i$ 的长度平方；$\vec e_j=\vec0$ 即检几余 | 任意内积空间的一组基 | 第 14 讲 |
| 正交基下坐标 $=$ 内积 | $\vec v=\sum c_i\vec q_i\Rightarrow c_j=\langle\vec v,\vec q_j\rangle$（交叉项全零）；斜基要解方程，正交基免费 | 单位正交基 | 第 14 讲 |
| $A=QR$：$r_{ij}=\vec q_i\cdot\vec a_j$，$r_{jj}=\|\vec e_j\|$ | $R$ 第 $j$ 列 $=\vec a_j$ 的正交坐标；$i>j$ 时 $\vec q_i\perp\vec a_j$ 所在地盘（上三角性）；$Q$ 可整体列变号（$R$ 同行变号） | $A$ 列满秩（不满足则 $R$ 对角出零） | 第 14 讲 |
| $P=QQ^T$ | 与 $A(A^TA)^{-1}A^T$ 恒等（$A^TA=R^TR$ 相消链）；投影“各取一次内积”；实测与 13 讲公式零差 | 列满秩 | 第 14 讲 |
| $QR$ 求解与稳定性 | $R\vec x=Q^T\vec b$ 回代；病态阵上比正规方程稳（希尔伯特 4x4 实测 $6.2\times10^{-13}$ vs $1.9\times10^{-9}$：正规方程把病自乘，$Q$ 保长度不放大） | 列满秩方程；条件数 20 讲 | 第 14 讲 |
| 最小二乘问题定义 $\min\|\vec b-A\vec x\|^2$ | 平方与长度同序（不改变最小点）、展开是二次好解、高斯噪声下等价最大似然（21 讲）；最优 $\hat{\vec x}$ 恒存在 | 任意 $A$；答案只用已教概念 | 第 15 讲 |
| 正规方程 $A^TA\hat{\vec x}=A^T\vec b$ | 最优 $\iff$ 误差垂直列空间 $\iff A^T(\vec b-A\hat{\vec x})=0$；与 13 讲投影同方程两面孔；元素 $=$ 列内积 $=$ 数据求和 | 任意 $A$（恒有解） | 第 15 讲 |
| $\hat{\vec x}=(A^TA)^{-1}A^T\vec b$ | $A$ 列满秩时唯一（$A^TA$ 可逆判定器 13 讲）；奇异时解集 $=\hat{\vec x}_0+N(A^TA)$ 但 $A\hat{\vec x}$、残差、SSE 恒唯一（零空间链条） | 列满秩时直接套；否则勿硬求逆 | 第 15 讲 |
| 残差回归性质 | $\sum e_i=0$（均值零）、$\sum t_ie_i=0$（与自变量不相关）；来自 $A^T\vec e=0$ 逐列翻译（B2） | 直线拟合 $A=[\vec1\ \vec t]$；每题必验 | 第 15 讲 |
| SSE 最小性（勾股版） | $\|\vec b-A\vec x\|^2=\|\vec e\|^2+\|\vec p-A\vec x\|^2\ge\|\vec e\|^2$，等号 $\iff A\vec x=\vec p$；两分解项正交 | 最优性完整证明 | 第 15 讲 |
| 嵌套定律 | $W_1\subseteq W_2\Rightarrow$ 投影距离不增；模型升次 SSE 只降不升（等号也可能成立）；阴暗面 $=$ 过拟合（21 讲） | 子空间嵌套 | 第 15 讲 |
| QR 路线 $R\hat{\vec x}=Q^T\vec b$ | 垂直条件左乘 $Q^T$ 消 $Q$；与 14 讲精确解公式同型；病态拟合实测差 3 个数量级（$2.7\times10^{1}$ vs $2.3\times10^{-2}$） | 上代码/高次/大数据一律此路线 | 第 15 讲 |
