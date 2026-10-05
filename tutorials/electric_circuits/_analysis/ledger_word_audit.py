# -*- coding: utf-8 -*-
# =====================================================================
# ledger_word_audit.py —— "账"字使用审计（第 01-19 讲正文）
# 规模纪律：纯文本扫描，< 3 秒。
# 目的：量化"账"字在课程正文中的分布、搭配与位置类型，为写作词汇纪律提供
#       可复现证据。一次性分析，落档于 _analysis/。
# 输出用 GBK 安全字符。
# =====================================================================
import io
import os
import re
import glob
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORD = "账"

# 正文范围：01-19 讲（排除 00_导览 / AA_一览 / PLAN / QnAnExperience）
files = []
for p in sorted(glob.glob(os.path.join(BASE, "*.md"))):
    name = os.path.basename(p)
    m = re.match(r"^(\d{2})_", name)
    if m and 1 <= int(m.group(1)) <= 19:
        files.append((int(m.group(1)), p))

print("=== 一、按讲分布（次数 / 行数 / 密度=次每千行） ===")
tot = 0
per_lec = []
for n, p in files:
    s = io.open(p, encoding="utf-8").read()
    cnt = s.count(WORD)
    lines = len(s.splitlines())
    dens = cnt * 1000.0 / lines
    per_lec.append((n, cnt, lines, dens))
    tot += cnt
for n, cnt, lines, dens in per_lec:
    bar = "#" * min(cnt, 60)
    print("  第 %02d 讲: %3d 次 / %4d 行 = %5.1f 次每千行  %s" % (n, cnt, lines, dens, bar))
print("  合计: %d 次" % tot)

print()
print("=== 二、全局搭配统计 ===")
alltext = ""
for n, p in files:
    alltext += io.open(p, encoding="utf-8").read() + "\n"

# 「X 账」前缀词（1-4 个汉字 + 账）
pref = Counter(re.findall(r"([\u4e00-\u9fff]{1,4})账", alltext))
print("  「X 账」前缀词 top 20:")
for w, c in pref.most_common(20):
    print("    %-6s x%d" % (w, c))

# 动词/固定搭配
fixed = ["账本", "记账", "算账", "对账", "核账", "入账", "结账", "平账", "账单", "账面", "账目", "轧平", "两本账", "三本账", "一笔账", "两笔账", "三笔账"]
print("  固定搭配次数:")
for w in fixed:
    c = alltext.count(w)
    if c:
        print("    %-6s x%d" % (w, c))

print()
print("=== 三、按行类型的分布（正文/小节标题/要点/引用/表格） ===")
typ = Counter()
for n, p in files:
    for l in io.open(p, encoding="utf-8").read().splitlines():
        if WORD not in l:
            continue
        if l.startswith("#"):
            typ["标题行"] += l.count(WORD)
        elif l.startswith(">"):
            typ["引用块(图注/态度表/模板等)"] += l.count(WORD)
        elif l.startswith("|"):
            typ["表格行"] += l.count(WORD)
        elif re.match(r"^\s*[-*\d]", l) and "**" in l:
            typ["列表要点行"] += l.count(WORD)
        else:
            typ["普通段落"] += l.count(WORD)
for k, v in typ.most_common():
    print("    %-24s %d" % (k, v))

print()
print("=== 四、抽样上下文（每讲最多 3 条） ===")
def gbk_safe(t):
    return t.encode("gbk", errors="ignore").decode("gbk")

for n, p in files:
    lines = io.open(p, encoding="utf-8").read().splitlines()
    shown = 0
    for i, l in enumerate(lines):
        if WORD in l and shown < 3:
            ctx = gbk_safe(l.strip())
            j = ctx.find(WORD)
            lo = max(0, j - 30)
            hi = min(len(ctx), j + 31)
            print("  第%02d讲 L%-4d %s%s%s" % (n, i + 1, "..." if lo > 0 else "", ctx[lo:hi], "..." if hi < len(ctx) else ""))
            shown += 1
    if shown == 0:
        print("  第%02d讲 （无）" % n)

print()
print("[DONE] ledger_word_audit 完成。")