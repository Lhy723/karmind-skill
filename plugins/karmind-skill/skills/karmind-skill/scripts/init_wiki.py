#!/usr/bin/env python3
"""Initialize a local LLM wiki scaffold."""

from __future__ import annotations

import argparse
import hashlib
import json
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


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "llm-wiki"


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


def build_agents_md(project_name: str) -> str:
    today = date.today().isoformat()
    return f"""# AGENTS.md

## Project

This repository is an LLM wiki named `{project_name}`.

## Wiki Contract

- `raw/` contains immutable source evidence. Read from it; do not rewrite it without explicit user approval.
- `wiki/` contains agent-maintained markdown pages.
- `wiki/index.md` is the content catalog and must be updated after ingest or major page changes.
- `wiki/log.md` is append-only chronological history. Add parseable headings like `## [YYYY-MM-DD] ingest | Title`.
- `wiki/cache/ingest-cache.json` records raw files that are pending or processed. Skip processed files unless the user asks to force re-extract.
- `raw/assets/` stores images and attachments referenced by sources.
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
- Update the ingest cache after manual or automated processing.
- File reusable answers into `wiki/questions/` or `wiki/synthesis/`; use tables, timelines, diagrams, or slide markdown when that better answers the question.
- Write generated reports under `wiki/reports/`.
- Run `python scripts/wiki_doctor.py .` if the helper script is available.

Initialized: {today}
"""


def build_index(project_name: str) -> str:
    today = date.today().isoformat()
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


def build_log(project_name: str) -> str:
    today = date.today().isoformat()
    return f"""# {project_name} Log

## [{today}] schema | Initialize wiki

- Created raw source layer and wiki layer.
- Created index, log, overview, and standard page directories.
- Created ingest cache at `wiki/cache/ingest-cache.json`.
- Created report directory at `wiki/reports/`.
"""


def build_overview(project_name: str) -> str:
    return f"""# {project_name} Overview

This page summarizes the current state of the wiki.

## Current Focus

No focus has been set yet.

## Main Threads

- Add sources to `raw/` and ask an agent to ingest them.

## Open Questions

- What should this wiki optimize for: research, personal memory, team knowledge, competitive analysis, or another domain?
"""


def build_template_page(page_type: str) -> str:
    today = date.today().isoformat()
    return f"""---
type: {page_type}
status: draft
created: {today}
last_updated: {today}
sources: []
tags: []
---

# Title

## Summary

## Evidence

## Links

## Open Questions
"""


def init_wiki(root: Path, force: bool) -> list[Path]:
    root = root.resolve()
    project_name = root.name
    changed: list[Path] = []

    for directory in [
        root / "raw",
        root / "raw" / "assets",
        root / "wiki",
        root / "wiki" / "sources",
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
        root / "AGENTS.md": build_agents_md(project_name),
        root / "wiki" / "index.md": build_index(project_name),
        root / "wiki" / "log.md": build_log(project_name),
        root / "wiki" / "overview.md": build_overview(project_name),
        root / "wiki" / "templates" / "source-note.md": build_template_page("source"),
        root / "wiki" / "templates" / "entity.md": build_template_page("entity"),
        root / "wiki" / "templates" / "concept.md": build_template_page("concept"),
        root / "wiki" / "templates" / "question.md": build_template_page("question"),
        root / "wiki" / "templates" / "synthesis.md": build_template_page("synthesis"),
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
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    changed = init_wiki(args.root, args.force)
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
