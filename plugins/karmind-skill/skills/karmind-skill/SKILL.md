---
name: "karmind-skill"
description: "Maintains a persistent LLM wiki: ingest raw sources, update interlinked markdown pages, answer from the wiki with citations, and run wiki health checks. Use when the user wants an agent to manage an Obsidian-style knowledge base, personal research wiki, project memory, source synthesis, or Karpathy-inspired LLM wiki workflow."
license: "MIT"
compatibility: "Portable Agent Skill format for Codex, Claude Code, OpenCode, Trae, and agents that read SKILL.md or AGENTS.md-style instructions."
metadata:
  repository: "https://github.com/Lhy723/karmind-skill"
  topic: "llm-wiki"
---

# Karmind Skill

You are maintaining an LLM wiki: a persistent, source-grounded, interlinked set of markdown files that compounds over time. The user curates sources and asks questions; you do the reading, filing, cross-linking, synthesis, contradiction checks, and bookkeeping.

## Core Model

- `raw/` is the immutable source layer. Read it, cite it, and do not rewrite original source files unless the user explicitly asks.
- `wiki/` is the maintained knowledge layer. Create and update pages here.
- The schema is the operating manual for the wiki. Prefer `AGENTS.md`; also support `CLAUDE.md`, `.trae/rules/project_rules.md`, or equivalent agent rule files when needed.
- `wiki/index.md` is content-oriented navigation. Update it after every meaningful ingest or restructuring.
- `wiki/log.md` is chronological and append-only. Add one dated entry for every ingest, query filed back into the wiki, lint pass, schema change, or major maintenance task.
- `wiki/cache/ingest-cache.json` tracks raw files as pending, processed, skipped, or failed. Use it to avoid duplicate extraction.
- The schema should evolve with the user. Keep conventions local, explicit, and useful for the domain.

Read [references/llm-wiki-principles.md](references/llm-wiki-principles.md) when you need the philosophy and tradeoffs. Read [references/wiki-schema.md](references/wiki-schema.md) when creating or revising a wiki layout. Read [references/operations.md](references/operations.md) for detailed ingest, query, and lint workflows. Read [references/obsidian-and-tools.md](references/obsidian-and-tools.md) when the user wants Obsidian, local attachments, graph view, slides, charts, Dataview, or search tooling guidance. Read [references/batch-processing.md](references/batch-processing.md) when many raw files need external-model or cache-driven processing. Read [references/agent-adapters.md](references/agent-adapters.md) when installing or adapting this skill to a specific coding agent.

## First Moves

1. Locate the wiki root. Look for `raw/`, `wiki/`, `wiki/index.md`, `wiki/log.md`, or an `AGENTS.md` that describes an LLM wiki.
2. If no wiki exists, propose or run:
   ```bash
   python scripts/init_wiki.py . --scan-existing
   ```
3. If existing notes/documents are found outside `raw/` and `wiki/`, ask the user whether to move them into `raw/imported/`, copy them, or leave them in place. Do not move project code or user files silently.
4. If there are many raw files, ask whether to configure an external-model batch extractor or process manually with the current agent. Use the ingest cache either way.
5. Read the local schema before changing wiki files.
6. Read `wiki/index.md` before browsing individual pages. Use `rg` or the bundled doctor/search patterns for larger wikis.

## Ingest Workflow

When the user asks to ingest a source:

1. Treat the current wiki root as the default root. Do not ask the user for paths unless no wiki root or no candidate source can be found.
2. Run or emulate `python scripts/ingest_cache.py . ensure`, then process pending raw files first.
3. If the user did not name a source, choose the next pending source from the ingest cache, or the newest unprocessed raw source.
4. Skip cache entries marked `processed` unless the user asks to force re-extract; for force re-extract, reset or mark relevant cache entries pending.
5. Extract claims, entities, concepts, dates, definitions, relationships, uncertainties, and source metadata.
6. If the source references images or local assets, inspect the most relevant assets separately and cite them when they affect the summary.
7. Create or update a source note under the default source-note folder.
8. Update relevant entity, concept, timeline, question, or synthesis pages using the default wiki folders. Prefer small, named pages over one giant summary.
9. Discuss surprising takeaways, contradictions, or emphasis choices with the user when the source is important or ambiguous.
10. Add cross-links with `[[Page Name]]` or relative markdown links, following the local schema.
11. Mark contradictions, superseded claims, and confidence levels instead of smoothing them away.
12. Update index, append to log, and mark the raw file `processed` in the ingest cache.

## Query Workflow

When the current directory is an LLM Wiki, normal user questions default to wiki-grounded answers. The user should not need to say "answer from the wiki" every time.

1. Read `wiki/index.md`, then the most relevant wiki pages and source notes.
2. Answer from maintained wiki knowledge first, then inspect raw sources when citations or verification are needed.
3. Cite the wiki pages and raw sources used. If evidence is missing, say what is missing.
4. Use the output form the question deserves: prose, comparison table, timeline, chart, Marp-compatible slide markdown, canvas notes, or a new wiki page.
5. If the answer creates reusable synthesis, ask whether to file it, or file it when the user has asked for a maintained wiki.
6. If filed, update index and log.

## Lint Workflow

When asked to health-check or maintain the wiki, inspect for:

- Broken links and missing index entries.
- Orphan pages that should be linked.
- Concepts/entities mentioned repeatedly but lacking pages.
- Contradictions, stale claims, and source/date gaps.
- Pages that have grown too large and should be split.
- Raw sources that have not been ingested.
- Data gaps that should become questions or source-finding tasks.

You may run:

```bash
python scripts/wiki_doctor.py .
```

This writes `wiki/reports/doctor-report.md` by default. Then summarize the most important findings and make focused edits if the user asked you to fix them.

## Fix Doctor Findings Workflow

When the user explicitly asks to fix health-check findings:

1. Read the latest `wiki/reports/doctor-report.md`; if it does not exist, run `python scripts/wiki_doctor.py .` first.
2. Classify findings by risk before editing:
   - Low risk: fix obvious broken links, add missing index entries, link orphan pages, create missing question pages, and add source citations.
   - Medium risk: propose a short plan before merging duplicated pages, splitting large pages, or renaming pages.
   - High risk: ask first before deleting pages, overwriting source notes, resetting ingest cache, batch-reingesting raw files, or changing the wiki schema.
3. Fix the smallest useful set of issues. Prefer adding links, notes, questions, and citations over rewriting whole pages.
4. For missing evidence, create or update a page under the default questions area instead of inventing support.
5. For pending raw files, follow the ingest cache. Manual fixes must also update `wiki/cache/ingest-cache.json` when they process, skip, or fail a raw source.
6. Preserve contradictions and dated claims. Do not collapse conflicting evidence into one unsupported conclusion.
7. Update `wiki/index.md` and append a dated entry to `wiki/log.md`.
8. Run `python scripts/wiki_doctor.py .` again and report what was fixed, what remains, and what needs user approval.

## Guardrails

- Do not invent source support. Every durable claim should trace to a wiki page, source note, or raw source.
- In an LLM Wiki directory, do not answer durable/factual questions from general model memory alone unless the user explicitly asks for outside knowledge or brainstorming.
- Preserve dissent and uncertainty. Contradictions are first-class wiki content.
- Prefer incremental updates over rewrites. Keep history legible.
- Ask before deleting pages, overwriting sources, batch-ingesting many files, or making schema changes with broad effects.
- Ask before moving existing documents into `raw/`, configuring external model APIs, or resetting the ingest cache.
- Keep generated pages useful to humans in Obsidian or any markdown editor.
