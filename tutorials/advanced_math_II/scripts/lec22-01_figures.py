# 规模纪律：3 张静态 SVG, 目标 < 5 秒。
# 第 22 讲图：三算子示意、梯度场无旋、旋度场无源。
# 图内文字只用 ASCII 与 mathtext（不用 \mathbf / \begin{vmatrix}），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: three operators ----------------
fig, axes = plt.subplots(1, 3, figsize=(11.0, 4.0))

# (a) gradient: contours + arrows
ax = axes[0]
x = np.linspace(-1.5, 1.5, 80)
y = np.linspace(-1.5, 1.5, 80)
X, Y = np.meshgrid(x, y)
F = X ** 2 + Y ** 2
ax.contour(X, Y, F, levels=8, colors="0.7", linewidths=0.8)
gx, gy = 2 * X, 2 * Y
ax.quiver(X[::10, ::10], Y[::10, ::10], gx[::10, ::10], gy[::10, ::10],
          color="tab:blue", angles="xy", scale=40, width=0.005)
ax.set_title("gradient: scalar -> vector", fontsize=9)
ax.set_aspect("equal")

# (b) divergence: source/sink
ax = axes[1]
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal")
for (cx, cy, s) in [(0.0, 0.0, 1.0), (-0.9, 0.8, -0.7)]:
    for r in [0.25, 0.5, 0.75]:
        th = np.linspace(0, 2 * np.pi, 60)
        ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), color="tab:red" if s > 0 else "tab:green", lw=0.9)
    ax.annotate("", xy=(cx + 1.15, cy), xytext=(cx + 0.85, cy),
                arrowprops=dict(arrowstyle="-|>", color="tab:red" if s > 0 else "tab:green", lw=1.5))
ax.set_title("divergence: source / sink", fontsize=9)

# (c) curl: rotating field
ax = axes[2]
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal")
th = np.linspace(0, 2 * np.pi, 9)[:-1]
for r in [0.45, 0.9, 1.3]:
    cx = r * np.cos(th); cy = r * np.sin(th)
    ax.quiver(cx, cy, -cy, cx, color="tab:purple", angles="xy", scale=12, width=0.006)
ax.set_title("curl: rotation", fontsize=9)

fig.tight_layout()
fig.savefig(OUT / "lec22_fig1_operators.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: gradient field is curl-free (closed loop) ----------------
fig, ax = plt.subplots(figsize=(5.6, 4.6))
x = np.linspace(-1.5, 1.5, 80)
y = np.linspace(-1.5, 1.5, 80)
X, Y = np.meshgrid(x, y)
F = X ** 2 + 2 * Y ** 2
ax.contour(X, Y, F, levels=8, colors="0.75", linewidths=0.8)
ax.quiver(X[::11, ::11], Y[::11, ::11], 2 * X[::11, ::11], 4 * Y[::11, ::11],
          color="tab:blue", angles="xy", scale=45, width=0.005)
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(0.8 * np.cos(th), 0.55 * np.sin(th), color="tab:red", lw=2.0)
ax.annotate("", xy=(0.8 * np.cos(0.2), 0.55 * np.sin(0.2)),
            xytext=(0.8 * np.cos(0.35), 0.55 * np.sin(0.35)),
            arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=1.8))
ax.text(0.05, 0.75, "closed loop: circulation 0", fontsize=9, color="tab:red")
ax.set_aspect("equal")
ax.set_title(r"gradient field is curl-free: $\nabla\times\nabla f=0$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec22_fig2_grad_curl.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: curl field is divergence-free (closed streamlines) ----------------
fig, ax = plt.subplots(figsize=(5.6, 4.6))
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal")
for r in [0.4, 0.75, 1.1, 1.4]:
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(r * np.cos(th), r * np.sin(th), color="tab:purple", lw=1.4)
    for a in [0.4, 2.2, 4.0]:
        ax.annotate("", xy=(r * np.cos(a + 0.12), r * np.sin(a + 0.12)),
                    xytext=(r * np.cos(a), r * np.sin(a)),
                    arrowprops=dict(arrowstyle="-|>", color="tab:purple", lw=1.4))
ax.text(-1.35, 1.35, "closed streamlines: no source/sink", fontsize=9, color="tab:purple")
ax.set_title(r"curl field is divergence-free: $\nabla\cdot(\nabla\times F)=0$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec22_fig3_curl_div.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec22_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
