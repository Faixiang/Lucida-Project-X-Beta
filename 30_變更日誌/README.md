# 30_變更日誌

按日期记录本仓库及其对应项目的变更。**仅记录有实际改动之日**，无改动不写。

## 格式

```
## YYYY-MM-DD

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 清单 / 工程 / 决策 | 文件或模块 | 新增或改了什么 | 哪条裁定或授权 |
```

## 记录

## 2026-10-28

上游基线：`activepieces` branch `main`，commit `280f6bb396f1fa55aed9267ca022429fd138a461`（2026-10-27）。

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 工程 | `20_工程/ee-strip-scan.py` | E-01 入库：EE 规模 / 引用 / 硬耦合 / 遥测的只读扫描器；支持 `--repo` `--out`，输出 md + json | 用户确认先改本地再同步 |
| 工程 | `20_工程/README.md` | E-01 状态改为已入库，补用法、实测基线与判定口径 | 同上 |
| 清单 | `10_清單/activepieces-EE剥离清单与保留清单.md` | 勘误第二章：引用 333→329、文件 157→155；community 20→0、sandbox 2→0、web 4→5；遥测计数改为 25 行 / 8 处 SDK 调用；新增第八章勘误记录 | E-01 复跑结果 |
| 清单 | `10_清單/README.md` | 索引摘要同步勘误值 | 同上 |

勘误成因：旧正则以裸 `ee-` 子串判定 EE 引用，`find-free-slots`、`json-tree-skeleton`、`employee-terminated`、`tree-kill`、`...migrate-ee-users-to-oldest-platform` 等 26 处普通文件被误判；同时逐行匹配漏掉 4 处多行 `ee-embed-sdk` import。新脚本改为全文语句级匹配 + 包名精确判定，复跑后 EE 规模 263/34,240、四处结构性注册点 46/22/20/21、三处业务硬耦合全部与清单原值一致。

### 第二批复核与低风险落地

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 源码 | `activepieces` 工作区 | 提交 `165a9e52`：移除 `fathom` / `actualbudget` / `vapi` 三个社区 piece 共 83 文件，同步 `tsconfig.base.json` 与 `bun.lock`（-56 包） | 前序许可硬冲突处置收尾 |
| 源码 | `activepieces/NOTICE.md` | 提交 `9e4586fd`：许可分区、本副本未分发状态、第三方组件声明（openpgp LGPL-3.0+、pizzip/jszip 择 MIT）、商标声明 | 履行根 LICENSE 第 2 条声明义务 |
| 源码 | `activepieces/verify-preflight.ps1` | 提交 `9e4586fd`：只读预检 7 项，阻断项返回退出码 1 | 建立发布前闸门 |
| 备份 | `P:\Github\_backup\activepieces.git` | 新建本地裸仓库并推送 `main`=`9e4586fd`；源仓为浅克隆，bare 侧已开 `receive.shallowUpdate` | 用户要求改动不留单点 |
| 备份 | `P:\Github\_backup\activepieces-git-20261028` | `.git` 目录物理副本 95.6 MB | 同上 |
| 决策 | fork 方案 | **否决**公开 fork：GitHub 仅允许把 public 仓库 fork 成 public，等同公开发布 EE 代码，违反 Enterprise License 禁止分发条款；改用本地裸库 + 物理副本 | 许可约束优先于便利性 |

复核结论（实机扫描）：当前无已发生违约——`LICENSE` 与 `packages/ee/LICENSE` 无改动；remote 仍指向上游，未推送；无任何 `dist` 构建产物。待触发项 4 个：`ee-embed-sdk` 被 web 端 5 处静态 import（构建即进前端产物）、server 端 EE 215 文件（打包镜像即分发）、第三方声明缺失（已由 NOTICE 补齐）、商标与第三方品牌资源。另更正：`packages/core/shared/src/lib/ee` 不在根 LICENSE 点名的 Enterprise 范围内，属 MIT Expat，剥离非义务；`hyperformula`（GPL-3.0-only）在源码中零引用，属未重装残留死包，无风险。

本日改动涉及产品源码工作区（两个本地提交），均未推送上游，仅落在本地裸库与物理副本。

### 资产盘点基线建立

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 清单 | `10_清單/项目资产与依赖总账.md` | 新建：项目全部资产、远端仓库、备份、第三方许可、运行数据、工具链、工程件、已知问题八项的单一事实来源 | 跨会话记忆漂移问题，用户要求建立清单基线 |
| 清单 | `10_清單/资产快照日志.md` | 新建：每日快照流水，由 E-06 自动追加，不手工编辑历史段 | 用户要求每日写入项目清单 |
| 工程 | `20_工程/asset-inventory.py` | E-06 入库：只读资产盘点器，输出 Markdown 片段，`--append` 追加到快照日志；不做深递归 walk | 同上 |
| 工程 | `20_工程/README.md`、`10_清單/README.md` | 索引同步新增条目 | 同上 |
| 配置 | `activepieces` remote | `origin`→`upstream`（官方）、`github`→`origin`（私有 `lucida-ap-core`），`backup` 不变；`main` tracking 自动指向 `upstream/main` | 消除三 remote 并存导致的误推风险 |
| 源码 | `n8n` 工作区 | 209 个「未提交变更」经核实为 `core.autocrlf=true` 引起的索引 stat 漂移，`git diff` 全空、porcelain v2 显示 HEAD blob 与 index blob hash 完全一致；执行 `git add -u` 重新归一化后归零，无 staged 变更、无内容改动 | 消除脏工作区对后续 pull 的干扰 |

实机扫描更正一处口径错误：n8n 合成产物 `openapi.yml` 实际位于 `packages/cli/dist/public-api/v1/`（1,023,814 B），非先前期次记录的仓库根 `dist/`；源文件 `src/public-api/v1/openapi.yml` 为 4,185 B。E-06 探针已按真实路径修正。

未执行项（需授权）：VS Build Tools 3.35 GB 卸载、Docker 安装、activepieces 目录归档移出、GitHub token 重签。

### 三项待决项执行（用户授权）

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 资产 | `P:\Github\_archive\activepieces` | AP 源码仓由 `P:\Github\AI-Hub\activepieces` 同盘 rename 归档至 `P:\Github\_archive\activepieces`（2.18 GB）。移动后 git 完整可用：HEAD `f1141dac`、三 remote（origin=私有 / upstream=官方 / backup=本地）正常、未提交 0 | 用户授权执行；路线已放弃，工作区收敛为 n8n 单底座 |
| 工具链 | VS Build Tools 2022 | `setup.exe uninstall --installPath "P:\VSBuildTools" --quiet --norestart` 卸载完成；验证注册表卸载项消失、`P:\VSBuildTools` 目录消失、无残留 installer 进程；回收 3.35 GB | 装机后全程未调用；isolated-vm 用预编译二进制，n8n 以 pnpm 源码 + dist 产物运行，不依赖 node-gyp 现场编译 |
| 工具链 | Docker | **未安装**。查明真实阻断点为 WSL2：`VirtualMachinePlatform` 与 `Microsoft-Windows-Subsystem-Linux` 均 Disabled，启用必须重启系统，未擅自执行 | 重启属高影响操作，留待用户指定时点；n8n 2.46 源码渠道已可运行，非当前阻塞 |
| 清单 | `10_清單/项目资产与依赖总账.md` | 同步更新第二节 AP 路径、第七节工具链（VS BT 已卸载 / WSL2 未启用 / Docker 受阻 / Docker Desktop 免费适用范围）、第九节问题 1/3/4 状态 | 实机执行结果 |

Docker 许可结论：个人使用、教育、非商业开源、员工 <250 且年收入 <1000 万美元的企业免费。本项目为个人自用，许可零成本，仅需首次运行接受协议。

结项状态：六项已知问题中 4 项闭环（#1 双底座、#2 索引漂移、#3 VS BT、#6 误推风险），1 项待用户本人操作（#5 token 重签），1 项待重启窗口（#4 Docker）。

### GitHub 云端冗余清理

范围界定：用户明确「只处理本项目在 GitHub 上的东西」，个人仓库（moodle-mcp、moodle-course-watch、obsidian-tech-website、e-portfolio、Pixel-Pindo）不在范围内，未动。

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 远端 | `Faixiang/lucida-ap-core` | **已删除**（Private，91.2 MB）。删前 `git push backup main` 将裸库补齐至 `f1141dac`，并校验三方 tree 一致：远端 `914e2fe5`、本地工作区、本地裸库均为 `d6569356`，内容零差异 | AP 路线已放弃，n8n 已定；该仓为本项目云端唯一冗余项；删除可由本地 `git push` 完全重建，属可逆操作 |
| 源码 | `P:\Github\_archive\activepieces` | `origin` remote 移除；`main` tracking 由 `upstream/main` 改指 `backup/main`；现为双 remote（upstream 只读参考 / backup 本地兜底） | 云端仓删除后 origin 失效，避免后续 push 报 404 造成误判 |
| 清单 | `10_清單/项目资产与依赖总账.md` | 第二节 AP 行标注云端仓已删；2.1 节改写为双 remote 结构并记两次变更；第三节远端仓库表移除 lucida-ap-core、个人仓库改为旁注；第四节备份表补充三方 tree 校验；第九节新增第 7 条 | 实机执行结果 |

删除后 GitHub 账号下本项目仅剩 `Lucida-Project-X-Beta`（Private）。本次未删除任何个人仓库。

### AP 遗留文件清理

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 清单 | `10_清單/activepieces-EE剥离清单与保留清单.md` | **已删除**（15,215 B）。AP 路线放弃后该清单仅作历史留痕，项目内无任何引用方仍在用；原文可从 git 历史（`af91a38` 及更早）取回 | 用户指令「一并清掉，且写进至变更日志」 |
| 工程 | `20_工程/ee-strip-scan.py` | **已删除**（14,444 B）。E-01 EE 剥离扫描器只服务于 AP 剥离作业，AP 已归档且不再剥离，脚本无扫描对象 | 同上 |
| 索引 | `10_清單/README.md` | 索引表移除该清单行，替换为一行清理说明（标注 git 可取回），并注明此次属路线级弃用，不适用「旧结论被修订时旧文件保留不改」规则 | 防止索引指向不存在的文件 |
| 索引 | `20_工程/README.md` | E-01 状态改为「已移除 2026-10-28，AP 路线放弃，随归档清理」；删除「E-01 用法」整段（含实测基线与判定口径，803 字符）；E-05 状态改为「随 AP 归档，现存于 `P:\Github\_archive\activepieces\`」 | 同上 |
| 索引 | `10_清單/项目资产与依赖总账.md` | 表头「关联文档」去掉 AP 专项；第八节移除 `ee-strip-scan.py`、`activepieces-EE剥离清单与保留清单.md` 两行；`verify-preflight.ps1` 位置表述由「AP 仓库根」改为「AP 归档仓库根」 | 同上 |
| 索引 | `README.md`（根） | 「当前收录」表移除该清单行 | 同上 |

保留判定：`20_工程/asset-inventory.py` 为通用资产盘点器（非 AP 专用），保留；`E-06 探针`中指向 `P:\Github\_archive\activepieces\verify-preflight.ps1` 的一条仍然有效（文件尚存于归档），未改。`P:\Github\_archive\activepieces\` 整目录不作任何删除——归档是完整镜像留痕，破坏单个文件会损害其可校验性。

清理后档案仓内已无 AP 专用文件：`10_清單/` 仅剩总账、快照日志、README；`20_工程/` 仅剩 `asset-inventory.py` 与 README。

### 盘点器探针纠错与总账事实校正

起因：汇报项目现状前实机复跑 `asset-inventory.py`，发现两处探针给出错误事实，若照抄即形成新的记忆漂移。

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 工程 | `20_工程/asset-inventory.py` | AP `app/ee` 探针原指 `\<仓库根>\app\ee`（该路径从不存在），恒报「不存在」，掩盖了真实状态。改指 `packages\server\api\src\app\ee`，实测 **215 文件仍在** | 目录深度搜索：EE 残留目录共 9 处，其中 `server/api/src/app/ee` 为最大项 |
| 工程 | 同上 | pnpm 探针原为 `cmd /c pnpm -v`，实际命中 Marvis Host 自带 corepack shim，输出宿主版本 `1.60.3200`（另一路径甚至返回 `0.29.4`）。改为直读 `P:\Program Files\nodejs\node_modules\pnpm\package.json`，实测 **12.15.0** | `Get-Command pnpm -All` 显示 PATH 首位为 `MarvisHost\1.60.3200.39\binaries\node\current\pnpm.ps1` |
| 工程 | 同上 | 新增两条探针：web `public-routes.tsx`（应已删）、`core/shared/lib/ee`（MIT，未剥，44 文件）；原 web `routes/embed` 探针改为探测 `public-routes.tsx`，避免空目录恒报「存在」 | 实测 `routes/embed` 为空目录且 `public-routes.tsx` 已不存在 |
| 清单 | `10_清單/项目资产与依赖总账.md` | 第二节 AP 行由「已剥 EE」改为「**部分剥离**」：已删 `packages/ee` 与 web embed 入口，`server/api/src/app/ee` 215 文件仍在归档内；第五节 AP EE 行同步写实规模；档案仓 HEAD `b16a7cf`→`89d7791` | 实机核实 |
| 清单 | 同上 | 第五节 n8n 行由「全量在盘并运行中」改为「在盘、服务当前未启动（5678 未监听）」；第七节 pnpm 行补探针口径与 shim 干扰说明；第九节新增第 8 条 | 端口探测 5678 → False |

结论修正一处：此前表述「AP 已剥 EE」不准确，实际是**部分剥离**。该状态不影响合规判定——EE 代码仅存于本地归档，未对外分发、未构建发布；若日后要发布 AP 产物，须先完成 `server/api/src/app/ee` 剥离（原 E-01 清单数据可从 git 历史 `af91a38` 取回）。

### 分发性质定档与凭据规则

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 决策 | 项目整体 | 产品性质由「未决」定档为**对外免费开源（非商业）**，明确不存在商业分发、白标收费、托管收费 | 用户原话：「我開源就是爲了免費，所以不存在商业分发，白标收费与托管收费。」 |
| 清单 | `10_清單/项目资产与依赖总账.md` 第一节 | 新增「分发性质」行载明定档结论；「当前阶段」改为「形态已定义（壳 + 运行时获取）」；原「未决的主线问题」改为「主线问题处置结果」，并写明 SUL 三条允许通道全部成立、三条禁止项均不触发、出现任何收费意图须回本节复核 | 同上 |
| 清单 | 同上 5.2 | 新增「本项目定档判定」：判定成立需同时满足壳内不含 n8n 代码与产物、交易环节零金额、不提供收费托管，三点当前均满足 | 推导自 SUL 原文与本次定档 |
| 清单 | 同上 第十节 | 补充：定档后「禁止」列触发概率降低，但「壳内不含 n8n 代码与产物」不可放松——它是判定是否构成分发的物理基础，与收费与否无关 | 同上 |
| 清单 | 同上 第九节 #5 | token 明文风险复查结案：仓库无 `.env`/`*.token`、无 `insteadOf` 凭据 URL、origin 无内嵌凭据、进程与用户级均无 `GITHUB_TOKEN`/`GH_TOKEN`；凭据实际仅存 `cmdkey` 条目 `gh:github.com:Faixiang`（gh CLI 托管）。状态由「待用户处理」改为「已关闭，转规则约束」 | 只读静态排查，未读取任何密钥值 |
| 清单 | 同上 第十二节（新增） | 建立《凭据使用规则》：token 仅 Agent 使用；**读取或调用前必须先说明用途并取得用户确认**；禁止任何形式打印明文；仅存凭据管理器；排查只报存在性与位置；gh/git 只读查询沿用既有凭据免逐次请示，写操作仍须逐次确认 | 用户原话：「GitHub token只對你使用……关于这个token的使用规则经过询问我，得到我的确认才可使用」 |

规则落地要点：第 5 条不再需要重签 token——排查确认明文从未落盘；真正的约束改为「使用前请示」，已写入总账第十二节，优先级高于操作便利性。


## 2026-10-27

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 仓库 | `Lucida-Project-X-Beta` | 建立私有档案仓库，隔离清单与工程文件 | 用户指示 |
| 清单 | `10_清單/activepieces-EE剥离清单与保留清单.md` | 首次入库：EE 剥离范围、耦合点、遥测点、保留与验收方案 | 只读扫描结果 |
| 工程 | `20_工程/` | 建立目录与收录规则，脚本待入库 | 用户指示 |
