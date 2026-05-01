# Obsidian and Tooling Reference

Use this when the user wants the wiki to work well in Obsidian or another markdown editor, or when the wiki grows large enough to need helper tools.

## Obsidian as the Wiki IDE

- Keep pages human-readable markdown.
- Prefer stable page titles and explicit links so graph view, backlinks, and search remain useful.
- Keep original or imported assets under `raw/` when they arrive with the source. During ingest, mirror referenced assets into `wiki/assets/` and link important assets from source notes or topic pages.
- Use frontmatter sparingly so Dataview or property filters can help without becoming a maintenance burden.
- The agent may suggest Obsidian Web Clipper for web pages, but raw source files should still be preserved.

## Attachments and Images

When a source references images:

1. Preserve the original asset under `raw/` or its existing local path.
2. Run `python scripts/mirror_assets.py . <raw-path>` or mirror equivalently.
3. Copy local assets into `wiki/assets/`; download remote image URLs into `wiki/assets/`.
4. Inspect only the mirrored assets that materially affect the source summary.
5. Mention important visual evidence in the source note.
6. Link images with relative markdown links or Obsidian-compatible embeds to the `wiki/assets/` copy according to the local schema.

## Optional Output Forms

User answers can become more than prose:

- Comparison tables in markdown.
- Timelines.
- Mermaid diagrams.
- Charts or CSV summaries.
- Marp-compatible slide markdown.
- Obsidian Canvas notes, if the user's editor supports them.

File durable outputs under the most appropriate wiki folder and update `wiki/index.md`.

## Search and Scale

Start with:

```bash
rg -n "term|related phrase" wiki raw
```

As the wiki grows, the user may add optional tools:

- Full-text search indexes.
- Local embedding search.
- MCP tools that expose `raw/` and `wiki/`.
- `qmd` or notebook-style reports for analysis-heavy workflows.

Do not add a search system before `index.md`, backlinks, and `rg` are insufficient.
