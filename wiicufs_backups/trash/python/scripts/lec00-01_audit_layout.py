# 规模纪律：只读 md 做版面统计，目标 < 1 秒。
# 用途：检查各讲排版是否同构（标题层级、加粗小标题、表格、代码块语言）。
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FENCE = chr(96) * 3

for f in sorted(ROOT.glob("0[1-9]_*.md")):
    lines = f.read_text(encoding="utf-8").splitlines()
    h2 = sum(1 for l in lines if l.startswith("## "))
    h3 = sum(1 for l in lines if l.startswith("### "))
    h4 = sum(1 for l in lines if l.startswith("#### "))
    bold_head = sum(1 for l in lines if l.startswith("**") and l.rstrip().endswith("**"))
    tables = sum(1 for l in lines if l.startswith("|---"))
    fences = sum(1 for l in lines if l.startswith(FENCE))
    langs = {}
    for l in lines:
        if l.startswith(FENCE) and len(l) > len(FENCE):
            key = l[len(FENCE):].strip()
            langs[key] = langs.get(key, 0) + 1
    numbered = [l for l in lines if l.startswith("## ")]
    bad_h3 = [l for l in lines if l.startswith("### ") and not re.match(r"^### \d+\.\d+ ", l)]
    unlabeled = []
    in_block = False
    for i, l in enumerate(lines, 1):
        if l.startswith(FENCE):
            if not in_block:
                if len(l.strip()) == len(FENCE):
                    unlabeled.append(i)
                in_block = True
            else:
                in_block = False
    print(f.name)
    print(f"  lines={len(lines)} h2={h2} h3={h3} h4={h4} bold-head={bold_head} tables={tables} fences={fences}")
    print(f"  langs={langs} unlabeled={unlabeled} bad_h3={len(bad_h3)}")
    for l in bad_h3:
        print("    bad:", l)
    for l in numbered:
        print("   ", l)
