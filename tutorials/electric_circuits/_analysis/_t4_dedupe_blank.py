# -*- coding: utf-8 -*-
# 删脉络图后，去除正文代码块外的连续空行（保留代码块内格式）
import glob, io, os, re

for p in sorted(glob.glob('*.md')):
    b = os.path.basename(p)
    if not re.match(r'^(\d{2})_', b):
        continue
    lines = io.open(p, encoding='utf-8').read().splitlines()
    new = []
    in_code = False
    removed = 0
    for line in lines:
        if line.strip().startswith('```'):
            in_code = not in_code
        if not in_code and line.strip() == '' and new and new[-1].strip() == '':
            removed += 1
            continue
        new.append(line)
    if removed:
        io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(new) + '\n')
        print(b, 'removed', removed)