"""第 15 讲验证脚本：定义与返回值 / 参数绑定 / 可变默认参数 / 作用域 / 传参语义 / *args 与 **kwargs。

规模纪律：纯内存操作，目标 < 2 秒。
运行：uv run python tutorials/python/scripts/lec15-01_demo_functions.py

讲义里引用的每一条输出都来自本脚本。
"""

import time

WIDTH = 68


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def add(a, b):
    """返回两个数的和。"""
    return a + b


def no_return(x):
    x * 2


def greet(name, greeting="你好"):
    return greeting + "，" + name


def bad_default(x, acc=[]):
    acc.append(x)
    return acc


def good_default(x, acc=None):
    if acc is None:
        acc = []
    acc.append(x)
    return acc


def describe(*args, **kwargs):
    return f"args={args}  kwargs={kwargs}"


def kw_only(a, *, b):
    return a + b


def stamp(when=time.time()):
    return when


def scope_demo():
    x = 10
    print(f"    函数内 x = {x}（局部）")
    return x


def unbound_demo():
    print(f"    进入函数时全局 x = {x}")
    x = 99
    return x


def mutate_list(xs):
    xs.append(99)
    return xs


def rebind_list(xs):
    xs = xs + [99]
    return xs


def main() -> None:
    section("1. def 定义了什么：一个可调用的对象")
    print(f"  add(1, 2) = {add(1, 2)}")
    print(f"  add.__name__ = {add.__name__!r}")
    print(f"  add.__doc__ = {add.__doc__!r}")
    print(f"  没写 return 的函数：no_return(3) = {no_return(3)!r}")
    f = add
    print(f"  函数也是对象，可以赋值给别的名字：f(2, 5) = {f(2, 5)}")
    print("  预期: def 把函数体包起来、绑到一个名字上；不写 return 就等于 return None；")
    print("        函数本身是对象，能赋值、能当参数传（第 16 讲展开）。\n")

    section("2. 参数绑定：位置、关键字、默认值")
    print(f"  greet('小明')            = {greet('小明')!r}")
    print(f"  greet('小明', '早上好')   = {greet('小明', '早上好')!r}")
    print(f"  greet(greeting='hi', name='Bob') = {greet(greeting='hi', name='Bob')!r}")
    try:
        greet()
    except TypeError as exc:
        print(f"  greet() -> TypeError: {exc}")
    try:
        greet("a", "b", "c")
    except TypeError as exc:
        print(f"  greet('a','b','c') -> TypeError: {exc}")
    print("  预期: 位置参数按顺序绑定，关键字参数按名字绑定，默认值在没传时生效；")
    print("        少传或多传都会在调用时立刻报 TypeError。\n")

    section("3. 可变默认参数：只创建一次，跨调用共享")
    print(f"  bad_default(1) = {bad_default(1)}")
    print(f"  bad_default(2) = {bad_default(2)}")
    print(f"  bad_default(3) = {bad_default(3)}")
    print(f"  换成好写法 good_default(1) = {good_default(1)}")
    print(f"  good_default(2) = {good_default(2)}")
    print("  预期: 坏写法的默认列表在“定义时”只建一次，三次调用往同一个列表里加；")
    print("        好写法用 None 占位、每次调用新建，三次结果各自独立。\n")

    section("4. 默认值在定义时求值，不是每次调用")
    t1 = stamp()
    time.sleep(0.01)
    t2 = stamp()
    print(f"  两次调用 stamp() 的返回值相同吗 = {t1 == t2}")
    print(f"  值 = {t1}")
    print("  预期: True。默认值在 def 执行那一刻就算好了，之后每次调用都用同一份。")
    print("        所以默认值不要写“每次都想重新算”的表达式。\n")

    section("5. 作用域：函数内赋值即成本地变量")
    x = 5
    print(f"  全局 x = {x}")
    scope_demo()
    try:
        unbound_demo()
    except UnboundLocalError as exc:
        print(f"  unbound_demo() -> UnboundLocalError: {exc}")
    print("  预期: 函数里一旦对 x 赋值，x 在整个函数内就是局部变量；")
    print("        赋值发生在 print 之后，于是 print 时它还没绑定 → UnboundLocalError。")
    print("        想改全局变量得显式声明 global，但日常写代码应尽量避免。\n")

    section("6. 传参语义：传的是对象引用，不是副本")
    xs = [1, 2]
    mutate_list(xs)
    print(f"  函数里 append：调用后 xs = {xs}")
    ys = [1, 2]
    rebind_list(ys)
    print(f"  函数里重新绑定：调用后 ys = {ys}")
    n = 10
    def try_change_number(v):
        v = v + 1
        return v
    try_change_number(n)
    print(f"  传数字进去改：调用后 n = {n}")
    print("  预期: 可变对象被改内容，外部跟着变；重新绑定只是换函数内的标签，外部不变；")
    print("        不可变对象（数字）改不了，“改”其实是新建。\n")

    section("7. *args 与 **kwargs：收下不确定个数的参数")
    print(f"  describe(1, 2)                = {describe(1, 2)}")
    print(f"  describe(1, k=2)              = {describe(1, k=2)}")
    print(f"  describe(*[1, 2], **{{'k': 3}}) = {describe(*[1, 2], **{'k': 3})}")
    print("  预期: *args 收多余的位置参数成元组；**kwargs 收多余的关键字参数成字典；")
    print("        调用时反过来用 * 和 ** 可以把序列/字典拆开传进去。\n")

    section("8. 仅关键字参数：* 之后的参数必须写名字")
    print(f"  kw_only(1, b=2) = {kw_only(1, b=2)}")
    try:
        kw_only(1, 2)
    except TypeError as exc:
        print(f"  kw_only(1, 2) -> TypeError: {exc}")
    print("  预期: 星号后面的参数只能用关键字传；这样调用处的意图更清楚，也不怕参数顺序变。\n")

    section("9. 卫语句：把异常情况挡在前面")
    def average(nums):
        if not nums:
            return None
        return sum(nums) / len(nums)

    for data in ([90, 80], []):
        print(f"    average({data}) = {average(data)}")
    print("  预期: 空列表直接返回 None，避免后面除零；正事代码留在最外层，不用层层缩进。")

    print("\n  提示: 判断该不该拆函数，看这段逻辑“要不要单独说清它做什么、输入什么、返回什么”。")


if __name__ == "__main__":
    main()
