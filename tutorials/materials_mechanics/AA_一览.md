# 材料力学——附录：关键概念·公式·中英对照字典（AA）

> 本文件是全课程的**字典**：条条给完整、自足的定义，不重复正文的铺垫与推导。每讲交付后增量增补；编号固定 `AA_`，永不重排。
> 使用方式：复习时按表扫读；写作业时若不确定某术语的严格含义，回这里对定义（正文不许退化成甩条目，本表也不许退化成只甩名字）。

## 一、概念与术语（中英对照）

| 概念（中文） | 英文/缩写 | 定义（说清"是什么"） | 首次出现 | 理解层次 |
|---|---|---|---|---|
| 材料力学 | Mechanics of Materials | 研究变形固体（主要是杆件）在外力作用下的应力、应变与变形，回答强度、刚度、稳定性问题的学科 | 第 01 讲 | 要能说清研究什么 |
| 强度 | strength | 构件抵抗破坏（断裂、屈服、疲劳断裂等）的能力；判据是应力不超过材料承受上限 | 第 01 讲 | 要能复述 |
| 刚度 | stiffness | 构件抵抗变形的能力；判据是变形不超过允许值 | 第 01 讲 | 要能复述 |
| 稳定性 | stability | 受压细长构件保持原有平衡形式、不突然失稳（侧向弯折）的能力 | 第 01 讲 | 要能复述 |
| 杆件 | bar / rod / member | 一个方向尺寸（长度）远大于另外两个方向（横截面尺寸）的构件；本课程主要研究对象 | 第 01 讲 | 识别 |
| 板壳 | plate & shell | 两个方向尺寸大、一个方向（厚度）小的构件，如楼板、压力容器壁 | 第 01 讲 | 识别 |
| 块体 | block / body | 三个方向尺寸相差不多、无长度优势的构件，如地基、水坝 | 第 01 讲 | 识别 |
| 变形固体 | deformable solid | 受力后会发生变形的物体；与"受力不变形的刚体"相对，是材料力学的研究对象 | 第 01 讲 | 要能辨析 |
| 刚体 | rigid body | 受力后形状与尺寸完全不变的理想物体（理论力学的研究对象）；材料力学不采用 | 第 01 讲 | 识别 |
| 连续性假设 | assumption of continuity | 假设材料毫无空隙地充满构件；使力与变形可用连续函数描述、微积分可用 | 第 01 讲 | 知道为何需要 |
| 均匀性假设 | assumption of homogeneity | 假设构件各处材料性质相同；使材料性能可用一组统一常数描述 | 第 01 讲 | 知道为何需要 |
| 各向同性假设 | assumption of isotropy | 假设材料沿各个方向力学性质相同；使应力与变形关系与方向无关（金属近似成立，木材/复合材料不成立） | 第 01 讲 | 知道适用边界 |
| 小变形假设 | assumption of small deformation | 假设变形量远小于构件尺寸；使可在原始尺寸上列平衡方程、并允许效果叠加（后面叠加法的依据） | 第 01 讲 | 焊成直觉（结论前提） |
| 外力 | external force | 外界作用在构件上的力；按范围分体积力/表面力，按分布分集中力/分布力，按变化快慢分静载荷/动载荷 | 第 01 讲 | 识别分类 |
| 体积力 | body force | 连续作用在构件内每个质点上的力，如重力、惯性力 | 第 01 讲 | 认识 |
| 表面力 | surface force | 作用在构件表面上的力，如压力、接触力 | 第 01 讲 | 认识 |
| 分布力 | distributed force | 沿长度或面积连续分布的力，如均布载荷 | 第 01 讲 | 认识 |
| 集中力 | concentrated force | 把力理想化地集中于一点的载荷形式 | 第 01 讲 | 认识 |
| 静载荷 | static load | 缓慢施加、大小方向基本不变（或变化很慢）的载荷 | 第 01 讲 | 识别 |
| 动载荷 | dynamic load | 加载过程伴随加速度或惯性的载荷（如冲击）；第 20 讲专门处理 | 第 01 讲 | 识别 |
| 内力 | internal force | 外力施加后，构件内部各部分之间为抵抗变形而产生的附加相互作用力；由外力诱发、去除外力即消失，非固有 | 第 01 讲 | 要能复述、破除"固有"误解 |
| 截面法 | method of sections | 求内力的方法：在所求位置假想切开构件，留下一部分，用内力代替被切去部分的作用，再列平衡方程解出内力（截、取、代、平四步） | 第 01 讲 | 要能闭眼执行 |
| 应力 | stress | 内力在截面某点处的集度（单位面积上的内力）；$\sigma = \lim_{\Delta A\to0}\Delta F/\Delta A$，是逐点的量 | 第 01 讲 | 要能复述、知道是"点"的量 |
| 正应力 | normal stress（σ） | 垂直于截面（沿法线方向）的应力分量，表现为把截面拉开或压紧 | 第 01 讲 | 要能判读 |
| 切应力 | shear stress（τ） | 平行于截面（沿切向）的应力分量，表现为使截面两侧错动 | 第 01 讲 | 要能判读 |
| 平均应力 | average stress | 用总内力除以截面面积得到的应力（$\sigma = N/A$）；仅在应力沿截面均匀分布时才等于逐点应力 | 第 01 讲 | 知道其适用条件 |
| 应变 | strain | 描述变形程度的量；线应变为单位长度上的变形，切应变为直角的改变量；无量纲（切应变用弧度） | 第 01 讲 | 要能复述 |
| 线应变（正应变） | normal strain（ε） | 单位长度上的伸长（缩）量：$\varepsilon = \Delta L/L$；伸长为正、缩短为负、无量纲 | 第 01 讲 | 要会算 |
| 切应变（剪应变） | shear strain（γ） | 原相互垂直的两线段受力后夹角发生的改变量，以弧度计 | 第 01 讲 | 要能复述 |
| 基本变形形式 | basic deformation forms | 杆件的四种基本变形：轴向拉压、剪切、扭转、弯曲 | 第 01 讲 | 能认、能对号 |
| 组合变形 | combined deformation | 两种以上基本变形同时发生的变形；处理办法是拆成基本变形分别算再叠加（第 16 讲正式讲） | 第 01 讲（首提） | 知道有这回事；第 16 讲展开 |
| 内力图 | internal force diagram | 沿杆长表示各截面内力变化的图（轴力图/扭矩图/剪力图/弯矩图）；本讲只用符号、后续各讲展开 | 第 01 讲（首提） | 认识；后续讲次正式作 |
| 轴向拉伸与压缩 | axial tension / compression | 外力合力沿杆轴线、杆沿轴线伸长（压短）的受力与变形形式；横截面上只有正应力 | 第 02 讲 | 识别 |
| 轴力 | axial force（normal force, N） | 横截面上沿杆轴线方向的内力分量；拉为正、压为负 | 第 02 讲 | 要会求、会定号 |
| 轴力图 | axial force diagram | 沿杆长表示各截面轴力 $N$ 的图；集中力处突变，跳跃量等于该处集中力的代数值 | 第 02 讲 | 要会作、会自检 |
| 平面假设 | plane assumption（plane sections remain plane） | 变形前为平面的横截面，变形后仍是平面（且垂直于轴线）；是"轴向拉压应力均匀"的依据 | 第 02 讲 | 要能复述其作用 |
| 圣维南原理 | Saint-Venant's principle | 加力方式的具体细节只影响加力点附近；远离加力点（超过横截面尺寸量级）后应力分布趋于均匀 | 第 02 讲 | 认识层：知道适用边界 |
| 斜截面应力 | stress on an inclined section | 与横截面成夹角 $\alpha$ 的斜面上的应力：正应力 $\sigma_\alpha=\sigma\cos^2\alpha$、切应力 $\tau_\alpha=\frac{\sigma}{2}\sin2\alpha$ | 第 02 讲 | 要会推导、会算 |
| 危险截面 | critical section | 应力最大的截面（等直杆取 $\lvert N\rvert$ 最大处、变截面取 $\lvert N\rvert/A$ 最大处）；破坏最可能从这里开始 | 第 02 讲 | 要会判断 |
| 应力集中 | stress concentration | 截面突变处（孔、槽、台阶）局部应力显著高于 $N/A$ 平均值的现象 | 第 02 讲（认识层） | 认识；第 03 讲展开 |
| 理论应力集中系数 | theoretical stress concentration factor（K） | $K=\sigma_{\max}/\sigma_{\text{名义}}$，$\sigma_{\text{名义}}$ 按净截面平均应力算；通常 $K>1$ | 第 02 讲（认识层） | 认识 |
| 切应力互等定理 | theorem of complementary shear stresses | 过同一点、相互垂直的两个面上切应力大小相等，方向都指向（或都背离）两面的交线 | 第 02 讲（伏笔） | 知道有这回事；第 13 讲展开 |
| 胡克定律 | Hooke's law | 线弹性范围内正应力与线应变成正比：$\sigma=E\varepsilon$（等价 $\Delta L=NL/(EA)$） | 第 03 讲 | 要能推导、会算，知道边界 |
| 弹性模量 | elastic modulus（Young's modulus, E） | $\sigma=E\varepsilon$ 中的比例常数；材料的"硬"度指标，越大越难变形；单位 MPa | 第 03 讲 | 要能复述、会用 |
| 拉压刚度 | tensile stiffness（EA） | 弹性模量与横截面积的乘积，衡量杆抵抗拉压变形的能力；越大越难拉长 | 第 03 讲 | 要能解释 |
| 泊松比 | Poisson's ratio（μ） | 横向线应变与轴向线应变之比取正：$\varepsilon'=-\mu\varepsilon$；各向同性材料 $0<\mu<0.5$，金属约 0.25~0.35 | 第 03 讲 | 要会算横向变形 |
| 体积应变 | volumetric strain（θ） | 单位体积的相对变化（三向线应变之和）；单向拉伸 $\theta=\frac{1-2\mu}{E}\sigma$，$\mu=0.5$（不可压缩）时 $\theta=0$ | 第 03 讲（引）、第 14 讲（正式） | 第 03 讲知道上界来历；第 14 讲展开 |
| 比例极限 | proportional limit（σ_p） | $\sigma$ 与 $\varepsilon$ 保持正比（胡克定律成立）的上限应力 | 第 03 讲 | 要能识别 |
| 弹性极限 | elastic limit（σ_e） | 卸载后变形完全恢复的上限应力；与 $\sigma_p$ 相近 | 第 03 讲 | 识别 |
| 屈服极限 | yield limit（yield strength, σ_s） | 屈服阶段对应的应力（应力不增、应变猛增）；塑性材料的强度指标 | 第 03 讲 | 要能识别、会取值 |
| 强度极限 | ultimate strength（σ_b） | 拉伸曲线的最高点应力（材料能承受的最大应力） | 第 03 讲 | 要能识别 |
| 塑性材料 | ductile material | 断裂前塑性变形较大（延伸率 $\delta>约 5\%$）的材料，如低碳钢；拉压性能接近、对应力集中不敏感 | 第 03 讲 | 要能判别 |
| 脆性材料 | brittle material | 塑性变形很小就脆断的材料，如铸铁、混凝土；抗压远强于抗拉、对应力集中敏感 | 第 03 讲 | 要能判别 |
| 延伸率 | elongation（δ） | 断裂时试件标距内的残余伸长率；判塑性/脆性的指标 | 第 03 讲 | 认识层 |
| 冷作硬化 | cold working | 预塑性变形后材料比例极限升高、塑性下降的现象 | 第 03 讲（认识层） | 认识 |
| 极限应力 | ultimate stress（σ_u） | 材料能承受的极限应力取值：塑性材料取 $\sigma_s$、脆性材料取 $\sigma_b$ | 第 03 讲 | 要能取值 |
| 许用应力 | allowable stress（[σ]） | 极限应力折减安全系数后的允许应力：$[\sigma]=\sigma_u/n$ | 第 03 讲 | 要会算 |
| 安全系数 | factor of safety（n） | 大于 1 的折减系数，覆盖载荷估计误差、材料不均匀、计算简化等不确定因素 | 第 03 讲 | 要能复述作用 |
| 连接件 | connector / fastener | 用来连接两个零件的构件（铆钉、螺栓、键、销）；主要发生剪切与挤压破坏 | 第 04 讲 | 识别 |
| 剪切 | shear | 一对相距很近、方向相反的外力使构件相邻截面相互错动的受力形式 | 第 04 讲 | 要能复述 |
| 剪切面 | shear plane | 连接件内部被剪开的横截面（单剪 1 个、双剪 2 个） | 第 04 讲 | 要会辨认、数清 |
| 名义切应力 | nominal shear stress（τ） | 剪力除以剪切面面积的平均切应力：$\tau=Q/A_s$ | 第 04 讲 | 要会算 |
| 挤压 | bearing | 连接件与孔壁（或被连接件）接触面上被局部压溃的现象 | 第 04 讲 | 要能复述 |
| 挤压面 | bearing surface | 连接件与被连接件的接触面（圆铆钉为半圆柱面） | 第 04 讲 | 要会辨认 |
| 名义挤压应力 | nominal bearing stress（σ_bs） | 挤压力除以投影面积的平均挤压应力：$\sigma_{bs}=F/(d\,t)$ | 第 04 讲 | 要会算 |
| 实用计算 | engineering / practical calculation | 用简单统一的名义口径（平均应力、投影面积）替代复杂精确分析的工程方法 | 第 04 讲 | 要能解释其含义与边界 |
| 单剪 / 双剪 | single / double shear | 连接件受剪截面数为 1 / 2 的接头形式 | 第 04 讲 | 要会区分 |
| 平键 | parallel key（flat key） | 嵌在轴与轮毂键槽间、靠侧面传递扭矩的连接件；受剪切与挤压 | 第 04 讲 | 要会算 |
| 外力偶矩 | applied torque（M） | 作用在轴上、绕轴线方向的力偶矩；与功率、转速由 $M=9550P/n$ 联系 | 第 05 讲 | 要会换算 |
| 扭矩 | torque（T） | 横截面上的内力偶矩（绕轴线的内力偶矩）；符号用右手螺旋定 | 第 05 讲 | 要会求、会定号 |
| 扭矩图 | torque diagram | 沿轴长表示各截面扭矩 $T$ 的图；集中外力偶矩处突变，跳跃量等于该处外力偶矩 | 第 05 讲 | 要会作 |
| 圆轴扭转 | torsion of a circular shaft | 外力偶矩绕轴线使圆轴各横截面绕轴相对转动的变形 | 第 05 讲 | 识别 |
| 剪切胡克定律 | Hooke's law in shear | 线弹性范围内切应力与切应变成正比：$\tau=G\gamma$ | 第 05 讲 | 要能复述、会用 |
| 剪切模量 | shear modulus（G） | $\tau=G\gamma$ 中的比例常数（材料常数）；$G=E/[2(1+\mu)]$ | 第 05 讲 | 要能复述 |
| 极惯性矩 | polar moment of inertia（I_p） | 横截面对形心的 $\int\rho^2\,\mathrm{d}A$；实心圆 $I_p=\pi d^4/32$ | 第 05 讲 | 要会算 |
| 抗扭截面系数 | torsional section modulus（W_t） | $I_p/(d/2)$；实心圆 $W_t=\pi d^3/16$；$\tau_{\max}=T/W_t$ | 第 05 讲 | 要会算 |
| 纯剪切应力状态 | pure shear stress state | 只有切应力、没有正应力的应力状态（切应力互等的直接结果） | 第 05 讲（引） | 知道；第 13 讲展开 |
| 扭转角 | angle of twist（φ） | 圆轴两端面相对转过的角度：$\varphi=TL/(GI_p)$（rad） | 第 06 讲 | 要会算 |
| 单位长度扭转角 | angle of twist per unit length（θ） | 每单位长度的扭转角：$\theta=\varphi/L=T/(GI_p)$；常用度/米（$^\circ/\mathrm{m}$） | 第 06 讲 | 要会算、会判 |
| 扭转刚度 | torsional rigidity（GI_p） | 剪切模量与极惯性矩的乘积，抵抗扭转变形的能力（对应拉压刚度 $EA$） | 第 06 讲 | 要能解释 |
| 刚度条件（扭转） | stiffness condition (torsion) | $\theta_{\max}=T/(GI_p)\le[\theta]$（或 $\varphi\le[\varphi]$） | 第 06 讲 | 要会用 |
| 空心轴 | hollow shaft | 内径 $d_0$、外径 $D$ 的圆环截面轴；$I_p=\pi(D^4-d_0^4)/32$；把低应力材料移到外缘 | 第 06 讲 | 要会算、会比较 |
| 内外径比 | ratio of inner to outer diameter（α） | $\alpha=d_0/D$；衡量空心轴的"挖空程度" | 第 06 讲 | 认识 |
| 翘曲 | warping | 非圆截面扭转后横截面不再保持平面、发生凹凸的现象（非圆不能用圆轴公式的根本原因） | 第 06 讲（认识层） | 知道 |
| 静矩 | first moment of area（S_z） | 面积对某轴的面积矩：$S_z=\int_A y\,\mathrm{d}A$；对形心轴的静矩为零 | 第 07 讲 | 要会算 |
| 形心 | centroid（C） | 截面的几何中心：$y_c=S_z/A=\int_A y\,\mathrm{d}A/A$；组合截面 $y_c=\sum A_iy_i/\sum A_i$ | 第 07 讲 | 要会求 |
| 惯性矩 | second moment of area（I_z、I_y） | 面积乘以其到轴距离平方的积分：$I_z=\int_A y^2\,\mathrm{d}A$；恒正，描述抗弯能力 | 第 07 讲 | 要会算 |
| 惯性半径 | radius of gyration（i） | $i=\sqrt{I/A}$，把惯性矩折算成的一个长度 | 第 07 讲 | 要会算 |
| 平行移轴定理 | parallel-axis theorem | $I_z=I_{z_c}+a^2 A$（从形心轴移向平行轴）；矩形对底边 $bh^3/3$ | 第 07 讲 | 要会用、会推导 |
| 惯性积 | product of inertia（I_yz） | $\int_A yz\,\mathrm{d}A$；描述截面相对坐标轴的不对称程度；转轴分析用 | 第 07 讲（认识层） | 认识 |
| 主惯性轴 | principal axes of inertia | 使惯性积为零的一对正交轴；截面的对称轴即主惯性轴 | 第 07 讲（认识层） | 认识 |
| 梁 | beam | 以弯曲为主要变形的杆件；常见简支/悬臂/外伸梁 | 第 08 讲 | 识别 |
| 简支梁 | simply supported beam | 一端铰支、一端滚支的梁（静定） | 第 08 讲 | 识别 |
| 悬臂梁 | cantilever beam | 一端固定、另一端自由的梁 | 第 08 讲 | 识别 |
| 剪力 | shear force（Q） | 横截面内垂直于梁轴线的内力；使微元顺时针转动为正（左上右下） | 第 08 讲 | 要会算、会定号 |
| 弯矩 | bending moment（M） | 横截面内的内力偶；使梁下凸（下部受拉）为正 | 第 08 讲 | 要会算、会定号 |
| 剪力图 | shear force diagram | 沿梁长表示剪力 $Q(x)$ 的图；集中力处突变 | 第 08 讲 | 要会作 |
| 弯矩图 | bending moment diagram | 沿梁长表示弯矩 $M(x)$ 的图；$Q=0$ 处取极值 | 第 08 讲 | 要会作 |
| 分布载荷 | distributed load（q） | 沿梁长连续分布的载荷（如自重），单位 N/m | 第 08 讲 | 识别 |
| 控制截面法 | control-section method | 用微分关系 + 控制截面快速作内力图的方法 | 第 08 讲 | 要会用 |
| 纯弯曲 | pure bending | 剪力为零、弯矩为常数的梁段 | 第 09 讲 | 识别 |
| 横力弯曲 | transverse bending | 横截面上同时有剪力与弯矩的弯曲 | 第 09 讲 | 识别 |
| 中性轴 | neutral axis | 横截面上正应力为零的轴；过形心；弯曲正应力沿其作线性分布 | 第 09 讲 | 要会定、会用 |
| 中性层 | neutral surface | 梁内长度不变的一层（含中性轴的纵向面） | 第 09 讲 | 识别 |
| 弯曲正应力 | bending normal stress | 弯矩引起的横截面正应力：$\sigma=My/I_z$；正负表示拉压 | 第 09 讲 | 要会算、会判拉压 |
| 抗弯截面系数 | section modulus in bending（W_z） | $W_z=I_z/y_{\max}$；$\sigma_{\max}=M/W_z$ | 第 09 讲 | 要会算 |
| 弯曲切应力 | bending shear stress（τ） | 剪力引起的横截面切应力：$\tau=Q S_z^*/(I_z b)$；中性轴最大、外缘为零 | 第 10 讲 | 要会算 |
| 面积静矩 S_z* | first moment of area of the cut-off part | 所求点以外（切到边缘）那部分面积对中性轴的静矩；随所求点位置变化 | 第 10 讲 | 要会算 |
| 挠度 | deflection（w） | 梁横截面形心沿竖向的位移；本课取向上为正（下挠为负，工程常指其大小） | 第 11 讲 | 要会算 |
| 转角 | slope / angle of rotation（θ） | 横截面绕自身转过的角：$\theta=\mathrm{d}w/\mathrm{d}x$ | 第 11 讲 | 要会算 |
| 挠曲线 | deflection curve | 梁变形后轴线弯成的曲线 | 第 11 讲 | 识别 |
| 挠曲线近似微分方程 | approximate differential equation of the deflection curve | $EI_z\,w''=M(x)$；适用线弹性 + 小变形 | 第 11 讲 | 要会用 |
| 边界条件 / 连续条件 | boundary / continuity conditions | 定积分常数的物理条件（支座处 $w$、$w'$；分段处 $w$、$w'$ 连续） | 第 11 讲 | 要会用 |
| 叠加法（求挠度） | method of superposition | 多载荷时分别求挠度再相加（前提：线弹性、小变形） | 第 11 讲 | 要会用 |
| 静定 | statically determinate | 未知反力数 = 独立平衡方程数的结构，反力可由平衡唯一求出 | 第 12 讲 | 识别 |
| 超静定 | statically indeterminate | 未知反力数 > 平衡方程数；反力还依赖刚度 | 第 12 讲 | 要能判断 |
| 多余约束 | redundant constraint | 超出维持平衡所必需的约束 | 第 12 讲 | 要能识别 |
| 超静定次数 | degree of static indeterminacy | 多余约束数 = 反力数 − 平衡方程数 | 第 12 讲 | 要会数 |
| 静定基 | primary (determinate) structure | 去掉多余约束后得到的静定结构；变形比较法的分析对象 | 第 12 讲 | 要会取 |
| 变形比较法 | method of deformation comparison | 用"静力平衡 + 变形协调 + 物理关系"解超静定的方法 | 第 12 讲 | 要会用 |
| 变形协调条件 | deformation compatibility condition | 多余约束处位移须满足的实际条件（常为"位移为零"） | 第 12 讲 | 要会写 |
| 温度应力 | thermal stress | 温度变化被约束阻止而产生的应力：$\sigma=-E\alpha\Delta T$ | 第 12 讲 | 要会算 |
| 装配应力 | assembly stress | 尺寸误差强制装配引起的应力：$\sigma=E\delta/L$ | 第 12 讲 | 要会算 |
| 线膨胀系数 | coefficient of linear thermal expansion（α） | 单位温升引起的单位长度伸长，单位 $1/^\circ\mathrm{C}$ | 第 12 讲 | 会用 |
| 一点的应力状态 | stress state at a point | 过一点所有方向截面上应力的总称；由单元体描述 | 第 13 讲 | 要理解 |
| 单元体 | infinitesimal element | 围绕一点取的无穷小正六面体，用以表示应力状态 | 第 13 讲 | 要会画 |
| 平面应力状态 | plane stress state | 单元体仅有两个方向正应力与一个切应力（$\sigma_x,\sigma_y,\tau_{xy}$）的状态 | 第 13 讲 | 要会判 |
| 斜截面应力 σ_α、τ_α | stresses on an inclined plane | 法线与 $x$ 成 $\alpha$ 的截面上的正应力与切应力 | 第 13 讲 | 要会算 |
| 主平面 | principal plane | 切应力为零的截面 | 第 13 讲 | 要会定 |
| 主应力 | principal stress | 主平面上的正应力 $\sigma_1$、$\sigma_2$（一点的正应力极值） | 第 13 讲 | 要会算 |
| 最大切应力 | maximum shear stress（τ_max） | 一点的最大切应力 $\tau_{\max}=R=(\sigma_1-\sigma_2)/2$，与主平面成 45° | 第 13 讲 | 要会算 |
| 应力圆（莫尔圆） | Mohr's circle | 以 $(C,0)$ 为圆心、$R$ 为半径的圆；点与斜截面一一对应（转 2α） | 第 13 讲 | 要会用 |
| 三向应力状态 | triaxial stress state | 三个方向都有应力（主应力 $\sigma_1\ge\sigma_2\ge\sigma_3$）的应力状态 | 第 14 讲 | 要会判 |
| 广义胡克定律 | generalized Hooke's law | 三向应力下应变与应力的关系：$\varepsilon_x=[\sigma_x-\mu(\sigma_y+\sigma_z)]/E$ 等 | 第 14 讲 | 要会用 |
| 体积应变 | volumetric strain（θ） | 单位体积的体积改变：$\theta=\varepsilon_x+\varepsilon_y+\varepsilon_z$ | 第 14 讲 | 要会算 |
| 弹性常数关系 E-G-μ | relation among elastic constants | 各向同性材料只有两个独立弹性常数：$G=E/[2(1+\mu)]$ | 第 14 讲 | 要会用 |
| 平面应变 | plane strain | $\varepsilon_z=0$ 的状态（区别于平面应力） | 第 14 讲 | 识别 |
| 体积模量 | bulk modulus | 体积应力与体积应变之比，$K=E/[3(1-2\mu)]$ | 第 14 讲 | 认识 |
| 强度理论 | strength theory | 用破坏原因假设把复杂应力折算为相当应力的判据体系 | 第 15 讲 | 要理解 |
| 相当应力 | equivalent stress（σ_r） | 按强度理论折算出的等效单向应力；判据 $\sigma_r\le[\sigma]$ | 第 15 讲 | 要会算 |
| 第一强度理论 | maximum normal stress theory | 最大拉应力理论：$\sigma_{r1}=\sigma_1$（脆性断裂） | 第 15 讲 | 要会算 |
| 第二强度理论 | maximum normal strain theory | 最大伸长线应变理论：$\sigma_{r2}=\sigma_1-\mu(\sigma_2+\sigma_3)$（脆性） | 第 15 讲 | 要会算 |
| 第三强度理论 | maximum shear stress theory | 最大切应力理论：$\sigma_{r3}=\sigma_1-\sigma_3$（塑性屈服；最保守） | 第 15 讲 | 要会算 |
| 第四强度理论 | distortion energy theory | 畸变能密度理论：$\sigma_{r4}=\sqrt{\frac{1}{2}\sum(\sigma_i-\sigma_j)^2}$（塑性；更精确） | 第 15 讲 | 要会算 |
| 薄壁圆筒 | thin-walled cylinder | 受内压的薄壁容器：$\sigma_\theta=\dfrac{pD}{2t}$、$\sigma_z=\dfrac{pD}{4t}$（二向应力状态） | 第 15 讲 | 要会算 |
| 组合变形 | combined loading | 两种以上基本变形同时出现的变形形式 | 第 16 讲 | 要会处理 |
| 偏心拉压 | eccentric axial loading | 轴力偏离形心的拉压；等效为轴力 + 弯矩 | 第 16 讲 | 要会算 |
| 截面核心 | core of a section | 偏心力作用点落于其中时全截面不出现拉应力的区域 | 第 16 讲 | 要会定 |
| 斜弯曲 | unsymmetrical (skew) bending | 载荷不过形心主轴时的两个平面弯曲叠加（认识层，取角点） | 第 16 讲 | 认识 |
| 压杆稳定 | column stability | 压杆保持直线平衡形式的能力；失效形式为失稳 | 第 17 讲 | 要理解 |
| 失稳 | buckling | 压力超过临界力时压杆突然侧向弯折 | 第 17 讲 | 要理解 |
| 临界力 | critical load（P_cr） | 压杆由稳定转为不稳定的压力上限 | 第 17 讲 | 要会算 |
| 长度系数 | effective length factor（μ） | 反映支座约束对临界力的影响（1 / 2 / 0.5 / 0.7） | 第 17 讲 | 要会取 |
| 柔度 | slenderness ratio（λ） | $\lambda=\mu L/i$（长细比）；压杆稳定问题的唯一无量纲参数 | 第 17 讲 | 要会算 |
| 大柔度 / 中柔度 / 小柔度杆 | long / intermediate / short column | 按 $\lambda$ 分类，分别用欧拉公式 / 直线公式 / 强度条件 | 第 17 讲 | 要会判 |
| 折减系数 | reduction factor（φ） | 稳定校核的简化系数：$\sigma\le\varphi[\sigma]$ | 第 17 讲 | 会用 |
| 应变能 | strain energy（V_ε） | 弹性体因变形储存的能量：$V_\varepsilon=\frac{1}{2}F\Delta$（缓慢加载） | 第 18 讲 | 要会算 |
| 外力功 | work of external forces（W） | 载荷缓慢加载所做的功 $W=\frac{1}{2}F\Delta$ | 第 18 讲 | 要会算 |
| 功的互等定理 | reciprocal work theorem | $F_1\delta_{12}=F_2\delta_{21}$ | 第 18 讲 | 要理解 |
| 位移互等定理 | reciprocal displacement theorem | $\delta_{12}=\delta_{21}$（单位力下） | 第 18 讲 | 要会用 |
| 单位载荷法 | unit load method | 在所求位移处加单位力，用内力图积分求位移 | 第 18 讲 | 要会用 |
| 莫尔积分 | Mohr's integral | $\Delta=\int M\bar{M}/(EI)\,\mathrm{d}x$（梁） | 第 18 讲 | 要会算 |
| 图形互乘法 | graphical multiplication | 莫尔积分的速算：$\Delta=\Omega\bar{M}_C/EI$（直线图形） | 第 18 讲 | 要会用 |
| 卡氏定理 | Castigliano's theorem | $\Delta_i=\partial V_\varepsilon/\partial F_i$ | 第 18 讲 | 会用 |
| 力法 | force method | 以多余未知力为基本未知量解超静定的方法 | 第 19 讲 | 要会用 |
| 基本体系 | primary system | 去掉多余约束后得到的静定结构（同第 12 讲静定基） | 第 19 讲 | 要会取 |
| 多余未知力 | redundant force（X_i） | 多余约束的作用，力法的基本未知量 | 第 19 讲 | 要会选 |
| 柔度系数 | flexibility coefficient（δ_ij） | $X_j=1$ 时在 $i$ 方向引起的位移 | 第 19 讲 | 要会算 |
| 自由项 | free term（Δ_iP） | 实际载荷在 $i$ 方向引起的位移 | 第 19 讲 | 要会算 |
| 正则方程 | canonical equations | $\sum_j\delta_{ij}X_j+\Delta_{iP}=0$ 的线性方程组 | 第 19 讲 | 要会写 |
| 半结构 | half structure | 利用对称性只取结构的一半（认识层） | 第 19 讲 | 认识 |
| 动载荷 | dynamic load | 加载过程产生加速度或速度突变的载荷（须计入惯性） | 第 20 讲 | 要理解 |
| 动荷系数 | dynamic factor（k_d） | 动效应与静效应之比：$\sigma_d=k_d\sigma_{st}$、$\Delta_d=k_d\Delta_{st}$ | 第 20 讲 | 要会算 |
| 惯性力 | inertia force | 加速度引起的附加力（$ma$） | 第 20 讲 | 要理解 |
| 突加载荷 | suddenly applied load | $h=0$ 的冲击；$k_d=2$ | 第 20 讲 | 要会算 |
| 交变应力 | alternating stress | 随时间周期性变化的应力 | 第 21 讲 | 要理解 |
| 应力循环 | stress cycle | 应力从最大到最小再回到最大的一个周期 | 第 21 讲 | 要会描述 |
| 循环特征 | stress ratio（r） | $r=\sigma_{\min}/\sigma_{\max}$；对称 $-1$、脉动 $0$、静载 $+1$ | 第 21 讲 | 要会算 |
| 平均应力 / 应力幅 | mean stress / stress amplitude | $\sigma_m=(\sigma_{\max}+\sigma_{\min})/2$；$\sigma_a=(\sigma_{\max}-\sigma_{\min})/2$ | 第 21 讲 | 要会算 |
| 疲劳破坏 | fatigue failure | 交变应力长期作用下、应力远低于 $\sigma_b$ 的突然断裂（断口分光滑区与粗糙区） | 第 21 讲 | 要理解 |
| S-N 曲线 | S-N curve | 应力水平与疲劳寿命的关系曲线（约 $10^6$ 次后变水平） | 第 21 讲 | 要会用 |
| 持久极限 | endurance limit（σ_−1） | 对称循环下材料不发生疲劳破坏的最高应力 | 第 21 讲 | 要会查用 |
| 有效应力集中系数 | effective stress concentration factor（k_σ） | $>1$，在构件持久极限公式的**分母**（最不利） | 第 21 讲 | 要会查用 |
| 尺寸系数 / 表面质量系数 | size factor（ε）/ surface finish factor（β） | 均 $\le1$，在分子 | 第 21 讲 | 要会查用 |
| 细长梁界限 | slender beam limit | $L/h\ge10$ 时剪切变形占比小于 3%，Euler-Bernoulli 梁理论适用 | 第 22 讲 | 认识 |
| 应力集中系数 | stress concentration factor（k_t） | 峰值应力与名义应力之比；圆孔 $k_t=2+(1-d/W)^3$ | 第 22 讲 | 认识 |
| 纵横弯曲 | beam-column | 轴向压力与横向弯曲耦合，挠度被放大（本课不展开的下游问题） | 第 22 讲 | 认识 |
| 有限元法 | finite element method | 把连续体离散为单元求解；以第 18 讲能量原理为数学基础 | 第 22 讲 | 认识 |
| 三项基本关系 / 两类判据 / 两种工具 | — | 全课三根支柱：平衡·几何·物理；强度·刚度（+稳定·疲劳）；解析法·能量法 | 第 22 讲 | 要理解 |

## 二、公式

| 公式 | 符号各指什么 | 适用条件 | 出处讲次 |
|---|---|---|---|
| $\sigma = \lim\limits_{\Delta A\to 0}\dfrac{\Delta F}{\Delta A}$ | $\Delta F$ 为微小面积 $\Delta A$ 上的内力，$\sigma$ 为该点应力 | 应力的一般定义（对任意截面、任意点） | 第 01 讲 |
| $\sigma = \dfrac{N}{A}$（**模板**：先定截面内力 $N$，再除以面积 $A$） | $N$ 为截面内力（N），$A$ 为截面面积（$\mathrm{mm^2}$），$\sigma$ 为平均正应力 | 轴向受力且应力沿截面**均匀分布**时；此时平均应力等于逐点应力 | 第 01 讲 |
| $1\ \mathrm{MPa} = 1\ \mathrm{N/mm^2} = 10^6\ \mathrm{Pa}$ | Pa 为帕斯卡（$\mathrm{N/m^2}$），MPa 为兆帕 | 单位换算通则 | 第 01 讲 |
| $\varepsilon = \dfrac{\Delta L}{L}$ | $\Delta L$ 为伸长量（伸长为正），$L$ 为原长，$\varepsilon$ 为平均线应变（无量纲） | 均匀变形时的平均线应变；逐点应变需取微小长度 | 第 01 讲 |
| $N = \sum F_{\text{一侧,轴向}}$（**模板**：某截面轴力 = 该侧外力沿轴向的代数和，拉为正） | 一侧全部外力沿轴线的分量 | 轴向拉压；取任一侧结果相同 | 第 02 讲 |
| $\sigma = \dfrac{N}{A}$（**模板**：先定轴力 $N$，再除以横截面面积 $A$） | $N$ 为轴力（N），$A$ 为横截面积（$\mathrm{mm^2}$） | 轴向拉压、远离加力点的横截面（平面假设 + 应力均匀） | 第 02 讲 |
| $\sigma_\alpha = \sigma\cos^2\alpha$ | $\sigma=N/A$ 为横截面正应力，$\alpha$ 为斜截面与横截面的夹角 | 轴向拉压；$\alpha=0$ 时 $\sigma_\alpha=\sigma$（最大） | 第 02 讲 |
| $\tau_\alpha = \dfrac{\sigma}{2}\sin 2\alpha$ | 同上 | 轴向拉压；$\alpha=45^\circ$ 时 $\tau_\alpha=\sigma/2$（最大） | 第 02 讲 |
| $\left(\sigma_\alpha-\dfrac{\sigma}{2}\right)^2+\tau_\alpha^2=\left(\dfrac{\sigma}{2}\right)^2$ | 斜截面上的应力分量 $(\sigma_\alpha,\tau_\alpha)$ | 恒成立；几何意义是第 13 讲应力圆的雏形 | 第 02 讲 |
| $K = \dfrac{\sigma_{\max}}{\sigma_{\text{名义}}}$ | $\sigma_{\max}$ 为峰值应力，$\sigma_{\text{名义}}$ 为净截面平均应力 | 应力集中度量；通常 $K>1$ | 第 02 讲（认识层） |
| $\sigma = E\varepsilon$ | $E$ 为弹性模量（MPa） | 线弹性范围（$\sigma\le\sigma_p$） | 第 03 讲 |
| $\Delta L = \dfrac{N L}{E A}$（**模板**：先定轴力 $N$，再代 $E$、$A$、$L$） | $N$ 轴力、$L$ 原长、$E$ 弹性模量、$A$ 横截面积（$EA$ 为拉压刚度） | 线弹性范围；等截面、单一轴力 | 第 03 讲 |
| $\Delta L = \sum_i \dfrac{N_i L_i}{E_i A_i}$（连续变力时 $\Delta L=\int_0^L\frac{N(x)}{EA(x)}\mathrm{d}x$） | 第 $i$ 段轴力 $N_i$、长度 $L_i$、面积 $A_i$ | 线弹性范围；变截面/多段杆（各段带符号相加） | 第 03 讲 |
| $\varepsilon' = -\mu\,\varepsilon$ | $\mu$ 泊松比，$\varepsilon'$ 横向线应变 | 线弹性、各向同性 | 第 03 讲 |
| $[\sigma] = \dfrac{\sigma_u}{n}$ | $\sigma_u$ 极限应力（塑性取 $\sigma_s$、脆性取 $\sigma_b$），$n$ 安全系数 | 许用应力的定义 | 第 03 讲 |
| $\sigma_{\max} = \dfrac{N}{A} \le [\sigma]$（**模板**：算工作应力，与许用应力比大小） | $N$ 为危险截面轴力 | 轴向拉压强度条件 | 第 03 讲 |
| $A \ge \dfrac{N}{[\sigma]}$ | 设计截面时所需最小面积 | 轴向拉压、已知 $N$ 与 $[\sigma]$ | 第 03 讲 |
| $N \le [\sigma]\,A$ | 已知 $A$ 与 $[\sigma]$ 时的最大允许轴力 | 轴向拉压、求许用载荷 | 第 03 讲 |
| $\tau = \dfrac{Q}{A_s} \le [\tau]$（**模板**：先定剪切面与剪切面数，再算名义切应力与许用值比较） | $Q$ 为剪力、$A_s$ 为剪切面面积 | 剪切实用计算 | 第 04 讲 |
| $A_s = \dfrac{\pi d^2}{4}$（单剪）；双剪 $A_s = 2\cdot\dfrac{\pi d^2}{4}$ | $d$ 为圆截面连接件直径 | 圆截面连接件的剪切面面积 | 第 04 讲 |
| $\sigma_{bs} = \dfrac{F}{A_{bs}} = \dfrac{F}{d\,t} \le [\sigma_{bs}]$ | $F$ 为挤压力、$d$ 直径、$t$ 被挤压件厚度 | 挤压实用计算（投影面积口径） | 第 04 讲 |
| $F = \dfrac{2T}{D}$ | $T$ 为扭矩、$D$ 为轴径（键传递的圆周力） | 平键受力 | 第 04 讲 |
| 键：$A_s = b\,l$；$A_{bs} = l\,\dfrac{h}{2}$ | $b$ 键宽、$h$ 键高、$l$ 键长 | 平键的剪切面与挤压面 | 第 04 讲 |
| $M = 9550\,\dfrac{P}{n}$ | $P$ 功率（kW）、$n$ 转速（r/min） | 功率、转速换算外力偶矩 | 第 05 讲 |
| $\tau = G\gamma$ | $G$ 剪切模量、$\gamma$ 切应变 | 剪切胡克定律（线弹性） | 第 05 讲 |
| $\tau_\rho = \dfrac{T\rho}{I_p}$ | $T$ 扭矩、$\rho$ 到轴心距离、$I_p$ 极惯性矩 | 圆轴扭转切应力（沿半径线性分布） | 第 05 讲 |
| $\tau_{\max} = \dfrac{T}{W_t}$ | $W_t$ 抗扭截面系数 | 圆轴表面最大切应力 | 第 05 讲 |
| $I_p = \dfrac{\pi d^4}{32}$；$W_t = \dfrac{\pi d^3}{16}$ | $d$ 圆轴直径 | 实心圆截面 | 第 05 讲 |
| $\gamma = \rho\,\dfrac{\mathrm{d}\varphi}{\mathrm{d}x}$ | $\mathrm{d}\varphi/\mathrm{d}x$ 单位长度扭转角 | 圆轴扭转切应变 | 第 05 讲 |
| $G = \dfrac{E}{2(1+\mu)}$ | $E$ 弹性模量、$\mu$ 泊松比 | 各向同性材料弹性常数关系（第 14 讲推导） | 第 05 讲（引） |
| $\varphi = \dfrac{T L}{G I_p}$ | $T$ 扭矩、$L$ 轴长、$G$ 剪切模量、$I_p$ 极惯性矩 | 圆轴扭转、线弹性 | 第 06 讲 |
| $\theta = \dfrac{\varphi}{L} = \dfrac{T}{G I_p}$ | $\theta$ 单位长度扭转角（常用 $^\circ/\mathrm{m}$） | 圆轴扭转刚度计算 | 第 06 讲 |
| $\theta_{\max} \le [\theta]$（刚度条件） | $[\theta]$ 许用单位长度扭转角 | 扭转刚度校核 / 设计 | 第 06 讲 |
| 空心圆环：$I_p = \dfrac{\pi(D^4-d_0^4)}{32}$；$W_t = \dfrac{\pi(D^4-d_0^4)}{16D}$ | $D$ 外径、$d_0$ 内径、$\alpha=d_0/D$ | 空心圆轴截面量 | 第 06 讲 |
| 矩形截面：$\tau_{\max}=\dfrac{T}{\alpha h b^2}$、$\varphi=\dfrac{TL}{G\beta h b^3}$ | $\alpha$、$\beta$ 随高宽比 $h/b$ 查表 | 非圆截面扭转（认识层） | 第 06 讲 |
| 薄壁管：$\tau = \dfrac{T}{2A_0 t}$ | $A_0$ 中线所围面积、$t$ 壁厚 | 薄壁截面扭转（认识层） | 第 06 讲 |
| $S_z = \int_A y\,\mathrm{d}A$；$y_c = S_z/A$ | 面积对轴的一次矩 | 静矩与形心定义 | 第 07 讲 |
| $y_c = \dfrac{\sum A_i y_i}{\sum A_i}$ | $A_i$ 分块面积、$y_i$ 其形心坐标（到参考轴） | 组合截面形心 | 第 07 讲 |
| $I_z = \int_A y^2\,\mathrm{d}A$ | 惯性矩定义 | 抗弯能力度量 | 第 07 讲 |
| $i = \sqrt{I/A}$ | 惯性半径 | 惯性矩折算成长度的关系 | 第 07 讲 |
| $I_p = I_z + I_y$ | 极惯性矩与两方向惯性矩 | 极惯性矩关系 | 第 07 讲 |
| 矩形：$I_z=\dfrac{bh^3}{12}$、$W_z=\dfrac{bh^2}{6}$；圆：$I_z=\dfrac{\pi d^4}{64}$、$W_z=\dfrac{\pi d^3}{32}$ | $b,h$ 宽高、$d$ 直径 | 常见截面惯性矩与抗弯截面系数 | 第 07 讲 |
| 圆环：$I_z=\dfrac{\pi(D^4-d_0^4)}{64}$ | $D$ 外径、$d_0$ 内径 | 圆环截面 | 第 07 讲 |
| $I_z = I_{z_c} + a^2 A$ | $a$ 两平行轴间距、$I_{z_c}$ 对形心轴 | 平行移轴定理（只从形心轴出发） | 第 07 讲 |
| $\dfrac{\mathrm{d}Q}{\mathrm{d}x}=q$；$\dfrac{\mathrm{d}M}{\mathrm{d}x}=Q$ | 载荷集度 $q$、剪力 $Q$、弯矩 $M$ | 载荷-剪力-弯矩微分关系 | 第 08 讲 |
| 简支梁：中点集中力 $M_{\max}=\dfrac{PL}{4}$；任意位置 $\dfrac{Pab}{L}$ | $P$ 集中力、$a,b$ 距两端、$L$ 跨度 | 简支梁受集中力 | 第 08 讲 |
| 简支梁均布：$M_{\max}=\dfrac{qL^2}{8}$ | $q$ 均布载荷、$L$ 跨度 | 简支梁受均布载荷（跨中） | 第 08 讲 |
| 悬臂梁端部集中力：$M_{\max}=PL$ | $P$ 端部集中力、$L$ 悬臂长 | 悬臂梁（固定端） | 第 08 讲 |
| $\sigma = \dfrac{My}{I_z}$ | $M$ 弯矩、$y$ 到中性轴距离、$I_z$ 惯性矩 | 梁弯曲正应力（线弹性、小变形） | 第 09 讲 |
| $\sigma_{\max} = \dfrac{M}{W_z}$ | $W_z=I_z/y_{\max}$ 抗弯截面系数 | 危险点（离中性轴最远处） | 第 09 讲 |
| $\dfrac{1}{\rho} = \dfrac{M}{E I_z}$ | $\rho$ 中性层曲率半径 | 纯弯曲（挠曲线曲率，11 讲用） | 第 09 讲 |
| $\int_A \sigma\,\mathrm{d}A = 0 \Rightarrow$ 中性轴过形心 | 正应力合成的轴力为零 | 纯弯曲静力关系 | 第 09 讲 |
| $\tau = \dfrac{Q S_z^*}{I_z b}$ | $Q$ 剪力、$S_z^*$ 所求点以外面积的静矩、$b$ 该处宽度 | 弯曲切应力 | 第 10 讲 |
| 矩形：$\tau_{\max}=\dfrac{3Q}{2A}$；圆：$\tau_{\max}=\dfrac{4Q}{3A}$ | $A$ 截面面积 | 最大弯曲切应力（中性轴处） | 第 10 讲 |
| $\tau_{\max} \le [\tau]$ | $[\tau]$ 许用切应力 | 弯曲切应力强度条件 | 第 10 讲 |
| $EI_z\,w'' = M(x)$ | $w$ 挠度（本课向上为正）、$M$ 弯矩 | 挠曲线近似微分方程（线弹性、小变形） | 第 11 讲 |
| 简支跨中 $w_{\max}=\dfrac{PL^3}{48EI_z}$；简支均布 $\dfrac{5qL^4}{384EI_z}$；悬臂端 $\dfrac{PL^3}{3EI_z}$ | 记其大小 $\lvert w\rvert$ | 常见梁最大挠度 | 第 11 讲 |
| $w_{\max}\le[w]$；$\theta_{\max}\le[\theta]$ | $[w]$、$[\theta]$ 许用挠度与转角 | 弯曲刚度条件 | 第 11 讲 |
| 一次超静定梁（固支+简支，均布 $q$）：$R_B=\dfrac{3qL}{8}$；$M_{\text{固定}}=-\dfrac{qL^2}{8}$ | $R_B$ 多余约束反力、$M$ 固定端弯矩 | 变形比较法典型结果 | 第 12 讲 |
| 拉压超静定（两端固定杆受 $P$）：$R_1=\dfrac{Pb}{L}$、$R_2=\dfrac{Pa}{L}$ | $a,b$ 加载点到两端距离 | 两端固定杆轴向载荷 | 第 12 讲 |
| $\sigma = -E\alpha\,\Delta T$ | $\alpha$ 线膨胀系数、$\Delta T$ 温升 | 温度应力（两端固定） | 第 12 讲 |
| $\sigma = E\dfrac{\delta}{L}$ | $\delta$ 装配误差、$L$ 原长 | 装配应力 | 第 12 讲 |
| $\sigma_\alpha = C + A\cos 2\alpha - B\sin 2\alpha$；$\tau_\alpha = A\sin 2\alpha + B\cos 2\alpha$ | $C=\dfrac{\sigma_x+\sigma_y}{2}$、$A=\dfrac{\sigma_x-\sigma_y}{2}$、$B=\tau_{xy}$ | 平面应力斜截面应力 | 第 13 讲 |
| $\sigma_{1,2} = \dfrac{\sigma_x+\sigma_y}{2} \pm \sqrt{\left(\dfrac{\sigma_x-\sigma_y}{2}\right)^2 + \tau_{xy}^2}$ | 写为 $C\pm R$，$R$ 即应力圆半径 | 主应力 | 第 13 讲 |
| $\tau_{\max} = R = \dfrac{\sigma_1-\sigma_2}{2}$ | — | 最大切应力 | 第 13 讲 |
| $\tan 2\alpha_p = -\dfrac{2\tau_{xy}}{\sigma_x-\sigma_y}$ | $\alpha_p$ 主平面方向 | 主平面方位 | 第 13 讲 |
| $\varepsilon_x = \dfrac{1}{E}[\sigma_x-\mu(\sigma_y+\sigma_z)]$（$\varepsilon_y,\varepsilon_z$ 三式对称） | $E$、$\mu$；$\sigma_x,\sigma_y,\sigma_z$ | 广义胡克定律（正应力部分） | 第 14 讲 |
| $\tau_{\max} = \dfrac{\sigma_1-\sigma_3}{2}$ | $\sigma_1$、$\sigma_3$ 最大/最小主应力 | 三向最大切应力 | 第 14 讲 |
| $\theta = \dfrac{1-2\mu}{E}(\sigma_1+\sigma_2+\sigma_3)$ | $\theta=\varepsilon_x+\varepsilon_y+\varepsilon_z$ | 体积应变（只与主应力之和有关） | 第 14 讲 |
| $G = \dfrac{E}{2(1+\mu)}$ | — | 三弹性常数关系（各向同性） | 第 14 讲 |
| $\sigma_{r1}=\sigma_1$；$\sigma_{r2}=\sigma_1-\mu(\sigma_2+\sigma_3)$；$\sigma_{r3}=\sigma_1-\sigma_3$；$\sigma_{r4}=\sqrt{\frac{1}{2}[(\sigma_1-\sigma_2)^2+(\sigma_2-\sigma_3)^2+(\sigma_3-\sigma_1)^2]}$ | $\sigma_1\ge\sigma_2\ge\sigma_3$ 主应力 | 四个强度理论的相当应力 | 第 15 讲 |
| $\sigma_r \le [\sigma]$ | $[\sigma]$ 许用应力 | 统一强度条件 | 第 15 讲 |
| $\sigma_\theta=\dfrac{pD}{2t}$；$\sigma_z=\dfrac{pD}{4t}$ | $D$ 中面直径、$t$ 壁厚、$p$ 内压 | 薄壁圆筒应力（二向） | 第 15 讲 |
| 二向状态（$\sigma_3=0$）：$\sigma_{r4}=\sqrt{\sigma_1^2+\sigma_2^2-\sigma_1\sigma_2}$ | $\sigma_1,\sigma_2$ 二向主应力 | 第四理论的二向化简 | 第 15 讲 |
| 纯剪切 $\sigma_{r3}=2\tau$、$\sigma_{r4}=\sqrt3\tau$；弯扭组合 $\sigma_{r3}=\sqrt{\sigma^2+4\tau^2}$、$\sigma_{r4}=\sqrt{\sigma^2+3\tau^2}$ | $\tau$ 切应力、$\sigma$ 弯曲正应力 | 经典情形核对 | 第 15 讲 |
| $\sigma = \dfrac{N}{A} \pm \dfrac{M}{W}$ | $N$ 轴力、$M$ 弯矩、$A$ 面积、$W$ 抗弯截面系数 | 拉（压）弯组合正应力 | 第 16 讲 |
| $\sigma = -\dfrac{F}{A} \pm \dfrac{Fe}{W}$ | $F$ 偏心压力、$e$ 偏心距 | 偏心拉压 | 第 16 讲 |
| 截面核心：矩形 $\lvert e\rvert\leq h/6$（或 $b/6$）；圆 $e\leq d/8$ | $e$ 偏心距、$h,b$ 截面尺寸、$d$ 直径 | 截面核心边界 | 第 16 讲 |
| $\sigma_{r3}=\sqrt{\sigma^2+4\tau^2}$；$\sigma_{r4}=\sqrt{\sigma^2+3\tau^2}$ | $\sigma$ 弯曲正应力、$\tau$ 扭转切应力 | 圆轴弯扭组合（第三/第四） | 第 16 讲 |
| $P_{cr} = \dfrac{\pi^2 E I_{\min}}{(\mu L)^2}$ | $I_{\min}$ 最小惯性矩、$\mu$ 长度系数、$L$ 杆长 | 欧拉临界力 | 第 17 讲 |
| $\lambda = \dfrac{\mu L}{i}$ | $i=\sqrt{I/A}$ 惯性半径 | 柔度（长细比） | 第 17 讲 |
| $\sigma_{cr} = \dfrac{\pi^2 E}{\lambda^2}$ | — | 欧拉临界应力（大柔度） | 第 17 讲 |
| $\lambda_p = \pi\sqrt{E/\sigma_p}$ | $\sigma_p$ 比例极限 | 大/中柔度分界 | 第 17 讲 |
| 中柔度：$\sigma_{cr}=a-b\lambda$；$\lambda_s=\dfrac{a-\sigma_s}{b}$ | $a,b$ 材料常数、$\sigma_s$ 屈服极限 | 直线公式与中/小柔度分界 | 第 17 讲 |
| $n_{st}=\dfrac{P_{cr}}{P}\ge[n_{st}]$；$\sigma\le\varphi[\sigma]$ | $[n_{st}]$ 稳定安全系数（3~5）、$\varphi$ 折减系数 | 压杆稳定校核 | 第 17 讲 |
| 拉压 $V_\varepsilon=\dfrac{N^2L}{2EA}$；扭转 $\dfrac{T^2L}{2GI_p}$；弯曲 $\displaystyle\int\dfrac{M^2}{2EI}\mathrm{d}x$ | $N,T,M$ 内力、$EA,GI_p,EI$ 刚度 | 三种基本变形的应变能 | 第 18 讲 |
| $\Delta=\displaystyle\int\dfrac{M(x)\bar{M}(x)}{EI}\mathrm{d}x$ | $M$ 实际载荷、$\bar{M}$ 单位载荷的弯矩图 | 莫尔积分（梁，单位载荷法） | 第 18 讲 |
| 直线×直线：$\Delta=\dfrac{\Omega\bar{M}_C}{EI}$；标准抛物线×直线：$\Delta=\dfrac{1}{EI}\cdot\dfrac{5}{8}\Omega\bar{M}_{\text{中点}}$ | $\Omega$ 图形面积、$\bar{M}_C$ 形心处竖标 | 图形互乘规则 | 第 18 讲 |
| $\delta_{12}=\delta_{21}$；$F_1\delta_{12}=F_2\delta_{21}$ | — | 位移互等 / 功的互等定理 | 第 18 讲 |
| $\Delta_i=\dfrac{\partial V_\varepsilon}{\partial F_i}$ | — | 卡氏定理 | 第 18 讲 |
| $\delta_{ij}=\displaystyle\int\dfrac{\bar{M}_i\bar{M}_j}{EI}\mathrm{d}x$；$\Delta_{iP}=\displaystyle\int\dfrac{M_P\bar{M}_i}{EI}\mathrm{d}x$ | $\bar{M}_i$ 为 $X_i=1$ 的弯矩图、$M_P$ 为实际载荷弯矩图 | 柔度系数与自由项（梁） | 第 19 讲 |
| $\displaystyle\sum_j\delta_{ij}X_j+\Delta_{iP}=0$ | — | 正则方程（$n$ 次 $n$ 个） | 第 19 讲 |
| 一次超静定：$X_1=-\dfrac{\Delta_{1P}}{\delta_{11}}$ | — | 一次超静定的解 | 第 19 讲 |
| $\delta_{ij}=\delta_{ji}$ | — | 系数对称性（位移互等） | 第 19 讲 |
| 两端固定梁：$M_{\text{固}}=-\dfrac{qL^2}{12}$、$M_{\text{跨中}}=\dfrac{qL^2}{24}$ | — | 对称性利用的典型结果 | 第 19 讲 |
| 静载法：$\sigma_d=k_d\sigma_{st}$；$\Delta_d=k_d\Delta_{st}$ | $k_d$ 动荷系数 | 动载荷的通用处理 | 第 20 讲 |
| 等加速：$k_d=1+\dfrac{a}{g}$ | $a$ 加速度、$g$ 重力加速度 | 等加速运动构件 | 第 20 讲 |
| 自由落体冲击：$k_d=1+\sqrt{1+\dfrac{2h}{\Delta_{st}}}$ | $h$ 落差、$\Delta_{st}$ 静变形 | 冲击动荷系数 | 第 20 讲 |
| $h=0$ 时 $k_d=2$；$h$ 大时 $k_d\approx\sqrt{\dfrac{2h}{\Delta_{st}}}$ | — | 冲击的两个特例 | 第 20 讲 |
| $r=\dfrac{\sigma_{\min}}{\sigma_{\max}}$；$\sigma_m=\dfrac{\sigma_{\max}+\sigma_{\min}}{2}$；$\sigma_a=\dfrac{\sigma_{\max}-\sigma_{\min}}{2}$ | — | 交变应力的描述 | 第 21 讲 |
| $N\sigma^m=C$ | $m$、$C$ 材料常数（钢材 $m\approx9$） | S-N 曲线幂律 | 第 21 讲 |
| $(\sigma_{-1})_{\text{构件}}=\sigma_{-1}\dfrac{\varepsilon\beta}{k_\sigma}$ | $k_\sigma$、$\varepsilon$、$\beta$ 三个修正系数 | 构件持久极限 | 第 21 讲 |
| $n=\dfrac{(\sigma_{-1})_{\text{构件}}}{\sigma_a}\ge[n]$ | $[n]=1.4\sim1.8$ | 对称循环疲劳强度校核 | 第 21 讲 |
| $\dfrac{w_s}{w_b}\approx 11.52\,\dfrac{I}{AL^2}\cdot\dfrac{E}{G}$（矩形） | — | 剪切变形占比（Timoshenko，认识层） | 第 22 讲 |
| $k_t = 2+\left(1-\dfrac{d}{W}\right)^3$ | $d/W$ 孔径比 | 有限宽板圆孔应力集中 | 第 22 讲 |
| $w = \dfrac{w_0}{1-P/P_{cr}}$ | $P_{cr}$ 欧拉临界力 | 纵横弯曲挠度放大（下游问题） | 第 22 讲 |
| 离散误差 $\propto h^2$（$O(h^2)$） | $h$ 单元尺寸 | 有限元收敛阶 | 第 22 讲 |
