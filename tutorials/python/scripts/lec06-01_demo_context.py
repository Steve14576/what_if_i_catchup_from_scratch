"""第 06 讲验证脚本：上下文预算的算术（字符 / token 量级 / 窗口占比 / 截断损失）。

规模纪律：只读本课程几个 md 文件，目标 < 2 秒。
运行：uv run python tutorials/python/scripts/lec06-01_demo_context.py

口径声明（重要）：
  1. 字符数、字节数是实测值；
  2. token 数是**量级估计**：按"中文字符 ×1.5 + 其余字符 ÷4"折算，
     不同分词器的真实差异可达两倍，要精确值必须用对应模型的 tokenizer；
  3. 本脚本不调用任何模型，不做模型行为实验。
"""

import unicodedata
from pathlib import Path

WIDTH = 68
COURSE = Path(__file__).resolve().parents[1]
WINDOWS = {"8k": 8_000, "32k": 32_000, "200k": 200_000}


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def split_chars(text: str) -> tuple[int, int, int]:
    """返回（总字符数，中日韩字符数，其余字符数）。"""
    cjk = sum(1 for ch in text if unicodedata.east_asian_width(ch) in ("W", "F"))
    return len(text), cjk, len(text) - cjk


def estimate_tokens(text: str) -> float:
    """按经验系数折算 token 数；只用于量级判断。"""
    total, cjk, other = split_chars(text)
    return cjk * 1.5 + other / 4


def main() -> None:
    section("1. 同一段内容，四种“长度”不是一回事")
    zh = "今天下午三点在小会议室开会，讨论下周的排课和实验安排。"
    en = "We will meet at 3 pm in the small meeting room to discuss next week's schedule."
    code = "def add(a, b):\n    return a + b\n"

    print(f"{'样本':<10}{'字符':>6}{'CJK':>6}{'其余':>6}{'字节':>7}{'token(估)':>12}")
    for name, text in (("中文句", zh), ("英文句", en), ("两行代码", code)):
        total, cjk, other = split_chars(text)
        print(f"{name:<10}{total:>6}{cjk:>6}{other:>6}"
              f"{len(text.encode('utf-8')):>7}{estimate_tokens(text):>12.1f}")

    print("\n  预期: 中文句 27 个字符，按经验系数折出约 40 token；")
    print("        英文 80 个字符却只有约 20 token —— 英文每个 token 平均装 4 个字符，")
    print("        中文每个字往往占 1 到 2 个 token。所以“多少字”不能直接当“多少 token”。\n")

    section("2. 本课程各讲的体量：换算成 token 大致多少")
    files = sorted(p for p in COURSE.glob("*.md") if p.name[:2].isdigit())
    print(f"{'文件':<26}{'字符':>8}{'token(估)':>11}{'占 8k':>8}{'占 32k':>8}{'占 200k':>9}")
    for path in files:
        text = path.read_text(encoding="utf-8")
        total, _, _ = split_chars(text)
        tokens = estimate_tokens(text)
        print(f"{path.name[:24]:<26}{total:>8}{tokens:>11.0f}"
              f"{tokens / WINDOWS['8k'] * 100:>7.0f}%{tokens / WINDOWS['32k'] * 100:>7.0f}%"
              f"{tokens / WINDOWS['200k'] * 100:>8.1f}%")

    print("\n  预期: 一讲约 1 万 token，占 32k 窗口三分之一上下；")
    print("        三讲就连同提示词一起超过 32k。这就是“把整个项目贴进去”很快超预算的原因。\n")

    section("3. 截断的算术：只保留最后一段，会丢掉什么")
    big = COURSE / "01_一台机器到底在跑什么.md"
    text = big.read_text(encoding="utf-8")
    keep = 4000
    kept = text[-keep:]
    dropped = text[:-keep]

    def first_sentence(block: str) -> str:
        for line in block.splitlines():
            line = line.strip()
            if line and not line.startswith(("#", ">", "|", "```")):
                return line[:40]
        return "(没有正文行)"

    print(f"  原文: {big.name}")
    print(f"  总字符 {len(text)}，只保留最后 {keep} 字符")
    print(f"  被丢掉的比例 = {len(dropped) / len(text) * 100:.1f}%")
    print(f"  被丢掉部分的第一句: {first_sentence(dropped)}…")
    print(f"  被保留部分的第一句: {first_sentence(kept)}…")
    print("\n  预期: 丢掉的是一整讲的开头（前置、本讲回答、第 0 节）。")
    print("        如果你只贴“最后一段代码”，它连这讲要解决什么问题都不知道——")
    print("        这正是“贴太少”与“贴太多”之间的同一个问题：预算要花在“目标与约束”上。\n")

    section("4. 一份请求的信息要素检查（人工标注，不是模型测的）")
    vague = "帮我看看这段代码为什么报错"
    clear = ("运行 python main.py 报 FileNotFoundError: 'scores.csv'（完整报错已附）。"
             "文件在 data/scores.csv，我从项目根目录运行。"
             "请只改路径构造，不要改函数签名。验收：从项目根运行输出 120。")

    checks = [
        ("目标（要什么结果）", "改到不报错", "从项目根运行能读到 data/scores.csv"),
        ("现状（错在哪、环境）", "未说明", "报错原文 + 文件位置 + 运行目录"),
        ("约束（不能动什么）", "未说明", "不改函数签名"),
        ("验收（怎么算完成）", "未说明", "输出 120"),
    ]
    print(f"{'要素':<22}{'模糊请求':<16}{'四要素请求'}")
    for name, a, b in checks:
        print(f"{name:<22}{a:<16}{b}")

    print(f"\n  长度对比: 模糊 {len(vague)} 字 / 四要素 {len(clear)} 字")
    print("  预期: 多写几十个字，换来的是四个可判定项；这几十个字的 token 花得最值。")


if __name__ == "__main__":
    main()
