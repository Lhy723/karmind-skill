# Usage Prompts

## Initialize

```text
Use karmind-skill to initialize an LLM wiki here.
```

```text
Use karmind-skill to initialize a wiki here. First scan for existing notes and ask me whether to move, copy, or skip them.
```

## Ingest

```text
Use karmind-skill to ingest new sources. Use the default wiki locations.
```

```text
There are many sources. Ask me whether to configure an external-model batch loop or process manually, then use the ingest cache so processed files are skipped.
```

```text
Configure the model-batch ingest helper with my OpenAI-compatible API settings, run a dry run first, then process the next pending text sources and write a batch report.
```

## Query

```text
What are the strongest arguments for maintaining a wiki instead of relying on RAG?
```

## Lint

```text
Use karmind-skill to run a health check.
```

```text
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```
