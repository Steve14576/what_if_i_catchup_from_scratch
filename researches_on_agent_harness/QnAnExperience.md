# QnAnExperience

> 一些知识性问题与具体工程问题的追问和答疑，它们流落在原始上下文中比较零散，甚至仍未成型，现在沉淀。一般都是追加式，当然也不排除删改。
> 不同条目具体地分点，一定要分点。且这是用户的追问和答疑，不是agent的默认的过程记录册。
> 此文档的定位就是卡片笔记，适当的也要引原文出处(如果有的话)。但是也不要怕单个点写长，如果它本身就值得详细讲的话。此文档可以应对"不知道自己不知道什么"的问题，通过用户自己问，或者从实践中意识到的，明确或有待发掘的好问题，对它们尽可能见一个记一个。
>
> - 知识性的内容全都是事实性的没有太多依赖问题，追加式。不要官腔，面向给用户的，怎么清楚怎么讲。
> - 工程性内容可能有返工但是一般不直接覆盖，所以要写清楚前提条件，删改也要写清楚当时是为什么现在是为什么，有点像ADR的意思但是没那么官腔和死板格式与行业黑话，否则用户看不懂。这条适用于当这个项目是具体的工程项目。如果这是学习项目，那反正，思路也能借鉴。
> - 这，特么的，不是，研发台账。
> - 分点记录。比如A1，A2 etc.

---

## A. 从sessions中沉淀的

> session中都会说人话，这里保持，不要擅自精简，不要吞内容或者说黑话，甚至可以适当扩一点。

> **本组前提（A1–A12 共用）**：来自 2026-10-06 至 10-08 一次针对"coding agent 的仓库级理解与记忆机制"的连续追问，观测机器是用户本机 Windows。凡涉及进程 PID、目录内容、行数、扩展版本号的都是**当时实测**；PID 会变、版本会升级，任何依赖这些的判断都要**当场重取**。第三方来源（非官方文档）逐条标注。
>
> **排列原则（用户 2026-10-08 定）**：按**提问出现的先后顺序**排，一条一轮问答，顺序读下来不跳来跳去。因此**后一轮修正前一轮的地方，修正写在后一轮里，不回改前一轮**——这样既保持顺序，又保留"当时怎么想、后来怎么改"的痕迹。

---

### A1【第 1 轮】Qoder 的"仓库级理解"到底靠什么？有一个默认在跑的本地/云服务在做它吗（不是 QMind，也不是 Repo Wiki）？

**问的是**：当前用到的是哪个？有本地服务/进程/本地 MCP server 吗？仓库级理解究竟怎么做到的？QMind 知识库和 Repo Wiki 是单独功能吧（用户说自己没建立、也没指望过这两个）？Qoder IDE 究竟是怎么保持"仓库级印象"的？

**结论（分点）**：

1. **有一个默认随 IDE 起来的本地组件**：`qoder-search.bundle.mjs daemon-server`（那次实测 PID 37680），陪伴一个同引擎的 `qoder-search.bundle.mjs mcp-bridge`（PID 42192）。它们属于 `qoder-context` 插件——**和 QMind、Repo Wiki 都不是一回事**。
2. 它对外暴露为 `SearchCodebase`（语义检索）和 `SearchSymbol`（符号与关系）。→ 也就是说，它是**"一个能查的索引"，不是"常驻在上下文里的理解"**；要主动调用才生效。
3. **策略是云端下发的**：命名空间 `codebase-features` 的 feature flag 经 SSE 从 `openapi.qoder.sh/.../qcs/config/stream` 拉取（断网时会循环刷 `ENOTFOUND`）。**代码不上云，配置下云。**
4. **它是租约式存活**：日志里有 `daemon shutdown grace started, reason: "last-client-lease-expired", delay 30000ms`——最后一个客户端租约过期 **30 秒后自己退出**。所以"现在开着"是真的，但它**不是系统级常驻服务**，是随 IDE 会话活。
5. **一个当时的错误推断（保留在此，如实记录顺序）**：我因为"日志里 0 次提到本仓库名""workspaceStorage 里没有索引目录""`.qoder/projects/` 里没有本仓库条目"，推断"本仓库大概没建过索引"。→ **这条后来被第 5 轮直接推翻**，见 A5；根因分析见 A12。
6. QMind 与 Repo Wiki 确实是与它并列的另外两件事（对照表见 A8）。

### A2【第 2 轮】Kilo Code、Codex、Claude Code 有类似的功能吗？

**结论（初查，按当时口径）**：

1. **Kilo Code：有索引**——叫 Codebase Indexing，机制是 Tree-sitter 解析 + embedding + 向量库；**但默认关闭**，要显式开。向量库可选 **LanceDB（嵌入式、不用另起服务）或 Qdrant（外部服务）**。
2. **Claude Code：没有索引**，而且**这是故意的**——它主张 agentic search，按需 grep/glob/read，不做 embedding。
3. **Codex：没有**——官方仓库里"加语义索引"的需求**至今仍是 open 的 issue**，社区一致说法是它就跑 ripgrep。
4. 注意：这一轮只是初查（联网 + 部分本机）。"默认关/默认开"是**后面才逐条核准的**；Kilo 的记忆机制、Claude 和 Codex 的记忆机制分别在 A10、A11。

### A3【第 3 轮】"装没装的都去查"——本机清点

**结论（本机实测）**：

1. **Claude Code：装了，在 VS Code 里**——扩展 `anthropic.claude-code-2.1.267-win32-x64`，扩展内**自带原生 `claude.exe`（220MB）**。所以"PATH 里没有 `claude`"不等于没装。但 `~/.claude/` 下**只有 `ide/54055.lock`**（IDE 集成握手文件，含 `pid`/`workspaceFolders`/`ideName`/`transport`，以及一个本地 `authToken` 字段，**不外传**）；**没有 `~/.claude.json`，也没有 `~/.claude/projects/`** → 只发生过握手，**没留下实际会话**。
2. **Kilo Code：装了，在 Qoder 里**——扩展 `kilocode.kilo-code-7.8.3`，另有 3 个 `kilo.exe serve` 进程在跑。配置与状态：`~/.config/kilo/kilo.jsonc`、`~/.local/share/kilo/`（`kilo.db` 462KB + 4.1MB WAL、`memory/`、`repos/` 为空）、`~/.local/state/kilo/`。
3. **没装**：Codex、Cursor、Windsurf、Trae、Cline、Roo、Gemini CLI、Aider、opencode。
4. **包管理器**：有 `winget`、`uv`；**没有 `npm` / `pip` / `scoop` / `choco` / `pnpm` / `yarn` / `bun`** → 所以不存在 npm 全局安装的 CLI。
5. 本机**装了两套 Qoder**（`C:\Program Files\Qoder IDE\` 与 `E:\E_MyApps\App-NewQoder\Qoder\`）→ 所以 qmind / qoder-search **可能不止一套在跑**，无法确证同时跑几套。
6. 顺带发现：本仓库里存在 `.kilo/worktrees/noble-grease/`——一份 **Kilo 的 git worktree 副本**，内容是**治理前的旧文本**（冻结快照，不会跟着正文改）。

### A4【第 4 轮】再确认一下：Qoder 真有一个"现在就在跑的、做仓库级理解的服务"对吗？Kilo Code 有吗？

**结论**：

1. **Qoder：有**。就是 A1 里那组 `qoder-search` daemon——**它与 QMind、Repo Wiki 都无关**；执行在本地、策略在云、按客户端租约存活。
2. **Kilo Code：有本地服务进程**（`kilo.exe serve`），**但仓库索引默认不建**（要显式开）。它默认在替 agent 干的事其实是**记忆**（详见 A10）。
3. 两家的结构很像：**一个常驻本地服务 + 一套记忆 + 一个可选索引**。差别在默认值——**Kilo 的索引是显式关闭的**。

### A5【第 5 轮】"这个功能之前一次都没用过吗？那你现在用一次"——索引实测（决定性，且推翻 A1 的推断）

**做法**：直接调用一次 `SearchCodebase`。它返回了索引状态头：

```text
workspace="e:\\E_Vault\\CC_Formed_Projs2\\WHATIFICATCHUPFROMSCRATCH" state=completed progress=finish vector=finish graph=finish
```

**结论（分点）**：

1. **本仓库的索引是 `completed`**——**不是这次调用才建的**（直接给的完成态，没有 In-progress 过渡）。→ **A1 第 5 点"没建索引"的推断是错的**。
2. 索引有 **`vector`** 和 **`graph`** 两条线，都 `finish`。**`graph` 的含义未验证**：我只知道构建管线里有一个叫 graph 的阶段，它建的是什么图、检索时怎么用，**不知道，不下结论**。
3. **检索质量分两极（实测）**：
   - 好的例子：问"三要素法 / 一阶电路 / 时间常数"→ 命中了 `scripts/lec11-01_verify_full_response.py` 里的三要素代码段，以及 10 讲讲 τ 的那几节。**这是关键词匹配做不到的**，说明语义检索确实在工作。
   - 坏的例子：问"预写结论和实测不一致怎么处理"→ 返回 9 条里 **8 条**是 `trash/`、`wiicufs_backups/`、`.kilo/worktrees/` 里的**陈旧副本**，真正的正文一条都没进前列。
4. → **结论：索引没有排除 `trash/`、备份目录、worktree 目录**，语义检索被废料挤占。修法是在 `Settings → Codebase Indexing → Index Exclusions` 加排除——**这属于用户的环境配置，不擅自动**。

### A6【第 6 轮】记忆读写是不是也有个服务像"按钮"一样接住（不用每次手动 PowerShell）？记忆那边还有没有负责 RAG 的服务？

**结论（分点）**：

1. **是，有服务接住**。我读写记忆用的是 `UpdateMemory`（create/update/delete）和 `SearchMemory`（fetch / search / explore），**全程不需要 PowerShell**。链路是：

   ```text
   我 → 本地 mcp-router（http://127.0.0.1:62974）
      → qoder-qmind-mcp-server.cjs（日志角色名 mcp-courier）
      → qoder-qmind-daemon.cjs（真正读写）
      → 落盘 ~/.qoder/memories/**.md
   ```
2. **它和文件操作是平级的**：文件用 `Read`/`SearchReplace`，记忆用 `SearchMemory`/`UpdateMemory`。而且记忆那套还带 schema（分类枚举 31 种、字数区间、内容质量原则），比文件工具更"有脑子"。
3. **"按相关性按需加载"确实有**，分两层：

   - **常驻骨架**：每轮注入的概览与知识树（只有标题 + 关键词），成本低；
   - **按需召回**：`SearchMemory` 的三种模式（fetch 按标题精确 / search 广召回 / explore 只要树结构）。
4. **但"它是 RAG"这条不成立（至少无证据）**：`SearchMemory` 的 search 模式**自述是 "broad keyword-based recall"**（关键词，不是向量相似度）；落盘全是 md、**没有任何索引产物**；`qmind-mcp.log` 尾部**只有 token/认证/投递事件**，没有 recall/search/inject 这类检索事件。→ 可以说它"有服务化的记忆通道 + 按相关性召回"，**不能说**它是向量库或 GraphRAG。daemon 内部是否另有一层缓存，我没打开实现代码，**不可知**。

### A7【第 7 轮】记忆是本地落盘的吗？管理记忆的是一个独立的进程或服务吗？

**结论（分点）**：

1. **是本地落盘，而且是纯 markdown**：位置 `C:\Users\Administrator\.qoder\memories\<账号目录>\`，下分两级——`global\<分类>\*.md`（实测 31 个分类）与 `projects\<编码后的仓库路径>\*.md`。**没有任何 sqlite / embedding / 索引文件** → **明文可读、可手改**（"服务接住"≠"黑箱"）。
2. **是独立进程，而且是两个**：`qoder-qmind-daemon.cjs`（真正读写记忆；本会话三次观测 PID 分别是 33044 → 43980 → 30312）+ `qoder-qmind-mcp-server.cjs`（MCP 入口，角色 `mcp-courier`；它收到的鉴权事件被标 `disposition: "ignored-non-authoritative"`，即**它不是权威方**）。
3. **但不是系统级服务**：这两个都是 `Qoder.exe`（扩展宿主）的**子进程，IDE 退出即结束**；PID 会变，说明会被重启拉起。
4. **唯一在云上的一环是鉴权**：日志反复出现 `QMind Service token update delivered to the Daemon`、`authState: "signed-in"`。→ **记忆内容在本地，token 在云**。
5. 一个小异常（只报事实）：`.qoder` 下**同时存在 `memories`（复数）和 `memory`（单数）两个目录**，单数那个是**空的**，实际生效的是复数；单数为何被创建**不知道**。
6. **附：上一轮说的"按当前问题自动预召回"，活体证据长这样**（它不需要 agent 调任何工具，是系统在读当前 prompt 后自动注入的）：

   ```text
   ## Trigger  type: agent_task_start
   content: Pre-recall based on the user's current prompt
   <relevant_memory_details> …两条记忆全文… </relevant_memory_details>
   ```

   **待确认**：这个预召回由谁计算（QMind 服务？还是 IDE 侧构造请求时做的）、注入有没有预算上限——**都没查到**。（对照：Claude Code 文档明写了 25KB / 200 行硬限，Qoder 这边没有对应文字。）

### A8【第 8 轮】再顺一遍：Qoder 默认开启的、除 QMind/RepoWiki 之外的"记忆管理服务"和"语义代码库索引服务"，分别是什么？

**先纠正提法**：**QMind 不是"记忆以外"的东西，它就是 Qoder 记忆管理那一套的名字**（`qoder.knowledge.center` 插件）。所以真正"除 QMind、Repo Wiki 之外"的独立一套，只有**仓库语义索引**。

**结论**：默认在跑的是**两组「daemon + MCP 接口」**，经本地 mcp-router（`http://127.0.0.1:62974`）分发；`mcp.json` 是空的 `{"mcpServers": {}}`，说明这些 MCP **全是内建的**。

| 名字                                  | 归哪个插件                 | 干什么                    | 默认                             | 形态                                   |
| ------------------------------------- | -------------------------- | ------------------------- | -------------------------------- | -------------------------------------- |
| **Codebase Indexing**           | `qoder-context`          | 语义代码检索 + 符号 graph | **默认起**（策略云端下发） | daemon + mcp-bridge                    |
| **Memory**（QMind）             | `qoder.knowledge.center` | 记忆读写 / 召回           | **默认起**                 | daemon + mcp-server                    |
| **Repo Wiki + Knowledge Cards** | 未验证归属                 | 生成结构化文档 / 知识卡   | **默认关**（需手动开）     | **未观测到专属进程**，按需本地跑 |

**Repo Wiki 的官方要点**：产物在 `<项目根>/.qoder/repowiki/`；**只支持至少有一次 commit 的 Git 仓库**；项目上限 **10,000 文件**；生成在**本地**跑、不上传整仓库；可用 `/knowledge` 干预、用 `wiki_plan.yaml` 预配置；**默认关闭**。

**两条独立证据互证**：Repo Wiki 文档写的"10,000 文件上限"，与本地日志里的 `maxFileCount: 10000` **完全吻合**。

**本仓库实测**：根目录下**连 `.qoder\` 都没有** → Repo Wiki **从未生成过**（这不是推断，是实测）。

**待确认**：Repo Wiki 归哪个插件、是否复用 QMind 的 knowledge cards，**我没验证**。

### A9【第 9 轮】它们能"接住"主 agent 吗？能减少注意力开销、让它专心正事吗？

**结论（分点）**：

1. **接住的是"动作"，不是"判断"**：
   - 接住的：记忆——不用 grep 一堆 md 手工拼上下文，`SearchMemory` 一次给全文；写入——一个 `UpdateMemory` 调用，不用手写文件、维护分类目录。代码定位——不用"猜词→grep→读→再猜"多轮迭代，`SearchCodebase` 一次语义查询拿文件 + 行区间。
   - 没接住的：**什么时候查、记什么、它给的东西可不可信**——仍然是主 agent 的判断。服务不做质量把关；它的约束条款（"不要随便写""少而精"）是**写给 agent 的纪律**，说明判断在 agent 这边。
2. **三笔隐形账单（都在本次会话里出现过）**：
   - **注入是静默的预算消耗**：常驻骨架 + 预召回全文，每轮/每任务自动发生；"少动手"的代价是"视野被它替你选了"，成本落在上下文里。
   - **索引不干净时，省下的时间会被读废料吃掉**：A5 里"9 条 8 条废料"就是例证——**废料比没有更危险**，因为它看起来相关。
   - **索引有滞后，grep 没有**：索引按 **60 秒**周期增量刷新；grep/read 读的是磁盘当下字节。
3. → **准确结论**：服务把"体力活"接走了，但注意力开销**只是换了形态**。净收益取决于三条：**索引干不干净、召回准不准、注入预算严不严**。

### A10【第 10 轮】Kilo Code、Zoo Code 分别有对应的机制吗？

**Kilo Code**：

1. **索引（官方文档 `kilo.ai/docs/customize/context/codebase-indexing`）**：Tree-sitter 解析出语义块（函数/类/方法，块 100–1000 字符）→ 生成 embedding → 存向量库 → 给 agent 一个 `semantic_search` 工具。
   - 向量库**可选 LanceDB（嵌入式、无服务、默认）或 Qdrant（外部服务）**；Embedding 提供方支持 OpenAI / Ollama（本地免费）/ Gemini / Mistral / Voyage（`voyage-code-3` 专调代码）/ Bedrock / OpenRouter 等。
   - **默认关闭**，官方明说"配了 embedding provider 也不会自动开始索引"，必须显式开。自动过滤：二进制、图片、>1MB、`.git`、`node_modules`/`vendor`、`.gitignore`/`.kilocodeignore` 命中项。
   - 历史可参考：v7 重写时索引被砍，社区要回来，2026-06 从 experimental 转正（出处 `blog.kilo.ai/p/codebase-indexing-is-back-in-kilo`）。
   - 本机对照：扩展 7.8.3 + 3 个 `kilo.exe serve` 在跑；但 `kilo.jsonc` 里**没有 `indexing` 键**、`~/.local/share/kilo/repos/` 为空 → **能力在，这台没启用**。
2. **记忆分"两代"，别混**：
   - **第一代 Memory Bank 已被官方弃用** → 改用 `AGENTS.md`（出处 `kilo.ai/docs/customize/agents-md`，原文 "The Kilo Code memory bank feature has been deprecated in favor of AGENTS.md"）。原内容在 `.kilo/rules/memory-bank/`（旧版 `.kilocode/rules/memory-bank/`）。现在的指令优先级：agent 专属 prompt > 项目 instructions > **AGENTS.md** > 全局 instructions > skills（按需）；子目录的 `AGENTS.md` 在读到该目录文件时**动态注入**（以 `<system-reminder>` 形式），且 `AGENTS.md` **写保护**。
   - **第二代是一个引擎级记忆——本机实测到，但官方文档里没找到对应说明**：

     ```text
     ~/.local/share/kilo/memory/<仓库名>-<哈希>/
         manifest.json     kind: "kilo-memory"
         project.md        # Facts / Decisions / Constraints / Open Questions
         environment.md    # Commands / Paths / Tooling
         corrections.md    # Corrections
         state.json        # autoInject:true, autoConsolidate:true,
                           # capture:{mode:"selective", turnClose, explicit},
                           # stats:{lastInjectedTokens, lastConsolidationTokens, lastRecallCount…}
         index.kmem        # 头部署名行：kilo-memory-v1 / context_not_instruction
     ```

     两个细节：① 它**自动注入 + 自动合并 + 召回计数**，比 Qoder 更自动化；② `index.kmem` 头部那行 **`context_not_instruction`** 是**显式的注入防护**——声明这段内容是"背景"不是"指令"，这一点比 Qoder 更明示。
   - **推断（待确认）**：这套 `.kmem` 记忆很可能是 v7 迁移到 **opencode** 架构时带进来的——旁证是扩展里有 `docs/opencode-migration-plan.md` 与 `log/opencode.log`。**我不知道对不对。**
   - 附带：`kilo.jsonc` 的权限模型很细（`read/edit/glob/grep/list/bash` 分类，bash 逐命令列白名单，`*>*` 要问，另有 `doom_loop: "ask"` 防死循环、`external_directory: "ask"`）。
3. **Kilo 与 Qoder 的关系**：它是这批里**最接近 Qoder 的**——索引那套用**嵌入式向量库**，比 Roo 一脉更"免运维"；记忆比 Qoder 更自动。区别只在默认值：**它的索引默认关**。

**Zoo Code（Roo Code 的 fork，`docs.zoocode.dev`）**：

1. 首页自述哲学是"**trade tokens for quality**""别省 token"——**与"减少注意力开销"是相反的取向**。
2. **索引**：有 Codebase Indexing，机制是 embedding + 语义搜索；但**向量库是 Qdrant，需要你自己跑**（Docker 或 Qdrant Cloud）。Roo 仓库的相关 issue 明说代价：Qdrant **配置要 30–60 分钟、额外占 500MB+ 内存**（对比嵌入式方案只要 5 分钟）。Kilo 正是拿"默认 LanceDB 免服务"来区别自己的。
3. **记忆**：**没有内置引擎**，一个 session 从干净上下文开始。通行做法是**社区项目 Memory Bank**（`GreatScottyMac/roo-code-memory-bank`）——本质是**一组 markdown + 一套让模型去读的规则**，是"约定"不是"服务"；或者挂第三方 MCP 记忆服务器。
4. 另有 Modes（Architect/Code/Ask/Debug/Orchestrator）、Checkpoints、Todo Lists、MCP。
5. **注意**：本机**没装 Zoo Code**，以上全是**文档/搜索级判断**，**无本机实证**；它的索引默认开关**未逐字核实**。

### A11【第 11 轮】Claude Code 和 Codex 有这样的东西吗？

**Claude Code**：

1. **索引：没有，而且这是故意的**。不建索引、不做 embedding，主张 **agentic search**（按需 grep/glob/read）。理由（多家来源一致复述）：**索引会滞后，现场 grep 读的是磁盘当下字节**——改完文件 100ms 后再问，它读到的是新内容；向量索引在那个瞬间是旧的。→ **没有索引进程、没有索引服务、没有索引 MCP**。
2. **记忆：有，但形态是"文件 + agent 自己写"**，不是服务：
   - 位置 `~/.claude/projects/<仓库名>/memory/`，每个项目一个文件夹，**跨会话持久**。
   - 两套系统，**别混**：**`CLAUDE.md`** 是**你写的**规则（三层作用域：组织托管 / 个人 `~/.claude/CLAUDE.md` / 项目 `./CLAUDE.md`；**全文加载、没有 200 行截断**，只有超过 4 MiB 会被跳过，官方建议控制在 200 行以内）；**`MEMORY.md` + 主题文件**是**Claude 自己写的**（`MEMORY.md` 是索引，会话开头注入，**硬上限 200 行 / 25KB 先到者为准，超了静默截断**——警告只写在文件里，模型看不到；记忆分 4 类：`user` / `feedback` / `project` / `reference`）。
   - **写入者有两个**（第三方来源，未能本机复现）：① 主 agent 会话中用普通文件工具直接写；② 一个**会话结束后运行的后台抽取 agent**（源码 `extract-memories`，feature flag `EXTRACT_MEMORIES`）：读 transcript → 合并新事实 → **删掉被推翻的笔记** → 把索引压回 200 行以内。业界把这套叫 **"Auto Dream"**，触发是双闸门（距上次合并约 **24 小时** 且新增至少 **5 个会话**）。
   - **关键**：即便如此，它仍然是"agent 亲自管记忆"——**没有 MCP、没有检索服务、没有向量**，读也是"模型自己读文件名/读文件"。→ 对"减少注意力开销"，Claude Code **不接**。

**Codex**：

1. **索引：没有**——官方仓库里 `codex index` / `codex search` 的需求**至今仍是 open 的 enhancement issue**（`github.com/openai/codex/issues/5181`，2025-10 开）。社区一致说法：**Codex CLI 就是跑 ripgrep**。
2. **记忆**：`AGENTS.md` 层级（`~/.codex/AGENTS.md` 全局 + 仓库根 + 子目录）；另有 **Memories**：`~/.codex/memories/` 里**一组固定的 markdown 文件**，用 `/memories` 控制，本地保存、**git/branch 感知**、会检查是否过期。**没有向量库，也不走 MCP。**
3. **来源冲突，如实记**：一边（2026-04）说"Codex 没有内置持久记忆，每个会话从零开始"，另一边（2026-05 起）说"记忆就在 `~/.codex/memories/`"。→ 说明它是**新加的、可能仍是实验特性**，时间点不同结论相反。
4. **本地服务：有 `codex app-server`，但职责是客户端集成**。官方文档把它描述为"Codex 用来支撑富客户端（例如 Codex VS Code 扩展）的接口"；第三方插件文档提到"当 TUI 挂在 codex app-server daemon 上时，会话结束事件会推迟到线程被卸载（**30 分钟**）或 daemon 关闭"。→ **它确实是个 local daemon，但跟仓库索引和记忆都无关。**
5. **MCP 是双向的**：Codex 能**消费**你配的 MCP server（`config.toml`），也能**把自己当 MCP server 跑**（`codex mcp`）给别人调。**但记忆不走 MCP。**
6. 本机**没装 Codex**；`~/.codex` 不存在。

### A12【收尾】这次的总图和翻车点

**一句话分野**（这批工具在"仓库理解 + 记忆"上的总图）：

- **托管派（Qoder、Kilo Code）**：索引和记忆都做成**常驻本地服务 + 专用工具（MCP）**，主 agent 一次调用拿结果。
- **文件派（Claude Code、Codex）**：**不建索引**；记忆是**一堆 markdown 文件**，靠主 agent 用通用文件工具自己读写，没有记忆服务、也没有记忆的 MCP。
- 一句话记法：**Qoder/Kilo 是"把视野托管出去"，Claude Code/Codex 是"视野自己长在手上"。** 托管派省"动作次数"，文件派省"配置与维护"，但两边的"注意力开销"都没真正消失（见 A9）。

**这次的翻车点与方法论（值得记）**：

1. **"看不到索引产物"不等于"没有索引"**（A1 → A5）。根因：**`qoder-search` 的日志本来就不记录 workspace 名**，所以"名字没出现"从一开始就不构成证据。**把"某处没记录"当成"某处没发生"，是逻辑漏洞。**
2. **查询范围要覆盖隐藏目录**：`.kilo/worktrees/noble-grease/` 这份整份副本，是我在语义检索结果里才发现的——因为前面只查了 `.qoder`，**从没列过仓库根下的隐藏目录**。
3. **先做可判定的探针，再下结论**：真正解决问题的是"直接调用一次 `SearchCodebase`"，它一次就把"有没有索引"变成了事实（返回 `state=completed`），胜过前面所有间接推断。
4. **第三方来源必须标出来**：Claude Code 的 Auto Dream / extract-memories 来自 mem0 的文章；Codex 的 app-server 细节来自官方文档标题 + 第三方描述；Zoo Code 全部来自文档——**这些都没能在本机复现**，条目里已分别标注。
