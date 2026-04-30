#!/usr/bin/env python3
"""Build the self-contained Claude Code plugin distribution."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "karmind-skill"
PLUGIN_SKILL = PLUGIN_ROOT / "skills" / "karmind-skill"


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns("__pycache__", ".DS_Store", "*.pyc"),
    )


def copy_scripts() -> None:
    dst = PLUGIN_SKILL / "scripts"
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)
    for name in [
        "model_batch_ingest.py",
        "ingest_cache.py",
        "init_wiki.py",
        "install.py",
        "smoke_test.py",
        "wiki_doctor.py",
    ]:
        copy_file(ROOT / "scripts" / name, dst / name)


def write_readme() -> None:
    readme = PLUGIN_ROOT / "README.md"
    readme.write_text(
        """# karmind-skill Claude Code Plugin

This plugin installs the `karmind-skill` skill into Claude Code.

After installation, ask Claude Code:

```text
Use karmind-skill to initialize and maintain this LLM wiki.
```

The bundled skill includes scripts for wiki initialization, ingest cache management, wiki health checks, and optional OpenAI-compatible model batch ingest.
""",
        encoding="utf-8",
    )


def validate() -> None:
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    plugin = json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if marketplace["plugins"][0]["name"] != plugin["name"]:
        raise ValueError("marketplace plugin name does not match plugin.json name")
    required = [
        PLUGIN_SKILL / "SKILL.md",
        PLUGIN_SKILL / "references" / "operations.md",
        PLUGIN_SKILL / "scripts" / "init_wiki.py",
        PLUGIN_SKILL / "scripts" / "ingest_cache.py",
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing plugin files: " + ", ".join(str(path) for path in missing))


def main() -> int:
    if not (ROOT / "SKILL.md").exists():
        print("error: run from karmind-skill repository", file=sys.stderr)
        return 2

    PLUGIN_SKILL.mkdir(parents=True, exist_ok=True)
    copy_file(ROOT / "SKILL.md", PLUGIN_SKILL / "SKILL.md")
    copy_tree(ROOT / "references", PLUGIN_SKILL / "references")
    copy_scripts()
    copy_tree(ROOT / "adapters", PLUGIN_SKILL / "adapters")
    write_readme()
    validate()
    print(f"built Claude Code plugin at {PLUGIN_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
