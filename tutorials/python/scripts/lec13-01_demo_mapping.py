"""第 13 讲验证脚本：字典增删改查 / 遍历 / get 与 setdefault / 词频 / 集合运算 / 查找速度对比。

规模纪律：查找对比用 1e3–1e5 三个规模，每个跑 3 次取中位数，目标 < 10 秒。
运行：uv run python tutorials/python/scripts/lec13-01_demo_mapping.py

讲义里引用的每一条输出与耗时都来自本脚本。
"""

import time
from collections import Counter, defaultdict

WIDTH = 68


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def median_ms(fn, repeat: int = 3) -> float:
    times = []
    for _ in range(repeat):
        t0 = time.perf_counter()
        fn()
        times.append((time.perf_counter() - t0) * 1000)
    times.sort()
    return times[len(times) // 2]


def main() -> None:
    section("1. 字典：按键取值，键不存在会报错")
    scores = {"alice": 90, "bob": 75}
    print(f"  scores = {scores}")
    print(f"  scores['alice'] = {scores['alice']}")
    try:
        _ = scores["carol"]
    except KeyError as exc:
        print(f"  scores['carol'] -> KeyError: {exc}")
    print(f"  scores.get('carol')      = {scores.get('carol')}")
    print(f"  scores.get('carol', 0)   = {scores.get('carol', 0)}")
    print("  预期: [] 取不到就报 KeyError；get 取不到给 None 或你指定的默认值。\n")

    section("2. 增删改：一把键就是定位条件")
    scores["carol"] = 88
    print(f"  scores['carol'] = 88  -> {scores}")
    scores["bob"] = 80
    print(f"  scores['bob'] = 80    -> {scores}（覆盖旧值）")
    removed = scores.pop("bob")
    print(f"  scores.pop('bob')     -> 返回 {removed}，剩下 {scores}")
    scores.update({"dave": 60, "alice": 95})
    print(f"  update({{...}})        -> {scores}")
    print(f"  'alice' in scores = {'alice' in scores}   'bob' in scores = {'bob' in scores}")
    print("  预期: 赋值即新增或覆盖；pop 按键删并返回；update 批量合并；in 查的是键不是值。\n")

    section("3. 遍历：keys / values / items，顺序是插入序")
    scores = {"alice": 90, "bob": 75, "carol": 88}
    print(f"  keys()   -> {list(scores.keys())}")
    print(f"  values() -> {list(scores.values())}")
    print(f"  items()  -> {list(scores.items())}")
    for name, score in scores.items():
        print(f"    遍历 items: {name} -> {score}")
    print("  预期: 顺序与插入顺序一致（3.7 起的保证），但不是按字母排序；")
    print("        想排序就 sorted(scores.items())（第 12 讲的 sorted）。\n")

    section("4. 遍历时修改：会直接报错")
    d = {"a": 1, "b": 2, "c": 3}
    try:
        for key in d:
            if key == "b":
                del d[key]
    except RuntimeError as exc:
        print(f"  边遍历边删 -> RuntimeError: {exc}")
    d = {"a": 1, "b": 2, "c": 3}
    for key in list(d):
        if key == "b":
            del d[key]
    print(f"  先 list(d) 复制键再删 -> {d}")
    print("  预期: 遍历中改变字典大小会抛 RuntimeError；绕法是先复制键列表再遍历。\n")

    section("5. setdefault 与 defaultdict：给缺失的键设默认值")
    counts = {}
    for word in ["a", "b", "a", "c", "a"]:
        counts[word] = counts.get(word, 0) + 1
    print(f"  用 get 计数      -> {counts}")

    counts2 = {}
    for word in ["a", "b", "a", "c", "a"]:
        counts2.setdefault(word, 0)
        counts2[word] += 1
    print(f"  用 setdefault    -> {counts2}")

    dd = defaultdict(list)
    for word, line in [("a", 1), ("b", 2), ("a", 3)]:
        dd[word].append(line)
    print(f"  defaultdict(list) -> {dict(dd)}")

    counter = Counter(["a", "b", "a", "c", "a"])
    print(f"  Counter           -> {dict(counter)}   most_common(1) = {counter.most_common(1)}")
    print("  预期: 四种写法都能做词频；get 最好懂，setdefault 少一次查表，")
    print("        defaultdict 适合“值是列表/字典”的累加，Counter 一行搞定计数。\n")

    section("6. 集合：去重与集合运算")
    nums = [3, 1, 3, 2, 1]
    unique = set(nums)
    print(f"  set([3,1,3,2,1]) = {unique}（无序，打印顺序不保证）")
    a = {1, 2, 3, 4}
    b = {3, 4, 5}
    print(f"  a = {a}   b = {b}")
    print(f"  a | b（并） = {a | b}")
    print(f"  a & b（交） = {a & b}")
    print(f"  a - b（差） = {a - b}")
    print(f"  a ^ b（对称差） = {a ^ b}")
    print(f"  {{1,2}}.issubset(a) = {{1, 2}}.issubset(a)")
    print("  预期: 集合自动去重、元素无序、支持并交差；判断“是否子集”用 issubset。\n")

    section("7. 为什么字典与集合“快”：三种容器的成员判断对比")
    sizes = [1_000, 10_000, 100_000]
    print(f"{'规模':>8}{'列表 in (us)':>16}{'集合 in (us)':>16}{'字典 in (us)':>16}")
    for n in sizes:
        data_list = list(range(n))
        data_set = set(range(n))
        data_dict = {i: None for i in range(n)}
        target = n - 1                       # 最坏情况：在末尾
        repeats = max(2, 200_000 // n)       # 小规模多跑几次，放大信号
        # median_ms 返回“总耗时（毫秒）”，除以轮数得到单次毫秒，再乘 1000 得到单次微秒
        list_us = median_ms(lambda: [target in data_list for _ in range(repeats)]) / repeats * 1000
        set_us = median_ms(lambda: [target in data_set for _ in range(repeats)]) / repeats * 1000
        dict_us = median_ms(lambda: [target in data_dict for _ in range(repeats)]) / repeats * 1000
        print(f"{n:>8}{list_us:>16.3f}{set_us:>16.3f}{dict_us:>16.3f}")
    print("  单位说明: 上表是“单次判断”的微秒数（us），由多轮总耗时除以轮数得到。")
    print("  预期: 列表随规模线性增长；集合与字典基本不随规模变化（哈希定位）。")
    print("        所以“在不在”的判断，数据一多就该换集合或字典。\n")

    section("8. 键必须可哈希：元组可以，列表不行")
    coords = {(0, 0): "原点", (1, 2): "点 A"}
    print(f"  {{(0,0): '原点'}} 可以，取值 = {coords[(0, 0)]}")
    try:
        bad = {[0, 0]: "原点"}
    except TypeError as exc:
        print(f"  用列表当键 -> TypeError: {exc}")
    print("  预期: 键必须可哈希（第 12 讲）；元组不可变所以可以，列表可变所以不行。\n")

    section("9. 合并与嵌套取值")
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 20, "c": 30}
    print(f"  d1 | d2 = {d1 | d2}（右边覆盖左边）")
    nested = {"alice": {"math": 90, "physics": 85}}
    print(f"  嵌套: nested['alice']['math'] = {nested['alice']['math']}")
    print(f"  嵌套缺失键: nested.get('bob', {{}}).get('math', '无记录') = "
          f"{nested.get('bob', {}).get('math', '无记录')}")
    print("  预期: | 合并字典（3.9+）；嵌套取值要一层层取，缺失时用 get 给默认值更安全。")


if __name__ == "__main__":
    main()
