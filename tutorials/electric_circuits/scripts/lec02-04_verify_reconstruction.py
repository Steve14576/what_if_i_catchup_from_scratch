# 第02讲重构验证：元件关系 + KCL/KVL 联立，数值作业，修正版配图。
# 规模纪律：纯计算目标 < 2 秒；12 张配图（含2张复用）目标 < 15 秒，无弹窗。
# --check-only 只计算，不写文件；默认出图拒绝覆盖已有产物。
# --redraw 仅重画本脚本的修正版图（编写期间调整排版用）；旧归档图永不覆盖。
# 新图替代讲义引用中的旧图，不删除或修改 lec02-01 至 lec02-03 的产物。
# 讲义：02_电路元件与基尔霍夫定律.md；精读与回查记录：PLAN.md 的第02讲。
import argparse
import re
from pathlib import Path
from time import perf_counter

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CASES = []
TOL = 1e-10  # 当场选取；下方比较 1e-9/1e-10/1e-11，并注入错误检验。


def checked(name, matrix, rhs, expected, powers):
    a, b = np.asarray(matrix, float), np.asarray(rhs, float)
    x = np.linalg.solve(a, b)
    residual = a @ x - b
    scale = np.maximum(np.abs(a) @ np.abs(x) + np.abs(b), 1e-12)
    relative = float(np.max(np.abs(residual) / scale))
    p = np.asarray(powers(x), float)
    p_relative = abs(float(np.sum(p))) / max(float(np.sum(np.abs(p))), 1e-12)
    np.testing.assert_allclose(x, expected, rtol=TOL, atol=1e-12)
    assert relative < TOL and p_relative < TOL
    CASES.append((name, relative, p_relative))
    print(name, 'solution=', np.array2string(x, precision=10))
    print('  scaled_equation_residual=%.3e power_sum_W=%.3e' % (relative, np.sum(p)))
    return x


def divider(name, voltage, r1, r2, load=None):
    # x = [u_out (V), i1 (A), i2 (A), i_load (A)]
    a = [[1, r1, 0, 0], [1, 0, -r2, 0], [0, 1, -1, -1]]
    a.append([0, 0, 0, 1] if load is None else [1, 0, 0, -load])
    b = [voltage, 0, 0, 0]
    # 解析值用于对照，求解实际使用完整元件/KCL/KVL 矩阵。
    out = voltage / (1 + r1 / r2 + (0 if load is None else r1 / load))
    i2, il = out / r2, 0 if load is None else out / load
    expected = [out, i2 + il, i2, il]
    return checked(name, a, b, expected,
                   lambda x: [-voltage * x[1], r1 * x[1]**2, r2 * x[2]**2,
                              0 if load is None else load * x[3]**2])


def ccvs(name, voltage, resistance, gain):
    # x = [i (A), u_R (V), u_d (V)]，源与电阻均上正下负，供电源反关联。
    return checked(name, [[resistance, -1, 0], [gain, 0, -1], [0, 1, 1]],
                   [0, 0, voltage],
                   [voltage / (resistance + gain),
                    resistance * voltage / (resistance + gain),
                    gain * voltage / (resistance + gain)],
                   lambda x: [-voltage * x[0], x[1] * x[0], x[2] * x[0]])


def node_pair(name, current, r1, r2):
    # x = [u (V), i1 (A), i2 (A)]，电流源箭头向上，电阻电流向下。
    u = current / (1 / r1 + 1 / r2)
    return checked(name, [[1, -r1, 0], [1, 0, -r2], [0, 1, 1]],
                   [0, 0, current], [u, u / r1, u / r2],
                   lambda x: [-x[0] * current, x[0] * x[1], x[0] * x[2]])


def controlled_output(name, control_voltage, gain, rc, rl):
    # x = [u_c, i_c, i_d, u_o, i_L]；控制与输出只共享参考结点0。
    a = [[1, 0, 0, 0, 0], [1, -rc, 0, 0, 0],
         [-gain, 0, 1, 0, 0], [0, 0, 0, 1, -rl], [0, 0, -1, 0, 1]]
    ic, id_ = control_voltage / rc, gain * control_voltage
    return checked(name, a, [control_voltage, 0, 0, 0, 0],
                   [control_voltage, ic, id_, rl * id_, id_],
                   lambda x: [-x[0] * x[1], x[0] * x[1], -x[3] * x[2], x[3] * x[4]])


def verify():
    print('=== SIX CIRCUIT EXAMPLES: all currents in A, voltages in V ===')
    divider('Example1 open divider', 9, 2000, 1000)
    ccvs('Example2 CCVS absorbs power', 3, 1, 2)
    node_pair('Example3 node pair', 2e-3, 1000, 1000)
    divider('Example4 battery with Ri', 6, 1000, 3000)
    # 在例4中 r1 为内阻，r2 为串联负载总阻；另核对负载两个电压。
    np.testing.assert_allclose([2000 * .0015, 1000 * .0015], [3, 1.5])
    divider('Example5 loaded divider', 9, 2000, 1000, 1000)
    controlled_output('Example6 VCCS delivers power', 2, .0005, 1000, 2000)

    print('=== NUMERICAL HOMEWORK ===')
    divider('Q2 series', 3, 100, 200)
    node_pair('Q3 node pair', .004, 2000, 2000)
    ccvs('Q4 CCVS', 6, 2, 2)
    divider('Q5 design', 12, 2000, 1000)
    q7 = divider('Q7 battery+divider', 12, 400, 2000)
    np.testing.assert_allclose([1600 * q7[1], 400 * q7[1]], [8, 2])
    np.testing.assert_allclose([400 * q7[1]**2, 1600 * q7[1]**2, 400 * q7[1]**2],
                               [.010, .040, .010])
    divider('Q9 load 2k', 9, 2000, 1000, 2000)
    controlled_output('Q10 external control', 3, .001, 1000, 1000)
    assert 2 + 3 - 1 == 4  # Q6 路径版 KVL
    print('Q6 path_voltage_V=4, reverse_path_V=-4')

    print('=== ELEMENTS, ZERO CONTROL, AND UNITS ===')
    np.testing.assert_allclose([3 * 2, .0005 * 2, 2000 * .001, 4 * .001],
                               [6, .001, 2, .004])
    np.testing.assert_allclose([2 / 1000, 2 / 1 * 1e-3], [.002, .002])
    assert abs(1000 * (-.002)**2 - .004) < 1e-12
    np.testing.assert_allclose([3 - .5 * i for i in [0, .5, 1, 2]], [3, 2.75, 2.5, 2])
    np.testing.assert_allclose([1 + 3 * .1, 1.1**3, 3 * 1.1], [1.3, 1.331, 3.3])
    controlled_output('zero voltage control', 0, .0005, 1000, 2000)
    assert abs((-2 + 1 + .5 + .5)) < 1e-12
    assert abs((-1 + 1 + .5 - .5)) < 1e-12
    print('negative_current_resistor_power_mW=4; KCL i4_mA=0.5 or -0.5')

    print('=== IDEAL-SOURCE COMPATIBILITY: finite constraints, not infinity ===')
    a = np.array([[1, 0], [0, 1], [1, -1]], float)
    for kind, same, different in [('parallel_voltage', [5, 5, 0], [5, 3, 0]),
                                  ('series_current', [.001, .001, 0], [.001, .002, 0])]:
        assert np.linalg.matrix_rank(a) == np.linalg.matrix_rank(np.c_[a, same])
        assert np.linalg.matrix_rank(a) < np.linalg.matrix_rank(np.c_[a, different])
        print(kind, 'same_values=consistent different_values=inconsistent')
    for pair in [[.002, .003], [.001, .004]]:
        assert abs(sum(pair) - .005) < 1e-12
    for pair in [[1, 1], [.5, 1.5]]:
        assert abs(sum(pair) - 2) < 1e-12
    print('equal sources: total known, individual source current/voltage not unique')
    assert 5 + 3 == 8 and 5 - 3 == 2
    assert 2 + 3 == 5 and abs(2 - 3) == 1
    np.testing.assert_allclose([10**2 / 1000, 20**2 / 1000], [.1, .4])
    print('series_voltage_V=8 or 2; parallel_current_mA=5 or opposite-direction 1')

    print('=== LOAD SENSITIVITY ===')
    for rl in [1000, 10000, 100000]:
        out = divider('load_RL_ohm=%d' % rl, 9, 2000, 1000, rl)[0]
        print('  output_V=%.10f' % out)

    worst = max(max(eq, power) for _, eq, power in CASES)
    print('=== TOLERANCE SENSITIVITY (chosen for these small examples) ===')
    for tol in [1e-9, 1e-10, 1e-11]:
        assert worst < tol
        print('tolerance=%.0e all_good_cases_pass=True' % tol)
    # 人为多写 f_i=1e-6 A，会破坏电阻关系，防止零残差自算自证。
    a = np.array([[1, 2000, 0], [1, 0, -1000], [0, 1, -1]], float)
    b = np.array([9, 0, 0], float)
    wrong = np.array([3, .003001, .003])
    mismatch = float(np.max(np.abs(a @ wrong - b)))
    assert mismatch > 1e-6
    print('injected_current_error_A=1e-6, max_equation_mismatch=%.3e (detected)' % mismatch)
    print('[OK] checked_circuit_cases=%d worst_scaled_residual=%.3e' % (len(CASES), worst))


def verify_text():
    # 结构卫生检查不能证明教学完整；正文精读及认知链回查另见PLAN。
    lecture = ROOT / '02_电路元件与基尔霍夫定律.md'
    text = lecture.read_text(encoding='utf-8')
    images = re.findall(r'!\[图 (\d+)：[^\]]*\]\(([^)]+)\)', text)
    assert [int(number) for number, _ in images] == list(range(1, 13))
    assert len({path for _, path in images}) == 12
    for _, path in images:
        image = ROOT / path
        assert image.is_file() and image.with_suffix('.png').is_file(), path
    questions = re.findall(r'\*\*Q(\d+)\.', text)
    assert [int(q) for q in questions] == list(range(1, 12))
    assert text.count('**参考答案：**') == 11
    head = '\n'.join(text.splitlines()[:30])
    for slot in ['前置', '预计时间', '一句话定位', '本讲回答什么', '本讲目标',
                 '目标达成', '怎么学这一讲', '这一讲有真实验证']:
        assert slot in head, slot
    for path in [lecture, ROOT / 'AA_一览.md']:
        source = path.read_text(encoding='utf-8')
        assert '<details' not in source
        assert source.count('$$') % 2 == 0
        assert source.count('```') % 2 == 0
        fenced, width = False, None
        for line_number, line in enumerate(source.splitlines(), 1):
            if line.startswith('```'):
                fenced = not fenced
                width = None
            if fenced:
                continue
            if line.startswith('|'):
                cells = len(line.split('|'))
                if width is None:
                    width = cells
                assert cells == width, (path.name, line_number, cells, width)
            else:
                width = None
    print('[DOC] images=12 (SVG+PNG exist), questions=11, answers=11, tables/delimiters=OK')


def render(redraw=False):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import schemdraw
    import schemdraw.elements as elm
    from shutil import copyfile

    outdir = ROOT / 'figures'
    stems = ['lec02_fig1_divider_revised', 'lec02_fig3_iv_profiles_revised',
             'lec02_fig5_branch_node_loop_revised', 'lec02_fig7_kvl_revised',
             'lec02_fig8_ccvs_revised', 'lec02_fig10_battery_load_revised',
             'lec02_fig11_loaded_divider', 'lec02_fig12_external_control',
             'lec02_fig2_nonlinear_tangent', 'lec02_fig4_source_connections',
             'lec02_fig6_kcl_reused', 'lec02_fig9_node_pair_reused']
    existing = [outdir / (s + ext) for s in stems for ext in ['.svg', '.png']
                if (outdir / (s + ext)).exists()]
    if existing and not redraw:
        raise FileExistsError('Figure outputs already exist; use --check-only. --redraw only regenerates this script\'s figures.')
    outdir.mkdir(exist_ok=True)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['svg.fonttype'] = 'path'
    plt.rcParams['axes.unicode_minus'] = False
    elm.style(elm.STYLE_IEC)
    schemdraw.config(font='Microsoft YaHei', fontsize=13)

    def save(d, stem):
        d.save(str(outdir / (stem + '.svg')), transparent=False)
        d.save(str(outdir / (stem + '.png')), transparent=False, dpi=160)
        plt.close('all')
        print('[FIG]', stem)

    def label(d, xy, text, color='black'):
        d += elm.Label().at(xy).label(text).color(color)

    def draw_divider(stem, load=False):
        d = schemdraw.Drawing(show=False)
        d += elm.SourceV().at((0, 0)).up().length(6)
        label(d, (-1.25, 3), '9 V')
        d += elm.Line().at((0, 6)).right().length(4)
        d += elm.Resistor().at((4, 6)).down().length(3)
        d += elm.Resistor().at((4, 3)).down().length(3)
        label(d, (2.4, 4.5), 'R1 = 2 kΩ')
        label(d, (2.4, 1.5), 'R2 = 1 kΩ')
        d += elm.Line().at((4, 0)).left().length(4)
        d += elm.Dot().at((4, 3))
        d += elm.Dot().at((4, 0))
        label(d, (4.25, 6.5), 'a: +9 V', '#2471a3')
        label(d, (4.25, 3.4), 'b', '#2471a3')
        label(d, (4.15, -.5), '0: 参考结点', '#2471a3')
        d += elm.Line().at((4, 3)).right().length(3)
        if load:
            d += elm.Resistor().at((7, 3)).down().length(3)
            label(d, (8.4, 1.5), 'RL = 1 kΩ')
            d += elm.Line().at((7, 0)).left().length(3)
            label(d, (7.2, 3.5), '+ uo = 1.8 V')
            label(d, (7.2, -.4), '-')
        else:
            d += elm.Dot(open=True).at((7, 3))
            label(d, (7, 2.3), 'uo = 3 V（空载）')
        save(d, stem)

    draw_divider(stems[0])
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    data = [([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], '线性电阻：u = Ri', 'i / mA'),
            ([0, 10], [9, 9], '理想电压源：u = 9 V', 'i / mA'),
            ([2, 2], [0, 8], '理想电流源：i = 2 mA', 'i / mA'),
            ([0, .5, 1, 2], [3, 2.75, 2.5, 2], '实际电池：输出电流口径', 'i_out / A')]
    for ax, (x, y, title, xlabel) in zip(axes.flat, data):
        ax.plot(x, y, color='#2471a3', lw=2)
        ax.set(title=title, xlabel=xlabel, ylabel='u / V')
        ax.grid(alpha=.3)
    axes[1, 0].set_xlim(0, 6)
    fig.tight_layout()
    fig.savefig(outdir / (stems[1] + '.svg'))
    fig.savefig(outdir / (stems[1] + '.png'), dpi=160)
    plt.close(fig)
    print('[FIG]', stems[1])

    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().at((0, 0)).up().length(3)
    label(d, (0, -1.15), '支路①')
    d += elm.Line().at((0, 3)).right().length(6)
    for x, text in [(3, '支路②'), (6, '支路③')]:
        d += elm.Resistor().at((x, 3)).down().length(3)
        label(d, (x, -1.15), text)
    d += elm.Line().at((0, 0)).right().length(6)
    for y, text in [(3, 'a'), (0, '0')]:
        d += elm.Dot().at((3, y))
        label(d, (3, y + (.5 if y else -.5)), text, '#2471a3')
    label(d, (1.5, 1.5), '左网孔')
    label(d, (4.5, 1.5), '右网孔')
    label(d, (3, -2), '整条上导线为结点 a；整条下导线为结点 0')
    save(d, stems[2])

    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().at((0, 0)).up().length(3)
    label(d, (-1.2, 1.5), 'A: 6 V')
    d += elm.Resistor().at((0, 3)).right().length(5).label('B: uB = 2 V', loc='top')
    d += elm.Resistor().at((5, 3)).down().length(3)
    label(d, (6.75, 1.5), 'C: uC = 4 V')
    d += elm.Line().at((5, 0)).left().length(5)
    for xy, text in [((.5, 3.4), '+'), ((4.5, 3.4), '-'),
                     ((5.35, 2.6), '+'), ((5.35, .4), '-')]:
        label(d, xy, text)
    for start, end in [((1, .7), (1, 2.2)), ((1, 2.2), (4, 2.2)),
                       ((4, 2.2), (4, .7)), ((4, .7), (1, .7))]:
        d += elm.Arrow().at(start).to(end).color('#2471a3')
    label(d, (2.5, -1), '顺时针：-6 + 2 + 4 = 0')
    save(d, stems[3])

    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().at((0, 0)).up().length(3)
    label(d, (-1, 1.5), '3 V')
    d += elm.Resistor().at((0, 3)).right().length(5).label('R = 1 Ω', loc='top')
    d += elm.SourceControlledV().at((5, 0)).up().length(3)
    label(d, (6.75, 1.5), 'ud = (2 Ω)i')
    d += elm.Line().at((0, 0)).right().length(5)
    d += elm.Arrow().at((1, 4.1)).right().length(1.5).label('i = 1 A', loc='top')
    label(d, (2.5, -1), '受控源上正下负：吸收功率 2 W')
    save(d, stems[4])

    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().at((0, 0)).up().length(6)
    label(d, (-1.45, 3), 'US = 6 V')
    d += elm.Line().at((0, 6)).right().length(4)
    d += elm.Resistor().at((4, 6)).down().length(2)
    d += elm.Resistor().at((4, 4)).down().length(2)
    d += elm.Resistor().at((4, 2)).down().length(2)
    label(d, (2.4, 5), 'Ri = 1 kΩ')
    label(d, (2.4, 3), '2 kΩ')
    label(d, (2.4, 1), '1 kΩ')
    d += elm.Line().at((4, 0)).left().length(4)
    for y, text in [(4, 'a'), (0, '0')]:
        d += elm.Dot().at((4, y))
        label(d, (4.35, y), text, '#2471a3')
    d += elm.Arrow().at((6, 3.8)).down().length(3.6).color('#2471a3')
    label(d, (6, 4.3), '+')
    label(d, (6, -.3), '-')
    label(d, (7.5, 2), 'u_a0 = 4.5 V')
    label(d, (4, -1), '端电压跨负载，不跨内部理想源')
    save(d, stems[5])
    draw_divider(stems[6], load=True)

    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().at((0, 0)).up().length(4)
    label(d, (-1.45, 2), 'US = 2 V')
    d += elm.Line().at((0, 4)).right().length(3)
    d += elm.Resistor().at((3, 4)).down().length(4)
    label(d, (1.5, 2), 'Rc = 1 kΩ')
    d += elm.Line().at((0, 0)).right().length(12)
    d += elm.SourceControlledI().at((8, 0)).up().length(4)
    label(d, (6.65, 2), 'id = g uc')
    d += elm.Line().at((8, 4)).right().length(4)
    d += elm.Resistor().at((12, 4)).down().length(4)
    label(d, (13.55, 2), 'RL = 2 kΩ')
    for xy, text in [((3, 4), 'a'), ((12, 4), 'b'), ((6, 0), '0')]:
        d += elm.Dot().at(xy)
        label(d, (xy[0], xy[1] + (.5 if xy[1] else -.5)), text, '#2471a3')
    label(d, (4.55, 2), 'uc = 2 V')
    label(d, (3.45, 3.5), '+')
    label(d, (3.45, .5), '-')
    label(d, (10, 5), 'g = 0.5 mS')
    label(d, (10, 2), 'uo = 2 V')
    label(d, (12.45, 3.5), '+')
    label(d, (12.45, .5), '-')
    label(d, (6, -1), '控制位置 a-0；输出位置 b-0（上端不相连）')
    save(d, stems[7])

    # 微分电阻针对增量；切线一般不经过原点。
    fig, ax = plt.subplots(figsize=(6, 4))
    i = np.linspace(0, 1.5, 150)
    near = np.linspace(.7, 1.3, 100)
    ax.plot(i, i**3, label='非线性特性 u = α i³，α = 1 V/A³')
    ax.plot(near, 1 + 3 * (near - 1), '--', label='工作点切线：u = 1 + 3(i-1)')
    ax.scatter([1], [1], color='black', zorder=3)
    ax.annotate('工作点 (1 A, 1 V)', (1, 1), xytext=(.1, 2.3),
                arrowprops={'arrowstyle': '->'})
    ax.set(xlabel='i / A', ylabel='u / V')
    ax.grid(alpha=.3)
    ax.legend(loc='upper left', fontsize=10)
    fig.tight_layout()
    fig.savefig(outdir / (stems[8] + '.svg'))
    fig.savefig(outdir / (stems[8] + '.png'), dpi=160)
    plt.close(fig)
    print('[FIG]', stems[8])

    # 四种理想源连接：各面板独立，并非彼此相连。
    d = schemdraw.Drawing(show=False)
    label(d, (2, 5), '(a) 压源串联：沿同一方向加电压')
    d += elm.SourceV().at((0, 0)).up().length(2)
    d += elm.SourceV().at((0, 2)).up().length(2)
    label(d, (-1, 1), '5 V')
    label(d, (-1, 3), '3 V')
    d += elm.Line().at((0, 4)).right().length(3)
    d += elm.Resistor().at((3, 4)).down().length(4)
    d += elm.Line().at((3, 0)).left().length(3)
    label(d, (4.2, 2), '外电路 R')
    label(d, (2, -.6), '总升压：5 + 3 = 8 V')

    label(d, (11, 5), '(b) 流源并联：沿同一方向加电流')
    for x, text in [(8, '2 mA'), (11, '3 mA')]:
        d += elm.SourceI().at((x, 0)).up().length(4)
        label(d, (x - 1, 2), text)
    d += elm.Line().at((8, 4)).right().length(6)
    d += elm.Line().at((8, 0)).right().length(6)
    d += elm.Resistor().at((14, 4)).down().length(4)
    label(d, (15.3, 2), '外电路 R')
    label(d, (11, -.6), '负载电流：2 + 3 = 5 mA')

    label(d, (2, -3), '(c) 不等压源并联：电压约束矛盾')
    for x, text in [(0, '5 V'), (3, '3 V')]:
        d += elm.SourceV().at((x, -8)).up().length(4)
        label(d, (x - 1, -6), text)
    d += elm.Line().at((0, -4)).right().length(3)
    d += elm.Line().at((0, -8)).right().length(3)
    label(d, (2, -8.7), '同一两端不能既为 5 V 又为 3 V')

    label(d, (11, -3), '(d) 不等流源串联：电流约束矛盾')
    for y, text in [(-8, '1 mA'), (-6, '2 mA')]:
        d += elm.SourceI().at((9, y)).up().length(2)
        label(d, (7.7, y + 1), text)
    d += elm.Line().at((9, -4)).right().length(4)
    d += elm.Resistor().at((13, -4)).down().length(4)
    d += elm.Line().at((13, -8)).left().length(4)
    label(d, (14.3, -6), '外电路 R')
    label(d, (11, -8.7), '同一电流不能既为 1 mA 又为 2 mA')
    save(d, stems[9])

    # 内容核对无误的旧KCL图/单结点对图按本轮首次出现顺序复制，不改原件。
    for source, target in [('lec02_fig4_kcl', stems[10]),
                           ('lec02_fig7_node_pair', stems[11])]:
        for extension in ['.svg', '.png']:
            copyfile(outdir / (source + extension), outdir / (target + extension))
        print('[REUSE]', target)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--redraw', action='store_true', help='重画本脚本的修正版图，不覆盖旧归档图')
    args = parser.parse_args()
    started = perf_counter()
    verify()
    if not args.check_only:
        render(redraw=args.redraw)
    verify_text()
    print('TOTAL runtime_s=%.3f' % (perf_counter() - started))
