"""探针：确认 SchemDraw 画 KCL/KVL 示意图所需的元素与用法。

检查项：
1. 元素名清单：Arrow / Dot / Label / Encircle / RBox / SourceControlled* / CurrentLabel
2. 关键元素构造签名
3. 冒烟测试：箭头、自由文本、虚线、菱形受控源、占位框逐个试画
   （每个独立 try，失败不影响其余；结果存 _probe_circuit/figures/probe_elements_*.png）
"""
import os
import inspect
import traceback

import matplotlib
matplotlib.use("Agg")

import schemdraw
import schemdraw.elements as elm

schemdraw.config(font="Microsoft YaHei", fontsize=14)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

# ---- 1. 元素名清单 ----
names = [n for n in dir(elm) if not n.startswith("_")]
for key in ("Arrow", "Dot", "Label", "Encircle", "RBox", "SourceControlled", "CurrentLabel", "Battery", "SourceV", "SourceI", "Line"):
    hits = [n for n in names if key.lower() in n.lower()]
    print(f"[names] {key}: {hits}")

# ---- 2. 签名 ----
for target in ("Arrow", "Encircle", "RBox", "SourceControlledV", "SourceControlledI", "Dot", "Label"):
    obj = getattr(elm, target, None)
    if obj is None:
        print(f"[sig] {target}: NOT FOUND")
        continue
    try:
        print(f"[sig] {target}.__init__: {inspect.signature(obj.__init__)}")
    except Exception as exc:
        print(f"[sig] {target}: sig err {exc}")

print("[sig] Drawing label/text methods:",
      [m for m in dir(schemdraw.Drawing) if "label" in m.lower() or "text" in m.lower() or m == "add"])

# ---- 3. 冒烟测试 ----
def smoke(tag, build):
    try:
        with schemdraw.Drawing(show=False) as d:
            build(d)
        path = os.path.join(OUT, f"probe_elements_{tag}.png")
        d.save(path, transparent=False, dpi=150)
        print(f"[smoke] {tag}: OK -> {path}")
    except Exception:
        print(f"[smoke] {tag}: FAIL")
        traceback.print_exc()

# 3a. 箭头 .at().to() + 标签，附带一个 Dot
def build_arrow(d):
    d += elm.Line().at((0, 2)).to((2, 2))
    d += elm.Arrow().at((2, 2)).to((4, 2)).label("->right", loc="top")
    d += elm.Arrow().at((4, 2)).to((4, 4)).label("^up", loc="right")
    d += elm.Dot().at((4, 2))
smoke("arrow", build_arrow)

# 3b. 自由文本（Label 元素）
def build_label(d):
    d += elm.Line().at((0, 0)).to((3, 0))
    d += elm.Label().at((1.5, 0.6)).label("free text 自由文本")
smoke("label", build_label)

# 3c. 虚线（Line 的 ls 参数试探）
def build_dash_line(d):
    d += elm.Resistor().at((0, 0)).to((3, 0)).label("R")
    d += elm.Line(ls="--").at((0, 1)).to((3, 1))
smoke("dash_line", build_dash_line)

# 3d. 虚线椭圆圈选（Encircle）——第一参数是元素列表

def build_encircle(d):
    r1 = elm.Resistor().at((0, 0)).to((3, 0)).label("R1")
    r2 = elm.Resistor().at((0, -1)).to((3, -1)).label("R2")
    d += r1
    d += r2
    try:
        d += elm.Encircle([r1, r2], padx=0.35, pady=0.35).linestyle("--")
        print("[encircle] method: .linestyle('--') works")
    except AttributeError:
        d += elm.Encircle([r1, r2], padx=0.35, pady=0.35, ls="--")
        print("[encircle] method: ls='--' kwarg works")
smoke("encircle", build_encircle)

# 3e. 受控源菱形 + 占位框 RBox
def build_controlled(d):
    d += elm.SourceControlledV().at((0, 0)).to((0, 3)).label("CCVS", loc="right")
    d += elm.RBox().at((3, 0)).to((3, 3)).label("A", loc="right")
smoke("controlled_rbox", build_controlled)