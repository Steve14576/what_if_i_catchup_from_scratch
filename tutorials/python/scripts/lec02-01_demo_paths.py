"""第 02 讲验证脚本：当前目录 / 相对路径 / 绝对路径 / PATH 查找 / 空格路径。

规模纪律：建十来个临时文件 + 2 个子进程，目标 < 5 秒。
运行：uv run python tutorials/python/scripts/lec02-01_demo_paths.py

所有临时文件都建在系统临时目录里，脚本结束自动删除，不污染工作区。
讲义里引用的每一条输出都来自本脚本。
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

WIDTH = 68


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def run_child(script: Path, cwd: Path) -> subprocess.CompletedProcess:
    # 显式让子进程用 UTF-8 写标准输出，否则 Windows 上它会按 GBK 写，
    # 父进程再按 UTF-8 解码就会得到替换字符。
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(cwd),
        env=env,
        timeout=30,
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)

        # 造一棵小树：root/data/reports/2026/a.csv
        (root / "data" / "reports" / "2026").mkdir(parents=True)
        target = root / "data" / "reports" / "2026" / "a.csv"
        target.write_text("name,score\nli,90\n", encoding="utf-8")

        section("1. 同一条命令，当前目录不同，结果不同")
        child = root / "show.py"
        child.write_text(
            "from pathlib import Path\n"
            "target = Path('data/reports/2026/a.csv')\n"
            "print('  子进程当前目录 =', Path.cwd())\n"
            "print('  相对路径 target =', target)\n"
            "print('  这个文件存在吗 =', target.exists())\n"
            "try:\n"
            "    with open(target, encoding='utf-8') as f:\n"
            "        print('  第一行 =', f.readline().strip())\n"
            "except FileNotFoundError as exc:\n"
            "    print('  FileNotFoundError:', exc)\n",
            encoding="utf-8",
        )

        print("[情形 A] 在 root 下运行（相对路径从这里算）")
        ra = run_child(child, root)
        print(ra.stdout.rstrip())

        print("[情形 B] 在 root/data 下运行（起点变了，同一句话找不到文件）")
        rb = run_child(child, root / "data")
        print(rb.stdout.rstrip())
        print(f"  退出码: A={ra.returncode}  B={rb.returncode}")

        section("2. 点与点点：同一条路径的不同写法指向哪里")
        base = root / "data" / "reports"
        print(f"  基准目录      = {base}")
        print(f"  base / '.'    = {base / '.'}")
        print(f"  解析后        = {(base / '.').resolve()}")
        print(f"  base / '..'   = {base / '..'}")
        print(f"  解析后        = {(base / '..').resolve()}")
        print(f"  绝对路径      = {target}")
        print(f"  相对 root 的路径 = {target.relative_to(root)}")

        section("3. PATH：命令名的查找目录清单")
        for name in ("python", "py", "pip", "git", "uv", "code"):
            print(f"  which({name!r}) = {shutil.which(name)}")

        entries = [p for p in os.environ.get("PATH", "").split(os.pathsep) if p]
        print(f"  当前 PATH 条目数 = {len(entries)}")
        print(f"  前 3 条 = {entries[:3]}")
        print("  预期: 本脚本是用 uv run 启动的，uv 会把 .venv\\Scripts 临时排到 PATH 最前，")
        print("        所以这里能找到 python，且指向 .venv 里的那个；普通终端里则找不到。")
        print("        git 在；pip 在这个虚拟环境里没有安装，所以是 None。")

        section("4. PATH 是一个可增删的目录列表，顺序决定谁被找到")
        tool_dir = root / "faketools"
        tool_dir.mkdir()
        (tool_dir / "mytool.bat").write_text(
            "@echo off\r\necho hello from mytool\r\n", encoding="ascii"
        )
        print(f"  把 {tool_dir.name} 加进 PATH 之前: which('mytool') = {shutil.which('mytool')}")
        os.environ["PATH"] = str(tool_dir) + os.pathsep + os.environ["PATH"]
        print(f"  加进 PATH 之后:            which('mytool') = {shutil.which('mytool')}")
        print("  预期: 由 None 变成该文件的完整路径 —— 查找不会去猜，只在清单里挨个找。")

        section("5. 路径里有空格：Python 层面没事，shell 层面要加引号")
        space_dir = root / "my project"
        space_dir.mkdir()
        space_script = space_dir / "hello.py"
        space_script.write_text("print('hello from a path with spaces')\n", encoding="utf-8")
        rs = run_child(space_script, root)
        print(f"  用参数列表直接启动: 退出码={rs.returncode} 输出={rs.stdout.strip()!r}")
        print("  预期: 正常。因为这里文件名是一个完整参数；")
        print("        在终端里敲则要写成 python \"my project\\hello.py\"。")

        section("6. Windows 的路径宽容度：大小写与分隔符")
        alt = root / "DATA" / "REPORTS" / "2026" / "A.CSV"
        print(f"  平台 = {sys.platform}")
        print(f"  全大写路径存在吗 = {alt.exists()}")
        print(f"  正斜杠写法的 Path  = {target.as_posix()}")
        print("  预期: Windows 上两项都成立（大小写不敏感、两种分隔符都认）；")
        print("        在 Linux 上大小写敏感，同名不同大小写是两个文件。")


if __name__ == "__main__":
    main()
