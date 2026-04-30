# Installation Guide

Prefer enabling this skill only inside directories that actually contain an LLM Wiki. Global installation is not recommended by default because this skill scans documents, maintains `raw/`, and edits `wiki/`.

Prefer the `skills` CLI from the target project directory:

```bash
npx -y skills add Lhy723/karmind-skill --skill karmind-skill --agent '*' -y
```

Preview a local checkout:

```bash
npx -y skills add . --list
```

Install the local checkout into the current project:

```bash
npx -y skills add . --skill karmind-skill --agent '*' -y
```

See [SKILLS_CLI.md](SKILLS_CLI.md) for details.

You can also install with the bundled helper script. Project-level install is recommended:

```bash
python scripts/install.py --target project-agents --project .
```

Use user-level install only when you intentionally want the skill available everywhere:

```bash
python scripts/install.py --target codex-user
python scripts/install.py --target claude-user
python scripts/install.py --target opencode-user
python scripts/install.py --target trae-user
```

List available targets:

```bash
python scripts/install.py --list-targets
```

Use `--symlink` during development:

```bash
python scripts/install.py --target project-agents --project . --symlink --force
```

## Initialize Existing Notes

When a target directory already contains notes or documents, scan first:

```bash
python scripts/init_wiki.py . --scan-existing
```

After review, import candidates into `raw/imported/`:

```bash
python scripts/init_wiki.py . --import-existing move
```

Use `copy` instead of `move` if the original files should remain in place:

```bash
python scripts/init_wiki.py . --import-existing copy
```

Imported files are marked `pending` in `wiki/cache/ingest-cache.json`.

## Ingest Cache

Keep the cache current:

```bash
python scripts/ingest_cache.py . ensure
python scripts/ingest_cache.py . list --status pending
```

After manual processing:

```bash
python scripts/ingest_cache.py . mark raw/example.md --processor manual-agent --source-note wiki/sources/example.md
```

If the user explicitly asks to force re-extract, reset the cache:

```bash
python scripts/ingest_cache.py . reset
```

For many documents, ask the user whether to configure an external-model API loop or let the current agent process pending files manually.

Model batch helper:

```bash
export LLM_API_KEY="..."
export LLM_MODEL="model-name"
python scripts/model_batch_ingest.py . --limit 10
```

Preview pending files without calling the API:

```bash
python scripts/model_batch_ingest.py . --dry-run
```

See [MODEL_KEYS.md](MODEL_KEYS.md) for API key configuration. Prefer environment variables or a local `.env.local`; do not write keys into the wiki.

## Agent-Specific Guides

- [Skills CLI](SKILLS_CLI.md)
- [Model API Keys](MODEL_KEYS.md)
- [Codex](CODEX.md)
- [Claude Code](CLAUDE_CODE.md)
- [OpenCode](OPENCODE.md)
- [Trae](TRAE.md)
- [Other agents](OTHER_AGENTS.md)

## Verify

Ask your agent:

```text
What skills are available?
```

Then try:

```text
Use karmind-skill to initialize an LLM Wiki in the current directory.
```

You can also run:

```bash
python scripts/smoke_test.py
```

Wiki doctor reports are written by default to:

```text
wiki/reports/doctor-report.md
```

## Doctor And Repair

Run a health check:

```text
Use karmind-skill to run a health check.
```

When you explicitly ask for repairs, the agent reads `wiki/reports/doctor-report.md` and triages findings by risk:

- Low risk: fix obvious broken links, missing index entries, orphan links, missing citations, and question-page stubs directly.
- Medium risk: propose a plan before merges, splits, or renames.
- High risk: confirm before deleting pages, overwriting source notes, resetting cache, batch re-ingesting, or changing schema.

After repairs, the agent should update `wiki/index.md`, append `wiki/log.md`, and rerun the doctor.
