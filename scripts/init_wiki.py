#!/usr/bin/env python3
"""Initialize a local LLM wiki scaffold.

For languages beyond the built-in zh/en fallback, agents should create a
temporary localized copy of this script, translate only human-readable
scaffold text in the build_* functions, then run that copy. Keep paths,
frontmatter keys and values, cache schema, status values, and Python
identifiers in English for stable tooling.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import date
from pathlib import Path
import re
import sys


DOCUMENT_EXTENSIONS = {
    ".csv",
    ".doc",
    ".docx",
    ".htm",
    ".html",
    ".json",
    ".jsonl",
    ".md",
    ".markdown",
    ".pdf",
    ".rtf",
    ".tex",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}
SKIP_DIRS = {
    ".agents",
    ".claude",
    ".git",
    ".github",
    ".opencode",
    ".trae",
    ".venv",
    "__pycache__",
    "node_modules",
    "raw",
    "wiki",
}
LANGUAGE_ALIASES = {
    "cn": "zh",
    "zh-cn": "zh",
    "zh_hans": "zh",
    "zh-hans": "zh",
    "chinese": "zh",
    "中文": "zh",
    "en-us": "en",
    "english": "en",
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "llm-wiki"


def normalize_language(value: str | None) -> str:
    if not value:
        return "auto"
    normalized = value.strip().lower().replace("_", "-")
    return LANGUAGE_ALIASES.get(normalized, normalized)


def has_cjk(text: str) -> bool:
    return re.search(r"[\u4e00-\u9fff]", text) is not None


def detect_language(root: Path, requested: str) -> str:
    requested = normalize_language(requested)
    if requested != "auto":
        return requested

    env_language = normalize_language(os.environ.get("KARMIND_LANGUAGE"))
    if env_language != "auto":
        return env_language

    for path in find_existing_documents(root)[:20]:
        if has_cjk(path.name):
            return "zh"
        if path.suffix.lower() in {".md", ".markdown", ".txt"}:
            try:
                if has_cjk(path.read_text(encoding="utf-8", errors="ignore")[:4000]):
                    return "zh"
            except OSError:
                continue

    locale = normalize_language(os.environ.get("LC_ALL") or os.environ.get("LANG"))
    if locale.startswith("zh"):
        return "zh"
    return "en"


def write_file(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def touch_gitkeep(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    keep = path / ".gitkeep"
    if not keep.exists():
        keep.write_text("", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_cache(cache_path: Path) -> dict:
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    return {
        "version": 1,
        "generated_by": "karmind-skill",
        "updated": date.today().isoformat(),
        "raw_files": {},
    }


def write_cache(cache_path: Path, cache: dict) -> None:
    cache["updated"] = date.today().isoformat()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ensure_cache(root: Path, reset: bool) -> Path:
    cache_path = root / "wiki" / "cache" / "ingest-cache.json"
    if reset:
        cache = {
            "version": 1,
            "generated_by": "karmind-skill",
            "updated": date.today().isoformat(),
            "raw_files": {},
        }
    else:
        cache = load_cache(cache_path)
    write_cache(cache_path, cache)
    return cache_path


def is_candidate_document(path: Path, root: Path) -> bool:
    if not path.is_file():
        return False
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    if any(part in SKIP_DIRS for part in rel.parts[:-1]):
        return False
    if path.name in {"AGENTS.md", "CLAUDE.md", "README.md", "LICENSE"}:
        return False
    return path.suffix.lower() in DOCUMENT_EXTENSIONS


def find_existing_documents(root: Path) -> list[Path]:
    if not root.exists():
        return []
    candidates = [p for p in root.rglob("*") if is_candidate_document(p, root)]
    return sorted(candidates)


def unique_destination(raw_dir: Path, source: Path) -> Path:
    base = raw_dir / "imported" / source.name
    if not base.exists():
        return base
    stem = source.stem
    suffix = source.suffix
    index = 2
    while True:
        candidate = raw_dir / "imported" / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def import_existing_documents(root: Path, mode: str) -> list[tuple[Path, Path]]:
    imported: list[tuple[Path, Path]] = []
    candidates = find_existing_documents(root)
    raw_dir = root / "raw"
    cache_path = root / "wiki" / "cache" / "ingest-cache.json"
    cache = load_cache(cache_path)
    raw_files = cache.setdefault("raw_files", {})

    for source in candidates:
        destination = unique_destination(raw_dir, source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if mode == "move":
            shutil.move(str(source), str(destination))
        elif mode == "copy":
            shutil.copy2(source, destination)
        else:
            raise ValueError(f"Unsupported import mode: {mode}")

        rel_destination = destination.relative_to(root).as_posix()
        raw_files[rel_destination] = {
            "status": "pending",
            "sha256": sha256_file(destination),
            "source_path": str(source),
            "imported_at": date.today().isoformat(),
            "import_mode": mode,
            "processed_at": None,
            "processor": None,
            "source_note": None,
            "wiki_pages": [],
        }
        imported.append((source, destination))

    write_cache(cache_path, cache)
    return imported


def build_agents_md(project_name: str, language: str) -> str:
    today = date.today().isoformat()
    if language == "zh":
        return f"""# AGENTS.md

## 项目

本目录是一个名为 `{project_name}` 的 LLM Wiki。

## Wiki 契约

- `raw/` 保存不可变原始资料。可以读取，不要在没有用户明确许可时改写。
- `wiki/` 保存 agent 维护的 Markdown 知识页。
- `wiki/index.md` 是内容索引，编译资料或大幅修改页面后必须更新。
- `wiki/log.md` 是追加式时间日志。使用类似 `## [YYYY-MM-DD] ingest | 标题` 的可解析标题。
- `wiki/cache/ingest-cache.json` 记录 raw 文件的 `pending`、`drafted`、`processed`、`skipped`、`failed` 状态。除非用户要求强制重新提取，否则跳过已处理文件。
- `wiki/cache/assets-cache.json` 记录 raw 文章中的本地附件副本和在线图片下载结果。
- 外部模型输出是草稿，放在 `wiki/sources/_drafts/`，复核前保持 `drafted`。
- `raw/assets/` 保存资料引用的图片和附件。
- `wiki/assets/` 保存从 raw 文章镜像出来、供 wiki 页面引用的图片和附件。
- 长期结论必须引用 source note 或 raw source 路径。
- 保留矛盾、不确定性和开放问题。
- 优先渐进式修改，避免大范围重写。
- schema 应随用户领域演化；本文件应保持本地、明确、可执行。

## 默认问答模式

- 本目录中的普通问题默认基于 wiki 回答。
- 先读 `wiki/index.md`，再读相关 wiki 页面和 source notes。
- 只有证据不足或需要精确引用时才检查 `raw/`。
- 除非用户明确要求外部知识或头脑风暴，不要只凭通用模型记忆回答事实性问题。
- 如果回答值得长期保存，建议归档到 `wiki/questions/` 或 `wiki/synthesis/`。

## 操作规则

- 第一次编译前，先检查已有笔记/文档是否应移动或复制到 `raw/imported/`。
- 除非用户要求批量编译或批准外部模型批处理，否则一次处理一个 source。
- 外部模型批处理结果只是待复核草稿；检查原文并更新相关页面后，才提升到正式 `wiki/sources/`。
- 编译 raw 文章前，先镜像重要图片和附件到 `wiki/assets/`；在线图片应下载为本地副本。
- 手动或自动处理后都要更新编译缓存（ingest cache）。
- 可复用回答归档到 `wiki/questions/` 或 `wiki/synthesis/`；必要时使用表格、时间线、图表或 slide markdown。
- 生成的报告写入 `wiki/reports/`。
- 修复体检问题时不要编造缺失事实。先搜索本地 wiki/raw；证据不足且可联网时，搜索/浏览权威来源并引用，再创建概念页或实体页。
- 如果 helper script 可用，可运行 `python scripts/wiki_doctor.py .`。

初始化日期：{today}
"""
    return f"""# AGENTS.md

## Project

This repository is an LLM wiki named `{project_name}`.

## Wiki Contract

- `raw/` contains immutable source evidence. Read from it; do not rewrite it without explicit user approval.
- `wiki/` contains agent-maintained markdown pages.
- `wiki/index.md` is the content catalog and must be updated after ingest or major page changes.
- `wiki/log.md` is append-only chronological history. Add parseable headings like `## [YYYY-MM-DD] ingest | Title`.
- `wiki/cache/ingest-cache.json` records raw files that are pending, drafted, processed, skipped, or failed. Skip processed files unless the user asks to force re-extract.
- `wiki/cache/assets-cache.json` records local attachment copies and downloaded remote images referenced by raw articles.
- External-model outputs are drafts under `wiki/sources/_drafts/` and should stay `drafted` until reviewed.
- `raw/assets/` stores images and attachments referenced by sources.
- `wiki/assets/` stores mirrored images and attachments for wiki page references.
- Durable claims should cite a source note or raw source path.
- Preserve contradictions, uncertainty, and open questions.
- Prefer incremental edits over broad rewrites.
- Let the schema evolve with the user's domain; keep conventions explicit in this file.

## Default Answer Mode

- Treat normal user questions in this directory as wiki-grounded by default.
- Start from `wiki/index.md`, then relevant wiki pages and source notes.
- Inspect `raw/` only when evidence is thin or exact citations are needed.
- Do not answer durable/factual questions from general model memory alone unless the user explicitly asks for outside knowledge or brainstorming.
- If an answer is reusable, suggest filing it into `wiki/questions/` or `wiki/synthesis/`.

## Operations

- Before first ingest, check whether existing notes/documents should be moved or copied into `raw/imported/`.
- Ingest one source at a time unless the user asks for batch ingest or approves an external-model batch processor.
- Treat external-model batch output as draft review material; promote it into reviewed `wiki/sources/` only after checking the raw source and updating related wiki pages.
- Before ingesting a raw article, mirror important images and attachments into `wiki/assets/`; remote images should be downloaded as local copies.
- Update the ingest cache after manual or automated processing.
- File reusable answers into `wiki/questions/` or `wiki/synthesis/`; use tables, timelines, diagrams, or slide markdown when that better answers the question.
- Write generated reports under `wiki/reports/`.
- When fixing health-check findings, do not invent missing factual content. Search local wiki/raw first; if evidence is insufficient and web access is available, search/browse authoritative sources and cite them before creating concept/entity pages.
- Run `python scripts/wiki_doctor.py .` if the helper script is available.

Initialized: {today}
"""


def build_index(project_name: str, language: str) -> str:
    today = date.today().isoformat()
    if language == "zh":
        return f"""# {project_name} 索引

更新日期：{today}

## 概览

- [概览](overview.md) - 当前 wiki 的高层地图。

## 资料

尚未编译资料。

## 实体

暂无实体页。

## 概念

暂无概念页。

## 问题

暂无问题页。

## 综合

暂无综合分析页。
"""
    return f"""# {project_name} Index

Updated: {today}

## Overview

- [Overview](overview.md) - Current high-level map of the wiki.

## Sources

No sources ingested yet.

## Entities

No entity pages yet.

## Concepts

No concept pages yet.

## Questions

No question pages yet.

## Synthesis

No synthesis pages yet.
"""


def build_log(project_name: str, language: str) -> str:
    today = date.today().isoformat()
    if language == "zh":
        return f"""# {project_name} 日志

## [{today}] schema | 初始化 wiki

- 创建 raw 资料层和 wiki 知识层。
- 创建 index、log、overview 和标准页面目录。
- 创建编译缓存（ingest cache）：`wiki/cache/ingest-cache.json`。
- 创建报告目录：`wiki/reports/`。
"""
    return f"""# {project_name} Log

## [{today}] schema | Initialize wiki

- Created raw source layer and wiki layer.
- Created index, log, overview, and standard page directories.
- Created ingest cache at `wiki/cache/ingest-cache.json`.
- Created report directory at `wiki/reports/`.
"""


def build_overview(project_name: str, language: str) -> str:
    if language == "zh":
        return f"""# {project_name} 概览

本页总结当前 wiki 的状态。

## 当前重点

尚未设置重点。

## 主要线索

- 将资料放入 `raw/`，然后让 agent 编译。

## 待解决问题

- 这个 wiki 应主要优化什么：研究、个人记忆、团队知识、竞品分析，还是其他领域？
"""
    return f"""# {project_name} Overview

This page summarizes the current state of the wiki.

## Current Focus

No focus has been set yet.

## Main Threads

- Add sources to `raw/` and ask an agent to ingest them.

## Open Questions

- What should this wiki optimize for: research, personal memory, team knowledge, competitive analysis, or another domain?
"""


def build_template_page(page_type: str, language: str) -> str:
    today = date.today().isoformat()
    frontmatter = f"""---
type: {page_type}
status: draft
created: {today}
last_updated: {today}
sources: []
tags: []
---
"""
    if language == "zh":
        templates = {
            "source": """# 资料标题

## 摘要

## 基本信息

- 原始文件：
- 作者/来源：
- 日期：

## 核心主张

## 证据摘录

## 提取的实体

## 提取的概念

## 更新的页面

## 待解决问题
""",
            "entity": """# 实体名称

## 简介

## 关键属性

## 时间线

## 关系

## 相关资料

## 矛盾与不确定性
""",
            "concept": """# 概念名称

## 定义

## 为什么重要

## 证据与例子

## 相关概念

## 边界与易混点

## 待解决问题
""",
            "question": """# 问题

## 当前回答

## 支持证据

## 反例或矛盾

## 仍不确定的部分

## 下一步要找的资料
""",
            "synthesis": """# 综合主题

## 核心结论

## 资料地图

## 对比与模式

## 可复用模型

## 需要回查的主张

## 后续方向
""",
        }
    else:
        templates = {
            "source": """# Source Title

## Summary

## Bibliographic Details

- Raw file:
- Author/source:
- Date:

## Key Claims

## Evidence Excerpts

## Extracted Entities

## Extracted Concepts

## Pages Updated

## Open Questions
""",
            "entity": """# Entity Name

## Overview

## Key Attributes

## Timeline

## Relationships

## Related Sources

## Contradictions and Uncertainty
""",
            "concept": """# Concept Name

## Definition

## Why It Matters

## Evidence and Examples

## Related Concepts

## Boundaries and Confusions

## Open Questions
""",
            "question": """# Question

## Current Answer

## Supporting Evidence

## Counterevidence or Contradictions

## Remaining Uncertainty

## Sources to Seek Next
""",
            "synthesis": """# Synthesis Topic

## Main Takeaways

## Source Map

## Comparisons and Patterns

## Reusable Model

## Claims to Recheck

## Next Directions
""",
        }

    body = templates.get(page_type, templates["source"])
    return f"{frontmatter}\n{body}"


def init_wiki(root: Path, force: bool, language: str = "auto") -> list[Path]:
    root = root.resolve()
    project_name = root.name
    wiki_language = detect_language(root, language)
    changed: list[Path] = []

    for directory in [
        root / "raw",
        root / "raw" / "assets",
        root / "wiki",
        root / "wiki" / "assets",
        root / "wiki" / "sources",
        root / "wiki" / "sources" / "_drafts",
        root / "wiki" / "entities",
        root / "wiki" / "concepts",
        root / "wiki" / "questions",
        root / "wiki" / "synthesis",
        root / "wiki" / "templates",
        root / "wiki" / "cache",
        root / "wiki" / "reports",
        root / "wiki" / "reports" / "batch",
    ]:
        touch_gitkeep(directory)

    files = {
        root / "AGENTS.md": build_agents_md(project_name, wiki_language),
        root / "wiki" / "index.md": build_index(project_name, wiki_language),
        root / "wiki" / "log.md": build_log(project_name, wiki_language),
        root / "wiki" / "overview.md": build_overview(project_name, wiki_language),
        root / "wiki" / "templates" / "source-note.md": build_template_page("source", wiki_language),
        root / "wiki" / "templates" / "entity.md": build_template_page("entity", wiki_language),
        root / "wiki" / "templates" / "concept.md": build_template_page("concept", wiki_language),
        root / "wiki" / "templates" / "question.md": build_template_page("question", wiki_language),
        root / "wiki" / "templates" / "synthesis.md": build_template_page("synthesis", wiki_language),
    }

    for path, content in files.items():
        if write_file(path, content, force):
            changed.append(path)

    cache_path = ensure_cache(root, reset=False)
    if cache_path not in changed:
        changed.append(cache_path)

    return changed


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize an LLM wiki scaffold.")
    parser.add_argument("root", type=Path, help="Wiki root directory to create or update.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files.")
    parser.add_argument("--scan-existing", action="store_true", help="List existing notes/documents that could be imported into raw/.")
    parser.add_argument("--import-existing", choices=["move", "copy"], help="Move or copy existing notes/documents into raw/imported/.")
    parser.add_argument("--reset-cache", action="store_true", help="Reset wiki/cache/ingest-cache.json.")
    parser.add_argument(
        "--language",
        default="auto",
        help=(
            "Scaffold language code. Built-in output is zh/en; for other languages, "
            "agents should run a temporary localized copy of this script."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    changed = init_wiki(args.root, args.force, args.language)
    root = args.root.resolve()
    print(f"Initialized LLM wiki at {args.root.resolve()}")
    if changed:
        print("Created or updated:")
        for path in changed:
            print(f"- {path}")
    else:
        print("No existing files were overwritten. Use --force to refresh scaffold files.")

    if args.reset_cache:
        cache_path = ensure_cache(root, reset=True)
        print(f"Reset ingest cache: {cache_path}")

    if args.scan_existing:
        candidates = find_existing_documents(root)
        print("Existing notes/documents outside raw/ and wiki/:")
        if candidates:
            for path in candidates:
                print(f"- {path.relative_to(root)}")
        else:
            print("- None found")

    if args.import_existing:
        imported = import_existing_documents(root, args.import_existing)
        print(f"Imported existing documents with mode={args.import_existing}:")
        if imported:
            for source, destination in imported:
                print(f"- {source.relative_to(root)} -> {destination.relative_to(root)}")
        else:
            print("- None found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
