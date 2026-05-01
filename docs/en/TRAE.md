# Trae Installation

Use the combined “project rules + lightweight skill” setup inside the wiki project directory. Prefer the no-Python install path.

- `project_rules.md` tells Trae that this project is an LLM Wiki and that normal questions should start from the wiki.
- `.trae/skills/karmind-skill/` contains only the skill files Trae needs to read: `SKILL.md`, `references/`, and `scripts/`.
- The install uses Git sparse checkout, so README files, docs, adapters, tests, and other repository files are not checked out into the project.

This keeps the behavior scoped to the current project and avoids affecting ordinary code projects.

## Recommended: No-Python Combined Install

macOS / Linux:

```bash
mkdir -p .trae/rules .trae/skills
curl -L https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md \
  -o .trae/rules/project_rules.md
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git .trae/skills/karmind-skill
git -C .trae/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force ".trae\rules", ".trae\skills"
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md" `
  -OutFile ".trae\rules\project_rules.md"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ".trae\skills\karmind-skill"
git -C ".trae\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts
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
        └── scripts/
```

Meaning:

- `.trae/rules/project_rules.md` is the Trae project-rule entrypoint.
- `.trae/skills/karmind-skill/SKILL.md` is the skill workflow entrypoint.
- `adapters/AGENTS.md` in this repository is for generic agents. Trae does not need it. The recommended install does not place `adapters/` inside `.trae/skills/karmind-skill/`, so it cannot be confused with `.trae/rules/project_rules.md`.

If you previously followed the old full-clone instructions, delete the old skill directory and reinstall:

```bash
rm -rf .trae/skills/karmind-skill
```

PowerShell:

```powershell
Remove-Item -Recurse -Force ".trae\skills\karmind-skill"
```

## Fallback: Python Script Install

If you already have Python and want the installer to create the directories, first fetch the repository that contains the script, then run it. This path now also copies only the lightweight Trae skill into the project directory.

macOS / Linux:

```bash
git clone --depth 1 https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
python /tmp/karmind-skill/scripts/install.py --target project-trae --project .
```

Windows PowerShell:

```powershell
git clone --depth 1 https://github.com/Lhy723/karmind-skill.git "$env:TEMP\karmind-skill"
python "$env:TEMP\karmind-skill\scripts\install.py" --target project-trae --project .
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
New-Item -ItemType Directory -Force ".trae\rules"
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/Lhy723/karmind-skill/main/adapters/trae_project_rules.md" `
  -OutFile ".trae\rules\project_rules.md"
```

This works, but it relies on the shorter project rule instructions. The combined install is preferred because Trae can read the full `SKILL.md` when needed.

## Common Prompts

```text
Use karmind-skill to initialize an LLM Wiki in the current directory. First scan for existing notes or documents, list candidates, and ask whether to move, copy, or skip them.
```

```text
Use karmind-skill to ingest new sources. Find pending material from the default directories, create source notes, update related pages, and maintain the index, log, and cache.
```

If multiple pending raw files exist, the skill should ask whether to use external-model batch processing, a manual agent loop, next file only, or defer.

```text
Use karmind-skill to run a health check.
```

```text
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```

## Update

If you used the recommended combined install, update the lightweight skill:

```bash
git -C .trae/skills/karmind-skill pull --ff-only
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
  -OutFile ".trae\rules\project_rules.md"
```
