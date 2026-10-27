#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E-01  EE 剥离扫描器（只读）
===========================

用途
----
对 Activepieces 仓库做剥离前的只读扫描，产出可复现的数据：
  1. EE 三个目录的真实规模（文件数 / 代码行数）与子模块分布
  2. 非 EE 代码对 EE 的引用统计（总处数 / 涉及文件数 / 按源目录 Top）
  3. 结构性注册点命中（app.ts、database-connection、postgres-connection、core/shared/index）
  4. 业务硬耦合点（文件 + 行号 + 引用符号），自动发现
  5. 遥测点（真正的 PostHog SDK 调用 vs community/posthog 集成件的误报）

输入
----
--repo   仓库根目录（默认 P:\\Github\\AI-Hub\\activepieces）
--out    报告输出目录（默认当前工作目录）

输出
----
ee-scan-report.md   人读报告
ee-scan-data.json   机读数据（供后续 diff 比对）

副作用
------
无。不修改、不删除、不移动被扫描仓库中的任何文件；只在 --out 目录写报告。
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------- 常量

EXCLUDE_DIRS = {"node_modules", "dist", "build", ".git", ".next", "coverage",
                "out", ".turbo", ".cache"}
CODE_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}

# 上游根 LICENSE 点名的商业许可目录 + 建议一并剥离的共享 EE 目录
EE_DIRS = [
    os.path.join("packages", "ee"),
    os.path.join("packages", "server", "api", "src", "app", "ee"),
    os.path.join("packages", "core", "shared", "src", "lib", "ee"),
]

# 结构性注册点：删 EE 前必须先改的位置
STRUCTURAL = [
    os.path.join("packages", "server", "api", "src", "app", "app.ts"),
    os.path.join("packages", "server", "api", "src", "app", "database", "database-connection.ts"),
    os.path.join("packages", "server", "api", "src", "app", "database", "postgres-connection.ts"),
    os.path.join("packages", "core", "shared", "src", "index.ts"),
]

# EE import 判定：from/require 指向 app/ee、lib/ee、packages/ee
# 全文匹配而非逐行匹配——多行 import 的模块名落在以 "}" 开头的续行上，
# 逐行规则会漏判（web 端 4 个 ee-embed-sdk 引用就是这种情况）。
MODULE_REF_RE = re.compile(
    r"""(?:from\s+|require\(\s*|import\(\s*)['"](?P<spec>[^'"]+)['"]"""
)
SYMBOL_RE = re.compile(r"\{([^}]*)\}", re.S)


def is_ee_spec(spec):
    """判断模块标识符是否指向 EE 代码。

    注意：不能用裸 `ee-` 子串匹配——社区目录里存在
    `1701261357197-migrate-ee-users-to-oldest-platform`、`find-free-slots`、
    `json-tree-skeleton`、`employee-terminated` 这类含 ee- 的普通文件名，
    会被误判（旧口径因此虚高 26 处）。packages/ee 的包名是 ee-embed-sdk，单独精确匹配。
    """
    if "/ee/" in spec or spec.startswith("ee/"):
        return True
    if spec == "ee-embed-sdk" or spec.startswith("ee-embed-sdk/"):
        return True
    return False


def iter_module_refs(path):
    """产出 (行号, 模块标识符, 符号列表)。

    符号列表取 import 语句大括号内的具名导入，用于识别硬耦合符号。
    """
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
    except OSError:
        return
    for m in MODULE_REF_RE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        spec = m.group("spec")
        head = max(text.rfind("import", 0, m.start()),
                   text.rfind("export", 0, m.start()))
        snippet = text[head if head != -1 else 0:m.start()]
        symbols = []
        sm = SYMBOL_RE.search(snippet)
        if sm:
            symbols = [s.strip().split(" as ")[0].strip()
                       for s in sm.group(1).split(",") if s.strip()]
        yield line, spec, symbols

TELEMETRY_UTIL = os.path.join("packages", "server", "api", "src", "app", "helper", "telemetry.utils.ts")
PIECE_POSTHOG = os.path.join("packages", "pieces", "community", "posthog")


# ---------------------------------------------------------------- 工具

def iter_code_files(repo):
    """遍历仓库内的源码文件，跳过依赖与构建产物。"""
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            if os.path.splitext(name)[1].lower() in CODE_EXT:
                yield os.path.join(dirpath, name)


def count_lines(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return sum(1 for _ in fh)
    except OSError:
        return 0


def rel(path, repo):
    return os.path.relpath(path, repo)


def in_ee(relpath):
    return any(relpath == d or relpath.startswith(d + os.sep) for d in EE_DIRS)


def read_lines(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.readlines()
    except OSError:
        return []


# ---------------------------------------------------------------- 扫描项

def scan_scale(repo):
    """EE 目录规模与子模块分布。"""
    result = {}
    for d in EE_DIRS:
        abs_dir = os.path.join(repo, d)
        key = d.replace(os.sep, "/")
        if not os.path.isdir(abs_dir):
            result[key] = {"exists": False}
            continue
        files = list(iter_code_files(abs_dir))
        subs = defaultdict(lambda: {"files": 0, "lines": 0})
        total = 0
        for f in files:
            lines = count_lines(f)
            total += lines
            top = rel(f, abs_dir).split(os.sep)[0]
            if top.lower().endswith(tuple(CODE_EXT)) or top == os.path.basename(f):
                top = "<root-files>"
            subs[top]["files"] += 1
            subs[top]["lines"] += lines
        result[key] = {
            "exists": True,
            "files": len(files),
            "lines": total,
            "submodules": dict(sorted(subs.items(), key=lambda kv: -kv[1]["lines"])),
        }
    result["_total"] = {
        "files": sum(v.get("files", 0) for k, v in result.items() if k != "_total"),
        "lines": sum(v.get("lines", 0) for k, v in result.items() if k != "_total"),
    }
    return result


def scan_refs(repo):
    """非 EE 代码对 EE 的引用与硬耦合点。"""
    refs = []
    for path in iter_code_files(repo):
        r = rel(path, repo)
        if in_ee(r):
            continue
        for idx, spec, symbols in iter_module_refs(path):
            if not is_ee_spec(spec):
                continue
            refs.append({
                "file": r.replace(os.sep, "/"),
                "line": idx,
                "spec": spec,
                "symbols": symbols,
            })
    return refs


def scan_structural(repo):
    """结构性注册点：每个文件里 EE 引用的条数。"""
    out = {}
    refs_by_file = defaultdict(int)
    for path in iter_code_files(repo):
        r = rel(path, repo)
        if in_ee(r):
            continue
        for _idx, spec, _symbols in iter_module_refs(path):
            if is_ee_spec(spec):
                refs_by_file[r] += 1
    for d in STRUCTURAL:
        out[d.replace(os.sep, "/")] = {
            "exists": os.path.isfile(os.path.join(repo, d)),
            "ee_imports": refs_by_file.get(d, 0),
        }
    return out


def scan_telemetry(repo):
    """区分真实遥测 SDK 与 community/posthog 集成件（后者为误报）。"""
    sdk_hits = []
    piece_hits = Counter()
    callers = []
    sdk_import_re = re.compile(r"""from\s+['"](posthog-node|posthog-js)['"]|require\(\s*['"](posthog-node|posthog-js)['"]""")

    for path in iter_code_files(repo):
        r = rel(path, repo)
        lines = read_lines(path)
        if r.startswith(PIECE_POSTHOG):
            for idx, line in enumerate(lines, 1):
                if "posthog" in line.lower():
                    piece_hits[r.replace(os.sep, "/")] += 1
            continue
        for idx, line in enumerate(lines, 1):
            low = line.lower()
            if "posthog" in low:
                sdk_hits.append({
                    "file": r.replace(os.sep, "/"),
                    "line": idx,
                    "text": re.sub(r"(phc_)[A-Za-z0-9]+", r"\1***", line.strip()[:160]),
                })
            if sdk_import_re.search(line) and "test" not in r.lower():
                callers.append(r.replace(os.sep, "/"))

    util = TELEMETRY_UTIL.replace(os.sep, "/")
    util_lines = [h for h in sdk_hits if h["file"] == util]
    hardcoded_host = [h for h in util_lines if "posthog.com" in h["text"]]

    # telemetry.utils 的调用者
    importers = []
    for path in iter_code_files(repo):
        r = rel(path, repo)
        if "test" in r.lower():
            continue
        for line in read_lines(path):
            if "telemetry.utils" in line and MODULE_REF_RE.search(line):
                importers.append(r.replace(os.sep, "/"))
                break

    return {
        "sdk_hits_total": len(sdk_hits),
        "sdk_hits": sdk_hits[:80],
        "telemetry_util_file": util,
        "telemetry_util_hits": len(util_lines),
        "telemetry_util_host_lines": hardcoded_host,
        "sdk_importer_files": sorted(set(callers)),
        "telemetry_util_importers": sorted(set(importers)),
        "piece_posthog_lines": sum(piece_hits.values()),
        "piece_posthog_files": len(piece_hits),
    }


# ---------------------------------------------------------------- 渲染

def render_md(repo, scale, refs, structural, telemetry):
    by_dir = Counter()
    for r in refs:
        parts = r["file"].split("/")
        by_dir["/".join(parts[:3]) if len(parts) >= 3 else r["file"]] += 1

    sym_counter = Counter()
    for r in refs:
        for s in r["symbols"]:
            sym_counter[s] += 1

    L = []
    L.append("# EE 剥离扫描报告\n")
    L.append(f"> 仓库：`{repo}`  \n> 生成方式：`ee-strip-scan.py`（只读）\n")

    L.append("## 1. EE 目录规模\n")
    L.append("| 目录 | 文件 | 代码行 |")
    L.append("|---|---:|---:|")
    for k, v in scale.items():
        if k == "_total":
            continue
        L.append(f"| `{k}` | {v.get('files', 0)} | {v.get('lines', 0):,} |")
    t = scale["_total"]
    L.append(f"| **合计** | **{t['files']}** | **{t['lines']:,}** |\n")

    for k, v in scale.items():
        if k == "_total" or not v.get("exists"):
            continue
        L.append(f"### `{k}` 子模块\n")
        L.append("| 子模块 | 文件 | 行数 |")
        L.append("|---|---:|---:|")
        for s, sv in v["submodules"].items():
            L.append(f"| {s} | {sv['files']} | {sv['lines']:,} |")
        L.append("")

    L.append("## 2. 耦合统计\n")
    L.append(f"- 引用总处数：**{len(refs)}**")
    L.append(f"- 涉及文件数：**{len({r['file'] for r in refs})}**\n")
    L.append("| 源目录 | 处数 |")
    L.append("|---|---:|")
    for k, v in by_dir.most_common(15):
        L.append(f"| `{k}` | {v} |")
    L.append("")

    L.append("### 结构性注册点\n")
    L.append("| 文件 | EE import 数 |")
    L.append("|---|---:|")
    for k, v in structural.items():
        mark = "" if v["exists"] else "（文件不存在）"
        L.append(f"| `{k}`{mark} | {v['ee_imports']} |")
    L.append("")

    L.append("### 被引 EE 符号 Top 20（硬耦合锚点）\n")
    L.append("| 符号 | 引用次数 |")
    L.append("|---|---:|")
    for s, c in sym_counter.most_common(20):
        L.append(f"| `{s}` | {c} |")
    L.append("")

    L.append("## 3. 遥测点\n")
    L.append(f"- PostHog SDK 相关行：**{telemetry['sdk_hits_total']}**")
    L.append(f"- `telemetry.utils.ts` 命中：**{telemetry['telemetry_util_hits']}** 行")
    L.append(f"- 引用 `telemetry.utils` 的生产文件：**{len(telemetry['telemetry_util_importers'])}** 个")
    L.append(f"- `community/posthog` 集成件误报行数：**{telemetry['piece_posthog_lines']}**"
             f"（{telemetry['piece_posthog_files']} 文件，与遥测无关）\n")
    if telemetry["telemetry_util_host_lines"]:
        L.append("> 硬编码外联地址（key 已打码）：\n")
        for h in telemetry["telemetry_util_host_lines"]:
            L.append(f"> - L{h['line']}: `{h['text']}`")
        L.append("")
    L.append("**调用者**\n")
    for f in telemetry["telemetry_util_importers"]:
        L.append(f"- `{f}`")
    L.append("")

    L.append("## 4. 结论提示\n")
    L.append("- 遥测位于社区目录，删 EE 不会使其停止上报，须单独处理。")
    L.append("- 结构性注册点须先改，再删目录，否则编译断裂。")
    L.append("- 本报告不构成删除授权。\n")
    return "\n".join(L)


# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser(description="EE 剥离只读扫描")
    ap.add_argument("--repo", default=r"P:\Github\AI-Hub\activepieces")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        print(f"[ERR] 仓库不存在：{repo}", file=sys.stderr)
        return 2

    scale = scan_scale(repo)
    refs = scan_refs(repo)
    structural = scan_structural(repo)
    telemetry = scan_telemetry(repo)

    os.makedirs(args.out, exist_ok=True)
    data = {"repo": repo, "scale": scale, "refs_total": len(refs),
            "refs_files": len({r["file"] for r in refs}),
            "structural": structural, "telemetry": telemetry, "refs": refs}
    with open(os.path.join(args.out, "ee-scan-data.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(args.out, "ee-scan-report.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md(repo, scale, refs, structural, telemetry))

    print(f"EE 文件 {scale['_total']['files']} / 行 {scale['_total']['lines']}")
    print(f"引用 {len(refs)} 处 / {len({r['file'] for r in refs})} 文件")
    print(f"遥测 SDK 行 {telemetry['sdk_hits_total']}，telemetry.utils 被 {len(telemetry['telemetry_util_importers'])} 个文件引用")
    print(f"报告：{os.path.join(args.out, 'ee-scan-report.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
