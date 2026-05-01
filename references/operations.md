# Operations Reference

## Ingest Source

Input can be a markdown clip, PDF-derived text, transcript, paper notes, CSV summary, image notes, or manually pasted source.

Steps:

1. Ensure the cache is current:
   ```bash
   python scripts/ingest_cache.py . ensure
   ```
2. List pending files before reading source content:
   ```bash
   python scripts/ingest_cache.py . list --status pending
   ```
3. If the user did not name a source and there are multiple pending files, ask the user to choose an external-model batch loop, manual agent processing through the cache, processing only the next file, or deferring.
   - External-model batch output should be treated as `drafted` review material, not final wiki knowledge.
4. If the user chooses manual agent processing, continue through pending entries until the cache is exhausted, the user stops, or the context budget requires a checkpoint. Do not stop after one file without reporting what remains.
5. If there is exactly one pending file, process it directly.
6. Skip files marked `processed` unless the user asks to force re-extract. For force re-extract, run:
   ```bash
   python scripts/ingest_cache.py . reset
   ```
7. Read the source and capture metadata: title, author, date, source path, retrieval date if web-derived.
8. Inspect important local assets or images referenced by the source when they materially affect meaning.
9. Extract durable items:
   - claims
   - definitions
   - entities
   - concepts
   - relationships
   - dates and timelines
   - contradictions with existing wiki pages
   - open questions
10. Read `wiki/index.md` and relevant existing pages.
11. Write or update the reviewed source note under `wiki/sources/`.
12. Update entity, concept, question, and synthesis pages.
13. Discuss surprising takeaways, contradictions, or important schema choices with the user when the source is high-value or ambiguous.
14. Update `wiki/index.md`.
15. Append to `wiki/log.md`.
16. Mark the file processed:
   ```bash
   python scripts/ingest_cache.py . mark raw/example.md --processor manual-agent --source-note wiki/sources/example.md --page wiki/concepts/example.md
   ```
17. Report changed pages, unresolved questions, and remaining pending count to the user.

## Initialize Existing Notes

When initializing a wiki in a directory that may already contain notes or documents:

1. Scan first:
   ```bash
   python scripts/init_wiki.py . --scan-existing
   ```
2. Ask the user whether to move, copy, or ignore candidates.
3. If approved, import into `raw/imported/`:
   ```bash
   python scripts/init_wiki.py . --import-existing move
   ```
   or:
   ```bash
   python scripts/init_wiki.py . --import-existing copy
   ```
4. Imported files are marked `pending` in `wiki/cache/ingest-cache.json`.
5. Continue ingestion from the pending cache list.

## Answer Query

Normal user questions default to this workflow when the current directory is an LLM Wiki. The user does not need to explicitly say "use the wiki".

Steps:

1. Start from `wiki/index.md`.
2. Search with `rg` if needed:
   ```bash
   rg -n "term|related phrase" wiki
   ```
3. Read relevant wiki pages and source notes.
4. Inspect raw sources only when the wiki evidence is thin or exact citation is needed.
5. Answer with citations to files used.
6. Choose the right output form: prose, comparison table, timeline, diagram, chart, slide markdown, canvas note, or maintained wiki page.
7. If the answer is reusable, create or update a page and log it.

## Lint Wiki

Steps:

1. Run:
   ```bash
   python scripts/wiki_doctor.py .
   ```
2. Review `wiki/reports/doctor-report.md`, starting with broken links.
3. Review orphan pages, missing index entries, stale pages, and untracked raw sources.
4. Turn missing information into `wiki/questions/` pages or source-finding tasks when useful.
5. Fix the smallest useful set of issues.
6. Update `wiki/index.md` and append to `wiki/log.md`.

## Fix Doctor Findings

When the user asks to fix health-check issues, treat the doctor report as a maintenance queue, not as permission to rewrite the wiki.

Steps:

1. Read `wiki/reports/doctor-report.md`; if missing, run `python scripts/wiki_doctor.py .`.
2. Triage findings:
   - Low risk: obvious broken links, missing index entries, orphan pages that have a clear parent topic, missing question pages, missing source citations.
   - Medium risk: factual concept/entity pages, duplicate pages, oversized pages, ambiguous page names, broad renames, or content that needs substantial synthesis.
   - High risk: deletion, overwriting source notes, cache reset, batch re-ingest, schema changes, or moving large sets of files.
3. Fix low-risk findings directly.
4. For medium-risk findings, write a short plan and proceed only when the user approves the merge, split, or rename.
5. For high-risk findings, ask before changing files.
6. For broken links, prefer correcting the link target. If the target concept is real but missing, create a question page first unless there is enough evidence to create a sourced concept page.
7. For orphan pages, link them from `wiki/index.md` or the nearest relevant topic page. If the page is intentionally archival, mark that explicitly in the page or index.
8. For raw files, follow `wiki/cache/ingest-cache.json`; process only pending entries unless the user requested force re-extract.
9. When a manual fix processes a raw source, mark it with `scripts/ingest_cache.py` or update the cache equivalently.
10. When creating or filling a factual concept/entity page, search local `wiki/` and `raw/` first. If local evidence is insufficient and the user has authorized repair, use available web search/browsing tools before writing factual content.
11. Prefer primary or authoritative sources. For web evidence, cite URL, title/source, and access date; use two independent sources for nontrivial claims when available.
12. If web search is unavailable, blocked, or evidence remains weak, do not invent evidence. Turn missing support into `wiki/questions/` entries or source-finding tasks.
13. Preserve contradictions with source names, dates, and confidence language.
14. Update `wiki/index.md` and append a dated maintenance entry to `wiki/log.md`.
15. Rerun `python scripts/wiki_doctor.py .`.
16. Report fixed items, external sources used, remaining issues, and items waiting for user approval.

## Contradiction Handling

When a new source conflicts with existing wiki content:

- Do not erase the older claim unless it is clearly obsolete and the schema permits replacement.
- Add a `Contradictions` or `Evidence Notes` section.
- Name the conflicting sources.
- Include dates and confidence language.
- Add an open question if resolution requires more evidence.

## Batch Work

Batch ingest is allowed only when the user asks or the source set is clearly low-risk.

For large batches:

- Ask whether to use an external-model API loop or manual agent processing.
- Use `wiki/cache/ingest-cache.json` as the manifest.
- Process only `pending` files, or review `drafted` files when the task is to promote model drafts.
- Mark files as `drafted`, `processed`, `failed`, or `skipped`.
- Write a report file with drafted, processed, skipped, failed, and needs-review items.
- Keep logs parseable.

For an unqualified request like "ingest new sources", multiple pending files count as batch work. Ask for the processing mode before extracting the first file.

For external-model batch mode, write drafts to `wiki/sources/_drafts/` and keep cache entries `drafted` until reviewed. Do not mix unreviewed model drafts with reviewed source notes.
