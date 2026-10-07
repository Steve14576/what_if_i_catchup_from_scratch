# -*- coding: utf-8 -*-
# =====================================================================
# host_language_audit.py —— 作者出镜/假客套审计（正文 01-26）
# 规模纪律：纯文本扫描，< 3 秒，只读。
#
# 原则：正文应由对象、条件、因果和例子推进。扫描作者广播、替读者
# 表演、人物登场、认证腔与无操作信息的口令。"先"不自动判错：
# 报告给人工判断，保留时必须携带具体操作顺序信息。
# =====================================================================
import glob
import io
import os
import re
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "_analysis", "host_language_audit_current.txt")

# 默认违规：命中即应改，除非列入 ALLOW_EXACT。
FORBIDDEN = [
    "下一站", "先睹为快", "老规矩", "主角", "出场", "亮牌", "半边天",
    "怪函数", "传说中的", "收编", "聚光灯", "请到", "请上", "拿下",
    "爬向", "松手", "好消息", "不用慌", "给你三秒钟", "你说不出口",
    "脱口而出", "可能想问", "一眼收齐", "当场可见", "全部实跑核对",
    "亲眼", "养成习惯", "肌肉记忆", "垫脚石", "开箱", "备齐", "到齐",
    "通吃", "老朋友", "复辟", "复活", "行李", "问题来了", "体力活",
    "一次买卖", "批量出货", "幼体", "大杀器", "魔法", "魔术", "舞台",
]

# 终章句是课程结束的特定收束，不作为下一站广播处理。
ALLOW_EXACT = {"下一站在你的课程表里"}

# 只报告，不自动判错：须检查是否表示必要的操作顺序。
SEQUENCE_WORDS = ["先看", "先把", "先记住", "第一步", "动手前先"]

files = []
for path in sorted(glob.glob(os.path.join(BASE, "*.md"))):
    name = os.path.basename(path)
    m = re.match(r"^(\d{2})_", name)
    if m:
        files.append((int(m.group(1)), path))

def gbk_safe(text):
    return text.encode("gbk", errors="ignore").decode("gbk")

def context(line, word):
    pos = line.find(word)
    lo = max(0, pos - 38)
    hi = min(len(line), pos + len(word) + 38)
    return gbk_safe(line.strip()[lo:hi])

forbidden_hits = []
sequence_hits = []
counts = Counter()
for lec, path in files:
    lines = io.open(path, encoding="utf-8").read().splitlines()
    for i, line in enumerate(lines, start=1):
        for word in FORBIDDEN:
            if word in line and not any(ok in line for ok in ALLOW_EXACT):
                counts[word] += line.count(word)
                forbidden_hits.append(
                    "第%02d讲 L%-4d [违规/%s] %s" % (lec, i, word, context(line, word))
                )
        for word in SEQUENCE_WORDS:
            if word in line:
                sequence_hits.append(
                    "第%02d讲 L%-4d [顺序待判/%s] %s" % (lec, i, word, context(line, word))
                )

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("=== 默认违规 ===\n")
    f.write("\n".join(forbidden_hits) + "\n")
    f.write("\n=== 操作顺序待判（保留需有具体顺序信息） ===\n")
    f.write("\n".join(sequence_hits) + "\n")

print("=== 作者出镜审计 ===")
print("默认违规：%d 处" % len(forbidden_hits))
for word, cnt in counts.most_common():
    print("  %s x%d" % (word, cnt))
print("操作顺序待判：%d 处" % len(sequence_hits))
print("上下文 -> %s" % os.path.relpath(OUT, BASE).replace("\\", "/"))
print("[DONE] host_language_audit 完成（只读）。")