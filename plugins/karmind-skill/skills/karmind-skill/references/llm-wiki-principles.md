# LLM Wiki Principles

## Pattern

An LLM wiki is not a chunk store. It is a maintained, human-readable markdown knowledge base that sits between raw sources and user questions.

The agent does not rediscover everything from scratch on each query. It incrementally compiles knowledge into durable pages, links related ideas, records disagreements, and keeps summaries current.

## Roles

- Human: curates sources, directs attention, asks questions, reviews important changes.
- Agent: reads sources, extracts structure, updates pages, cross-links, logs work, and flags uncertainty.
- Wiki: the durable artifact. It should become more useful after every source and every serious question.

## Three Layers

1. Raw sources: immutable evidence. Articles, papers, notes, transcripts, images, CSVs, PDFs, or clipped markdown.
2. Wiki: generated and maintained markdown pages. Summaries, entities, concepts, timelines, comparisons, and synthesis.
3. Schema: rules for structure and operations. Usually `AGENTS.md`, with optional mirrors for agent-specific files.

## Practical Tradeoffs

- Start with plain files. Do not add vector search until `index.md` and `rg` stop being enough.
- Prefer one source at a time for careful research. Batch ingest is useful only when review quality can drop.
- Let high-value ingests include a short conversation with the user about emphasis, contradictions, and what should become durable.
- Keep citations close to claims, especially for facts likely to change or be disputed.
- Let contradictions remain visible. A wiki that preserves disagreement is more useful than one that prematurely harmonizes sources.
- Keep pages small enough to update safely. Split pages when the topic has clear subtopics or separate entities.
- Treat Obsidian or another markdown editor as the browsing/inspection layer: graph view, backlinks, frontmatter queries, and local attachments are optional but useful.
- Let answers take the shape they need: prose, tables, timelines, charts, slide markdown, canvas-style notes, or maintained wiki pages.

## Good Wiki Pages

- Have a clear title and stable purpose.
- Explain what is known, what is uncertain, and where evidence comes from.
- Link to related concepts, entities, source notes, and open questions.
- Include `last_updated` or an equivalent timestamp when the schema uses frontmatter.
- Are written for future agents and future humans, not just the current chat.
