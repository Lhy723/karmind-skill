# AGENTS.md

## LLM Wiki Instructions

Use `karmind-skill` when maintaining this wiki.

- Treat `raw/` as immutable source evidence.
- Maintain generated knowledge in `wiki/`.
- Read `wiki/index.md` before editing topic pages.
- Append to `wiki/log.md` after ingest, query filing, lint, or schema maintenance.
- Maintain `wiki/cache/ingest-cache.json`; skip processed raw files unless the user asks to force re-extract.
- Cite source notes or raw files for durable claims.
- Preserve contradictions, uncertainties, and open questions.
- Do not delete or overwrite sources without explicit user approval.
- Before initializing a new wiki, scan for existing notes/documents and ask before moving or copying them into `raw/imported/`.
- In this wiki directory, normal user questions are wiki-grounded by default. Start from `wiki/index.md`, cite wiki/source files, and avoid answering durable factual questions from general model memory unless the user explicitly asks for outside knowledge.
- When fixing health-check findings, read `wiki/reports/doctor-report.md`, fix low-risk issues directly, ask before merges/splits/renames, and require approval before deletion, source-note overwrite, cache reset, batch re-ingest, or schema changes.

If the `karmind-skill` folder is available, read its `SKILL.md` for the complete workflow.
