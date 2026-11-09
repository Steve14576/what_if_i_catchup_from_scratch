# 全课程第 2 遍回查的机器可查项（结构契约/链条锚点/AA 覆盖/讲次一致性/跨讲引用）。
# 用法: uv run python scripts/tool_course_audit.py
# 输出问题清单；退出码 1 表示有问题待修。
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CN = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}
problems = []


def note(kind, msg):
    problems.append(f"[{kind}] {msg}")


# ---------- A. 讲次文件 ----------
files = sorted(p.name for p in ROOT.glob("[0-9][0-9]_*.md") if not p.name.startswith("00_"))
nums = {int(n[:2]) for n in files}
for n in range(1, 32):
    if n not in nums:
        note("文件", f"缺少第 {n:02d} 讲正文")
print(f"A. 正文文件数 = {len(files)}（期望 31）")

texts = {int(p.name[:2]): p.read_text(encoding="utf-8")
         for p in ROOT.glob("[0-9][0-9]_*.md") if not p.name.startswith("00_")}

# ---------- B. 每讲结构块 ----------
need = ["本讲目标", "## 本讲怎么走", "## 本讲小结", "## 掌握度自测", "## 作业"]
for n, t in sorted(texts.items()):
    for blk in need:
        if blk not in t:
            note("结构", f"第 {n:02d} 讲缺结构块: {blk}")
    if "> **前置**" not in t:
        note("结构", f"第 {n:02d} 讲前置说明不是引用块")
print("B. 结构块检查完毕")

# ---------- C. PLAN 链条锚点 ----------
plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
anchors = re.findall(r"\[→(\d\d) §([^\]]+)\]", plan)
bad = 0
for nn, sec in anchors:
    n = int(nn)
    if n not in texts:
        note("锚点", f"PLAN 锚点指向不存在的第 {nn} 讲")
        bad += 1
        continue
    for part in sec.split("/"):
        part = part.strip().lstrip("§").strip()
        m_num = re.match(r"^(\d+\.\d+)", part)
        m_int = re.match(r"^(\d+)(?!\.)", part)
        m_cn = re.match(r"^([一二三四五六七八九十]+)(?!\.)", part)
        if m_num:
            pat = f"### {m_num.group(1)}"
        elif m_int:
            pat = f"## {CN.get(int(m_int.group(1)), '?')}、"
        elif m_cn:
            pat = f"## {m_cn.group(1)}、"
        else:
            # 自由描述（如"§三 罪二"）由人工抽检，不在此处误报
            continue
        if pat not in texts[n]:
            note("锚点", f"第 {nn} 讲 §{sec}: 正文找不到 '{pat}'")
            bad += 1
print(f"C. 链条锚点 = {len(anchors)} 条，异常 = {bad}")

# ---------- D. 待回填 / 痕迹词（分级：硬痕迹 vs 修辞启发） ----------
hard_words = ["待回填", "<details"]
soft_words = ["？——", "干净版", "算干净"]
for n, t in sorted(texts.items()):
    for w in hard_words:
        for m in re.finditer(re.escape(w), t):
            line_no = t.count("\n", 0, m.start()) + 1
            note("痕迹", f"第 {n:02d} 讲 L{line_no}: 出现 '{w}'")
print("D. 硬痕迹扫描完毕")

# ---------- E. AA 覆盖 ----------
aa = (ROOT / "AA_一览.md").read_text(encoding="utf-8")
zero = []
for n in range(1, 32):
    cnt = len(re.findall(rf"第\s*{n:02d}\s*讲|第\s*{n}\s*讲", aa))
    if cnt == 0:
        zero.append(n)
if zero:
    note("AA", f"以下讲次在 AA 中无任何条目: {zero}")
print(f"E. AA 覆盖缺口 = {zero if zero else '无'}")

# ---------- E2. AA 条目重名（分区：概念表/公式表 各自内部查重；跨表分工不算） ----------
secs = {}
start = aa.find("## 一、概念与术语")
end = aa.find("## 二、")
secs["概念表"] = aa[start:end] if start >= 0 and end > start else ""
s2 = aa.find("## 二、")
secs["公式表"] = aa[s2:] if s2 >= 0 else ""
dup = []
for sec_name, body in secs.items():
    names = []
    for line in body.splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|", line)
        if not m:
            continue
        name = m.group(1)
        if set(name) <= set("-: "):
            continue
        names.append(name)
    dup += [f"{sec_name}: {x}" for x in sorted({x for x in names if names.count(x) > 1})]
if dup:
    note("AA", f"重名条目: {dup}")
print(f"E2. AA 分区重名 = {dup if dup else '无'}")

# ---------- F. 讲次表一致性 ----------
plan_rows = {int(m) for m in re.findall(r"^\|\s*(\d\d)\s+\S+", plan, re.M)} - {0}
guide = (ROOT / "00_导览.md").read_text(encoding="utf-8")
guide_rows = {int(m) for m in re.findall(r"^\|\s*(\d\d)\s*\|", guide, re.M)}
for label, s in [("PLAN 状态表", plan_rows), ("导览讲次表", guide_rows)]:
    miss = set(range(1, 32)) - s
    if miss:
        note("讲次", f"{label} 缺行: {sorted(miss)}")
print(f"F. PLAN 行 = {len(plan_rows)}，导览行 = {len(guide_rows)}")

# ---------- G. 跨讲引用 ----------
for n, t in sorted(texts.items()):
    for m in re.finditer(r"第\s*(\d{1,2})\s*讲", t):
        ref = int(m.group(1))
        if ref > 31 or ref not in texts:
            line_no = t.count("\n", 0, m.start()) + 1
            note("引用", f"第 {n:02d} 讲 L{line_no}: 引用了不存在的第 {ref} 讲")
print("G. 跨讲引用检查完毕")

print()
if problems:
    print(f"发现 {len(problems)} 个问题：")
    for p in problems:
        print("  " + p)
    sys.exit(1)
print("全部机器可查项通过（0 问题）")