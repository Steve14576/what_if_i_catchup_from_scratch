"""探针：对比 SchemDraw 的 Lamp 与 Lamp2 灯泡符号，选定更贴近国内教材"圆圈带叉"的画法。"""
import os

import matplotlib
matplotlib.use("Agg")

import schemdraw
import schemdraw.elements as elm

schemdraw.config(font="Microsoft YaHei", fontsize=14)

with schemdraw.Drawing(show=False) as d:
    d += elm.Lamp().right().label("Lamp", loc="bottom")
    d += elm.Lamp2().right().label("Lamp2", loc="bottom")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(out, exist_ok=True)
d.save(os.path.join(out, "lamp_symbols.png"), transparent=False, dpi=200)
print("[OK] probe lamp symbols -> _probe_circuit/figures/lamp_symbols.png")