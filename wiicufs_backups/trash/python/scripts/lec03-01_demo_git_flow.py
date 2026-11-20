# 规模纪律：本地 git 操作，不联网，目标 < 15 秒。
# 用途：为第 03 讲提供真实输出——提交、回退、ignore、远程、冲突。
import os
import shutil
import stat
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / ".tmp_git_demo"


def clean(path):
    """Windows 上 git 对象文件是只读的，直接 rmtree 会 PermissionError。"""
    if not path.exists():
        return

    def on_exc(func, p, exc):
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except Exception:
            pass

    shutil.rmtree(path, onexc=on_exc)


clean(BASE)
BASE.mkdir(parents=True)

ENV = os.environ.copy()
ENV.update({
    "GIT_AUTHOR_NAME": "demo",
    "GIT_AUTHOR_EMAIL": "demo@example.com",
    "GIT_COMMITTER_NAME": "demo",
    "GIT_COMMITTER_EMAIL": "demo@example.com",
    "GIT_CONFIG_NOSYSTEM": "1",
})


def git(*args, cwd=BASE, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, env=ENV, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        print("FAILED:", " ".join(args))
        print(r.stdout)
        print(r.stderr)
        clean(BASE)
        raise SystemExit(1)
    return r


def write(name, text, cwd=BASE):
    (Path(cwd) / name).write_text(text, encoding="utf-8", newline="\n")


print("=== EXP1: 从空目录到第一次提交 ===")
repo = BASE / "proj"
repo.mkdir()
print(git("init", cwd=repo).stdout.strip().splitlines()[0])
write("hello.py", 'print("hello")\n', cwd=repo)
status = git("status", "--short", cwd=repo).stdout.strip()
print("status before add:", repr(status))
git("add", "hello.py", cwd=repo)
print("status after add :", repr(git("status", "--short", cwd=repo).stdout.strip()))
git("commit", "-m", "first: print hello", cwd=repo)
print("log:", git("log", "--oneline", cwd=repo).stdout.strip())

print()
print("=== EXP2: 一次提交只装一件事（分两次 add/commit）===")
write("hello.py", 'print("hello")\nprint("bye")\n', cwd=repo)
git("add", "hello.py", cwd=repo)
git("commit", "-m", "add bye line", cwd=repo)
write("grade.py", 'score = 85\nprint("A" if score >= 85 else "B")\n', cwd=repo)
git("add", "grade.py", cwd=repo)
git("commit", "-m", "add grade script", cwd=repo)
print(git("log", "--oneline", cwd=repo).stdout.strip())

print()
print("=== EXP3: 改坏了还没提交：restore 退回 ===")
write("hello.py", 'print("broken"\n', cwd=repo)
print("diff before restore:")
print(git("diff", "--", "hello.py", cwd=repo).stdout.strip())
git("restore", "hello.py", cwd=repo)
print("after restore:", repr((repo / "hello.py").read_text(encoding="utf-8")))

print()
print("=== EXP4: 已经提交了才发现错：revert 加一次反向提交 ===")
write("hello.py", 'print("A")\nprint("bye")\n', cwd=repo)
git("add", "hello.py", cwd=repo)
git("commit", "-m", "change hello to A", cwd=repo)
print("before revert:", repr((repo / "hello.py").read_text(encoding="utf-8")))
git("revert", "--no-edit", "HEAD", cwd=repo)
print("after revert :", repr((repo / "hello.py").read_text(encoding="utf-8")))
print("log head:", git("log", "--oneline", "-2", cwd=repo).stdout.strip())

print()
print("=== EXP5: .gitignore 让不该进仓库的东西变灰 ===")
write(".gitignore", ".venv/\n__pycache__/\n*.log\n", cwd=repo)
(repo / ".venv").mkdir()
write("x.log", "noise\n", cwd=repo)
write("keep.py", "print(1)\n", cwd=repo)
print("untracked (with ignore):", repr(git("status", "--short", cwd=repo).stdout.strip()))
git("add", ".gitignore", "keep.py", cwd=repo)
git("commit", "-m", "add ignore rules", cwd=repo)

print()
print("=== EXP6: 本地 bare 仓库模拟远程：push / pull ===")
remote = BASE / "remote.git"
git("init", "--bare", str(remote), cwd=BASE)
git("remote", "add", "origin", str(remote), cwd=repo)
git("push", "-u", "origin", "master", cwd=repo)
print("push ok; remote branches:",
      git("branch", "-r", cwd=repo).stdout.strip())
clone = BASE / "clone"
git("clone", str(remote), str(clone), cwd=BASE)
print("clone files:", sorted(p.name for p in clone.iterdir() if p.is_file()))

print()
print("=== EXP7: 两个人改同一行：push 被拒 + 冲突标记 ===")
write("hello.py", 'print("from repo")\nprint("bye")\n', cwd=repo)
git("add", "hello.py", cwd=repo)
git("commit", "-m", "repo change", cwd=repo)
git("push", cwd=repo)
print("repo pushed its change first")

write("hello.py", 'print("from clone")\nprint("bye")\n', cwd=clone)
git("add", "hello.py", cwd=clone)
git("commit", "-m", "clone change", cwd=clone)
push_clone = git("push", cwd=clone, check=False)
print("clone push rejected:", push_clone.returncode != 0)
for line in push_clone.stderr.splitlines():
    if "rejected" in line or "fetch first" in line:
        print("  ", line.strip())

pull = git("pull", "--no-rebase", cwd=clone, check=False)
print("pull exit code:", pull.returncode)
print("status during conflict:", repr(git("status", "--short", cwd=clone).stdout.strip()))
conflict_text = (clone / "hello.py").read_text(encoding="utf-8")
for line in conflict_text.splitlines():
    if line.startswith(("<<<<<<<", "=======", ">>>>>>>")) or "from " in line:
        print("  ", line)
print("conflict markers present:", "<<<<<<<" in conflict_text)

print()
print("=== EXP8: 解决冲突后再提交 ===")
write("hello.py", 'print("merged")\nprint("bye")\n', cwd=clone)
git("add", "hello.py", cwd=clone)
git("commit", "-m", "resolve conflict", cwd=clone)
git("push", cwd=clone)
print("final log:", git("log", "--oneline", cwd=clone).stdout.strip().splitlines()[:3])

clean(BASE)
print()
print("[OK] git flow demo finished")
