"""第 16 讲验证脚本：函数当值 / lambda / map 与 filter / 闭包 / 装饰器 / 递归 / 生成器。

规模纪律：递归只跑到能看出差异的规模，目标 < 3 秒。
运行：uv run python tutorials/python/scripts/lec16-01_demo_functional.py

讲义里引用的每一条输出都来自本脚本。
"""

import functools
import sys
import time

WIDTH = 68


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"    [{func.__name__}] 耗时 {time.perf_counter() - t0:.6f} 秒")
        return result
    return wrapper


@timer
def slow_sum(n):
    return sum(range(n))


def make_counter():
    count = 0

    def bump():
        nonlocal count
        count += 1
        return count

    return bump


def make_counters_buggy():
    funcs = []
    for i in range(3):
        funcs.append(lambda: i)
    return funcs


def make_counters_fixed():
    funcs = []
    for i in range(3):
        funcs.append(lambda i=i: i)
    return funcs


def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


@functools.lru_cache(maxsize=None)
def fib_memo(n):
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


def fib_naive(n):
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def countdown(n):
    while n > 0:
        yield n
        n -= 1


def main() -> None:
    section("1. 函数是值：可以当参数传")
    words = ["Banana", "apple", "Cherry"]
    print(f"  sorted(words)               = {sorted(words)}")
    print(f"  sorted(words, key=len)      = {sorted(words, key=len)}")
    print(f"  sorted(words, key=str.lower) = {sorted(words, key=str.lower)}")
    rows = [("alice", 90), ("bob", 95), ("carol", 90)]
    print(f"  按分数降序、同分按名字升序 = {sorted(rows, key=lambda r: (-r[1], r[0]))}")
    print("  预期: key 收一个函数，排序时对每个元素先调用它；返回值只用于比较。")
    print("        多个字段就用元组：先按第一项，相同再按第二项。\n")

    section("2. lambda：只能写一个表达式")
    double = lambda x: x * 2
    print(f"  lambda x: x * 2   -> double(5) = {double(5)}")
    print(f"  double.__name__ = {double.__name__!r}")
    try:
        exec("f = lambda x: x = 1", {})
    except SyntaxError as exc:
        print(f"  lambda 里写赋值 -> SyntaxError: {exc.msg}")
    print("  预期: lambda 是“没有名字的短函数”，体只能是表达式；赋值、print 这类语句不能写。")
    print("        超过一行的逻辑，老老实实写 def。\n")

    section("3. map 与 filter 返回迭代器，只能遍历一次")
    nums = [1, 2, 3, 4]
    mapped = map(lambda x: x * 10, nums)
    print(f"  map 第一次遍历: {list(mapped)}")
    print(f"  map 第二次遍历: {list(mapped)}")
    filtered = filter(lambda x: x % 2 == 0, nums)
    print(f"  filter 结果: {list(filtered)}")
    print(f"  用推导式做同一件事: {[x * 10 for x in nums]}")
    print("  预期: map/filter 产出的是“值一次就没了”的迭代器；第二遍是空。")
    print("        日常优先用列表推导式，它更直接、可重复使用（第 14 讲）。\n")

    section("4. 闭包：捕获的是变量，不是当时的值")
    counter = make_counter()
    print(f"  第一次调用 {counter()}，第二次 {counter()}，第三次 {counter()}")
    buggy = make_counters_buggy()
    fixed = make_counters_fixed()
    print(f"  循环里造三个 lambda（buggy）= {[f() for f in buggy]}")
    print(f"  用默认参数固定住 i      = {[f() for f in fixed]}")
    print("  预期: 闭包记的是“变量 i 本身”，循环结束后 i 已经是 2，所以三个都返回 2；")
    print("        用 i=i 把当时的值当成默认参数存下来，三个才是 0/1/2。\n")

    section("5. 装饰器：把一个函数换成另一个函数")
    def plain():
        return "原函数"

    def loud(func):
        def wrapper():
            return "【" + func() + "】"
        return wrapper

    wrapped = loud(plain)
    print(f"  loud(plain)() = {wrapped()}")
    print(f"  原函数还在吗 = {plain()}")
    print(f"  没加 wraps 时 __name__ = {wrapped.__name__!r}")
    print("  预期: 装饰器就是“收一个函数、返回一个新函数”；@ 只是把 wrapped = loud(plain) 写成一行。\n")

    result = slow_sum(1_000_000)
    print(f"  @timer 装饰后的 slow_sum(1e6) = {result}")
    print(f"  装饰后 __name__ = {slow_sum.__name__!r}（functools.wraps 保住了原名）")
    print("  预期: 装饰器能在不改原函数代码的前提下加“计时/日志/重试”等外层行为。\n")

    section("6. 递归：要有终止条件，也有深度上限")
    print(f"  factorial(5) = {factorial(5)}")
    for n in (20, 25, 30):
        t0 = time.perf_counter()
        v = fib_naive(n)
        parts = time.perf_counter() - t0
        print(f"  fib_naive({n}) = {v}  耗时 {parts:.4f} 秒")
    print(f"  fib_memo(30) = {fib_memo(30)}（带 lru_cache）")
    print(f"  递归上限 sys.getrecursionlimit() = {sys.getrecursionlimit()}")

    def dive(n):
        return dive(n + 1)

    try:
        dive(0)
    except RecursionError as exc:
        print(f"  无限递归 -> RecursionError: {exc}")
    print("  预期: 递归写法干净，但重复子问题会指数级变慢（fib 三个规模可见）；")
    print("        缓存能救重复计算；递归层数超过上限会抛 RecursionError。\n")

    section("7. 生成器：用 yield 产出，一次一个")
    gen = countdown(3)
    print(f"  第一次遍历: {list(gen)}")
    print(f"  第二次遍历: {list(gen)}")
    big_list = [x for x in range(100_000)]
    big_gen = (x for x in range(100_000))
    print(f"  10 万个元素的列表占内存？用 sys.getsizeof 看结构体：")
    print(f"    list  = {sys.getsizeof(big_list)} 字节（元素另算）")
    print(f"    gen   = {sys.getsizeof(big_gen)} 字节")
    print("  预期: 生成器只能遍历一次；它不把全部元素存起来，所以省内存。")
    print("        大文件逐行读、大数据流水线，生成器是标准做法（第 19 讲会用）。")

    print("\n  提示: 判断该用生成器还是列表，看“这些元素要不要同时存在、要不要用两遍”。")


if __name__ == "__main__":
    main()