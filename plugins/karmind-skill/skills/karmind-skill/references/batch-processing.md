# Batch Processing and Cache Reference

Use this when a wiki has multiple raw files, many raw files, or the user asks to avoid reprocessing documents.

## User Choice

Before extracting multiple pending files, ask the user to choose:

- External-model batch loop: best for many documents where a configured API model can draft source notes and structured facts for later review.
- Manual agent processing: best for small collections, sensitive documents, or when the current agent should reason carefully.
- Defer: leave files in `pending` state for later.

Do not configure an external API without the user's approval.

For an unqualified request like "compile new sources" or "ingest new sources", first run the cache sync/list step. If more than one pending file exists, ask for this choice before extracting the first file. If the user chooses manual agent processing, continue through cache gaps until no pending files remain, the user stops, or a context checkpoint is needed.

## Cache Contract

Cache path:

```text
wiki/cache/ingest-cache.json
```

Statuses:

- `pending`: raw file exists but has not been organized into the wiki.
- `drafted`: an external model created a review draft, usually under `wiki/sources/_drafts/`, but the draft has not been promoted into reviewed wiki knowledge.
- `processed`: source note and relevant wiki pages were updated.
- `failed`: processing was attempted but needs retry or human review.
- `skipped`: user or schema decided not to ingest this file.

Before processing:

```bash
python scripts/ingest_cache.py . ensure
python scripts/ingest_cache.py . list --status pending
```

After manual processing:

```bash
python scripts/ingest_cache.py . mark raw/example.md \
  --processor manual-agent \
  --source-note wiki/sources/example.md \
  --page wiki/concepts/example.md
```

After external-model batch processing, keep the raw file in `drafted` state unless the user explicitly requested final publication:

```bash
python scripts/ingest_cache.py . mark raw/example.md \
  --status drafted \
  --processor model-draft:model-name \
  --source-note wiki/sources/_drafts/example.md
```

Force re-extract:

```bash
python scripts/ingest_cache.py . reset
```

Only reset when the user explicitly asks to force re-extract. Otherwise preserve processed entries.

## Model Batch Loop Guidance

A model batch extraction loop should:

1. Read pending raw files from the cache.
2. Convert binary documents to text first when needed.
3. Send one source at a time to the model.
4. Ask for structured extraction: summary, claims, entities, concepts, dates, contradictions, open questions, suggested wiki pages.
5. Write draft source notes to `wiki/sources/_drafts/`, not directly to reviewed `wiki/sources/`.
6. Mark each successful file `drafted`.
7. Record failures as `failed` with a short note in the report.

Store batch outputs in a reviewable file such as:

```text
wiki/reports/batch/YYYY-MM-DD-model-batch-ingest.md
```

Bundled helper:

```bash
export LLM_API_KEY="..."
export LLM_MODEL="model-name"
python scripts/model_batch_ingest.py . --limit 10 --language auto
```

Dry run:

```bash
python scripts/model_batch_ingest.py . --dry-run --language auto
```

The helper expects an OpenAI-compatible `/chat/completions` API. By default it writes draft source notes under `wiki/sources/_drafts/`, writes a batch report, and marks successful files as `drafted`.

Use `--language zh`, `--language en`, or another language code to force draft headings and prose. `auto` reads the wiki scaffold and templates. Because this helper calls an LLM, non-zh/en languages are requested from the model instead of maintained as static language packs.

To bypass review and publish directly into `wiki/sources/`, pass `--publish-final-source-notes`. Use this only for low-risk sources or after the user explicitly accepts lower-quality batch output.

## Promoting Drafts

When reviewing a `drafted` raw file:

1. Read the raw source, the model draft, and relevant existing wiki pages.
2. Create or update a reviewed source note under `wiki/sources/`.
3. Promote only source-grounded, useful claims; discard weak or generic draft text.
4. Update related entity, concept, question, synthesis, index, and log pages.
5. Mark the raw file `processed` with the reviewed source note path.

## Manual Agent Guidance

When processing manually, follow cache gaps:

1. Run `list --status pending`.
2. Process the next highest-value source.
3. Update wiki pages, index, and log.
4. Mark the cache entry processed.
5. Continue until pending entries are exhausted, the user stops, or context budget requires a checkpoint.
6. If pausing, report the remaining pending count and the next file to process.
