# Wiki Schema Reference

Use this reference when creating or revising a wiki layout.

## Recommended Structure

```text
wiki-root/
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
    └── reports/
        ├── doctor-report.md
        └── batch/
```

## Required Files

`raw/`

- Immutable source evidence. The agent reads from this layer and does not rewrite it without explicit approval.
- `raw/assets/` stores local images and attachments, especially files downloaded from clipped web pages.
- Raw sources can include markdown, PDFs, transcripts, images, CSVs, HTML clips, and other source material.

`wiki/index.md`

- Content-oriented catalog.
- Group pages by type: overview, sources, entities, concepts, questions, synthesis.
- Each entry should have a link and a one-line description.
- Update after every ingest or major maintenance pass.

`wiki/log.md`

- Append-only chronological record.
- Use parseable headings:
  ```markdown
  ## [YYYY-MM-DD] ingest | Source Title
  ```
- Include changed pages, source files, decisions, and open questions.

`wiki/cache/ingest-cache.json`

- Operational cache for raw source processing.
- Tracks each raw file as `pending`, `drafted`, `processed`, `skipped`, or `failed`.
- Includes hash, processor, source note, updated wiki pages, and timestamps.
- Agents must update it whether processing is manual or automated.
- Reset only when the user asks for forced re-extraction.

`wiki/assets/`

- Local wiki copies of images and attachments referenced by raw sources.
- Local assets are copied here; remote image URLs are downloaded here during ingest.
- Source notes and topic pages should link to `wiki/assets/` copies for durable browsing.
- Keep `raw/` unchanged; mirrored assets are working copies for the wiki layer.

`wiki/cache/assets-cache.json`

- Operational cache for asset mirroring.
- Tracks each raw file's referenced images/attachments, copy/download status, wiki asset path, hash, and errors.

`wiki/reports/`

- Generated health checks, batch ingest reports, and other operational reports.
- `wiki/reports/doctor-report.md` is the default wiki doctor output.
- Batch processing reports should live under `wiki/reports/batch/`.

`AGENTS.md`

- Defines wiki conventions for all agents.
- Should be short, local, and specific.
- May point to this skill for detailed workflows.

## Page Types

Use the wiki's established language for page headings and prose. A Chinese wiki should use headings such as `摘要`, `证据`, `链接`, and `待解决问题` instead of English boilerplate headings unless the local schema intentionally says otherwise.

Source note: `wiki/sources/<source-slug>.md`

- Bibliographic/source metadata.
- Concise summary.
- Key claims.
- Extracted entities and concepts.
- Links to pages updated because of this source.
- Open questions and caveats.

Source draft: `wiki/sources/_drafts/<source-slug>.md`

- Machine-generated or otherwise unreviewed extraction output.
- Must be visibly marked as draft or `needs-review`.
- Does not count as a reviewed source note.
- After review, promote useful content into `wiki/sources/`, update related pages, and mark the raw file `processed`.

Entity page: `wiki/entities/<entity-name>.md`

- Who/what the entity is.
- Known attributes.
- Timeline or relationship notes when useful.
- Sources and contradictions.

Concept page: `wiki/concepts/<concept-name>.md`

- Definition.
- Competing interpretations.
- Related concepts.
- Evidence and examples.

Question page: `wiki/questions/<question-slug>.md`

- The question asked.
- Current answer.
- Evidence.
- Remaining uncertainty.
- Follow-up sources to seek.

Synthesis page: `wiki/synthesis/<topic>.md`

- Higher-level analysis across sources.
- Comparisons, models, timelines, or takeaways.
- Claims should link back to source notes or raw evidence.

## Frontmatter

Frontmatter is optional but recommended for larger wikis:

```yaml
---
type: concept
status: active
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
sources:
  - wiki/sources/example.md
tags:
  - example
---
```

Keep frontmatter stable and sparse. Do not let metadata become harder to maintain than the page itself.

## Links

- Use Obsidian wikilinks such as `[[Page Name]]` when the wiki is mainly browsed in Obsidian.
- Use relative markdown links when GitHub rendering matters more.
- Do not leave unexplained dangling links. If a page should exist but does not yet, add it to open questions or create a short stub.
