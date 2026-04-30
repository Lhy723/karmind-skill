#!/usr/bin/env python3
"""Draft source notes for pending raw files with an OpenAI-compatible model API."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

import ingest_cache


TEXT_EXTENSIONS = {
    ".csv",
    ".htm",
    ".html",
    ".json",
    ".jsonl",
    ".md",
    ".markdown",
    ".rtf",
    ".tex",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_local_env(root: Path | None = None) -> None:
    candidates = [Path.cwd() / ".env.local", Path.cwd() / ".env"]
    if root is not None:
        candidates.extend([root / ".env.local", root / ".env"])
    for path in candidates:
        load_env_file(path)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "source"


def read_text_source(path: Path, max_chars: int) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n[TRUNCATED]"
    return text


def chat_completion(base_url: str, api_key: str, model: str, prompt: str, temperature: float) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {
                "role": "system",
                "content": "You extract source notes for a markdown LLM wiki. Be concise, source-grounded, and preserve uncertainty.",
            },
            {"role": "user", "content": prompt},
        ],
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API request failed: {exc.code} {body}") from exc
    return data["choices"][0]["message"]["content"]


def build_prompt(raw_path: str, source_text: str) -> str:
    return f"""Create a source note for this LLM wiki raw source.

Raw path: {raw_path}

Return markdown with these sections:

# Source Title

## Metadata

- raw_path:
- inferred_title:
- date_or_time_period:
- author_or_origin:
- confidence:

## Summary

## Key Claims

## Entities

## Concepts

## Dates and Timeline

## Contradictions or Caveats

## Suggested Wiki Pages

## Open Questions

Source text:

```text
{source_text}
```
"""


def append_report(root: Path, lines: list[str]) -> Path:
    report_dir = root / "wiki" / "reports" / "batch"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{date.today().isoformat()}-model-batch-ingest.md"
    existing = report_path.read_text(encoding="utf-8") if report_path.exists() else f"# Model Batch Ingest {date.today().isoformat()}\n\n"
    report_path.write_text(existing + "\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Use an OpenAI-compatible model to draft source notes for pending raw files.")
    parser.add_argument("root", type=Path, help="Wiki root containing raw/ and wiki/.")
    parser.add_argument("--model", help="Model name. Can also use LLM_MODEL or OPENAI_MODEL.")
    parser.add_argument("--base-url", help="OpenAI-compatible base URL. Can also use LLM_BASE_URL or OPENAI_BASE_URL.")
    parser.add_argument("--api-key", help="API key. Prefer env LLM_API_KEY or OPENAI_API_KEY.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum pending files to process.")
    parser.add_argument("--max-chars", type=int, default=40000, help="Maximum characters sent per source.")
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--dry-run", action="store_true", help="List files that would be processed without calling the API.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    load_local_env()
    args = parse_args(argv)
    root = args.root.resolve()
    load_local_env(root)
    args.model = args.model or os.environ.get("LLM_MODEL") or os.environ.get("OPENAI_MODEL")
    args.base_url = args.base_url or os.environ.get("LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1"
    args.api_key = args.api_key or os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    cache = ingest_cache.ensure(root)
    pending = [
        (path, entry)
        for path, entry in sorted(cache.get("raw_files", {}).items())
        if entry.get("status") == "pending"
    ][: args.limit]

    if not pending:
        print("No pending raw files.")
        return 0

    if args.dry_run:
        for raw_path, _entry in pending:
            print(raw_path)
        return 0

    if not args.api_key:
        print("error: missing API key. Set LLM_API_KEY or OPENAI_API_KEY.", file=sys.stderr)
        return 2
    if not args.model:
        print("error: missing model. Pass --model or set LLM_MODEL.", file=sys.stderr)
        return 2

    report_lines: list[str] = []
    processed = 0
    failed = 0

    for raw_path, _entry in pending:
        absolute_raw = root / raw_path
        if absolute_raw.suffix.lower() not in TEXT_EXTENSIONS:
            ingest_cache.mark(root, raw_path, "failed", f"model-batch:{args.model}", None, [])
            report_lines.append(f"- failed `{raw_path}`: unsupported binary or non-text extension")
            failed += 1
            continue

        try:
            source_text = read_text_source(absolute_raw, args.max_chars)
            note = chat_completion(
                args.base_url,
                args.api_key,
                args.model,
                build_prompt(raw_path, source_text),
                args.temperature,
            )
            digest = hashlib.sha256(raw_path.encode("utf-8")).hexdigest()[:8]
            source_note = root / "wiki" / "sources" / f"{slugify(absolute_raw.stem)}-{digest}.md"
            source_note.parent.mkdir(parents=True, exist_ok=True)
            source_note.write_text(note.rstrip() + "\n", encoding="utf-8")
            rel_source_note = source_note.relative_to(root).as_posix()
            ingest_cache.mark(root, raw_path, "processed", f"model-batch:{args.model}", rel_source_note, [rel_source_note])
            report_lines.append(f"- processed `{raw_path}` -> `{rel_source_note}`")
            processed += 1
        except Exception as exc:
            ingest_cache.mark(root, raw_path, "failed", f"model-batch:{args.model}", None, [])
            report_lines.append(f"- failed `{raw_path}`: {exc}")
            failed += 1

    report_path = append_report(root, report_lines)
    print(f"processed={processed} failed={failed} report={report_path}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
