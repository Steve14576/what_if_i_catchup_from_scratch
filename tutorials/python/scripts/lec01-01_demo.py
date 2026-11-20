"""第 01 讲验证脚本：文本 / 解释器 / 两种运行方式 / 报错结构 / 退出码。

规模纪律：启动 7 个子进程 + 一次 REPL 模拟，目标 < 5 秒。
运行：uv run python tutorials/python/scripts/lec01-01_demo.py

讲义里引用的每一段输出、每一个返回码，都由本脚本实际跑出；
读者可以把本文件复制出来自己跑，对照讲义。
"""

import code
import contextlib
import io
import subprocess
import sys
import tempfile
from pathlib import Path

WIDTH = 68


def banner(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def run(path: Path) -> subprocess.CompletedProcess:
    """用当前这个解释器再启动一个子进程去跑脚本，抓回三条信息。"""
    return subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )


def tail(text: str, n: int) -> str:
    """取 stderr 末尾 n 行非空内容——报错最要紧的信息在最后。"""
    lines = [line for line in text.splitlines() if line.strip()]
    return "\n".join(lines[-n:])


def write(root: Path, name: str, body: str) -> Path:
    path = root / name
    path.write_text(body, encoding="utf-8")
    return path


def main() -> None:
    banner("0. 现在干活的到底是谁")
    print(f"解释器版本: {sys.version.split()[0]}")
    print(f"解释器路径: {sys.executable}")
    print("预期: 这里打印的路径就是 '装 Python' 装出来的那个可执行文件；")
    print("      下面所有子进程都用同一个解释器启动。")

    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)

        banner("1. 脚本里光写表达式，结果是丢掉的")
        expr_only = write(root, "expr_only.py", "1 + 1\n'abc'.upper()\n")
        expr_print = write(root, "expr_print.py", "print(1 + 1)\nprint('abc'.upper())\n")

        r1 = run(expr_only)
        print(f"[expr_only.py] 退出码={r1.returncode}  stdout={r1.stdout!r}")
        print("预期: stdout 为空字符串 —— 两行表达式算完就扔，不会被显示。")

        r2 = run(expr_print)
        print(f"[expr_print.py] 退出码={r2.returncode}  stdout={r2.stdout!r}")
        print("预期: stdout 里是 '2' 与 'ABC' —— 只有 print 才把值送到屏幕上。")

        banner("2. 交互式解释器（REPL）会自动显示表达式的值")
        sink = io.StringIO()
        console = code.InteractiveConsole()
        with contextlib.redirect_stdout(sink):
            for source in ["1 + 1", "name = 'python'", "name.upper()"]:
                console.push(source)
        repl_out = sink.getvalue()
        print(f"[模拟 REPL 输出] {repl_out!r}")
        print("预期: 出现 '2' 与 \"'PYTHON'\"，而 'name = ...' 这一行没有任何输出。")
        print("      同一句 1 + 1，在 REPL 里有回显，在脚本里没有 —— 这就是两种环境的差别。")

        banner("3. 后缀名不决定它是不是程序")
        hello_py = write(root, "hello.py", "print('hello, python')\n")
        hello_txt = write(root, "hello.txt", "print('hello, python')\n")
        for path in (hello_py, hello_txt):
            r = run(path)
            print(f"[{path.name}] 退出码={r.returncode}  stdout={r.stdout.strip()!r}")
        print("预期: 两个文件输出完全一样 —— 解释器看的是内容，不是扩展名。")

        banner("4. 四种常见报错：最后一行是类型和消息")
        cases = {
            "err_syntax.py": 'print("hello"\n',
            "err_name.py": "print(total)\n",
            "err_indent.py": 'if True:\nprint("x")\n',
            "err_missing.py": 'open("no_such_file.txt", encoding="utf-8")\n',
        }
        for name, body in cases.items():
            path = write(root, name, body)
            r = run(path)
            print(f"--- {name}  退出码={r.returncode}")
            print(tail(r.stderr, 4))
        print("预期: 四种错误的最后一行分别是 SyntaxError / NameError /")
        print("      IndentationError / FileNotFoundError，且退出码都是 1。")

        banner("5. 退出码：没有输出不等于成功")
        ok = write(root, "ok.py", "print('done')\n")
        quiet = write(root, "quiet.py", "x = 1 + 1\n")
        for path in (ok, quiet):
            r = run(path)
            print(f"[{path.name}] 退出码={r.returncode}  stdout={r.stdout.strip()!r}")
        print("预期: ok.py 退出码 0；quiet.py 退出码也是 0，但一个字都没输出。")
        print("      所以'没输出'不能证明'成功'，'有输出'也不能证明'正确'。")

        banner("6. 一次汇总")
        print(f"{'脚本':<18}{'退出码':<8}{'stdout 长度':<12}")
        for path in (expr_only, expr_print, hello_py, ok, quiet):
            r = run(path)
            print(f"{path.name:<18}{r.returncode:<8}{len(r.stdout):<12}")
        print("预期: 全部退出码 0（正常结束）；差异只在 stdout 有没有内容。")


if __name__ == "__main__":
    main()
