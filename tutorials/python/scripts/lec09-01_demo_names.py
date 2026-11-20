"""第 09 讲验证脚本：执行顺序 / print 参数 / input 返回类型 / 绑定与对象 / 缩进 / 注释与文档字符串。

规模纪律：4 个子进程 + 若干内存操作，目标 < 5 秒。
运行：uv run python tutorials/python/scripts/lec09-01_demo_names.py

讲义里引用的每一段输出都来自本脚本。
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


def run_script(path: Path, stdin: str = "") -> subprocess.CompletedProcess:
    # 让子进程用 UTF-8 写输出，否则 Windows 上按 GBK 写、父进程按 UTF-8 解码会得到替换字符。
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    return subprocess.run(
        [sys.executable, str(path)],
        input=stdin, capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=env, timeout=30,
    )


def tail(text: str, n: int = 2) -> str:
    lines = [line for line in text.splitlines() if line.strip()]
    return "\n".join(lines[-n:])


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)

        section("1. 脚本自上而下执行：写在前面的先发生")
        order = root / "order.py"
        order.write_text(
            'print("第一行")\n'
            'print("第二行")\n'
            'print("第三行")\n',
            encoding="utf-8",
        )
        r = run_script(order)
        print("  输出:")
        for line in r.stdout.rstrip().splitlines():
            print("    " + line)
        print(f"  退出码 = {r.returncode}")
        print("  预期: 顺序就是书写顺序；Python 不声明入口，从第一行开始逐句执行。\n")

        section("2. print 的三个参数：sep / end / file")
        print("  print('a', 'b', 'c')            ->", end=" ")
        print("a", "b", "c")
        print("  print('a', 'b', sep='-')        ->", end=" ")
        print("a", "b", sep="-")
        print("  print('x', end='')  再 print('y') ->", end=" ")
        print("x", end="")
        print("y")
        out_file = root / "out.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            print("写进文件的一行", file=f)
        print(f"  用 file= 写文件后，文件内容是: {out_file.read_text(encoding='utf-8').strip()!r}")
        print("  预期: sep 管多个值之间的分隔（默认空格），end 管结尾（默认换行），")
        print("        file 管写到哪里（默认标准输出）。第 19 讲会正式讲文件。\n")

        section("3. input 拿回来的永远是字符串")
        ask = root / "ask.py"
        ask.write_text(
            'a = input("第一个数: ")\n'
            'b = input("第二个数: ")\n'
            'print("a 的类型:", type(a).__name__)\n'
            'print("直接相加:", a + b)\n'
            'print("转成整数后相加:", int(a) + int(b))\n',
            encoding="utf-8",
        )
        r = run_script(ask, stdin="3\n4\n")
        print("  输入 3 和 4 之后:")
        for line in r.stdout.rstrip().splitlines():
            print("    " + line)
        print("  预期: a 的类型是 str；直接相加得到 '34'（字符串拼接），")
        print("        int() 转换之后才得到 7。所以 input 之后必须自己转类型。\n")

        bad = root / "bad_input.py"
        bad.write_text('n = int("abc")\n', encoding="utf-8")
        rb = run_script(bad)
        print("  如果转不了会怎样（int('abc')）:")
        print("    " + tail(rb.stderr, 1))
        print(f"    退出码 = {rb.returncode}")
        print("  预期: ValueError，消息里给出具体的字符串。第 18 讲会讲怎么处理它。\n")

        section("4. 变量是标签：重新绑定不会改旧对象")
        a = 1
        b = a
        print(f"  a = 1; b = a       -> a={a}, b={b}, id 相同吗 = {id(a) == id(b)}")
        a = 2
        print(f"  再执行 a = 2       -> a={a}, b={b}")
        print("  预期: b 仍然是 1。`a = 2` 是把名字 a 撕下来贴到新对象 2 上，")
        print("        并没有改动对象 1，b 还贴在 1 上。\n")

        section("5. 可变对象的别名：改内容会影响同一个对象的另一个名字")
        xs = [1, 2]
        ys = xs
        ys.append(3)
        print(f"  xs = [1, 2]; ys = xs; ys.append(3)")
        print(f"  -> xs={xs}, ys={ys}, 是同一个对象吗 = {xs is ys}")
        zs = [1, 2, 3]
        print(f"  另造一个内容相同的 zs=[1,2,3]：xs == zs 吗 = {xs == zs}，xs is zs 吗 = {xs is zs}")
        print("  预期: xs 和 ys 是同一个列表的两个名字，改一个两个都变；")
        print("        zs 内容相等但是另一个对象。第 12 讲讲拷贝时会正式处理这个坑。\n")

        section("6. 动态类型：同一个名字可以先后指向不同类型的对象")
        x = 10
        print(f"  x = 10      -> type = {type(x).__name__}")
        x = "十"
        print(f"  x = '十'    -> type = {type(x).__name__}")
        x = 3.5
        print(f"  x = 3.5     -> type = {type(x).__name__}")
        print("  预期: 不报错。类型属于对象，不属于名字；名字只是标签。\n")

        section("7. 名字的规则：关键字不能用，中文可以但不建议")
        kw = root / "kw.py"
        kw.write_text("for = 1\n", encoding="utf-8")
        rk = run_script(kw)
        print("  用关键字当名字（for = 1）:")
        print("    " + tail(rk.stderr, 1))
        cn = root / "cn.py"
        cn.write_text('半径 = 3\nprint("半径 =", 半径)\n', encoding="utf-8")
        rc = run_script(cn)
        print(f"  用中文当名字: 退出码={rc.returncode} 输出={rc.stdout.strip()!r}")
        print("  预期: 关键字（for/if/class 等）保留给语法用，不能当名字，会报 SyntaxError；")
        print("        中文名字技术上合法，但团队协作时会造成输入法切换与检索困难，不建议。\n")

        section("8. 缩进是语法，不是排版")
        ind = root / "ind.py"
        ind.write_text('if True:\nprint("x")\n', encoding="utf-8")
        ri = run_script(ind)
        print("  if 后面没有缩进:")
        print("    " + tail(ri.stderr, 1))
        ok = root / "ok.py"
        ok.write_text('if True:\n    print("x")\n', encoding="utf-8")
        ro = run_script(ok)
        print(f"  加上四个空格: 退出码={ro.returncode} 输出={ro.stdout.strip()!r}")
        print("  预期: 前者 IndentationError，后者正常。")
        print("        if 本身是控制流（第 14 讲），这里只借它演示'块由缩进决定'。\n")

        section("9. 注释与文档字符串不是一回事")
        doc = root / "doc.py"
        doc.write_text(
            "# 这是注释，Python 执行时会忽略它\n"
            "def area(r):\n"
            '    """返回圆面积，r 为半径。"""\n'
            "    return 3.14 * r * r\n"
            "\n"
            "print('函数的文档字符串 =', repr(area.__doc__))\n"
            "print('调用结果 =', area(1))\n",
            encoding="utf-8",
        )
        rd = run_script(doc)
        for line in rd.stdout.rstrip().splitlines():
            print("    " + line)
        print("  预期: `#` 开头的那行不会出现在 __doc__ 里；函数体里第一句三引号字符串会成为")
        print("        area.__doc__。`def` 与三引号字符串的完整规则在第 15、11 讲讲。\n")

        section("10. 一个完整的小脚本：读两个数，输出四则运算")
        calc = root / "calc.py"
        calc.write_text(
            'a_text = input("a = ")\n'
            'b_text = input("b = ")\n'
            "a = float(a_text)\n"
            "b = float(b_text)\n"
            'print("和 =", a + b)\n'
            'print("差 =", a - b)\n'
            'print("积 =", a * b)\n'
            'print("商 =", a / b)\n',
            encoding="utf-8",
        )
        rcalc = run_script(calc, stdin="7\n2\n")
        print("  输入 7 与 2:")
        for line in rcalc.stdout.rstrip().splitlines():
            print("    " + line)
        print(f"  退出码 = {rcalc.returncode}")
        print("  预期: 四个结果分别是 9.0 / 5.0 / 14.0 / 3.5。")
        print("        注意全是小数：float 参与运算，结果就是 float（第 10 讲细讲）。")


if __name__ == "__main__":
    main()
