"""第 17 讲验证脚本：import 做了什么 / __name__ / 包的目录结构 / python -m / sys.path / 循环导入。

规模纪律：建一个临时小项目并跑 4 个子进程，目标 < 5 秒。
运行：uv run python tutorials/python/scripts/lec17-01_demo_modules.py

讲义里引用的每一条输出都来自本脚本。
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

WIDTH = 68


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    return subprocess.run(
        args, cwd=str(cwd), capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=env, timeout=60,
    )


def show(result: subprocess.CompletedProcess, label: str) -> None:
    print(f"  [{label}] 退出码={result.returncode}")
    body = (result.stdout + result.stderr).rstrip()
    for line in body.splitlines():
        print("    " + line)
    print()


def build_project(root: Path) -> None:
    (root / "tools.py").write_text(
        'print("tools 模块被加载了")\n'
        "\n"
        "def double(x):\n"
        '    """返回两倍。"""\n'
        "    return x * 2\n"
        "\n"
        'if __name__ == "__main__":\n'
        '    print("直接运行 tools.py，__name__ =", __name__)\n'
        '    print("double(21) =", double(21))\n',
        encoding="utf-8",
    )
    (root / "main.py").write_text(
        "import tools\n"
        'print("在 main.py 里，tools.__name__ =", tools.__name__)\n'
        'print("double(5) =", tools.double(5))\n',
        encoding="utf-8",
    )
    pkg = root / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text(
        'print("pkg/__init__.py 被执行了")\n',
        encoding="utf-8",
    )
    (pkg / "a.py").write_text(
        'print("pkg/a.py 被加载")\n'
        "VALUE = '来自 a'\n"
        "\n"
        "def hello():\n"
        '    return "hello from a"\n',
        encoding="utf-8",
    )
    (pkg / "b.py").write_text(
        "from pkg import a\n"
        'print("b 看到 a.VALUE =", a.VALUE)\n',
        encoding="utf-8",
    )
    (pkg / "__main__.py").write_text(
        'print("pkg/__main__.py 被当作入口执行")\n'
        "from pkg import a\n"
        "print(a.hello())\n",
        encoding="utf-8",
    )
    cyc = root / "cyc"
    cyc.mkdir()
    (cyc / "__init__.py").write_text("", encoding="utf-8")
    (cyc / "x.py").write_text(
        "from cyc.y import y_func\n"
        "def x_func():\n"
        "    return 'x'\n",
        encoding="utf-8",
    )
    (cyc / "y.py").write_text(
        "from cyc.x import x_func\n"
        "def y_func():\n"
        "    return 'y'\n",
        encoding="utf-8",
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        build_project(root)

        section("1. import 执行了什么：整个模块文件被跑一遍")
        show(run([sys.executable, "main.py"], root), "python main.py")
        print("  预期: 先出现 'tools 模块被加载了'，再出现后面的输出 —— import 会执行模块顶层代码。")
        print("        第二次 import 同一个模块不会重复执行（模块被缓存）。\n")

        section("2. __name__ 的两个值：直接运行 vs 被导入")
        show(run([sys.executable, "tools.py"], root), "python tools.py")
        print("  预期: 直接运行 scripts 时 __name__ 是 '__main__'，所以 if 块执行；")
        print("        被 import 时 __name__ 是 'tools'，if 块不执行（上一节的输出里没有那句）。\n")

        section("3. 三种 import 写法")
        snippet = (
            "import json\n"
            "import json as js\n"
            "from math import sqrt, pi\n"
            "print('json.dumps:', json.dumps({'a': 1}, ensure_ascii=False))\n"
            "print('as 别名   :', js.dumps({'a': 1}))\n"
            "print('from 直接拿:', sqrt(9), round(pi, 4))\n"
        )
        (root / "import_demo.py").write_text(snippet, encoding="utf-8")
        show(run([sys.executable, "import_demo.py"], root), "三种写法")
        print("  预期: `import 模块` 拿整个模块；`as` 起别名；`from 模块 import 名字` 只拿某几个名字。")
        print("        名字拿进来之后就和本地名字一样用，看不出来源——这正是命名冲突的来源。\n")

        section("4. 包：一个目录 + __init__.py")
        (root / "use_pkg.py").write_text(
            "import pkg.a\n"
            "from pkg import b\n"
            'print("pkg.a.VALUE =", pkg.a.VALUE)\n',
            encoding="utf-8",
        )
        show(run([sys.executable, "use_pkg.py"], root), "import pkg.a / from pkg import b")
        print("  预期: import 包里的模块会先执行 pkg/__init__.py，再执行被导入的那个模块。")
        print("        __init__.py 可以留空，它的存在本身就是“这是一个包”的标志。\n")

        section("5. python -m 与直接跑文件的区别")
        show(run([sys.executable, "-m", "pkg"], root), "python -m pkg")
        print("  预期: -m 把包当作入口，执行 pkg/__main__.py；sys.path[0] 是当前目录。")
        print("        直接 `python pkg/__main__.py` 也能跑，但 sys.path[0] 会变成 pkg/，")
        print("        包内的绝对导入就可能失败——这是“能跑”与“该怎么跑”的区别。\n")

        section("6. sys.path：import 去哪找模块")
        (root / "path_demo.py").write_text(
            "import sys\n"
            "for i, p in enumerate(sys.path[:4]):\n"
            "    print(f'  sys.path[{i}] = {p!r}')\n",
            encoding="utf-8",
        )
        show(run([sys.executable, "path_demo.py"], root), "sys.path 前四项")
        print("  预期: 第一项是脚本所在目录（绝对路径或空串），接着是标准库目录；")
        print("        site-packages 在更后面。自己写的模块能被导入，靠的就是第一项。\n")

        section("7. 循环导入：真实报错")
        (root / "circular_demo.py").write_text("from cyc.x import x_func\n", encoding="utf-8")
        show(run([sys.executable, "circular_demo.py"], root), "循环导入")
        print("  预期: 抛 ImportError，消息里点名 partially initialized module，并提示可能是循环导入。")
        print("        注意：不是所有“你导我、我导你”都报错 —— 导“子模块”往往能过，")
        print("        导“半初始化模块里的名字”才会失败；修法是把公共部分拆出去，或把 import 挪进函数里。\n")

        section("8. 标准库地图：先知道有什么")
        stdlib = [
            ("math", "数学函数：sqrt、sin、log、pi"),
            ("random", "随机数：randint、choice、shuffle、seed"),
            ("statistics", "统计：mean、median、stdev"),
            ("datetime", "日期时间：date、datetime、timedelta"),
            ("json", "JSON 读写：loads/dumps、load/dump"),
            ("csv", "CSV 读写：reader/writer、DictReader"),
            ("pathlib", "路径操作：Path 的拼接、判断、遍历"),
            ("collections", "容器扩展：Counter、defaultdict、deque"),
            ("itertools", "迭代工具：product、groupby、chain"),
            ("functools", "函数工具：lru_cache、wraps、reduce"),
            ("re", "正则表达式：search、findall、sub"),
            ("os / sys", "与操作系统、解释器交互：环境变量、参数、路径"),
            ("logging", "日志：分级、格式化、输出到文件"),
            ("unittest", "单元测试框架（第 25 讲）"),
        ]
        for name, desc in stdlib:
            print(f"  {name:<12}{desc}")
        print("  预期: 这张表就是“标准库大概有什么”的索引；用到时再查文档，不必背 API。\n")

        section("9. 安装名与导入名可能不同")
        print("  pip 装的名字不一定是 import 的名字，例子：")
        print("    pip install pillow      ->  import PIL")
        print("    pip install opencv-python -> import cv2")
        print("    pip install scikit-learn  -> import sklearn")
        print("    pip install beautifulsoup4 -> import bs4")
        print("  本机未安装这些包，所以这里只列事实，不做实测；装不上时先看官方文档的 import 名。")

    print("\n  提示: 判断“该不该拆模块”，看这段代码是不是“一组只服务同一件事的函数与数据”。")


if __name__ == "__main__":
    main()
