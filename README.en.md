<div align="center">
  <img src="assets/banner.png" alt="karmind-skill banner" width="100%" />

  <h1>karmind-skill</h1>

  <p><strong>A portable Agent Skill for maintaining a Karpathy-style LLM Wiki.</strong></p>

  <p>
    <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg" /></a>
    <a href="https://www.python.org/"><img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3776AB.svg" /></a>
    <a href="SKILL.md"><img alt="Agent Skill" src="https://img.shields.io/badge/Agent%20Skill-SKILL.md-111827.svg" /></a>
    <a href=".claude-plugin/marketplace.json"><img alt="Claude Code Plugin" src="https://img.shields.io/badge/Claude%20Code-Plugin-7C3AED.svg" /></a>
  </p>

  <p><a href="README.md">中文 README</a> | <a href="docs/zh/INSTALL.md">中文文档</a> | English | <a href="docs/en/INSTALL.md">English Docs</a></p>

</div>

`karmind-skill` is a portable Agent Skill for coding agents. It maintains a long-lived LLM Wiki: a source-grounded, linked, logged, and continuously updated Markdown knowledge base.

It follows Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) idea: instead of asking an LLM to rediscover scattered chunks from scratch every time, let an agent continuously compile sources into a structured wiki. Every new source, question, and contradiction should make the wiki more useful.

## Why This Exists

Typical RAG splits material into chunks and retrieves them at question time. An LLM Wiki is different: it separates raw evidence, maintained wiki pages, and local operating schema so an agent can maintain knowledge the way it maintains a codebase.

| Layer | Path | Role |
| --- | --- | --- |
| Raw sources | `raw/` | Immutable evidence: papers, clipped web pages, interviews, images, CSVs, PDF-derived text |
| Wiki | `wiki/` | Maintained knowledge: source notes, entity pages, concept pages, questions, synthesis |
| Schema | `AGENTS.md` | Local operating manual for directories, citations, cache, logs, and maintenance rules |

## Features

| Feature | Description |
| --- | --- |
| Wiki initialization | Creates `raw/`, `wiki/`, `wiki/index.md`, `wiki/log.md`, `wiki/cache/`, and `wiki/reports/` |
| Existing-note import | Scans existing documents and moves or copies them into `raw/imported/` after user approval |
| Source ingest | Extracts claims, entities, concepts, timelines, contradictions, and open questions |
| Cache-aware processing | Tracks `pending`, `drafted`, `processed`, `failed`, and `skipped` in `wiki/cache/ingest-cache.json` |
| Asset mirroring | Copies local raw images/attachments into `wiki/assets/` and downloads remote images |
| External model batch ingest | Uses any OpenAI-compatible model to draft reviewable source notes in batches |
| Wiki doctor | Reports broken links, orphan pages, unprocessed sources, cache status, and maintenance actions |
| Doctor finding repair | Fixes report findings only after explicit user request, with risk-based approval rules |
| Obsidian-friendly | Supports wikilinks, assets, graph/backlinks, Dataview, Canvas, and Marp-style outputs |
| Multi-agent support | Works with Codex, Claude Code, OpenCode, Trae, Skills CLI, and generic `AGENTS.md` workflows |

## Installation Guidance

Enable this skill only inside projects that actually contain an LLM Wiki. Global installation is not recommended by default because the skill scans documents and maintains `raw/` and `wiki/`, which can be noisy in ordinary code projects.

Once installed in a wiki directory, normal questions default to wiki-grounded answers. You can ask directly without saying "use the wiki" every time.

### Claude Code Plugin

Claude Code users should prefer plugin marketplace installation:

```text
/plugin marketplace add karmind-skills Lhy723/karmind-skill
/plugin install karmind-skill@karmind-skills
```

### Skills CLI

Run from the target wiki project:

```bash
npx -y skills add Lhy723/karmind-skill --skill karmind-skill --agent '*' -y
```

### Bundled Installer

The bundled helper comes from this repository. Fetch it first:

macOS / Linux:

```bash
git clone https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
```

Windows PowerShell:

```powershell
git clone https://github.com/Lhy723/karmind-skill.git "$env:TEMP\karmind-skill"
```

Then run this from the target wiki project:

macOS / Linux:

```bash
python /tmp/karmind-skill/scripts/install.py --target project-agents --project .
```

Windows PowerShell:

```powershell
python "$env:TEMP\karmind-skill\scripts\install.py" --target project-agents --project .
```

List all targets:

```bash
python /tmp/karmind-skill/scripts/install.py --list-targets
```

In Windows PowerShell, replace the script path with `"$env:TEMP\karmind-skill\scripts\install.py"`.

### Local Development Install

Preview a local checkout:

```bash
npx -y skills add . --list
```

Install the local checkout:

```bash
npx -y skills add . --skill karmind-skill --agent '*' -y
```

Claude Code local plugin install:

```text
/plugin marketplace add karmind-local /path/to/karmind-skill
/plugin install karmind-skill@karmind-local
```

## Quick Start

Open your agent in the target directory and say:

```text
Use karmind-skill to initialize an LLM Wiki in the current directory. First scan for existing notes or documents, list candidates, ask whether to move, copy, or skip them, then create raw/, wiki/, index, log, cache, and reports after confirmation.
```

During initialization, the agent should generate templates in the current conversation language. A Chinese conversation should create headings such as `摘要`, `证据`, and `待解决问题`.

After adding sources, continue with:

```text
Use karmind-skill to ingest new sources. Find pending material from the default directories, create source notes, update related entity, concept, question, or synthesis pages, and maintain the default index, log, and cache.
```

If there are many raw files:

```text
Use karmind-skill to inspect pending material. Suggest a processing order first; if external-model batch processing is appropriate, run a dry run, explain which files, model, and reports will be used, then wait for my confirmation.
```

Manual fallback command:

macOS / Linux:

```bash
python /tmp/karmind-skill/scripts/init_wiki.py . --scan-existing --language en
```

Windows PowerShell:

```powershell
python "$env:TEMP\karmind-skill\scripts\init_wiki.py" . --scan-existing --language en
```

## Recommended Wiki Layout

```text
my-llm-wiki/
├── AGENTS.md
├── raw/
│   └── assets/
└── wiki/
    ├── index.md
    ├── log.md
    ├── overview.md
    ├── assets/
    ├── sources/
    │   └── _drafts/
    ├── entities/
    ├── concepts/
    ├── questions/
    ├── synthesis/
    ├── cache/
    │   ├── ingest-cache.json
    │   └── assets-cache.json
    ├── reports/
    │   ├── doctor-report.md
    │   └── batch/
    └── templates/
```

## Common Workflows

Prefer natural-language prompts. The bundled scripts are deterministic tools for the agent or user to call when needed.

| Workflow | Recommended prompt |
| --- | --- |
| Initialize wiki | `Use karmind-skill to initialize an LLM Wiki in the current directory. First scan for existing notes or documents, list candidates, and ask whether to move, copy, or skip them.` |
| Ingest sources | `Use karmind-skill to ingest new sources.` |
| Process pending sources | `Use karmind-skill to inspect pending material, suggest what to process next by importance, and wait for my confirmation.` |
| Model batch ingest | `Use karmind-skill to configure external-model batch processing. Run a dry run first, tell me which files, model, and reports will be used, then wait for confirmation.` |
| Force re-extract | `Use karmind-skill to force re-extraction. Explain which cache entries will be reset before doing it.` |
| Default Q&A | `What evidence supports this claim?` |
| Comparative analysis | `Compare A and B in a table.` |
| Trace sources | `Which sources support this conclusion?` |
| Archive an answer | `File the previous answer.` |
| Wiki doctor | `Use karmind-skill to run a health check.` |
| Fix doctor findings | `Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.` |

When multiple pending raw files exist, `ingest new sources` asks for the processing mode first: external-model batch processing, manual agent loop, next file only, or defer.

External-model batch processing writes to `wiki/sources/_drafts/` by default and marks cache entries `drafted`; reviewed notes are promoted to `wiki/sources/` and then marked `processed`.

If a raw article references images or attachments, the agent mirrors them into `wiki/assets/`; remote image URLs are downloaded as local copies, and source notes should cite the local copies.

Wiki doctor reports are written to:

```text
wiki/reports/doctor-report.md
```

Model batch reports are written to:

```text
wiki/reports/batch/
```

Configure model API keys through environment variables or a local `.env.local`; do not write keys into the wiki. See [模型 API Key 配置](docs/zh/MODEL_KEYS.md) / [Model API Key Configuration](docs/en/MODEL_KEYS.md).

Doctor repair policy:

- Low-risk findings can be fixed directly: obvious broken links, missing index entries, orphan links, missing citations, and question-page stubs.
- Medium-risk findings need a short plan first: duplicated pages, large-page splits, and page renames.
- High-risk findings require confirmation: deleting pages, overwriting source notes, resetting cache, batch re-ingest, or schema changes.
- If a repair creates factual concept/entity pages, search local wiki/raw first; when evidence is insufficient, use available web search/browsing to verify authoritative sources and cite them instead of writing from memory.
- After repairs, update `wiki/index.md`, append `wiki/log.md`, and rerun the doctor.

## Agent Support

| Agent / Tool | Recommended approach | Docs |
| --- | --- | --- |
| Skills CLI | `npx skills add` from the project directory | [中文](docs/zh/SKILLS_CLI.md) / [English](docs/en/SKILLS_CLI.md) |
| Model API keys | Environment variables or local `.env.local` | [中文](docs/zh/MODEL_KEYS.md) / [English](docs/en/MODEL_KEYS.md) |
| Obsidian graph | Directory-responsibility color groups | [中文](docs/zh/OBSIDIAN_GRAPH.md) / [English](docs/en/OBSIDIAN_GRAPH.md) |
| Codex | Project-level `.agents/skills` | [中文](docs/zh/CODEX.md) / [English](docs/en/CODEX.md) |
| Claude Code | Plugin marketplace | [中文](docs/zh/CLAUDE_CODE.md) / [English](docs/en/CLAUDE_CODE.md) |
| OpenCode | Project-level `.opencode/skills` | [中文](docs/zh/OPENCODE.md) / [English](docs/en/OPENCODE.md) |
| Trae | Combined project rules + full skill install | [中文](docs/zh/TRAE.md) / [English](docs/en/TRAE.md) |
| Other agents | Project-level `AGENTS.md` / `CLAUDE.md` | [中文](docs/zh/OTHER_AGENTS.md) / [English](docs/en/OTHER_AGENTS.md) |

## Repository Layout

```text
.
├── SKILL.md                    # Portable Agent Skill entrypoint
├── .claude-plugin/             # Claude Code marketplace manifest
├── agents/openai.yaml          # Optional Codex app metadata
├── references/                 # On-demand skill reference docs
├── scripts/                    # Init, cache, batch, doctor, and install scripts
├── adapters/                   # Generic agent rule templates
├── assets/                     # Static assets such as the README banner
├── plugins/karmind-skill/      # Claude Code plugin distribution
├── docs/
│   ├── en/
│   └── zh/
├── examples/
└── tests/
```

## Design Principles

- Raw sources are immutable; wiki pages are maintained.
- Important claims should trace back to source notes or raw sources.
- `index.md` is for navigation, and `log.md` is for chronological history.
- `ingest-cache.json` tracks processing state. External-model output starts as `drafted`; reviewed notes become `processed`.
- Contradictions and uncertainty are part of the knowledge base and should be explicit.
- Start with Markdown, `rg`, and index files. Add vector databases, MCP search, or other tools only when scale demands them.
- Answers do not have to be prose; they can become tables, timelines, diagrams, Marp slide markdown, or Obsidian Canvas notes.

## License

MIT. See [LICENSE](LICENSE).

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Lhy723/karmind-skill&type=Date)](https://www.star-history.com/#Lhy723/karmind-skill&Date)
