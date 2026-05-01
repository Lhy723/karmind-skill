# OpenCode Installation

OpenCode supports native `.opencode/skills`, global `~/.config/opencode/skills`, and Claude/Agent-compatible skill directories.

Prefer lightweight project-level installation inside the LLM Wiki directory. Do not install globally by default, and do not copy the full repository into the wiki project.

## Recommended: No-Python Project Install

This checks out only the files needed at runtime:

- `SKILL.md`
- `references/`
- `scripts/`

macOS / Linux:

```bash
mkdir -p .opencode/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git .opencode/skills/karmind-skill
git -C .opencode/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force ".opencode\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ".opencode\skills\karmind-skill"
git -C ".opencode\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts
```

After installation, the project contains:

```text
.opencode/
└── skills/
    └── karmind-skill/
        ├── SKILL.md
        ├── references/
        └── scripts/
```

If you previously copied the full repository, delete the old directory and reinstall with the commands above.

macOS / Linux:

```bash
rm -rf .opencode/skills/karmind-skill
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force ".opencode\skills\karmind-skill"
```

## Fallback: Python Script Install

If you already have Python and want the installer to create the directories, first fetch this repository, then run the script. This path now also copies only the lightweight runtime skill files.

macOS / Linux:

```bash
git clone --depth 1 https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
python /tmp/karmind-skill/scripts/install.py --target project-opencode --project .
```

Windows PowerShell:

```powershell
git clone --depth 1 https://github.com/Lhy723/karmind-skill.git "$env:TEMP\karmind-skill"
python "$env:TEMP\karmind-skill\scripts\install.py" --target project-opencode --project .
```

## Optional: User Install

Use this only when you intentionally want the skill available in every OpenCode project.

macOS / Linux:

```bash
mkdir -p ~/.config/opencode/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ~/.config/opencode/skills/karmind-skill
git -C ~/.config/opencode/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.config\opencode\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git "$HOME\.config\opencode\skills\karmind-skill"
git -C "$HOME\.config\opencode\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts
```

## Permissions

If your OpenCode config restricts skills, allow this skill:

```json
{
  "permission": {
    "skill": {
      "karmind-skill": "allow"
    }
  }
}
```

## Update

Project-level install:

```bash
git -C .opencode/skills/karmind-skill pull --ff-only
```

User-level install:

```bash
git -C ~/.config/opencode/skills/karmind-skill pull --ff-only
```

## Usage

```text
Use karmind-skill to run a health check.
```

When ingesting new sources, if multiple pending raw files exist, the skill asks for the processing mode instead of silently processing only the first file.

```text
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```
