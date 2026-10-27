---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: c6eb62ba6ec5a28db2139adf23a2fe4b_892ed3bad23511f196c5525400248c00
    ReservedCode1: 2cxXr8nnlLeBALtXAys9IYWBj1hGcvo86ZaW4xIklST9lYBjmUAfLv5SI+sA0rdceYPgFnm6PzmR9aZ2oPdGSvsO0szQ2ewMJeL7z3qb2ehQpnf+KAtT5nRcpe8r+S4e3hE8vNd8xPIbQT6rx/Gba0EDScg6SsS5jOSiMpz33et6pAvhSOfgPmv7IK0=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: c6eb62ba6ec5a28db2139adf23a2fe4b_892ed3bad23511f196c5525400248c00
    ReservedCode2: 2cxXr8nnlLeBALtXAys9IYWBj1hGcvo86ZaW4xIklST9lYBjmUAfLv5SI+sA0rdceYPgFnm6PzmR9aZ2oPdGSvsO0szQ2ewMJeL7z3qb2ehQpnf+KAtT5nRcpe8r+S4e3hE8vNd8xPIbQT6rx/Gba0EDScg6SsS5jOSiMpz33et6pAvhSOfgPmv7IK0=
---

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

## 2026-10-27

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 仓库 | `Lucida-Project-X-Beta` | 建立私有档案仓库，隔离清单与工程文件 | 用户指示 |
| 清单 | `10_清單/activepieces-EE剥离清单与保留清单.md` | 首次入库：EE 剥离范围、耦合点、遥测点、保留与验收方案 | 只读扫描结果 |
| 工程 | `20_工程/` | 建立目录与收录规则，脚本待入库 | 用户指示 |
*（内容由AI生成，仅供参考）*
