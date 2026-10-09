# =====================================================================
# second_pass_check.py —— 第二遍（全课程回查）的可复现检查脚本
# 作者自用（维护层），不属读者文本。
#
# 检查项：
#   C1 全角引号计数（应为 0）
#   C2 LaTeX 圆括号定界符 \( \)（应为 0；仓库口径用 $...$）
#   C3 禁用词族（喻体词 + 作者出镜 + 自我推翻句式，应为 0）
#   C4 图引用：文件是否真实存在；每讲引用数是否为 3
#   C5 数字对账：脚本 EXP 行的数字是否在对应正文中出现（含舍入候选）
#
# 复跑：先在上一级目录用 runner 重跑全部脚本到 _analysis/_rerun/，再
#       uv run python _analysis/second_pass_check.py
# =====================================================================
import glob
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RERUN = os.path.join(BASE, "_analysis", "_rerun")

BANNED = ["账", "武器", "面孔", "宪法", "金律", "舞台", "地基", "镜子", "门票",
          "魔法", "骨架", "主角", "出场", "亮牌", "核账", "需谨慎"]
# 自我推翻/半途改口的句式（单用"……"不算，须后接改口词）
SELF_RE = re.compile(r"……\s*.{0,8}(更|不|其实|应当|应该|换成|改成|准确)")

FIG_RE = re.compile(r"!\[[^\]]*\]\(figures/([^)]+)\)")
NUM_RE = re.compile(r"\d+\.\d+")
LEC_RE = re.compile(r"^(0[1-9]|[12]\d)_")

issues = []
mds = sorted(glob.glob(os.path.join(BASE, "*.md")))

for md in mds:
    name = os.path.basename(md)
    s = open(md, encoding="utf-8").read()
    is_lec = bool(LEC_RE.match(name))

    # C1 全角引号
    n = s.count("\u201c") + s.count("\u201d")
    if n:
        issues.append("[C1] %s: 全角引号 %d" % (name, n))

    # C2 圆括号定界符
    n = s.count("\\(") + s.count("\\)")
    if n:
        issues.append("[C2] %s: 圆括号定界符 %d" % (name, n))

    # C3 禁用词（PLAN 是作者台账，其"台账/骨架"属工作流行话，不查）
    if name != "PLAN.md":
        for w in BANNED:
            c = s.count(w)
            if c:
                issues.append("[C3] %s: 禁用词 %s x%d" % (name, w, c))
        for m in SELF_RE.finditer(s):
            issues.append("[C3] %s: 疑似自我推翻句式「%s」" % (name, m.group(0)[:20]))

    # C4 图引用
    refs = FIG_RE.findall(s)
    for r in refs:
        if not os.path.exists(os.path.join(BASE, "figures", r)):
            issues.append("[C4] %s: 图文件缺失 %s" % (name, r))
    if is_lec and len(refs) != 3:
        issues.append("[C4] %s: 图引用数 %d != 3" % (name, len(refs)))

    # C5 数字对账
    if not is_lec:
        continue
    nn = LEC_RE.match(name).group(1)
    txts = sorted(glob.glob(os.path.join(RERUN, "lec%s-*.txt" % nn)))
    if not txts:
        issues.append("[C5] %s: 找不到重跑输出（lec%s-*）" % (name, nn))
        continue
    out = open(txts[0], encoding="utf-8").read()

    nums = set()
    for line in out.splitlines():
        if "EXP" not in line:
            continue
        for m in NUM_RE.findall(line):
            v = float(m)
            if 0.01 <= abs(v) <= 1e6:
                nums.add(m)

    missing = []
    for m in sorted(nums, key=float):
        v = float(m)
        cands = {m, "%g" % v, "%.0f" % v, "%.1f" % v, "%.2f" % v, "%.3f" % v, "%.4f" % v}
        if not any(c in s for c in cands):
            missing.append(m)
    if missing:
        issues.append("[C5] %s: 脚本数字未在正文出现 -> %s" % (name, ", ".join(missing)))

print("=== 第二遍检查结果 ===")
print("扫描 md 文件数：%d（其中讲次正文 %d）"
      % (len(mds), sum(1 for m in mds if LEC_RE.match(os.path.basename(m)))))

# ---------------------------------------------------------------------
# C6 覆盖清单逐项确认：PLAN 3.1 每讲条目 -> 关键词 -> 回查该讲正文
COVERAGE = {
    "01": ["强度", "刚度", "稳定性", "杆件", "块体", "各向同性", "小变形", "截面法",
           "线应变", "切应变", "体积力", "表面力"],
    "02": ["轴力图", "平面假设", "圣维南", "切应力互等", "应力集中"],
    "03": ["变截面", "泊松比", "胡克定律", "冷作硬化", "铸铁", "安全系数", "三类问题"],
    "04": ["剪切面", "挤压面", "平键", "双剪", "铆钉"],
    "05": ["剪切模量", "剪切胡克定律", "扭矩图", "极惯性矩", "抗扭截面系数", "9550"],
    "06": ["扭转角", "扭转刚度", "空心", "非圆截面", "翘曲"],
    "07": ["静矩", "平行移轴", "惯性半径", "主惯性轴"],
    "08": ["剪力方程", "弯矩方程", "微分关系", "控制截面", "叠加原理"],
    "09": ["纯弯曲", "中性轴", "抗弯截面系数", "横力弯曲"],
    "10": ["抛物线", "腹板", "等强度梁", "许用切应力"],
    "11": ["挠曲线近似微分方程", "边界条件", "连续条件", "叠加法", "提高弯曲刚度"],
    "12": ["超静定次数", "静定基", "变形比较法", "拉压超静定", "温度应力", "装配应力"],
    "13": ["单元体", "主平面", "应力圆", "莫尔圆", "主应力"],
    "14": ["广义胡克定律", "体积应变", "体积模量", "弹性常数", "应变能"],
    "15": ["第一强度理论", "第二强度理论", "第三强度理论", "第四强度理论",
           "薄壁圆筒", "环向", "相当应力"],
    "16": ["截面核心", "斜弯曲", "偏心"],
    "17": ["欧拉", "长度系数", "柔度", "折减系数", "临界应力总图"],
    "18": ["应变能", "卡氏定理", "单位载荷法", "莫尔积分", "图形互乘", "互等"],
    "19": ["基本体系", "柔度系数", "正则方程", "对称性"],
    "20": ["动荷系数", "等加速", "冲击", "水平冲击"],
    "21": ["循环特征", "脉动循环", "持久极限", "S-N", "有效应力集中系数",
           "尺寸系数", "表面质量系数"],
    "22": ["结构力学", "弹性力学", "塑性力学", "有限元", "断裂力学", "实验应力分析"],
}
for nn, kws in sorted(COVERAGE.items()):
    hits = sorted(glob.glob(os.path.join(BASE, "%s_*.md" % nn)))
    if not hits:
        issues.append("[C6] 找不到第 %s 讲正文" % nn)
        continue
    s = open(hits[0], encoding="utf-8").read()
    miss = [k for k in kws if k not in s]
    if miss:
        issues.append("[C6] %s 讲：覆盖关键词未命中 -> %s"
                      % (nn, ", ".join(miss)))

# ---------------------------------------------------------------------
# C7 认知链对账：PLAN 链条里的 [-> §N] 标记 -> 该讲正文是否存在对应小节
plan = open(os.path.join(BASE, "PLAN.md"), encoding="utf-8").read()
chain_blocks = re.findall(r"^- \*\*(\d\d)[^*]*\*\*((?:(?!\n- \*\*\d\d)[\s\S])*)",
                          plan, re.M)
HEAD_RE = re.compile(r"^#{2,3}\s+(\d+(?:\.\d+)*)", re.M)
SEC_RE = re.compile(r"§(\d+(?:\.\d+)*)")
for nn, block in chain_blocks:
    hits = sorted(glob.glob(os.path.join(BASE, "%s_*.md" % nn)))
    if not hits:
        continue
    secs = set(HEAD_RE.findall(open(hits[0], encoding="utf-8").read()))
    for num in sorted(set(SEC_RE.findall(block))):
        if num not in secs:
            issues.append("[C7] %s 讲：链条标记 §%s 在正文中无对应小节标题"
                          % (nn, num))

# ---------------------------------------------------------------------
# C8 AA 概念表批量对账：条目声称的"首次出现讲次"里必须真的出现该概念
aa = open(os.path.join(BASE, "AA_一览.md"), encoding="utf-8").read()
concept_part = aa.split("## 二、公式")[0]
for line in concept_part.splitlines():
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip("|").split("|")]
    if len(cells) < 5 or cells[0] in ("概念", "---"):
        continue
    name_cn, lec = cells[0], cells[3]
    m = re.search(r"第\s*(\d\d)\s*讲", lec)
    if not m:
        continue
    nn = m.group(1)
    hits = sorted(glob.glob(os.path.join(BASE, "%s_*.md" % nn)))
    if not hits:
        issues.append("[C8] AA 条目《%s》指向不存在的第 %s 讲" % (name_cn, nn))
        continue
    s = open(hits[0], encoding="utf-8").read()
    frags = [p.strip(" 　") for p in re.split(r"[（(／/、，,]", name_cn) if p.strip(" 　")]
    if frags and not any(f in s for f in frags):
        issues.append("[C8] AA 概念《%s》声称首见第 %s 讲，但该讲正文未出现该词"
                      % (name_cn, nn))

# ---------------------------------------------------------------------
# C9 跨讲引用一致性：讲号合法 / 前置只引早于本讲 / 下一讲预告指向下一讲
for md in mds:
    name = os.path.basename(md)
    mm = LEC_RE.match(name)
    if not mm:
        continue
    nn = int(mm.group(1))
    s = open(md, encoding="utf-8").read()

    for ref in re.findall(r"第\s*(\d{1,2})\s*讲", s):
        if not (1 <= int(ref) <= 22):
            issues.append("[C9] %s: 非法讲号「第 %s 讲」" % (name, ref))

    for m2 in re.finditer(r"^> \*\*前置\*\*：(.+)$", s, re.M):
        for a, b in re.findall(r"(\d+)\s*(?:[–—-]\s*(\d+))?\s*讲", m2.group(1)):
            top = int(b) if b else int(a)
            if top >= nn:
                issues.append("[C9] %s: 前置引用了不早于本讲的「第 %s 讲」" % (name, b or a))

    m3 = re.search(r"下一讲预告——第\s*(\d+)\s*讲", s)
    if nn < 22:
        if not m3:
            issues.append("[C9] %s: 缺「下一讲预告」" % name)
        elif int(m3.group(1)) != nn + 1:
            issues.append("[C9] %s: 下一讲预告指向第 %s 讲（应为 %d）"
                          % (name, m3.group(1), nn + 1))
    elif m3:
        issues.append("[C9] %s: 末讲仍保留「下一讲预告」" % name)

if issues:
    print("发现问题 %d 项：" % len(issues))
    for it in issues:
        print("  " + it)
else:
    print("[OK] 未发现问题")