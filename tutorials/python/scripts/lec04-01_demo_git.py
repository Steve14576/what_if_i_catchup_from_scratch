"""第 04 讲验证脚本：git 的快照 / 三区 / 提交取哪一份 / 回退 / 分支 / 冲突 / .gitignore。

规模纪律：在系统临时目录建一个仓库，跑二十来条 git 命令，目标 < 10 秒。
运行：uv run python tutorials/python/scripts/lec04-01_demo_git.py

纪律说明：
  1. 所有命令都在临时目录里执行，绝不碰教程仓库本身；
  2. 提交身份用环境变量临时指定，不写、不改任何全局 git 配置。
讲义里引用的每一条输出都来自本脚本。
"""

import os
import subprocess
import sys
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
        cwd=str(repo),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=ENV,
        timeout=60,
    )


def show(repo: Path, *args: str) -> None:
    r = git(repo, *args)
    print(f"$ git {' '.join(args)}   (退出码 {r.returncode})")
    body = (r.stdout + r.stderr).rstrip()
    print("  " + body.replace("\n", "\n  ") if body else "  (无输出)")
    print()


def write(name: str, text: str, repo: Path) -> None:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_py(repo: Path, name: str) -> None:
    r = subprocess.run(
        [sys.executable, name], cwd=str(repo), capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=30,
    )
    tail = [line for line in (r.stderr or r.stdout).splitlines() if line.strip()]
    print(f"  运行 {name}: 退出码={r.returncode}  最后一行={tail[-1] if tail else '(无输出)'}")
    print()


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw) / "demo-repo"
        repo.mkdir()

        section("1. 建仓库：git init")
        show(repo, "init", "-b", "main")
        print(f"  出现 .git 目录吗 = {(repo / '.git').is_dir()}")
        print("  预期: .git 是仓库本体，历史全在里面；删掉它，这个目录就退回普通文件夹。\n")

        section("2. 第一个版本 + 三区状态码")
        write("hello.py", 'print("hello, git")\nprint("version 1")\n', repo)
        show(repo, "status", "--short")
        print("  预期: '?? hello.py' —— 第一个问号是暂存区状态，第二个是工作区状态。\n")

        show(repo, "add", "hello.py")
        show(repo, "status", "--short")
        print("  预期: 'A  hello.py' —— 已暂存，还没提交。\n")

        section("3. 关键实验：add 之后又改，提交进去的是哪一份？")
        write("hello.py", 'print("hello, git")\nprint("version 1")\nprint("version 2")\n', repo)
        print("  现在文件已是 v2，但暂存区里是 v1。直接提交：")
        show(repo, "commit", "-m", "加入问候与版本号")
        show(repo, "show", "HEAD:hello.py")
        print("  预期: 打印的是 v1（没有 version 2）—— 提交只取暂存区那一份。")
        print("        git show HEAD:文件 能取出整份文件，这本身就是'快照'的证据。\n")

        show(repo, "status", "--short")
        print("  预期: ' M hello.py' —— v2 还在工作区，未暂存。\n")

        section("4. 三种 diff 各看哪一段")
        show(repo, "diff")
        print("  预期: 工作区相对暂存区，能看到 + print(\"version 2\")。\n")
        show(repo, "diff", "--staged")
        print("  预期: 空 —— 暂存区与 HEAD 一致（v1 已提交）。\n")

        show(repo, "add", "hello.py")
        show(repo, "diff")
        print("  预期: 空 —— 暂存后，工作区与暂存区一致。\n")
        show(repo, "diff", "--staged")
        print("  预期: 出现 version 2 的新增行。\n")

        show(repo, "commit", "-m", "补上版本号第二行")
        show(repo, "log", "--oneline")
        print("  预期: 两条提交，各有短哈希与消息。\n")

        section("5. 改坏了：先看 diff，再 restore")
        write("hello.py", 'print("hello, git"\nprint("version 1"\n', repo)
        git(repo, "add", "hello.py")
        show(repo, "diff", "--staged")
        print("  这是一份删掉右括号、还丢了引号的坏文件。先把它取消暂存：")
        show(repo, "restore", "--staged", "hello.py")
        show(repo, "status", "--short")
        print("  预期: 变回 ' M hello.py'，暂存区干净了，但工作区还是坏的。\n")
        run_py(repo, "hello.py")
        print("  现在用 restore 把工作区恢复到上一次提交：")
        show(repo, "restore", "hello.py")
        run_py(repo, "hello.py")
        print("  预期: restore 之后运行退出码回到 0 —— 坏改动被丢弃。\n")

        section("6. 分支：它只是指向某个提交的名字")
        show(repo, "switch", "-c", "feature")
        write("hello.py", 'print("hello, git")\nprint("version 1")\nprint("version 2")\nprint("只在分支上加的一行")\n', repo)
        git(repo, "add", "hello.py")
        git(repo, "commit", "-m", "分支上增加一行说明")
        print("  切回 main 看文件内容：")
        show(repo, "switch", "main")
        print("  hello.py 现在的内容：")
        print("  " + (repo / "hello.py").read_text(encoding="utf-8").replace("\n", "\n  ").rstrip())
        print("  预期: 那行'只在分支上加的'消失了 —— 分支不是复制文件，而是换了 HEAD 指向。\n")

        show(repo, "merge", "feature")
        show(repo, "log", "--oneline", "--graph", "--all", "--decorate")
        print("  预期: 因为 main 没有新提交，合并是快进（fast-forward）。\n")

        section("7. 冲突长什么样")
        show(repo, "switch", "-c", "side")
        write("hello.py", 'print("side 改的第一行")\nprint("version 1")\nprint("version 2")\nprint("只在分支上加的一行")\n', repo)
        git(repo, "add", "hello.py")
        git(repo, "commit", "-m", "side 分支改第一行")
        git(repo, "switch", "main")
        write("hello.py", 'print("main 改的第一行")\nprint("version 1")\nprint("version 2")\nprint("只在分支上加的一行")\n', repo)
        git(repo, "add", "hello.py")
        git(repo, "commit", "-m", "main 分支改第一行")
        show(repo, "merge", "side")
        show(repo, "status", "--short")
        print("  冲突标记长这样（文件实际内容）：")
        print("  " + (repo / "hello.py").read_text(encoding="utf-8").rstrip().replace("\n", "\n  "))
        print()
        print("  <<<<<<< 与 ======= 之间是当前分支的内容，======= 与 >>>>>>> 之间是对方分支的。")
        print("  解决方式是手工改成想要的样子，再 add + commit：")
        write("hello.py", 'print("合并后的第一行")\nprint("version 1")\nprint("version 2")\nprint("只在分支上加的一行")\n', repo)
        git(repo, "add", "hello.py")
        show(repo, "commit", "-m", "解决冲突：合并两边的第一行")

        section("8. .gitignore：哪些东西不该进仓库")
        write(".gitignore", ".venv/\n__pycache__/\n*.log\n", repo)
        write(".venv/dummy.txt", "x\n", repo)
        write("__pycache__/mod.cpython-312.pyc", "x\n", repo)
        write("debug.log", "x\n", repo)
        write("data.csv", "name,score\nli,90\n", repo)
        show(repo, "status", "--short")
        print("  预期: 只看到 .gitignore 与 data.csv；.venv、__pycache__、debug.log 不见。\n")
        show(repo, "check-ignore", "-v", "debug.log")
        print("  预期: 指出是哪一条规则忽略了它。\n")

        section("9. 一个提交里到底有什么")
        git(repo, "add", ".gitignore")
        git(repo, "commit", "-m", "加入 .gitignore，忽略环境与缓存")
        show(repo, "show", "--stat", "--oneline", "HEAD")
        show(repo, "log", "--oneline")


if __name__ == "__main__":
    main()
