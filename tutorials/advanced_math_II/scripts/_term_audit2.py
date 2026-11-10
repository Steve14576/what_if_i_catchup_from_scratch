import io, re, glob, os
base = r"e:\E_Vault\CC_Formed_Projs2\WHATIFICATCHUPFROMSCRATCH\tutorials\advanced_math_II"
aa = io.open(os.path.join(base, "AA_一览.md"), encoding="utf-8").read()
# AA concept rows: | 中文名 | 英文 | ...
aa_terms = set()
for line in aa.split("\n"):
    m = re.match(r"\|\s*([\u4e00-\u9fff][^|]{1,24}?)\s*\|", line)
    if m:
        aa_terms.add(m.group(1).strip())
out = []
for f in sorted(glob.glob(os.path.join(base, "*.md"))):
    name = os.path.basename(f)
    if not re.match(r"^\d\d_", name):
        continue
    txt = io.open(f, encoding="utf-8").read()
    for t in aa_terms:
        i = txt.find("**" + t + "**")
        if i < 0:
            continue
        ctx = txt[i:i+100]
        if not re.search(r"[A-Za-z]{3,}", ctx):
            out.append((name, t))
lines = [f"{n}\t{t}" for n, t in out]
io.open(os.path.join(base, "scripts", "_term_audit2.txt"), "w", encoding="utf-8").write("\n".join(lines))
print("AA terms:", len(aa_terms), "| first-mention without English:", len(out))
