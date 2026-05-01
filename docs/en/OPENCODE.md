# OpenCode Installation

OpenCode supports native `.opencode/skills`, global `~/.config/opencode/skills`, and Claude/Agent-compatible skill directories.

Prefer project-level installation inside the LLM Wiki directory.

## Recommended: Project Install

If you use the install script, fetch this repository first:

```bash
git clone https://github.com/Lhy723/karmind-skill.git /tmp/karmind-skill
```

Then run this from the target LLM Wiki project directory:

```bash
python /tmp/karmind-skill/scripts/install.py --target project-opencode --project .
```

## Optional: User Install

Use this only when you intentionally want the skill available in every OpenCode project.

```bash
python /tmp/karmind-skill/scripts/install.py --target opencode-user
```

Equivalent manual install:

```bash
mkdir -p ~/.config/opencode/skills
cp -R /path/to/karmind-skill ~/.config/opencode/skills/karmind-skill
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

```text
Use karmind-skill to fix issues from the latest health report. Do not delete pages; ask me before merging, splitting, or renaming pages.
```
