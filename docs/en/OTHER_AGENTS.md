# Other Agents

For agents without native Agent Skills support, use the repository instruction-file pattern.

Put these rules only in LLM Wiki project directories. Avoid global instructions so ordinary code projects do not trigger wiki maintenance behavior.

## AGENTS.md

Copy [adapters/AGENTS.md](../../adapters/AGENTS.md) into the root of the wiki project, then keep this skill repo accessible.

## CLAUDE.md

Copy [adapters/CLAUDE.md](../../adapters/CLAUDE.md) into projects where the agent reads `CLAUDE.md`.

## Generic Prompt

```text
Read SKILL.md in the karmind-skill repository. Follow it whenever I ask you to maintain the LLM wiki in the current directory. Treat raw/ as immutable sources, maintain wiki/index.md, append to wiki/log.md, cite sources, and preserve contradictions/open questions. Normal questions should start from the wiki by default. When fixing doctor findings, read wiki/reports/doctor-report.md, fix low-risk issues directly, and ask me before medium- or high-risk changes. When creating factual concept/entity pages, search local wiki/raw first; if evidence is insufficient and web access is available, browse/search authoritative sources and cite them instead of writing from memory.
```

## Recommended Project Layout

```text
project/
├── AGENTS.md
├── raw/
└── wiki/
```
