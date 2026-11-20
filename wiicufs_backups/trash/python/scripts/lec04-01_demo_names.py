# 规模纪律：只做内存与算术观察，目标 < 3 秒。
# 用途：为第 04 讲提供真实数据——绑定、别名、id/is、类型、整除、浮点、大整数。
import math
import sys

print(f"python {sys.version.split()[0]}")

print()
print("=== EXP1: print 出来的字 vs 类型 ===")
print("print(12)   ->", 12)
print("print('12') ->", "12")
print("type(12)    =", type(12).__name__)
print("type('12')  =", type("12").__name__)
print("expect: 屏幕上看起来一样，但一个是 int、一个是 str")
assert type(12) is int and type("12") is str

print()
print("=== EXP2: input 拿到的是 str，要算数必须转换 ===")
raw = "12"  # 模拟 input() 的返回值
print("raw + 1 会报错; int(raw) + 1 =", int(raw) + 1)
print("float('3.5') + 1 =", float("3.5") + 1)
try:
    raw + 1
except TypeError as e:
    print("raw + 1 ->", type(e).__name__, str(e))
print("expect: 不转换就 TypeError")
assert type(raw) is str

print()
print("=== EXP3: b = a 不复制，两个名字指向同一个列表 ===")
a = [1, 2]
b = a
b.append(3)
print("a =", a, "b =", b, "a is b =", a is b)
print("expect: a 也变成 [1, 2, 3]，因为只有一个列表对象")
assert a == [1, 2, 3] and a is b

print()
print("=== EXP4: a = a + [3] 新建；a += [3] 原地 ===")
x = [1]
id_before = id(x)
x = x + [3]
print("after x = x + [3]: id changed =", id(x) != id_before, "x =", x)

y = [1]
id_before = id(y)
y += [3]
print("after y += [3]   : id changed =", id(y) != id_before, "y =", y)
print("expect: + 新建（id 变），+= 原地（id 不变）")
assert x == [1, 3] and y == [1, 3]

print()
print("=== EXP5: id / == / is，小整数缓存 ===")
p = 256
q = int("256")
print("256: p is q =", p is q, "p == q =", p == q)
r = 257
s = int("257")
print("257: r is s =", r is s, "r == s =", r == s)
print("expect: 256 被缓存（同一对象），257 不保证")
assert p is q and r == s

print()
print("=== EXP6: 动态类型 + 强类型 ===")
v = 1
print("v 先是", type(v).__name__, "值", v)
v = "one"
print("v 改绑后是", type(v).__name__, "值", v)
print("1 + 1.0 =", 1 + 1.0, type(1 + 1.0).__name__)
print("True == 1:", True == 1, "| True + True =", True + True, "| isinstance(True, int):", isinstance(True, int))
try:
    1 + "1"
except TypeError as e:
    print("1 + '1' ->", type(e).__name__)
print("expect: 名字可改绑（动态），但运算不隐式转换（强）")
assert v == "one" and 1 + 1.0 == 2.0 and True + True == 2

print()
print("=== EXP7: 整除、取余、幂 ===")
print("7 / 2  =", 7 / 2)
print("-7 // 2 =", -7 // 2, "| -7 % 2 =", -7 % 2)
print("check -7 == (-7 // 2) * 2 + (-7 % 2):", -7 == (-7 // 2) * 2 + (-7 % 2))
print("2 ** 10 =", 2 ** 10)
print("expect: / 出 float；// 向下取整（-4）；% 与 // 配套")
assert 7 / 2 == 3.5 and -7 // 2 == -4 and -7 % 2 == 1

print()
print("=== EXP8: round 与浮点误差 ===")
print("round(2.5) =", round(2.5), "| round(3.5) =", round(3.5), "| round(0.5) =", round(0.5))
z = 0.1 + 0.2
print("0.1 + 0.2 =", repr(z), "| == 0.3:", z == 0.3, "| isclose:", math.isclose(z, 0.3))
print("expect: round 是银行家舍入；浮点不相等但 isclose")
assert round(2.5) == 2 and round(3.5) == 4 and not (z == 0.3)

print()
print("=== EXP9: int 任意精度 ===")
big = 2 ** 100
print("2**100 的位数 =", len(str(big)))
print("2**1000 的位数 =", len(str(2 ** 1000)))
print("bool: 2**1000 有上限吗? 没有，位数随内存增长")
assert len(str(big)) == 31

print()
print("=== EXP10: 可变与不可变 ===")
t = (1, 2)
try:
    t[0] = 3
except TypeError as e:
    print("tuple 改元素 ->", type(e).__name__)
text = "a"
id_before = id(text)
text += "b"
print("str += 后 id changed =", id(text) != id_before, "| text =", text)
lst = [1]
id_before = id(lst)
lst.append(2)
print("list append 后 id changed =", id(lst) != id_before, "| lst =", lst)
print("expect: tuple/str 不可变（改=新建），list 原地改")
assert text == "ab" and lst == [1, 2]

print()
print("=== EXP11: None 与假值 ===")
print("None is None:", None is None, "| None == False:", None == False)
print("bool(None):", bool(None), "| bool(0):", bool(0), "| bool(''):", bool(""), "| bool([]):", bool([]))
print("expect: None 只等于自己；上面这些在 if 里都为假")
assert None is None and not bool(None) and None != False

print()
print("=== EXP12: docstring 能被 __doc__ 取出 ===")
def bmi(weight, height):
    """返回 BMI：体重(kg) / 身高(m) 的平方。"""
    return weight / (height ** 2)

print("bmi.__doc__ =", repr(bmi.__doc__))
print("bmi(70, 1.75) =", round(bmi(70, 1.75), 1))
assert "BMI" in bmi.__doc__

print()
print("[OK] names and types demo finished")
