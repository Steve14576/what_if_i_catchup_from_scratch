# 按 WIICUFS 1.10.1 读者合同做结构体检（只读，不改文件）。
# 输出 ASCII-safe，避免 GBK 控制台报错。
import re
from pathlib import Path

ROOT = Path(r"e:\E_Vault\CC_Formed_Projs2\WHATIFICATCHUPFROMSCRATCH\tutorials\advanced_math_II")
LEC = sorted([p for p in ROOT.glob("*.md") if re.match(r"^\d{2}_", p.name)])

OPEN_SLOTS = [
    ("前置", r"\*\*前置\*\*"),
    ("时间", r"\*\*预计时间\*\*"),
    ("定位", r"\*\*一句话定位\*\*"),
    ("回答", r"\*\*本讲回答什么\*\*"),
    ("目标", r"\*\*本讲目标"),
    ("怎么学", r"\*\*怎么学这一讲\*\*"),
    ("验证", r"\*\*这一讲有真实验证\*\*"),
]
ASSERT = r"可以验证|显然|同理|即得|不难|略去|类似地|只需|留给读者|容易看出|众所周知"

rows = []
for p in LEC:
    text = p.read_text(encoding="utf-8")
    head = "\n".join(text.split("\n")[:45])
    slots = {name: bool(re.search(pat, head)) for name, pat in OPEN_SLOTS}
    has_route = "## 本讲怎么走" in text
    secs = [ln for ln in text.split("\n") if ln.startswith("## ")]
    body_secs = [s for s in secs if not re.match(r"^## (本讲怎么走|本讲小结|掌握度自测|作业)", s)]
    next_stop = text.count("下一站")
    tail = {"小结": "## 本讲小结" in text, "自测": "## 掌握度自测" in text, "作业": "## 作业" in text}
    asserts = len(re.findall(ASSERT, text))
    rows.append(
        dict(
            name=p.name[:2],
            lines=text.count("\n") + 1,
            slots=sum(slots.values()),
            miss="".join(k for k, v in slots.items() if not v),
            route=has_route,
            secs=len(body_secs),
            next=next_stop,
            tail=sum(tail.values()),
            tail_miss="".join(k for k, v in tail.items() if not v),
            asserts=asserts,
        )
    )

print("lec lines open_slots missing_slots route body_secs next_stop tail missing_tail asserts")
for r in rows:
    print(
        f"{r['name']} {r['lines']:4d} {r['slots']}/7 {r['miss'] or '-':22s} "
        f"{'Y' if r['route'] else 'N'} {r['secs']:2d} {r['next']:2d} "
        f"{r['tail']}/3 {r['tail_miss'] or '-':8s} {r['asserts']:2d}"
    )

print()
print("summary:",
      "open_block_full =", sum(1 for r in rows if r["slots"] == 7),
      "/", len(rows),
      "| route =", sum(1 for r in rows if r["route"]),
      "| tail_full =", sum(1 for r in rows if r["tail"] == 3),
      "| next_stop_missing =", sum(1 for r in rows if r["next"] == 0))
