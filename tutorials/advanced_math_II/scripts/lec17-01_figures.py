# 规模纪律：4 张静态 SVG, 目标 < 4 秒。
# 第 17 讲图：做功、方向、两类关系、闭合曲线。
# 图内文字只用 ASCII 与 mathtext（≤ 用 Unicode），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: work as a dot product ----------------
fig, ax = plt.subplots(figsize=(6.2, 4.4))
x = np.linspace(0, 2.4, 400)
y = 0.4 + 0.5 * np.sin(1.5 * x)
ax.plot(x, y, color="tab:blue", lw=2.0)
x0 = 1.2
y0 = 0.4 + 0.5 * np.sin(1.5 * x0)
dx, dy = 0.45, 0.30
ax.annotate("", xy=(x0 + dx, y0 + dy), xytext=(x0, y0),
            arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=2.0))
ax.annotate("", xy=(x0 + 0.55, y0 + 0.12), xytext=(x0, y0),
            arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=2.0))
ax.text(x0 + dx + 0.03, y0 + dy, r"$(\Delta x,\Delta y)$", color="tab:red", fontsize=9)
ax.text(x0 + 0.5, y0 - 0.16, r"$F=(P,Q)$", color="tab:green", fontsize=9)
ax.plot([x0, x0 + dx], [y0, y0], color="0.5", lw=1.0, ls="--")
ax.plot([x0 + dx, x0 + dx], [y0, y0 + dy], color="0.5", lw=1.0, ls="--")
ax.text(x0 + dx / 2, y0 - 0.08, r"$\Delta x$", fontsize=9, ha="center")
ax.text(x0 + dx + 0.02, y0 + dy / 2, r"$\Delta y$", fontsize=9)
ax.text(0.05, 1.15, r"$\Delta W\approx P\,\Delta x+Q\,\Delta y$", fontsize=11)
ax.set_xlim(0, 2.6); ax.set_ylim(0.0, 1.25)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"work: force dot displacement", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec17_fig1_work.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: direction reverses the sign ----------------
fig, ax = plt.subplots(figsize=(5.8, 4.4))
t = np.linspace(0, np.pi, 300)
ax.plot(np.cos(t), np.sin(t), color="tab:blue", lw=2.2)
ax.annotate("", xy=(np.cos(0.25 * np.pi), np.sin(0.25 * np.pi) + 0.08),
            xytext=(np.cos(0.7 * np.pi), np.sin(0.7 * np.pi) + 0.08),
            arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=1.9))
ax.annotate("", xy=(np.cos(0.7 * np.pi), np.sin(0.7 * np.pi) - 0.08),
            xytext=(np.cos(0.25 * np.pi), np.sin(0.25 * np.pi) - 0.08),
            arrowprops=dict(arrowstyle="-|>", color="tab:orange", lw=1.9))
ax.text(-0.2, 0.60, r"$A\to B$: $+\int$", color="tab:green", fontsize=10)
ax.text(-0.2, 0.28, r"$B\to A$: $-\int$", color="tab:orange", fontsize=10)
ax.set_aspect("equal")
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-0.2, 1.25)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"second kind: reversing the direction flips the sign", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec17_fig2_direction.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: dx, dy are projections of ds ----------------
fig, ax = plt.subplots(figsize=(5.8, 4.6))
x = np.linspace(0, 2.0, 400)
y = 0.4 + 0.4 * np.sin(1.3 * x)
ax.plot(x, y, color="tab:blue", lw=2.0)
x0 = 1.0
y0 = 0.4 + 0.4 * np.sin(1.3 * x0)
slope = 0.4 * 1.3 * np.cos(1.3 * x0)
ax.annotate("", xy=(x0 + 0.5, y0 + 0.5 * slope), xytext=(x0, y0),
            arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=1.8))
ax.plot([x0, x0 + 0.5], [y0, y0], color="0.45", lw=1.0, ls="--")
ax.plot([x0 + 0.5, x0 + 0.5], [y0, y0 + 0.5 * slope], color="0.45", lw=1.0, ls="--")
ax.text(x0 + 0.24, y0 - 0.07, r"$dx=\cos\alpha\,ds$", fontsize=9, ha="center")
ax.text(x0 + 0.52, y0 + 0.5 * slope / 2, r"$dy=\cos\beta\,ds$", fontsize=9)
ax.text(x0 + 0.28, y0 + 0.30, r"$e_\tau$", color="tab:red", fontsize=10)
ax.set_xlim(0, 2.4); ax.set_ylim(0.0, 1.35)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"$dx,dy$ are signed projections of $ds$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec17_fig4_relation.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: closed curve, counterclockwise ----------------
fig, ax = plt.subplots(figsize=(5.4, 5.0))
t = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(t), np.sin(t), color="tab:blue", lw=2.2)
for a in [0.2, 1.8, 3.4, 5.0]:
    b = a + 0.5
    ax.annotate("", xy=(np.cos(b), np.sin(b)), xytext=(np.cos(a), np.sin(a)),
                arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=1.8))
ax.text(-0.95, 0.85, r"$\oint_L -y\,dx+x\,dy=2\pi$", fontsize=11)
ax.text(-0.95, -1.25, r"$=2\times$ area", fontsize=10)
ax.set_aspect("equal")
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.4, 1.2)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"closed curve: positive = counterclockwise", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec17_fig3_closed.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec17_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
