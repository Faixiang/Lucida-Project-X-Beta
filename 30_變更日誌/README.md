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

未改动产品源码仓库；本日改动均为本档案仓库内的脚本与文档。

## 2026-10-27

| 类型 | 对象 | 变更 | 依据 |
|---|---|---|---|
| 仓库 | `Lucida-Project-X-Beta` | 建立私有档案仓库，隔离清单与工程文件 | 用户指示 |
| 清单 | `10_清單/activepieces-EE剥离清单与保留清单.md` | 首次入库：EE 剥离范围、耦合点、遥测点、保留与验收方案 | 只读扫描结果 |
| 工程 | `20_工程/` | 建立目录与收录规则，脚本待入库 | 用户指示 |
*（内容由AI生成，仅供参考）*
