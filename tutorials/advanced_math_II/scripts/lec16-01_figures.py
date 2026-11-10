# 规模纪律：4 张静态 SVG, 目标 < 4 秒。
# 第 16 讲图：小段弦长、参数曲线 ds、线密度质量、方向无关。
# 图内文字只用 ASCII 与 mathtext（≤ 用 Unicode），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: chord approximation ----------------
fig, ax = plt.subplots(figsize=(6.2, 4.2))
x = np.linspace(0, 2.2, 400)
y = 0.5 + 0.4 * np.sin(1.8 * x)
ax.plot(x, y, color="tab:blue", lw=2.0)
x0, x1 = 0.85, 1.15
y0 = 0.5 + 0.4 * np.sin(1.8 * x0)
y1 = 0.5 + 0.4 * np.sin(1.8 * x1)
ax.plot([x0, x1], [y0, y1], color="tab:red", lw=2.2)
ax.scatter([x0, x1], [y0, y1], color="k", s=28, zorder=5)
ax.plot([x0, x1], [y0, y0], color="0.4", lw=1.0, ls="--")
ax.plot([x1, x1], [y0, y1], color="0.4", lw=1.0, ls="--")
ax.text((x0 + x1) / 2, y0 - 0.07, r"$\Delta x$", fontsize=10, ha="center")
ax.text(x1 + 0.03, (y0 + y1) / 2, r"$\Delta y$", fontsize=10)
ax.text((x0 + x1) / 2 - 0.12, (y0 + y1) / 2 + 0.09, r"$\Delta s$", color="tab:red", fontsize=11)
ax.set_xlim(0, 2.3); ax.set_ylim(0.0, 1.1)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"one small piece: $\Delta s\approx\sqrt{(\Delta x)^2+(\Delta y)^2}$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec16_fig1_chord.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: parametric ds = |r'(t)| dt ----------------
fig, ax = plt.subplots(figsize=(6.0, 4.8))
t = np.linspace(0, 2 * np.pi, 400)
X, Y = 2 * np.cos(t), np.sin(t)
ax.plot(X, Y, color="tab:blue", lw=2.0)
t0 = np.pi / 3
p = np.array([2 * np.cos(t0), np.sin(t0)])
v = np.array([-2 * np.sin(t0), np.cos(t0)])
v = v / np.linalg.norm(v) * 0.8
ax.annotate("", xy=p + v, xytext=p,
            arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=1.8))
ax.scatter([p[0]], [p[1]], color="k", s=26, zorder=5)
ax.text(p[0] + v[0] + 0.04, p[1] + v[1], r"$(x',y')$", color="tab:red", fontsize=10)
ax.text(-0.4, 1.25, r"$ds=\sqrt{(x')^2+(y')^2}\,dt$", fontsize=11)
ax.set_aspect("equal")
ax.set_xlim(-2.3, 2.3); ax.set_ylim(-1.4, 1.5)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"parametric curve: $ds$ = speed $\times\,dt$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec16_fig2_param.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: mass of a wire (density varies) ----------------
fig, ax = plt.subplots(figsize=(6.2, 4.2))
x = np.linspace(0, 3, 400)
y = 1.0 + 0.45 * np.sin(1.5 * x)
rho = 1 + x
pts = np.array([x, y]).T.reshape(-1, 1, 2)
segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
lc = LineCollection(segs, cmap="viridis", linewidths=7)
lc.set_array(rho[:-1])
ax.add_collection(lc)
x0 = 1.9
y0 = 1.0 + 0.45 * np.sin(1.5 * x0)
ax.plot([x0, x0], [y0 - 0.18, y0 + 0.18], color="tab:red", lw=2.0)
ax.text(x0 + 0.06, y0 + 0.2, r"$\rho\,ds$", color="tab:red", fontsize=10)
ax.text(0.05, 1.62, r"density $\rho(x)$ grows to the right", fontsize=9)
ax.set_xlim(0, 3.1); ax.set_ylim(0.35, 1.75)
ax.set_xlabel("x")
ax.set_title(r"mass of a wire: $\int_L\rho\,ds$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec16_fig3_mass.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: direction independence ----------------
fig, ax = plt.subplots(figsize=(5.8, 4.4))
t = np.linspace(0, np.pi, 300)
ax.plot(np.cos(t), np.sin(t), color="tab:blue", lw=2.2)
# forward arrow (upper offset)
ax.annotate("", xy=(np.cos(0.25 * np.pi), np.sin(0.25 * np.pi) + 0.08),
            xytext=(np.cos(0.65 * np.pi), np.sin(0.65 * np.pi) + 0.08),
            arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=1.8))
# backward arrow (lower offset)
ax.annotate("", xy=(np.cos(0.65 * np.pi), np.sin(0.65 * np.pi) - 0.08),
            xytext=(np.cos(0.25 * np.pi), np.sin(0.25 * np.pi) - 0.08),
            arrowprops=dict(arrowstyle="-|>", color="tab:orange", lw=1.8))
ax.text(-0.15, 0.62, "A to B", color="tab:green", fontsize=9)
ax.text(-0.15, 0.30, "B to A", color="tab:orange", fontsize=9)
ax.text(-1.25, 0.95, r"same value: $\int_L f\,ds$", fontsize=11)
ax.set_aspect("equal")
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-0.2, 1.25)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"first kind: $ds>0$, no direction", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec16_fig4_direction.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec16_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
