# CLAUDE.md

When the task involves an LLM wiki, follow `karmind-skill`.

- `raw/` contains immutable sources.
- `wiki/` contains agent-maintained markdown pages.
- `wiki/index.md` is the content catalog.
- `wiki/log.md` is append-only chronological history.
- `wiki/cache/ingest-cache.json` tracks raw files that are pending, drafted, processed, skipped, or failed.
- External-model outputs are drafts under `wiki/sources/_drafts/` and should stay `drafted` until reviewed.
- Keep claims source-grounded and link related pages.
- Record contradictions and uncertainty instead of hiding them.
- Ask before moving existing documents into `raw/imported/`, configuring model APIs, or resetting the ingest cache.
- Normal user questions in this directory are wiki-grounded by default. Start from `wiki/index.md` and cite wiki/source files.
- When fixing health-check findings, read `wiki/reports/doctor-report.md`, fix low-risk issues directly, ask before merges/splits/renames, and require approval before deletion, source-note overwrite, cache reset, batch re-ingest, or schema changes.

Read `karmind-skill/SKILL.md` when available.
