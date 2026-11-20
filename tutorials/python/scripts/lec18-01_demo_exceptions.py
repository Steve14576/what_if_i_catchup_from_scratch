"""第 18 讲验证脚本：traceback 读法 / try 四段 / except 匹配 / 裸 except / finally 与 return / 异常链 / 自定义异常。

规模纪律：4 个子进程 + 若干内存操作，目标 < 3 秒。
运行：uv run python tutorials/python/scripts/lec18-01_demo_exceptions.py

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


def run_file(path: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    return subprocess.run(
        [sys.executable, str(path)], capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=env, timeout=30,
    )


def indent(text: str, prefix: str = "    ") -> None:
    for line in text.rstrip().splitlines():
        print(prefix + line)


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)

        section("1. 一条 traceback 怎么读：从下往上")
        demo = root / "trace_demo.py"
        demo.write_text(
            "def read_config(path):\n"
            "    return open(path, encoding='utf-8').read()\n"
            "\n"
            "def load():\n"
            "    return read_config('config.ini')\n"
            "\n"
            "load()\n",
            encoding="utf-8",
        )
        r = run_file(demo)
        print(f"  退出码 = {r.returncode}")
        indent(r.stderr)
        print("  预期: 最后一行是“类型 + 消息”，往上每一行是一层调用（哪文件哪行）。")
        print("        最下面那层是真正出错的地方，上面的层说明“谁调用了它”。\n")

        section("2. try / except / else / finally 的执行顺序")
        def demo_order(raise_it: bool):
            marks = []
            try:
                marks.append("try")
                if raise_it:
                    raise ValueError("故意")
            except ValueError:
                marks.append("except")
            else:
                marks.append("else")
            finally:
                marks.append("finally")
            return marks

        print(f"  没出错时: {demo_order(False)}")
        print(f"  出错时  : {demo_order(True)}")
        print("  预期: 正常走 try→else→finally；出错走 try→except→finally。")
        print("        else 只在不抛异常时执行；finally 无论走哪条路都执行。\n")

        section("3. except 的匹配与顺序")
        def classify(exc):
            try:
                raise exc
            except KeyError:
                return "KeyError 分支"
            except LookupError:
                return "LookupError 分支（KeyError 的父类）"
            except Exception:
                return "Exception 分支"

        print(f"  KeyError      -> {classify(KeyError('k'))}")
        print(f"  IndexError    -> {classify(IndexError('i'))}")
        print(f"  ValueError    -> {classify(ValueError('v'))}")
        print("  预期: 从上往下匹配，命中第一个就停；所以子类要写在父类前面，")
        print("        否则父类会把子类全吃掉（KeyError 是 LookupError 的子类）。\n")

        section("4. 裸 except 会吞掉什么")
        bare = root / "bare.py"
        bare.write_text(
            "try:\n"
            "    raise SystemExit(3)\n"
            "except:\n"
            "    print('裸 except 抓到了，程序继续')\n"
            "print('这一行还会执行')\n",
            encoding="utf-8",
        )
        rb = run_file(bare)
        print(f"  裸 except 抓 SystemExit: 退出码={rb.returncode}，输出={rb.stdout.strip()!r}")
        narrow = root / "narrow.py"
        narrow.write_text(
            "try:\n"
            "    raise SystemExit(3)\n"
            "except Exception:\n"
            "    print('except Exception 不会抓它')\n",
            encoding="utf-8",
        )
        rn = run_file(narrow)
        print(f"  except Exception 抓 SystemExit: 退出码={rn.returncode}，输出={rn.stdout.strip()!r}")
        print("  预期: 裸 except 等价于抓 BaseException，会把 SystemExit、KeyboardInterrupt 也吞掉，")
        print("        导致“程序该退出却继续跑”；只写 except Exception 则不会。")
        print("        另一类问题：except 里只写 pass，错误被静默吞掉，出问题时毫无线索。\n")

        section("5. finally 里的 return 会覆盖返回值")
        def tricky():
            try:
                return "try 的返回值"
            finally:
                return "finally 的返回值"

        def tricky2():
            try:
                raise ValueError("原始错误")
            finally:
                return "错误被吞掉了"

        print(f"  正常路径: tricky() = {tricky()!r}")
        print(f"  异常路径: tricky2() = {tricky2()!r}")
        print("  预期: finally 里的 return 会覆盖 try 的返回值，甚至把异常也吞掉。")
        print("        所以 finally 里不要写 return；它该用来“收尾”（关文件、释放资源）。\n")

        section("6. raise 与异常链")
        def parse_age(text):
            try:
                return int(text)
            except ValueError as exc:
                raise ValueError(f"年龄必须是整数，收到 {text!r}") from exc

        try:
            parse_age("abc")
        except ValueError as exc:
            print(f"  捕获到: {exc}")
            print(f"  __cause__ 是原始异常吗 = {exc.__cause__ is not None}")
        print("  预期: raise ... from ... 把原始异常挂在 __cause__ 上，traceback 里会显示")
        print("        “The above exception was the direct cause of...”，两层原因都留得住。\n")

        section("7. 自定义异常：给调用方一个可分类的名字")
        class ConfigError(Exception):
            """配置有问题时抛出。"""

        class MissingKey(ConfigError):
            """配置里缺了必填项。"""

        def read_setting(config, key):
            if key not in config:
                raise MissingKey(f"缺少配置项: {key}")
            return config[key]

        try:
            read_setting({"host": "localhost"}, "port")
        except MissingKey as exc:
            print(f"  MissingKey: {exc}")
        except ConfigError:
            print("  这行不会执行，因为 MissingKey 先被匹配")
        print("  预期: 自定义异常的价值是“调用方可以只捕这一类”；继承体系让分类更细。")
        print("        命名习惯以 Error 结尾，继承 Exception（不要继承 BaseException）。\n")

        section("8. EAFP 与 LBYL：两种风格")
        data = {"a": 1}
        # LBYL: look before you leap
        if "b" in data:
            lbyl = data["b"]
        else:
            lbyl = "默认值"
        # EAFP: easier to ask forgiveness than permission
        try:
            eafp = data["b"]
        except KeyError:
            eafp = "默认值"
        print(f"  LBYL 结果 = {lbyl!r}；EAFP 结果 = {eafp!r}")
        print("  预期: 两种都能跑。字典这种“缺键很常见”的场景，get() 已经是最简形式；")
        print("        EAFP 更适合“检查与使用之间可能被别人改掉”的场合（并发、文件）。")
        print("        本条只要求知道两种名字与取舍，不要求背。\n")

        section("9. 常见内置异常与触发条件")
        cases = [
            ("KeyError", lambda: {"a": 1}["b"]),
            ("IndexError", lambda: [1, 2][5]),
            ("ValueError", lambda: int("abc")),
            ("TypeError", lambda: "a" + 1),
            ("ZeroDivisionError", lambda: 1 / 0),
            ("AttributeError", lambda: "abc".nonexistent()),
            ("FileNotFoundError", lambda: open("no_such.txt", encoding="utf-8")),
        ]
        for name, fn in cases:
            try:
                fn()
            except Exception as exc:
                print(f"  {name:<20}-> 实际类型 {type(exc).__name__}")
        print("  预期: 每一行的实际类型与左边名字一致；记住“哪个操作会抛哪个异常”，")
        print("        写 except 时才不会捕错（捕宽了会掩盖 bug，捕窄了会漏）。")

    print("\n  提示: 判断“该不该用异常”，看这件事是“预期内的分支”还是“不该发生的意外”。")


if __name__ == "__main__":
    main()
