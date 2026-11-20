"""第 14 讲验证脚本：真值判断 / if 匹配 / range 边界 / while 与 for / 循环 else / break 与 continue / 遍历时修改 / 迭代协议。

规模纪律：纯内存操作，目标 < 2 秒。
运行：uv run python tutorials/python/scripts/lec14-01_demo_control.py

讲义里引用的每一条输出都来自本脚本。
"""

WIDTH = 68


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def main() -> None:
    section("1. 真值判断：哪些东西算“假”")
    falsy = [0, 0.0, "", [], {}, set(), None, False]
    truthy = [1, -1, "0", " ", [0], {"a": 1}, True]
    print("  判为假的值：")
    for v in falsy:
        print(f"    {v!r:<10} bool -> {bool(v)}")
    print("  判为真的值：")
    for v in truthy:
        print(f"    {v!r:<10} bool -> {bool(v)}")
    print("  预期: 零、空字符串、空容器、None 为假；非空字符串 '0' 与 ' ' 都是真。")
    print("        所以“判断有没有输入”和“判断输入是不是 0”是两件事。\n")

    section("2. if / elif / else：只执行第一个成立的")
    def classify(n):
        if n < 0:
            return "负数"
        elif n == 0:
            return "零"
        elif n < 10:
            return "个位数"
        else:
            return "两位数及以上"

    for n in (-3, 0, 7, 42):
        print(f"    classify({n:>3}) = {classify(n)}")
    print("  预期: 从上往下匹配，命中一个就跳出整个 if 链，后面的 elif 不再判断。")
    print("        所以顺序很重要：把 n < 10 放到 n == 0 前面，0 会被判成“个位数”。\n")

    section("3. 条件表达式：一行版的 if")
    for n in (0, 5):
        label = "零点" if n == 0 else "非零"
        print(f"    n = {n} -> {label}")
    print("  预期: `A if 条件 else B` 是一个表达式，能直接赋值；嵌套过多就别用了。\n")

    section("4. while：条件为真就继续")
    count = 3
    while count > 0:
        print(f"    while 里: count = {count}")
        count -= 1
    print(f"    循环结束: count = {count}")
    print("  预期: 每轮都重新判断条件；count 必须真的变化，否则死循环（Ctrl+C 停）。\n")

    section("5. while ... else：没被 break 打断才执行")
    n = 0
    while n < 3:
        n += 1
    else:
        print(f"    自然结束（n={n}）-> else 执行了")
    n = 0
    while n < 3:
        n += 1
        if n == 2:
            break
    else:
        print("    这行不会打印")
    print("  预期: 循环“正常跑完”会执行 else；被 break 打断则不执行。")
    print("        else 的语义是“没有提前退出”，不是“否则”。\n")

    section("6. for 与 range：含头不含尾")
    print(f"    list(range(5))      = {list(range(5))}")
    print(f"    list(range(1, 6))   = {list(range(1, 6))}")
    print(f"    list(range(1, 10, 3)) = {list(range(1, 10, 3))}")
    print(f"    list(range(5, 0, -1)) = {list(range(5, 0, -1))}")
    print("  预期: range(5) 是 0..4，不含 5；三个参数依次是起点、终点（不含）、步长。")
    print("        for 只负责“逐个取出”，不负责计数与结束条件——那是 while 的工作。\n")

    section("7. for ... else：找得到就不执行 else")
    target = 7
    for x in [1, 3, 7, 9]:
        if x == target:
            print(f"    找到了 {target}，break")
            break
    else:
        print("    这行不会打印")
    target = 5
    for x in [1, 3, 7, 9]:
        if x == target:
            print(f"    找到了 {target}")
            break
    else:
        print(f"    没找到 {target} -> else 执行")
    print("  预期: 循环 else 最常用的场景就是“找东西，找不到才提示”。\n")

    section("8. break 与 continue")
    nums = [1, 2, 3, 4, 5]
    out_break = []
    for x in nums:
        if x == 3:
            break
        out_break.append(x)
    print(f"    x == 3 时 break   -> 收集到 {out_break}")
    out_continue = []
    for x in nums:
        if x == 3:
            continue
        out_continue.append(x)
    print(f"    x == 3 时 continue -> 收集到 {out_continue}")
    print("  预期: break 结束整个循环；continue 只跳过本轮剩余语句，继续下一轮。\n")

    section("9. enumerate 与 zip：要下标、要成对")
    names = ["alice", "bob"]
    for i, name in enumerate(names, start=1):
        print(f"    enumerate: {i} -> {name}")
    for name, score in zip(["alice", "bob"], [90, 75]):
        print(f"    zip: {name} = {score}")
    print("  预期: 要下标用 enumerate（别手写计数器）；要并行遍历两个序列用 zip。")
    print("        zip 以最短的序列为准，多出来的会被丢弃。\n")

    section("10. 遍历时修改列表：会漏掉元素（但症状很有欺骗性）")
    xs = [1, 2, 3, 4]
    removed = []
    for x in xs:
        if x % 2 == 0:
            xs.remove(x)
            removed.append(x)
    print(f"    删偶数: 实际删掉 {removed}，剩下 {xs}")
    print("    这一次看起来“删全了”，因为被跳过的是奇数 3——它本来就不该被删。\n")

    xs = [1, 2, 3, 4]
    removed = []
    for x in xs:
        if x < 3:
            xs.remove(x)
            removed.append(x)
    print(f"    删小于 3 的: 实际删掉 {removed}，剩下 {xs}")
    print("    真正的问题在这里：2 也是小于 3 的，却没被删——删 1 之后下标前移，2 被跳过了。\n")

    xs = [1, 2, 3, 4]
    kept = [x for x in xs if x >= 3]
    print(f"    用列表推导式重建: {kept}（原列表 {xs} 不变，需要时再赋值回去）")
    print("  预期: 删到前面元素后，后面的元素会往前滑一位，for 的下标却已加一，于是跳过。")
    print("        “跳过”本身是稳定的，但跳过的那个元素要不要删，决定了你看不出还是看得出错。")
    print("        靠得住的做法只有两种：先收集再删，或用推导式重建。\n")

    section("11. 嵌套循环：break 只跳出内层")
    pairs = []
    for i in range(3):
        for j in range(3):
            if j == 1:
                break
            pairs.append((i, j))
    print(f"    内层 j==1 时 break -> {pairs}")
    print("  预期: 外层照常跑完 3 轮，每轮内层只取到 j=0。要跳出两层得用标志位或函数返回。\n")

    section("12. 迭代协议：for 背后做了什么")
    it = iter([10, 20])
    print(f"    iter([10,20]) -> {it!r}")
    print(f"    next(it) = {next(it)}")
    print(f"    next(it) = {next(it)}")
    try:
        next(it)
    except StopIteration:
        print("    再 next -> StopIteration（for 就是靠它知道结束）")
    print("  预期: for 先调 iter() 拿迭代器，再反复 next()，遇到 StopIteration 结束。")
    print("        所以“能被 for 遍历”的东西叫可迭代对象；生成器只能遍历一次（第 16 讲）。")

    print("\n  提示: 判断该用 for 还是 while，看你要表达“逐个处理”还是“直到某个条件不成立”。")


if __name__ == "__main__":
    main()
