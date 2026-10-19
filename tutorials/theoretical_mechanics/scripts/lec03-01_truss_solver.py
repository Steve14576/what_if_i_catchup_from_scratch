# L03 平面桁架通用求解器 + 三组验证
# 规模纪律: 目标 < 1 秒; numpy 线性代数, 无其他依赖
# 方法: 每节点列汇交力系两个投影方程 (共 2n 个), 未知量 = m 根杆内力 + 支反力
#       (固定铰 2 个分量, 滚动支座 1 个竖直分量), 组装 A x = b 后 numpy 求解;
#       解后代回算平衡残差 (校验器的自动化).
# 约定: 杆内力以拉为正; 节点上杆力 = N * (node - other)/|node - other| (背离节点).
# print 全 ASCII (GBK 控制台安全).

import numpy as np

TOL = 1e-9


def solve_truss(nodes, members, pin, roller, loads):
    """平面桁架静定求解器.

    nodes:   dict 节点名 -> (x, y)
    members: list (杆名, 端点1, 端点2)
    pin:     固定铰支座节点名 (2 未知量 Fx, Fy)
    roller:  滚动支座节点名 (1 未知量 Fy, 支承面水平)
    loads:   dict 节点名 -> (Fx, Fy) 外载荷
    返回: (解向量 dict, 残差范数)
    """
    n_eq = 2 * len(nodes)
    n_unk = len(members) + 3
    assert n_eq == n_unk, "not statically determinate: eq=%d unknowns=%d" % (n_eq, n_unk)
    A = np.zeros((n_eq, n_unk))
    b = np.zeros(n_eq)
    # 杆内力未知量: 列 0..m-1; 支反力: 列 m (pin_x), m+1 (pin_y), m+2 (roller_y)
    for k, (name, i, j) in enumerate(members):
        xi, yi = nodes[i]
        xj, yj = nodes[j]
        L = np.hypot(xj - xi, yj - yi)
        # 对节点 i: 杆力 = N * (i - j)/L (背离 i); 方程移项到左侧取负
        for node, sign in ((i, -1.0), (j, -1.0)):
            r = 2 * list(nodes.keys()).index(node)
            if node == i:
                ux, uy = (xi - xj) / L, (yi - yj) / L
            else:
                ux, uy = (xj - xi) / L, (yj - yi) / L
            A[r, k] = sign * ux
            A[r + 1, k] = sign * uy
    m = len(members)
    r_pin = 2 * list(nodes.keys()).index(pin)
    A[r_pin, m] = 1.0       # pin_x 未知量 (方程: sum(杆力) + R + F_load = 0, R 正号进左)
    A[r_pin + 1, m + 1] = 1.0
    r_rol = 2 * list(nodes.keys()).index(roller)
    A[r_rol + 1, m + 2] = 1.0
    for node, (Fx, Fy) in loads.items():
        r = 2 * list(nodes.keys()).index(node)
        b[r] += -Fx
        b[r + 1] += -Fy
    x = np.linalg.solve(A, b)
    residual = np.linalg.norm(A @ x - b)
    forces = {name: x[k] for k, (name, i, j) in enumerate(members)}
    reactions = {"pin_x": x[m], "pin_y": x[m + 1], "roller_y": x[m + 2]}
    return forces, reactions, residual


def fmt(forces, keys):
    return "  ".join("%s=%+.3f" % (k, forces[k]) for k in keys)


print("=" * 64)
print("L03 truss solver verification")
print("=" * 64)

# ---------------- Exp 1: 单柱桁架, P=12 kN @ D (正文例 3) ----------------
nodes = {"A": (0.0, 0.0), "B": (2.0, 0.0), "C": (4.0, 0.0), "D": (2.0, 1.5)}
members = [("AB", "A", "B"), ("AD", "A", "D"), ("BD", "B", "D"),
           ("CD", "C", "D"), ("BC", "B", "C")]
f, r, res = solve_truss(nodes, members, "A", "C", {"D": (0.0, -12.0)})
print("[Exp 1] king-post truss, P=12 kN at D (textbook example)")
print("  supports: F_A = (%.3f, %.3f) kN, F_C = %.3f kN" % (r["pin_x"], r["pin_y"], r["roller_y"]))
print("  member forces (tension+): %s" % fmt(f, ["AB", "AD", "BD"]))
print("                          %s" % fmt(f, ["CD", "BC"]))
hand = {"AB": 8.0, "AD": -10.0, "BD": 0.0, "CD": -10.0, "BC": 8.0}
ok1 = (abs(r["pin_x"]) < TOL and abs(r["pin_y"] - 6.0) < TOL
       and abs(r["roller_y"] - 6.0) < TOL
       and all(abs(f[k] - v) < TOL for k, v in hand.items()) and res < TOL)
print("  matches hand calculation: %s" % ("PASS" if ok1 else "FAIL"))

# ---------------- Exp 2: 同桁架, 载荷挪到 B (零杆工况相关性) ----------------
f2, r2, res2 = solve_truss(nodes, members, "A", "C", {"B": (0.0, -12.0)})
print("[Exp 2] same truss, P=12 kN moved to node B")
print("  member forces: %s" % fmt(f2, ["AB", "AD", "BD"]))
print("                          %s" % fmt(f2, ["CD", "BC"]))
print("  BD is no longer zero (was 0, now %+.3f kN): zero-member is load-case-dependent" % f2["BD"])
ok2 = abs(f2["BD"] - 12.0) < TOL and abs(f2["AB"] - 8.0) < TOL and abs(f2["AD"] + 10.0) < TOL
print("  check vs hand (homework 4): %s" % ("PASS" if ok2 else "FAIL"))

# ---------------- Exp 3: 普腊桁架 (作业题 5, 解出零型零杆 + 残差) ----------------
nodes3 = {"A": (0.0, 0.0), "B": (4.0, 0.0), "C": (8.0, 0.0), "D": (2.0, 2.0), "E": (6.0, 2.0)}
members3 = [("AB", "A", "B"), ("BC", "B", "C"), ("DE", "D", "E"), ("AD", "A", "D"),
            ("BD", "B", "D"), ("BE", "B", "E"), ("CE", "C", "E")]
f3, r3, res3 = solve_truss(nodes3, members3, "A", "C", {"D": (0.0, -10.0), "E": (0.0, -10.0)})
print("[Exp 3] Pratt truss, D and E each loaded 10 kN downward")
print("  F_A = (%.3f, %.3f), F_C = %.3f" % (r3["pin_x"], r3["pin_y"], r3["roller_y"]))
print("  %s" % fmt(f3, ["AB", "BC", "DE", "AD", "BD"]))
print("  %s" % fmt(f3, ["BE", "CE"]))
print("  equilibrium residual norm = %.1e  (machine precision)" % res3)
print("  BD and BE are 'solved-to-zero' members (no visual rule applies)")
hand3 = {"AB": 10.0, "BC": 10.0, "DE": -10.0, "AD": -14.1421356, "BD": 0.0,
         "BE": 0.0, "CE": -14.1421356}
ok3 = (abs(r3["pin_y"] - 10.0) < TOL and abs(r3["roller_y"] - 10.0) < TOL
       and all(abs(f3[k] - v) < 1e-4 for k, v in hand3.items()))
print("  check vs hand (homework 5): %s" % ("PASS" if ok3 else "FAIL"))

print("=" * 64)
print("OVERALL: %s" % ("ALL PASS" if (ok1 and ok2 and ok3) else "SOME FAILED"))
