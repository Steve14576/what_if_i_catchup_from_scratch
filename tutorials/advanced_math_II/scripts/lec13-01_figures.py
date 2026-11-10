# 规模纪律：4 张静态 SVG, 目标 < 4 秒。
# 第 13 讲图：极坐标面积元、三种区域、雅可比、心形线。
# 图内文字只用 ASCII 与 mathtext，不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- fig 1: polar grid and the area element ----------------
fig, ax = plt.subplots(figsize=(5.6, 5.2))
th = np.linspace(0, 2 * np.pi, 400)
for r in [0.25, 0.5, 0.75, 1.0]:
    ax.plot(r * np.cos(th), r * np.sin(th), color="0.8", lw=0.9)
for k in range(12):
    a = k * np.pi / 6
    ax.plot([0, np.cos(a)], [0, np.sin(a)], color="0.8", lw=0.9)
# highlight one cell
r0, th0 = 0.6, np.pi / 6
dr, dth = 0.2, np.pi / 6
tt = np.linspace(th0, th0 + dth, 30)
ax.fill(np.concatenate([r0 * np.cos(tt), (r0 + dr) * np.cos(tt[::-1])]),
        np.concatenate([r0 * np.sin(tt), (r0 + dr) * np.sin(tt[::-1])]),
        color="tab:red", alpha=0.35)
ax.annotate("", xy=(r0 + dr, 0.0), xytext=(r0, 0.0),
            arrowprops=dict(arrowstyle="<->", color="tab:red", lw=1.4))
ax.text(0.62, -0.07, r"$dr$", color="tab:red", fontsize=10)
ax.text(0.2, 0.42, r"$r\,d\theta$", color="tab:red", fontsize=10)
ax.text(0.05, 0.03, "O", fontsize=9)
ax.set_aspect("equal")
ax.set_xlim(-0.1, 1.15); ax.set_ylim(-1.15, 1.15)
ax.set_title(r"polar grid: cell area $\approx r\,dr\,d\theta$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec13_fig1_area_element.svg", format="svg")
plt.close(fig)

# ---------------- fig 2: disk, sector, annulus ----------------
fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.7))
th = np.linspace(0, 2 * np.pi, 400)
ax = axes[0]
ax.fill(np.cos(th), np.sin(th), color="tab:blue", alpha=0.25)
ax.plot(np.cos(th), np.sin(th), color="tab:blue", lw=1.5)
ax.set_title(r"disk: $0 ≤ \theta ≤ 2\pi,\ 0 ≤ r ≤ R$", fontsize=8)
ax = axes[1]
tt = np.linspace(0, np.pi / 3, 100)
ax.fill(np.concatenate([[0], np.cos(tt)]), np.concatenate([[0], np.sin(tt)]),
        color="tab:green", alpha=0.25)
ax.plot([0, 1], [0, 0], color="tab:green", lw=1.3)
ax.plot(np.cos(tt), np.sin(tt), color="tab:green", lw=1.5)
ax.set_title(r"sector: $0 ≤ \theta ≤ \alpha$", fontsize=8)
ax = axes[2]
ax.fill(np.concatenate([np.cos(th), 0.5 * np.cos(th[::-1])]),
        np.concatenate([np.sin(th), 0.5 * np.sin(th[::-1])]),
        color="tab:orange", alpha=0.3)
ax.plot(np.cos(th), np.sin(th), color="tab:orange", lw=1.4)
ax.plot(0.5 * np.cos(th), 0.5 * np.sin(th), color="tab:orange", lw=1.4)
ax.set_title(r"annulus: $a ≤ r ≤ b$", fontsize=8)
for ax in axes:
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
    ax.grid(alpha=0.15)
    ax.axhline(0, color="0.85", lw=0.6); ax.axvline(0, color="0.85", lw=0.6)
fig.tight_layout()
fig.savefig(OUT / "lec13_fig2_regions.svg", format="svg")
plt.close(fig)

# ---------------- fig 4: Jacobian as area scaling ----------------
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4))
ax = axes[0]
for k in range(5):
    ax.plot([k / 4, k / 4], [0, 1], color="0.8", lw=0.8)
    ax.plot([0, 1], [k / 4, k / 4], color="0.8", lw=0.8)
ax.add_patch(plt.Rectangle((0.5, 0.5), 0.25, 0.25, color="tab:blue", alpha=0.35))
ax.set_title("uv-plane: cell area $du\\,dv$", fontsize=9)
ax = axes[1]
# map (u,v) -> (u + v/2, u/2 + v)
for k in range(5):
    u = k / 4
    ax.plot([u, u + 0.5], [u / 2, u / 2 + 1], color="0.8", lw=0.8)
    v = k / 4
    ax.plot([v / 2, 0.5 + v / 2], [v, 1 + v], color="0.8", lw=0.8)
ax.fill([0.75, 1.0, 1.25, 1.0], [0.75, 0.625, 0.875, 1.0], color="tab:red", alpha=0.4)
ax.set_title(r"xy-plane: parallelogram, area $|J|\,du\,dv$", fontsize=9)
for ax in axes:
    ax.set_aspect("equal")
    ax.grid(alpha=0.1)
    ax.set_xlim(-0.1, 1.5); ax.set_ylim(-0.1, 1.6)
fig.tight_layout()
fig.savefig(OUT / "lec13_fig4_jacobian.svg", format="svg")
plt.close(fig)

# ---------------- fig 3: cardioid region ----------------
fig, ax = plt.subplots(figsize=(5.6, 5.0))
th = np.linspace(0, 2 * np.pi, 500)
r = 1 + np.cos(th)
ax.fill(r * np.cos(th), r * np.sin(th), color="tab:purple", alpha=0.25)
ax.plot(r * np.cos(th), r * np.sin(th), color="tab:purple", lw=1.8)
for a in [0, np.pi / 3, 2 * np.pi / 3, np.pi]:
    rr = 1 + np.cos(a)
    ax.plot([0, rr * np.cos(a)], [0, rr * np.sin(a)], color="0.5", lw=0.8, ls="--")
ax.text(0.02, 0.04, "O", fontsize=9)
ax.set_aspect("equal")
ax.set_xlim(-1.2, 2.3); ax.set_ylim(-1.6, 1.6)
ax.grid(alpha=0.15)
ax.set_title(r"cardioid: $0 ≤ r ≤ 1+\cos\theta$", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lec13_fig3_cardioid.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec13_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
