# 文本卫生自检（WIICUFS 1.5.0）：喻体词、表格残留、作业格式、图引用
# 用法：uv run --offline python scripts/check_text_hygiene.py
# 输出纯 ASCII，便于 GBK 控制台
import glob
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(glob.glob(os.path.join(BASE, "*.md")))

BAN = ["账", "武器", "地基", "面孔", "舞台", "魔法", "灵魂", "翻车", "户口", "招牌",
       "主角", "失明", "身份证", "外挂", "打折", "解剖", "性格", "快递", "登机牌", "降维打击"]

reader = [f for f in FILES if os.path.basename(f) != "PLAN.md"]
text = "".join(io.open(f, encoding="utf-8").read() for f in reader)

print("[1] metaphor words in reader files")
for w in BAN:
    n = text.count(w)
    if n:
        print("    %-6s %d  <-- should be 0" % (w, n))
print("    banned total:", sum(text.count(w) for w in BAN))

print("[2] <details> tags")
n_det = sum(io.open(f, encoding="utf-8").read().count("<details>") for f in reader)
print("    count:", n_det)

print("[3] answer blocks per lecture")
for f in FILES:
    name = os.path.basename(f)
    if not re.match(r"^\d\d_", name):
        continue
    c = io.open(f, encoding="utf-8").read()
    n = c.count("参考答案：")
    if name.startswith("22"):
        ok = n >= 3
    else:
        ok = n == 7
    print("    %-30s %d %s" % (name[:28], n, "" if ok else "  <-- check"))

print("[4] figure references")
bad = 0
for f in FILES:
    name = os.path.basename(f)
    c = io.open(f, encoding="utf-8").read()
    for m in re.finditer(r"!\[[^]]*\]\((figures/[^)]+)\)", c):
        if not os.path.exists(os.path.join(BASE, m.group(1).replace("/", "\\"))):
            print("    missing:", m.group(1), "in", name)
            bad += 1
print("    broken refs:", bad, " png files:", len(glob.glob(os.path.join(BASE, "figures", "*.png"))))

print("[5] heading count per lecture (h2 should be >= 8)")
for f in FILES:
    name = os.path.basename(f)
    if not re.match(r"^\d\d_", name):
        continue
    c = io.open(f, encoding="utf-8").read()
    h2 = len(re.findall(r"^## ", c, re.M))
    if h2 < 8:
        print("    %-30s h2=%d" % (name[:28], h2))
print("done")
