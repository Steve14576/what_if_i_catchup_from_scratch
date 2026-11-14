# 规模纪律：只读解释器与环境状态，不建环境、不装包，目标 < 2 秒。
# 目的：为第 02 讲"装在哪、谁被找到、包装到哪、编码走哪条路"提供可复跑的实测。
import locale
import os
import sys
import sysconfig
from pathlib import Path

print("=== EXP1: 现在这份解释器是谁、是不是虚拟环境 ===")
print(f"executable   : {sys.executable}")
print(f"prefix       : {sys.prefix}")
print(f"base_prefix  : {sys.base_prefix}")
print(f"in a venv?   : {sys.prefix != sys.base_prefix}")
print(f"version      : {sys.version.split()[0]}")
print("expect: prefix 是当前环境目录；它不等于 base_prefix 时，说明在一个虚拟环境里")
assert sys.prefix and sys.base_prefix

print()
print("=== EXP2: 第三方包装在哪 ===")
purelib = sysconfig.get_paths()["purelib"]
print(f"site-packages: {purelib}")
print(f"is it site-packages? {purelib.endswith('site-packages')}")
import json  # noqa: E402  用一个标准库模块演示"模块在磁盘上的位置"
print(f"json module   : {json.__file__}")
assert purelib.endswith("site-packages")
assert Path(json.__file__).exists()

print()
print("=== EXP3: 编码不是只有一个 ===")
print(f"stdout.encoding      : {sys.stdout.encoding}")
print(f"stdout.isatty()      : {sys.stdout.isatty()}")
print(f"locale preferred     : {locale.getpreferredencoding(False)}")
print(f"filesystem encoding  : {sys.getfilesystemencoding()}")
print("expect: 被重定向/被捕获时 stdout 用区域编码(中文 Windows 常为 gbk/cp936)；文件系统用 utf-8")

print()
print("=== EXP4: PATH 里到底有没有 Python ===")
entries = [p for p in os.environ.get("PATH", "").split(os.pathsep) if p]
python_like = [p for p in entries if "python" in p.lower()]
print(f"PATH entries       : {len(entries)}")
print(f"entries with python: {len(python_like)}")
for p in python_like[:3]:
    print(f"  {p}")
print("expect: 本仓库这台机器上为 0——所以裸敲 python 会报'不是内部或外部命令'")

print()
print("=== EXP5: import 时 Python 去哪里找 ===")
for i, p in enumerate(sys.path[:3]):
    shown = p if p else "<空字符串，表示当前工作目录>"
    print(f"sys.path[{i}] = {shown}")
print("expect: 用脚本方式运行时，sys.path[0] 是脚本所在目录；其后是标准库与 site-packages")

print()
print("[OK] environment demo finished")
