---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: c6eb62ba6ec5a28db2139adf23a2fe4b_ed5e0e59d22f11f196c5525400248c00
    ReservedCode1: 1uQ8GewB3xuCmeWfl+9L0CAsOX4rjUxjMLisnElLoMz+rmoY6AdmXjHPxuYodUE8acJFwDUZ1+puCDLQoaue0sqsXGB/HIir6dUM9x8DvjgXy6jELz2ockQbSTTbGd5d8ZvYuN5OE44E2gNOpdDTd7Vh6j49vBlTN8ujj3KhGPtNSyt/0kYuvH0M5JM=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: c6eb62ba6ec5a28db2139adf23a2fe4b_ed5e0e59d22f11f196c5525400248c00
    ReservedCode2: 1uQ8GewB3xuCmeWfl+9L0CAsOX4rjUxjMLisnElLoMz+rmoY6AdmXjHPxuYodUE8acJFwDUZ1+puCDLQoaue0sqsXGB/HIir6dUM9x8DvjgXy6jELz2ockQbSTTbGd5d8ZvYuN5OE44E2gNOpdDTd7Vh6j49vBlTN8ujj3KhGPtNSyt/0kYuvH0M5JM=
---

# Activepieces EE 剥离清单与保留清单

> 生成日期：2026-10-27
> 仓库：`P:\Github\AI-Hub\activepieces`（commit 280f6bb3）
> 扫描口径：`.ts/.tsx/.js/.jsx/.mjs/.cjs`，排除 `node_modules`、`dist`、`build`、`.git`、`.next`、`coverage`
> 本轮性质：**只读扫描，未执行任何删除、移动、重命名操作**

## 〇、执行原则（先定死，后续所有动作不得违反）

| 编号 | 原则 | 说明 |
|---|---|---|
| P-01 | 根 `LICENSE` 原文一字不改 | 含 `Copyright (c) 2020-2024 Activepieces Inc.` 与三段分区说明。MIT 义务段要求保留版权声明与许可声明，改它才是违约 |
| P-02 | `packages/ee/LICENSE`（Enterprise License 文本）原文保留 | 即使 EE 代码已删，也不删除该文件，避免出现「声明被删」的争议；其存在仅是历史说明 |
| P-03 | 只删代码，不删声明 | 剥离对象是 `.ts` 源码，不是许可文本、不是版权注释 |
| P-04 | 保留部分的文件头版权注释不得改写署名 | 不得批量替换为自己 |
| P-05 | 另行新增 `NOTICE.md` 说明剥离事实 | 声明本仓库已移除 EE 目录、仍基于 Activepieces MIT 部分、版权归上游 |

结论：**删代码 ≠ 抹声明**。MIT 义务段约束的是「副本中必须含有版权声明与许可声明」，不约束「哪些代码文件必须存在」。

---

## 一、剥离清单（规模）

### 1.1 总量

| 目录 | 文件数 | 代码行数 | 说明 |
|---|---:|---:|---|
| `packages/ee` | 4 | 1,132 | 仅 embed-sdk |
| `packages/server/api/src/app/ee` | 215 | 28,838 | 主要商业逻辑 |
| `packages/core/shared/src/lib/ee` | 44 | 4,270 | 共享类型与常量 |
| **合计** | **263** | **34,240** | |

### 1.2 `app/ee` 子模块（按行数降序，可按模块粒度分批删除）

| 子模块 | 文件 | 行数 | 自用场景是否必需 |
|---|---:|---:|---|
| agent | 52 | 10,175 | **是**（AI 教师层核心，删后需自建或外挂） |
| projects | 36 | 4,847 | 否（项目/成员/发布管理） |
| platform | 18 | 3,447 | 部分（platform 基础能力需评估） |
| authentication | 14 | 1,541 | 否（SSO/SAML/RBAC 企业认证） |
| scim | 6 | 1,330 | 否（企业目录同步） |
| secret-managers | 10 | 914 | 否（可用 `.env` 替代） |
| database | 20 | 803 | **是**（20 个 EE 迁移，需处理 schema） |
| pieces | 7 | 667 | 部分（piece-set 管理） |
| helper | 5 | 658 | 否 |
| flows | 5 | 641 | 否（flow-approval 审批流） |
| audit-logs | 4 | 568 | 否（可用日志替代） |
| managed-authn | 4 | 461 | 否 |
| embed-subdomain | 5 | 439 | 否（嵌入子域） |
| license-key-usage-report | 2 | 420 | 否（许可用量上报，且含遥测） |
| alerts | 4 | 317 | 否 |
| signing-key | 5 | 280 | 否 |
| api-keys | 3 | 230 | **部分**（若无平台 API Key 需求可弃） |
| oauth-apps | 3 | 228 | 否 |
| appsumo | 3 | 218 | 否 |
| global-connections | 1 | 170 | 否 |
| platform-webhooks | 3 | 140 | 否 |
| users | 2 | 104 | 否 |
| app-connections | 1 | 100 | 否 |
| flags | 1 | 71 | 否 |
| template | 1 | 69 | 否 |

### 1.3 `core/shared/src/lib/ee` 子模块

| 子模块 | 文件 | 行数 |
|---|---:|---:|
| audit-events | 2 | 1,393 |
| agent | 8 | 1,258 |
| secret-managers | 2 | 326 |
| piece-set | 3 | 287 |
| scim | 1 | 194 |
| billing | 1 | 172 |
| event-destinations | 2 | 129 |
| authn | 4 | 102 |
| git-repo | 1 | 72 |
| embed-subdomain | 1 | 59 |
| project-members | 2 | 58 |
| flow-approval | 1 | 45 |
| otp | 4 | 38 |
| alerts | 3 | 36 |
| signing-key | 4 | 34 |
| api-key | 1 | 31 |
| oauth-apps | 2 | 27 |
| managed-authn | 2 | 9 |

> 注：`audit-events` 单模块 1,393 行最大，且 `AuditEventEntity` 被社区代码（`piece-upgrade.service.ts`）直接引用，属必须先解耦的点。

---

## 二、耦合清单（删之前必须先改）

### 2.1 总览

| 指标 | 数值 |
|---|---:|
| 非 EE 代码引用 EE 的总处数 | 333 |
| 涉及文件数 | 157 |

按源目录分布：

| 源目录 | 引用处数 |
|---|---:|
| `packages/server/api` | 238 |
| `packages/server/worker` | 36 |
| `packages/core/shared` | 33 |
| `packages/pieces/community` | 20 |
| `packages/web/src` | 4 |
| `packages/server/sandbox` | 2 |

### 2.2 四处结构性注册点（必须改）

| 文件 | 行数 | EE 命中 | 内容 |
|---|---:|---:|---|
| `packages/server/api/src/app/app.ts` | 621 | 46 | 第 35–59 行等，46 个 EE 模块的**静态 import**，随后统一注册进 Nest 容器 |
| `packages/server/api/src/app/database/database-connection.ts` | 213 | 22 | 第 13–34 行，22 个 EE Entity 进入 TypeORM entities 数组 |
| `packages/server/api/src/app/database/postgres-connection.ts` | 1,024 | 20 | 第 5–24 行，20 个 EE migration 进入 migrations 数组 |
| `packages/core/shared/src/index.ts` | 82 | 21 | 第 52、61–80 行，`export * from './lib/ee/*'` 共 21 条 re-export |

### 2.3 三处业务硬耦合（编译必红的点）

| 文件 | 行号 | 引用符号 |
|---|---:|---|
| `packages/server/api/src/app/database/seeds/role-seed.ts` | 4 | `ProjectRoleEntity`（`../../ee/projects/project-role/project-role.entity`） |
| `packages/server/api/src/app/mcp/oauth/mcp-oauth.controller.ts` | 8 / 9 / 10 | `AgentConversationEntity`、`agentHelpers`、`CONVERSATION_ID_HEADER`（均来自 `../../ee/agent/*`） |
| `packages/server/api/src/app/flows/flow-version/piece-upgrade.service.ts` | 5 | `AuditEventEntity`（`../../ee/audit-logs/audit-event-entity`） |

处理建议：

- `role-seed.ts`：种子逻辑改为不写入 ProjectRole（社区版无项目角色概念），或内联一个最小枚举。
- `mcp-oauth.controller.ts`：MCP OAuth 与 AI agent 会话绑定，若不做 agent，则该 controller 的会话绑定分支整体切除；若要保留 MCP，需保留 `CONVERSATION_ID_HEADER` 常量（仅 1 个字符串常量，可内联）。
- `piece-upgrade.service.ts`：审计事件写入改为可选空实现（no-op），或用本地日志替换。

---

## 三、遥测清单（**不在 EE 内，删 EE 无法消除**）

这是本轮扫描最重要的发现。

| 项 | 位置 | 说明 |
|---|---|---|
| 真实的 PostHog 客户端 | `packages/server/api/src/app/helper/telemetry.utils.ts` | 23 处引用；第 15 行**硬编码 project key**（`phc_7F92...`），第 16 行 host 为 `https://us.i.posthog.com`；含 `identify` / `alias` / `groupIdentify` / `capture` / `flush` |
| 事件枚举 | 同文件第 200–271 行 | `LicenseKeyPostHogEvents`：AI 用量、日运行数、聊天消息、平台初始化报告 |
| 调用者（生产代码） | 19 个文件 | 含 `app.ts`、`authentication.controller.ts`、`passwordless-auth.*`、`flow.service.ts`、`flow-run-module.ts`、`mcp-server-builder.ts`、`mcp-oauth.controller.ts`、`platform/billing-and-telemetry.ts`、`platform.service.ts`、`user-invitation.*` |

关键判断：

1. 该文件位于**社区目录**，不在 `app/ee` 下，所以「删 EE」不会让它停止上报。
2. 调用链穿过认证、流程执行、用户邀请等核心路径，意味着本地自托管运行时仍会向 `us.i.posthog.com` 发送事件。
3. 这与你「本地运行、无账号、无租户」的目标直接冲突，必须在剥离 EE 的同一批动作中处理。

误报澄清：扫描中 `posthog` 关键词共 882 行，其中绝大多数来自 `packages/pieces/community/posthog/**`（PostHog 集成件本身的源码），**与遥测无关**，不要误删。

---

## 四、保留清单

### 4.1 必须原样保留（不得修改、不得删除）

| 文件 | 处理 |
|---|---|
| `LICENSE`（根） | 原样保留，含版权行与三段分区说明 |
| `packages/ee/LICENSE` | 原样保留（Enterprise License 全文） |

### 4.2 建议保留的社区能力

| 模块 | 位置 | 理由 |
|---|---|---|
| 社区认证 | `packages/server/api/src/app/authentication/authentication.controller.ts` | 邮箱/OTP/Passwordless 登录，不依赖 EE 许可 |
| 社区 piece 体系 | `packages/pieces/community/**` | 工作流能力的实际来源（116 个 AI 相关 piece 可接本地 Ollama） |
| platform 基础模块 | `packages/server/api/src/app/platform/**`（非 ee 部分） | 平台配置、项目容器的基础实现 |
| 社区构建入口 | `app.ts` 中 community 模式 4 模块注册 | denoMigration / platformProject / communityPieces / otp |

### 4.3 需要新增的文件

| 文件 | 内容 |
|---|---|
| `NOTICE.md` | 声明基于 Activepieces MIT 部分、已移除上游 EE 目录、LICENSE 未修改、EE 目录说明仅具历史意义 |
| `THIRD-PARTY-NOTICES.md` | 收录依赖闭包中的第三方许可（含 MPL-2.0 双许可项、BSD、Apache 等），与既有许可清单 CSV 对齐 |

---

## 五、执行步骤与验收（待授权后执行）

### 阶段 1：解耦（先改代码，不删文件）

1. 改 `core/shared/src/index.ts`：删除 21 条 `export * from './lib/ee/*'`。
2. 改 `database-connection.ts`：移除 22 个 EE Entity 导入与数组项。
3. 改 `postgres-connection.ts`：移除 20 个 EE migration 导入与数组项；确认社区 migration 链仍能建出完整 schema。
4. 改 `app.ts`：移除 46 个 EE 模块静态 import 与注册。
5. 修三处业务硬耦合：`role-seed.ts`、`mcp-oauth.controller.ts`、`piece-upgrade.service.ts`。
6. 处理遥测：移除 `telemetry.utils.ts` 或其全部调用点（或改为本地 no-op）。

验收：`bun run build` 通过；`grep -r "app/ee" packages --include=*.ts` 结果为空（EE 自身除外）。

### 阶段 2：删除

7. 删除 `packages/ee/`（**保留其 LICENSE 文件**，先单独备份该文件再重建目录）。
8. 删除 `packages/server/api/src/app/ee/`。
9. 删除 `packages/core/shared/src/lib/ee/`。
10. 清理 `tsconfig` 中指向上述目录的 paths/references。

验收：`grep -rn "lib/ee\|app/ee\|ee/" packages --include=*.ts` 仅剩注释或空结果。

### 阶段 3：验证

11. `bun install` → `bun run build` → 启动社区模式。
12. 冒烟：登录（社区认证）、创建 flow、执行一次 flow、查看 run 记录。
13. 网络核验：抓包或日志确认启动与执行期间无 `us.i.posthog.com` 请求。
14. 许可复核：`LICENSE` 与上游原始文件做 `diff`，必须完全一致。

### 阶段 4：文档与档案

15. 新增 `NOTICE.md`、`THIRD-PARTY-NOTICES.md`。
16. 变更记录写入 Notion「Activepieces 开源合规档案」页。

---

## 六、功能损失清单（自用场景影响）

| 能力 | 损失 | 自用影响 |
|---|---|---|
| AI agent（10,175 行） | 全失 | **最重**，AI 教师层需自建或外挂 |
| projects（4,847 行） | 项目/成员/发布/git-sync 全失 | 中，单人使用可用单项目替代 |
| platform（3,447 行） | 平台级配置/计费/并发池部分失 | 低，并发可用环境变量兜底 |
| authentication EE（1,541 行） | SSO/SAML/RBAC 失 | 无影响 |
| scim（1,330 行） | 企业目录同步失 | 无影响 |
| secret-managers（914 行） | 密钥托管失 | 低，`.env` 替代 |
| audit-logs（568 行） | 审计日志失 | 低，可用文件日志 |
| license-key-usage-report（420 行） | 许可上报失 | 无影响 |
| api-keys（230 行） | 平台 API Key 失 | 低，如需可自建中间件 |

---

## 七、下一步待授权动作

| 编号 | 动作 | 风险级 | 状态 |
|---|---|---|---|
| A-01 | 备份仓库（`git tag` + 打包） | 低 | 待确认 |
| A-02 | 阶段 1 解耦改造 | 中 | 待确认 |
| A-03 | 阶段 2 删除三目录 | 中高（不可逆，需回收站/备份） | 待确认 |
| A-04 | 遥测移除 | 中 | 待确认 |
| A-05 | 新增 NOTICE / THIRD-PARTY-NOTICES | 低 | 待确认 |

> 本次仅产出清单，未改动仓库任何文件。
*（内容由AI生成，仅供参考）*
