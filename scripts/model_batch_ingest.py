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
    for path in [root / "AGENTS.md", root / "wiki" / "index.md", root / "wiki" / "templates" / "source-note.md"]:
        if path.exists() and has_cjk(path.read_text(encoding="utf-8", errors="ignore")[:4000]):
            return "zh"
    return "en"


def read_text_source(path: Path, max_chars: int) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n[TRUNCATED]"
    return text


def chat_completion(base_url: str, api_key: str, model: str, prompt: str, temperature: float, language: str) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    output_language = (
        "Simplified Chinese"
        if language == "zh"
        else "English"
        if language == "en"
        else f"the wiki language identified by language code `{language}`"
    )
    payload = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You extract source notes for a markdown LLM wiki. "
                    f"Write human-facing headings and prose in {output_language}. "
                    "Keep machine-facing metadata keys, raw paths, and wiki paths in English. "
                    "Be concise, source-grounded, and preserve uncertainty."
                ),
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


def build_prompt(raw_path: str, source_text: str, language: str) -> str:
    if language == "zh":
        return f"""请为这个 LLM Wiki raw source 创建一份 source note 草稿。

Raw path: {raw_path}

请返回 Markdown，并使用这些中文章节：

# 资料标题

## 元数据

- raw_path:
- inferred_title:
- date_or_time_period:
- author_or_origin:
- confidence:

## 摘要

## 关键论点

## 实体

## 概念

## 日期与时间线

## 矛盾或注意事项

## 建议的 Wiki 页面

## 待解决问题

Source text:

```text
{source_text}
```
"""
    language_instruction = (
        "Use English headings and prose."
        if language == "en"
        else (
            "Translate the human-facing section headings and prose into the wiki "
            f"language identified by `{language}`. Keep metadata keys such as raw_path, "
            "inferred_title, date_or_time_period, author_or_origin, and confidence in English."
        )
    )
    return f"""Create a source note for this LLM wiki raw source.

Raw path: {raw_path}

{language_instruction}

Return markdown with this semantic structure:

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


def wrap_draft_note(note: str, raw_path: str, model: str, language: str) -> str:
    notice = (
        "> 机器生成草稿。人工或主 agent 应复核原文，将有价值的内容提升到 `wiki/sources/`，然后把 raw 文件标记为 `processed`。"
        if language == "zh"
        else "> Machine-generated draft. A human or primary agent should review, promote useful claims into `wiki/sources/`, and then mark the raw file `processed`."
    )
    return f"""---
type: source-draft
status: needs-review
raw_path: {json.dumps(raw_path, ensure_ascii=False)}
processor: {json.dumps(f"model-draft:{model}", ensure_ascii=False)}
created: {date.today().isoformat()}
---

{notice}

{note.rstrip()}
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
    parser.add_argument("--language", default="auto", help="Draft language code. Default auto-detects from the wiki scaffold.")
    parser.add_argument(
        "--publish-final-source-notes",
        action="store_true",
        help="Write directly to wiki/sources/ and mark raw files processed. Default writes review drafts to wiki/sources/_drafts/.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    load_local_env()
    args = parse_args(argv)
    root = args.root.resolve()
    load_local_env(root)
    args.model = args.model or os.environ.get("LLM_MODEL") or os.environ.get("OPENAI_MODEL")
    args.base_url = args.base_url or os.environ.get("LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1"
    args.api_key = args.api_key or os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    args.language = detect_language(root, args.language)
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
    succeeded = 0
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
                build_prompt(raw_path, source_text, args.language),
                args.temperature,
                args.language,
            )
            digest = hashlib.sha256(raw_path.encode("utf-8")).hexdigest()[:8]
            source_dir = root / "wiki" / "sources"
            if args.publish_final_source_notes:
                source_note = source_dir / f"{slugify(absolute_raw.stem)}-{digest}.md"
                note_text = note.rstrip() + "\n"
                status = "processed"
                processor = f"model-batch:{args.model}"
                report_action = "processed"
            else:
                source_note = source_dir / "_drafts" / f"{slugify(absolute_raw.stem)}-{digest}.md"
                note_text = wrap_draft_note(note, raw_path, args.model, args.language)
                status = "drafted"
                processor = f"model-draft:{args.model}"
                report_action = "drafted"
            source_note.parent.mkdir(parents=True, exist_ok=True)
            source_note.write_text(note_text, encoding="utf-8")
            rel_source_note = source_note.relative_to(root).as_posix()
            ingest_cache.mark(root, raw_path, status, processor, rel_source_note, [rel_source_note])
            report_lines.append(f"- {report_action} `{raw_path}` -> `{rel_source_note}`")
            succeeded += 1
        except Exception as exc:
            ingest_cache.mark(root, raw_path, "failed", f"model-batch:{args.model}", None, [])
            report_lines.append(f"- failed `{raw_path}`: {exc}")
            failed += 1

    report_path = append_report(root, report_lines)
    success_label = "processed" if args.publish_final_source_notes else "drafted"
    print(f"{success_label}={succeeded} failed={failed} report={report_path}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
