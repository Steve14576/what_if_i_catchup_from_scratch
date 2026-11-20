"""第 12 讲验证脚本：列表增删改查 / sort 与 sorted / 切片是拷贝 / 浅拷贝与别名 / 元组 / 可变陷阱。

规模纪律：纯内存操作，目标 < 2 秒。
运行：uv run python tutorials/python/scripts/lec12-01_demo_sequences.py

讲义里引用的每一条输出都来自本脚本。
"""

import copy

WIDTH = 68


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def main() -> None:
    section("1. 列表：有顺序、可修改、可混装")
    xs = [3, 1, 2]
    print(f"  xs = {xs}   len = {len(xs)}   第一个 = {xs[0]}   最后一个 = {xs[-1]}")
    print(f"  切片 xs[:2] = {xs[:2]}（与字符串规则相同：含起点不含终点）")
    mixed = [1, "two", 3.0, True, None]
    print(f"  可混装不同类型: {mixed}")
    print("  预期: 列表用方括号，元素之间逗号分隔；索引与切片规则和字符串一致。\n")

    section("2. 增删改查：方法都作用在原列表上")
    xs = [3, 1, 2]
    xs.append(9)
    print(f"  append(9)        -> {xs}")
    xs.extend([7, 8])
    print(f"  extend([7, 8])   -> {xs}")
    xs.insert(0, 100)
    print(f"  insert(0, 100)   -> {xs}")
    popped = xs.pop()
    print(f"  pop()            -> 返回 {popped}，剩下 {xs}")
    xs.remove(100)
    print(f"  remove(100)      -> {xs}")
    print(f"  index(1) = {xs.index(1)}   count(1) = {xs.count(1)}")
    print("  预期: 这些方法都“直接改原列表”，返回值多半是 None 或被删掉的元素；")
    print("        与字符串方法（返回新对象）完全相反，这一点最容易混。\n")

    section("3. sort() 返回 None，sorted() 返回新列表")
    xs = [3, 1, 2]
    result = xs.sort()
    print(f"  xs.sort() 的返回值 = {result}；sort 之后 xs = {xs}")
    ys = sorted([3, 1, 2])
    print(f"  sorted([3,1,2]) = {ys}")
    print("  预期: xs.sort() 原地排序、返回 None；写成 xs = xs.sort() 会把列表弄丢。\n")

    section("4. 切片是拷贝：改副本不影响原列表")
    a = [1, 2, 3]
    b = a[:]
    b.append(4)
    print(f"  a = {a}   b = a[:] 后 b.append(4) -> b = {b}")
    print(f"  a 变了吗 = {a}   是同一个对象吗 = {a is b}")
    print("  预期: 切片产生新列表；这是最常用的“浅复制”写法。\n")

    section("5. 别名：不切片直接赋值，两个名字共用一个列表")
    a = [1, 2, 3]
    c = a
    c.append(4)
    print(f"  a = [1,2,3]; c = a; c.append(4)")
    print(f"  -> a = {a}   c = {c}   是同一个对象吗 = {a is c}")
    print("  预期: 改 c 就是改 a，因为它们是同一个列表的两张标签（第 09 讲）。\n")

    section("6. 浅拷贝的边界：只复制第一层")
    nested = [[1, 2], [3, 4]]
    shallow = nested[:]
    shallow[0].append(99)
    print(f"  nested = {nested}")
    print(f"  shallow = nested[:] 后 shallow[0].append(99)")
    print(f"  -> nested = {nested}（外层没换，但内层被改了）")
    print(f"  外层是同一个对象吗 = {nested is shallow}；内层是同一个对象吗 = {nested[0] is shallow[0]}")
    deep = copy.deepcopy(nested)
    deep[0].append(1000)
    print(f"  deepcopy 之后改 deep[0] -> nested = {nested}   deep = {deep}")
    print("  预期: 浅拷贝只复制第一层，嵌套的可变对象仍共享；要彻底独立用 deepcopy。\n")

    section("7. 一个经典坑：[[0] * 2] * 3 共享内层")
    grid = [[0] * 2] * 3
    grid[0][0] = 1
    print(f"  grid = [[0]*2]*3; grid[0][0] = 1")
    print(f"  -> {grid}")
    print(f"  三行是同一个内层吗 = {grid[0] is grid[1] is grid[2]}")
    safe = [[0] * 2 for _ in range(3)]
    safe[0][0] = 1
    print(f"  用推导式重建: {safe}")
    print("  预期: `*` 复制的是“引用”，三行指向同一个内层列表；")
    print("        要独立的内层，用列表推导式逐行新建（推导式第 14 讲正式讲）。\n")

    section("8. 元组：不可变，但可以装可变的东西")
    point = (3, 5)
    print(f"  point = {point}   point[0] = {point[0]}   len = {len(point)}")
    single = (7,)
    not_tuple = (7)
    print(f"  单元素元组 (7,) 的类型 = {type(single).__name__}；写 (7) 的类型 = {type(not_tuple).__name__}")
    x, y = point
    print(f"  解包: x = {x}, y = {y}")
    try:
        point[0] = 9
    except TypeError as exc:
        print(f"  point[0] = 9 -> TypeError: {exc}")
    holder = ([1, 2], "tag")
    holder[0].append(3)
    print(f"  元组里放列表，改列表是允许的: {holder}")
    print("  预期: 元组本身不可改（不能换元素），但如果元素可变，元素内部仍可改；")
    print("        “不可变”说的是元组这一层的绑定，不是里面所有东西。\n")

    section("9. 为什么元组能当字典的键，列表不能")
    print(f"  hash((1, 2)) = {hash((1, 2))}")
    try:
        hash([1, 2])
    except TypeError as exc:
        print(f"  hash([1, 2]) -> TypeError: {exc}")
    print("  预期: 只有“可哈希”的对象能当键；可变对象不可哈希。")
    print("        字典与集合第 13 讲正式讲，这里先建立“可哈希 = 不可变带来的能力”这个印象。\n")

    section("10. 通用操作：len / in / sum / max / min / 拼接")
    nums = [4, 1, 7]
    print(f"  nums = {nums}   len={len(nums)}   sum={sum(nums)}   max={max(nums)}   min={min(nums)}")
    print(f"  7 in nums = {7 in nums}   9 in nums = {9 in nums}")
    print(f"  [1, 2] + [3] = {[1, 2] + [3]}   [0] * 3 = {[0] * 3}")
    print("  预期: 这些是序列通用操作，字符串与元组也支持 len / in / + / *。")

    print("\n  提示: 判断“该用列表还是元组”，先问一句“这些元素以后还要不要改”。")


if __name__ == "__main__":
    main()
