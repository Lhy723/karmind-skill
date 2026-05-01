# Security Notes

This skill is intentionally local-first and uses only Python standard library helper scripts.

Review before enabling any third-party skill:

- `SKILL.md`
- scripts under `scripts/`
- lightweight skill files in the agent install directory
- agent-specific rule files

For sensitive wikis:

- Keep private raw sources out of public repositories.
- Redact secrets before ingestion.
- Store model API keys in environment variables or local `.env.local`, not in wiki pages, logs, or reports.
- Avoid pasting confidential source material into hosted agents unless approved.
- Use local-only agents or controlled workspaces for sensitive research.
- Treat generated wiki claims as drafts until reviewed.

See [MODEL_KEYS.md](MODEL_KEYS.md) for details.
