# OpenCode Installation

OpenCode supports native `.opencode/skills`, global `~/.config/opencode/skills`, and Claude/Agent-compatible skill directories.

Prefer lightweight project-level installation inside the LLM Wiki directory. Do not install globally by default, and do not copy the full repository into the wiki project.

## Minimal Install

Run this from the target wiki project:

macOS / Linux:

```bash
curl -sSL https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.sh | KARMIND_AGENT=opencode bash
```

Windows PowerShell:

```powershell
$env:KARMIND_AGENT = "opencode"; irm https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.ps1 | iex; Remove-Item Env:KARMIND_AGENT
```

## Recommended: Manual Project Install

This checks out only the lightweight skill files:

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
