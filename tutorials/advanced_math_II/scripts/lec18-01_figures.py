# 规模纪律：4 张静态 SVG, 目标 < 4 秒。
# 第 18 讲图：矩形推导、正向边界、路径无关、多连通。
# 图内文字只用 ASCII 与 mathtext（≤ 用 Unicode；不用 \mathbf / \oint），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: rectangle, counterclockwise ----------------
fig, ax = plt.subplots(figsize=(6.2, 4.6))
ax.add_patch(plt.Rectangle((0.5, 0.5), 2.0, 1.2, fill=False, edgecolor="tab:blue", lw=2.0))
edges = [((0.5, 0.5), (2.5, 0.5)), ((2.5, 0.5), (2.5, 1.7)),
         ((2.5, 1.7), (0.5, 1.7)), ((0.5, 1.7), (0.5, 0.5))]
for a, b in edges:
    ax.annotate("", xy=(a[0] + 0.85 * (b[0] - a[0]), a[1] + 0.85 * (b[1] - a[1])),
                xytext=a, arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=1.8))
ax.text(1.4, 0.34, r"$y=c$", fontsize=9)
ax.text(1.4, 1.78, r"$y=d$", fontsize=9)
ax.text(0.28, 1.05, r"$x=a$", fontsize=9, rotation=90)
ax.text(2.55, 1.05, r"$x=b$", fontsize=9, rotation=90)
ax.text(1.3, 1.0, r"$D$", fontsize=12)
ax.text(0.15, 2.05, r"$\int_L P\,dx+Q\,dy=\iint_D(Q_x-P_y)\,d\sigma$", fontsize=10)
ax.set_xlim(0, 3.4); ax.set_ylim(0.1, 2.2)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"Green: start from the four sides of a rectangle", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec18_fig1_rect.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: partition, inner edges cancel ----------------
fig, ax = plt.subplots(figsize=(6.2, 4.6))
ax.add_patch(plt.Rectangle((0.4, 0.4), 2.4, 1.4, fill=False, edgecolor="tab:blue", lw=2.0))
ax.plot([1.6, 1.6], [0.4, 1.8], color="0.45", lw=1.2, ls="--")
ax.plot([0.4, 2.8], [1.1, 1.1], color="0.45", lw=1.2, ls="--")
for a, b in [((0.4, 0.4), (2.8, 0.4)), ((2.8, 0.4), (2.8, 1.8)),
             ((2.8, 1.8), (0.4, 1.8)), ((0.4, 1.8), (0.4, 0.4))]:
    ax.annotate("", xy=(a[0] + 0.8 * (b[0] - a[0]), a[1] + 0.8 * (b[1] - a[1])), xytext=a,
                arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=1.5))
ax.annotate("", xy=(1.6, 1.55), xytext=(1.6, 0.65),
            arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=1.5))
ax.annotate("", xy=(1.62, 0.7), xytext=(1.62, 1.6),
            arrowprops=dict(arrowstyle="-|>", color="tab:orange", lw=1.5))
ax.text(1.68, 1.15, "cancel", fontsize=8, color="tab:red")
ax.text(0.5, 1.55, r"$A$", fontsize=10)
ax.text(2.2, 0.55, r"$B$", fontsize=10)
ax.set_xlim(0.2, 3.0); ax.set_ylim(0.2, 2.0)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"partition: shared inner edges run in opposite directions", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec18_fig2_partition.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: positive boundary ----------------
fig, ax = plt.subplots(figsize=(5.6, 4.8))
t = np.linspace(0, 2 * np.pi, 400)
r = 1 + 0.18 * np.sin(3 * t)
ax.fill(r * np.cos(t), r * np.sin(t), color="tab:blue", alpha=0.12)
ax.plot(r * np.cos(t), r * np.sin(t), color="tab:blue", lw=2.0)
for a in [0.1, 1.7, 3.3, 4.9]:
    b = a + 0.35
    ax.annotate("", xy=(np.interp(b, t, r * np.cos(t)), np.interp(b, t, r * np.sin(t))),
                xytext=(np.interp(a, t, r * np.cos(t)), np.interp(a, t, r * np.sin(t))),
                arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=1.8))
ax.text(-0.85, 1.12, "region on the left", fontsize=9)
ax.text(-0.2, 0.0, r"$D$", fontsize=12)
ax.set_aspect("equal")
ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.3, 1.3)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"positive boundary: counterclockwise", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec18_fig3_positive.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: path independence ----------------
fig, ax = plt.subplots(figsize=(6.0, 4.2))
A, B = np.array([0.0, 0.0]), np.array([2.0, 1.0])
ax.plot([A[0], B[0]], [A[1], B[1]], color="tab:green", lw=2.0)
x = np.linspace(0, 2, 200)
ax.plot(x, 0.25 * x + 0.25 * x * (2 - x), color="tab:orange", lw=2.0)
ax.scatter([A[0], B[0]], [A[1], B[1]], color="k", s=30, zorder=5)
ax.text(-0.12, -0.1, "A", fontsize=11)
ax.text(2.03, 0.95, "B", fontsize=11)
ax.text(0.85, 0.62, "path 1", color="tab:green", fontsize=9)
ax.text(1.15, 0.12, "path 2", color="tab:orange", fontsize=9)
ax.text(0.2, 1.35, r"$P_y=Q_x$: both paths give the same value", fontsize=10)
ax.set_xlim(-0.2, 2.4); ax.set_ylim(-0.2, 1.5)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"path independence on a simply connected region", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec18_fig4_paths.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: multiply connected (annulus) ----------------
fig, ax = plt.subplots(figsize=(5.6, 5.2))
t = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(t), np.sin(t), color="tab:blue", lw=2.0)
ax.plot(0.4 * np.cos(t), 0.4 * np.sin(t), color="tab:blue", lw=2.0)
for a in [0.2, 1.8, 3.4, 5.0]:
    b = a + 0.3
    ax.annotate("", xy=(np.cos(b), np.sin(b)), xytext=(np.cos(a), np.sin(a)),
                arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=1.8))
    ax.annotate("", xy=(0.4 * np.cos(a), 0.4 * np.sin(a)),
                xytext=(0.4 * np.cos(b), 0.4 * np.sin(b)),
                arrowprops=dict(arrowstyle="-|>", color="tab:orange", lw=1.8))
ax.plot([0.4, 1.0], [0.15, 0.15], color="0.45", lw=1.2, ls="--")
ax.text(-1.25, 1.12, "outer: CCW", color="tab:green", fontsize=9)
ax.text(-1.25, -1.25, "inner: CW", color="tab:orange", fontsize=9)
ax.text(0.55, 0.19, "cut", fontsize=8, color="0.4")
ax.set_aspect("equal")
ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.4, 1.3)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"multiply connected: outer CCW, inner CW", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec18_fig5_multiply.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec18_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
