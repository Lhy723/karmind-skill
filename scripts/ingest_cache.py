#!/usr/bin/env python3
"""Manage the karmind-skill ingest cache."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
import sys


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cache_path(root: Path) -> Path:
    return root.resolve() / "wiki" / "cache" / "ingest-cache.json"


def load_cache(root: Path) -> dict:
    path = cache_path(root)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "version": 1,
        "generated_by": "karmind-skill",
        "updated": date.today().isoformat(),
        "raw_files": {},
    }


def save_cache(root: Path, cache: dict) -> None:
    path = cache_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    cache["updated"] = date.today().isoformat()
    path.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def iter_raw_files(root: Path) -> list[Path]:
    raw = root.resolve() / "raw"
    if not raw.exists():
        return []
    return sorted(p for p in raw.rglob("*") if p.is_file() and p.name != ".gitkeep")


def ensure(root: Path) -> dict:
    root = root.resolve()
    cache = load_cache(root)
    raw_files = cache.setdefault("raw_files", {})
    today = date.today().isoformat()

    for path in iter_raw_files(root):
        rel = path.relative_to(root).as_posix()
        digest = sha256_file(path)
        entry = raw_files.get(rel)
        if entry is None:
            raw_files[rel] = {
                "status": "pending",
                "sha256": digest,
                "imported_at": None,
                "discovered_at": today,
                "processed_at": None,
                "processor": None,
                "source_note": None,
                "wiki_pages": [],
            }
        elif entry.get("sha256") != digest:
            entry["sha256"] = digest
            entry["status"] = "pending"
            entry["changed_at"] = today
            entry["processed_at"] = None
            entry["processor"] = None
    save_cache(root, cache)
    return cache


def reset(root: Path) -> dict:
    cache = {
        "version": 1,
        "generated_by": "karmind-skill",
        "updated": date.today().isoformat(),
        "raw_files": {},
    }
    save_cache(root, cache)
    return ensure(root)


def mark(root: Path, raw_path: str, status: str, processor: str | None, source_note: str | None, pages: list[str]) -> dict:
    root = root.resolve()
    cache = ensure(root)
    rel = Path(raw_path)
    if rel.is_absolute():
        rel_key = rel.resolve().relative_to(root).as_posix()
    else:
        rel_key = rel.as_posix()
    if rel_key not in cache["raw_files"]:
        raise KeyError(f"{rel_key} is not present in the ingest cache")

    entry = cache["raw_files"][rel_key]
    entry["status"] = status
    if status == "processed":
        entry["processed_at"] = date.today().isoformat()
    if status == "drafted":
        entry["drafted_at"] = date.today().isoformat()
    if processor:
        entry["processor"] = processor
    if source_note:
        entry["source_note"] = source_note
    if pages:
        entry["wiki_pages"] = pages
    save_cache(root, cache)
    return cache


def list_entries(cache: dict, status: str | None) -> list[tuple[str, dict]]:
    entries = sorted(cache.get("raw_files", {}).items())
    if status:
        entries = [(path, entry) for path, entry in entries if entry.get("status") == status]
    return entries


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage wiki/cache/ingest-cache.json.")
    parser.add_argument("root", type=Path, help="Wiki root containing raw/ and wiki/.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("ensure", help="Add missing raw files to the cache as pending.")

    list_parser = subparsers.add_parser("list", help="List cached raw files.")
    list_parser.add_argument("--status", choices=["pending", "drafted", "processed", "failed", "skipped"], help="Filter by status.")

    mark_parser = subparsers.add_parser("mark", help="Mark a raw file status.")
    mark_parser.add_argument("raw_path", help="Raw path, relative to wiki root or absolute.")
    mark_parser.add_argument("--status", default="processed", choices=["pending", "drafted", "processed", "failed", "skipped"])
    mark_parser.add_argument("--processor", help="Processor label, for example manual-agent or model-batch:gpt-4o-mini.")
    mark_parser.add_argument("--source-note", help="Source note path created for this raw file.")
    mark_parser.add_argument("--page", action="append", default=[], help="Wiki page updated. Repeat for multiple pages.")

    subparsers.add_parser("reset", help="Reset cache and rediscover raw files as pending.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.root.resolve()

    if args.command == "ensure":
        cache = ensure(root)
        print(f"cache entries: {len(cache.get('raw_files', {}))}")
        return 0

    if args.command == "list":
        cache = ensure(root)
        for path, entry in list_entries(cache, args.status):
            print(f"{entry.get('status', 'pending')}\t{path}")
        return 0

    if args.command == "mark":
        try:
            mark(root, args.raw_path, args.status, args.processor, args.source_note, args.page)
        except (KeyError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(f"marked {args.raw_path} as {args.status}")
        return 0

    if args.command == "reset":
        cache = reset(root)
        print(f"reset cache; pending entries: {len(cache.get('raw_files', {}))}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
