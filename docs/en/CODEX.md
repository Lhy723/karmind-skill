# Codex Installation

Codex reads Agent Skills from `.agents/skills` in a repository and from `~/.agents/skills` for user-level skills.

Prefer project-level installation so this skill is enabled only in the LLM Wiki directory.

## Recommended: Project Install

If you use the install script, fetch this repository first.

macOS / Linux:

```bash
git clone https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
```

Windows PowerShell:

```powershell
git clone https://github.com/Lhy723/karmind-skill.git "$env:TEMP\karmind-skill"
```

Then run this from the target LLM Wiki project directory.

macOS / Linux:

```bash
python /tmp/karmind-skill/scripts/install.py --target project-agents --project .
```

Windows PowerShell:

```powershell
python "$env:TEMP\karmind-skill\scripts\install.py" --target project-agents --project .
```

Equivalent manual install.

macOS / Linux:

```bash
mkdir -p .agents/skills
cp -R /path/to/karmind-skill .agents/skills/karmind-skill
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force ".agents\skills"
Copy-Item -Recurse -Force "C:\path\to\karmind-skill" ".agents\skills\karmind-skill"
```

## Optional: User Install

Use this only when you intentionally want the skill available in every project.

macOS / Linux:

```bash
python /tmp/karmind-skill/scripts/install.py --target codex-user
```

Windows PowerShell:

```powershell
python "$env:TEMP\karmind-skill\scripts\install.py" --target codex-user
```

Equivalent manual install.

macOS / Linux:

```bash
mkdir -p ~/.agents/skills
cp -R /path/to/karmind-skill ~/.agents/skills/karmind-skill
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills"
Copy-Item -Recurse -Force "C:\path\to\karmind-skill" "$HOME\.agents\skills\karmind-skill"
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

If multiple pending raw files exist, the skill asks for the processing mode instead of silently processing only the first file.

Health check and repair:

```text
Use karmind-skill to run a health check.
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```
