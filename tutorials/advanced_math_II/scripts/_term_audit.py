import io, re, glob, os
base = r"e:\E_Vault\CC_Formed_Projs2\WHATIFICATCHUPFROMSCRATCH\tutorials\advanced_math_II"
stop = set("注意 例子 为什么 验证 解法 小结 说明 答案 参考 作业 解释 结论 证明 推导 定义 记法 理解 直觉 一句话 怎么做 怎么读 边界 易错 问题桥 目标 前置 本讲 下一步 对照 意义 读法 判断 用法 回顾 补充 修正 警告 提醒 思路 步骤 结果 目的 条件 方向 来源 形式 记 例 解".split())
out = []
for f in sorted(glob.glob(os.path.join(base, "*.md"))):
    name = os.path.basename(f)
    if not re.match(r"^\d\d_", name):
        continue
    txt = io.open(f, encoding="utf-8").read()
    terms = re.findall(r"\*\*([\u4e00-\u9fff][^*\n]{1,14})\*\*", txt)
    seen = set()
    for t in terms:
        if t in stop or t in seen:
            continue
        seen.add(t)
        i = txt.find("**" + t + "**")
        ctx = txt[i:i+90]
        if not re.search(r"[A-Za-z]{3,}", ctx):
            out.append((name, t))
lines = [f"{n}\t{t}" for n, t in out]
io.open(os.path.join(base, "scripts", "_term_audit.txt"), "w", encoding="utf-8").write("\n".join(lines))
print("count:", len(out))
