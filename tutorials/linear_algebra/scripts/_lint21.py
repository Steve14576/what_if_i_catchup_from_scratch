# -*- coding: utf-8 -*-
# 一次性探针(只读): 21 讲+三件套 的 $/$$ 奇偶与 latex 环境配对统计 (全 ASCII 输出)
# 用法: 从项目根运行 uv run python tutorials/linear_algebra/scripts/_lint21.py
import os

BASE = "tutorials/linear_algebra/"
FILES = ["21_面向ML的矩阵微积分.md", "AA_一览.md", "PLAN.md", "00_导览.md"]


def stat(name):
    path = BASE + name
    s = open(path, encoding="utf-8").read()
    dd = s.count("$$")
    rest = s.count("$") - 2 * dd
    begin = s.count(chr(92) + "begin{")
    end = s.count(chr(92) + "end{")
    left = s.count(chr(92) + "left")
    right = s.count(chr(92) + "right")
    rowbreak = s.count(chr(92) + chr(92))
    la = s.count(chr(92) + "leftarrow")
    ra = s.count(chr(92) + "rightarrow")
    lra = s.count(chr(92) + "leftrightarrow")
    pure_ra = ra - lra
    dleft = left - la - lra
    dright = right - ra
    print("%-30s dd=%d single=%d even=%s begin=%d end=%d left=%d right=%d rowbr=%d"
          % (name, dd, rest, (rest % 2 == 0), begin, end, left, right, rowbreak))
    print("%-30s arrows: leftarrow=%d pure_rightarrow=%d leftrightarrow=%d || delim left=%d right=%d equal=%s"
          % ("", la, pure_ra, lra, dleft, dright, (dleft == dright)))


for f in FILES:
    stat(f)