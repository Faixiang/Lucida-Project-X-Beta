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
| E-01 | `ee-strip-scan.py` | 扫描 EE 目录规模、非 EE 引用点、硬耦合行号、遥测点（清单数据来源） | **已移除** 2026-10-28，AP 路线放弃，随归档清理 |
| E-02 | `license-scan.py` | 依赖闭包许可扫描，输出 CSV 明细 | 待入库 |
| E-03 | `verify-license-intact.ps1` | 剥离后校验根 LICENSE 与上游原文逐字一致 | 待入库（E-05 已覆盖静态部分） |
| E-04 | `verify-no-telemetry.ps1` | 启动与执行期间核验无 PostHog 外联 | 待入库（E-05 仅静态扫描） |
| E-05 | `verify-preflight.ps1` | 发布前只读闸门：LICENSE 完整性、NOTICE 存在性、EE 目录状态、构建产物污染、前端 EE import、遥测配置 | 随 AP 归档，现存于 `P:\Github\_archive\activepieces\` |

## 收录规则

- 脚本必须可重复执行、只读优先；涉及删除的操作单独标注并需显式授权。
- 每个脚本头部注明：用途、输入、输出、是否有副作用。
- 不在本仓库存放任何密钥、token、账号凭据。
*（内容由AI生成，仅供参考）*
