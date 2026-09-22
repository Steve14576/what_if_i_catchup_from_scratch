# fix21_esc_corruption.py
# One-off, auditable repair for escape-layer corruption in the lecture 21 markdown.
# Dry-run by default; pass --apply to write back.
#
# Pattern A (fragment): a real newline (CR+LF on this file) immediately followed by
#   'abla' -- produced when the literal six-character command BS+'nabla' had its
#   BS+'n' escape sequence decoded into a platform newline by some writing layer.
#   Repair: CR + LF + 'abla' -> BS + 'nabla'   (stitches the formula back into one line)
#   A bare LF variant is handled as a fallback; on this file it should be zero.
# Pattern B (doubled backslash): BS + BS + 'nabla' -> BS + 'nabla'.
#
# Both patterns cannot occur in healthy content: a line of this document never
# legitimately starts with the bare token 'abla', and a doubled backslash
# followed by 'nabla' is never used in it. Stats are printed regardless.

import sys

BS = chr(92)
LF = chr(10)
TAB = chr(9)
CR = chr(13)

PATH = 'e:/E_Vault/CC_Formed_Projs2/WHATIFICATCHUPFROMSCRATCH/tutorials/linear_algebra/21_面向ML的矩阵微积分.md'

def stats(s):
    out = {}
    out['total_len'] = len(s)
    out['CRLF+abla'] = s.count(CR + LF + 'abla')
    out['LF+abla'] = s.count(LF + 'abla')
    out['BS+LF+abla'] = s.count(BS + LF + 'abla')
    out['BS BS nabla'] = s.count(BS + BS + 'nabla')
    out['BS BS BS nabla'] = s.count(BS + BS + BS + 'nabla')
    out['TAB'] = s.count(TAB)
    out['CR'] = s.count(CR)
    out['ctrl_other'] = len([c for c in s if ord(c) < 32 and c not in (LF, TAB, CR)])
    for pre in ['eq', 'ot', 'otin', 'leq', 'geq', 'ewline', 'neg']:
        k = s.count(LF + pre)
        if k:
            out['LF+' + pre] = k
    return out

with open(PATH, 'r', encoding='utf-8', newline='') as f:
    data = f.read()

print('--- before ---')
for k, v in stats(data).items():
    print(k, '=', v)

idx = data.find(CR + LF + 'abla')
while idx >= 0:
    print('ctx:', ascii(data[max(0, idx - 40):idx + 24]))
    idx = data.find(CR + LF + 'abla', idx + 1)

from collections import Counter
hist = Counter()
i = data.find(BS + 'nabla')
while i >= 0:
    hist[data[i - 1] if i > 0 else 'BOL'] += 1
    i = data.find(BS + 'nabla', i + 1)
print('--- prev-char histogram (char right before each BS+nabla) ---')
for ch, k in sorted(hist.items()):
    print(ascii(ch), k)

if '--scan' in sys.argv:
    i = data.find(BS + 'nabla')
    while i >= 0:
        prev = data[i - 1] if i > 0 else 'BOL'
        if prev != '$':
            print('scan:', ascii(prev), '::', ascii(data[max(0, i - 45):i + 30]))
        i = data.find(BS + 'nabla', i + 1)

grad = BS + 'nabla'
# Order matters: normalize doubled backslashes first, then stitch CRLF fragments,
# then any bare-LF fragments as a fallback.
fixed = data.replace(BS + BS + 'nabla', grad)
fixed = fixed.replace(CR + LF + 'abla', grad)
fixed = fixed.replace(LF + 'abla', grad)

# Confirmed single typo: a CJK comma directly followed by the command with no
# '$' delimiter in between (the only such spot; all sibling spots keep their '$').
CJK_COMMA = chr(0xFF0C)
n_c = fixed.count(CJK_COMMA + grad)
fixed = fixed.replace(CJK_COMMA + grad, CJK_COMMA + '$' + grad)
print('CJK-comma-before-nabla occurrences =', n_c)

print('--- planned ---')
print('char delta =', len(fixed) - len(data))

if '--apply' in sys.argv:
    with open(PATH, 'w', encoding='utf-8', newline='') as f:
        f.write(fixed)
    with open(PATH, 'r', encoding='utf-8', newline='') as f:
        chk = f.read()
    print('--- after ---')
    for k, v in stats(chk).items():
        print(k, '=', v)
    print('APPLIED')
else:
    print('dry-run only; run with --apply to write back')