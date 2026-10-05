# -*- coding: utf-8 -*-
# 一次性治理辅助：逐位一致→一致 + 删行后结构检查（双空行/粘连）
# 只处理正文 NN_*.md
import io, os, re, glob

n_sub = 0
for p in sorted(glob.glob('*.md')):
    b = os.path.basename(p)
    if not re.match(r'^(\d{2})_', b):
        continue
    s = io.open(p, encoding='utf-8').read()
    if '逐位一致' in s:
        c = s.count('逐位一致')
        s = s.replace('逐位一致', '一致')
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
        n_sub += c
        print(b, 'x%d' % c)
print('replaced:', n_sub)

print()
print('=== 结构检查 ===')
FENCE = '```'
for p in sorted(glob.glob('*.md')):
    b = os.path.basename(p)
    if not re.match(r'^(\d{2})_', b):
        continue
    lines = io.open(p, encoding='utf-8').read().splitlines()
    in_code = False
    dbl = []
    for i in range(len(lines) - 1):
        if lines[i].strip().startswith(FENCE):
            in_code = not in_code
            continue
        if not in_code and lines[i].strip() == '' and lines[i + 1].strip() == '':
            dbl.append(i + 1)
    glue = [i + 1 for i, l in enumerate(lines)
            if re.match(r'^-{3}[^\s]', l) or re.search(r'[^\s\-|]-{2,}$', l)]
    if dbl or glue:
        print(b, 'double-blank:', dbl[:8], 'glue:', glue[:8])
print('check done')