"""探针 B：matplotlib 画 RC 充电暂态曲线 v_C(t)，与探针 A 的电路图配套。

验证点：
1. 数值计算 v_C = U_S * (1 - e^(-t/tau)) 与绘图；
2. 中文字体 + 负号 + SVG 文字转路径；
3. SVG/PNG 双格式输出。

输出：figures/probe_rc_curve.svg / .png
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')  # 无头渲染，防弹窗阻塞
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'DengXian']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['svg.fonttype'] = 'path'
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / 'figures'
OUT.mkdir(exist_ok=True)

R = 1e3       # 欧姆
C = 1e-6      # 法拉
Us = 5.0      # 伏特
tau = R * C   # 时间常数 = 1 ms

t = np.linspace(0, 5 * tau, 600)
vc = Us * (1 - np.exp(-t / tau))
v_at_tau = Us * (1 - np.exp(-1))   # t = tau 时刻的电容电压，约 3.16 V

fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(t * 1e3, vc, lw=2.2, color='#1f4e79',
        label=r'$v_C(t) = U_S\,(1 - e^{-t/\tau})$')
ax.axhline(Us, color='gray', lw=1, ls='--')
ax.axvline(tau * 1e3, color='gray', lw=1, ls=':')
ax.plot([tau * 1e3], [v_at_tau], 'o', color='#c0392b', ms=6, zorder=5)

ax.annotate(r't = $\tau$：$v_C$ 约为 3.16 V（63.2% $U_S$）',
            xy=(tau * 1e3, v_at_tau), xytext=(2.6, 1.55),
            arrowprops=dict(arrowstyle='->', color='#c0392b'),
            color='#c0392b')

ax.set_xlabel('时间 $t$ / ms')
ax.set_ylabel('电容电压 $v_C$ / V')
ax.set_title('RC 充电电路的暂态响应（R = 1 kΩ，C = 1 μF，$U_S$ = 5 V）')
ax.set_xlim(0, 5 * tau * 1e3)
ax.set_ylim(0, 5.5)
ax.grid(True, alpha=0.3)
ax.legend(loc='lower right')

fig.tight_layout()
fig.savefig(OUT / 'probe_rc_curve.svg')
fig.savefig(OUT / 'probe_rc_curve.png', dpi=200)
print('[OK] curve -> figures/probe_rc_curve.svg / .png')