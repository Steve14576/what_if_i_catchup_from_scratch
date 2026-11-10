# 规模纪律：1 张静态 SVG, 目标 < 3 秒。
# 第 29 讲图：接口地图（英文标签，图内不放中文）。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(9.0, 6.0))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

# center box
center = FancyBboxPatch((3.4, 4.4), 3.2, 1.2, boxstyle="round,pad=0.08",
                        fc="#e8f0fe", ec="tab:blue", lw=2)
ax.add_patch(center)
ax.text(5.0, 5.0, "Calculus II\n(semester 2)", ha="center", va="center", fontsize=12)

targets = [
    ("Complex analysis\n(17/18/26)", 1.0, 8.0),
    ("Probability\n(12-14)", 5.0, 8.6),
    ("ODE\n(26/27)", 9.0, 8.0),
    ("Signals\n(28)", 9.2, 5.0),
    ("Numerical analysis\n(27)", 9.0, 2.0),
    ("Linear algebra\n(09)", 5.0, 1.2),
    ("Physics / EM\n(22)", 1.0, 2.0),
]

for label, x, y in targets:
    box = FancyBboxPatch((x - 1.15, y - 0.55), 2.3, 1.1, boxstyle="round,pad=0.06",
                         fc="#fff4e5", ec="tab:orange", lw=1.4)
    ax.add_patch(box)
    ax.text(x, y, label, ha="center", va="center", fontsize=9)
    arr = FancyArrowPatch((5.0, 5.0), (x, y), arrowstyle="-|>", mutation_scale=12,
                          color="0.45", lw=1.2, shrinkA=55, shrinkB=40)
    ax.add_patch(arr)

ax.set_title("interfaces: where Calculus II shows up later", fontsize=12)
fig.tight_layout()
fig.savefig(OUT / "lec29_fig1_map.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec29_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
