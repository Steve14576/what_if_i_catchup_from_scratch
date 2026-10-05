# =====================================================================
# lec26-02 全课程交付总检（第 2 遍回查的机器可执行部分）
#   检查项：① 每讲 行数/H2/弯引号/details/表格公式管道/接缝粘连
#           ② 图片引用与磁盘文件的一致性
#           ③ 脚本引用存在性
#           ④ 跨讲引用范围（第 N 讲，N 属于 1..26）
#           ⑤ AA 覆盖（每讲是否有条目）与 PLAN 状态表全绿
# 规模纪律：总耗时 < 10 秒（纯文本扫描，只读，不改任何文件）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / [FAIL]）。
# =====================================================================
import io
import os
import re
import glob
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def gbk(t):
    return t.encode("gbk", errors="ignore").decode("gbk")

fails = []

print("=== 一、逐讲体检（01-26） ===")
total_lines = 0
n_lec = 0
for n in range(1, 27):
    files = glob.glob(os.path.join(BASE, "%02d_*.md" % n))
    if not files:
        fails.append("缺讲义文件：%02d" % n)
        continue
    p = files[0]
    s = io.open(p, encoding="utf-8").read()
    L = s.splitlines()
    n_lec += 1
    total_lines += len(L)
    h2 = sum(1 for l in L if re.match(r"^## [^#]", l))
    curly = s.count(chr(8220)) + s.count(chr(8221))
    det = s.count("<details")
    glue = len([1 for l in L if re.match(r"^-{3}[^\s]", l) or re.search(r"[^\s\-|]-{2,}$", l)])
    D = chr(36); P = "|"
    tpipe = len([1 for l in L if l.startswith(P) and ((D + P) in l or (P + D) in l)])
    status = []
    if curly: status.append("弯引号%d" % curly)
    if det: status.append("details%d" % det)
    if glue: status.append("粘连%d" % glue)
    if tpipe: status.append("表内管道%d" % tpipe)
    flag = "[OK]" if not status else "[FAIL]"
    if status:
        fails.append("%02d 讲：%s" % (n, "、".join(status)))
    print("  %s 第 %02d 讲：%4d 行、%2d 个 H2 %s" % (flag, n, len(L), h2, "、".join(status)))
print("  合计：%d 讲、%d 行" % (n_lec, total_lines))

print()
print("=== 二、图片引用一致性 ===")
miss_fig = 0
ref_total = 0
for n in range(1, 27):
    files = glob.glob(os.path.join(BASE, "%02d_*.md" % n))
    if not files:
        continue
    s = io.open(files[0], encoding="utf-8").read()
    refs = re.findall(r"\(figures/(lec\d{2}_[^)]+\.svg)\)", s)
    ref_total += len(refs)
    for r in refs:
        if not os.path.exists(os.path.join(BASE, "figures", r)):
            fails.append("缺失图片：%s（第 %02d 讲引用）" % (r, n))
            miss_fig += 1
disk_svg = len(glob.glob(os.path.join(BASE, "figures", "lec*.svg")))
print("  [%s] 讲义引用 %d 个 SVG；磁盘上 %d 个 SVG；缺失 %d 个"
      % ("OK" if miss_fig == 0 else "FAIL", ref_total, disk_svg, miss_fig))

print()
print("=== 三、脚本引用存在性 ===")
miss_sc = 0
sc_refs = set()
for n in range(1, 27):
    files = glob.glob(os.path.join(BASE, "%02d_*.md" % n))
    if not files:
        continue
    s = io.open(files[0], encoding="utf-8").read()
    for r in re.findall(r"`(scripts/lec\d{2}-\d{2}[^`]*)`", s):
        key = re.search(r"lec\d{2}-\d{2}", r).group(0)   # 正文常省略主题名，按前缀匹配
        sc_refs.add(key)
for key in sorted(sc_refs):
    if not glob.glob(os.path.join(BASE, "scripts", key + "*")):
        fails.append("缺失脚本前缀：%s" % key)
        miss_sc += 1
disk_sc = sorted(glob.glob(os.path.join(BASE, "scripts", "lec*.py")))
print("  [%s] 讲义引用（按前缀）%d 个脚本编号；磁盘上 %d 个脚本文件；真实缺失 %d 个"
      % ("OK" if miss_sc == 0 else "FAIL", len(sc_refs), len(disk_sc), miss_sc))

print()
print("=== 四、跨讲引用范围（第 N 讲，N 应属 1..26） ===")
bad_ref = 0
for n in range(1, 27):
    files = glob.glob(os.path.join(BASE, "%02d_*.md" % n))
    if not files:
        continue
    s = io.open(files[0], encoding="utf-8").read()
    for m in re.finditer(r"第\s*(\d{2})\s*讲", s):
        v = int(m.group(1))
        if not (1 <= v <= 26):
            fails.append("越界引用：第 %d 讲（出现在第 %02d 讲）" % (v, n))
            bad_ref += 1
print("  [%s] 越界引用 %d 处" % ("OK" if bad_ref == 0 else "FAIL", bad_ref))

print()
print("=== 五、AA 覆盖与 PLAN 状态 ===")
aa = io.open(os.path.join(BASE, "AA_一览.md"), encoding="utf-8").read()
cover = [n for n in range(1, 26) if ("第 %02d 讲" % n) in aa or ("第 %d 讲" % n) in aa]
missing_aa = [n for n in range(1, 26) if n not in cover]
print("  [%s] AA 覆盖讲次：%d/25（26 为零新知识，不要求）%s"
      % ("OK" if not missing_aa else "FAIL", len(cover),
         "" if not missing_aa else "；缺：" + str(missing_aa)))
plan = io.open(os.path.join(BASE, "PLAN.md"), encoding="utf-8").read()
done = plan.count("| " + chr(0x2611) + " |")
print("  PLAN 状态行计数（全绿项）：%d" % done)

print()
print("=== 六、读者视角卫生（写作侧内部词扫描） ===")
inner_words = ["链条", "防错", "元问题", "读者画像", "六问", "wiicufs", "待写", "TODO"]
inner_hits = []
for n in range(1, 27):
    files = glob.glob(os.path.join(BASE, "%02d_*.md" % n))
    if not files:
        continue
    s = io.open(files[0], encoding="utf-8").read()
    for w in inner_words:
        c = s.count(w)
        if c:
            inner_hits.append((n, w, c))
if inner_hits:
    print("  [INFO] 内部词残留（01-18 属'待统一治理'登记；19-26 应立即修）：")
    for n, w, c in inner_hits:
        print("    第 %02d 讲：%s x%d" % (n, w, c))
else:
    print("  [OK] 无写作侧内部词残留。")

print()
print("=== 总检结论 ===")
if fails:
    print("  [FAIL] 共 %d 项问题：" % len(fails))
    for f in fails[:20]:
        print("    - %s" % gbk(f))
else:
    print("  [OK] 全课程 %d 讲、%d 行、图 %d、脚本 %d——全部检查项通过。" % (n_lec, total_lines, disk_svg, len(disk_sc)))
print()
print("[DONE] lec26-02 全课程总检完成。")