# 第03讲重构：等效公式与原网络独立求解、三端验证、源功率、受控源边界。
# 规模纪律：纯计算 < 2 秒，7张修正版图 < 15 秒；默认只计算，不覆盖旧归档。
# --figures 首次出图；--redraw 仅重画本脚本的新图；--audit-text 检查讲义引用。
# 正文：03_等效变换.md；范围、认知链及实测记录：PLAN.md 第03讲本轮记录。
import argparse
from pathlib import Path
import re
from time import perf_counter

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-10  # 当场选取；下方用1e-9/1e-10/1e-11检验敏感性。
ERRORS = []
CASES = 0


def close(actual, expected):
    np.testing.assert_allclose(actual, expected, rtol=TOL, atol=1e-12)


def passive(edges, fixed):
    # edges=(起点,终点,Ω)；从真实接线组装KCL，不使用预先化简的电阻公式。
    global CASES
    nodes = sorted({node for a, b, _ in edges for node in (a, b)})
    unknown = [node for node in nodes if node not in fixed]
    index = {node: k for k, node in enumerate(unknown)}
    a = np.zeros((len(unknown), len(unknown)))
    rhs = np.zeros(len(unknown))
    for n1, n2, resistance in edges:
        assert resistance > 0
        for node, other in [(n1, n2), (n2, n1)]:
            if node in index:
                row = index[node]
                a[row, row] += 1 / resistance
                if other in index:
                    a[row, index[other]] -= 1 / resistance
                else:
                    rhs[row] += fixed[other] / resistance
    voltages = dict(fixed)
    if unknown:
        solution = np.linalg.solve(a, rhs)
        voltages.update(zip(unknown, solution))
        denominator = np.maximum(np.abs(a) @ np.abs(solution) + np.abs(rhs), 1e-12)
        ERRORS.append(float(np.max(np.abs(a @ solution - rhs) / denominator)))
    injections = {node: 0.0 for node in nodes}
    currents, powers = [], []
    for n1, n2, resistance in edges:
        voltage = voltages[n1] - voltages[n2]
        current = voltage / resistance
        injections[n1] += current
        injections[n2] -= current
        currents.append(current)
        powers.append(voltage * current)
    supplied = sum(voltages[node] * injections[node] for node in fixed)
    # 同电位测试中真实功率为零；不用近零功率作分母放大舍入误差。
    # 此处按至少1 W归一化，配合下方1e-9/1e-10/1e-11阈值比较。
    error = abs(supplied - sum(powers)) / max(abs(supplied) + sum(abs(p) for p in powers), 1.0)
    ERRORS.append(error)
    assert error < TOL
    CASES += 1
    return voltages, injections, np.array(currents), np.array(powers)


def loaded(name, voltage, r1, r2, rl):
    edges = [('a', 'b', r1), ('b', '0', r2), ('b', '0', rl)]
    v, injection, currents, powers = passive(edges, {'a': voltage, '0': 0})
    rp = r2 * rl / (r2 + rl)
    total = r1 + rp
    simplified = voltage * rp / total
    close([v['b'], injection['a']], [simplified, voltage / total])
    print(name, 'R_parallel_ohm=', rp, 'R_total_ohm=', total,
          'output_V=', v['b'], 'currents_mA=', currents * 1000, 'powers_mW=', powers * 1000)
    return v, currents, powers


def y_to_delta(arms):
    r1, r2, r3 = arms
    p = r1 * r2 + r2 * r3 + r3 * r1
    return np.array([p / r3, p / r1, p / r2])  # R12,R23,R31


def delta_to_y(edges):
    r12, r23, r31 = edges
    total = sum(edges)
    return np.array([r12 * r31, r12 * r23, r23 * r31]) / total


def three_terminal(arms):
    delta = y_to_delta(arms)
    close(delta_to_y(delta), arms)
    y_edges = [('1', 'n', arms[0]), ('2', 'n', arms[1]), ('3', 'n', arms[2])]
    d_edges = [('1', '2', delta[0]), ('2', '3', delta[1]), ('3', '1', delta[2])]
    worst = 0.0
    # 测三对端口时第三端没有连接外部源，是未知结点；并非钉死为0。
    for p, q in [('1', '2'), ('2', '3'), ('3', '1')]:
        _, iy, _, _ = passive(y_edges, {p: 1.0, q: 0.0})
        _, id_, _, _ = passive(d_edges, {p: 1.0, q: 0.0})
        expected = arms[int(p) - 1] + arms[int(q) - 1]
        close([1 / iy[p], 1 / id_[p]], [expected, expected])
        worst = max(worst, abs(iy[p] - id_[p]))
    # 三端同时接入任意电位，比较完整端口电流向量，不只比较开路电阻。
    for values in [(1, 2, 0), (1.5, -2, 3), (-4, 5, -1), (7, 7, 7)]:
        fixed = dict(zip(['1', '2', '3'], values))
        _, iy, _, _ = passive(y_edges, fixed)
        _, id_, _, _ = passive(d_edges, fixed)
        close([iy[k] for k in fixed], [id_[k] for k in fixed])
        worst = max(worst, max(abs(iy[k] - id_[k]) for k in fixed))
    print('Y_ohm=', arms, 'Delta_ohm=', delta, 'max_port_current_difference_A=%.3e' % worst)


def bridge(name, resistances, voltage=11):
    r1, r2, r3, r4, r5 = resistances
    edges = [('A', 'C', r1), ('A', 'D', r2), ('C', 'B', r3),
             ('D', 'B', r4), ('C', 'D', r5)]
    v, injection, currents, powers = passive(edges, {'A': voltage, 'B': 0})
    yc = r3 * r5 / (r3 + r4 + r5)
    yd = r4 * r5 / (r3 + r4 + r5)
    yb = r3 * r4 / (r3 + r4 + r5)
    left, right = r1 + yc, r2 + yd
    req = left * right / (left + right) + yb
    close(injection['A'], voltage / req)
    print(name, 'R_AB_ohm=', req, 'VC_V=', v['C'], 'VD_V=', v['D'],
          'currents_mA=', currents * 1000, 'powers_mW=', powers * 1000)
    return req, v, currents


def sources(us, rs, rl):
    # 电压源串阻：内部源结点s固定；电流源并阻：直接KCL求u。
    v, _, i, _ = passive([('s', 'a', rs), ('a', '0', rl)], {'s': us, '0': 0})
    current_source = us / rs
    u_i = np.linalg.solve(np.array([[1 / rs + 1 / rl]]), [current_source])[0]
    close(u_i, v['a'])
    p_v = np.array([-us * i[0], rs * i[0]**2, v['a']**2 / rl])
    p_i = np.array([-u_i * current_source, u_i**2 / rs, u_i**2 / rl])
    close([sum(p_v), sum(p_i)], [0, 0])
    print('source US_V=', us, 'Rs_ohm=', rs, 'RL_ohm=', rl,
          'terminal_V=', u_i, 'V_model_absorbed_mW=', p_v * 1000,
          'I_model_absorbed_mW=', p_i * 1000)
    for u in [-3, 0, 3, 4.5, 6, 9]:
        out_v = (us - u) / rs
        out_i = current_source - u / rs
        close(out_v, out_i)
    return u_i


def controlled(resistance, gain, direction, voltage):
    # direction=+1 时源箭头a→b，与端口输入同向；-1时b→a。
    current_r = voltage / resistance
    current_d = direction * gain * voltage
    current_t = current_r + current_d
    powers = [voltage * current_r, voltage * current_d, -voltage * current_t]
    close(sum(powers), 0)
    conductance = 1 / resistance + direction * gain
    close(current_t, conductance * voltage)
    print('controlled R_ohm=', resistance, 'g_S=', gain, 'direction=', direction,
          'test_V=', voltage, 'input_mA=', current_t * 1000,
          'Rin_ohm=', 'open' if conductance == 0 else 1 / conductance,
          'absorbed_powers_mW=', np.array(powers) * 1000)
    return current_t


def verify_math():
    print('=== 原网络与化简结果：电流用A，电压用V，电阻用Ω ===')
    close([2000 * .001, 1 + 1000 * .001, 2000 * .002, 1 + 1000 * .002], [2, 2, 4, 3])
    for uc in [1, 3]:
        us, is_ = 2 * uc, .002 * uc
        close([us, is_], [2 * uc, 2 * uc / 1000])
        for u in [0, 1, 4.5]:
            close((us - u) / 1000, is_ - u / 1000)
    print('单个工作点相同不等效；受控源互换保持整个控制关系')
    loaded('带载分压器', 9, 2000, 1000, 1000)
    loaded('Q2混联', 12, 2000, 6000, 3000)
    loaded('Q7带载', 12, 2000, 2000, 2000)
    v, _, currents, powers = passive([('a', 'c', 2000), ('c', '0', 1000)], {'a': 9, '0': 0})
    close([v['c'], *currents], [3, .003, .003])
    split = np.linalg.solve(np.array([[1 / 2000 + 1 / 3000]]), [.006])[0]
    close([split, split / 2000, split / 3000], [7.2, .0036, .0024])
    print('分流：u_V=', split, 'i1_mA=', split / 2, 'i2_mA=', split / 3)
    sources(6, 1000, 3000)
    sources(10, 2000, 3000)  # Q3
    # 两个同向有内阻源先变成流源：9mA与0.5kΩ。
    for u in [0, 1, 4.5, 9]:
        original = (6 - u) / 1000 + .003 - u / 1000
        equivalent = .009 - u / 500
        close(original, equivalent)
    print('合并含源支路：Ueq_V=4.5, Req_ohm=500')
    for arms in [(1000, 1000, 1000), (1000, 2000, 3000), (1000, 1000, 2000)]:
        three_terminal(np.array(arms, float))
    close(delta_to_y(np.array([3000, 3000, 3000])), [1000, 1000, 1000])
    close(y_to_delta(np.array([1000, 1000, 2000])), [2500, 5000, 5000])
    for voltage in [1, 2, 5, 11, 20]:
        req, vb, ib = bridge('不平衡桥', [1000, 2000, 3000, 3000, 3000], voltage)
        if voltage == 11:
            close([req, vb['C'], vb['D'], ib[4]], [2200, 8, 7, 1 / 3000])
    bridge('Q5放大桥', [2000, 4000, 6000, 6000, 6000])
    for voltage in [1, 5, 10]:
        req, vb, ib = bridge('平衡桥', [1000, 2000, 2000, 4000, 1000], voltage)
        close([req, vb['C'] - vb['D'], ib[4]], [2000, 0, 0])
    for voltage in [1, 2, -1, 8]:
        close(controlled(2000, .0005, 1, voltage), voltage / 1000)
    close(controlled(4000, .00025, 1, 1), .0005)  # Q6
    for gain, expect in [(.00025, .00025), (.0005, 0), (.00075, -.00025)]:
        close(controlled(2000, gain, -1, 1), expect)
    # 零输入电阻：串联正电阻与反向CCVS抵消，改用测试电流。
    test_i, r = .001, 2000
    ur, ud = r * test_i, -r * test_i
    close([ur + ud, ur * test_i + ud * test_i], [0, 0])
    print('零输入电阻：test_current_mA=1, resistor_V=2, CCVS_V=-2, terminal_V=0')
    # 匹配一个工作点不能证明关系等效；比值不是固定斜率。
    close([1 / .001, 2 / .008], [1000, 250])
    # 三端关系漏一个外部控制量：同u=1V，uc变化导致输入电流变化。
    close([1 / 2000 + .0005 * uc for uc in [0, 2]], [.0005, .0015])
    print('非线性反例：i=(1mA/V^3)u^3，1V/2V时R_operating=1k/0.25kΩ')
    print('外部控制反例：同u=1V，uc=0V/2V时input=0.5mA/1.5mA')
    worst = max(ERRORS)
    for tol in [1e-9, 1e-10, 1e-11]:
        assert worst < tol
        print('阈值=%.0e，KCL及功率归一化检查通过' % tol)
    # 省略桥支路可看似接近，但原图电流非零，端口电阻确实改变。
    wrong = (1000 + 3000) * (2000 + 3000) / (1000 + 3000 + 2000 + 3000)
    assert abs(wrong - 2200) > 20
    print('误删桥支路：R_wrong_ohm=%.9f, R_correct_ohm=2200' % wrong)
    print('[OK] 原网络求解次数=%d，最大规范化KCL/功率残差=%.3e' % (CASES, worst))


def audit_text():
    text = (ROOT / '03_等效变换.md').read_text(encoding='utf-8')
    images = re.findall(r'!\[图 (\d+)：[^\]]*\]\(([^)]+)\)', text)
    assert [int(n) for n, _ in images] == list(range(1, 8))
    assert len(set(path for _, path in images)) == 7
    for _, path in images:
        assert (ROOT / path).is_file() and (ROOT / path).with_suffix('.png').is_file(), path
    questions = [int(n) for n in re.findall(r'\*\*Q(\d+)\.', text)]
    assert questions == list(range(1, 11))
    assert text.count('**参考答案：**') == 10
    assert '“' not in text and '”' not in text
    assert '<details' not in text and text.count('$$') % 2 == 0
    assert text.count('```') % 2 == 0
    head = '\n'.join(text.splitlines()[:40])
    for slot in ['前置', '预计时间', '一句话定位', '本讲回答什么', '本讲目标', '目标达成',
                 '怎么学这一讲', '这一讲有真实验证']:
        assert slot in head, slot
    for path in [ROOT / '03_等效变换.md', ROOT / 'AA_一览.md']:
        code, width = False, None
        for line_number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            if line.startswith('```'):
                code = not code
                width = None
            if code:
                continue
            if line.startswith('|'):
                count = len(line.split('|'))
                if width is None:
                    width = count
                assert width == count, (path.name, line_number, width, count)
            else:
                width = None
    print('[DOC] 7张图双格式引用、10道题/答案、ASCII引号、表格及公式容器通过')


def figures(redraw=False):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import schemdraw
    import schemdraw.elements as elm

    stems = ['lec03_fig1_loaded_divider_revised', 'lec03_fig2_divider_splitter_revised',
             'lec03_fig3_source_transform_revised', 'lec03_fig4_wye_delta_revised',
             'lec03_fig5_bridge_revised', 'lec03_fig6_controlled_port_revised',
             'lec03_fig7_input_boundaries']
    directory = ROOT / 'figures'
    if not redraw and any((directory / (s + ext)).exists() for s in stems for ext in ['.svg', '.png']):
        raise FileExistsError('修正版已存在，默认不覆盖；编写期间可用--redraw。')
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['svg.fonttype'] = 'path'
    plt.rcParams['axes.unicode_minus'] = False
    elm.style(elm.STYLE_IEC)
    schemdraw.config(font='Microsoft YaHei', fontsize=13)

    def label(d, xy, value, color='black'):
        d += elm.Label().at(xy).label(value).color(color)

    def save(d, stem):
        d.save(str(directory / (stem + '.svg')), transparent=False)
        d.save(str(directory / (stem + '.png')), transparent=False, dpi=160)
        plt.close('all')
        print('[FIG]', stem)

    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().at((0, 0)).up().length(6)
    label(d, (-1.2, 3), '9 V')
    d += elm.Line().at((0, 6)).right().length(4)
    d += elm.Resistor().at((4, 6)).down().length(3)
    d += elm.Resistor().at((4, 3)).down().length(3)
    label(d, (2.3, 4.5), 'R1 = 2 kΩ')
    label(d, (2.3, 1.5), 'R2 = 1 kΩ')
    d += elm.Line().at((4, 3)).right().length(3)
    d += elm.Resistor().at((7, 3)).down().length(3)
    label(d, (8.5, 1.5), 'RL = 1 kΩ')
    d += elm.Line().at((0, 0)).right().length(7)
    d += elm.Dot().at((4, 3))
    label(d, (5.5, 3.65), 'b: uo = 1.8 V')
    label(d, (4, -.6), '0: 参考结点')
    save(d, stems[0])

    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().at((0, 0)).up().length(4)
    label(d, (-1, 2), '9 V')
    d += elm.Resistor().at((0, 4)).right().length(3)
    d += elm.Resistor().at((3, 4)).right().length(3)
    d += elm.Line().at((6, 4)).down().length(4)
    d += elm.Line().at((6, 0)).left().length(6)
    label(d, (1.5, 4.6), 'R1 = 2 kΩ')
    label(d, (4.5, 4.6), 'R2 = 1 kΩ')
    label(d, (1.5, 3.4), '+ u1 -')
    label(d, (4.5, 3.4), '+ u2 -')
    d += elm.Arrow().at((1.2, 2.2)).right().length(1.5)
    label(d, (3.5, 1.4), 'i = 3 mA')
    label(d, (3, -.7), '(a) 串联：同电流，分电压')
    d += elm.SourceI().at((10, 0)).up().length(4)
    label(d, (8.6, 2), '6 mA')
    d += elm.Line().at((10, 4)).right().length(6)
    d += elm.Line().at((10, 0)).right().length(6)
    for x, text in [(13, '2 kΩ'), (16, '3 kΩ')]:
        d += elm.Resistor().at((x, 4)).down().length(4)
        label(d, (x + .9, 2), text)
        d += elm.Arrow().at((x, 3.9)).down().length(.65)
    label(d, (13.7, 3.6), 'i1')
    label(d, (16.7, 3.6), 'i2')
    label(d, (13, -.7), '(b) 并联：同电压u，分电流')
    save(d, stems[1])

    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().at((0, 0)).up().length(3)
    d += elm.Resistor().at((0, 3)).up().length(3)
    label(d, (-1.5, 1.5), 'US = 6 V')
    label(d, (-1.5, 4.5), 'Rs = 1 kΩ')
    for xy, value in [((0, 6), 'a'), ((0, 0), 'b')]:
        d += elm.Dot().at(xy)
        label(d, (.45, xy[1]), value)
    label(d, (4, 4.2), 'IS = US / Rs')
    label(d, (4, 3.5), '相同端子a、b')
    d += elm.SourceI().at((8, 0)).up().length(6)
    d += elm.Resistor().at((12, 6)).down().length(6)
    d += elm.Line().at((8, 6)).right().length(4)
    d += elm.Line().at((8, 0)).right().length(4)
    label(d, (6.65, 2.1), 'IS = 6 mA')
    label(d, (13.5, 3), 'Rs = 1 kΩ')
    for xy, value in [((12, 6), 'a'), ((12, 0), 'b')]:
        d += elm.Dot().at(xy)
        label(d, (12.45, xy[1]), value)
    label(d, (6, -1), '阻值保持；内部电流和功率不保持')
    save(d, stems[2])

    d = schemdraw.Drawing(show=False)
    for terminal, xy in [('1', (0, 4)), ('2', (0, 0)), ('3', (5, 2))]:
        d += elm.Resistor().at(xy).to((2.5, 2))
        d += elm.Dot().at(xy)
        label(d, (xy[0] + (-.5 if xy[0] == 0 else .5), xy[1]), terminal)
    d += elm.Dot().at((2.5, 2))
    label(d, (2.5, 1.3), 'n')
    label(d, (1.4, 3.6), 'r1')
    label(d, (1.4, .4), 'r2')
    label(d, (3.8, 2.5), 'r3')
    label(d, (2.5, -1), 'Y：中心只连这三臂')
    points = {'1': (10, 4), '2': (10, 0), '3': (15, 2)}
    for n1, n2, xy, text in [('1', '2', (9.1, 2), 'R12'),
                             ('2', '3', (12.8, .35), 'R23'),
                             ('3', '1', (12.8, 3.65), 'R31')]:
        d += elm.Resistor().at(points[n1]).to(points[n2])
        label(d, xy, text)
    for terminal, xy in points.items():
        d += elm.Dot().at(xy)
        label(d, (xy[0] + (-.5 if xy[0] == 10 else .5), xy[1]), terminal)
    label(d, (12.5, -1), 'Δ：三个端子两两连接')
    label(d, (7.5, 2), '三端等效')
    save(d, stems[3])

    d = schemdraw.Drawing(show=False)
    points = {'A': (0, 2), 'C': (3, 4), 'D': (3, 0), 'B': (6, 2)}
    for n1, n2, text, xy in [('A', 'C', 'R1 = 1 kΩ', (1, 4.15)),
                              ('A', 'D', 'R2 = 2 kΩ', (1, -.45)),
                              ('C', 'B', 'R3 = 3 kΩ', (5, 4.15)),
                              ('D', 'B', 'R4 = 3 kΩ', (5, -.45)),
                              ('C', 'D', 'R5 = 3 kΩ', (4.5, 2))]:
        color = '#2471a3' if n1 in ['C', 'D'] else 'black'
        d += elm.Resistor().at(points[n1]).to(points[n2]).color(color)
        label(d, xy, text, color)
    for node, xy in points.items():
        d += elm.Dot().at(xy)
        label(d, (xy[0], xy[1] + (.5 if xy[1] >= 2 else -.5)), node)
    label(d, (3, -1.4), '原桥：选蓝色Δ(C,D,B)')
    p = {'A': (10, 2), 'C': (13, 4), 'D': (13, 0), 'n': (16, 2), 'B': (20, 2)}
    for n1, n2, text, xy in [('A', 'C', '1 kΩ', (11.3, 4.15)),
                              ('A', 'D', '2 kΩ', (11.3, -.45)),
                              ('C', 'n', '1 kΩ', (14.8, 4.15)),
                              ('D', 'n', '1 kΩ', (14.8, -.45)),
                              ('n', 'B', '1 kΩ', (18, 2.6))]:
        d += elm.Resistor().at(p[n1]).to(p[n2])
        label(d, xy, text)
    for node, xy in p.items():
        d += elm.Dot().at(xy)
        label(d, (xy[0], xy[1] + (.5 if xy[1] >= 2 else -.5)), node)
    label(d, (15, -1.4), '变换后：A-n两路并联，再串n-B')
    save(d, stems[4])

    d = schemdraw.Drawing(show=False)
    d += elm.Resistor().at((0, 4)).down().length(4)
    d += elm.SourceControlledI().at((4, 4)).down().length(4)
    d += elm.Line().at((0, 4)).right().length(4)
    d += elm.Line().at((0, 0)).right().length(4)
    d += elm.Arrow().at((2, 6)).down().length(2)
    d += elm.Dot().at((2, 4))
    d += elm.Dot().at((2, 0))
    label(d, (4, 5.5), 'it（流入a）')
    label(d, (2.5, 4.5), 'a: +')
    label(d, (2.5, -.5), 'b: -')
    label(d, (-1.7, 2), 'R = 2 kΩ')
    label(d, (6, 2.5), 'id = g ut')
    label(d, (6, 1.7), 'g = 0.5 mS')
    label(d, (2, -1.2), 'ut = Va - Vb；it = iR + id')
    save(d, stems[5])

    fig, ax = plt.subplots(figsize=(7, 4.5))
    u = np.linspace(-2, 2, 100)
    for gain, description in [(.00025, 'g=0.25mS：Rin=4kΩ'),
                              (.0005, 'g=0.5mS：开路型'),
                              (.00075, 'g=0.75mS：Rin=-4kΩ')]:
        ax.plot(u, (1 / 2000 - gain) * u * 1000, label=description)
    ax.plot([0, 0], [-.55, .55], '--', label='零输入电阻：ut=0（改用流源测试）')
    ax.set(xlabel='测试电压 ut / V', ylabel='流入正端电流 it / mA')
    ax.grid(alpha=.3)
    ax.legend(fontsize=10)
    fig.tight_layout()
    fig.savefig(directory / (stems[6] + '.svg'))
    fig.savefig(directory / (stems[6] + '.png'), dpi=160)
    plt.close(fig)
    print('[FIG]', stems[6])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--figures', action='store_true')
    parser.add_argument('--redraw', action='store_true')
    parser.add_argument('--audit-text', action='store_true')
    args = parser.parse_args()
    start = perf_counter()
    verify_math()
    if args.figures:
        figures(args.redraw)
    if args.audit_text:
        audit_text()
    print('运行时间_s=%.3f' % (perf_counter() - start))
