"""第 07 讲验证脚本：本机编辑器事实 / 扩展 / 解释器选择 / 调试器 / 命令行代理。

规模纪律：两次 `code --version` + 两次列表命令 + 一次 pdb 会话，目标 < 30 秒。
运行：uv run python tutorials/python/scripts/lec07-01_demo_editor.py

说明：
  1. 脚本只做只读检查（查版本、列扩展、读目录），不安装、不改配置；
  2. 路径按"常见位置 + PATH"探测，你的机器上可能只命中一部分，属正常；
  3. pdb 会话用管道输入命令模拟"暂停—查看—单步—继续"，不需要图形界面。
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

WIDTH = 68
HOME = Path.home()


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def run(cmd: list[str], stdin: str | None = None, timeout: int = 60) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    return subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
        input=stdin, env=env, timeout=timeout,
    )


def find_editors() -> list[tuple[str, Path]]:
    """按 PATH、常见安装位置与命令行参数找 code 命令。"""
    found: list[tuple[str, Path]] = []
    on_path = shutil.which("code")
    if on_path:
        found.append(("PATH 里的 code", Path(on_path)))

    candidates = [
        ("VS Code（用户安装）", Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Microsoft VS Code/bin/code.cmd"),
        ("VS Code（系统安装）", Path("C:/Program Files/Microsoft VS Code/bin/code.cmd")),
        ("Qoder（系统安装）", Path("C:/Program Files/Qoder IDE/bin/code.cmd")),
    ]
    candidates += [("参数指定", Path(arg)) for arg in sys.argv[1:]]
    for label, path in candidates:
        if path.exists() and all(path != p for _, p in found):
            found.append((label, path))
    return found


def main() -> None:
    section("1. 本机装了哪些编辑器：同名命令谁先被找到")
    editors = find_editors()
    for label, path in editors:
        print(f"  {label}: {path}")
    print("  预期: PATH 是“清单 + 顺序”，同名命令只跑第一个命中；")
    print("        装了多个编辑器时，`code` 指向谁取决于 PATH 顺序（第 02 讲）。\n")

    section("2. 版本：一个命令就能验证装没装好")
    for label, path in editors:
        r = run([str(path), "--version"], timeout=90)
        first = (r.stdout or r.stderr).splitlines()
        version = first[0] if first else "(无输出)"
        print(f"  {label}: 退出码={r.returncode} 版本={version}")
    print("  预期: 退出码 0 且打印出版本号，说明命令行入口是通的；")
    print("        这比“双击图标能打开”更有意义——终端与编辑器打通了。\n")

    section("3. 扩展：编辑器的能力是装出来的")
    for label, path in editors:
        r = run([str(path), "--list-extensions"], timeout=120)
        names = [line.strip() for line in r.stdout.splitlines() if line.strip()]
        print(f"  {label}: {len(names)} 个扩展")
        keys = [n for n in names if any(k in n.lower() for k in ("python", "pylance", "claude", "copilot", "cline"))]
        for name in keys:
            print(f"    - {name}")
    for label, folder in (("VS Code", HOME / ".vscode" / "extensions"),
                          ("Qoder", HOME / ".qoder" / "extensions")):
        if folder.is_dir():
            count = len([p for p in folder.iterdir() if p.is_dir()])
            print(f"  {label} 扩展目录: {folder}（{count} 个目录）")
    print("  预期: Python 相关扩展里最关键的是 ms-python.python；")
    print("        它负责“让编辑器认识 Python”，并把调试、环境选择串起来。\n")

    section("4. 选解释器：选的其实是一条路径")
    print(f"  当前脚本的解释器（venv）: {sys.executable}")
    base_root = Path(sys.base_prefix)
    base = next((p for p in (base_root / "python.exe", base_root / "Scripts" / "python.exe") if p.exists()), None)
    if base:
        r = run([str(base), "-c", "import sys; print(sys.executable)"])
        print(f"  基础解释器（母本）   : {r.stdout.strip()}")
    else:
        print(f"  基础解释器（母本）   : 未在 {base_root} 下找到 python.exe")
    print("  预期: 两个路径不同，但版本可能相同。编辑器里的 Select Interpreter 选的就是")
    print("        其中一条路径；选错时表现为“明明装了库却 ModuleNotFoundError”（第 03 讲）。\n")

    section("5. 调试器：暂停、查看、单步（用 pdb 演示，不需要图形界面）")
    with tempfile.TemporaryDirectory() as raw:
        script = Path(raw) / "debug_demo.py"
        script.write_text(
            "def total(xs):\n"
            "    s = 0\n"
            "    for x in xs:\n"
            "        breakpoint()\n"
            "        s += x\n"
            "    return s\n"
            "\n"
            "numbers = [3, 5]\n"
            "print('result =', total(numbers))\n",
            encoding="utf-8",
        )
        # pdb 命令：看 x、看 s、单步、再看 s、继续；循环两轮所以 continue 两次
        commands = "p x\np s\nn\np s\nc\nc\n"
        r = run([sys.executable, str(script)], stdin=commands, timeout=30)
        out = (r.stdout + r.stderr).splitlines()
        keep = [line for line in out if line.strip() and not line.startswith("Traceback")]
        for line in keep[:14]:
            print("  " + line)
        print("  预期: 出现 (Pdb) 提示与三次数值：x=3、s=0、s=3；")
        print("        这就是调试器的三件事：停住（breakpoint）、看变量（p）、单步（n）。")
        print("        图形界面里对应：行号左侧点红点、F5 启动、变量面板、F10 单步。\n")

    section("6. 命令行代理：一个能读写文件的可执行程序")
    claude_home = HOME / ".claude"
    print(f"  ~/.claude 存在吗 = {claude_home.is_dir()}")
    print(f"  PATH 里有 claude 命令吗 = {shutil.which('claude')}")
    exe_hits: list[Path] = []
    for root in (HOME / ".vscode" / "extensions", HOME / ".qoder" / "extensions"):
        if root.is_dir():
            exe_hits.extend(list(root.glob("**/resources/**/claude*.exe"))[:2])
    for path in exe_hits[:3]:
        print(f"  找到的可执行文件: {path}")
    print("  预期: 扩展把 CLI 放在自己的资源目录里，`不`自动进 PATH；")
    print("        想用命令行版，要么用它自带的命令，要么把路径加进 PATH（第 02 讲）。")
    print("        它能读你的项目、能执行命令 —— 权限就是你给它的权限（第 08 讲）。")


if __name__ == "__main__":
    main()
