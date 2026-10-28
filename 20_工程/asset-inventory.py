#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
asset-inventory.py —— Project X / Lucida 资产与依赖盘点器（只读）

用途
----
按固定口径扫描本项目"掺和"的全部本地/远端资产，输出 Markdown 片段。
供 10_清單/项目资产与依赖总账.md 与 10_清單/资产快照日志.md 使用，
避免凭记忆描述项目现状。

铁律
----
1. 本脚本**只读**：不写任何业务仓库、不改 git 状态、不启停服务。
2. 唯一写入目标：10_清單/资产快照日志.md（仅 --append 时）。
3. 不做全盘递归 walk（node_modules 过大会拖死），只做定向探测。

用法
----
    python asset-inventory.py            # 打印 Markdown 片段
    python asset-inventory.py --append    # 追加当日快照到资产快照日志.md
"""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime

# ---------------------------------------------------------------- 配置区

REPOS = {
    "activepieces": r"P:\Github\AI-Hub\activepieces",
    "n8n": r"P:\Github\AI-Hub\n8n",
    "Lucida-Project-X-Beta": r"P:\Github\Lucida-Project-X-Beta",
}

BACKUPS = [
    r"P:\Github\_backup\activepieces.git",
    r"P:\Github\_backup\activepieces-git-20261028",
]

RUNTIME = {
    "n8n 数据库": r"P:\n8n-data\.n8n\database.sqlite",
    "n8n 数据根": r"P:\n8n-data",
}

TOOLCHAIN = [
    ("Node.js", [r"P:\Program Files\nodejs\node.exe", "-v"]),
    ("pnpm", ["cmd", "/c", "pnpm -v"]),
    ("Python", [sys.executable, "--version"]),
    ("Docker", ["docker", "--version"]),
]

BIG_DIRS = [
    ("VS Build Tools 2022", r"P:\VSBuildTools"),
]

# 关键存在性探针：(标签, 路径)
PROBES = [
    ("AP 根 LICENSE", r"P:\Github\AI-Hub\activepieces\LICENSE"),
    ("AP NOTICE.md", r"P:\Github\AI-Hub\activepieces\NOTICE.md"),
    ("AP 预检脚本", r"P:\Github\AI-Hub\activepieces\verify-preflight.ps1"),
    ("AP EE 许可归档", r"P:\Github\AI-Hub\activepieces\LICENSES\Activepieces-Enterprise-License.txt"),
    ("AP packages/ee (应已删)", r"P:\Github\AI-Hub\activepieces\packages\ee"),
    ("AP app/ee (应已删)", r"P:\Github\AI-Hub\activepieces\app\ee"),
    ("n8n LICENSE.md", r"P:\Github\AI-Hub\n8n\LICENSE.md"),
    ("n8n LICENSE_EE.md", r"P:\Github\AI-Hub\n8n\LICENSE_EE.md"),
    ("n8n 合成 openapi(dist)", r"P:\Github\AI-Hub\n8n\packages\cli\dist\public-api\v1\openapi.yml"),
    ("n8n 源 openapi(src)", r"P:\Github\AI-Hub\n8n\packages\cli\src\public-api\v1\openapi.yml"),
    ("n8n agent-library-bundle", r"P:\Github\AI-Hub\n8n\packages\cli\dist\agent-library-bundle.js"),
    ("n8n cli 入口", r"P:\Github\AI-Hub\n8n\packages\cli\bin\n8n"),
]

LOG_FILE = r"P:\Github\Lucida-Project-X-Beta\10_清單\资产快照日志.md"


# ---------------------------------------------------------------- 工具函数

def run(args, cwd=None, timeout=25):
    """执行命令，失败返回空串，不抛异常。"""
    try:
        r = subprocess.run(
            args, cwd=cwd, capture_output=True, text=True,
            timeout=timeout, encoding="utf-8", errors="replace",
        )
        return (r.stdout or "") + (r.stderr or "")
    except Exception:
        return ""


def git(repo, *args):
    if not os.path.isdir(repo):
        return ""
    return run(["git", "-C", repo, *args]).strip()


def dir_size_fast(path):
    """仅统计顶层文件 + 一级子目录的下一层，避开 node_modules 深递归。"""
    if not os.path.isdir(path):
        return None
    total = 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False) and entry.name not in (".git", "node_modules"):
                    for sub in os.scandir(entry.path):
                        if sub.is_file(follow_symlinks=False):
                            total += sub.stat().st_size
            except OSError:
                continue
    except OSError:
        return None
    return total


def human(nbytes):
    if nbytes is None:
        return "—"
    for unit in ("B", "KB", "MB", "GB"):
        if nbytes < 1024 or unit == "GB":
            return f"{nbytes:.1f} {unit}" if unit != "B" else f"{int(nbytes)} B"
        nbytes /= 1024.0
    return "—"


# ---------------------------------------------------------------- 采集

def collect():
    now = datetime.now()
    out = []
    w = out.append

    w(f"## 快照 {now.strftime('%Y-%m-%d %H:%M')}")
    w("")

    # --- 仓库状态
    w("### 仓库状态")
    w("")
    w("| 仓库 | 分支 | HEAD | 未提交 | remote |")
    w("|---|---|---|---|---|")
    for name, path in REPOS.items():
        if not os.path.isdir(path):
            w(f"| {name} | — | **缺失** | — | — |")
            continue
        branch = git(path, "branch", "--show-current") or "(detached)"
        head = git(path, "log", "-1", "--format=%h %ad", "--date=short") or "—"
        dirty_raw = git(path, "status", "--porcelain")
        dirty = len([x for x in dirty_raw.splitlines() if x.strip()])
        remotes = git(path, "remote")
        remotes = ", ".join(remotes.split()) if remotes else "无"
        w(f"| {name} | {branch} | {head} | {dirty} | {remotes} |")
    w("")

    # --- 关键探针
    w("### 关键资产探针")
    w("")
    w("| 项 | 状态 |")
    w("|---|---|")
    for label, p in PROBES:
        w(f"| {label} | {'存在' if os.path.exists(p) else '**不存在**'} |")
    w("")

    # --- 运行数据
    w("### 运行数据")
    w("")
    w("| 项 | 大小 | 路径 |")
    w("|---|---|---|")
    for label, p in RUNTIME.items():
        if os.path.exists(p):
            size = os.path.getsize(p) if os.path.isfile(p) else dir_size_fast(p)
            w(f"| {label} | {human(size)} | `{p}` |")
        else:
            w(f"| {label} | **缺失** | `{p}` |")
    w("")

    # --- 工具链
    w("### 工具链")
    w("")
    w("| 工具 | 版本/状态 |")
    w("|---|---|")
    for label, cmd in TOOLCHAIN:
        out_txt = run(cmd).strip().splitlines()
        val = out_txt[0].strip() if out_txt else "**不可用**"
        w(f"| {label} | {val} |")
    w("")

    # --- 大件目录
    w("### 大件占用")
    w("")
    w("| 项 | 估算 | 路径 |")
    w("|---|---|---|")
    for label, p in BIG_DIRS:
        w(f"| {label} | {'存在（体积见磁盘）' if os.path.exists(p) else '未安装'} | `{p}` |")
    for p in BACKUPS:
        w(f"| 备份 `{os.path.basename(p)}` | {'存在' if os.path.exists(p) else '**缺失**'} | `{p}` |")
    w("")

    return "\n".join(out)


# ---------------------------------------------------------------- 主流程

def main():
    text = collect()
    if "--append" not in sys.argv:
        print(text)
        return

    header = (
        "# 资产快照日志\n\n"
        "> 由 `20_工程/asset-inventory.py` 自动追加，仅供追溯，不手工编辑历史段落。\n"
        "> 口径与《项目资产与依赖总账》一致；如需改口径，先改脚本再重跑。\n\n"
    )

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(header)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n---\n\n")

    print(f"已追加当日快照：{LOG_FILE}")


if __name__ == "__main__":
    main()
