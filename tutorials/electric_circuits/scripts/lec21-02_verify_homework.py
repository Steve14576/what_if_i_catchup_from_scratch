# =====================================================================
# lec21-02 作业数字预验证（Q2-Q8）
# 规模纪律：总耗时 < 5 秒（sympy 符号 + 数值核对）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import sympy as sp

t, s = sp.symbols("t s", real=True)

print("=== Q2：常用变换对（查表核对） ===")
print("  L[e^{-3t}] = %s；L[2] = %s；L[cos 4t] = %s"
      % (sp.laplace_transform(sp.exp(-3 * t), t, s, noconds=True),
         sp.laplace_transform(2, t, s, noconds=True),
         sp.laplace_transform(sp.cos(4 * t), t, s, noconds=True)))

print()
print("=== Q3：RL 阶跃+初值（R = 4、L = 2 H、20 V、i(0) = 1 A） ===")
R, L, E, i0 = 4.0, 2.0, 20.0, 1.0
Is = (E / s + L * i0) / (s * L + R)
print("  I(s) = %s = %s" % (sp.simplify(Is), sp.apart(Is, s)))
it = sp.inverse_laplace_transform(Is, s, t)
print("  i(t) = %s" % sp.simplify(it))
print("  核对：i(0+) = %.2f（expect 1）；i(inf) = %.2f（expect 5）；i'(0+) = %.2f（expect %.2f）"
      % (float(it.subs(t, 1e-9)), float(it.subs(t, 100)),
         float(sp.diff(it, t).subs(t, 1e-9)), (E - R * i0) / L))

print()
print("=== Q5：部分分式·单根 ===")
F5 = (s + 5) / ((s + 1) * (s + 3))
print("  %s = %s" % (sp.simplify(F5), sp.apart(F5, s)))

print()
print("=== Q6：部分分式·双实根（RLC 型） ===")
F6 = 100 / (s ** 2 + 15 * s + 50)
print("  %s = %s" % (F6, sp.apart(F6, s)))
f6 = sp.inverse_laplace_transform(F6, s, t)
print("  f(t) = %s" % sp.simplify(f6))

print()
print("=== Q7：部分分式·复根 ===")
F7 = 10 / (s ** 2 + 6 * s + 25)
print("  F7 = %s" % F7)
print("  配方法 -> (10/4) * 4/((s+3)^2+16) -> f(t) = 2.5 e^{-3t} sin 4t")
f7 = sp.inverse_laplace_transform(F7, s, t)
print("  sympy 逆变换：%s" % sp.simplify(f7))

print()
print("=== Q8：运算法重解一阶电路（R = 5、L = 1 H、10 V、i(0) = 4 A） ===")
R8, L8, E8, i08 = 5.0, 1.0, 10.0, 4.0
Is8 = (E8 / s + L8 * i08) / (s * L8 + R8)
print("  I(s) = %s = %s" % (sp.simplify(Is8), sp.apart(Is8, s)))
it8 = sp.simplify(sp.inverse_laplace_transform(Is8, s, t))
print("  i(t) = %s" % it8)
print("  与三要素法对照：f(inf) = %.1f、f(0+) = %.1f、tau = %.2f s -> 2 + 2 e^{-5t}"
      % (E8 / R8, i08, L8 / R8))

print()
print("[DONE] lec21-02 完成。")