# OpenCode Installation

OpenCode supports native `.opencode/skills`, global `~/.config/opencode/skills`, and Claude/Agent-compatible skill directories.

Prefer project-level installation inside the LLM Wiki directory.

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
python /tmp/karmind-skill/scripts/install.py --target project-opencode --project .
```

Windows PowerShell:

```powershell
python "$env:TEMP\karmind-skill\scripts\install.py" --target project-opencode --project .
```

## Optional: User Install

Use this only when you intentionally want the skill available in every OpenCode project.

macOS / Linux:

```bash
python /tmp/karmind-skill/scripts/install.py --target opencode-user
```

Windows PowerShell:

```powershell
python "$env:TEMP\karmind-skill\scripts\install.py" --target opencode-user
```

Equivalent manual install.

macOS / Linux:

```bash
mkdir -p ~/.config/opencode/skills
cp -R /path/to/karmind-skill ~/.config/opencode/skills/karmind-skill
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.config\opencode\skills"
Copy-Item -Recurse -Force "C:\path\to\karmind-skill" "$HOME\.config\opencode\skills\karmind-skill"
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

## Usage

```text
Use karmind-skill to run a health check.
```

When ingesting new sources, if multiple pending raw files exist, the skill asks for the processing mode instead of silently processing only the first file.

```text
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```
