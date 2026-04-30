# Obsidian and Tooling Reference

Use this when the user wants the wiki to work well in Obsidian or another markdown editor, or when the wiki grows large enough to need helper tools.

## Obsidian as the Wiki IDE

- Keep pages human-readable markdown.
- Prefer stable page titles and explicit links so graph view, backlinks, and search remain useful.
- Use `raw/assets/` for downloaded images and attachments. Link important assets from source notes or topic pages.
- Use frontmatter sparingly so Dataview or property filters can help without becoming a maintenance burden.
- The agent may suggest Obsidian Web Clipper for web pages, but raw source files should still be preserved.

## Attachments and Images

When a source references images:

1. Store the original asset under `raw/assets/` or preserve the existing local path.
2. Inspect only the assets that materially affect the source summary.
3. Mention important visual evidence in the source note.
4. Link images with relative markdown links or Obsidian-compatible embeds according to the local schema.

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
