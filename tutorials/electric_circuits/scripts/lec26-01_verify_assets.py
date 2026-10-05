# =====================================================================
# lec26-01 与后续的接口：课程资产总清单 + 三张地图（主线地图 / 下游接口 / 边界示意）
#          （第 26 讲为"零新知识地图讲"：本脚本不产生新数值结论，
#           只做交付总检（资产清单）与三张地图的绘制）
# 规模纪律：总耗时 < 10 秒（文件扫描 + 三图）。
# 输出用 GBK 安全字符（无特殊符号，用 [OK] / ->）。
# =====================================================================
import os
import re
import glob

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# ---------------------------------------------------------------------
print("=== 课程资产总检（交付清单） ===")
lects = []
for p in sorted(glob.glob(os.path.join(BASE, "*.md"))):
    name = os.path.basename(p)
    m = re.match(r"^(\d{2})_(.+)\.md$", name)
    if m:
        s = open(p, encoding="utf-8").read()
        lects.append((int(m.group(1)), name, len(s.splitlines())))
total_lines = 0
for n, name, lines in lects:
    total_lines += lines
print("  讲义正文：%d 个文件、合计 %d 行" % (len(lects), total_lines))
sc = sorted(glob.glob(os.path.join(BASE, "scripts", "lec*.py")))
fg = sorted(glob.glob(os.path.join(BASE, "figures", "lec*.svg")))
print("  验证脚本：%d 个；图形（SVG）：%d 个" % (len(sc), len(fg)))

# ---------------------------------------------------------------------
print()
print("=== 生成图 1：全课程主线地图（七大板块） ===")
blocks = [
    ("直流电阻电路 01-08", 1, 8, "#1f5fa8"),
    ("动态电路 09-12", 9, 12, "#2e7d32"),
    ("正弦稳态 13-16", 13, 16, "#c0392b"),
    ("磁路与耦合 17-18", 17, 18, "#8e44ad"),
    ("频率与变换 19-22", 19, 22, "#e67e22"),
    ("二端口与矩阵 23-25", 23, 25, "#16a085"),
    ("接口 26", 26, 26, "#7f8c8d"),
]
fig, ax = plt.subplots(figsize=(11.0, 3.0))
for i, (name, a, b, cc) in enumerate(blocks):
    ax.barh(0, b - a + 1, left=a - 0.5, height=0.55, color=cc, alpha=0.85, edgecolor="white")
    tag_y = 0.42 if name != "接口 26" else -0.42
    ax.text((a + b) / 2, tag_y, name, ha="center", va="bottom" if tag_y > 0 else "top", fontsize=9.5, color=cc)
    ax.text((a + b) / 2, 0, "%d-%d" % (a, b), ha="center", va="center", fontsize=9, color="white")
ax.set_xlim(0, 27)
ax.set_ylim(-0.75, 0.9)
ax.set_yticks([])
ax.set_xticks(range(1, 27))
ax.set_xticklabels([str(i) for i in range(1, 27)], fontsize=8)
ax.set_xlabel("讲次")
ax.set_title("《电路学》26 讲主线地图：七大板块", fontsize=12)
plt.tight_layout()
save_stem = "lec26_fig1_map"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 2：下游课程接口地图 ===")
fig, ax = plt.subplots(figsize=(10.6, 6.0))
ax.axis("off")
ax.text(0.5, 0.5, "《电路学》\n（本课程）", ha="center", va="center", fontsize=14,
        bbox=dict(boxstyle="round,pad=0.5", fc="#eaf2fb", ec="#1f5fa8", lw=2))
targets = [
    (0.5, 0.90, "模拟电子技术", "受控源→晶体管小信号（H 参数）\n虚短虚断→反馈放大器（08 讲）", "#c0392b"),
    (0.88, 0.60, "信号与系统", "拉氏变换与 H(s)（21/22 讲）\n卷积/傅里叶/滤波（11/19/20 讲）", "#2e7d32"),
    (0.75, 0.12, "自动控制原理", "传递函数与极点零点（22 讲）\n状态空间（25 讲）→ PID/稳定性", "#e67e22"),
    (0.25, 0.12, "电力工程", "三相与变压器（16/17/18 讲）\n功率因数补偿（15 讲）", "#8e44ad"),
    (0.12, 0.60, "电力电子与 DSP", "开关变换器的非正弦（20 讲）\n采样与离散（信号接口分支）", "#16a085"),
]
for x, y, title, desc, cc in targets:
    ax.annotate("", xy=(x, y), xytext=(0.5, 0.5),
                arrowprops=dict(arrowstyle="->", color=cc, lw=1.8))
    ax.text(x, y + 0.045, title, ha="center", va="bottom", fontsize=11.5, color=cc, weight="bold")
    ax.text(x, y - 0.035, desc, ha="center", va="top", fontsize=8.6, color="#333333")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_title("从《电路学》出发：五条下游接口与它们带走的工具", fontsize=12)
plt.tight_layout()
save_stem = "lec26_fig2_interface"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

# ---------------------------------------------------------------------
print()
print("=== 生成图 3：集总参数的边界（尺寸 vs 波长） ===")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 3.8))
# 左：集总模型
a1.set_title("尺寸 << 波长（低频）：集总参数模型", fontsize=11)
a1.plot([0.1, 0.9], [0.65, 0.65], color="#333333", lw=2)
a1.plot([0.2, 0.2], [0.65, 0.5], color="#333333", lw=1.5)
a1.plot([0.5, 0.5], [0.65, 0.5], color="#333333", lw=1.5)
a1.plot([0.8, 0.8], [0.65, 0.5], color="#333333", lw=1.5)
a1.plot([0.1, 0.9], [0.5, 0.5], color="#333333", lw=2)
a1.add_patch(plt.Rectangle((0.25, 0.66), 0.14, 0.12, fc="#eaf2fb", ec="#1f5fa8"))
a1.add_patch(plt.Circle((0.5, 0.72), 0.06, fc="#fdecea", ec="#c0392b"))
a1.add_patch(plt.Rectangle((0.72, 0.66), 0.14, 0.12, fc="#eaf7ee", ec="#2e7d32"))
a1.text(0.5, 0.30, "导线只是连接：R、L、C 集中到元件上\n每个元件用一个代数式描述（全课程前提）",
        ha="center", fontsize=9)
a1.set_xlim(0, 1); a1.set_ylim(0, 1); a1.axis("off")
# 右：分布参数模型
a2.set_title("尺寸 ~ 波长（高频）：分布参数（传输线）", fontsize=11)
a2.plot([0.08, 0.92], [0.6, 0.6], color="#333333", lw=2)
a2.plot([0.08, 0.92], [0.45, 0.45], color="#333333", lw=2)
t = np.linspace(0.08, 0.92, 200)
a2.plot(t, 0.6 + 0.06 * np.sin((t - 0.08) / 0.84 * 4 * np.pi), color="#1f5fa8", lw=1.2)
a2.plot(t, 0.45 + 0.06 * np.sin((t - 0.08) / 0.84 * 4 * np.pi - 0.6), color="#c0392b", lw=1.2)
a2.text(0.5, 0.28, "导线本身也是元件：电压/电流沿导线不同\n波在传播，要解偏微分方程（传输线/电磁场）",
        ha="center", fontsize=9)
a2.set_xlim(0, 1); a2.set_ylim(0, 1); a2.axis("off")
plt.tight_layout()
save_stem = "lec26_fig3_boundary"
plt.savefig(os.path.join(FIGDIR, save_stem + ".svg"), transparent=False)
plt.savefig(os.path.join(FIGDIR, save_stem + ".png"), transparent=False, dpi=200)
plt.close(fig)
print("[OK] figures/%s.svg 与 .png 已生成。" % save_stem)

print()
print("[DONE] lec26-01 完成（课程收官）。")