# Codex Installation

Codex reads Agent Skills from `.agents/skills` in a repository and from `~/.agents/skills` for user-level skills.

Prefer lightweight project-level installation inside the LLM Wiki directory. Do not install globally by default, and do not copy the full repository into the wiki project.

## Minimal Install

Run this from the target wiki project:

macOS / Linux:

```bash
curl -sSL https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.ps1 | iex
```

Choose `Codex / generic agents` when prompted. Non-interactive runs default to `.agents/skills/karmind-skill`.

## Recommended: Manual Project Install

This checks out only the lightweight skill files:

- `SKILL.md`
- `references/`
- `scripts/`
- `agents/`, for Codex skill metadata

macOS / Linux:

```bash
mkdir -p .agents/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git .agents/skills/karmind-skill
git -C .agents/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts /agents
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force ".agents\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ".agents\skills\karmind-skill"
git -C ".agents\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts /agents
```

After installation, the project contains:

```text
.agents/
└── skills/
    └── karmind-skill/
        ├── SKILL.md
        ├── agents/
        ├── references/
        └── scripts/
```

If you previously copied the full repository, delete the old directory and reinstall with the commands above.

macOS / Linux:

```bash
rm -rf .agents/skills/karmind-skill
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force ".agents\skills\karmind-skill"
```

## Optional: User Install

Use this only when you intentionally want the skill available in every project.

macOS / Linux:

```bash
mkdir -p ~/.agents/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ~/.agents/skills/karmind-skill
git -C ~/.agents/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts /agents
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git "$HOME\.agents\skills\karmind-skill"
git -C "$HOME\.agents\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts /agents
```

Restart Codex if the skill does not appear.

## Update

Project-level install:

```bash
git -C .agents/skills/karmind-skill pull --ff-only
```

User-level install:

```bash
git -C ~/.agents/skills/karmind-skill pull --ff-only
```

## Usage

```text
$karmind-skill initialize the current directory as an LLM Wiki
```

or:

```text
Use karmind-skill to ingest new sources.
```

If multiple pending raw files exist, the skill asks for the processing mode instead of silently processing only the first file.

Health check and repair:

```text
Use karmind-skill to run a health check.
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```
