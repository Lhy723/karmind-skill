# Obsidian Graph Color Groups

This palette groups the graph by LLM Wiki responsibility rather than file extension. The goal is to make the flow from `raw/` evidence to source notes, concepts, entities, questions, and synthesis visible in Obsidian Graph View.

## How to Use

In Obsidian, open:

```text
Graph View -> Filters -> Groups -> New group
```

Add the following queries and colors. Keep the order when possible; specific groups should appear before broader path groups.

## Recommended Groups

| Order | Name | Query | Color | Purpose |
| --- | --- | --- | --- | --- |
| 1 | Source Drafts | `path:wiki/sources/_drafts` | `#A855F7` | External-model or unreviewed source-note drafts |
| 2 | Reviewed Sources | `path:wiki/sources -path:wiki/sources/_drafts` | `#2563EB` | Reviewed source notes, the bridge from evidence to wiki pages |
| 3 | Concepts | `path:wiki/concepts` | `#16A34A` | Concepts, mechanisms, definitions, methods |
| 4 | Entities | `path:wiki/entities` | `#0891B2` | People, organizations, products, projects, places |
| 5 | Questions | `path:wiki/questions` | `#E11D48` | Open questions, hypotheses, research tasks |
| 6 | Synthesis | `path:wiki/synthesis` | `#D97706` | Cross-source synthesis, comparisons, models, conclusions |
| 7 | Core Navigation | `path:wiki/index.md OR path:wiki/overview.md OR path:wiki/log.md` | `#6366F1` | Index, overview, log |
| 8 | Assets | `path:wiki/assets OR path:raw/assets` | `#0D9488` | Mirrored images, attachments, original assets |
| 9 | Raw Evidence | `path:raw -path:raw/assets` | `#71717A` | Immutable raw source layer |
| 10 | Reports and Cache | `path:wiki/reports OR path:wiki/cache` | `#64748B` | Doctor reports, batch reports, cache files |

If your Obsidian version does not support `OR` or negative queries, split those groups into multiple entries or start with only `path:wiki/sources/_drafts`, `path:wiki/sources`, `path:wiki/concepts`, `path:wiki/entities`, `path:wiki/questions`, `path:wiki/synthesis`, and `path:raw`.

## Design Rationale

- Blue marks reviewed evidence: `wiki/sources/`.
- Green marks reusable concepts: `wiki/concepts/`.
- Cyan marks entities: `wiki/entities/`.
- Red marks uncertainty and work still to resolve: `wiki/questions/`.
- Amber marks synthesis output: `wiki/synthesis/`.
- Purple marks drafts so they are not mistaken for reviewed knowledge.
- Gray lowers the visual weight of raw evidence, reports, and cache files.

## Suggested Graph View Settings

Start with:

```text
Show attachments: on
Show existing files only: on
Show orphans: on
```

If the graph is too noisy:

```text
Show attachments: off
Show orphans: off
```

For maintenance checks:

```text
Show orphans: on
```

Orphaned `concepts/`, `entities/`, or `synthesis/` pages usually indicate missing index links, source-note links, or backlinks.

## Optional Tag Layer

Path-based groups are the stable default. Add tags only when a page crosses directory responsibilities:

```yaml
tags:
  - llm-wiki/concept
  - llm-wiki/needs-review
```

Then add a graph group like:

```text
tag:#llm-wiki/needs-review
```

Do not depend on heavy tagging too early; keep the folder structure and links clear first.
