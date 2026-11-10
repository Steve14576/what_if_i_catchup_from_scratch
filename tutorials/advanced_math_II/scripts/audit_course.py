# 第二遍全课程回查：机器可查项（只读，不改文件）
# 输出 ASCII-safe，避免 GBK 控制台报错。
import io
import re
from pathlib import Path

ROOT = Path(r"e:\E_Vault\CC_Formed_Projs2\WHATIFICATCHUPFROMSCRATCH\tutorials\advanced_math_II")
LEC = sorted([p for p in ROOT.glob("*.md") if re.match(r"^\d{2}_", p.name)])
PLAN = (ROOT / "PLAN.md").read_text(encoding="utf-8")
AA = (ROOT / "AA_一览.md").read_text(encoding="utf-8")

problems = []


def add(kind, where, detail):
    problems.append((kind, where, detail))


# ---------- 1. 结构：施工图条数 vs 正文二级节数 ----------
def plan_counts():
    # 只解析 §三（到 "## 四、" 为止），避免 §四 的同名讲标题覆盖
    out = {}
    cur = None
    in_sec3 = False
    for line in PLAN.split("\n"):
        if line.startswith("## 三、"):
            in_sec3 = True
            continue
        if line.startswith("## 四、"):
            in_sec3 = False
            cur = None
            continue
        if not in_sec3:
            continue
        m = re.match(r"^### (\d{2}) ", line)
        if m:
            cur = m.group(1)
            out[cur] = 0
            continue
        if cur and re.match(r"^\s*(?:-\s*)?\d+\.\s", line):
            out[cur] += 1
        elif cur and line.startswith("### "):
            cur = None
    return out


pc = plan_counts()
for p in LEC:
    m = re.match(r"^(\d{2})_", p.name)
    if not m:
        continue
    n = m.group(1)
    text = p.read_text(encoding="utf-8")
    secs = [ln for ln in text.split("\n") if ln.startswith("## ")]
    secs = [s for s in secs if not re.match(r"^## (小结|作业|结课)", s)]
    if n in pc and pc[n] != len(secs):
        add("STRUCT", p.name, f"plan={pc[n]} body_sections={len(secs)}")

# ---------- 2. 图引用存在 + 图号顺序 ----------
for p in LEC:
    text = p.read_text(encoding="utf-8")
    for ref in re.findall(r"figures/([\w.\-]+\.svg)", text):
        if not (ROOT / "figures" / ref).exists():
            add("FIG_MISSING", p.name, ref)
    nums = [int(x) for x in re.findall(r"\*图\s*(\d+)：", text)]
    if nums != sorted(nums):
        add("FIG_ORDER", p.name, str(nums))

# ---------- 3. 脚本引用存在 ----------
for p in LEC:
    text = p.read_text(encoding="utf-8")
    for ref in re.findall(r"scripts/([\w.\-]+\.py)", text):
        if not (ROOT / "scripts" / ref).exists():
            add("SCRIPT_MISSING", p.name, ref)

# ---------- 4. 占位 / details ----------
for p in LEC:
    for i, ln in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        if re.search(r"待回填|TODO|同上|见例|同例", ln) and not ln.lstrip().startswith("|"):
            add("PLACEHOLDER", f"{p.name}:{i}", ln.strip()[:60])
        if "<details>" in ln:
            add("DETAILS", f"{p.name}:{i}", ln.strip()[:60])

# ---------- 5. 喻体词族 / 自造动词 ----------
BAD = ["核账", "账本", "旧账", "两本账", "三笔账", "武器", "面孔", "宪法", "金律", "舞台", "地基", "镜子", "门票", "魔法"]
for p in LEC:
    for i, ln in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        for w in BAD:
            if w in ln:
                add("METAPHOR", f"{p.name}:{i}", f"{w}: {ln.strip()[:50]}")

# ---------- 6. 行内公式 $ 配对（粗查） ----------
for p in LEC:
    for i, ln in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        if ln.strip().startswith("$$"):
            continue
        if ln.count("$") % 2 == 1:
            add("DOLLAR_ODD", f"{p.name}:{i}", ln.strip()[:60])

# ---------- 7. AA 首次讲次：该讲正文是否出现该概念 ----------
# AA 表格行：| 中文名 | 英文 | 定义 | 第 NN 讲 | 层次 |
aa_rows = [ln for ln in AA.split("\n") if ln.startswith("|") and "第" in ln and "讲" in ln]
for ln in aa_rows:
    cells = [c.strip() for c in ln.strip("|").split("|")]
    if len(cells) < 5:
        continue
    name, first = cells[0], cells[-2] if cells[-1] else cells[-2]
    m = re.search(r"第\s*(\d{2})\s*讲", ln)
    if not m or name.startswith("概念"):
        continue
    n = m.group(1)
    target = ROOT / next((p.name for p in LEC if p.name.startswith(n + "_")), "")
    if not target.exists():
        add("AA_NO_LECTURE", name, f"first={n}")
        continue
    text = target.read_text(encoding="utf-8")
    key = re.sub(r"\$[^$]*\$", "", name)
    key = re.sub(r"[（(].*?[）)]", "", key).strip()
    key = key.split("、")[0].strip()
    if key and key not in text:
        add("AA_KEY_NOT_IN_LECTURE", name, f"first={n}, key={key}")

# ---------- 8. 非讲次文件的占位 ----------
for f in ["AA_一览.md", "00_导览.md"]:
    t = (ROOT / f).read_text(encoding="utf-8")
    if "待回填" in t or "TODO" in t:
        add("PLACEHOLDER_FILE", f, "contains placeholder")

# ---------- 输出 ----------
print(f"lectures={len(LEC)} problems={len(problems)}")
from collections import Counter
print("by kind:", dict(Counter(k for k, _, _ in problems)))
for k, where, detail in problems[:200]:
    print(ascii(f"[{k}] {where} :: {detail}"))
