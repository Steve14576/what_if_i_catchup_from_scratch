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
