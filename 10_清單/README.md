---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: c6eb62ba6ec5a28db2139adf23a2fe4b_8811f917d23511f196c5525400248c00
    ReservedCode1: gmLOnRr9KTeNOAKxtx32S53N1TAt3hRvvJqfU/+P4s9HPPL3M07WTM/QZXGGa+XjEpxsYJYXTDTyXcY0DbAfcx5HJ4z98y81BgpaL6z1FeZbWph8b3lIDcHSKMhffd3i2i4W5WoNv1e3DyhPZZN06qMEQ0+4/MI/HFplW9vBcmtKhAHs3GixE93ZY40=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: c6eb62ba6ec5a28db2139adf23a2fe4b_8811f917d23511f196c5525400248c00
    ReservedCode2: gmLOnRr9KTeNOAKxtx32S53N1TAt3hRvvJqfU/+P4s9HPPL3M07WTM/QZXGGa+XjEpxsYJYXTDTyXcY0DbAfcx5HJ4z98y81BgpaL6z1FeZbWph8b3lIDcHSKMhffd3i2i4W5WoNv1e3DyhPZZN06qMEQ0+4/MI/HFplW9vBcmtKhAHs3GixE93ZY40=
---

# 10_清單

审计、许可、依赖、剥离范围等一切清单与判定报告。

## 索引

| 文件 | 生成日期 | 类型 | 摘要 |
|---|---|---|---|
| `项目资产与依赖总账.md` | 2026-10-28 | **基线总账** | 项目掺和的全部资产、远端仓库、备份、第三方许可、运行数据、工具链、工程件与已知问题的唯一事实来源 |
| `资产快照日志.md` | 2026-10-28 起每日追加 | 自动流水 | `asset-inventory.py --append` 生成的每日快照：仓库状态、关键探针、运行数据、工具链版本 |

> AP 专项清单 `activepieces-EE剥离清单与保留清单.md` 已于 2026-10-28 随 AP 路线放弃一并清理，原文件内容可从 git 历史（提交 `af91a38` 及更早）取回。该清理不适用于上一条"旧文件保留不改"规则的常规修订场景，属路线级弃用。

## 收录规则

- 命名：`<对象>-<主题>.md`，中文可，避免空格。
- 每份清单必须含：扫描口径、真实数据来源、结论、待授权动作。
- 结论一旦被后续清单修订，旧文件保留不改，新增文件并在仓库根 README 登记取代关系。
*（内容由AI生成，仅供参考）*
