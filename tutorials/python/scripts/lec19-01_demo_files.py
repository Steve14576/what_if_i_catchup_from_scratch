"""第 19 讲验证脚本：open 参数 / 模式 / 默认编码 / with / pathlib / 大文件内存 / CSV / JSON / 二进制。

规模纪律：临时目录里造一个约 5 MB 的文本文件，三个读法各测一次内存，目标 < 10 秒。
运行：uv run python tutorials/python/scripts/lec19-01_demo_files.py

讲义里引用的每一条输出都来自本脚本。
"""

import csv
import io
import json
import locale
import os
import sys
import tempfile
import tracemalloc
from pathlib import Path

WIDTH = 70
CRLF = b"\r\n"
CRCRLF = b"\r\r\n"


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def human(n: int) -> str:
    if n >= 1024 * 1024:
        return f"{n / 1024 / 1024:.2f} MB"
    if n >= 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n} B"


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)

        section("1. 默认编码：不写 encoding 会发生什么")
        print(f"  locale.getpreferredencoding(False) = {locale.getpreferredencoding(False)!r}")
        print(f"  sys.getdefaultencoding()           = {sys.getdefaultencoding()!r}")
        print(f"  sys.getfilesystemencoding()        = {sys.getfilesystemencoding()!r}")

        cn = root / "cn.txt"
        cn.write_text("中文内容 abc\n", encoding="utf-8")
        print(f"  utf-8 文件字节数 = {cn.stat().st_size}")
        try:
            text = cn.read_text()  # 不指定 encoding
            print(f"  不指定 encoding 读: 成功, 内容={text.strip()!r}")
        except UnicodeDecodeError as exc:
            print(f"  不指定 encoding 读: UnicodeDecodeError -> {exc}")
        print(f"  显式 utf-8 读: {cn.read_text(encoding='utf-8').strip()!r}")

        cn2 = root / "cn2.txt"
        with open(cn2, "w") as f:  # 不指定 encoding
            f.write("中文内容 abc\n")
        print(f"  不指定 encoding 写: 字节数 = {cn2.stat().st_size}（utf-8 应为 {cn.stat().st_size}）")
        print("  预期: Windows 中文环境下默认是 GBK/cp936（每个汉字 2 字节），utf-8 是 3 字节。")

        section("2. 模式：w 清空、a 追加、x 独占、b 与 encoding 互斥")
        target = root / "mode.txt"
        target.write_text("0123456789" * 10, encoding="utf-8")
        print(f"  写入 100 字节后 size = {target.stat().st_size}")
        fh = open(target, "w", encoding="utf-8")
        print(f"  以 'w' 打开、未写之前 size = {target.stat().st_size}  ← 打开即清空")
        fh.write("new\n")
        fh.close()
        print(f"  写入 'new\\n' 后 size = {target.stat().st_size}")
        with open(target, "a", encoding="utf-8") as f:
            f.write("appended\n")
        print(f"  'a' 追加后内容 = {target.read_text(encoding='utf-8')!r}")

        exist = root / "exist.txt"
        exist.write_text("x", encoding="utf-8")
        try:
            open(exist, "x", encoding="utf-8")
        except FileExistsError as exc:
            print(f"  'x' 打已存在文件: FileExistsError -> {exc.strerror}")

        try:
            open(root / "bad.bin", "rb", encoding="utf-8")
        except ValueError as exc:
            print(f"  'rb' 同时给 encoding: ValueError -> {exc}")

        section("3. with 保证了什么")
        f = open(root / "handle.txt", "w", encoding="utf-8")
        print(f"  进入块之前 f.closed = {f.closed}")
        with f:
            f.write("hi\n")
            print(f"  块内 f.closed   = {f.closed}")
        print(f"  退出块之后 f.closed = {f.closed}")
        print("  预期: 不用 with 时，异常/提前 return 会让文件留在打开状态，缓冲内容可能没落盘。")

        section("4. pathlib：拼路径不依赖当前目录")
        proj = root / "proj"
        data_dir = proj / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        p = data_dir / "raw.csv"
        p.write_text("a,b\n1,2\n", encoding="utf-8")
        print(f"  cwd              = {Path.cwd()}")
        print(f"  拼出来的绝对路径 = {p}")
        print(f"  p.parent.name    = {p.parent.name}")
        print(f"  p.suffix / stem  = {p.suffix!r} / {p.stem!r}")
        print(f"  p.exists()       = {p.exists()}")
        print(f"  相对写法 data/raw.csv 的 resolve() = {Path('data/raw.csv').resolve()}")
        print("  预期: 相对路径以 cwd 为起点；脚本里写死相对路径，换目录运行就找不到。")

        section("5. 读大文件：三种写法的峰值内存")
        big = root / "big.txt"
        line = "2026-11-20 10:00:00 INFO 这是一行日志，用于测量内存占用\n"
        with open(big, "w", encoding="utf-8") as f:
            for _ in range(200_000):
                f.write(line)
        size = big.stat().st_size
        print(f"  文件大小 = {human(size)}，行数 = 200000")

        def peak_read_all() -> int:
            tracemalloc.start()
            with open(big, encoding="utf-8") as f:
                data = f.read()
            peak = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            assert len(data) > 0
            return peak

        def peak_readlines() -> int:
            tracemalloc.start()
            with open(big, encoding="utf-8") as f:
                rows = f.readlines()
            peak = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            assert len(rows) == 200_000
            return peak

        def peak_iter() -> int:
            tracemalloc.start()
            count = 0
            with open(big, encoding="utf-8") as f:
                for _line in f:
                    count += 1
            peak = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            assert count == 200_000
            return peak

        for name, fn in [("f.read()", peak_read_all), ("f.readlines()", peak_readlines),
                         ("for line in f", peak_iter)]:
            print(f"  {name:<16} 峰值 {human(fn())}")
        print("  预期: 前两种把整份内容搬进内存；逐行迭代只保留一行。")

        section("6. CSV：newline='' 为什么必须写")
        rows = [["name", "score"], ["张三", "90"], ["李四", "85"]]
        no_nl = root / "no_newline.csv"
        with no_nl.open("w", encoding="utf-8") as f:
            csv.writer(f).writerows(rows)
        with_nl = root / "with_newline.csv"
        with with_nl.open("w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerows(rows)
        no_bytes = no_nl.read_bytes()
        nl_bytes = with_nl.read_bytes()
        print(f"  不写 newline: 字节 {len(no_bytes)}，CRLF {no_bytes.count(CRLF)} 个，"
              f"CR+CRLF {no_bytes.count(CRCRLF)} 个，首句 {no_bytes.split(CRLF)[0]!r}")
        print(f"  写 newline  : 字节 {len(nl_bytes)}，CRLF {nl_bytes.count(CRLF)} 个，"
              f"CR+CRLF {nl_bytes.count(CRCRLF)} 个，首句 {nl_bytes.split(CRLF)[0]!r}")
        print("  预期: newline='' 时每行一个 \\r\\n；不写时行尾变 \\r\\r\\n，"
              "多出的 \\r 在 Excel 等工具里表现为空行。")

        with with_nl.open(encoding="utf-8", newline="") as f:
            back = list(csv.DictReader(f))
        print(f"  DictReader 读回 {len(back)} 行，第一行 = {back[0]}")

        section("7. JSON：ensure_ascii 与编码")
        payload = {"name": "张三", "scores": [90, 85], "note": "中文注释"}
        ascii_out = json.dumps(payload, ensure_ascii=True)
        utf8_out = json.dumps(payload, ensure_ascii=False)
        print(f"  ensure_ascii=True  字符数 {len(ascii_out)}: {ascii_out[:44]}...")
        print(f"  ensure_ascii=False 字符数 {len(utf8_out)}: {utf8_out[:44]}...")
        jp = root / "data.json"
        jp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        loaded = json.loads(jp.read_text(encoding="utf-8"))
        print(f"  写盘再读回: {loaded}")
        print(f"  写盘字节数（utf-8, 不转义）= {jp.stat().st_size}")

        section("8. 文本与二进制：b 模式拿到的是字节")
        raw = cn.read_bytes()
        print(f"  read_bytes() 前 12 字节 = {raw[:12]}")
        print(f"  len(bytes) = {len(raw)}，解码后 len(str) = {len(raw.decode('utf-8'))}")
        with open(cn, "rb") as f:
            head = f.read(6)
        print(f"  'rb' 读 6 字节 = {head}  ← 可能切在汉字中间")
        print("  预期: 文本模式解码、二进制模式不做任何解码；二进制读中文要自己 decode。")

        section("9. 一行的结尾到底是什么")
        mixed = root / "mixed.txt"
        mixed.write_bytes("第一行\n第二行\r\n第三行\n".encode("utf-8"))
        with open(mixed, encoding="utf-8") as f:
            default_lines = f.read().splitlines()
        with open(mixed, encoding="utf-8", newline="") as f:
            raw_newline = f.read()
        print(f"  默认模式 splitlines 得 {len(default_lines)} 行: {default_lines}")
        print(f"  newline='' 原样读到的 repr = {raw_newline!r}")
        print("  预期: 默认的 universal newlines 会把 \\r\\n 归一成 \\n；newline='' 才看得见原貌。")

        os.remove(big)
        print("\n  提示: 交付脚本里，open 永远写 encoding='utf-8'；处理 CSV 永远写 newline=''。")


if __name__ == "__main__":
    main()
