"""探针：源类元素（SourceI / SourceControlledI / SourceControlledV）在"向下"方向的
.at().to() 与 .at().down().length() 两种写法下的实际绘制范围。

输出：_probe_circuit/figures/probe_src_down.png（两种写法并排对照）
"""
import os

import matplotlib
matplotlib.use("Agg")

import schemdraw
import schemdraw.elements as elm

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

elm.style(elm.STYLE_IEC)
schemdraw.config(font="Microsoft YaHei", fontsize=13)

with schemdraw.Drawing(show=False) as d:
    # 第 1 组：.at().to() 向下
    e1 = elm.SourceI().at((0, 3)).to((0, 0))
    d += e1
    print("[at.to] SourceI: start =", e1.start, " end =", e1.end)
    # 第 2 组：.at().down().length() 向下
    e2 = elm.SourceI().at((2.5, 3)).down().length(3)
    d += e2
    print("[chain] SourceI: start =", e2.start, " end =", e2.end)
    # 第 3 组：受控电流源 .at().to() 向下
    e3 = elm.SourceControlledI().at((5, 3)).to((5, 0))
    d += e3
    print("[at.to] SourceControlledI: start =", e3.start, " end =", e3.end)
    # 第 4 组：受控电压源 .at().to() 向下
    e4 = elm.SourceControlledV().at((7.5, 3)).to((7.5, 0))
    d += e4
    print("[at.to] SourceControlledV: start =", e4.start, " end =", e4.end)

    for x, tag in [(0, "at.to"), (2.5, "chain"),
                   (5, "SC-I at.to"), (7.5, "SC-V at.to")]:
        d += elm.Label().at((x, 3.6)).label(tag)
        d += elm.Dot().at((x, 3))
        d += elm.Dot().at((x, 0))

d.save(os.path.join(OUT, "probe_src_down.png"), dpi=150)
print("[OK] probe_src_down.png 已生成")