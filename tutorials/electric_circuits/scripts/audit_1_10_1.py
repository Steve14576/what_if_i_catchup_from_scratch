# 按 WIICUFS 1.10.1 读者合同体检电路学（只读）。
# 额外统计长段落（>260 字）与“点到为止”类措辞，用于定位“散漫/手停”症状。
import re
import glob

OPEN = [
    ("前置", r"\*\*前置\*\*"),
    ("时间", r"\*\*预计时间\*\*"),
    ("定位", r"\*\*一句话定位\*\*"),
    ("回答", r"\*\*本讲回答什么\*\*"),
    ("目标", r"\*\*本讲目标"),
    ("怎么学", r"\*\*怎么学这一讲\*\*"),
    ("验证", r"\*\*这一讲有真实验证\*\*"),
]
SOFT = r"点到为止|不再赘述|这里不展开|不展开讲|略去|留给读者|这里不细讲|不细说|一笔带过|顺便说|题外话"

print("lec lines slots route secs next tail soft longparas")
rows = []
for f in sorted(glob.glob("[0-9][0-9]_*.md")):
    text = open(f, encoding="utf-8").read()
    head = "\n".join(text.split("\n")[:50])
    slots = sum(bool(re.search(p, head)) for _, p in OPEN)
    secs = [l for l in text.split("\n") if l.startswith("## ")]
    body = [
        s for s in secs
        if not re.match(r"^## (本讲怎么走|本讲小结|掌握度自测|作业|小结)", s)
    ]
    nxt = text.count("下一站")
    tail = sum(x in text for x in ["## 本讲小结", "## 掌握度自测", "## 作业"])
    soft = len(re.findall(SOFT, text))
    paras = [
        len(p) for p in re.split(r"\n\s*\n", text)
        if p.strip() and not p.strip().startswith(("#", "|", ">", "!", "$$"))
    ]
    longp = sum(1 for p in paras if p > 260)
    rows.append((f[:2], text.count("\n") + 1, slots,
                 "Y" if "## 本讲怎么走" in text else "N",
                 len(body), nxt, tail, soft, longp))

for r in rows:
    print("%s %4d %d/7 %s %2d %2d %d/3 %3d %3d" % r)
print("summary: full_open=%d/%d route=%d tail=%d soft_total=%d longparas_total=%d"
      % (sum(1 for r in rows if r[2] == 7), len(rows),
         sum(1 for r in rows if r[3] == "Y"),
         sum(1 for r in rows if r[6] == 3),
         sum(r[7] for r in rows), sum(r[8] for r in rows)))
