# Trae Project Rules: LLM Wiki

Use the `karmind-skill` workflow for LLM wiki tasks. This project rule is the trigger layer; the installed `.trae/skills/karmind-skill/SKILL.md` folder is the full workflow layer when available.

- Read `SKILL.md` from `.trae/skills/karmind-skill/` or another installed `karmind-skill` folder when available.
- Treat `raw/` as immutable source evidence.
- Maintain generated pages in `wiki/`.
- Update `wiki/index.md` after ingest and major page changes.
- Append to `wiki/log.md` after ingest, query filing, lint, or schema changes.
- Maintain `wiki/cache/ingest-cache.json` and skip processed raw files unless forced re-extraction is requested. External-model outputs are drafts under `wiki/sources/_drafts/` and should stay `drafted` until reviewed.
- Cite source notes or raw files for durable claims.
- Keep contradictions, caveats, and open questions visible.
- Before initializing a wiki, scan existing notes/documents and ask before moving or copying them into `raw/imported/`.
- For "ingest new sources", sync/list the cache first. If multiple raw files are pending and no specific source was named, ask whether to configure external-model batch processing, manually process the pending cache, process only the next file, or defer. If manual processing is chosen, do not silently stop after one file.
- Normal user questions in this directory are wiki-grounded by default. Start from `wiki/index.md` and cite wiki/source files.
- When fixing health-check findings, read `wiki/reports/doctor-report.md`, fix low-risk issues directly, ask before merges/splits/renames, and require approval before deletion, source-note overwrite, cache reset, batch re-ingest, or schema changes. If creating factual concept/entity pages, search local wiki/raw first; if evidence is insufficient and web access is available, search/browse authoritative sources and cite them instead of inventing content.
