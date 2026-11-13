# 规模纪律：只做解释器状态与文件系统观察，目标 < 2 秒。
# 目的：为第 01 讲"一段源码到结果"的每一环提供可复跑的实测证据。
import importlib
import shutil
import sys
import tempfile
from pathlib import Path

print("=== EXP1: 现在是谁在跑这个文件 ===")
print(f"python version : {sys.version.split()[0]}")
print(f"interpreter    : {sys.executable}")
print(f"script file    : {__file__}")
print(f"module name    : {__name__}")
print(f"cwd            : {Path.cwd()}")
print(f"script dir     : {Path(__file__).resolve().parent}")
print("expect: interpreter 是某个 python.exe；script file 是这个 .py；module name 是 __main__")
assert sys.executable.lower().endswith("python.exe") or "python" in Path(sys.executable).name.lower()
assert __name__ == "__main__"

print()
print("=== EXP2: sys.path[0] 是脚本所在目录 ===")
for i, p in enumerate(sys.path[:3]):
    print(f"sys.path[{i}] = {p!r}")
print("expect: sys.path[0] 等于 script dir；其余是标准库与 site-packages")
assert Path(sys.path[0]).resolve() == Path(__file__).resolve().parent

print()
print("=== EXP3: __pycache__ 由 import 生成，删掉照样能跑 ===")
with tempfile.TemporaryDirectory() as td:
    d = Path(td)
    (d / "mini_mod.py").write_text("VALUE = 42\n", encoding="utf-8")
    sys.path.insert(0, str(d))

    import mini_mod  # noqa: E402  (故意在函数外 import，演示 import 的副作用)

    pycache = d / "__pycache__"
    pyc_files = sorted(p.name for p in pycache.glob("mini_mod*.pyc"))
    print(f"after import   : __pycache__ exists = {pycache.exists()}")
    print(f"pyc files      : {pyc_files}")
    assert pycache.exists() and len(pyc_files) == 1

    shutil.rmtree(pycache)
    print(f"after delete   : __pycache__ exists = {pycache.exists()}")
    print(f"module still   : mini_mod.VALUE = {mini_mod.VALUE}")
    assert mini_mod.VALUE == 42

    del sys.modules["mini_mod"]
    importlib.invalidate_caches()
    import mini_mod as mini_mod_2  # noqa: F811

    print(f"re-import      : __pycache__ exists = {pycache.exists()}")
    assert pycache.exists()
    print("expect: 删掉缓存不影响已加载的模块；重新 import 会再生成缓存")

print()
print("=== EXP4: 名字指向对象，id 观察（先只记现象）===")
a = 256
b = 256
c = int("257")
d = int("257")
print(f"a is b (256)      : {a is b};  id(a)==id(b): {id(a) == id(b)}")
print(f"c is d ('257')    : {c is d};  c == d: {c == d};  id 相同: {id(c) == id(d)}")
print("expect: 256 的两个名字常指向同一对象；用 int('257') 造出的两个 257 是不同对象但相等")
assert a is b
assert c == d

print()
print("=== EXP5: cwd 与脚本所在目录是两个东西 ===")
here = Path.cwd()
script_dir = Path(__file__).resolve().parent
print(f"cwd        : {here}")
print(f"script dir : {script_dir}")
print(f"same?      : {here == script_dir}")
print("expect: 从项目根运行本脚本时两者不同；换个目录再运行，cwd 会变而 script dir 不变")

print()
print("[OK] launcher chain demo finished")
