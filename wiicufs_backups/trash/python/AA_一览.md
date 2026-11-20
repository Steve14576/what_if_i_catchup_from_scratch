# Python 程序设计——AA 一览

> 这是附录与字典，不是速查口令。每条概念给中文名、英文/缩写、完整定义、首次出现讲次、本讲要求。字典条目说明"它是什么"，不写成用法提示；要用人话把它讲开，仍看对应讲次的正文。
>
> 本讲要求分两档：**要会**＝现在就要能用（哪怕只是五条命令）；**只认得**＝别人提起你知道指什么、在哪一站，不要求现在会用。

## 一、概念

| 概念（中文） | 英文/缩写 | 定义 | 首次出现 | 本讲要求 |
|---|---|---|---|---|
| 文件 | file | 磁盘上按名字存放的一段内容，可以是文本、图片、程序等 | 第 01 讲 | 只认得（天天在用） |
| 扩展名 | extension | 文件名最后那个点后面的部分，用来告诉系统该把文件交给哪个程序打开；`.py` 表示"写给 Python 的文本" | 第 01 讲 | 要会（认出 `.py` 与 `.py.txt`） |
| 命令 | command | 在黑窗口里敲的一行字，由 shell 解析后执行 | 第 01 讲 | 要会（会用五条） |
| 参数 | argument | 跟在命令名后面、用空格隔开的部分，告诉程序"对谁做这件事"，如 `hello.py` | 第 01 讲 | 要会 |
| 源代码 | source code | 人写的、以文本形式保存的程序；Python 的 `.py` 文件就是源代码 | 第 01 讲 | 只认得 |
| 机器码 | machine code | CPU 能直接执行的二进制指令序列 | 第 01 讲 | 只认得 |
| 解释器 | interpreter | 读取源代码、把它编译成字节码并逐条执行的程序；Windows 上就是 `python.exe` | 第 01 讲 | 要会（会启动、会看版本） |
| 字节码 | bytecode | 解释器内部使用的中间指令；比源代码更接近机器，但不是 CPU 直接执行的机器码 | 第 01 讲 | 只认得 |
| `__pycache__` | —— | 存放 `.pyc` 字节码缓存的目录，由 `import` 生成；删掉不影响正确性 | 第 01 讲 | 要会判断（删了没事） |
| 交互式解释器 | REPL | Read-Eval-Print Loop：读一行、求值、打印、再等下一行；提示符是 `>>>`，它只是提示符不是语法 | 第 01 讲 | 只认得（知道抄进文件会报错） |
| 标准输出 | standard output（stdout） | 程序写普通结果的输出通道；`print` 写的是字节，显示是窗口的事 | 第 01 讲 | 只认得 |
| 程序 | program | 磁盘上的文件，例如 `hello.py`、`python.exe` | 第 01 讲 | 只认得 |
| 进程 | process | 程序的一次运行；拥有独立内存，结束即释放 | 第 01 讲 | 只认得 |
| 名字绑定 | name binding | 让一个名字指向某个对象；`=` 执行的就是绑定 | 第 01 讲（第 04 讲系统化） | 只认得（04 讲要会） |
| 对象身份 | identity | 对象在本次运行中的唯一标识，由 `id()` 给出；`is` 比较的正是它 | 第 01 讲（第 04 讲展开） | 只认得 |
| 绝对路径 | absolute path | 从盘符或根目录写起的完整路径，在任何目录下都指向同一个文件 | 第 01 讲 | 要会 |
| 相对路径 | relative path | 从当前工作目录写起的路径 | 第 01 讲 | 要会 |
| 当前工作目录 | current working directory（cwd） | 解析相对路径的起点；随你在哪个目录敲命令而变，与脚本所在目录是两件事 | 第 01 讲 | 要会 |
| 终端 | terminal | 显示命令行、接收键盘输入并显示程序输出的窗口程序 | 第 01 讲 | 要会（会用五条命令） |
| shell | shell | 解析并执行你敲的命令的程序；PowerShell 与 cmd 是两种 | 第 01 讲 | 只认得 |
| 码页 | code page | 终端用来把字节解码成字符的那套编码规则；Windows 中文环境历史默认 936（GBK） | 第 01 讲 | 只认得（知道乱码与它有关） |
| 环境变量 | environment variable | 操作系统提供给程序的一组"名字=值"配置；`PATH` 就是其中一个 | 第 02 讲 | 只认得 |
| `PATH` | —— | 一个环境变量，内容是一串目录；shell 按顺序在这些目录里找命令 | 第 02 讲 | 要会（会看、会加） |
| 虚拟环境 | virtual environment（venv） | 一个项目专用的小环境：独立的 site-packages 加上指向解释器的启动器 | 第 02 讲 | 要会（建/激活/退出/删） |
| `site-packages` | —— | 第三方包装在磁盘上的目录；每个解释器或环境各有一份 | 第 02 讲 | 要会（能找到它） |
| `pip` | pip | Python 自带的包管理命令，从包索引下载并安装包 | 第 02 讲 | 要会 |
| 包索引 | package index（PyPI） | 公开的 Python 包仓库，`pip` 默认从这里取包 | 第 02 讲 | 只认得 |
| wheel | `.whl` | 预编译好的包文件格式，`pip` 下载后解压到 site-packages | 第 02 讲 | 只认得 |
| 锁文件 | lock file（`uv.lock`） | 记录每个依赖的确切版本，保证别人装出同样的环境 | 第 02 讲 | 只认得 |
| IDE | integrated development environment | 在编辑器之上集成"选解释器、运行、调试"的工具 | 第 02 讲 | 只认得（会用即可） |
| 执行策略 | execution policy | Windows 限制哪些脚本可以运行的设置 | 第 02 讲 | 只认得（知道怎么临时放行） |
| BOM | byte order mark | 文件开头用来标记编码的几个字节；UTF-8 BOM 会让某些读取多出 `\ufeff` | 第 02 讲 | 只认得 |
| 标准库 | standard library | 随 Python 一起安装的模块集合（如 `json`），来自原始解释器而不是 site-packages | 第 02 讲 | 只认得 |
| 模块 | module | 一个可以被引用的 `.py` 文件，或一组这样的文件；`import` 拿的是它里面的名字 | 第 01 讲（第 12 讲系统化） | 只认得 |
| 包 | package | 把一组模块打包发布的东西；用 `pip install` 装进 site-packages | 第 02 讲 | 只认得 |
| 管道 | pipe | 把一个程序的输出直接接给另一个程序，写法是 `\|` | 第 01 讲 | 只认得 |
| `cmdlet` | —— | PowerShell 对"命令"的叫法 | 第 01 讲 | 只认得 |
| 镜像 | mirror | 包索引的替代下载站，内容相同、地址不同；`pip install -i 地址` 临时指定 | 第 02 讲 | 只认得（知道加 `-i`） |
| `PYTHONIOENCODING` | —— | 一个环境变量，告诉 Python 输出该用哪种编码 | 第 02 讲 | 只认得 |
| `utf-8-sig` | —— | 读文件时能自动丢掉开头 BOM 的 UTF-8 编码名 | 第 02 讲 | 只认得 |
| 仓库 | repository | 被 git 管理的目录；历史存在其中的 `.git` 目录里 | 第 03 讲 | 要会（会 init） |
| 提交 | commit | 把当前所有被跟踪文件的样子存成一份带说明的快照，追加到历史 | 第 03 讲 | 要会 |
| 快照 | snapshot | 某次提交时所有文件内容的一份记录 | 第 03 讲 | 只认得 |
| 工作区 | working tree | 你正在编辑的那份文件；`restore` 会把它的改动丢掉 | 第 03 讲 | 要会（知道它在哪） |
| 暂存区 | staging area（index） | "下次提交要包含什么"的清单，由 `git add` 填充 | 第 03 讲 | 要会 |
| `HEAD` | —— | 指向当前所在那次提交的引用；`HEAD~1` 是上一次 | 第 03 讲 | 只认得 |
| 分支 | branch | 指向某次提交的可移动标签；默认叫 `master` 或 `main` | 第 03 讲 | 只认得 |
| 远程仓库 | remote | 放在另一处的同一份仓库；用 `clone`/`push`/`pull` 同步 | 第 03 讲 | 要会（push/pull） |
| `diff` | —— | 两次内容之间的逐行对照，`-` 是原来的行、`+` 是现在的行 | 第 03 讲 | 要会（会看） |
| `.gitignore` | —— | 列出不让 git 跟踪的文件模式；只对未跟踪文件生效 | 第 03 讲 | 要会 |
| 反向提交 | `git revert` | 新增一次把某次改动反过来的提交，历史保留 | 第 03 讲 | 要会 |
| 大语言模型 | large language model（LLM） | 根据前文预测下一个 token 的模型 | 第 03 讲 | 只认得 |
| 上下文窗口 | context window | 模型一次能读入的文字量；没读进去的内容它不知道 | 第 03 讲 | 只认得 |
| agent | —— | 在模型外面加"读文件 / 改文件 / 跑命令"循环的工具形态 | 第 03 讲 | 只认得 |
| 变量 | variable | 贴在对象上的名字；赋值就是改绑，不是把值装进盒子 | 第 04 讲 | 要会 |
| 对象 | object | 内存里一块有类型、有值的数据；变量名贴在它上面 | 第 04 讲 | 要会（理解模型） |
| 类型 | type | 对象所属的种类，决定它能参与哪些运算 | 第 04 讲 | 要会 |
| 表达式 | expression | 能算出一个值的代码片段，如 `1 + 2` | 第 04 讲 | 要会 |
| 可变对象 | mutable object | 能原地修改内容的对象：list、dict、set、自定义实例 | 第 04 讲 | 要会（判断互相影响） |
| 不可变对象 | immutable object | 改动等于新建对象：int、float、bool、None、str、tuple、frozenset | 第 04 讲 | 要会 |
| 浮点误差 | floating-point error | 二进制无法精确表示某些十进制小数，导致计算有微小偏差 | 第 04 讲 | 要会（不用 `==` 比较） |
| 银行家舍入 | banker's rounding | 恰好 .5 时向偶数靠的舍入规则，`round` 采用 | 第 04 讲 | 要会（知道不是四舍五入） |
| 任意精度整数 | arbitrary-precision integer | int 的位数只受内存限制，不会溢出 | 第 04 讲 | 只认得 |
| `math.isclose` | —— | 判断两个浮点数是否足够接近的函数 | 第 04 讲 | 要会 |
| docstring | documentation string | 函数 / 模块 / 类开头的三引号字符串，存进 `__doc__` | 第 04 讲 | 要会（会写一句） |

## 二、公式与常量

第 01 讲无公式。

后续加入公式的讲次在此登记：公式本身、每个符号指什么与单位、适用条件、出处讲次。

## 三、本讲涉及的命令

| 用途 | 命令 | 备注 |
|---|---|---|
| 进入交互式解释器 | `python` | 出现 `>>>` 提示符；`exit()` 退出 |
| 运行脚本 | `python hello.py` | 前提是 `python` 在 PATH 中 |
| 执行一行 | `python -c "print(1+1)"` | 引号内内容交给解释器 |
| 查版本 | `python -V` | 形如 `Python 3.12.13` |
| 查解释器位置 | `where python` | 可能列出多个；不打印说明没进 PATH |
| 看当前工作目录 | `pwd` | PowerShell |
| 列目录 | `dir` | PowerShell 与 cmd 通用 |
| 进入目录 | `cd 路径` | 绝对或相对都行 |
| 建目录 | `mkdir 名字` | 已存在会报错 |
| 写入文本（UTF-8） | `"文本" \| Set-Content -Encoding utf8 文件名` | PowerShell 5.1 的 `>` 写 UTF-16，不能用来写 `.py` |
| 看当前码页 | `chcp` | 中文环境常见 936 |
| 中止程序 | `Ctrl+C` | 死循环时使用 |
| 建虚拟环境 | `python -m venv .venv` | 第二个参数是目录名，惯例叫 `.venv` |
| 激活（PowerShell） | `.\.venv\Scripts\Activate.ps1` | 提示符前会出现 `(.venv)` |
| 激活（cmd） | `.\.venv\Scripts\activate.bat` | 同上 |
| 退出虚拟环境 | `deactivate` | 只影响当前窗口 |
| 装包 | `python -m pip install 包名` | 比裸 `pip` 稳 |
| 看已装包 | `python -m pip list` | —— |
| 看包信息 | `python -m pip show 包名` | `Location` 是安装位置 |
| 导出依赖 | `python -m pip freeze > requirements.txt` | 含间接依赖 |
| 临时带依赖运行 | `uv run --with 包名 python 脚本.py` | 不改项目环境 |
| 看/改码页 | `chcp` | 65001 为 UTF-8 |
| 临时放行脚本 | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` | 只对当前窗口生效 |
| 确认是否在虚拟环境 | `python -c "import sys; print(sys.prefix, sys.base_prefix)"` | 两值不同即在环境里 |
| 查 site-packages | `python -c "import sysconfig; print(sysconfig.get_paths()['purelib'])"` | 包装在哪一目了然 |
| 查包的真实位置 | `python -c "import 包名; print(包名.__file__)"` | 定位"装到了哪个解释器" |
| 设 git 身份 | `git config --global user.name "名字"` | 一次即可 |
| 建仓库 | `git init` | 生成隐藏目录 `.git` |
| 看状态 | `git status --short` | 两个字符：暂存区 + 工作区 |
| 加入暂存区 | `git add 文件名` | —— |
| 提交 | `git commit -m "说明"` | 一次只做一件事 |
| 看历史 | `git log --oneline` | 最新在最上面 |
| 看未提交改动 | `git diff` | `-` 原行、`+` 现行 |
| 撤销未提交改动 | `git restore 文件名` | 不可恢复，先看 diff |
| 移出暂存区 | `git restore --staged 文件名` | 不改文件内容 |
| 反向提交 | `git revert HEAD` | 保留历史 |
| 加远程并推送 | `git remote add origin 地址` + `git push -u origin master` | 地址可以是本地目录 |
| 克隆并取回 | `git clone 地址` / `git pull --no-rebase` | 冲突时见第 03 讲 5.4 |

## 四、名称对照（本讲出现的文件与概念）

| 名称 | 说清它是什么 |
|---|---|
| `.py` | Python 源代码文件，纯文本，可用记事本打开 |
| `.py.txt` | 另存为时选错"保存类型"的产物：扩展名是 `.txt`，不会被当成 Python 代码 |
| `.pyc` | 编译后的字节码缓存文件，位于 `__pycache__`，文件名含解释器版本（如 `cpython-312`） |
| `python.exe` | Windows 上的解释器可执行文件 |
| `cmd` / `powershell` | 两种 shell 程序的名字，也可以直接用来打开黑窗口 |
| `__main__` | 一个脚本被直接运行时，解释器赋予它的模块名 |
| `hello.py`、`data.csv` | 只是示例文件名，不代表特定内容 |
| `.venv` | 虚拟环境目录的惯例名；内含一份独立 site-packages 与启动器 |
| `py` | Windows 的 Python 启动器，用 `py -3.12` 指定版本 |
| `uv` | 管解释器/环境/依赖/运行的工具，自带锁文件 |
| `requirements.txt` | 依赖清单，记录包名与版本 |
| `sys` | Python 自带的模块；`sys.executable` 是当前解释器路径，`sys.prefix` / `sys.base_prefix` 用于判断是否在虚拟环境 |
| `sysconfig` | Python 自带模块；`get_paths()['purelib']` 给出 site-packages 路径 |
| `os` | Python 自带模块；`os.getcwd()` 返回当前工作目录 |
