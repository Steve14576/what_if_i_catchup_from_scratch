"""第 03 讲验证脚本：venv 的目录结构 / 激活改了什么 / 隔离在哪一层 / uv 的对照。

规模纪律：建两个临时虚拟环境（一个用标准库 venv，一个用 uv venv），目标 < 60 秒。
运行：uv run python tutorials/python/scripts/lec03-01_demo_venv.py

所有环境都建在系统临时目录里，脚本结束自动删除，不碰全局环境。
讲义里引用的每一条输出都来自本脚本。
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

WIDTH = 68


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(cwd) if cwd else None,
        env=env,
        timeout=180,
    )


def tree_names(root: Path, max_depth: int = 2) -> list[str]:
    """列出目录树的前两层，只给名字，用于看清结构。"""
    out: list[str] = []
    for path in sorted(root.rglob("*")):
        depth = len(path.relative_to(root).parts)
        if depth <= max_depth:
            out.append("  " * depth + path.name + ("/" if path.is_dir() else ""))
    return out


PROBE = (
    "import sys\n"
    "print('  sys.executable =', sys.executable)\n"
    "print('  sys.prefix     =', sys.prefix)\n"
    "print('  sys.base_prefix=', sys.base_prefix)\n"
    "print('  是虚拟环境吗   =', sys.prefix != sys.base_prefix)\n"
    "print('  site-packages  =', [p for p in sys.path if 'site-packages' in p])\n"
    "try:\n"
    "    import pip\n"
    "    print('  pip 模块       = 有，版本', pip.__version__)\n"
    "except ModuleNotFoundError:\n"
    "    print('  pip 模块       = 没有')\n"
)


def main() -> None:
    section("1. 当前这个解释器是谁（后面所有对比的基准）")
    print(f"  sys.executable = {sys.executable}")
    print(f"  sys.prefix     = {sys.prefix}")
    print(f"  sys.base_prefix= {sys.base_prefix}")
    print("  预期: 本脚本用 uv run 启动，所以它自己就跑在一个虚拟环境里，")
    print("        两个 prefix 不相等；它上面还压着一层基础安装。")

    with tempfile.TemporaryDirectory() as raw:
        base = Path(raw)

        section("2. 用标准库建一个虚拟环境：python -m venv .venv")
        venv_dir = base / "demo" / ".venv"
        (base / "demo").mkdir()
        t0 = time.perf_counter()
        r = run([sys.executable, "-m", "venv", str(venv_dir)])
        elapsed = time.perf_counter() - t0
        print(f"  退出码 = {r.returncode}   耗时 = {elapsed:.1f} 秒")
        if r.returncode != 0:
            print(r.stderr.strip()[:800])
            return
        print("  预期: 退出码 0。本机两次实测 4.3 / 4.8 秒（固态盘）；")
        print("        机械硬盘或杀软实时扫描时可到几十秒，但这属于一次性成本。")

        section("3. 它在磁盘上留下了什么（前两层）")
        for line in tree_names(venv_dir, max_depth=1):
            print("  " + line)
        scripts = sorted(p.name for p in (venv_dir / "Scripts").iterdir())
        print(f"  Scripts/ 里共 {len(scripts)} 个文件，例如：")
        for name in scripts[:8]:
            print("    " + name)
        print(f"  Lib/site-packages/ 里有 {len(list((venv_dir / 'Lib' / 'site-packages').iterdir()))} 项")
        print("  预期: 有 python.exe、Activate.ps1、activate.bat、pip.exe 等；")
        print("        site-packages 里是空的或只有 pip 相关的东西。")

        section("4. pyvenv.cfg：这个环境的“出生证明”")
        print("  " + "\n  ".join((venv_dir / "pyvenv.cfg").read_text(encoding="utf-8").splitlines()))
        print("  预期: home 指向基础安装目录；include-system-site-packages = false")
        print("        意思是“不借看全局装的包”；version 是解释器版本。")

        section("5. 用这个环境里的解释器跑一段代码")
        probe_file = base / "probe.py"
        probe_file.write_text(PROBE, encoding="utf-8")
        inside = run([str(venv_dir / "Scripts" / "python.exe"), str(probe_file)])
        print(inside.stdout.rstrip())
        print("  预期: sys.prefix 指向 demo\\.venv，sys.base_prefix 指向基础安装，")
        print("        两者不相等，所以“是虚拟环境吗 = True”。")

        section("6. 隔离的实质：site-packages 换成这个环境自己的")
        outside = run([sys.executable, str(probe_file)])
        print("[用基准解释器跑同一段代码]")
        print(outside.stdout.rstrip())
        print("  预期: 两边打印的 site-packages 路径完全不同 —— 这就是“隔离”。")

        section("7. 不激活也能用：激活不是开关，只是改 PATH")
        activate = (venv_dir / "Scripts" / "Activate.ps1").read_text(encoding="utf-8")
        hits = [line.strip() for line in activate.splitlines() if "env:path" in line.lower()]
        print("  Activate.ps1 里与 PATH 有关的行：")
        for line in hits[:5]:
            print("    " + line)
        print("  预期: 它把本环境的 Scripts 目录插到 PATH 最前面。")
        print("        所以激活只做三件事：改 PATH、设 VIRTUAL_ENV、改提示符；")
        print("        它没有“打开”任何东西，直接写绝对路径调用同样有效（第 5 节已证明）。")

        section("8. uv 建的环境长什么样")
        uv = shutil.which("uv")
        if not uv:
            print("  本机没有 uv，跳过本节。")
        else:
            uv_dir = base / "uvdemo" / ".venv"
            t0 = time.perf_counter()
            ru = run([uv, "venv", str(uv_dir)])
            uv_elapsed = time.perf_counter() - t0
            print(f"  uv venv 退出码 = {ru.returncode}   耗时 = {uv_elapsed:.1f} 秒")
            if ru.returncode == 0:
                uv_scripts = sorted(p.name for p in (uv_dir / "Scripts").iterdir())
                print(f"  Scripts/ 里共 {len(uv_scripts)} 个文件：{uv_scripts[:6]}")
                print("  " + "\n  ".join((uv_dir / "pyvenv.cfg").read_text(encoding="utf-8").splitlines()))
                print("  预期: 结构相近，但没有 pip.exe —— uv 不往环境里装 pip。")
                pip_probe = run([str(uv_dir / "Scripts" / "python.exe"), str(probe_file)])
                print(pip_probe.stdout.rstrip())

        section("9. 删掉文件夹就干净了吗")
        print(f"  删除前 demo/.venv 存在吗 = {venv_dir.exists()}")
        shutil.rmtree(venv_dir)
        print(f"  删除后 demo/.venv 存在吗 = {venv_dir.exists()}")
        print("  预期: 环境的一切都在这个目录里，删掉即还原；")
        print("        但“移动或改名”不行 —— 路径写在 pyvenv.cfg 和启动脚本里。")


if __name__ == "__main__":
    main()
