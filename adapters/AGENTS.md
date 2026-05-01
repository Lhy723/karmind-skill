# AGENTS.md

## LLM Wiki Instructions

Use `karmind-skill` when maintaining this wiki.

- Treat `raw/` as immutable source evidence.
- Maintain generated knowledge in `wiki/`.
- Read `wiki/index.md` before editing topic pages.
- Append to `wiki/log.md` after ingest, query filing, lint, or schema maintenance.
- Maintain `wiki/cache/ingest-cache.json`; skip processed raw files unless the user asks to force re-extract. External-model outputs are drafts under `wiki/sources/_drafts/` and should stay `drafted` until reviewed.
- Cite source notes or raw files for durable claims.
- Preserve contradictions, uncertainties, and open questions.
- Do not delete or overwrite sources without explicit user approval.
- Before initializing a new wiki, scan for existing notes/documents and ask before moving or copying them into `raw/imported/`.
- For "ingest new sources", sync/list the cache first. If multiple raw files are pending and no specific source was named, ask whether to configure external-model batch processing, manually process the pending cache, process only the next file, or defer. If manual processing is chosen, do not silently stop after one file.
- In this wiki directory, normal user questions are wiki-grounded by default. Start from `wiki/index.md`, cite wiki/source files, and avoid answering durable factual questions from general model memory unless the user explicitly asks for outside knowledge.
- When fixing health-check findings, read `wiki/reports/doctor-report.md`, fix low-risk issues directly, ask before merges/splits/renames, and require approval before deletion, source-note overwrite, cache reset, batch re-ingest, or schema changes. If creating or filling missing concept/entity pages, report local search terms, inspected wiki/raw files, whether web search was used, and why the page is sourced or left as a stub. If creating factual content, search local wiki/raw first; if evidence is insufficient and web access is available, search/browse authoritative sources and cite them instead of inventing content.

If the `karmind-skill` folder is available, read its `SKILL.md` for the complete workflow.
