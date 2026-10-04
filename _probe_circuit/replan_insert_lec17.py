# -*- coding: utf-8 -*-
"""编号平移审计脚本：为"插入新第 17 讲《磁路与铁心线圈》"执行 17..25 -> +1 平移。

范围：仅 PLAN.md 与 00_导览.md（已交付讲次的正文不在此脚本内，改用定点替换）。
规则：独立出现的讲次编号 17..25 全部 +1（保护小数/多位数字：前后不得为数字或小数点）；
      整行包含"磁路与铁芯变压器的工程计算"的行跳过（稍后整体重写，不参与平移）。
用法：
    python replan_insert_lec17.py          # 干跑：只打印逐行 before/after 供人工审计
    python replan_insert_lec17.py apply    # 应用：先备份 .bak，写入后立即复核行数
"""
import io
import os
import re
import shutil
import sys

BASE = r"e:\E_Vault\CC_Formed_Projs2\WHATIFICATCHUPFROMSCRATCH\tutorials\electric_circuits"
FILES = [os.path.join(BASE, "PLAN.md"), os.path.join(BASE, "00_导览.md")]
SKIP_SUBSTR = ["磁路与铁芯变压器的工程计算", "第 17 章（非线性）"]

PAT = re.compile(r"(?<![\d.])(1[7-9]|2[0-5])(?![\d.])")


def bump(match):
    return str(int(match.group(1)) + 1)


apply_mode = len(sys.argv) > 1 and sys.argv[1] == "apply"
grand_total = 0
report = []

for path in FILES:
    name = os.path.basename(path)
    with io.open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    new_lines = []
    changes = []
    for idx, ln in enumerate(lines):
        if any(s in ln for s in SKIP_SUBSTR):
            new_lines.append(ln)
            continue
        new = PAT.sub(bump, ln)
        new_lines.append(new)
        if new != ln:
            changes.append((idx + 1, ln, new))

    report.append("=" * 78)
    report.append("[{}] 命中并改动 {} 行".format(name, len(changes)))
    for (n, old, new) in changes:
        report.append("L{}  旧: {}".format(n, old))
        report.append("     新: {}".format(new))
    print("[{}] 命中并改动 {} 行".format(name, len(changes)))
    grand_total += len(changes)

    if apply_mode:
        bak = path + ".bak"
        shutil.copy2(path, bak)
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(new_lines))
        with io.open(path, encoding="utf-8") as f:
            re_lines = f.read().split("\n")
        assert len(re_lines) == len(lines), "行数应保持不变"
        old_skip = [x for x in lines if "磁路与铁芯变压器的工程计算" in x]
        new_skip = [x for x in re_lines if "磁路与铁芯变压器的工程计算" in x]
        assert old_skip == new_skip, "跳过行应 Byte 保持不变"
        print("[OK] {} 已应用（备份 {}）".format(name, bak))

print("=" * 78)
print("总计两文件改动行数：{}（模式：{}）".format(grand_total, "apply" if apply_mode else "dry-run"))
audit_path = os.path.join(BASE, "..", "..", "_probe_circuit", "replan_audit.txt")
audit_path = os.path.abspath(audit_path)
with io.open(audit_path, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(report))
print("审计明细已写入：", audit_path)
sys.exit(0)