# -*- coding: utf-8 -*-
# =====================================================================
# rhetoric_audit.py —— 黑话与牵强比喻审计（第 01-18 讲正文，只读）
#   与 ledger_word_audit.py（"账"字专查）配套：本脚本做全词族扫描。
#   词表来源：2026-10-05"账"事件审计记录 + 写作纪律.md 红线 + 收官总检内部词表。
# 规模纪律：纯文本扫描，< 3 秒。
# 输出：控制台分布摘要；逐处上下文写入 _analysis/rhetoric_contexts_01-18.txt
# 说明：本脚本只读正文，不改任何文件。
# =====================================================================
import io
import os
import re
import glob
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_CTX = os.path.join(BASE, "_analysis", "rhetoric_contexts_01-18.txt")

# --- 词表：A 喻体族（含自造动词）/ B 写作侧内部词 ---
GROUP_A = [
    "账", "核账", "记账", "算账", "对账", "入账", "结账", "平账", "账单", "账面", "账目",
    "两本账", "三本账", "一笔账", "两笔账", "三笔账",
    "武器", "武器库", "面孔", "宪法", "金律", "镜子", "舞台", "性格", "命运", "坑",
    "地基", "戏剧", "会师", "风景", "手艺", "骨架", "主菜", "手术刀", "重头戏", "机关",
    "魔法", "判决书", "点燃", "名单", "切一刀", "地图", "定死", "接力", "山峰",
    "大打出手", "故事", "谜团", "高地", "阵地", "防线", "底牌", "王牌", "护身符",
    "紧箍咒", "天花板", "地板", "黑箱", "放大镜", "显微镜", "钥匙", "锁", "天平",
    "算盘", "抽屉", "口袋", "闸门", "闸刀", "窗户", "门面", "舞台", "底色", "骨骼",
]
GROUP_B = [
    "链条", "防错", "元问题", "读者画像", "六问", "认知思维链", "本skill", "wiicufs",
    "PLAN", "agent", "待写", "TODO", "占位",
]
# C 类：半术语（写作纪律：不扩容、每讲 ≤5）——保留但监控
GROUP_C = ["档案"]

def gbk(t):
    return t.encode("gbk", errors="ignore").decode("gbk")

# 正文范围：01-18 讲
files = []
for p in sorted(glob.glob(os.path.join(BASE, "*.md"))):
    name = os.path.basename(p)
    m = re.match(r"^(\d{2})_", name)
    if m and 1 <= int(m.group(1)) <= 18:
        files.append((int(m.group(1)), p))

print("=== 一、按讲 × 词族分布 ===")
all_count = Counter()
per_lec_total = {}
ctx_lines = []
for n, p in files:
    s = io.open(p, encoding="utf-8").read()
    L = s.splitlines()
    hit = Counter()
    for w in GROUP_A + GROUP_B:
        c = s.count(w)
        if c:
            hit[w] += c
            all_count[w] += c
    # 逐处上下文
    for i, l in enumerate(L):
        for w in GROUP_A + GROUP_B:
            if w in l:
                j = l.find(w)
                lo = max(0, j - 30)
                hi = min(len(l), j + 30 + len(w))
                ctx_lines.append("第%02d讲 L%-4d [%s] %s" % (n, i + 1, w, gbk(l[lo:hi].strip())))
    per_lec_total[n] = sum(hit.values())
    if hit:
        print("  第 %02d 讲: 合计 %3d 处  %s" % (n, sum(hit.values()),
              gbk("、".join("%s×%d" % (w, c) for w, c in hit.most_common()))))

print()
print("=== 二、按词汇总（>0 才列） ===")
for w, c in all_count.most_common():
    grp = "A喻体" if w in GROUP_A else "B内部"
    print("  [%s] %-8s x%d" % (grp, w, c))
print("  合计：%d 处（A 喻体 %d、B 内部 %d）"
      % (sum(all_count.values()),
         sum(c for w, c in all_count.items() if w in GROUP_A),
         sum(c for w, c in all_count.items() if w in GROUP_B)))

print()
print("=== 二·补、半术语监控（写作纪律：每讲 ≤5） ===")
bad_arch = []
for n, p in files:
    c = io.open(p, encoding="utf-8").read().count("档案")
    if c:
        flag = "OK" if c <= 5 else "超额"
        bad_arch.append((n, c, flag))
        print("  第 %02d 讲: 档案 x%d  [%s]" % (n, c, flag))
print("  合计 %d 处；超额讲次：%s"
      % (sum(c for _, c, _ in bad_arch),
         [n for n, c, f in bad_arch if f == "超额"] or "无"))

print()
print("=== 三、逐处上下文已写入 ===")
with io.open(OUT_CTX, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(ctx_lines) + "\n")
print("  %s（%d 行）" % (os.path.relpath(OUT_CTX, BASE).replace("\\", "/"), len(ctx_lines)))

print()
print("[DONE] rhetoric_audit 完成（只读）。")