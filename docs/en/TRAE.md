# Trae Installation

Trae support varies by version. Prefer native skills if your version exposes `.trae/skills`. Otherwise, use project rules and point them at this skill.

Enable this skill or project rule only inside LLM Wiki project directories.

## Project Skill Install

```bash
python scripts/install.py --target project-trae --project .
```

Equivalent manual install:

```bash
mkdir -p .trae/skills
cp -R /path/to/karmind-skill .trae/skills/karmind-skill
```

## Project Rules Fallback

Copy [adapters/trae_project_rules.md](../../adapters/trae_project_rules.md) into:

```text
.trae/rules/project_rules.md
```

Then keep this repository available in the project or install the skill under `.trae/skills/karmind-skill`.

## Usage

```text
Use the karmind-skill workflow to initialize this LLM wiki, ingest new sources, and maintain the default index and log.
```

```text
Use karmind-skill to run a health check.
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```
