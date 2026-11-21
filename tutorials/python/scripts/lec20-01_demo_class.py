"""第 20 讲验证脚本：class 创建了什么 / self / 实例与类属性 / 方法绑定 / 私有约定 / 多实例。

规模纪律：纯内存操作，< 1 秒。
运行：uv run python tutorials/python/scripts/lec20-01_demo_class.py

讲义里引用的每一条输出都来自本脚本。
"""

WIDTH = 68


def section(title: str) -> None:
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


class Account:
    """最小账户：只放例子要用的东西。"""

    rate = 0.02          # 类属性：所有实例共享，默认利率
    tags = []            # 类属性且可变：本讲讲它为什么危险

    def __init__(self, owner: str, balance: int = 0) -> None:
        self.owner = owner
        self.balance = balance
        self._history = []          # 单下划线：约定为内部
        self.__secret = "pin-1234"  # 双下划线：会被改名

    def deposit(self, amount: int) -> None:
        self.balance += amount
        self._history.append(("deposit", amount))

    def withdraw(self, amount: int) -> None:
        if amount > self.balance:
            raise ValueError(f"余额不足: {self.balance} < {amount}")
        self.balance -= amount
        self._history.append(("withdraw", amount))

    def statement(self) -> list[tuple[str, int]]:
        return list(self._history)


def main() -> None:
    section("1. class 创建了什么：一个类对象")
    print(f"  type(Account)             = {type(Account)}")
    print(f"  Account 的公开名字        = {[k for k in Account.__dict__ if not k.startswith('__')]}")
    a = Account("张三", 100)
    print(f"  type(a)                   = {type(a)}")
    print(f"  a.__dict__                = {a.__dict__}")
    print(f"  isinstance(a, Account)    = {isinstance(a, Account)}")
    print("  预期: class 语句运行时造出一个类对象；实例的 __dict__ 只装实例自己的属性。")

    section("2. self 是谁：绑定方法实测")
    print(f"  Account.deposit           = {Account.deposit}")
    print(f"  a.deposit                 = {a.deposit}")
    print(f"  a.deposit.__self__ is a   = {a.deposit.__self__ is a}")
    print(f"  type(a.deposit)           = {type(a.deposit)}")
    Account.deposit(a, 50)          # 未绑定调用：自己把实例传进去
    print(f"  用 Account.deposit(a, 50) 直接调后 a.balance = {a.balance}")
    print("  预期: a.deposit 是绑定了 a 的方法对象；self 就是调用时被绑进去的那个实例。")

    section("3. 实例属性与类属性：读取靠查找，赋值只改一层")
    b = Account("李四")
    print(f"  a.rate（读类属性）        = {a.rate}")
    a.rate = 0.05
    print(f"  a.rate = 0.05 之后        = {a.rate}，b.rate = {b.rate}，Account.rate = {Account.rate}")
    print(f"  'rate' in a.__dict__      = {'rate' in a.__dict__}")
    Account.rate = 0.03
    print(f"  Account.rate 改为 0.03 后：a.rate = {a.rate}（被自己遮蔽），b.rate = {b.rate}")
    del a.rate
    print(f"  del a.rate 之后           = {a.rate}  ← 又去看类属性")
    print("  预期: 读的时候逐层往类上找；赋值只在实例自己身上新建，不碰类。")

    section("4. 可变类属性的坑：所有实例共享同一份")
    c = Account("王五")
    d = Account("赵六")
    c.tags.append("vip")
    print(f"  c.tags = {c.tags}")
    print(f"  d.tags = {d.tags}  ← 被连带改了")
    print(f"  c.tags is d.tags = {c.tags is d.tags}")
    print("  预期: 类属性只在 class 语句执行时建一次；可变对象被所有实例共享。")

    section("5. 方法也是查找出来的：实例属性会遮蔽方法")
    e = Account("钱七", 10)
    print(f"  e.deposit 可调用          = {callable(e.deposit)}")
    e.deposit = 5
    print(f"  给 e.deposit 赋 5 之后    = {e.deposit!r}")
    try:
        e.deposit(1)
    except TypeError as exc:
        print(f"  再调用抛                  = TypeError: {exc}")
    print(f"  其它实例不受影响            = {callable(c.deposit)}")
    print("  预期: 查找顺序是 实例 __dict__ → 类 → 父类；实例上放同名值就把方法挡住了。")

    section("6. 私有只是约定：改名，不是封锁")
    f = Account("孙八")
    print(f"  f.__dict__ 的键            = {list(f.__dict__)}")
    print(f"  访问 _Account__secret      = {f._Account__secret}")
    print(f"  访问 _history（约定内部）   = {f._history}")
    try:
        f.nonexistent
    except AttributeError as exc:
        print(f"  访问不存在的属性            = AttributeError: {exc}")
    print("  预期: 双下划线被改名为 _类名__属性；单下划线完全没变。两者都拦不住访问。")

    section("7. 多实例：BankAccount 的存取与流水互不干扰")
    p = Account("张三", 100)
    q = Account("李四", 200)
    p.deposit(50)
    p.withdraw(30)
    q.withdraw(20)
    print(f"  p: balance={p.balance} statement={p.statement()}")
    print(f"  q: balance={q.balance} statement={q.statement()}")
    try:
        p.withdraw(10_000)
    except ValueError as exc:
        print(f"  超额取款                    = ValueError: {exc}")
    print(f"  失败后 p.balance 仍为       = {p.balance}")
    print("  预期: 每个实例的 balance / _history 独立；异常路径不会改坏状态。")

    section("8. isinstance 的两个容易误判的例子")
    print(f"  isinstance(True, int)      = {isinstance(True, int)}  ← bool 是 int 子类")
    print(f"  isinstance(a, object)      = {isinstance(a, object)}")
    print("  预期: isinstance 看继承链；类型判断用它，别用 type(x) == 某类。")


if __name__ == "__main__":
    main()
