# Trae Installation

Trae project rules are the most stable path, so start with a project rule file. This scopes `karmind-skill` to the current LLM Wiki project and avoids affecting unrelated projects.

## Recommended: Project Rules

Run this from your LLM Wiki project root:

```bash
mkdir -p .trae/rules
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
```

After installation, the project should contain:

```text
.trae/rules/project_rules.md
```

Open the project in Trae and say:

```text
Use karmind-skill to initialize an LLM Wiki in the current directory.
```

or:

```text
Use karmind-skill to ingest new sources.
```

## Optional: Full Skill Files

If your Trae version can read `.trae/skills/`, place the full repository inside the project:

```bash
mkdir -p .trae/skills
git clone https://github.com/Lhy723/karmind-skill.git .trae/skills/karmind-skill
```

After installation, the project should contain:

```text
.trae/skills/karmind-skill/SKILL.md
```

If Trae does not automatically read this directory, keep the project rule file from the recommended setup. The rule tells Trae to read `karmind-skill`'s `SKILL.md` when wiki maintenance is needed.

## Suggested Layout

Recommended final layout:

```text
your-wiki-project/
├── .trae/
│   ├── rules/
│   │   └── project_rules.md
│   └── skills/
│       └── karmind-skill/
│           └── SKILL.md
├── raw/
└── wiki/
```

If you only use project rules, `.trae/skills/` can be absent.

## Common Prompts

```text
Use karmind-skill to initialize an LLM Wiki in the current directory. First scan for existing notes or documents, list candidates, and ask whether to move, copy, or skip them.
```

```text
Use karmind-skill to ingest new sources. Find pending material from the default directories, create source notes, update related pages, and maintain the index, log, and cache.
```

```text
Use karmind-skill to run a health check.
```

```text
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```

## Update

If you installed `.trae/skills/karmind-skill`, update it with:

```bash
git -C .trae/skills/karmind-skill pull
```

If you only use the project rule, download the rule file again:

```bash
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
```
