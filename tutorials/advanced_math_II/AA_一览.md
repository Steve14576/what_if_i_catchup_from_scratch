# 高等数学 II（下）：概念、公式与中英对照（字典）

> 本文件是**附录字典**：每条给出完整定义（读者忘了翻回来能重新明白"它到底是什么"），不是用法提示的堆砌；正文不缩写成字典条目，字典也不只甩名字。
> 每条标注：首次出现讲次 + 理解层次（**要会用**（含推导/手算）｜**知道有这回事**（知道是什么 + 何时找它）｜**建立直觉**（辅助理解的路标，不是证明））。
> 随讲增补；第 2 遍回查时批量对账（首次出现讲次、定义、公式条件与正文交叉核对）。

> 当前覆盖：第 01–10 讲。

## 一、概念与术语（中英对照）

| 概念（中文） | 英文/缩写 | 定义（说清是什么） | 首次出现 | 理解层次 |
|---|---|---|---|---|
| 向量（自由向量） | vector (free vector) | 既有大小又有方向的量；用有向线段表示，**起点可平移**（平移后相同的有向线段表同一向量）；与“点”的区别：点=位置，向量=位移与方向 | 第 01 讲 | 要会用 |
| 模、方向余弦、单位向量 | norm / direction cosines / unit vector | $\lvert\mathbf a\rvert=\sqrt{a_x^2+a_y^2+a_z^2}$；方向余弦 $\cos\alpha=a_x/\lvert\mathbf a\rvert$ 等，满足平方和 $=1$；$\mathbf e_a=\mathbf a/\lvert\mathbf a\rvert$（需 $\mathbf a\ne\mathbf 0$） | 第 01 讲 | 要会用 |
| 数量积（点积） | dot product | $\mathbf a\cdot\mathbf b=\lvert\mathbf a\rvert\lvert\mathbf b\rvert\cos\theta=a_xb_x+a_yb_y+a_zb_z$（一个**数**）；管夹角、投影（带符号）、垂直判定；**无结合律**（$(\mathbf a\cdot\mathbf b)\mathbf c$ 是数乘向量） | 第 01 讲 | 要会用 |
| 向量积（叉积） | cross product | $\mathbf a\times\mathbf b$（一个**向量**）：大小 $\lvert\mathbf a\rvert\lvert\mathbf b\rvert\sin\theta$＝平行四边形面积，方向右手定则；坐标式 $(a_yb_z-a_zb_y,a_zb_x-a_xb_z,a_xb_y-a_yb_x)$；**反交换**；管法向量、面积、平行判定 | 第 01 讲 | 要会用 |
| 混合积 | scalar triple product | $(\mathbf a\times\mathbf b)\cdot\mathbf c$（一个数）：绝对值＝平行六面体体积，符号由左右手系定；共面 ⇔ 混合积 $=0$ | 第 01 讲 | 知道有这回事 |
| 符号约定与术语同名（辨析） | notation and terminology | **列向量**：几何向量不分行列，接矩阵时按列（行向量写转置 $\top$）；**点积** $\cdot$ ⇔ 矩阵形式 $\mathbf a^\top\mathbf b$；**叉积**只在三维，矩阵身份 $[\mathbf a]_\times\mathbf b$；**“外积”同名不同物**（物理旧称=叉积；线代 outer product=$\mathbf u\mathbf v^\top$）——本课程不用该词；**模** $\lvert\cdot\rvert$ ⇔ 2-范数 $\lVert\cdot\rVert_2$（数值相同）；$\mathbf e_a$（方向单位向量）与 $\mathbf e_i$（标准基）看下标；**“坐标”两义**：分量 vs 相对基系数（标准基下重合） | 第 01 讲 | 要会用 |
| 平面方程 | plane equation | **点法式** $A(x-x_0)+B(y-y_0)+C(z-z_0)=0$（一点＋法向量）；**一般式** $Ax+By+Cz+D=0$（法向量就是系数 $(A,B,C)$）；**截距式** $\frac xa+\frac yb+\frac zc=1$（截距均存在且非零时）；系数为零 ⇒ 过原点/平行坐标轴 | 第 02 讲 | 要会用 |
| 平面束（简介） | pencil of planes | 过两平面交线的平面族 $\Pi_1+\lambda\Pi_2=0$（不含 $\Pi_2$ 本身）；常用于“过交线且满足某条件”的题 | 第 02 讲 | 要会用 |
| 直线方程 | line equation | **参数式** $M_0+t\mathbf s$（求交点/动点最方便）；**对称式** $\frac{x-x_0}{l}=\frac{y-y_0}{m}=\frac{z-z_0}{n}$（分母为 $0$ ⇒ 对应坐标恒等，不能写成分数）；**一般式**（两平面交线，方向 $=\mathbf n_1\times\mathbf n_2$） | 第 02 讲 | 要会用 |
| 线面角与两直线关系 | angle / skew lines | 线面角 $\sin\theta=\lvert\mathbf s\cdot\mathbf n\rvert/(\lvert\mathbf s\rvert\lvert\mathbf n\rvert)$（与法向夹角互余，**用 sin**）；两直线夹角用 $\lvert\mathbf s_1\cdot\mathbf s_2\rvert$；异面判定 $\lvert(\mathbf s_1\times\mathbf s_2)\cdot\overrightarrow{M_1M_2}\rvert\ne0$（混合积） | 第 02 讲 | 要会用 |
| 曲面方程（隐式/显式） | implicit / explicit surface | 隐式 $F(x,y,z)=0$ 可表示整张曲面；显式 $z=f(x,y)$ 每个 $(x,y)$ 只对应一个 $z$（只能表示单值部分——开方只取一支） | 第 03 讲 | 要会用 |
| 柱面 | cylinder | 母线平行于定直线的曲面；**判据：方程缺哪个变量，母线就平行哪个轴**（$F(x,y)=0$ 母线平行 $z$ 轴）；柱面≠圆柱面（准线可为任意曲线） | 第 03 讲 | 要会用 |
| 旋转面 | surface of revolution | 曲线（母线）绕定直线旋转扫出的曲面；**替换规则**：绕 $z$ 轴 $z$ 不变、$y^2\to x^2+y^2$（其他轴同理）——由“到轴距离不变”而来；开方双支要补范围（锥面是上下两个） | 第 03 讲 | 要会用 |
| 二次曲面五标准型 | quadric surfaces | 椭球 $\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}=1$；椭圆抛物面 $\frac{x^2}{a^2}+\frac{y^2}{b^2}=z$；双曲抛物面 $\frac{x^2}{a^2}-\frac{y^2}{b^2}=z$；单叶/双叶双曲面 $\frac{x^2}{a^2}+\frac{y^2}{b^2}-\frac{z^2}{c^2}=\pm1$；锥面 $\frac{x^2}{a^2}+\frac{y^2}{b^2}=z^2$；**用截痕认图**（水平截 + 竖直截） | 第 03 讲 | 认识层（能认图/说形状） |
| 空间曲线与投影柱面 | space curve / projecting cylinder | 一般式（两曲面交线）与参数式 $\mathbf r(t)$；消去一个变量得**投影柱面**（母线平行该轴），再与坐标面联合得投影曲线 | 第 03 讲 | 要会用 |
| 重极限（二重极限） | double limit | $\lim_{(x,y)\to(x_0,y_0)}f=A$：$\forall\varepsilon\exists\delta$，$0<\sqrt{(x-x_0)^2+(y-y_0)^2}<\delta\Rightarrow\lvert f-A\rvert<\varepsilon$；邻域是**圆盘**、趋近路径**无穷多**、要求所有路径同时趋于同一个值；一元性质（唯一/局部有界/四则）照搬 | 第 04 讲 | 要会用 |
| 路径法 | path test | 两条路径得到不同极限 ⇒ 重极限不存在；**只能证不存在，不能证存在**（无穷多路径未试）；常用反例路径：直线 $y=kx$、抛物线 $y=x^2$；**“直线全试遍”仍可能漏**（$x^2y/(x^4+y^2)$ 例） | 第 04 讲 | 要会用 |
| 极坐标夹逼 | polar coordinates + squeeze | 令 $x=r\cos\theta,y=r\sin\theta$；若 $\lvert f-A\rvert\le g(r)$ 且界**不含 $\theta$**、$g(r)\to0$，则重极限存在为 $A$ | 第 04 讲 | 要会用 |
| 累次极限 | iterated limits | 先对一个变量、再对另一个取极限（两次一元）；**与重极限互不蕴含**：累次都存在但不等、重不存在（$(x^2-y^2)/(x^2+y^2)$）；重存在、累次不存在（$y\sin(1/x)$） | 第 04 讲 | 要会用 |
| 多元连续性 | continuity | $\lim_{(x,y)\to P_0}f=f(P_0)$；初等函数在定义域内连续；沿路径不同值 ⇒ 不连续（**路径型间断**，一元没有这一类）；有界闭区域上最值/介值定理与一元同构 | 第 04 讲 | 要会用 |
| 偏导数 | partial derivative | $f_x(x_0,y_0)=\lim_{\Delta x\to0}\frac{f(x_0+\Delta x,y_0)-f(x_0,y_0)}{\Delta x}$——固定 $y$、对一元求导；几何意义：坐标轴方向截面曲线的切线斜率；**接缝点（原点/分段点）必须回定义**（$\sqrt{x^2+y^2}$ 原点偏导不存在但连续） | 第 05 讲 | 要会用 |
| 可微与全微分 | differentiability / total differential | $\Delta z=A\Delta x+B\Delta y+o(\rho)$（$\rho=\sqrt{\Delta x^2+\Delta y^2}$）；**几何：曲面在一点附近被一个平面逼近**（误差 $o(\rho)$——整个邻域，不只两条轴）；可微则 $A=f_x,B=f_y$、$dz=f_xdx+f_ydy$；**$o(\rho)$ 管所有方向**（不是 $o(\Delta x)+o(\Delta y)$） | 第 05 讲 | 要能推导 |
| 偏导/连续/可微的强弱链 | partials / continuity / differentiability | **偏导连续 ⇒ 可微 ⇒ 连续**、**可微 ⇒ 偏导存在**；反向均有反例：连续⇏偏导存在（$\sqrt{x^2+y^2}$）、偏导存在⇏连续（$xy=0$ 取 1 的分段例）、偏导存在⇏可微（$\sqrt{\lvert xy\rvert}$，沿 $y=x$ 比值恒 $1/\sqrt2$） | 第 05 讲 | 要能推导 |
| 混合偏导 | mixed partials | $f_{xy}$ 与 $f_{yx}$；**二者连续则相等**（定理；考试初等函数默认满足）；存在不相等的反例（不要求记） | 第 05 讲 | 知道有这回事 |
| 多元链式法则 | multivariable chain rule | $z=f(u,v)$、$u,v$ 为 $x,y$ 的函数：**每条从 $z$ 到目标的路径相乘、同一目标相加**（**项数=路径数**）；**多层**（如 $z\to u\to s\to t$）就是多个因子连乘；**变量同时出现在多个层（直接+间接）**时直连项与间接项都要算（$z=f(x,u),u=u(x,y)$：$z_x=f_x+f_uu_x$，$f_x$ 只是直连项而不是 $z_x$）；二阶时 **$f_u,f_v$ 仍是复合函数**，再求导要走链式（$z_{xx}=f_{uu}u_x^2+2f_{uv}u_xv_x+f_{vv}v_x^2+\cdots$） | 第 06 讲 | 要会用 |
| 全导数与形式不变性 | total derivative / invariance | 中间变量全为一元时用 $\dfrac{dz}{dt}=f_u u'+f_v v'$（全导数）；**一阶全微分形式不变**：$dz=f_u du+f_v dv$（不分变量层次；只对一阶成立） | 第 06 讲 | 要会用 |
| 隐函数求导 | implicit differentiation | $F(x,y)=0$：$y'=-F_x/F_y$；$F(x,y,z)=0$：$z_x=-F_x/F_z$、$z_y=-F_y/F_z$（**要求 $F_z\ne0$**）；直接两边求导与公式等价；**几何：$(F_x,F_y)$ 垂直于曲线**（切向量 $(1,y')$ 与之点积为 0）——第 08 讲梯度的伏笔；二阶导需代回并用原方程化简 | 第 06 讲 | 要会用 |
| 隐函数存在条件（简介） | implicit function theorem | $F$ 连续可偏导、$F(P_0)=0$、**$F_z(P_0)\ne0$** ⇒ 邻域内唯一确定 $z=z(x,y)$；$F_z=0$ 处可无单值隐函数（$x^2+y^2+z^2=1$ 赤道、双锥原点） | 第 06 讲 | 知道有这回事 |
| 切平面与法线 | tangent plane / normal line | 曲面 $F(x,y,z)=0$ 在 $P_0$：**法向量 $∇F=(F_x,F_y,F_z)$**（曲面上任意过 $P_0$ 的曲线切向量都与它垂直）；切平面 $F_xΔx+F_yΔy+F_zΔz=0$；法线过 $P_0$ 方向 $∇F$；法向乘 $-1$ 不改变切平面；**显式 $z=f(x,y)$**：法向 $(f_x,f_y,-1)$，切平面 $z-z_0=f_xΔx+f_yΔy$（即 05 讲的局部逼近平面）；边界：$F_z=0$ 时切平面竖直（写不出 $z(x,y)$ 但切平面仍在），$∇F=0$ 时可能无切平面（锥顶） | 第 07 讲 | 要会用 |
| 空间曲线的切线与法平面 | tangent line / normal plane | 曲线 $\mathbf r(t)$ 在 $t_0$：**切向量 $\mathbf T=\mathbf r'(t_0)$**；切线过 $P_0$ 方向 $\mathbf T$；**法平面过 $P_0$ 以 $\mathbf T$ 为法向**（曲线穿过它）；两曲面交线：$\mathbf T=∇F×∇G$，**$∇F∥∇G$ 时叉积为零、可能不光滑** | 第 07 讲 | 要会用 |
| 方向导数 | directional derivative | 沿**单位方向** $\mathbf e=(\cosα,\cosβ)$ 的变化率：$\partial f/\partial l=\lim_{t\to0^+}[f(P_0+t\mathbf e)-f(P_0)]/t$；**必须单位化**（否则值被方向向量长度缩放）；可微时 $=∇f·\mathbf e=f_x\cosα+f_y\cosβ$（三元加 $f_z\cosγ$）；几何：竖直截面曲线的切线斜率；偏导是 $\mathbf e=(1,0),(0,1)$ 的特例 | 第 08 讲 | 要会用 |
| 梯度 | gradient | $∇f=(f_x,f_y)$（或三元）——**向量**；方向导数 $=∇f·\mathbf e=|∇f|\cosθ$：同向取最大 $|∇f|$（**最速上升**）、反向最小 $-|∇f|$（最速下降）、垂直为 $0$；$∇f$ **垂直于等值线/等值面**（指向 $f$ 增大侧），07 讲曲面法向是它的特例（$∇F=∇(f-c)$；显式曲面 $(f_x,f_y,-1)$）；$∇f=0$ 只是一阶平坦（驻点候选，**不是**极值判据） | 第 08 讲 | 要会用 |
| 极值与驻点 | local extremum / stationary point | 极值：邻域内 $f(P)\le f(P_0)$（或 $\ge$），**局部**概念；可微极值点 ⇒ $∇f=0$（驻点）；**候选点 = 驻点 ∪ 偏导不存在的点**（$\sqrt{x^2+y^2}$、$|x|+|y|$ 原点）；驻点不一定是极值（鞍点） | 第 09 讲 | 要会用 |
| 极值判据（$AC-B²$） | second derivative test | $A=f_{xx},B=f_{xy},C=f_{yy},\Delta=AC-B^2$：$\Delta>0,A>0$ 极小；$\Delta>0,A<0$ 极大；$\Delta<0$ 鞍点；$\Delta=0$ 失效（需定义/高阶）；来源：二阶展开的二次型 $Q=Au^2+2Buv+Cv^2$ 配方 | 第 09 讲 | 要会用 |
| 条件极值与乘数法 | Lagrange multipliers | 在 $g=0$ 上找 $f$ 的极值：约束曲线切向上 $∇f$ 的方向导数为 0 且 $∇g⊥$ 切向 ⇒ **$∇f=λ∇g$**，与 $g=0$ 联立；$λ$ 是比例系数（也度量约束敏感度，认识层）；**边界**：$∇g=0$ 的约束点需单独查 | 第 09 讲 | 要会用 |
| 闭区域最值与三步法 | global extrema on a closed region | 有界闭区域上连续 ⇒ 最值存在；最值点只可能在**内部驻点、内部偏导不存在点、边界上**；三步：内部候选 → 边界候选（直线段代入、圆弧参数化、**角点单独代入**）→ 比较函数值；开区域需补边界行为论证（唯一驻点不自动是全局最值） | 第 10 讲 | 要会用 |

## 二、公式

| 公式 | 符号各指什么 | 适用条件 | 出处讲次 |
|---|---|---|---|
| 方向余弦平方和：$\cos^2\alpha+\cos^2\beta+\cos^2\gamma=1$ | $\alpha,\beta,\gamma$ 为与三坐标轴的夹角 | 任意非零向量 | 第 01 讲 |
| 数量积：$\mathbf a\cdot\mathbf b=a_xb_x+a_yb_y+a_zb_z=\lvert\mathbf a\rvert\lvert\mathbf b\rvert\cos\theta$ | $\theta\in[0,\pi]$ 为夹角 | 任意向量 | 第 01 讲 |
| 投影：$\operatorname{Prj}_{\mathbf b}\mathbf a=\dfrac{\mathbf a\cdot\mathbf b}{\lvert\mathbf b\rvert}$ | 带符号标量（可负） | $\mathbf b\ne\mathbf 0$ | 第 01 讲 |
| 向量积：$\mathbf a\times\mathbf b=(a_yb_z-a_zb_y,\ a_zb_x-a_xb_z,\ a_xb_y-a_yb_x)$ | 分量按循环次序减 | 任意向量；$\mathbf a\times\mathbf a=0$ | 第 01 讲 |
| 混合积：$(\mathbf a\times\mathbf b)\cdot\mathbf c=\lvert\mathbf a,\mathbf b,\mathbf c\rvert$（三阶行列式） | 行＝三向量的坐标 | 共面 ⇔ 行列式 $=0$ | 第 01 讲 |
| 点到平面距离：$d=\dfrac{\lvert Ax_0+By_0+Cz_0+D\rvert}{\sqrt{A^2+B^2+C^2}}$ | $P(x_0,y_0,z_0)$；平面 $Ax+By+Cz+D=0$ | 任意平面（系数不全为 0） | 第 02 讲 |
| 两平面夹角：$\cos\theta=\dfrac{\lvert\mathbf n_1\cdot\mathbf n_2\rvert}{\lvert\mathbf n_1\rvert\lvert\mathbf n_2\rvert}$ | $\theta\in[0,\frac\pi2]$ | 分子取绝对值（锐角） | 第 02 讲 |
| 线面角：$\sin\theta=\dfrac{\lvert\mathbf s\cdot\mathbf n\rvert}{\lvert\mathbf s\rvert\lvert\mathbf n\rvert}$ | $\mathbf s$ 直线方向、$\mathbf n$ 平面法向 | 注意是 $\sin$（与法向夹角互余） | 第 02 讲 |
| 点到直线距离：$d=\dfrac{\lvert\overrightarrow{M_0P}\times\mathbf s\rvert}{\lvert\mathbf s\rvert}$ | $M_0$ 直线上一点，$\mathbf s$ 方向 | 平行四边形面积除以底（简介） | 第 02 讲 |
| 旋转面替换：绕 $z$ 轴 $z$ 不变、$y^2\to x^2+y^2$；绕 $x$ 轴 $x$ 不变、$y^2\to y^2+z^2$；绕 $y$ 轴 $y$ 不变、$x^2\to x^2+z^2$ | 母线在含轴的坐标面内；只换平方项 | 母线方程只含轴坐标与到轴的距离平方 | 第 03 讲 |
| 重极限的夹逼判据：$\lvert f(r\cos\theta,r\sin\theta)-A\rvert\le g(r)$，$g(r)\to0$ | $g$ 只依赖 $r$（**不含 $\theta$**） | 极坐标将 $(x,y)\to(0,0)$ 化为 $r\to0$ | 第 04 讲 |
| 全微分：$dz=f_x(x,y)\,dx+f_y(x,y)\,dy$ | $f_x,f_y$ 为偏导 | 可微时成立（初等函数在定义域内可微；分段/接缝点需验 $o(\rho)$） | 第 05 讲 |
| 链式法则：$z_x=f_u u_x+f_v v_x$；$z_y=f_u u_y+f_v v_y$ | $f_u,f_v$ 为对位置变量的偏导 | $u,v$ 可微；项数=路径数 | 第 06 讲 |
| 隐函数：$y'=-\dfrac{F_x}{F_y}$；$z_x=-\dfrac{F_x}{F_z}$，$z_y=-\dfrac{F_y}{F_z}$ | $F_x,F_y,F_z$ 为对各自变量的偏导 | 分母不为 $0$（$F_y\ne0$ / $F_z\ne0$） | 第 06 讲 |
| 切平面：$F_x(x-x_0)+F_y(y-y_0)+F_z(z-z_0)=0$；显式 $z-z_0=f_x(x-x_0)+f_y(y-y_0)$ | $F_x,F_y,F_z$ 在 $P_0$ 取值；显式 $f_x,f_y$ 在 $(x_0,y_0)$ 取值 | $∇F(P_0)\ne0$；显式需 $f$ 可微 | 第 07 讲 |
| 法线：$\dfrac{x-x_0}{F_x}=\dfrac{y-y_0}{F_y}=\dfrac{z-z_0}{F_z}$ | 分母为 0 时该坐标恒定（与 02 讲对称式同读法） | $∇F(P_0)\ne0$ | 第 07 讲 |
| 曲线切线：$\dfrac{x-x_0}{x'(t_0)}=\dfrac{y-y_0}{y'(t_0)}=\dfrac{z-z_0}{z'(t_0)}$；法平面：$x'Δx+y'Δy+z'Δz=0$ | $x',y',z'$ 在 $t_0$ 取值 | $\mathbf r'(t_0)\ne\mathbf 0$（否则切向不定） | 第 07 讲 |
| 交线切向：$\mathbf T=∇F×∇G$ | $∇F,∇G$ 在交点取值 | $∇F$ 与 $∇G$ 不平行（否则退化为零向量） | 第 07 讲 |
| 方向导数：$\dfrac{\partial f}{\partial l}=f_x\cosα+f_y\cosβ=∇f·\mathbf e$ | $(\cosα,\cosβ)$ 为单位方向；三元加 $f_z\cosγ$ | **可微时成立**；方向导数都存在也不保证公式成立（$\sqrt{\lvert xy\rvert}$） | 第 08 讲 |
| 最速上升：方向 $\dfrac{∇f}{\lvert∇f\rvert}$，最大变化率 $\lvert∇f\rvert$ | $∇f≠0$ | 梯度非零；反向为最速下降 | 第 08 讲 |
| 极值判据：$\Delta=AC-B^2$（$A=f_{xx},B=f_{xy},C=f_{yy}$） | $\Delta>0,A>0$ 极小；$\Delta>0,A<0$ 极大；$\Delta<0$ 鞍点；$\Delta=0$ 失效 | 二阶偏导存在且连续；$\Delta>0$ 时看 $A$ | 第 09 讲 |
| 拉格朗日：$∇f=λ∇g$，联立 $g=0$ | $λ$ 为乘数；三元加 $f_z=λg_z$；多约束 $∇f=λ∇g+μ∇h$ | $∇g≠0$（否则约束奇异需单独查） | 第 09 讲 |
