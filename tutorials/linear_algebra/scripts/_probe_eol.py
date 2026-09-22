# -*- coding: utf-8 -*-
# 一次性探针(只读): 统计指定文件的行尾形态与引号形态 (全 ASCII 代码)
# 用法: uv run python _probe_eol.py
import os

BASE = "tutorials/linear_algebra/"
FILES = ["AA_一览.md", "PLAN.md", "00_导览.md", "21_面向ML的矩阵微积分.md"]


def stat(path):
    d = open(path, "rb").read()
    crlf = d.count(bytes([13, 10]))
    lf_total = d.count(bytes([10]))
    cr_total = d.count(bytes([13]))
    bare_lf = lf_total - crlf
    bare_cr = cr_total - crlf
    straight_dq = d.count(bytes([34]))
    curved_l = d.count(bytes([0xE2, 0x80, 0x9C]))
    curved_r = d.count(bytes([0xE2, 0x80, 0x9D]))
    sq_l = d.count(bytes([0xE2, 0x80, 0x98]))
    sq_r = d.count(bytes([0xE2, 0x80, 0x99]))
    print("%-28s CRLF=%-5d bare_LF=%-3d bare_CR=%-3d DQ=%-4d cL=%-3d cR=%-3d sqL=%d sqR=%d"
          % (os.path.basename(path), crlf, bare_lf, bare_cr,
             straight_dq, curved_l, curved_r, sq_l, sq_r))


for f in FILES:
    stat(BASE + f)