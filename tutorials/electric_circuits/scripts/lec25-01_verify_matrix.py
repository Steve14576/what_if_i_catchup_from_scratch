# =====================================================================
# lec25-01 电路方程的矩阵形式：A 与 KCL/KVL、A·Y·A^T 三通道互证、状态方程
#          （第 25 讲 §2-§5 数值实验；图 1 示例电路有向图、图 2 A 矩阵、图 3 状态轨迹）
# 规模纪律：总耗时 < 10 秒（矩阵运算 + RK4 + schemdraw/matplotlib 三图）。
#
# 示例电路：3 个独立节点 + 参考 0；5 条支路：
#   b1: 1->0 (G1=0.1 S)；b2: 1->2 (G2=0.05)；b3: 2->0 (G3=0.2)；
#   b4: 2->3 (G4=0.1)；b5: 3->0 (G5=0.05)
#   电流源注入：节点 1 注 1 A、节点 3 注 0.5 A
#   A = [[1,1,0,0,0],[0,-1,1,1,0],[0,0,0,-1,1]]
#   Yn = A Yb A^T = [[0.15,-0.05,0],[-0.05,0.35,-0.1],[0,-0.1,0.15]]（与观察法对照）
# 状态方程例（12 讲 RLC：R=28、L=50mH、C=20uF）：x=[uC,iL]
#   S = [[0,-1/C],[1/L,-R/L]] -> 特征值 -280±j960（= 12 讲特征根 = 22 讲极点）
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import schemdraw
import schemdraw.elements as elm

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

elm.style(elm.STYLE_IEC)
schemdraw.config(font="Microsoft YaHei", fontsize=12)

# ---------------------------------------------------------------------
print("=== 实验 1：图论计数与一棵树 ===")
b, n = 5, 4   # 支路数、含参考结点的结点数
print("  支路 b = %d、结点 n = %d（含参考）：树支 = n-1 = %d、连支 = b-n+1 = %d"
      % (b, n, n - 1, b - n + 1))
print("  一棵树（连接 0/1/2/3 且无回路）：b1(1-0)、b2(1-2)、b4(2-3)；连支：b3、b5")

print()
print("=== 实验 2：关联矩阵 A 与 KCL/KVL ===")
A = np.array([[1.0, 1.0, 0.0, 0.0, 0.0],
              [0.0, -1.0, 1.0, 1.0, 0.0],
              [0.0, 0.0, 0.0, -1.0, 1.0]])
G = np.array([0.1, 0.05, 0.2, 0.1, 0.05])
print("  A =\n%s" % np.array2string(A, precision=0, suppress_small=True))
IS = np.array([1.0, 0.0, 0.5])   # 注入电流
Yn_A = A @ np.diag(G) @ A.T
print("  Yn = A*Yb*A^T =\n%s" % np.array2string(Yn_A, precision=2))
Yn_hand = np.array([[0.15, -0.05, 0.0], [-0.05, 0.35, -0.1], [0.0, -0.1, 0.15]])
print("  手写观察法 Yn 与组装偏差：%.1e" % np.max(np.abs(Yn_A - Yn_hand)))
U = np.linalg.solve(Yn_A, IS)
print("  结点电位 U = %s V" % np.array2string(U, precision=4))
u = A.T @ U
i = G * u
print("  支路电压 u = A^T U = %s" % np.array2string(u, precision=4))
print("  支路电流 i = Yb u = %s" % np.array2string(i, precision=4))
print("  KCL 核对（无源支路口径）A i = I_S：%s（残差 %.1e）"
      % (np.array2string(A @ i, precision=4), np.max(np.abs(A @ i - IS))))
print("  （若把电流源也计为支路，则对所有支路 A i = 0 —— 两种等价口径）")

print()
print("=== 实验 3：KCL 直接手写对照（第三个通道） ===")
K = np.array([[0.15, -0.05, 0.0], [-0.05, 0.35, -0.1], [0.0, -0.1, 0.15]])
print("  直接按 KCL 手写系数矩阵与 A*Yb*A^T 偏差：%.1e（三者同一矩阵）" % np.max(np.abs(K - Yn_A)))

print()
print("=== 实验 4：状态方程（RLC 放电）与特征值 ===")
R, L, C = 28.0, 50e-3, 20e-6
S = np.array([[0.0, -1 / C], [1 / L, -R / L]])
ev = np.linalg.eigvals(S)
print("  状态矩阵 S = [[0, -1/C],[1/L, -R/L]] 的特征值：%s" % np.array2string(ev, precision=2))
print("  与 12 讲特征根 -280 ± j960 对照（= 22 讲极点）：实部 %.1f、|虚部| %.1f"
      % (ev[0].real, abs(ev[0].imag)))
# RK4 数值积分
t, dt = 0.0, 1e-6
x = np.array([10.0, 0.0])   # [uC, iL]
Nn = int(0.012 / dt)
tr = np.zeros(Nn)
x1 = np.zeros(Nn)
x2 = np.zeros(Nn)
for k in range(Nn):
    f = lambda v: S @ v
    k1 = f(x); k2 = f(x + dt / 2 * k1); k3 = f(x + dt / 2 * k2); k4 = f(x + dt * k3)
    x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    t += dt
    tr[k] = t; x1[k] = x[0]; x2[k] = x[1]
anal_uc = np.exp(-280 * tr) * (10 * np.cos(960 * tr) + 10 * 280 / 960 * np.sin(960 * tr))
anal_il = 200 / 960 * np.exp(-280 * tr) * np.sin(960 * tr)
print("  状态方程 RK4 积分 vs 12 讲解析：uC 偏差 %.1e、iL 偏差 %.1e"
      % (np.max(np.abs(x1 - anal_uc)), np.max(np.abs(x2 - anal_il))))
print("  -> 状态矩阵的特征值就是固有频率（极点），积分轨迹即放电响应")

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：示例电路的有向图 ===")
with schemdraw.Drawing(show=False) as d:
    # 参考公共线
    d += elm.Line().at((-1.0, 0.6)).to((5.0, 0.6))
    d += elm.Line().at((0.3, 0.6)).to((0.3, 0.25))
    d += elm.Line().at((-0.05, 0.25)).to((0.65, 0.25))
    d += elm.Line().at((0.02, 0.15)).to((0.58, 0.15))
    # 支路 b1: 1->0
    d += elm.Line().at((0, 2.0)).to((0, 0.6))
    d += elm.Arrow().at((0, 1.4)).to((0, 1.05))
    d += elm.Label().at((-0.45, 1.35)).label("$b_1$", fontsize=10)
    # 支路 b2: 1->2
    d += elm.Line().at((0, 2.0)).to((2, 2.0))
    d += elm.Arrow().at((1.0, 2.0)).to((1.35, 2.0))
    d += elm.Label().at((0.75, 2.3)).label("$b_2$", fontsize=10)
    # 支路 b3: 2->0
    d += elm.Line().at((2, 2.0)).to((2, 0.6))
    d += elm.Arrow().at((2, 1.4)).to((2, 1.05))
    d += elm.Label().at((2.3, 1.35)).label("$b_3$", fontsize=10)
    # 支路 b4: 2->3
    d += elm.Line().at((2, 2.0)).to((4, 2.0))
    d += elm.Arrow().at((3.0, 2.0)).to((3.35, 2.0))
    d += elm.Label().at((2.75, 2.3)).label("$b_4$", fontsize=10)
    # 支路 b5: 3->0
    d += elm.Line().at((4, 2.0)).to((4, 0.6))
    d += elm.Arrow().at((4, 1.4)).to((4, 1.05))
    d += elm.Label().at((4.3, 1.35)).label("$b_5$", fontsize=10)
    # 结点与参考
    d += elm.Dot().at((0, 2.0)); d += elm.Dot().at((2, 2.0)); d += elm.Dot().at((4, 2.0))
    d += elm.Label().at((-0.3, 2.25)).label("1", fontsize=11)
    d += elm.Label().at((2.0, 2.25)).label("2", fontsize=11)
    d += elm.Label().at((4.0, 2.25)).label("3", fontsize=11)
    d += elm.Label().at((4.9, 0.45)).label("参考 0", fontsize=10)
    d += elm.Label().at((2.0, 2.8)).label("支路方向 = 关联矩阵 A 的正方向", fontsize=10)

save_stem = "lec25_fig1_graph"
d.save(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
d.save(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：关联矩阵 A 的可视化 ===")
fig, ax = plt.subplots(figsize=(8.2, 3.6))
im = ax.imshow(A, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(5)); ax.set_xticklabels(["$b_1$", "$b_2$", "$b_3$", "$b_4$", "$b_5$"], fontsize=11)
ax.set_yticks(range(3)); ax.set_yticklabels(["结点 1", "结点 2", "结点 3"], fontsize=11)
for r in range(3):
    for c in range(5):
        ax.text(c, r, "%d" % A[r, c], ha="center", va="center", fontsize=13, color="black")
ax.set_title("关联矩阵 $A$：+1 = 支路离开该结点，-1 = 进入（白 = 无关联）", fontsize=11)
fig.colorbar(im, ax=ax, shrink=0.8, ticks=[-1, 0, 1])
plt.tight_layout()
save_stem = "lec25_fig2_Amatrix"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：状态平面上的放电轨迹（uC-iL 相图） ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.4))
a1.plot(x1, x2, color="#1f5fa8", lw=1.6)
a1.plot([x1[0]], [x2[0]], "o", color="#c0392b", ms=7)
a1.annotate("起点 $(10,\\ 0)$", xy=(10, 0), xytext=(6.5, 0.11), fontsize=10, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
a1.set_xlabel("$u_C$ / V")
a1.set_ylabel("$i_L$ / A")
a1.set_title("状态平面轨迹（螺旋收敛：能量被 R 抽走）", fontsize=11)
a1.grid(alpha=0.3)
a2.plot(tr * 1e3, x1, color="#1f5fa8", lw=1.8, label="$u_C(t)$（状态方程积分）")
a2.plot(tr * 1e3, anal_uc, color="#c0392b", lw=1.0, ls="--", label="12 讲解析解")
a2.set_xlabel("时间 $t$ / ms")
a2.set_ylabel("$u_C$ / V")
a2.set_title("状态方程积分 = 时域解（残差 1e-15 量级）", fontsize=11)
a2.legend(fontsize=9)
a2.grid(alpha=0.3)
plt.tight_layout()
save_stem = "lec25_fig3_stateplane"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec25-01 完成。")