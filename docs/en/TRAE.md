# Trae Installation

Use the combined “project rules + full skill” setup.

- `project_rules.md` tells Trae that this project is an LLM Wiki and that normal questions should start from the wiki.
- `.trae/skills/karmind-skill/` provides the full `SKILL.md`, references, and scripts.

This keeps the behavior scoped to the current project and avoids affecting ordinary code projects.

## Recommended: Combined Install

macOS / Linux:

```bash
git clone https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
python /tmp/karmind-skill/scripts/install.py --target project-trae --project .
```

Windows PowerShell:

```powershell
git clone https://github.com/Lhy723/karmind-skill.git "$env:TEMP\karmind-skill"
python "$env:TEMP\karmind-skill\scripts\install.py" --target project-trae --project .
```

After installation, the project contains:

```text
.trae/
├── rules/
│   └── project_rules.md
└── skills/
    └── karmind-skill/
        ├── SKILL.md
        ├── references/
        ├── scripts/
        └── adapters/
```

Meaning:

- `.trae/rules/project_rules.md` is the Trae project-rule entrypoint.
- `.trae/skills/karmind-skill/SKILL.md` is the full skill entrypoint.

## Manual Install Without Python

If you do not want to run the install script, do it manually.

macOS / Linux:

```bash
mkdir -p .trae/rules .trae/skills
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
git clone https://github.com/Lhy723/karmind-skill.git .trae/skills/karmind-skill
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force .trae/rules, .trae/skills
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md" `
  -OutFile ".trae/rules/project_rules.md"
git clone https://github.com/Lhy723/karmind-skill.git .trae/skills/karmind-skill
```

## Minimal Project Rules Only

For a minimal install, use only the project rule.

macOS / Linux:

```bash
mkdir -p .trae/rules
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force .trae/rules
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md" `
  -OutFile ".trae/rules/project_rules.md"
```

This works, but it relies on the shorter project rule instructions. The combined install is preferred because Trae can read the full `SKILL.md` when needed.

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

If you used the combined install, update the full skill:

```bash
git -C .trae/skills/karmind-skill pull
```

Update the project rule:

macOS / Linux:

```bash
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
```

Windows PowerShell:

```powershell
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md" `
  -OutFile ".trae/rules/project_rules.md"
```
