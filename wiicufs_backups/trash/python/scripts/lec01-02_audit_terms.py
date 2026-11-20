# 规模纪律：只读一个 md 文件做术语首现扫描，目标 < 1 秒。
# 用法：python lec01-02_audit_terms.py [md 路径]；不带参数则扫第 01 讲。
from pathlib import Path
import sys

TERMS = [
    "扩展名", "Python", "终端", "shell", "cd ", "目录", "当前目录", "命令", "参数",
    "print", "编码", "UTF-8", "python.exe", ".exe", "进程", "字节码", "标准输出",
    "码页", "磁盘", "内存", "CPU", "环境变量", "PATH", "cwd", "相对路径",
    "绝对路径", "重定向", "import", "模块", "缓存", "对象", "id(", "码点",
    "chcp", "pip", "包", "Path(", "解释器", "cmdlet", "管道", "盘符", "整数",
    "py 启动器", "site-packages", "虚拟环境", "venv", "wheel", "包索引", "标准库",
    "sys", "sysconfig", "-m ", "-c ", "open(", "PYTHONIOENCODING", "utf-8-sig",
    "os", "IDE", "执行策略", "镜像", "锁文件", "ModuleNotFoundError", "FileNotFoundError",
    "仓库", "提交", "快照", "工作区", "暂存区", "HEAD", "分支", "远程", "clone",
    "push", "pull", "diff", ".gitignore", "LLM", "token", "上下文窗口", "agent", "幻觉",
    "密钥", "反向提交",
    "winget", "PortableGit", "git-bash", "Vim", "Nano", "root-commit", "working tree",
    "--cached", "stash", "push -f", "--no-edit", "--no-rebase", "@@",
    "脚本", "注释", "字符串", "变量", "赋值", "表达式", "对象", "运算符", "浮点",
    "精度", "docstring", "函数", "返回值", "参数", "方法", "关键字", "snake_case",
    "ValueError", "TypeError", "Decimal", "isclose", "isinstance", "append", "class",
    "不可变", "可变", "子类",
]

if len(sys.argv) > 1:
    md = Path(sys.argv[1])
else:
    md = Path(__file__).resolve().parent.parent / "01_程序是怎么在计算机里跑起来的.md"
lines = md.read_text(encoding="utf-8").splitlines()
print(f"file: {md.name}, lines: {len(lines)}")
for term in TERMS:
    for i, line in enumerate(lines, 1):
        if term in line:
            print(f"[{term}] L{i}: {line.strip()[:100]}")
            break
    else:
        print(f"[{term}] NOT FOUND")
