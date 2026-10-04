# -*- coding: utf-8 -*-
"""修复 05 讲正文：清除"思考文本+工具标记"泄入块与其后重复的 Part A 副本。

策略（全自动边界识别 + 备份 + 前置/后置校验）：
  1. 备份原文件为 .bak；
  2. 起点 = 第一行以 "Hmm wait" 开头的泄入行；
     终点 = 其后第一个恰为 "## 3. 两类钉子户的修正" 的标题行（不删这一行）；
  3. 删除 [起点, 终点) 全部行，并在接缝处插入 "---" 分隔线；
  4. 校验：被删区必须包含工具标记与重复标题；新文件不得残留污染词、
     标题唯一、首行正确、尾部完整。
"""
import io
import os
import shutil
import sys

BASE = r"e:\E_Vault\CC_Formed_Projs2\WHATIFICATCHUPFROMSCRATCH\tutorials\electric_circuits"
P = os.path.join(BASE, "05_结点电压法.md")
BAK = P + ".bak"

shutil.copy2(P, BAK)
print("[OK] 已备份 ->", BAK)

with io.open(P, encoding="utf-8") as f:
    lines = f.read().split("\n")

crlf = all(L.endswith("\r") for L in lines if L)
if crlf:
    lines = [L[:-1] if L.endswith("\r") else L for L in lines]
print("[info] CRLF:", crlf, "; total lines:", len(lines))

start = next(i for i, L in enumerate(lines) if L.startswith("Hmm wait"))
end = next(i for i, L in enumerate(lines)
           if i > start and L.strip() == "## 3. 两类钉子户的修正")
removed = lines[start:end]
print("[info] 起点行号 =", start + 1, "；终点行号（保留）=", end + 1,
      "；删除行数 =", len(removed))

joined = "\n".join(removed)
assert "<｜DSML｜ calls>" in joined, "删除区应包含工具标记"
assert "## 本讲怎么走（脉络图）" in joined, "删除区应包含重复副本的标题"
assert joined.count("# 第 05 讲：结点电压法") >= 1, "删除区应包含重复的讲标题"

new = lines[:start] + ["---", ""] + lines[end:]
j2 = "\n".join(new)

for bad in ["Hmm wait", "<｜DSML｜ calls>", "Continue planning", "dubious",
            "ensure clean", "（修正：）", "别加不确定"]:
    assert bad not in j2, "残留污染词: " + bad
assert j2.count("# 第 05 讲：结点电压法") == 1, "讲标题应唯一"
assert new[0].startswith("# 第 05 讲"), "首行应为讲标题"
assert "## 5. 三种方法选型" in j2 and "下一讲预告" in j2, "尾部应完整"
assert "## 3. 两类钉子户的修正" in j2, "§3 应保留"
assert "受控源三步。---" not in j2, "粘连尾行应已随删除区移除"

with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(new))

print("[OK] 修复完成：", len(lines), "->", len(new), "行（净删", len(lines) - len(new), "行）")
print("[check] 讲标题唯一:", j2.count("# 第 05 讲：结点电压法") == 1)
print("[check] §3/§5/预告齐全:", all(s in j2 for s in
      ["## 3. 两类钉子户的修正", "## 5. 三种方法选型", "下一讲预告"]))
sys.exit(0)