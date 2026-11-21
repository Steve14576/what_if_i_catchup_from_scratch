"""第 00 讲配套：讲义排版审计（作者侧，交付前必跑）。

检查项（与 PLAN 的排版契约对应）：
  1. 四级及更深标题（####）数量，应为 0
  2. `###` 是否都带 X.Y 编号
  3. 代码块是否都标了语言
  4. 表格数量（按连续以 | 开头的行分组计数）
  5. `<details>` 残留
  6. 弯引号（U+201C/201D/2018/2019）残留
  7. LaTeX 行内/块级定界符 \\( \\) \\[ \\] 残留
  8. 独占一行的加粗文本（伪标题）
  9. 读者合同槽位：开头块八项、脉络图、本讲小结、掌握度自测
 10. 每个编号正文节（## N.）末尾是否有一句“下一节/下一讲”导向

运行：uv run python tutorials/python/scripts/lec00-01_audit_layout.py [目录或文件...]
默认审计 tutorials/python 目录下的 NN_*.md 与 AA_*.md。
"""

import re
import sys
from pathlib import Path

SMART_QUOTES = {"\u201c": "U+201C", "\u201d": "U+201D", "\u2018": "U+2018", "\u2019": "U+2019"}
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
H3_NUMBERED = re.compile(r"^#{3}\s+\d+\.\d+\s")
BOLD_ONLY = re.compile(r"^\*\*[^*]+\*\*\s*$")
CONTENT_H2 = re.compile(r"^##\s+\d+\.\s")
OPENING_SLOTS = [
    "前置", "预计时间", "一句话定位", "本讲回答什么",
    "本讲目标", "目标达成", "怎么学这一讲", "这一讲有真实验证",
]
FIXED_SECTIONS = ["## 本讲怎么走（脉络图）", "## 本讲小结", "## 掌握度自测（行为化）", "## 作业"]


def audit(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    problems: list[str] = []

    h4 = 0
    bad_h3: list[int] = []
    unlabeled: list[int] = []
    tables = 0
    in_table = False
    in_fence = False

    for number, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            if not in_fence:
                lang = line.strip()[3:].strip()
                if not lang:
                    unlabeled.append(number)
                in_fence = True
            else:
                in_fence = False
            continue
        if in_fence:
            continue

        match = HEADING.match(line)
        if match:
            level = len(match.group(1))
            if level >= 4:
                h4 += 1
            if level == 3 and not H3_NUMBERED.match(line):
                bad_h3.append(number)

        if line.startswith("|"):
            if not in_table:
                tables += 1
                in_table = True
        else:
            in_table = False

    details = text.count("<details>")
    smart = [f"{SMART_QUOTES[ch]}@{lines.index(next(l for l in lines if ch in l)) + 1}"
             for ch in SMART_QUOTES if ch in text]
    latex_brackets = len(re.findall(r"\\[\(\)\[\]]", text))
    bold_only = [n for n, line in enumerate(lines, start=1) if BOLD_ONLY.match(line)]

    if h4:
        problems.append(f"四级标题 {h4} 处（应为 0）")
    if bad_h3:
        problems.append(f"未带 X.Y 编号的 ###：行 {bad_h3}")
    if unlabeled:
        problems.append(f"未标语言的代码块：行 {unlabeled}")
    if tables > 6:
        problems.append(f"表格 {tables} 个（契约上限 6）")
    if details:
        problems.append(f"<details> 残留 {details} 处")
    if smart:
        problems.append(f"弯引号残留：{', '.join(smart)}")
    if latex_brackets:
        problems.append(f"LaTeX 括号定界符 {latex_brackets} 处")
    if bold_only:
        problems.append(f"独占一行的加粗：行 {bold_only}")

    # 读者合同：开头块八项 + 脉络图 + 结尾三块（00 导览与 AA 附录不适用）
    if not (path.name.startswith("00_") or path.name.startswith("AA_")):
        head = "\n".join(lines[:60])
        missing = [slot for slot in OPENING_SLOTS if slot not in head]
        if missing:
            problems.append(f"开头块缺：{missing}")
        for section in FIXED_SECTIONS:
            if section not in text:
                problems.append(f"缺固定块：{section}")

        # 每个编号正文节末尾应有一句导向（下一节/下一讲）
        boundaries = [i for i, line in enumerate(lines) if CONTENT_H2.match(line)]
        for idx, start in enumerate(boundaries):
            end = boundaries[idx + 1] if idx + 1 < len(boundaries) else len(lines)
            body = "\n".join(lines[start:end])
            if "下一节" not in body and "下一讲" not in body:
                problems.append(f"节末缺导向：第 {start + 1} 行 {lines[start].strip()}")

    status = "OK" if not problems else "待修"
    print(f"[{status}] {path.name}  行数={len(lines)}  表格={tables}  h4={h4}  "
          f"bad_h3={len(bad_h3)}  unlabeled={len(unlabeled)}")
    for problem in problems:
        print(f"    - {problem}")
    return problems


def collect(args: list[str]) -> list[Path]:
    if args:
        targets = [Path(arg) for arg in args]
    else:
        targets = [Path(__file__).resolve().parents[1]]
    files: list[Path] = []
    for target in targets:
        if target.is_dir():
            files.extend(sorted(p for p in target.glob("*.md")
                                if p.name[:2].isdigit() or p.name.startswith("AA_")))
        elif target.suffix == ".md":
            files.append(target)
    return files


def main() -> int:
    files = collect(sys.argv[1:])
    if not files:
        print("没有找到要审计的 .md 文件")
        return 1
    failures = 0
    for path in files:
        failures += len(audit(path))
    print(f"\n合计问题 {failures} 项" if failures else "\n全部通过")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
