# temporary: L19 section 7 backfill (deleted after run)
import io

p = r"e:\E_Vault\CC_Formed_Projs2\LearnTheoreticalMechanics\TheoreticalMechanics-tutorial\19_第二类拉格朗日方程.md"
c = io.open(p, encoding="utf-8").read()

old_row = "| 3 | 例 3 双摆 | 拉格朗日方程组 RK4（一般初值）全程能量守恒；**同相初值退化验证**：$\\theta_1 = \\theta_2$ 时两角逐位同步、等效单摆 $\\ddot\\theta = -\\frac{3g}{5l}\\sin\\theta$ |"
new_row = "| 3 | 例 3 双摆 | 拉格朗日方程组 RK4（一般初值）全程能量守恒；**质量退化极限**（$m_2 \\to 0$：$\\theta_1$ 必须跟单摆走）；**对齐构型破坏确认**（$\\theta_1 = \\theta_2$ 初值下偏离发展到 0.457 rad——铰链传力不传矩） |"
assert old_row in c, "row3 not found"
c = c.replace(old_row, new_row)

old_out = """[Exp 3] double pendulum via Lagrange (m1=m2=1, l1=l2=1)
  generic initial condition: max |E - E0| = 2.5e-09  PASS (conserved)
  in-phase degenerate test (th1=th2=60deg, zero vel):
    theta1(t) - theta2(t) = 0 exactly for all t  PASS (symmetry preserved)
    effective single pendulum check: ddot(theta) vs -(3g/5l)sin(theta)
      max mismatch = 1.3e-12  PASS (degeneration verified)"""
new_out = """[Exp 3] double pendulum via Lagrange (m1=m2=1, l1=l2=1)
  generic initial condition: max |E - E0| = 1.0e-12  PASS (conserved)
  massless-limit test (m2=1e-9): theta1 vs single pendulum (m=1,l=1):
    max |th1 - th1_ref| = 5.1e-09  PASS (degeneration verified)
  aligned test (th1=th2=60deg, zero vel): max |th1-th2| = 0.457 rad
    PASS (alignment breaks -- hinge transmits force, not moment)"""
assert old_out in c, "output block not found"
c = c.replace(old_out, new_out)

old_pts = """三个读点：① **同相退化验证**是本讲最硬的交叉检验——双摆的拉格朗日方程在 $\\theta_1 = \\theta_2$ 初值下两角**逐位同步**（对称性保持）、且等效单摆 $\\ddot\\theta = -\\frac{3g}{5l}\\sin\\theta$ 到 $10^{-12}$——两条独立推导路线（双摆拉格朗日 vs §4.3 的力矩账）在同一物理上会合；② 一般初值下双摆能量守恒到 $10^{-9}$（双摆是**混沌**系统——能量依然守恒，混沌的是轨迹对初值的敏感性、不是守恒律）；③ 循环坐标的 $p_x$ **精确**守恒（自由质点无任何力——守恒律浮点零漂移）。"""
new_pts = """**一个诚实的修正（预写的"同相退化"验证是错误物理——推导自查抓包）**：预写把 $\\theta_1 = \\theta_2$ 初值当成双摆的不变构型（声称退化为 $\\frac{3g}{5l}$ 单摆）——**不成立**：把对齐条件代入两个拉格朗日方程立刻自相矛盾（$\\ddot\\theta_1 = -g\\sin\\theta$ vs $\\ddot\\theta_2 = 0$）；物理解剖是**光滑铰链传力不传矩**（对齐的"等效刚性直杆"直觉僭越了铰链的实际性质——L02 的约束性质在此埋了 17 讲后的一枪）。实测：对齐初值 2 秒内偏离发展到 0.457 rad。这个错误已改写成 §4.3 的教学点（"对称初值 ⇒ 对称轨道"捷径失灵）。另：脚本首跑一处 printf 漏传参（`%.3f` 原样输出）——修正后重跑。

三个读点：① **质量退化极限**是本讲最硬的交叉检验——$m_2 = 10^{-9}$ 时双摆拉格朗日方程的 $\\theta_1$ 与独立积分的单摆逐点跟到 $5\\times10^{-9}$（两条独立路径在同一物理上会合）；② 一般初值下双摆能量守恒到 $10^{-12}$（双摆是**混沌**系统——能量依然守恒，混沌的是轨迹对初值的敏感性、不是守恒律）；③ 循环坐标的 $p_x$ **精确**守恒（自由方向无任何力——守恒律浮点零漂移）。"""
assert old_pts in c, "reading points not found"
c = c.replace(old_pts, new_pts)

io.open(p, "w", encoding="utf-8").write(c)
print("L19 section 7 backfilled OK")
