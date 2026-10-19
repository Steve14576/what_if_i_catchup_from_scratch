# L22 full-course regression: re-run all lec scripts and summarize
# 规模纪律: 单脚本各自 <5 s, 20 个总时长 <90 s; 纯 numpy
# print 全 ASCII

import glob
import io
import os
import subprocess
import sys

base = os.path.dirname(os.path.abspath(__file__))
scripts = sorted(glob.glob(os.path.join(base, "lec[0-9][0-9]-01_*.py")))
scripts = [s for s in scripts if "lec22" not in os.path.basename(s)]

print("=" * 64)
print("L22 full-course regression: re-run all %d lec scripts" % len(scripts))
print("=" * 64)

results = []
for s in scripts:
    name = os.path.basename(s)
    try:
        out = subprocess.run([sys.executable, s], capture_output=True, text=True,
                             timeout=120, cwd=base).stdout
        ok = "OVERALL: ALL PASS" in out
    except Exception as e:
        ok = False
        out = str(e)
    results.append((name, ok))
    print("%s  ...  %s" % (name, "OVERALL: ALL PASS" if ok else "FAILED"))

n_ok = sum(1 for _, ok in results if ok)
print("-" * 64)
print("REGRESSION SUMMARY: %d/%d scripts ALL PASS" % (n_ok, len(results)))
if n_ok != len(results):
    print("FAILED scripts:")
    for name, ok in results:
        if not ok:
            print("  " + name)
    sys.exit(1)
