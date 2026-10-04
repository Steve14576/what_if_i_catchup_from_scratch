# =====================================================================
# probe_lc_symbols 电容/电感符号备选对比（选型探针）
# 目的：确认 IEC 风格下 Capacitor/Capacitor2、Inductor/Inductor2 的
#       实际外观，为第 09 讲图 1 选定"无极性电容 + 空心线圈"的标准形态。
# =====================================================================
import os

import matplotlib
matplotlib.use("Agg")

import schemdraw
import schemdraw.elements as elm

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

schemdraw.config(font="Microsoft YaHei", fontsize=12)
elm.style(elm.STYLE_IEC)

with schemdraw.Drawing(show=False) as d:
    def manual_cap(x, y0):
        global d
        d += elm.Line().at((x, y0)).to((x, y0 - 0.45))
        d += elm.Line().at((x - 0.5, y0 - 0.45)).to((x + 0.5, y0 - 0.45))
        d += elm.Line().at((x - 0.5, y0 - 0.65)).to((x + 0.5, y0 - 0.65))
        d += elm.Line().at((x, y0 - 0.65)).to((x, y0 - 1.1))

    for j, (elem, lab) in enumerate([
        (None, "Capacitor(手绘)"),
        (elm.Capacitor, "Capacitor(IEC)"),
        (elm.Inductor, "Inductor(IEC)"),
        (elm.Inductor2, "Inductor2(IEC)"),
    ]):
        x = j * 2.4
        if elem is None:
            manual_cap(x, 2.3)
        else:
            d += elm.Line().at((x, 2.4)).to((x, 2.1))
            d += elem().at((x, 2.1)).down().length(1.0)
            d += elm.Line().at((x, 1.1)).to((x, 0.8))
        d += elm.Label().at((x, 0.35)).label(lab, fontsize=9)

d.save(os.path.join(BASE, "_probe_circuit", "figures", "probe_lc_symbols.png"),
       transparent=False, dpi=200)
print("[OK] probe_lc_symbols.png 已生成")