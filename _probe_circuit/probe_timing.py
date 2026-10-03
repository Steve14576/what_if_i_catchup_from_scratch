"""计时探针：逐步定位探针 A 卡在哪一步（每步 print + flush，超时也能看到卡点）。

输出：figures/_timing_test.svg / .png（临时产物）
"""
import sys
import time

t0 = time.time()
import matplotlib
print('[T] import matplotlib: %.1fs' % (time.time() - t0)); sys.stdout.flush()

t1 = time.time()
import matplotlib.font_manager as fm
fm.fontManager.findfont('Microsoft YaHei')
print('[T] fontmanager findfont YaHei: %.1fs' % (time.time() - t1)); sys.stdout.flush()

t2 = time.time()
import schemdraw
import schemdraw.elements as elm
print('[T] import schemdraw: %.1fs' % (time.time() - t2)); sys.stdout.flush()

t3 = time.time()
elm.style(elm.STYLE_IEC)
schemdraw.config(font='Microsoft YaHei', fontsize=15)
print('[T] config: %.1fs' % (time.time() - t3)); sys.stdout.flush()

t4 = time.time()
with schemdraw.Drawing() as d:
    d += elm.SourceV().up().label('$U_S$ = 5 V', loc='left')
    d += elm.Switch().right().label('S（t = 0 闭合）')
    d += elm.Resistor().right().label('R = 1 kΩ')
    d += elm.Capacitor().down().label('C = 1 μF', loc='right')
    d += elm.Line().left()
print('[T] build circuit: %.1fs' % (time.time() - t4)); sys.stdout.flush()

t5 = time.time()
d.save('_probe_circuit/figures/_timing_test.svg', transparent=False)
print('[T] save svg: %.1fs' % (time.time() - t5)); sys.stdout.flush()

t6 = time.time()
d.save('_probe_circuit/figures/_timing_test.png', transparent=False, dpi=200)
print('[T] save png: %.1fs' % (time.time() - t6)); sys.stdout.flush()
print('[OK] timing probe done')