# Installation Guide

Prefer enabling this skill only inside directories that actually contain an LLM Wiki. Global installation is not recommended by default because this skill scans documents, maintains `raw/`, and edits `wiki/`.

## Recommended: Claude Code Plugin

Claude Code users should prefer plugin marketplace installation:

```text
/plugin marketplace add karmind-skills Lhy723/karmind-skill
/plugin install karmind-skill@karmind-skills
```

See [CLAUDE_CODE.md](CLAUDE_CODE.md) for details.

## Skills CLI

If your agent supports the `skills` CLI, run this from the target wiki project:

```bash
npx -y skills add Lhy723/karmind-skill --skill karmind-skill --agent '*' -y
```

See [SKILLS_CLI.md](SKILLS_CLI.md) for details.

## Recommended: One-Command Install

Run the one-command installer from the target wiki project. It asks for the target agent and copies only the lightweight skill files.

macOS / Linux:

```bash
cd your-project
curl -sSL https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.sh | bash
```

Windows PowerShell:

```powershell
cd your-project
irm https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.ps1 | iex
```

To skip the prompt, specify the target agent:

macOS / Linux:

```bash
cd your-project
curl -sSL https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.sh | KARMIND_AGENT=trae bash
```

Windows PowerShell:

```powershell
cd your-project
$env:KARMIND_AGENT = "trae"; irm https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.ps1 | iex; Remove-Item Env:KARMIND_AGENT
```

Supported values: `codex`, `opencode`, `trae`, `claude`, `all`.

## Manual Install

If you are not using plugin marketplace or the `skills` CLI, manually install into the project directory using each agent's guide. Install only the lightweight runtime files: `SKILL.md`, `references/`, and `scripts/`; Codex also gets `agents/`, and Trae also gets project rules.

Manual install can use the sparse checkout commands in these docs, or you can copy the same lightweight files from a local checkout into the target directory. Do not copy README files, docs, tests, plugin distribution folders, or other repository maintenance files.

- Codex / generic agents: [CODEX.md](CODEX.md)
- OpenCode: [OPENCODE.md](OPENCODE.md)
- Trae: [TRAE.md](TRAE.md)
- Other agents: [OTHER_AGENTS.md](OTHER_AGENTS.md)

Claude Code should use plugin installation first; use the project-level fallback in [CLAUDE_CODE.md](CLAUDE_CODE.md) only when the plugin path is unavailable.

If you need user-level installation, manually place the lightweight files in the user-level directory documented by the target agent.

## Local Development Install

Preview a local checkout:

```bash
npx -y skills add . --list
```

Install the local checkout into the current project:

```bash
npx -y skills add . --skill karmind-skill --agent '*' -y
```

Claude Code local plugin install:

```text
/plugin marketplace add karmind-local <local-repo-path>
/plugin install karmind-skill@karmind-local
```

The helper scripts below come from this repository. If the current project does not contain a `scripts/` directory, call them as `/tmp/karmind-skill/scripts/...`, or use `scripts/...` from the installed skill directory.

On Windows PowerShell, use `"$env:TEMP\karmind-skill\scripts\..."`.

## Initialize Existing Notes

When a target directory already contains notes or documents, scan first:

```bash
python /tmp/karmind-skill/scripts/init_wiki.py . --scan-existing --language en
```

For a Chinese wiki, use `--language zh`; `auto` lets the script infer from existing files. For other languages, avoid permanent language packs: ask the agent to copy a temporary `init_wiki.py`, localize only human-readable template text, and run that temporary script.

After review, import candidates into `raw/imported/`:

```bash
python /tmp/karmind-skill/scripts/init_wiki.py . --import-existing move
```

Use `copy` instead of `move` if the original files should remain in place:

```bash
python /tmp/karmind-skill/scripts/init_wiki.py . --import-existing copy
```

Imported files are marked `pending` in `wiki/cache/ingest-cache.json`.

## Ingest Cache

Keep the cache current:

```bash
python /tmp/karmind-skill/scripts/ingest_cache.py . ensure
python /tmp/karmind-skill/scripts/ingest_cache.py . list --status pending
```

After manual processing:

```bash
python /tmp/karmind-skill/scripts/ingest_cache.py . mark raw/example.md --processor manual-agent --source-note wiki/sources/example.md
```

If the user explicitly asks to force re-extract, reset the cache:

```bash
python /tmp/karmind-skill/scripts/ingest_cache.py . reset
```

## Image and Attachment Mirroring

Before ingesting a raw article, copy local images/attachments referenced by the article into `wiki/assets/`, and download remote image URLs:

macOS / Linux:

```bash
python /tmp/karmind-skill/scripts/mirror_assets.py . raw/example.md
```

Windows PowerShell:

```powershell
python "$env:TEMP\karmind-skill\scripts\mirror_assets.py" . raw/example.md
```

Mirror results are recorded in `wiki/cache/assets-cache.json`. To preview without copying or downloading:

```bash
python /tmp/karmind-skill/scripts/mirror_assets.py . raw/example.md --dry-run
```

For many documents, ask the user whether to configure an external-model API loop or let the current agent process pending files manually.

Model batch helper:

macOS / Linux:

```bash
export LLM_API_KEY="..."
export LLM_MODEL="model-name"
python /tmp/karmind-skill/scripts/model_batch_ingest.py . --limit 10 --language en
```

Windows PowerShell:

```powershell
$env:LLM_API_KEY = "..."
$env:LLM_MODEL = "model-name"
python "$env:TEMP\karmind-skill\scripts\model_batch_ingest.py" . --limit 10 --language en
```

Preview pending files without calling the API:

macOS / Linux:

```bash
python /tmp/karmind-skill/scripts/model_batch_ingest.py . --dry-run --language en
```

Windows PowerShell:

```powershell
python "$env:TEMP\karmind-skill\scripts\model_batch_ingest.py" . --dry-run --language en
```

See [MODEL_KEYS.md](MODEL_KEYS.md) for API key configuration. Prefer environment variables or a local `.env.local`; do not write keys into the wiki.

For model batch processing, `--language` may be any language code; the helper asks the external model to write human-facing headings and prose in that language while keeping machine fields in English.

By default, model batch processing writes review drafts to `wiki/sources/_drafts/` and marks cache entries `drafted`. The current agent should review the raw source and draft, create the final source note, update related pages, and then mark the file `processed`. Use `--publish-final-source-notes` only when the user explicitly accepts lower-quality direct batch output.

## Agent-Specific Guides

- [Skills CLI](SKILLS_CLI.md)
- [Model API Keys](MODEL_KEYS.md)
- [Obsidian Graph](OBSIDIAN_GRAPH.md)
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
python /tmp/karmind-skill/scripts/smoke_test.py
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
- If a repair creates factual concept/entity pages, the agent should search local wiki/raw first; when evidence is insufficient, use available web search/browsing to verify authoritative sources and cite them instead of writing from memory.

After repairs, the agent should update `wiki/index.md`, append `wiki/log.md`, and rerun the doctor.
