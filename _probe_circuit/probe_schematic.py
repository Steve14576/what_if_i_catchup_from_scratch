"""探针 A：SchemDraw 画 RC 充电电路（IEC 风格 + 中文标签）。

验证点：
1. schemdraw 在 uv 临时依赖下可运行；
2. elm.style(elm.STYLE_IEC) 全局 IEC 风格（矩形电阻，国内教材习惯）生效；
3. 中文标签（Microsoft YaHei）正常渲染；
4. SVG（文字转路径）+ PNG 双格式输出；
5. show=False + Agg 无头渲染：脚本不弹窗、无需人工关窗。

输出：figures/probe_rc_schematic.svg / .png
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # 无头渲染，防弹窗阻塞
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'DengXian']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['svg.fonttype'] = 'path'

import schemdraw
import schemdraw.elements as elm

OUT = Path(__file__).resolve().parent / 'figures'
OUT.mkdir(exist_ok=True)

# 全局设置：IEC/欧式符号 + 中文字体
elm.style(elm.STYLE_IEC)
schemdraw.config(font='Microsoft YaHei', fontsize=15)

with schemdraw.Drawing(show=False) as d:
    d += elm.SourceV().up().label('$U_S$ = 5 V', loc='left')
    d += elm.Switch().right().label('S（t = 0 闭合）')
    d += elm.Resistor().right().label('R = 1 kΩ')
    d += elm.Capacitor().down().label('C = 1 μF', loc='left')
    d += elm.Line().left().length(6)

d.save(str(OUT / 'probe_rc_schematic.svg'), transparent=False)
d.save(str(OUT / 'probe_rc_schematic.png'), transparent=False, dpi=200)
print('[OK] schematic -> figures/probe_rc_schematic.svg / .png')