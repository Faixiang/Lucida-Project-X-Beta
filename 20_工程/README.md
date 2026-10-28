---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: c6eb62ba6ec5a28db2139adf23a2fe4b_88a4bfb1d23511f18460525400393706
    ReservedCode1: UfXaj46Q8x1MjC3onP685c6JycOtJLpy5wA8yD9SZiLSqvTrZo7f47C75PPlfKFm3zqMe3PHr3z2ZNY/8FRQROGnZVDI4J93dCYsMS3RuwKTAattCc5gaNPDgMQK2ACw9i+/1z5XnUoVoOKg8fnlHzPEIWKU/GRELAdKQP974PU7EPVwMVrZohUSJGQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: c6eb62ba6ec5a28db2139adf23a2fe4b_88a4bfb1d23511f18460525400393706
    ReservedCode2: UfXaj46Q8x1MjC3onP685c6JycOtJLpy5wA8yD9SZiLSqvTrZo7f47C75PPlfKFm3zqMe3PHr3z2ZNY/8FRQROGnZVDI4J93dCYsMS3RuwKTAattCc5gaNPDgMQK2ACw9i+/1z5XnUoVoOKg8fnlHzPEIWKU/GRELAdKQP974PU7EPVwMVrZohUSJGQ=
---

# 20_工程

工程侧的脚本、配置与验证工具。**不含产品源码**，源码仍留在各自代码仓库。

## 规划中的条目

| 编号 | 名称 | 用途 | 状态 |
|---|---|---|---|
| E-06 | `asset-inventory.py` | 只读资产与依赖盘点器，输出 Markdown 快照，支持 `--append` 追加到 `10_清單/资产快照日志.md`（每日记录的数据来源） | **已入库** 2026-10-28 |
| E-01 | `ee-strip-scan.py` | 扫描 EE 目录规模、非 EE 引用点、硬耦合行号、遥测点（清单数据来源） | **已入库** 2026-10-28 |
| E-02 | `license-scan.py` | 依赖闭包许可扫描，输出 CSV 明细 | 待入库 |
| E-03 | `verify-license-intact.ps1` | 剥离后校验根 LICENSE 与上游原文逐字一致 | 待入库（E-05 已覆盖静态部分） |
| E-04 | `verify-no-telemetry.ps1` | 启动与执行期间核验无 PostHog 外联 | 待入库（E-05 仅静态扫描） |
| E-05 | `verify-preflight.ps1` | 发布前只读闸门：LICENSE 完整性、NOTICE 存在性、EE 目录状态、构建产物污染、前端 EE import、遥测配置 | **已入库** 2026-10-28，位于源码仓库根目录 |

## E-01 用法

```
python 20_工程\ee-strip-scan.py --repo P:\Github\AI-Hub\activepieces --out <输出目录>
```

输出 `ee-scan-report.md`（人读）与 `ee-scan-data.json`（机读，供后续 diff 比对）。
只读，不改被扫描仓库。

2026-10-28 实测基线（上游 activepieces，commit 见 `30_變更日誌`）：

| 指标 | 实测值 |
|---|---:|
| EE 文件 / 代码行 | 263 / 34,240 |
| 非 EE 引用 EE | 329 处 / 155 文件 |
| 结构性注册点 | app.ts 46、database-connection 22、postgres-connection 20、core/shared/index 21 |
| 业务硬耦合 | role-seed.ts:4、mcp-oauth.controller.ts:8-10、piece-upgrade.service.ts:5 |
| `telemetry.utils.ts` | 25 处 PostHog 行 / 8 处 SDK 调用，被 19 个生产文件引用 |

已知判定口径：

- EE 引用 = 模块说明符含 `/ee/` 或 `ee/` 前缀，或包名精确等于 `ee-embed-sdk`。
- **不得**用裸 `ee-` 子串匹配，否则 `find-free-slots`、`json-tree-skeleton`、`employee-terminated`、`tree-kill` 等普通文件会误报（旧口径虚高 26 处）。
- 必须全文匹配而非逐行匹配，多行 import 的模块名落在 `} from '...'` 续行上。

## 收录规则

- 脚本必须可重复执行、只读优先；涉及删除的操作单独标注并需显式授权。
- 每个脚本头部注明：用途、输入、输出、是否有副作用。
- 不在本仓库存放任何密钥、token、账号凭据。
*（内容由AI生成，仅供参考）*
