#!/usr/bin/env python3
"""Produce a health report for a markdown LLM wiki."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
import re
import sys


WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MDLINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]+)?)\)")


@dataclass
class WikiState:
    root: Path
    wiki: Path
    pages: list[Path]
    page_by_stem: dict[str, Path]
    page_by_name: dict[str, Path]


def normalize_title(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).lower()


def load_state(root: Path) -> WikiState:
    root = root.resolve()
    wiki = root / "wiki"
    pages = sorted(
        p for p in wiki.rglob("*.md")
        if p.is_file() and "reports" not in p.relative_to(wiki).parts
    ) if wiki.exists() else []
    page_by_stem = {normalize_title(p.stem.replace("-", " ")): p for p in pages}
    page_by_name = {normalize_title(p.stem): p for p in pages}
    return WikiState(root=root, wiki=wiki, pages=pages, page_by_stem=page_by_stem, page_by_name=page_by_name)


def extract_links(text: str) -> tuple[list[str], list[str]]:
    wiki_links = [m.group(1).strip() for m in WIKILINK_RE.finditer(text)]
    md_links = [m.group(1).split("#", 1)[0].strip() for m in MDLINK_RE.finditer(text)]
    return wiki_links, md_links


def resolve_wikilink(state: WikiState, title: str) -> Path | None:
    key_space = normalize_title(title.replace("-", " "))
    key_raw = normalize_title(title)
    return state.page_by_stem.get(key_space) or state.page_by_name.get(key_raw)


def resolve_mdlink(source: Path, link: str) -> Path:
    return (source.parent / link).resolve()


def build_report(root: Path) -> str:
    state = load_state(root)
    lines: list[str] = []
    inbound: dict[Path, set[Path]] = {p: set() for p in state.pages}
    broken: list[str] = []
    all_link_targets: set[Path] = set()

    lines.append(f"# Wiki Doctor Report")
    lines.append("")
    lines.append(f"Date: {date.today().isoformat()}")
    lines.append(f"Root: `{state.root}`")
    lines.append("")

    required = [
        state.root / "raw",
        state.wiki,
        state.wiki / "index.md",
        state.wiki / "log.md",
    ]
    missing_required = [p for p in required if not p.exists()]

    if not state.wiki.exists():
        lines.append("## Fatal")
        lines.append("")
        lines.append("- Missing `wiki/` directory.")
        return "\n".join(lines) + "\n"

    for page in state.pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        wiki_links, md_links = extract_links(text)

        for title in wiki_links:
            target = resolve_wikilink(state, title)
            if target is None:
                broken.append(f"{page.relative_to(state.root)} -> [[{title}]]")
            else:
                inbound.setdefault(target, set()).add(page)
                all_link_targets.add(target)

        for link in md_links:
            if re.match(r"^[a-z]+://", link):
                continue
            target = resolve_mdlink(page, link)
            if not target.exists():
                broken.append(f"{page.relative_to(state.root)} -> {link}")
            else:
                inbound.setdefault(target, set()).add(page)
                all_link_targets.add(target)

    index = state.wiki / "index.md"
    log = state.wiki / "log.md"
    ignored_orphans = {index, log}
    orphans = [p for p in state.pages if p not in ignored_orphans and not inbound.get(p)]

    raw_files = sorted(
        p for p in (state.root / "raw").rglob("*")
        if p.is_file() and p.name != ".gitkeep"
    ) if (state.root / "raw").exists() else []
    source_notes = sorted((state.wiki / "sources").rglob("*.md")) if (state.wiki / "sources").exists() else []
    cache_path = state.wiki / "cache" / "ingest-cache.json"
    cache_entries: dict[str, dict] = {}
    if cache_path.exists():
        try:
            cache_entries = json.loads(cache_path.read_text(encoding="utf-8")).get("raw_files", {})
        except json.JSONDecodeError:
            cache_entries = {}
    pending_cache = sorted(path for path, entry in cache_entries.items() if entry.get("status") == "pending")
    processed_cache = sorted(path for path, entry in cache_entries.items() if entry.get("status") == "processed")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Markdown pages: {len(state.pages)}")
    lines.append(f"- Raw source files: {len(raw_files)}")
    lines.append(f"- Source notes: {len(source_notes)}")
    lines.append(f"- Cached pending raw files: {len(pending_cache)}")
    lines.append(f"- Cached processed raw files: {len(processed_cache)}")
    lines.append(f"- Broken links: {len(broken)}")
    lines.append(f"- Orphan pages: {len(orphans)}")
    lines.append("")

    lines.append("## Required Files")
    lines.append("")
    if missing_required:
        for path in missing_required:
            lines.append(f"- Missing: `{path.relative_to(state.root) if path.is_relative_to(state.root) else path}`")
    else:
        lines.append("- OK")
    lines.append("")

    lines.append("## Broken Links")
    lines.append("")
    if broken:
        for item in broken:
            lines.append(f"- {item}")
    else:
        lines.append("- None found")
    lines.append("")

    lines.append("## Orphan Pages")
    lines.append("")
    if orphans:
        for page in orphans:
            lines.append(f"- `{page.relative_to(state.root)}`")
    else:
        lines.append("- None found")
    lines.append("")

    lines.append("## Raw Sources")
    lines.append("")
    if raw_files and not source_notes:
        lines.append("- Raw files exist but no source notes were found in `wiki/sources/`.")
    elif raw_files:
        lines.append("- Raw files and source notes both exist. Review manually for uningested sources.")
    else:
        lines.append("- No raw source files found.")
    lines.append("")

    lines.append("## Ingest Cache")
    lines.append("")
    if not cache_path.exists():
        lines.append("- Missing `wiki/cache/ingest-cache.json`. Run `python scripts/ingest_cache.py . ensure`.")
    elif pending_cache:
        lines.append("- Pending raw files:")
        for path in pending_cache[:50]:
            lines.append(f"  - `{path}`")
        if len(pending_cache) > 50:
            lines.append(f"  - ... {len(pending_cache) - 50} more")
    else:
        lines.append("- No pending raw files in cache.")
    lines.append("")

    lines.append("## Suggested Next Actions")
    lines.append("")
    actions: list[str] = []
    if broken:
        actions.append("Fix broken links or create missing pages.")
    if orphans:
        actions.append("Link orphan pages from `wiki/index.md` or related pages, or mark them as archive.")
    if raw_files and not source_notes:
        actions.append("Ingest raw sources into `wiki/sources/`.")
    if pending_cache:
        actions.append("Process pending cache entries or mark intentionally skipped files.")
    if not actions:
        actions.append("Review stale claims, contradictions, and missing cross-links manually.")
    for index, action in enumerate(actions, start=1):
        lines.append(f"{index}. {action}")

    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an LLM wiki health report.")
    parser.add_argument("root", type=Path, help="Wiki root containing raw/ and wiki/.")
    parser.add_argument("--output", type=Path, help="Write report to this path. Relative paths are resolved from root. Defaults to wiki/reports/doctor-report.md.")
    parser.add_argument("--stdout", action="store_true", help="Print report instead of writing the default report file.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    report = build_report(root)

    if args.stdout:
        print(report, end="")
    else:
        output = args.output or Path("wiki/reports/doctor-report.md")
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        print(f"Wrote {output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
