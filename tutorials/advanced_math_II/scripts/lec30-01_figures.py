# 规模纪律：1 张静态 SVG, 目标 < 3 秒。
# 第 30 讲图：六模块题型地图（英文标签，图内不放中文）。
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(9.0, 5.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

mods = [
    ("1 Vectors &\nspace", "dot / cross / planes", 1.2, 8.2),
    ("2 Multivariable\ndifferential", "partials / gradient / extrema", 5.0, 9.0),
    ("3 Multiple\nintegrals", "double / triple / coords", 8.8, 8.2),
    ("4 Line & surface\nintegrals", "Green / Gauss / Stokes", 1.2, 4.6),
    ("5 Field theory", "grad / div / curl", 5.0, 4.6),
    ("6 Series", "tests / power / Fourier", 8.8, 4.6),
]

for title, tool, x, y in mods:
    box = FancyBboxPatch((x - 1.35, y - 0.75), 2.7, 1.5, boxstyle="round,pad=0.07",
                         fc="#eef4ff", ec="tab:blue", lw=1.6)
    ax.add_patch(box)
    ax.text(x, y + 0.25, title, ha="center", va="center", fontsize=10, weight="bold")
    ax.text(x, y - 0.35, tool, ha="center", va="center", fontsize=8, color="tab:blue")

ax.text(5.0, 2.2, "locate the module first, then pick the first tool", ha="center", fontsize=10)
ax.text(5.0, 1.6, "(region / curve / surface -> module; direction -> first vs second kind)", ha="center", fontsize=8, color="0.4")
ax.set_title("calculus II: six modules and their core tools", fontsize=12)
fig.tight_layout()
fig.savefig(OUT / "lec30_fig1_map.svg", format="svg")
plt.close(fig)

for p in sorted(OUT.glob("lec30_fig*.svg")):
    print(f"{p.name}: {p.stat().st_size} bytes")
print("[OK] figures written to", OUT)
