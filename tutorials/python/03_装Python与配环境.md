# 第 03 讲 装 Python 与配环境

> **前置**：第 01 讲（解释器是一个程序、装 Python 装了三样东西）、第 02 讲（`PATH` 决定命令能不能被找到）。
> **预计时间**：约 2 小时（第 3、4 节要在自己机器上动手，别只看）。
> **本讲回答**：装 Python 到底在我电脑上放了什么？安装向导里"Add python.exe to PATH"勾不勾差在哪？`pip install` 装的东西去哪了，为什么换个项目就找不到？虚拟环境到底隔离了什么，删掉文件夹是不是就干净了？"激活"到底改了哪几样东西？没网络、没管理员权限怎么办？`uv` 是必须学的吗？
> **本讲结束你能做到**：装好解释器并验证；建一个虚拟环境、装一个包、卸掉它；说清每一步在磁盘上留下什么；在只能装到用户目录、甚至没有网络的机器上也能把环境配起来。

## 0. 这一讲要解决的麻烦

你有两个项目。项目 A 是一个两年前的脚本，依赖某个库的老版本；项目 B 是刚接手的，要求同一个库的新版本。你在全局装了新版，A 立刻报错；装回老版，B 又跑不起来。来回折腾半小时，最后把两个项目都弄坏了。

问题的根源不在于你操作错了，而在于**全局环境只有一份**。这一讲讲的就是给每个项目配自己的那一份，并说清它在磁盘上到底是什么。

和前一讲一样，这一讲属于素养卷：现在只要求跟着做一遍、知道每一步在干什么。看不懂的地方可以先跳过，第 09 讲开始写 Python 主线不依赖这里的任何一步——但你越往后写，越会频繁用到它。

## 1. 装 Python 到底装了什么

第 01 讲说过是三样：解释器、标准库、`pip`。这里落到具体位置。

### 1.1 三种常见安装途径

| 途径 | 怎么做 | 优点 | 要注意的 |
|---|---|---|---|
| 官网安装包 | 访问 python.org 下载 Windows installer，双击安装 | 最标准，选项看得见 | 第一屏的 "Add python.exe to PATH" 必须勾 |
| 系统包管理器 | Windows 用 `winget install Python.Python.3.12`；macOS 用 `brew install python`；Ubuntu 用 `apt install python3` | 一条命令装完，升级方便 | 装到哪、有没有 `pip` 取决于发行版 |
| 应用商店 | 微软商店搜 Python | 点一下就装 | 路径和权限与官网版不同，出问题时不好排查，学习阶段不推荐 |

装完之后，解释器一般在这个位置（版本号会不同）：

```text
C:\Users\你\AppData\Local\Programs\Python\Python312\python.exe
```

macOS / Linux 上通常在 `/usr/local/bin/python3` 或 `/usr/bin/python3`。

### 1.2 安装向导里两个必须看懂的选项

- **Add python.exe to PATH**：这一项决定安装目录是否写进 `PATH`。不勾，装完敲 `python` 就是第 02 讲那个"无法将 python 项识别为 cmdlet"的报错。勾上之后仍然要**新开终端**才生效，因为已经开着的窗口用的是它启动时读到的那份环境变量。
- **Install for all users / 只为我安装**：所有用户安装要管理员权限，装到 `C:\Program Files\` 附近；只为我安装不需要权限，装到你的用户目录。**没有管理员权限的机房机器就选后者**，后面的问题也就解决了一半。

安装向导第二页还有几个可选项，默认值通常可以直接用：`pip`（包管理器，必须有）、`py launcher`（Windows 的多版本启动器，建议留着）、`tcl/tk`（图形界面库，本课程不用，但留着不碍事）。

### 1.3 装完先验证三条

```powershell
python --version
where.exe python
python -c "import sys; print(sys.executable)"
```

三条命令分别回答：装的什么版本、命令实际指向哪个文件、这个解释器住在哪。三条都能给出答案，才说明环境是通的。

如果第一条就失败，回第 02 讲 5.5 节的三条修复路线，不要急着重装——重装但不勾 `PATH`，问题会原样复现。

### 1.4 装了多个版本怎么办

Windows 上装了多个 Python 是常态。`py` 启动器就是为此存在的：

```powershell
py -0            # 列出本机装了哪些版本
py -3.12 --version
py -3.11 --version
```

`py` 自己装在 `C:\Windows\py.exe`，它不依赖你 `PATH` 里那个 `python` 是谁，所以排查"到底用的哪个版本"时很好用。macOS / Linux 上对应的是 `python3.11`、`python3.12` 这种带版本号的名字。

## 2. 全局装包为什么会打架

每一个解释器都有一份自己的 `site-packages` 目录，`pip install` 装的东西就放在那儿。全局安装意味着**所有项目共用这一份**。

于是两个项目要同一个库的不同版本时，后装的会覆盖先装的。更麻烦的是这种覆盖不会报错：装的那一步一切正常，等到运行项目 A 时才崩，而那时你已经忘了自己装过什么。

解决办法不是"小心一点"，而是让每个项目有自己的 `site-packages`。这就是虚拟环境。

## 3. 虚拟环境：一个目录装下一套环境

### 3.1 建：`python -m venv .venv`

在项目目录里执行：

```powershell
python -m venv .venv
```

逐个部分解释：

- `python`：用哪个解释器来建。**这一步决定了新环境的"母本"是谁**。
- `-m venv`：`-m` 的意思是"运行一个模块"，`venv` 是标准库里负责建虚拟环境的模块。所以这不是外部命令，是解释器自带的能力。
- `.venv`：新环境放在哪个目录。名字是约定俗成的（点开头表示隐藏），叫 `venv`、`env` 都行，但**全世界的工具默认都认 `.venv`**，跟着用省事。

实测（脚本 `scripts/lec03-01_demo_venv.py`）：本机两次创建分别用了 4.3 秒和 4.8 秒。固态盘上这是正常量级；机械硬盘或杀毒软件实时扫描时可能到几十秒。这是一次性成本，一个项目只用建一次。

### 3.2 磁盘上留下了什么

创建完成后，`.venv` 目录里是这些（实测，只看前两层）：

```text
    Include/
    Lib/
    pyvenv.cfg
    Scripts/
```

逐项说清：

| 名字 | 里面是什么 | 你需要关心吗 |
|---|---|---|
| `Scripts/` | 这个环境的可执行文件：`python.exe`、`pip.exe`、三个激活脚本（`Activate.ps1` / `activate.bat` / `activate`）、`deactivate.bat`。实测共 9 个文件 | 要：激活脚本和 `pip` 都在这 |
| `Lib/site-packages/` | 这个环境装的第三方包。实测刚建好时有 2 项（`pip` 相关） | 要：`pip install` 就装到这里 |
| `pyvenv.cfg` | 这个环境的"出生证明"，纯文本 | 要知道有它，排错时会看 |
| `Include/` | 编译 C 扩展时用的头文件，本课程用不到 | 不用 |

`pyvenv.cfg` 的实测内容（五行长这样）：

```text
home = C:\Users\Administrator\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none
include-system-site-packages = false
version = 3.12.13
executable = E:\...\.venv\Scripts\python.exe
command = E:\...\.venv\Scripts\python.exe -m venv C:\Users\...\Temp\...\demo\.venv
```

三行要读懂：

- `home`：基础解释器（母本）在哪。这个环境自己不存一份完整的标准库，它运行时去 `home` 指的地方借。
- `include-system-site-packages = false`：**不**把全局 `site-packages` 借给你看。这就是"隔离"的开关。
- `executable` 和 `command`：建它的时候用了谁、用了什么命令。这两行是绝对路径，也是"环境不能随便移动或改名"的直接原因——文件里写死了位置。

### 3.3 激活：它只改了三样东西

Windows PowerShell 里：

```powershell
.\.venv\Scripts\Activate.ps1
```

cmd 里：

```text
.venv\Scripts\activate.bat
```

macOS / Linux 里：

```bash
source .venv/bin/activate
```

激活成功的标志是提示符前面多了一段 `(.venv)`。它到底做了什么？实测打开 `Activate.ps1` 就能看到答案，关键几行是：

```text
Copy-Item -Path Env:PATH -Destination Env:_OLD_VIRTUAL_PATH
$Env:PATH = "$VenvExecDir$([System.IO.Path]::PathSeparator)$Env:PATH"
```

翻成中文：

1. **把原来的 `PATH` 存起来**（存进 `_OLD_VIRTUAL_PATH`）；
2. **把这个环境的 `Scripts` 目录插到 `PATH` 最前面**；
3. **设置 `VIRTUAL_ENV` 环境变量、改提示符前缀**（脚本后面的几行）。

所以"激活"不是打开什么开关，它就是**改了当前这个 shell 的 `PATH` 顺序**。这正好接上第 02 讲的结论：`PATH` 里排在前面的目录先被找到，于是你敲的 `python`、`pip` 都落到这个环境里。

退出用：

```powershell
deactivate
```

它做的事就是把 `PATH` 还原成存起来的那份。

一个 PowerShell 特有的坑：默认执行策略可能不允许运行脚本，激活时报"无法加载文件……因为在此系统上禁止运行脚本"。两条出路：改用 cmd 的 `activate.bat`；或者对当前用户放开本地脚本（`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`）。这是 Windows 的安全默认值，不是环境坏了。

### 3.4 不激活也能用

这是最容易被误解的一点：**激活只是让你少打字，不是使用环境的前提**。实测直接用绝对路径调用环境里的解释器：

```text
  sys.executable = C:\Users\...\Temp\...\demo\.venv\Scripts\python.exe
  sys.prefix     = C:\Users\...\Temp\...\demo\.venv
  sys.base_prefix= C:\Users\Administrator\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none
  是虚拟环境吗   = True
```

没激活，一样跑在这个环境里，`sys.prefix` 照样指向它。这也是很多工具（IDE、`uv run`、任务脚本）的做法：**不去动你的 `PATH`，直接拿绝对路径启动对的解释器**。

什么时候该激活：你接下来要连续敲很多条 `python` / `pip` 命令时。只跑一条，写全路径更省心。

### 3.5 隔离的确切含义

隔离不是玄学，是两个变量和一条路径的差别。用同一段探测代码分别跑在两个环境里，实测结果：

```text
[新环境里的 python]
  site-packages  = ['...\demo\.venv\Lib\site-packages']
  pip 模块       = 有，版本 25.0.1

[基准解释器]
  site-packages  = ['E:\...\WHATIFICATCHUPFROMSCRATCH\.venv\Lib\site-packages']
  pip 模块       = 没有
```

三条结论：

1. `sys.prefix` 与 `sys.base_prefix` 不相等，就说明你跑在虚拟环境里。这是判断"我到底在哪个环境"最可靠的办法，比看提示符可靠。
2. 两边 `site-packages` 是**完全不同的目录**。装在 A 环境里的包，B 环境看不到——这就是隔离。
3. 实测里那个基准解释器本身也是虚拟环境（项目根目录下的 `.venv`），它里面**没有 `pip`**。原因见第 4 节。

### 3.6 完整形态：六个容易被问到的问题

- **能删吗？** 能。环境的全部内容都在这个目录里，实测删掉之后 `exists()` 变成 `False`，母本解释器毫发无损。这也是它比"卸载重装 Python"省事的地方。
- **能移动或改名吗？** 不建议。`pyvenv.cfg` 里写的是绝对路径，挪走之后可能还能跑，但一旦出问题会很难查。**要换位置就删了重建**，反正只要几秒。
- **能一个项目建多个吗？** 能，但没必要。一个项目一个 `.venv` 是通行做法。
- **能嵌套吗？** 技术上可以（在环境里再建环境），实际没人这么做，只会把自己绕晕。
- **要提交进 git 吗？** 不要。它体积大、和你的机器绑定；第 04 讲会讲 `.gitignore`，第 26 讲会讲"凭什么别人能重建出一样的环境"。
- **`include-system-site-packages = true` 有什么用？** 让这个环境也能看见全局装的包。只在"全局已经有一大堆包、懒得重装"时用；日常关着，否则隔离就漏了。

## 4. pip：往当前环境里放包

### 4.1 pip 住在环境里，不是住在系统里

`pip` 本身也是一个 Python 程序，它被装进某个环境，就只管那个环境。所以同一台机器上可以有好几个 `pip`。

由此得出一条纪律：**优先用 `python -m pip`，而不是裸 `pip`**。

```powershell
python -m pip install requests
```

理由很直接：`python -m pip` 的意思是"用**这个** python 去跑 pip 模块"，目标环境由前面的 `python` 唯一确定；而裸 `pip` 到底指向哪个环境，取决于 `PATH` 顺序，第 02 讲已经演示过 `PATH` 会被各种工具临时改动。用 `python -m pip`，你写的是谁就是谁。

### 4.2 一个实测出来的反例：环境里可能没有 pip

第 02 讲实测 `which('pip') = None`，本讲又实测那个环境里 `pip 模块 = 没有`。再看 `uv venv` 建出来的环境：

```text
  uv venv 退出码 = 0   耗时 = 0.1 秒
  Scripts/ 里共 11 个文件：['activate', 'activate.bat', ..., 'activate.ps1', ...]
  pyvenv.cfg:
    home = ...
    implementation = CPython
    uv = 0.11.26
    version_info = 3.12
    include-system-site-packages = false
  pip 模块 = 没有
```

没有 `pip.exe`。原因很简单：`uv` 自己就能装包，不需要 pip，所以它建环境时**不往里塞 pip**。

对照之下，标准库的 `python -m venv` 建出来的环境里 pip 是齐的（实测 `pip 25.0.1`）。给"装完 Python 为什么没有 pip"这个问题一个准确答案：**看环境是谁建的**。

### 4.3 常用命令

| 要做的事 | 命令 | 说明 |
|---|---|---|
| 装包 | `python -m pip install 包名` | 可带版本：`包名==1.2.3` |
| 卸包 | `python -m pip uninstall 包名` | 会问一次确认 |
| 看装了什么 | `python -m pip list` | 全量清单 |
| 看某个包的信息 | `python -m pip show 包名` | 版本、依赖、安装位置 |
| 导出依赖清单 | `python -m pip freeze > requirements.txt` | 把当前环境里所有包和版本写成一行一个 |
| 按清单恢复 | `python -m pip install -r requirements.txt` | 换台机器时用 |

`freeze` 和 `install -r` 这一对是"把环境说清楚"的最小手段：别人拿到你的清单，就能装出一样的包集合。更好的做法是第 26 讲的 `pyproject.toml`，现在知道有这条路就够。

### 4.4 国内网络：换镜像源

直连官方源经常很慢或超时。用国内镜像：

```powershell
python -m pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

每次都加 `-i` 很烦，可以写进配置文件，之后自动生效：

- Windows：`%APPDATA%\pip\pip.ini`
- macOS / Linux：`~/.config/pip/pip.conf`

文件内容：

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```

镜像只解决"下载慢"，不解决"没网"。没网的情况看第 6 节。

### 4.5 三条边界与坏习惯

- **别用管理员权限全局装包**。`sudo pip install`、管理员 PowerShell 里 `pip install`，装进的是系统解释器，会把整台机器的环境搞脏，而且以后很难还原。
- **别在同一个环境里装冲突的版本**。`pip` 不会阻止你把一个包降级到另一个包不接受的版本，它只在装的时候对依赖做一次检查。跑起来才炸是常态。
- **别不记版本**。只写 `requests` 而不写版本，今天装出 2.32、半年后装出 3.0，行为可能变。学习阶段无所谓，一旦代码要交给别人，就要锁版本。

## 5. uv：同一件事的另一种做法

`uv` 是一个用 Rust 写的 Python 包与项目管理器。它不替代 Python，替代的是"建环境 + 装包 + 跑命令"这一套动作。

同一件事的对应关系：

| 你要做的事 | 传统做法（本课主线） | uv 的做法 |
|---|---|---|
| 建虚拟环境 | `python -m venv .venv`（实测 4.3–4.8 秒） | `uv venv`（实测 0.1 秒） |
| 装包 | `python -m pip install 包名` | `uv add 包名`（会写进项目配置）；或 `uv pip install 包名`（更接近 pip） |
| 用环境里的解释器跑 | 激活后 `python 脚本.py` | `uv run python 脚本.py`（不激活，临时改 `PATH`） |
| 装环境里的 pip | 自带 | 不装（实测没有 `pip.exe`） |

为什么快：它自己维护一个全局的包缓存，同一个包在第二个项目里只做链接，不重复下载和解压；建环境时也不跑 `ensurepip` 那一套。实测的 0.1 秒和 4.3 秒就是这个差别，不是测量误差。

那还要不要学传统做法？要。理由是三条现实情况：

1. 学校机房、公司老项目、别人给你的脚本，给的都是 `requirements.txt` 和 `python -m venv`；
2. `uv add` 需要有项目配置文件（第 26 讲的 `pyproject.toml`）才能正常用，而你现在还没有；
3. 出一问题时，你必须知道底层在干什么，才能判断是 uv 的问题还是环境的问题。

所以本课程的主线是 `venv` + `pip`，uv 作为"知道有、用得上的时候用"的加速器。两者建出来的环境结构几乎一样（实测 `include-system-site-packages = false` 相同），所以切换成本很低。

## 6. 三种恶劣环境怎么办

| 场景 | 现象 | 可行路径 |
|---|---|---|
| 没有管理员权限 | 安装器要提权，装不进去 | 安装时选 "Install for me only"，装到用户目录；虚拟环境也建在用户目录或项目目录里 |
| 没有网络 | `pip install` 超时、`Could not find a version` | 提前在有网的机器上 `pip download 包名 -d wheels` 下好 wheel 文件，拷过去用 `--no-index --find-links=wheels` 安装 |
| 机房还原卡 | 重启后装的东西全没了 | 把项目和 `.venv` 一起放在 U 盘 / 网盘里；或写一个几行的重建脚本，每次开机跑一遍；或用便携版解释器 |

三条都不用记细节，知道"有这些路"就够，需要时再回来看这一节。

顺带说清一个容易混的东西：官网提供的 "Windows embeddable package"（嵌入版）是给"把 Python 嵌进别的程序"用的，它默认没有 `pip`、也不能直接建虚拟环境，不适合当日常开发环境。想便携，用第三方的便携版，或者干脆把 `.venv` 拷在 U 盘里。

## 7. 环境出问题时的诊断顺序

按这个顺序查，五步之内基本能定位：

1. `python --version` —— 命令都找不到，是 `PATH` 问题（第 02 讲）。
2. `where.exe python`（Windows）或 `which python3` —— 找到的是不是你以为的那个。
3. `python -c "import sys; print(sys.executable)"` —— 路径是否在项目目录里。
4. `python -c "import sys; print(sys.prefix, sys.base_prefix)"` —— 两个值相等说明**不在**虚拟环境里，你以为的隔离没生效。
5. `python -m pip list` —— 包到底装在这个环境里，还是装到别处去了。

五条都是只读命令，不会改变任何东西，可以放心跑。

## 8. 这一讲留下的东西

- 环境 = 一个解释器 + 一份 `site-packages`；`venv` 就是把这两样装进一个目录，让它只属于这个项目。
- 激活只改 `PATH`（外加两个环境变量和提示符）；不激活，用绝对路径一样能用。
- `pyvenv.cfg` 是这个环境的出生证明，`home` 决定母本，`include-system-site-packages` 决定隔离是否漏。
- `pip` 住在环境里，`python -m pip` 比裸 `pip` 更可靠；不是每个环境都有 pip（uv 建的就没有）。
- uv 把同样的事做到 0.1 秒，但本课主线仍是 `venv` + `pip`：机房和别人的项目都按那套走。

下一讲换一个方向：代码会越改越乱，改坏了想退回去怎么办。

## 小结

- 官网安装器第一屏的 "Add python.exe to PATH" 必须勾，勾完要新开终端；没有管理员权限就选"只为我安装"。
- 验证环境的三条命令：`python --version`、`where.exe python`、`python -c "import sys; print(sys.executable)"`。
- `python -m venv .venv` 生成 `Scripts/`、`Lib/site-packages/`、`pyvenv.cfg`、`Include/` 四样；本机实测 4.3–4.8 秒。
- 激活脚本做的核心一件事是把环境的 `Scripts` 插到 `PATH` 最前面；不激活直接写绝对路径同样有效。
- 判断"我在哪个环境"看 `sys.prefix` 与 `sys.base_prefix` 是否相等，比看提示符可靠。
- 环境可删（删目录即干净），不可随意移动（路径写死在配置与脚本里），不该提交进 git。
- `pip` 是环境里的程序，`python -m pip` 能保证装到"这个"环境；uv 建的环境默认没有 pip。
- 无网络用离线 wheel 与 `--no-index --find-links`，无权限用用户级安装，还原卡用便携环境或重建脚本。

## 作业

**Q1.** 你在项目目录里执行了 `python -m venv .venv`，然后直接在新开的终端里敲 `pip install requests`，装完运行脚本却报 `ModuleNotFoundError: No module named 'requests'`。为什么？给出两种正确写法。

**参考答案：** 因为你没有激活环境，裸 `pip` 用的是 `PATH` 里找到的那个 pip，很可能装进了另一个环境（或全局），而运行脚本用的解释器不是那个环境。

两种正确写法：(1) 先激活再装：`.\.venv\Scripts\Activate.ps1`，然后 `pip install requests`；(2) 不激活，直接指定解释器：`.\.venv\Scripts\python.exe -m pip install requests`。

验证：装完用 `.\.venv\Scripts\python.exe -m pip list` 看清单里有没有 `requests`。

**Q2.** 有人送你一个项目文件夹，里面带一个 `.venv` 目录。他把它压缩、拷到你的 D 盘解压，然后说"直接运行就行"。可能出什么问题？

**参考答案：** 大概率跑不起来或行为异常。虚拟环境里的 `pyvenv.cfg`、激活脚本、`Scripts` 下的启动文件都记着创建时使用的绝对路径（本讲实测 `pyvenv.cfg` 里有 `home`、`executable`、`command` 三行绝对路径）。换盘符、换目录后这些路径失效，解释器可能找不到标准库或找不到母本。

正确做法：删掉他给的 `.venv`，在他提供的依赖清单（`requirements.txt` 或 `pyproject.toml`）基础上，在你自己的机器上重建一个。

**Q3.** `python -m venv` 和 `uv venv` 建出来的环境，本讲实测有两个明显差别。分别是什么？

**参考答案：** (1) 速度：本机实测 `python -m venv` 用 4.3–4.8 秒，`uv venv` 用 0.1 秒；(2) 内容：标准库建的带 pip（实测 25.0.1，`Scripts` 里有 `pip.exe`），uv 建的没有 pip（`Scripts` 里没有 `pip.exe`，`import pip` 报 `ModuleNotFoundError`）。

两者的目录结构和隔离设置是一样的：都有 `Scripts`、`Lib/site-packages`、`pyvenv.cfg`，且 `include-system-site-packages = false`。

**Q4.** 用三条只读命令判断"我现在到底跑在哪个环境里"。

**参考答案：** 依次跑下面三条只读命令：

```powershell
python -c "import sys; print(sys.executable)"
python -c "import sys; print(sys.prefix)"
python -c "import sys; print(sys.prefix == sys.base_prefix)"
```

第一条给出解释器的绝对路径，第二条给出环境的根目录，第三条输出 `False` 说明在虚拟环境里、`True` 说明用的是基础安装。

补充：还可以用 `python -m pip list` 看这个环境装了什么，与前两条互相印证。

**Q5.** 机房电脑不允许装软件、也没有管理员权限，但你需要跑一个依赖第三方库的脚本。给出两条可行路径，并说出各自的代价。

**参考答案：** (1) 用"只为我安装"的方式装 Python（装到用户目录，不需要管理员权限），再在项目目录建虚拟环境装包——代价是占用户目录空间，且换机器要重来；(2) 在有网的机器上把包下载成 wheel（`pip download 包名 -d wheels`），和便携版解释器一起拷到 U 盘，在机房用 `--no-index --find-links=wheels` 离线安装——代价是要提前准备，且 wheel 必须和机房的 Python 版本、系统位数匹配（例如 `cp312-win_amd64` 的包不能装在 3.11 上）。

**Q6.** 用自己的话解释：`include-system-site-packages = false` 这一行在管什么？把它改成 `true` 会发生什么？

**参考答案：** 它管"这个虚拟环境看不看得见全局安装的包"。设成 `false`（默认）时，`sys.path` 里只有这个环境自己的 `site-packages`，全局装的包对它不可见，隔离完整；改成 `true` 后，解释器会额外把全局的 `site-packages` 加进搜索路径，于是"全局装过的包在这个环境里也能 import"。

代价是隔离被打破：你在这个环境里看到的不一定是你装的，换台机器或别人帮你查问题时会对不上。日常开发保持 `false`。
