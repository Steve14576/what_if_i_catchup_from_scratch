# 规模纪律：14 张静态 SVG, 目标 < 8 秒。
# 第 11 讲 §0：一重/二重/三重的每一种"值"各一张图。
#   一重 4：面积、带符号面积、线质量、变力做功
#   二重 5：曲顶柱体体积、面积、面质量、质心、转动惯量
#   三重 4：体积、体质量、质心、转动惯量
#   另 1：长度元/面积元/体积元嵌套
# 图内文字只用 ASCII 与 mathtext（≤ 用 Unicode），不放中文。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, format="svg")
    plt.close(fig)


# ================= 一重 integral =================

# fig 0-01: area under a curve (f >= 0)
fig, ax = plt.subplots(figsize=(6.2, 4.2))
x = np.linspace(0, 3, 400)
f = 1 + x / 3 + np.sin(2 * x) / 2
ax.plot(x, f, color="tab:blue", lw=2.0)
ax.fill_between(x, 0, f, color="tab:blue", alpha=0.18)
x0, w = 1.6, 0.16
y0 = 1 + x0 / 3 + np.sin(2 * x0) / 2
ax.add_patch(plt.Rectangle((x0 - w / 2, 0), w, y0, color="tab:red", alpha=0.35))
ax.text(x0, -0.16, r"$dx$", color="tab:red", fontsize=10, ha="center")
ax.text(x0 + w / 2 + 0.06, y0 / 2, r"$f(x)$", color="tab:red", fontsize=10)
ax.plot([0, 3], [0, 0], color="k", lw=1.0)
ax.set_xlim(-0.05, 3.1); ax.set_ylim(0, 2.6)
ax.set_xlabel("x"); ax.set_ylabel("value")
ax.set_title(r"1) area: bars $f(x)\,dx$, summed", fontsize=10)
save(fig, "lec11_fig0_01_single_area.svg")

# fig 0-02: signed area (f changes sign)
fig, ax = plt.subplots(figsize=(6.2, 4.0))
x = np.linspace(0, 2 * np.pi, 500)
s = np.sin(x)
ax.plot(x, s, color="k", lw=1.8)
ax.fill_between(x, 0, s, where=(s >= 0), color="tab:blue", alpha=0.30)
ax.fill_between(x, 0, s, where=(s < 0), color="tab:red", alpha=0.30)
ax.axhline(0, color="0.5", lw=1.0)
ax.text(np.pi / 2, 0.55, "positive", ha="center", fontsize=9, color="tab:blue")
ax.text(3 * np.pi / 2, -0.62, "negative", ha="center", fontsize=9, color="tab:red")
ax.set_xlim(0, 2 * np.pi); ax.set_ylim(-1.25, 1.25)
ax.set_xlabel("x"); ax.set_ylabel("f(x)")
ax.set_title(r"2) signed area: $\int_0^{2\pi}\sin x\,dx=0$", fontsize=10)
save(fig, "lec11_fig0_02_single_signed.svg")

# fig 0-03: mass of a rod with linear density
fig, ax = plt.subplots(figsize=(6.2, 3.0))
x = np.linspace(0, 1, 400)
rho = 1 + x
pts = np.array([x, np.zeros_like(x)]).T.reshape(-1, 1, 2)
segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
lc = LineCollection(segs, cmap="viridis", linewidths=9)
lc.set_array(rho[:-1])
ax.add_collection(lc)
x0, wd = 0.62, 0.06
ax.plot([x0, x0], [-0.28, 0.28], color="tab:red", lw=2.0)
ax.text(x0 + 0.02, 0.34, r"$\rho(x)\,dx$", color="tab:red", fontsize=9)
ax.text(0.05, 0.34, r"density $\rho(x)=1+x$", fontsize=9)
ax.set_xlim(-0.05, 1.08); ax.set_ylim(-0.45, 0.55)
ax.set_yticks([]); ax.set_xlabel("x")
ax.set_title(r"3) mass of a rod: $\int_0^1(1+x)\,dx=1.5$", fontsize=10)
save(fig, "lec11_fig0_03_single_mass.svg")

# fig 0-04: work of a variable force
fig, ax = plt.subplots(figsize=(6.2, 4.2))
x = np.linspace(0, 2, 300)
F = 1 + 0.6 * x
ax.plot(x, F, color="tab:green", lw=2.0)
ax.fill_between(x, 0, F, color="tab:green", alpha=0.18)
x0, wd = 1.2, 0.12
y0 = 1 + 0.6 * x0
ax.add_patch(plt.Rectangle((x0 - wd / 2, 0), wd, y0, color="tab:red", alpha=0.35))
ax.text(x0, -0.16, r"$dx$", color="tab:red", fontsize=10, ha="center")
ax.text(x0 + wd / 2 + 0.05, y0 / 2, r"$F(x)$", color="tab:red", fontsize=10)
ax.set_xlim(-0.05, 2.05); ax.set_ylim(0, 2.5)
ax.set_xlabel("displacement x"); ax.set_ylabel("force F")
ax.set_title(r"4) work: $\int_0^2(1+0.6x)\,dx=3.2$", fontsize=10)
save(fig, "lec11_fig0_04_single_work.svg")

# ================= 二重 integral =================

# fig 0-05: volume under a surface (solid)
fig = plt.figure(figsize=(6.2, 5.0))
ax = fig.add_subplot(projection="3d")
u = np.linspace(0, 1, 25)
U, V = np.meshgrid(u, u)
Z = 0.4 + 0.8 * (U ** 2 + V ** 2)
ax.plot_surface(U, V, Z, cmap="viridis", alpha=0.55, linewidth=0, rstride=2, cstride=2)
ax.plot_surface(U, V, np.zeros_like(U), color="0.8", alpha=0.35, linewidth=0, rstride=2, cstride=2)
cx, cy, cs = 0.6, 0.4, 0.14
corners = [(cx, cy), (cx + cs, cy), (cx + cs, cy + cs), (cx, cy + cs)]
for (a, b) in corners:
    h = 0.4 + 0.8 * (a ** 2 + b ** 2)
    ax.plot([a, a], [b, b], [0, h], color="tab:red", lw=1.2)
top = [(a, b, 0.4 + 0.8 * (a ** 2 + b ** 2)) for (a, b) in corners]
ax.plot([p[0] for p in top] + [top[0][0]], [p[1] for p in top] + [top[0][1]],
        [p[2] for p in top] + [top[0][2]], color="tab:red", lw=1.2)
ax.plot([cx, cx + cs, cx + cs, cx, cx], [cy, cy, cy + cs, cy + cs, cy],
        [0, 0, 0, 0, 0], color="tab:red", lw=1.4)
ax.text(cx + 0.02, cy - 0.2, 0.05, r"$d\sigma$", color="tab:red", fontsize=9)
ax.text(cx + cs + 0.05, cy + cs, 1.35, r"$f$", color="tab:red", fontsize=10)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 2.2)
ax.set_box_aspect((1, 1, 1.35))
ax.view_init(elev=20, azim=-60)
ax.set_title(r"5) volume: columns $f\,d\sigma$, summed", fontsize=10)
save(fig, "lec11_fig0_05_double_volume.svg")

# fig 0-06: area (f = 1)
fig, ax = plt.subplots(figsize=(5.4, 5.0))
th = np.linspace(0, 2 * np.pi, 300)
ax.fill(np.cos(th), np.sin(th), color="tab:blue", alpha=0.15)
ax.plot(np.cos(th), np.sin(th), color="tab:blue", lw=1.8)
for g in np.linspace(-1, 1, 9):
    ax.plot([g, g], [-1, 1], color="0.85", lw=0.6)
    ax.plot([-1, 1], [g, g], color="0.85", lw=0.6)
ax.add_patch(plt.Rectangle((0.48, 0.24), 0.18, 0.18, facecolor="tab:red", alpha=0.4))
ax.text(0.6, 0.55, r"$d\sigma$", color="tab:red", fontsize=10, ha="center")
ax.set_aspect("equal")
ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.15, 1.15)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"6) area: $\iint_D 1\,d\sigma=\pi$ for the unit disk", fontsize=10)
save(fig, "lec11_fig0_06_double_area.svg")

# fig 0-07: mass of a lamina with areal density
fig, ax = plt.subplots(figsize=(5.6, 4.8))
xx, yy = np.meshgrid(np.linspace(0, 1, 200), np.linspace(0, 1, 200))
rho = xx + yy
im = ax.imshow(rho, origin="lower", extent=[0, 1, 0, 1], cmap="viridis", alpha=0.85)
ax.add_patch(plt.Rectangle((0.55, 0.45), 0.12, 0.12, fill=False, edgecolor="tab:red", lw=2.0))
ax.text(0.62, 0.35, r"$\rho\,d\sigma$", color="tab:red", fontsize=10, ha="center")
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"7) mass: $\iint_{[0,1]^2}(x+y)\,d\sigma=1$", fontsize=10)
save(fig, "lec11_fig0_07_double_mass.svg")

# fig 0-08: centroid (first moment)
fig, ax = plt.subplots(figsize=(5.6, 4.8))
xx, yy = np.meshgrid(np.linspace(0, 1, 200), np.linspace(0, 1, 200))
rho = xx + yy
ax.imshow(rho, origin="lower", extent=[0, 1, 0, 1], cmap="viridis", alpha=0.55)
cx, cy = 7 / 12, 7 / 12
ax.plot([0, cx], [0, cy], color="k", lw=1.0, ls="--")
ax.plot([cx, cx], [0, cy], color="tab:red", lw=1.0, ls=":")
ax.plot([0, cx], [cy, cy], color="tab:red", lw=1.0, ls=":")
ax.scatter([cx], [cy], color="tab:red", s=55, zorder=5)
ax.text(cx + 0.04, cy + 0.04, r"$(\bar x,\bar y)=(7/12,7/12)$", fontsize=9, color="tab:red")
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"8) centroid: $\bar x=M_{yz}/m$, $\bar y=M_{zx}/m$", fontsize=10)
save(fig, "lec11_fig0_08_double_centroid.svg")

# fig 0-09: moment of inertia (second moment)
fig, ax = plt.subplots(figsize=(5.4, 5.0))
th = np.linspace(0, 2 * np.pi, 300)
ax.fill(np.cos(th), np.sin(th), color="tab:orange", alpha=0.15)
ax.plot(np.cos(th), np.sin(th), color="tab:orange", lw=1.8)
for rr in [0.33, 0.66]:
    ax.plot(rr * np.cos(th), rr * np.sin(th), color="0.8", lw=0.8)
# axis out of the page: two small circles at the origin
ax.plot(0.06 * np.cos(th), 0.06 * np.sin(th), color="k", lw=1.2)
ax.plot(0.025 * np.cos(th), 0.025 * np.sin(th), color="k", lw=1.2)
ax.text(0.08, 0.06, r"$z$ axis", fontsize=9)
ax.annotate("", xy=(0.75, 0.55), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=1.6))
ax.text(0.30, 0.36, r"$r$", color="tab:red", fontsize=11)
ax.set_aspect("equal")
ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.15, 1.15)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"9) inertia: $I_z=\iint r^2\rho\,d\sigma$", fontsize=10)
save(fig, "lec11_fig0_09_double_inertia.svg")

# ================= 三重 integral =================

# fig 0-10: volume (f = 1)
fig = plt.figure(figsize=(6.0, 5.0))
ax = fig.add_subplot(projection="3d")
edges = [((0,0,0),(1,0,0)), ((1,0,0),(1,1,0)), ((1,1,0),(0,1,0)), ((0,1,0),(0,0,0)),
         ((0,0,1),(1,0,1)), ((1,0,1),(1,1,1)), ((1,1,1),(0,1,1)), ((0,1,1),(0,0,1)),
         ((0,0,0),(0,0,1)), ((1,0,0),(1,0,1)), ((1,1,0),(1,1,1)), ((0,1,0),(0,1,1))]
for a, b in edges:
    ax.plot([a[0], b[0]], [a[1], b[1]], [a[2], b[2]], color="0.55", lw=1.0)
x0, y0, z0, s = 0.55, 0.4, 0.45, 0.2
cell = [((x0,y0,z0),(x0+s,y0,z0)), ((x0+s,y0,z0),(x0+s,y0+s,z0)),
        ((x0+s,y0+s,z0),(x0,y0+s,z0)), ((x0,y0+s,z0),(x0,y0,z0)),
        ((x0,y0,z0+s),(x0+s,y0,z0+s)), ((x0+s,y0,z0+s),(x0+s,y0+s,z0+s)),
        ((x0+s,y0+s,z0+s),(x0,y0+s,z0+s)), ((x0,y0+s,z0+s),(x0,y0,z0+s)),
        ((x0,y0,z0),(x0,y0,z0+s)), ((x0+s,y0,z0),(x0+s,y0,z0+s)),
        ((x0+s,y0+s,z0),(x0+s,y0+s,z0+s)), ((x0,y0+s,z0),(x0,y0+s,z0+s))]
for a, b in cell:
    ax.plot([a[0], b[0]], [a[1], b[1]], [a[2], b[2]], color="tab:red", lw=1.6)
ax.text(x0 + s + 0.03, y0 + s + 0.03, z0 + s + 0.05, r"$dV$", color="tab:red", fontsize=10)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.05); ax.set_zlim(0, 1.15)
ax.set_box_aspect((1, 1, 1.05))
ax.view_init(elev=20, azim=-60)
ax.set_title(r"10) volume: $\iiint_\Omega 1\,dV$", fontsize=10)
save(fig, "lec11_fig0_10_triple_volume.svg")

# fig 0-11: mass of a body with density
fig = plt.figure(figsize=(6.0, 5.0))
ax = fig.add_subplot(projection="3d")
rng = np.random.default_rng(7)
pts = rng.random((260, 3))
rho = pts[:, 0] + pts[:, 1] + pts[:, 2]
sc = ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], c=rho, cmap="viridis", s=14, alpha=0.85)
for a, b in edges:
    ax.plot([a[0], b[0]], [a[1], b[1]], [a[2], b[2]], color="0.7", lw=0.8, alpha=0.6)
ax.text(0.0, 0.0, 1.12, r"density $\rho(x,y,z)$", fontsize=9)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.05); ax.set_zlim(0, 1.12)
ax.set_box_aspect((1, 1, 1.05))
ax.view_init(elev=20, azim=-60)
ax.set_title(r"11) mass: cells $\rho\,dV$, summed", fontsize=10)
save(fig, "lec11_fig0_11_triple_mass.svg")

# fig 0-12: centroid of a solid
fig = plt.figure(figsize=(6.0, 5.0))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi / 2, 41); ph = np.linspace(0, 2 * np.pi, 61)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH),
                color="tab:purple", alpha=0.22, linewidth=0, rstride=2, cstride=2)
zc = 3 / 8
ax.plot([0, 0], [0, 0], [0, 1.1], color="k", lw=1.0, ls="--")
ax.scatter([0], [0], [zc], color="tab:red", s=45, zorder=5)
ax.text(0.05, 0.05, zc + 0.06, r"$\bar z=3R/8$", color="tab:red", fontsize=9)
ax.plot([-0.3, 0.3], [0, 0], [zc, zc], color="tab:red", lw=1.0, ls=":")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05); ax.set_zlim(0, 1.2)
ax.set_box_aspect((2.1, 2.1, 2.4))
ax.view_init(elev=18, azim=-58)
ax.set_title(r"12) centroid: $\bar z=M_{xy}/m$ (uniform hemisphere)", fontsize=10)
save(fig, "lec11_fig0_12_triple_centroid.svg")

# fig 0-13: moment of inertia of a solid
fig = plt.figure(figsize=(6.0, 5.0))
ax = fig.add_subplot(projection="3d")
th = np.linspace(0, np.pi, 31); ph = np.linspace(0, 2 * np.pi, 49)
TH, PH = np.meshgrid(th, ph)
ax.plot_surface(np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH),
                color="tab:orange", alpha=0.10, linewidth=0.4, rstride=3, cstride=3)
ax.plot([0, 0], [0, 0], [-1.15, 1.15], color="k", lw=1.4, ls="--")
x1, z1 = 0.75, 0.55
ax.plot([0, x1], [0, 0], [z1, z1], color="tab:red", lw=1.8)
ax.text(x1 / 2, 0.06, z1 + 0.03, r"$r$", color="tab:red", fontsize=11)
ax.text(0.05, 0.05, 1.1, r"axis $z$", fontsize=9)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05); ax.set_zlim(-1.2, 1.2)
ax.set_box_aspect((1, 1, 1.15))
ax.view_init(elev=16, azim=-60)
ax.set_title(r"13) inertia: $I_z=\iiint r^2\rho\,dV=\frac{2}{5}mR^2$", fontsize=10)
save(fig, "lec11_fig0_13_triple_inertia.svg")

# ================= nested elements =================

fig, ax = plt.subplots(figsize=(9.4, 3.0))
ax.set_xlim(0, 10); ax.set_ylim(0, 3.0); ax.axis("off")
ax.plot([0.7, 2.5], [1.4, 1.4], color="tab:blue", lw=4)
ax.annotate("", xy=(2.5, 1.4), xytext=(0.7, 1.4),
            arrowprops=dict(arrowstyle="<->", color="tab:blue", lw=1.2))
ax.text(1.6, 1.62, r"$dx$", color="tab:blue", fontsize=13, ha="center")
ax.text(1.6, 0.75, "length", ha="center", fontsize=9)
ax.add_patch(plt.Rectangle((3.9, 1.0), 1.2, 0.85, facecolor="tab:green", alpha=0.35,
                           edgecolor="tab:green", lw=1.6))
ax.text(4.5, 1.35, r"$d\sigma$", color="tab:green", fontsize=13, ha="center")
ax.text(4.5, 0.75, "area", ha="center", fontsize=9)
dx = 0.55
ox, oy = 7.0, 0.95
ax.add_patch(plt.Rectangle((ox, oy), 1.0, 0.8, facecolor="tab:orange", alpha=0.35,
                           edgecolor="tab:orange", lw=1.5))
ax.add_patch(plt.Polygon([[ox, oy + 0.8], [ox + dx, oy + 0.8 + dx / 2],
                          [ox + 1.0 + dx, oy + 0.8 + dx / 2], [ox + 1.0, oy + 0.8]],
                         closed=True, facecolor="tab:orange", alpha=0.25,
                         edgecolor="tab:orange", lw=1.5))
ax.add_patch(plt.Polygon([[ox + 1.0, oy], [ox + 1.0 + dx, oy + dx / 2],
                          [ox + 1.0 + dx, oy + 0.8 + dx / 2], [ox + 1.0, oy + 0.8]],
                         closed=True, facecolor="tab:orange", alpha=0.20,
                         edgecolor="tab:orange", lw=1.5))
ax.text(ox + 0.5, oy + 0.32, r"$dV$", color="tab:orange", fontsize=13, ha="center")
ax.text(ox + 0.5, 0.50, "volume", ha="center", fontsize=9)
ax.annotate("", xy=(3.65, 1.4), xytext=(2.65, 1.4),
            arrowprops=dict(arrowstyle="-|>", color="0.4", lw=1.6))
ax.annotate("", xy=(6.7, 1.4), xytext=(5.25, 1.4),
            arrowprops=dict(arrowstyle="-|>", color="0.4", lw=1.6))
ax.text(3.15, 1.60, "add one direction", fontsize=8, ha="center")
ax.text(5.98, 1.60, "add one direction", fontsize=8, ha="center")
ax.set_title(r"$dx$ (length)  ->  $d\sigma$ (area)  ->  $dV$ (volume)", fontsize=10)
save(fig, "lec11_fig0_14_nested.svg")

for p in sorted(OUT.glob("lec11_fig0_*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
