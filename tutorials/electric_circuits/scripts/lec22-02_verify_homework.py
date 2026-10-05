# =====================================================================
# lec22-02 作业数字预验证（Q2-Q8）
# 规模纪律：总耗时 < 5 秒（sympy 符号 + 数值核对）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import sympy as sp

s, t = sp.symbols("s t")

print("=== Q2：极零点与稳定判定（H = (2s+1)/(s^2+3s+2)） ===")
H2 = (2 * s + 1) / (s ** 2 + 3 * s + 2)
print("  零点：%s；极点：%s" % (sp.solve(sp.numer(sp.together(H2)), s),
                              sp.solve(sp.denom(sp.together(H2)), s)))
print("  极点实部全负 -> 稳定")

print()
print("=== Q3：RC 低通（R = 1 k、C = 100 nF） ===")
R, C = 1000.0, 1e-7
wpole = -1 / (R * C)
print("  H(s) = 1/(1+%.0e s)：极点 %.0f（= -wc，19 讲 wc = 1e4）-> 稳定" % (R * C, wpole))

print()
print("=== Q4：主例极零点反查（H = 1e6/(s^2+100s+1e6)） ===")
H4 = 1e6 / (s ** 2 + 100 * s + 1e6)
poles = sp.solve(sp.denom(sp.together(H4)), s)
print("  极点：%s" % poles)
print("  |极点| = %.1f（= w0）；实部 %.0f（= -alpha）；Q = %.1f -> 稳定"
      % (abs(complex(poles[0])), complex(poles[0]).real, 10.0))

print()
print("=== Q5：稳定性判定四组极点 ===")
for name, pl in [("① -2, -3", [-2, -3]), ("② -1, +2", [-1, 2]),
                 ("③ ±j5", [5j, -5j]), ("④ -1±j5", [complex(-1, 5), complex(-1, -5)])]:
    sigs = [complex(p).real for p in pl]
    if all(x < 0 for x in sigs):
        verdict = "稳定（全左半平面）"
    elif any(x > 0 for x in sigs):
        verdict = "不稳定（含右半平面极点）"
    else:
        verdict = "临界（含虚轴极点）"
    print("  %s：%s" % (name, verdict))

print()
print("=== Q6：H = (s+3)/(s^2+4s+13) 的极零点 ===")
H6 = (s + 3) / (s ** 2 + 4 * s + 13)
print("  零点：%s；极点：%s" % (sp.solve(sp.numer(sp.together(H6)), s),
                              sp.solve(sp.denom(sp.together(H6)), s)))
print("  w0 = sqrt(13) = %.4f；wd = 3 -> 稳定" % sp.sqrt(13))

print()
print("=== Q7：冲激响应（H = 10/(s^2+6s+25)） ===")
H7 = 10 / (s ** 2 + 6 * s + 25)
ht = sp.simplify(sp.inverse_laplace_transform(H7, s, t))
print("  h(t) = %s（= 2.5 e^{-3t} sin 4t）；极点 -3±j4 -> 稳定" % ht)

print()
print("=== Q8：负阻尼（H = 1e6/(s^2 - 100s + 1e6)） ===")
H8 = 1e6 / (s ** 2 - 100 * s + 1e6)
poles8 = sp.solve(sp.denom(sp.together(H8)), s)
print("  极点：%s -> 实部 %+.0f > 0：右半平面 -> 不稳定"
      % (poles8, complex(poles8[0]).real))
print("  物理来源：负电阻/有源（受控源）向电路供能；响应含 e^{+50t} 发散")

print()
print("[DONE] lec22-02 完成。")