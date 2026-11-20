"""第 05 讲验证脚本：审查 AI 给出的改动时，怎么拿到"真假判据"。

三个场景，全部可在本机复现，不依赖任何 AI 产品：
  1. 它说"这条规则已经忽略虚拟环境了" —— 用 git check-ignore 核；
  2. 它说"只改了一行" —— 用 git diff --stat 核；
  3. 它让你跑一条删除命令 —— 先用 dry-run 形式看一眼。

规模纪律：临时仓库 + 十几条命令，目标 < 5 秒。
运行：uv run python tutorials/python/scripts/lec05-01_demo_verify.py
所有操作都在系统临时目录里，提交身份用环境变量临时指定，不碰任何全局配置。
"""

import os
import subprocess
import tempfile
from pathlib import Path

WIDTH = 68
ENV = dict(
    os.environ,
    GIT_AUTHOR_NAME="Tutorial Demo",
    GIT_AUTHOR_EMAIL="demo@example.com",
    GIT_COMMITTER_NAME="Tutorial Demo",
    GIT_COMMITTER_EMAIL="demo@example.com",
    GIT_PAGER="cat",
)


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-c", "color.ui=false", *args],
        cwd=str(repo), capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=ENV, timeout=60,
    )


def show(repo: Path, *args: str) -> None:
    r = git(repo, *args)
    print(f"$ git {' '.join(args)}   (退出码 {r.returncode})")
    body = (r.stdout + r.stderr).rstrip()
    print("  " + body.replace("\n", "\n  ") if body else "  (无输出)")
    print()


def write(repo: Path, name: str, text: str) -> None:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw) / "review-demo"
        repo.mkdir()
        git(repo, "init", "-b", "main")

        section("场景一：它说“已经忽略虚拟环境了”，核对一下")
        write(repo, ".venv/lib/x.py", "print('x')\n")
        write(repo, "venv/bin/y.py", "print('y')\n")
        write(repo, "logs/run.log", "started\n")
        write(repo, "data.csv", "name,score\nli,90\n")

        print("  它给的 .gitignore 内容：")
        print("    venv/")
        print("    *.log")
        write(repo, ".gitignore", "venv/\n*.log\n")
        show(repo, "status", "--short")
        print("  注意：.venv/ 仍然出现在未跟踪列表里。逐条核一下：\n")
        for target in (".venv/lib/x.py", "venv/bin/y.py", "logs/run.log"):
            show(repo, "check-ignore", "-v", target)
        print("  判据：check-ignore 退出码 0 = 被忽略，1 = 没被忽略（且不打印任何东西）。")
        print("  所以“忽略了 venv”这句话对，“忽略了虚拟环境”这句话错 —— 项目的目录叫 .venv。\n")

        print("  改成 .venv/ 之后：")
        write(repo, ".gitignore", ".venv/\nvenv/\n*.log\n")
        show(repo, "status", "--short")
        for target in (".venv/lib/x.py", "logs/run.log"):
            show(repo, "check-ignore", "-v", target)

        section("场景二：它说“只改了一行”，用 diff --stat 核")
        write(repo, "a.py", "def area(r):\n    return 3.14 * r * r\n")
        write(repo, "b.py", "def perimeter(r):\n    return 2 * 3.14 * r\n")
        git(repo, "add", "-A")
        git(repo, "commit", "-m", "初始版本：面积与周长")
        print("  现在按它的说法只动了 a.py 的一行，同时它其实还改了 b.py、加了新文件：\n")
        write(repo, "a.py",
              "def area(r):\n"
              "    s = 3.14159 * r * r\n"
              "    return round(s, 2)\n")
        write(repo, "b.py", "def perimeter(r):\n    return 2 * 3.14159 * r\n")
        write(repo, "util.py", "def show(x):\n    print(x)\n")
        show(repo, "status", "--short")
        show(repo, "diff", "--stat")
        show(repo, "diff")
        print("  判据：stat 里的 'x file changed, n insertions(+), m deletions(-)' 就是改动规模；")
        print("        与“只改了一行”这句话对不上，就要看下面逐行的 diff 到底改了什么。\n")

        section("场景三：它让你跑一条删除命令，先找 dry-run 形式")
        print("  git clean 会删掉未跟踪的文件。它的 -n 参数表示只报告、不动手：\n")
        show(repo, "clean", "-nd")
        print("  上面这条只列出“会被删的未跟踪文件”，这里只有 util.py；")
        print("        已经提交过的 data.csv 不在列表里 —— 未跟踪与已跟踪是两回事。\n")
        show(repo, "clean", "-ndX")
        print("  加 -X 只针对被忽略的文件：.venv/、venv/ 与 logs/ 会被带走，源码不受影响。")
        print("  两个都是 dry-run，仓库此刻没有任何文件被删。\n")

        section("场景四：不接受改动时的回退成本")
        show(repo, "restore", "a.py", "b.py")
        show(repo, "status", "--short")
        print("  判据：一条命令回到上次提交的状态，未跟踪的 util.py 仍在 —— 回退是分得清的。")


if __name__ == "__main__":
    main()
