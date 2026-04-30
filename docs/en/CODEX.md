# Codex Installation

Codex reads Agent Skills from `.agents/skills` in a repository and from `~/.agents/skills` for user-level skills.

Prefer project-level installation so this skill is enabled only in the LLM Wiki directory.

## Recommended: Project Install

```bash
python scripts/install.py --target project-agents --project .
```

Equivalent manual install:

```bash
mkdir -p .agents/skills
cp -R /path/to/karmind-skill .agents/skills/karmind-skill
```

## Optional: User Install

Use this only when you intentionally want the skill available in every project.

```bash
python scripts/install.py --target codex-user
```

Equivalent manual install:

```bash
mkdir -p ~/.agents/skills
cp -R /path/to/karmind-skill ~/.agents/skills/karmind-skill
```

Restart Codex if the skill does not appear.

## Usage

```text
$karmind-skill initialize the current directory as an LLM Wiki
```

or:

```text
Use karmind-skill to ingest new sources.
```

Health check and repair:

```text
Use karmind-skill to run a health check.
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```
