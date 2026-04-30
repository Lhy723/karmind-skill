# Batch Processing and Cache Reference

Use this when a wiki has many raw files or the user asks to avoid reprocessing documents.

## User Choice

Before large extraction, ask the user to choose:

- External-model batch loop: best for many documents where a configured API model can extract source notes and structured facts.
- Manual agent processing: best for small collections, sensitive documents, or when the current agent should reason carefully.
- Defer: leave files in `pending` state for later.

Do not configure an external API without the user's approval.

## Cache Contract

Cache path:

```text
wiki/cache/ingest-cache.json
```

Statuses:

- `pending`: raw file exists but has not been organized into the wiki.
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

After external-model batch processing:

```bash
python scripts/ingest_cache.py . mark raw/example.md \
  --processor model-batch:model-name \
  --source-note wiki/sources/example.md \
  --page wiki/entities/example.md \
  --page wiki/synthesis/topic.md
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
5. Write source notes and draft updates to wiki pages.
6. Mark each file processed only after successful file writes.
7. Record failures as `failed` with a short note in the report.

Store batch outputs in a reviewable file such as:

```text
wiki/reports/batch/YYYY-MM-DD-model-batch-ingest.md
```

Bundled helper:

```bash
export LLM_API_KEY="..."
export LLM_MODEL="model-name"
python scripts/model_batch_ingest.py . --limit 10
```

Dry run:

```bash
python scripts/model_batch_ingest.py . --dry-run
```

The helper expects an OpenAI-compatible `/chat/completions` API. It drafts source notes for text-like raw files, writes a batch report, and marks successful files as `processed`.

## Manual Agent Guidance

When processing manually, follow cache gaps:

1. Run `list --status pending`.
2. Process the next highest-value source.
3. Update wiki pages, index, and log.
4. Mark the cache entry processed.
5. Continue until pending entries are exhausted or the user stops.
