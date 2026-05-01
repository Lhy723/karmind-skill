# Agent Adapter Reference

Use this when installing or adapting `karmind-skill` across coding agents.

## Portable Skill Locations

Common locations:

- Codex user skill: `~/.agents/skills/karmind-skill/SKILL.md`
- Codex repo skill: `.agents/skills/karmind-skill/SKILL.md`
- Claude Code user skill: `~/.claude/skills/karmind-skill/SKILL.md`
- Claude Code repo skill: `.claude/skills/karmind-skill/SKILL.md`
- OpenCode native user skill: `~/.config/opencode/skills/karmind-skill/SKILL.md`
- OpenCode repo skill: `.opencode/skills/karmind-skill/SKILL.md`
- Trae combined project install: `.trae/rules/project_rules.md` plus `.trae/skills/karmind-skill/SKILL.md`
- Generic agent skill: `.agents/skills/karmind-skill/SKILL.md`

When an agent has no skill loader, put the wiki operating instructions in `AGENTS.md` and link to this repository.

## Adapter Strategy

1. Prefer native Agent Skills support when available.
2. If unavailable, install this repo as plain markdown instructions and add a short rule file that says when to read `SKILL.md`.
3. Keep one canonical skill folder. Use symlinks only when the platform follows them reliably.
4. Keep tool-specific config minimal. The workflow should remain portable.

## Rule File Snippet

Use this in `AGENTS.md`, `CLAUDE.md`, Trae rules, or other agent instructions:

```markdown
When the task involves maintaining the LLM wiki, read and follow the `karmind-skill` instructions. Treat `raw/` as immutable source evidence. Maintain `wiki/index.md` and append to `wiki/log.md` after ingest, query filing, or lint work. Preserve citations, cross-links, contradictions, and open questions.
Maintain `wiki/cache/ingest-cache.json` so processed raw files are skipped unless forced re-extraction is requested. When initializing a wiki, scan for existing notes/documents and ask before moving or copying them into `raw/imported/`.
Normal questions in this directory are wiki-grounded by default. When fixing health-check findings, read `wiki/reports/doctor-report.md`, fix low-risk issues directly, ask before merges/splits/renames, and require approval before deletion, source-note overwrite, cache reset, batch re-ingest, or schema changes.
```
