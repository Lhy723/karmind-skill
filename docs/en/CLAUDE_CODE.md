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
/plugin marketplace add karmind-local <local-repo-path>
/plugin install karmind-skill@karmind-local
```

If the repository moves, replace the path with the new repository root.

### Sync the Plugin Distribution

`plugins/karmind-skill/` is a self-contained plugin directory built from root `SKILL.md`, `references/`, `scripts/`, and `adapters/`. This command is for developers.

macOS / Linux:

```bash
git clone https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
cd /tmp/karmind-skill
python scripts/build_claude_plugin.py
```

Windows PowerShell:

```powershell
git clone https://github.com/Lhy723/karmind-skill.git "$env:TEMP\karmind-skill"
Set-Location "$env:TEMP\karmind-skill"
python scripts/build_claude_plugin.py
```

## Fallback: Manual Install

Claude Code can also load skills from `~/.claude/skills/<skill-name>/SKILL.md` and project-local `.claude/skills/<skill-name>/SKILL.md`.

Prefer lightweight project-level installation inside the LLM Wiki directory.

### Recommended: One-Command Install

Run this from the target wiki project:

macOS / Linux:

```bash
curl -sSL https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.sh | KARMIND_AGENT=claude bash
```

Windows PowerShell:

```powershell
$env:KARMIND_AGENT = "claude"; irm https://raw.githubusercontent.com/Lhy723/karmind-skill/main/scripts/install.ps1 | iex; Remove-Item Env:KARMIND_AGENT
```

### Project Install

macOS / Linux:

```bash
mkdir -p .claude/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git .claude/skills/karmind-skill
git -C .claude/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force ".claude\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ".claude\skills\karmind-skill"
git -C ".claude\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts
```

### User Install

Use this only when you intentionally want the skill available in every Claude Code project.

macOS / Linux:

```bash
mkdir -p ~/.claude/skills
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git ~/.claude/skills/karmind-skill
git -C ~/.claude/skills/karmind-skill sparse-checkout set --no-cone /SKILL.md /references /scripts
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lhy723/karmind-skill.git "$HOME\.claude\skills\karmind-skill"
git -C "$HOME\.claude\skills\karmind-skill" sparse-checkout set --no-cone /SKILL.md /references /scripts
```

## Update

Project-level install:

```bash
git -C .claude/skills/karmind-skill pull --ff-only
```

User-level install:

```bash
git -C ~/.claude/skills/karmind-skill pull --ff-only
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

If multiple pending raw files exist, the skill asks for the processing mode instead of silently processing only the first file.

Health check and repair:

```text
Use karmind-skill to run a health check.
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```

If the directory did not exist when Claude Code started, restart Claude Code.
