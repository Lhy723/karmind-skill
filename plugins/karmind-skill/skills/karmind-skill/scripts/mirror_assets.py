#!/usr/bin/env python3
"""Mirror raw-source images and attachments into wiki/assets/."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
import mimetypes
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import unquote, urlparse
import urllib.error
import urllib.request


ASSET_EXTENSIONS = {
    ".avif",
    ".bmp",
    ".csv",
    ".doc",
    ".docx",
    ".gif",
    ".jpeg",
    ".jpg",
    ".json",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".svg",
    ".tif",
    ".tiff",
    ".tsv",
    ".webp",
    ".xls",
    ".xlsx",
    ".zip",
}
IMAGE_EXTENSIONS = {
    ".avif",
    ".bmp",
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".svg",
    ".tif",
    ".tiff",
    ".webp",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "source"


def clean_markdown_target(value: str) -> str:
    value = value.strip()
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")]
    for marker in [' "', " '"]:
        if marker in value:
            return value.split(marker, 1)[0].strip()
    return value


def extension_from_ref(ref: str) -> str:
    parsed = urlparse(ref)
    return Path(unquote(parsed.path)).suffix.lower()


def is_remote(ref: str) -> bool:
    return urlparse(ref).scheme in {"http", "https"}


def is_asset_ref(ref: str, image_context: bool) -> bool:
    if ref.startswith("#") or ref.startswith("mailto:") or ref.startswith("data:"):
        return False
    ext = extension_from_ref(ref)
    if image_context:
        return True
    return ext in ASSET_EXTENSIONS


def extract_asset_refs(text: str) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    patterns = [
        ("image", re.compile(r"!\[[^\]]*\]\(([^)]+)\)")),
        ("image", re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)),
        ("attachment", re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")),
        ("attachment", re.compile(r"<a\b[^>]*\bhref=[\"']([^\"']+)[\"']", re.IGNORECASE)),
    ]

    for kind, pattern in patterns:
        for match in pattern.finditer(text):
            ref = clean_markdown_target(match.group(1))
            if not is_asset_ref(ref, kind == "image"):
                continue
            key = (kind, ref)
            if key in seen:
                continue
            seen.add(key)
            refs.append(key)
    return refs


def cache_path(root: Path) -> Path:
    return root / "wiki" / "cache" / "assets-cache.json"


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


def output_dir_for(root: Path, raw_path: Path) -> Path:
    rel = raw_path.relative_to(root).as_posix()
    digest = sha256_text(rel)[:8]
    return root / "wiki" / "assets" / f"{slugify(raw_path.stem)}-{digest}"


def safe_filename(name: str, fallback: str) -> str:
    name = unquote(name).strip() or fallback
    name = re.sub(r"[\\/:*?\"<>|]+", "-", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name or fallback


def unique_destination(directory: Path, filename: str) -> Path:
    destination = directory / filename
    if not destination.exists():
        return destination
    stem = destination.stem
    suffix = destination.suffix
    index = 2
    while True:
        candidate = directory / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def resolve_local_ref(raw_file: Path, ref: str) -> Path:
    parsed = urlparse(ref)
    raw_target = unquote(parsed.path)
    target = Path(raw_target)
    if not target.is_absolute():
        target = raw_file.parent / target
    return target.resolve()


def infer_extension_from_content_type(content_type: str | None) -> str:
    if not content_type:
        return ""
    media_type = content_type.split(";", 1)[0].strip().lower()
    return mimetypes.guess_extension(media_type) or ""


def download_remote(ref: str, destination_dir: Path, timeout: int) -> tuple[Path, str]:
    request = urllib.request.Request(ref, headers={"User-Agent": "karmind-skill/asset-mirror"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
        content_type = response.headers.get("Content-Type")

    parsed = urlparse(ref)
    basename = Path(unquote(parsed.path)).name
    ext = Path(basename).suffix.lower() or infer_extension_from_content_type(content_type)
    if not basename:
        basename = f"remote-{sha256_text(ref)[:10]}{ext or '.bin'}"
    elif not Path(basename).suffix and ext:
        basename = f"{basename}{ext}"

    destination = unique_destination(destination_dir, safe_filename(basename, f"remote-{sha256_text(ref)[:10]}{ext or '.bin'}"))
    destination.write_bytes(data)
    return destination, hashlib.sha256(data).hexdigest()


def mirror_raw_file(root: Path, raw_file: Path, download: bool, timeout: int, dry_run: bool) -> list[dict]:
    root = root.resolve()
    raw_file = raw_file.resolve()
    text = raw_file.read_text(encoding="utf-8", errors="replace")
    refs = extract_asset_refs(text)
    destination_dir = output_dir_for(root, raw_file)
    records: list[dict] = []

    for kind, ref in refs:
        record = {
            "kind": kind,
            "source_ref": ref,
            "status": "pending",
            "wiki_asset": None,
            "sha256": None,
            "error": None,
        }
        try:
            if is_remote(ref):
                if not download:
                    record["status"] = "skipped"
                    record["error"] = "remote download disabled"
                else:
                    if not dry_run:
                        destination_dir.mkdir(parents=True, exist_ok=True)
                        destination, digest = download_remote(ref, destination_dir, timeout)
                        record["wiki_asset"] = destination.relative_to(root).as_posix()
                        record["sha256"] = digest
                    record["status"] = "downloaded"
            else:
                source = resolve_local_ref(raw_file, ref)
                if not source.exists() or not source.is_file():
                    record["status"] = "missing"
                    record["error"] = "local asset not found"
                else:
                    if not dry_run:
                        destination_dir.mkdir(parents=True, exist_ok=True)
                        destination = unique_destination(destination_dir, safe_filename(source.name, "asset"))
                        shutil.copy2(source, destination)
                        record["wiki_asset"] = destination.relative_to(root).as_posix()
                        record["sha256"] = sha256_file(destination)
                    record["status"] = "copied"
                    record["local_source"] = source.as_posix()
        except (OSError, urllib.error.URLError, ValueError) as exc:
            record["status"] = "failed"
            record["error"] = str(exc)
        records.append(record)

    return records


def iter_raw_text_files(root: Path) -> list[Path]:
    raw = root / "raw"
    if not raw.exists():
        return []
    return sorted(
        path
        for path in raw.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".markdown", ".html", ".htm"}
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mirror raw-source images and attachments into wiki/assets/.")
    parser.add_argument("root", type=Path, help="Wiki root containing raw/ and wiki/.")
    parser.add_argument("raw_path", nargs="?", help="Optional raw file path, relative to wiki root or absolute.")
    parser.add_argument("--no-download", action="store_true", help="Do not download remote HTTP(S) assets.")
    parser.add_argument("--dry-run", action="store_true", help="List assets without copying or downloading.")
    parser.add_argument("--timeout", type=int, default=30, help="Remote download timeout in seconds.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    if args.raw_path:
        raw_path = Path(args.raw_path)
        raw_files = [(raw_path if raw_path.is_absolute() else root / raw_path).resolve()]
    else:
        raw_files = iter_raw_text_files(root)

    cache = load_cache(root)
    raw_cache = cache.setdefault("raw_files", {})
    total = 0
    failures = 0

    for raw_file in raw_files:
        if not raw_file.exists():
            print(f"missing raw file: {raw_file}", file=sys.stderr)
            failures += 1
            continue
        rel_raw = raw_file.relative_to(root).as_posix()
        records = mirror_raw_file(root, raw_file, not args.no_download, args.timeout, args.dry_run)
        raw_cache[rel_raw] = {
            "updated": date.today().isoformat(),
            "assets": records,
        }
        for record in records:
            total += 1
            if record["status"] == "failed":
                failures += 1
            wiki_asset = record.get("wiki_asset") or "-"
            print(f"{record['status']}\t{rel_raw}\t{record['source_ref']}\t{wiki_asset}")

    if not args.dry_run:
        save_cache(root, cache)
    print(f"assets={total} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
