"""第 10 讲验证脚本：整数精度 / 浮点误差 / 双除法 / 取余符号 / 优先级 / round / 转换 / bool / complex / 金额。

规模纪律：纯内存运算，目标 < 2 秒。
运行：uv run python tutorials/python/scripts/lec10-01_demo_numbers.py

讲义里引用的每一个数字都来自本脚本。
"""

import math
import sys
from decimal import Decimal

WIDTH = 68


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def main() -> None:
    section("1. int 是任意精度：没有溢出这回事")
    big = 2 ** 100
    print(f"  2 ** 100 = {big}")
    print(f"  它的十进制位数 = {len(str(big))}")
    much = 10 ** 1000
    print(f"  10 ** 1000 的位数 = {len(str(much))}（照样算得出来）")
    print("  预期: 与 C/Java 的 64 位整数不同，Python 的 int 会随需要变长；")
    print("        代价是大数运算变慢，这属于第 23 讲的性能话题。\n")

    section("2. float 是固定精度的二进制小数：0.1 + 0.2 的真相")
    s = 0.1 + 0.2
    print(f"  0.1 + 0.2        = {s!r}")
    print(f"  等于 0.3 吗     = {s == 0.3}")
    print(f"  两者相差        = {s - 0.3!r}")
    print(f"  用 isclose 判定  = {math.isclose(s, 0.3)}")
    print(f"  0.1 的精确值     = {Decimal(0.1)}")
    print("  预期: 0.3 无法用有限位二进制精确表示，0.1 与 0.2 各自都有微小误差，")
    print("        相加后误差露出来。isclose 用相对容差判断“够不够近”，这是正确姿势。\n")

    section("3. 双除法：/ 给小数，// 向下取整")
    pairs = [(7, 2), (-7, 2), (7, -2), (-7, -2)]
    print(f"{'算式':<12}{'/ 结果':>10}{'// 结果':>10}{'divmod 结果':>18}")
    for a, b in pairs:
        print(f"{a} / {b:<8}{a / b:>10}{a // b:>10}{str(divmod(a, b)):>18}")
    print("  预期: // 不是“去掉小数部分”，而是“向下取整”（朝负无穷）：")
    print("        -7 // 2 = -4，而 int(-7/2) = -3。两者不同，考试与业务逻辑都会考这一点。\n")

    print(f"  int(-3.7) = {int(-3.7)}   而  -3.7 // 1 = {-3.7 // 1}")
    print("  预期: int() 朝零截断，// 朝负无穷取整；负数上二者结果不同。\n")

    section("4. 取余的符号跟着除数走")
    for a, b in [(7, 2), (-7, 2), (7, -2), (-7, -2)]:
        print(f"  {a} % {b} = {a % b}")
    print("  预期: 余数的符号与除数相同；且恒有 a == (a // b) * b + (a % b)。")
    a, b = -7, 2
    print(f"  验算: {a} == ({a} // {b}) * {b} + ({a} % {b}) -> "
          f"{a == (a // b) * b + (a % b)}\n")

    section("5. 幂与优先级：-2 ** 2 不是 4")
    print(f"  2 ** 10   = {2 ** 10}")
    print(f"  2 ** -1   = {2 ** -1}（负指数得到小数）")
    print(f"  2 + 3 * 4 = {2 + 3 * 4}； (2 + 3) * 4 = {(2 + 3) * 4}")
    print(f"  -2 ** 2   = {-2 ** 2}； (-2) ** 2 = {(-2) ** 2}")
    print("  预期: ** 的优先级高于一元负号，所以 -2 ** 2 等价于 -(2 ** 2) = -4。")
    print("        拿不准就加括号——括号是最便宜的保险。\n")

    section("6. round 不是“四舍五入”，是“银行家舍入”")
    for value in (0.5, 1.5, 2.5, 3.5):
        print(f"  round({value}) = {round(value)}")
    print(f"  round(2.675, 2) = {round(2.675, 2)}")
    print(f"  round(1.005, 2) = {round(1.005, 2)}")
    print("  预期: 恰好 .5 时向“偶数”取整（2.5 -> 2，3.5 -> 4）；")
    print("        而 2.675 存成 2.67499...、1.005 存成 1.00499...，舍入后分别得 2.67 与 1.0。")
    print("        所以“用 round 做金额”是不安全的，见第 8 节。\n")

    section("7. 类型转换与 bool")
    print(f"  int('12') = {int('12')}   float('1.5') = {float('1.5')}")
    print(f"  int(3.9)  = {int(3.9)}   int(-3.9) = {int(-3.9)}")
    print(f"  bool(0) = {bool(0)}  bool('') = {bool('')}  bool('0') = {bool('0')}  bool([]) = {bool([])}")
    print(f"  True + True = {True + True}   isinstance(True, int) = {isinstance(True, int)}")
    print("  预期: 非空字符串 '0' 是真；bool 是 int 的子类，所以 True 能直接参与加法。")
    print("        这意味着 “if x:” 与 “if x == True:” 不是一回事。\n")

    section("8. 金额为什么用“整数分”而不是 float")
    pennies = 0
    for _ in range(10):
        pennies += 10
    yuan = 0.0
    for _ in range(10):
        yuan += 0.1
    print(f"  整数分累加 10 次：{pennies} 分 = {pennies / 100} 元")
    print(f"  float 累加 10 次：{yuan!r} 元")
    print(f"  两者相等吗 = {yuan == 1.0}")
    print("  预期: 整数分精确；float 累加十次已经和 1.0 差一点点。")
    print("        做法：金额一律存整数分，只在显示时除以 100。\n")

    section("9. complex：有，但本课程只在“知道存在”这一层")
    z = 1 + 2j
    print(f"  z = {z!r}  实部 = {z.real}  虚部 = {z.imag}  模 = {abs(z)}")
    print("  预期: Python 内置复数类型，工程计算里用得少；复变函数课的算法用 numpy 更方便。\n")

    section("10. 字面量写法：同一种数字可以有多种写法")
    print(f"  1_000_000 = {1_000_000}   0b1010 = {0b1010}   0o17 = {0o17}   0xFF = {0xFF}")
    print(f"  1e3 = {1e3}   1.5e-3 = {1.5e-3}")
    print("  预期: 下划线只是给人看的（读大数不容易数错），进制前缀与科学计数都是同一类整数/浮点。")

    print(f"\n  解释器版本 = {sys.version.split()[0]}")


if __name__ == "__main__":
    main()
