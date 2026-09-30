# 基础设施工具（非讲次验证脚本）：扫描本课程目录所有 md 文件的控制字符损坏。
# 背景：写文件时若 LaTeX 命令的单反斜杠在传输层被解析为 JSON 转义，
#       会发生静默损坏：\b -> 退格(U+0008)、\t -> 制表(U+0009)、\n -> 换行注入(U+000A) 等。
#       08 讲曾实测发生 4 处 \ne -> 换行注入（A4(3) 段），此工具用于例行体检。
# 用法：uv run python scripts/tool_md_health_check.py     （每讲交付前跑一次，应为 0 处）
import glob
import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"扫描目录: {root}")
bad_count = 0
for path in sorted(glob.glob(os.path.join(root, "*.md"))):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")
    name = os.path.basename(path)
    for lineno, line in enumerate(lines, 1):
        # 1) 控制字符（正常换行已由 split 处理；其余均异常）
        for ch in line:
            o = ord(ch)
            if o < 32 or o == 127:
                idx = line.index(ch)
                print(f"[CTRL] {name}:{lineno}: U+{o:04X} 上下文: ...{line[max(0, idx - 20):idx + 20]}...")
                bad_count += 1
        # 2) 行首孤立模式（\ne/\not 损坏的断裂残迹）
        stripped = line.lstrip()
        if stripped.startswith("ot") and ("\\not" not in line):
            print(f"[LINE] {name}:{lineno}: 行首 ot -> {line[:60]}")
            bad_count += 1
        if stripped[:1] == "e" and len(stripped) > 1 and stripped[1] in "0123456789\\$+-|":
            is_code_assign = "=" in stripped and stripped.split("=")[0].strip().replace(" ", "").replace(",", "").isalnum()
            if not is_code_assign:
                print(f"[LINE] {name}:{lineno}: 行首可疑 -> {line[:60]}")
                bad_count += 1
print(f"体检结果: {bad_count} 处可疑 (期望 0)")