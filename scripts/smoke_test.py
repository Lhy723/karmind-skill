#!/usr/bin/env python3
"""Run a lightweight end-to-end check for bundled scripts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout


def main() -> int:
    with TemporaryDirectory() as tmp:
        wiki = Path(tmp) / "demo-wiki"
        run([sys.executable, str(ROOT / "scripts" / "init_wiki.py"), str(wiki)])
        run([sys.executable, str(ROOT / "scripts" / "ingest_cache.py"), str(wiki), "ensure"])
        run([sys.executable, str(ROOT / "scripts" / "wiki_doctor.py"), str(wiki)])
        report_path = wiki / "wiki" / "reports" / "doctor-report.md"
        report = report_path.read_text(encoding="utf-8")
        required = [
            wiki / "AGENTS.md",
            wiki / "raw",
            wiki / "wiki" / "index.md",
            wiki / "wiki" / "log.md",
            wiki / "wiki" / "cache" / "ingest-cache.json",
            report_path,
        ]
        missing = [p for p in required if not p.exists()]
        if missing:
            for path in missing:
                print(f"missing: {path}", file=sys.stderr)
            return 1
        if "Broken links: 0" not in report:
            print(report)
            print("expected no broken links in fresh wiki", file=sys.stderr)
            return 1
    print("smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
