"""第 11 讲验证脚本：字面量 / 索引 / 切片 / 不可变 / 方法 / f-string / 编码 / 日志切分。

规模纪律：纯内存操作，目标 < 2 秒。
运行：uv run python tutorials/python/scripts/lec11-01_demo_strings.py

讲义里引用的每一条输出都来自本脚本。
"""

WIDTH = 68


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def main() -> None:
    section("1. 四种写法的同一段文本")
    print("  双引号: " + "他说\"你好\"")
    print("  单引号内用双引号: " + '他说"你好"')
    print("  转义换行: " + "第一行\n第二行".replace("\n", "\\n"))
    tab = "a\tb"
    print(f"  制表符 \\t: {tab!r}")
    print("  raw 字符串 r\"a\\nb\": " + repr(r"a\nb"))
    print("  三引号可以跨行:")
    multi = """第一行
第二行"""
    print("    " + multi.replace("\n", "\n    "))
    print("  预期: 引号选择只是写法；反斜杠转义在普通字符串里生效，r\"...\" 里不生效；")
    print("        三引号保留换行，适合写多行文本与文档字符串。\n")

    section("2. 索引：从 0 开始，负数从尾部数")
    s = "python"
    print(f"  s = {s!r}   len(s) = {len(s)}")
    print(f"  s[0] = {s[0]!r}   s[3] = {s[3]!r}   s[-1] = {s[-1]!r}   s[-2] = {s[-2]!r}")
    print("  预期: 索引范围是 0..len-1 或 -len..-1；s[len(s)] 越界。\n")

    try:
        _ = s[100]
    except IndexError as exc:
        print(f"  s[100] -> IndexError: {exc}")
    print("  预期: 单点索引越界会报 IndexError，不会给你一个“空字符”。\n")

    section("3. 切片：三个数字，缺省与越界都安全")
    s = "0123456789"
    cases = [
        ("s[2:5]", s[2:5]),
        ("s[:3]", s[:3]),
        ("s[7:]", s[7:]),
        ("s[:]", s[:]),
        ("s[::2]", s[::2]),
        ("s[::-1]", s[::-1]),
        ("s[1:100]", s[1:100]),
        ("s[100:200]", s[100:200]),
        ("s[5:2]", s[5:2]),
    ]
    print(f"  s = {s!r}")
    for expr, value in cases:
        print(f"  {expr:<12} = {value!r}")
    print("  预期: 切片越界不报错，只截到有的部分；起点大于终点得到空串；")
    print("        step 为负时反向取，常用 s[::-1] 反转字符串。\n")

    section("4. 字符串不可变：改不了，只能新建")
    try:
        s = "python"
        s[0] = "P"
    except TypeError as exc:
        print(f"  s[0] = 'P' -> TypeError: {exc}")
    s = "python"
    upper = "P" + s[1:]
    print(f"  用拼接新建: {'P' + s[1:]!r}，原字符串仍是 {s!r}")
    print("  预期: 字符串对象本身不可改；所有“修改”操作都返回新对象。")
    print("        这意味着循环里反复拼接会不断产生新对象（第 23 讲性能会再提）。\n")

    section("5. 方法：一次看清常用八个")
    raw = "  Alice, Bob , Carol  "
    print(f"  raw = {raw!r}")
    print(f"  strip()          -> {raw.strip()!r}")
    print(f"  split(',')       -> {raw.strip().split(',')!r}")
    print(f"  split(',') 后再 strip 每项 -> {[x.strip() for x in raw.strip().split(',')]!r}")
    print(f"  'a,b,c'.split(',') -> {'a,b,c'.split(',')!r}")
    print(f"  '-'.join(['a','b','c']) -> {'-'.join(['a', 'b', 'c'])!r}")
    print(f"  'abcabc'.replace('a','X') -> {'abcabc'.replace('a', 'X')!r}")
    print(f"  'abcabc'.find('ca')       -> {'abcabc'.find('ca')}")
    print(f"  'abcabc'.count('a')       -> {'abcabc'.count('a')}")
    print(f"  'log.txt'.endswith('.txt') -> {'log.txt'.endswith('.txt')}")
    print("  预期: 多数方法是“返回新字符串”，原字符串不变；split 与 join 互为逆操作。\n")

    joined = ",".join("a,b,c".split(","))
    print(f"  ','.join('a,b,c'.split(',')) == 'a,b,c' ? {joined == 'a,b,c'}")
    print("  预期: True。记住这个对称性，解析与重组就都有了方向。\n")

    section("6. f-string：把值嵌进文本，还能控制格式")
    name = "小明"
    score = 87.456
    count = 1234567
    ratio = 0.8734
    print(f"  直接嵌入: f'{{name}}' -> {f'{name}'}")
    print(f"  两位小数: {score:.2f}")
    print(f"  宽度 8 右对齐: {name:>8}|")
    print(f"  宽度 10 居中: {name:^10}|")
    print(f"  千分位: {count:,}")
    print(f"  百分比一位: {ratio:.1%}")
    print(f"  调试写法 score=: {score=}")
    print("  预期: 冒号后面是格式说明符：.2f 小数位、> / ^ 对齐、, 千分位、.1% 百分比。")
    print("        `{expr=}` 会连同表达式一起打印，调试时很省事。\n")

    section("7. 编码：字符串是字符，字节是字节")
    text = "中文a"
    utf8 = text.encode("utf-8")
    gbk = text.encode("gbk")
    print(f"  text = {text!r}   len(text) = {len(text)}（字符数）")
    print(f"  utf-8 字节 = {utf8}   长度 = {len(utf8)}")
    print(f"  gbk   字节 = {gbk}   长度 = {len(gbk)}")
    print(f"  utf-8 解回来 -> {utf8.decode('utf-8')!r}")
    try:
        utf8.decode("gbk")
    except UnicodeDecodeError as exc:
        print(f"  用错编码解码 -> UnicodeDecodeError: {str(exc)[:60]}...")
    print("  预期: 同一个字符串在不同编码下字节数不同；用错编码解码会报错或乱码。")
    print("        读文件时永远显式写 encoding='utf-8'（第 19 讲）。\n")

    section("8. 实战：把一行日志切成四个字段")
    line = "2026-11-14 09:30:12 ERROR 连接超时"
    print(f"  原文: {line}\n")

    wrong = line.split(" ", 2)
    print(f"  先看一种错切法 split(' ', 2): {wrong!r}")
    print("  问题: 只切两刀，得到三段，级别与消息粘在第三段里 —— 字段数数错就会乱。\n")

    right = line.split(" ", 3)
    print(f"  正确切法 split(' ', 3): {right!r}")
    date_part, time_part, level, message = right
    print(f"  日期 = {date_part!r}  时刻 = {time_part!r}")
    print(f"  级别 = {level!r}    消息 = {message!r}")
    print(f"  取小时: time_part[:2] = {time_part[:2]!r}")
    print("  预期: split(sep, maxsplit) 限制切几次，后面的原样保留 —— 所以 maxsplit")
    print("        要比字段数少 1；字段数拿不准时先 print 出来数一数。")

    print(f"\n  提示: len('中文') = {len('中文')} 这是字符数，不是字节数；字节数要用 encode 之后再看。")


if __name__ == "__main__":
    main()
