# Claude Code Installation

Prefer Claude Code plugin marketplace installation. Plugin installation can carry the skill, scripts, and future extension configuration together, which is better for long-term maintenance than copying a skill folder by hand.

Enable this plugin/skill only inside LLM Wiki project directories when possible. Global enablement is not recommended by default.

The repository root contains the files required by Claude Code plugin marketplace installation:

```text
.claude-plugin/marketplace.json
plugins/karmind-skill/.claude-plugin/plugin.json
plugins/karmind-skill/skills/karmind-skill/SKILL.md
```

## Recommended: Plugin Install

Install from GitHub:

```text
/plugin marketplace add karmind-skills Lhy723/karmind-skill
/plugin install karmind-skill@karmind-skills
```

With a full GitHub URL:

```text
/plugin marketplace add karmind-skills https://github.com/Lhy723/karmind-skill
/plugin install karmind-skill@karmind-skills
```

Local development install:

```text
/plugin marketplace add karmind-local /path/to/karmind-skill
/plugin install karmind-skill@karmind-local
```

If the repository moves, replace the path with the new repository root.

### Sync the Plugin Distribution

`plugins/karmind-skill/` is a self-contained plugin directory built from root `SKILL.md`, `references/`, `scripts/`, and `adapters/`. After changing those source files, run:

```bash
python scripts/build_claude_plugin.py
```

## Manual Install

Claude Code can also load skills from `~/.claude/skills/<skill-name>/SKILL.md` and project-local `.claude/skills/<skill-name>/SKILL.md`.

### User Install

```bash
python scripts/install.py --target claude-user
```

Equivalent manual install:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/karmind-skill ~/.claude/skills/karmind-skill
```

### Project Install

```bash
python scripts/install.py --target project-claude --project .
```

## Usage

Invoke directly:

```text
/karmind-skill ingest new sources
```

Or describe the task naturally:

```text
Please maintain the LLM wiki in the current directory and process new sources.
```

Health check and repair:

```text
Use karmind-skill to run a health check.
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```

If the directory did not exist when Claude Code started, restart Claude Code.
